"""Execution substrate.

The benchmark runs the same commands in two environments:

* the VPS, where there is no host PHP - everything happens inside a long-lived
  Docker container with the repository mounted at /bench;
* a GitHub runner, where PHP is installed natively.

Both are addressed through one interface. Argv paths are given as host paths and
translated with ``runtime_path`` so callers never have to care which mode is
active.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTAINER_MOUNT = "/bench"


class RunnerError(RuntimeError):
    pass


class Runner:
    def __init__(self, mode: str | None = None, image: str | None = None,
                 container: str | None = None, php_version: str | None = None):
        requested = mode or os.environ.get("BENCH_PHP", "auto")
        self.php_series = php_version
        self.image = image or os.environ.get("BENCH_PHP_IMAGE") or ""
        if not self.image:
            self.image = f"php:{php_version or '8.3'}-cli"
        self.container = container or os.environ.get("BENCH_CONTAINER") or self._default_container()
        self.mode = self._resolve(requested)

    def _default_container(self) -> str:
        """Container name unique per repository root.

        Several checkouts of this repository (worktrees of the autonomous
        factory) run in parallel, and a container is only usable for the tree it
        was started with: the mount is fixed at creation time. A shared name
        would silently run analyzers against the wrong files, so the root path is
        part of the name.
        """
        import hashlib
        digest = hashlib.sha1(ROOT.encode()).hexdigest()[:8]
        return f"bench-{self.image.replace(':', '-')}-{digest}"

    def _resolve(self, requested: str) -> str:
        if requested == "native":
            return "native"
        if requested == "docker":
            return "docker"
        # auto: prefer Docker when it is usable, otherwise fall back to a host PHP.
        if shutil.which("docker") and self._docker_ok():
            return "docker"
        if shutil.which("php"):
            return "native"
        raise RunnerError("neither Docker nor a host PHP is available")

    @staticmethod
    def _docker_ok() -> bool:
        try:
            proc = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, timeout=30)
            return proc.returncode == 0
        except Exception:
            return False

    # -- environment -----------------------------------------------------

    def ensure(self) -> None:
        if self.mode != "docker":
            return
        state = subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", self.container],
                               capture_output=True, text=True)
        if state.returncode != 0:
            subprocess.run([
                "docker", "run", "-d", "--name", self.container,
                "--label", f"bench.root={ROOT}",
                "--user", f"{os.getuid()}:{os.getgid()}",
                "-e", "HOME=/tmp",
                "-v", f"{ROOT}:{CONTAINER_MOUNT}", "-w", CONTAINER_MOUNT,
                self.image, "sleep", "infinity",
            ], check=True, capture_output=True, text=True)
        elif state.stdout.strip() != "true":
            subprocess.run(["docker", "start", self.container], check=True, capture_output=True, text=True)

    def image_available(self) -> bool:
        if self.mode != "docker":
            return True
        proc = subprocess.run(["docker", "image", "inspect", self.image],
                              capture_output=True, text=True)
        return proc.returncode == 0

    def php_version(self) -> str:
        result = self.exec(self._php_argv(["-r", "echo PHP_VERSION;"]), cwd=ROOT, timeout=60)
        return result["stdout"].strip() if result["exit_code"] == 0 else "unknown"

    # -- path helpers ----------------------------------------------------

    def runtime_path(self, host_path: str) -> str:
        """Translate a host path into the path the analyzer has to be given."""
        if not host_path.startswith("/"):
            return host_path
        if self.mode == "docker":
            if host_path == ROOT:
                return CONTAINER_MOUNT
            if host_path.startswith(ROOT + "/"):
                return CONTAINER_MOUNT + host_path[len(ROOT):]
            raise RunnerError(f"{host_path} is outside the mounted repository")
        return host_path

    def runtime_cwd(self, host_dir: str) -> str:
        return self.runtime_path(host_dir)

    # -- execution -------------------------------------------------------

    def exec(self, argv: list[str], cwd: str, timeout: int = 300,
             env: dict | None = None) -> dict:
        if self.mode == "docker":
            self.ensure()
            cmd = ["docker", "exec", "-u", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp"]
            for key, value in (env or {}).items():
                cmd += ["-e", f"{key}={value}"]
            cmd += ["-w", self.runtime_cwd(cwd), self.container] + argv
        else:
            cmd = argv
        started = time.time()
        try:
            proc = subprocess.run(cmd, cwd=(cwd if self.mode == "native" else None),
                                  capture_output=True, text=True, timeout=timeout,
                                  env={**os.environ, **(env or {})})
            code, out, err = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            code = 124
            out = (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            err = (exc.stderr or b"").decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            err += f"\n[runner] timeout after {timeout}s"
        return {
            "exit_code": code,
            "stdout": out,
            "stderr": err,
            "duration_s": round(time.time() - started, 3),
            "argv": argv,
            "cwd": cwd,
        }

    def php(self, args: list[str], cwd: str, timeout: int = 300, env: dict | None = None) -> dict:
        """Run the PHP interpreter with the given arguments."""
        return self.exec(self._php_argv(args), cwd=cwd, timeout=timeout, env=env)

    def _php_argv(self, args: list[str]) -> list[str]:
        if self.mode == "docker":
            return ["php"] + args
        php = shutil.which("php")
        if not php:
            raise RunnerError("no host PHP found; run with BENCH_PHP=docker")
        return [php] + args
