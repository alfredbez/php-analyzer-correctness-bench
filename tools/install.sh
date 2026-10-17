#!/usr/bin/env bash
# Install the pinned analyzer versions into tools/bin/.
# Idempotent: a tool that already matches the pinned version is left alone.
#
#   ./tools/install.sh            install the versions pinned in tools/versions.json
#   ./tools/install.sh --latest    install the current stable releases instead and
#                                  write the resolved versions to
#                                  tools/versions.resolved.json (used by the
#                                  nightly drift job, not by the pinned runs)
set -euo pipefail

MODE="pinned"
[ "${1:-}" = "--latest" ] && MODE="latest"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="$ROOT/tools/bin"
mkdir -p "$BIN_DIR"

read_version() { python3 -c "import json;print(json.load(open('$ROOT/tools/versions.json'))['tools']['$1']['version'])"; }
read_url()     { python3 -c "import json;print(json.load(open('$ROOT/tools/versions.json'))['tools']['$1']['url'])"; }
read_upstream(){ python3 -c "import json;print(json.load(open('$ROOT/tools/versions.json'))['tools']['$1']['upstream'])"; }

latest_version() { # upstream repo -> newest release tag without the leading v
  curl --fail --silent --show-error --location \
    "https://api.github.com/repos/$(read_upstream "$1")/releases/latest" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['tag_name'].lstrip('v'))"
}

want() { # name -> version to install
  if [ "$MODE" = "latest" ]; then
    latest_version "$1"
  else
    read_version "$1"
  fi
}

fetch() { # url dest
  local url="$1" dest="$2"
  echo "    GET $url"
  curl --fail --location --silent --show-error --retry 3 --output "$dest.tmp" "$url"
  mv "$dest.tmp" "$dest"
}

install_phar() { # name, version-check-command
  local name="$1" version
  version="$(want "$name")"
  local dest="$BIN_DIR/$name.phar"
  if [ -f "$dest" ] && php_ok "$name" "$dest" "$version"; then
    echo "  [=] $name $version already installed"
    return 0
  fi
  echo "  [+] $name $version"
  local url
  url="$(read_url "$name" | sed "s/{version}/$version/g")"
  fetch "$url" "$dest"
  chmod +x "$dest"
}

# Version probe. Runs through the same PHP runner the harness uses, so the check
# is meaningful in Docker and on a bare runner alike.
php_ok() { # name dest version
  local name="$1" dest="$2" version="$3" out
  out="$("$ROOT/harness/php" "$dest" --version 2>/dev/null || true)"
  case "$name" in
    phpstan) printf '%s' "$out" | grep -q "$version" ;;
    psalm)   printf '%s' "$out" | grep -q "$version" ;;
    *)       return 1 ;;
  esac
}

echo "Installing pinned analyzers into tools/bin/"

for name in phpstan psalm; do
  install_phar "$name"
done

# Mago ships as a static binary in a tarball.
MAGO_VERSION="$(want mago)"
MAGO_DEST="$BIN_DIR/mago"
if [ -x "$MAGO_DEST" ] && "$MAGO_DEST" --version 2>/dev/null | grep -q "$MAGO_VERSION"; then
  echo "  [=] mago $MAGO_VERSION already installed"
else
  echo "  [+] mago $MAGO_VERSION"
  TMP="$(mktemp -d)"
  fetch "$(read_url mago | sed "s/{version}/$MAGO_VERSION/g")" "$TMP/mago.tar.gz"
  tar -xzf "$TMP/mago.tar.gz" -C "$TMP"
  found="$(find "$TMP" -type f -name mago -perm -u+x | head -1)"
  [ -n "$found" ] || { echo "    mago binary not found in archive" >&2; exit 1; }
  mv "$found" "$MAGO_DEST"
  chmod +x "$MAGO_DEST"
  rm -rf "$TMP"
fi

echo "Done. Installed:"
printf '  %s\n' "$(ls -1 "$BIN_DIR")"

if [ "$MODE" = "latest" ]; then
  python3 - "$ROOT" <<'PY'
import json
import os
import subprocess
import sys

root = sys.argv[1]
pins = json.load(open(os.path.join(root, "tools/versions.json")))
resolved = {"_comment": "Resolved by tools/install.sh --latest during a drift run.",
            "resolved_at": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                                          capture_output=True, text=True).stdout.strip(),
            "tools": {}}
commands = {
    "phpstan": ["php", "tools/bin/phpstan.phar", "--version"],
    "psalm": ["php", "tools/bin/psalm.phar", "--version"],
    "mago": ["tools/bin/mago", "--version"],
}
for name in pins["tools"]:
    resolved["tools"][name] = {"pinned": pins["tools"][name]["version"]}
    binary = os.path.join(root, commands[name][0])
    if not os.path.exists(binary):  # php is not in tools/bin
        command = [commands[name][0]] + [os.path.join(root, part) for part in commands[name][1:]]
        if command[0] == "php":
            command = [os.environ.get("BENCH_PHP_EXECUTABLE", "php")] + command[1:]
        out = subprocess.run(command, capture_output=True, text=True)
        resolved["tools"][name]["reported"] = (out.stdout or out.stderr).strip().splitlines()[0]
with open(os.path.join(root, "tools/versions.resolved.json"), "w") as handle:
    json.dump(resolved, handle, indent=2)
print(json.dumps(resolved, indent=2))
PY
fi
