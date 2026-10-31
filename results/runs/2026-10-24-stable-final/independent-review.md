All verification is complete. Here is the independent review report.

# Independent Review — 2026-10-24 batch & Pzoom lane

**Verdict: ACCEPT — CORE batch** (2 cases, catalog/assessment expansion, harvest gate, factory skip change). **Pzoom: ACCEPT as opt-in, fail-closed experiment — explicitly NOT ready to score**, which matches the docs' own claim. No correctness blockers found; two process/documentation findings below.

## What I executed (all read-only / `--no-save`)

| Command | Result |
|---|---|
| `BENCH_PHP_IMAGE=php:8.4-cli harness/php cases/…/catalog-psalm-2ed1be42908ccc536dd5/runtime/check.php` | exit 0 |
| `BENCH_PHP_IMAGE=php:8.4-cli harness/php cases/…/catalog-phpstan-da61ed3a1be4f5592a03/runtime/check.php` | exit 0 |
| `python3 harness/bench.py run --php 8.4 --no-save --case <both> --tool phpstan --tool psalm --tool mago --tool pzoom` | phpstan ok/ok, psalm ok/ok, mago false_negative+ok, pzoom tool_error×2 — **identical to recorded raw** |
| same with default tools (no `--tool`) | pzoom correctly excluded |
| `python3 harness/bench.py validate` | 144 cases, 0 invalid |
| `python3 -m unittest discover -s tests -t . -q` | 53 tests OK |
| `python3 factory/catalog.py check` | OK: 122 outcomes (114 measured, 7 covered, 1 deferred) |
| `python3 factory/catalog.py check --inventory results/harvest/2026-10-24/catalog.json --assessment …/assessment.json` | **exit 1, `unfinished candidate assessment: psalm:0258f917…`** — pending gate works as designed |
| `python3 harness/bench.py audit --report …/2026-10-24-new-batch-final/report.json` | exit 1 (2 pzoom tool errors + empty denominator) — intentional fail-closed evidence |
| `python3 harness/bench.py audit --report …/2026-10-24-stable-final/report.json` (read-only peek; run finished separately) | exit 0, 144 cases, phpstan/psalm/mago only, new-case verdicts match |

## Ground truth & novelty (verified, not trusted)

- **Bitwise case**: `~true`/`~false` throw `TypeError("Cannot perform bitwise not…")`; int/string controls pass at runtime. Required diagnostic at `src/probe.php:5` is the actual operator line. Psalm expectation is grounded in the cited upstream test (`BinaryOperationTest.php:1340` = `invalidBooleanBitwiseNot`, confirmed present at pinned ref).
- **Readonly case**: runtime proves two-object independent init, same-value *and* changed-value writes throw `Error("Cannot modify readonly property…")`, state preserved. Error line 12 correct. Upstream lead confirmed at `readonly-assign.php:19–22`.
- **Novelty**: grep + full enumeration of all 122 assessment entries and 144 case manifests — no existing criterion covers unary-complement operand validity or readonly write-once state. Nearest neighbors (`assignability/asymmetric-property-override`, boolean-guard narrowing criteria, `magic-property-contract`) are genuinely distinct, as claimed. Harness criterion count convention (id fallback) reproduces the doc's 127→129 exactly.
- **Preservation**: all 120 prior `catalog.json` records byte-identical (2 new prepended), all prior assessment entries identical, `target_criteria`/`sources` unchanged.
- **Harvest**: 202 = 122 + 80 fresh (40 psalm/40 phpstan), all IDs unique, zero probe-hash overlap with main or within fresh, **all 202 source_sha256 re-verified against local checkouts** at pinned refs (psalm `62e52cd…`, phpstan `2c12dac…`, both clean). All 80 pending have empty `case_ids`/`criterion_ids`/`semantic_statement` — none promoted or claimed reviewed.
- **Pzoom pin**: `.tools-alt/pzoom-source` clean at `c8162978…`; lock file identical to `tools/pzoom-Cargo.lock` and receipt `lock_sha256`; binary matches receipt; `pzoom.LICENSE` (MIT, Matt Brown) retained. Claims in docs verified in source: `--format` field declared but never read (`crates/pzoom-cli/src/main.rs:32-34`), only `stubs/extensions/optional/` configurable, invalid literal confirmed at `stubs/extensions/sockets.phpstub:419` (`const SKF_AD_OFF = -096;`). The two cases' pzoom expectations are **not inferred from Psalm** — pzoom's own partial stdout shows `InvalidOperand …:5:12` and `InaccessibleProperty …:12:9`, and `classify.py` guarantees `tool_error` precedence so they can never silently pass.

## Findings (non-blocking)

1. **`tools/versions.json` edited inside a non-version-bump task** (psalm 6.20.0→6.20.1, mago 1.57.0→1.58.2). AGENT-PROTOCOL.md: "Never edit tools/versions.json outside an explicit version-bump task." Installed binaries do match the new pins (run meta proves it) and the pilot doc discloses the refresh, so no measurement corruption — but this is a protocol deviation Alfred should ratify or revert.
2. **`history_ledger_sha256` is stale** (pre-existing, not this diff): catalog records `0ccca55b…` but live `mago/COORDINATION.json` hashes to `82277003…`. Same value at HEAD, so untouched by this change; `expand` preserves it verbatim.
3. **Nit**: `GAPS-pzoom.md` says "matched every case it was judged against" over 0 judged + 2 tool errors — vacuously true; audit catches it, but the sentence reads as success.
4. **Note**: `docs/local-pilot-2026-10-24.md` (referenced by README) is untracked, mode 600 — must be `git add`ed for the README reference to survive a commit. New-case `.generated/psalm.xml` files are properly gitignored.

## SHA256 receipt (bytes as reviewed)

New case files:
- `87f04b30…f4` cases/assignability/catalog-psalm-2ed1be42908ccc536dd5/case.json
- `ecd9457a…09` …/composer.json
- `4ea40257…08` …/src/probe.php
- `dc6e4133…eb8` …/runtime/check.php
- `914cd26e…f3` cases/assignability/catalog-phpstan-da61ed3a1be4f5592a03/case.json
- `f131fcff…80` …/composer.json
- `9f978ecb…80` …/src/probe.php
- `1527accd…0c` …/runtime/check.php

Changed Python / config / pins:
- `925f8fa4…19` factory/catalog.py · `08b925ac…10` factory/bench_factory.py
- `709e7edf…1d` factory/catalog.json · `32eb8e0f…fc` factory/assessment.json
- `7cbe79bd…4d` harness/bench.py · `f8c21270…2f` harness/bench/adapters.py
- `1babd8cb…c7` harness/bench/case.py · `a11dd8ae…36` harness/bench/classify.py · `a2dab31f…66` harness/bench/execute.py
- `892e5029…d4` tools/install-pzoom.py · `b3914962…6a` tools/pzoom-Cargo.lock (= source Cargo.lock = receipt `lock_sha256`)
- `24fe29b6…3f` tools/versions.json
- `7ab02cee…f6` tests/test_catalog.py · `9bb10c2c…b7` tests/test_factory.py · `cd3ee1bf…51` tests/test_harness.py · `60159aa1…82` tests/fixtures/pzoom-stub-scan-error.json
- Pzoom binary: `961f57c6…da` (= `tools/bin/pzoom.provenance.json` and `results/runs/2026-10-24-new-batch-final/pzoom-provenance.json`), ref `c8162978033745e585f8e60d15a66a48862333cc`, rustc 1.99.1

I did not modify, commit, or push anything, did not touch `results/runs/2026-10-24-stable-final`, and contacted no upstream.
