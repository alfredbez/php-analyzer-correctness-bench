"use strict";

const data = JSON.parse(document.getElementById("report-data").textContent);
const $ = (id) => document.getElementById(id);
const names = {
  ok: "OK", false_positive: "FP", false_negative: "FN", mixed: "FP+FN",
  divergence: "DIV", tool_error: "ERR", case_error: "BAD", skipped: "skip",
  fixed: "Improved", regressed: "Regressed", still_open: "Still open",
  still_ok: "Still OK", not_comparable: "Not comparable",
};
const profiles = new Map(data.profiles.map((p) => [p.id, p]));
const records = new Map(data.profiles.map((p) => [p.id, new Map(p.report.cases.map((c) => [c.case, c]))]));
const columns = [
  { id: "phpstan", label: "PHPStan", profile: "stable", tool: "phpstan" },
  { id: "psalm", label: "Psalm", profile: "stable", tool: "psalm" },
  ...data.profiles.map((p) => ({ id: p.id, label: p.label, profile: p.id, tool: "mago" })),
];
let selected = null;
let visible = [];

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function badge(verdict) { return node("span", names[verdict] || "Not measured", `badge ${verdict || "skipped"}`); }
function result(id, column) { return records.get(column.profile).get(id)?.results[column.tool]; }
function external(url, title) {
  const a = node("a", title);
  if (typeof url === "string" && url.startsWith("https://")) {
    a.href = url; a.target = "_blank"; a.rel = "noopener noreferrer";
  }
  return a;
}
function pair() {
  if (!data.comparisons.length) return null;
  return data.comparisons[Number($("pair").value || 0)] || null;
}
function change(id) {
  const p = pair();
  if (!p) return null;
  return p.cases.find((row) => row.case === id)?.transition || "not_comparable";
}
function toolColumn(toolName) {
  if (toolName === "mago" && pair()) {
    return columns.find((col) => col.tool === "mago" && col.profile === pair().after) || columns.find((col) => col.tool === "mago");
  }
  return columns.find((col) => col.tool === toolName);
}
const isDefect = (v) => ["false_positive", "false_negative", "mixed", "tool_error", "case_error"].includes(v);

const stable = profiles.get("stable").report;
const runtimeChecks = stable.cases.filter((c) => c.runtime_proof).length;
const catalog = data.catalog || { target_criteria: 120, candidates: [] };
const assessments = new Map((data.catalog_assessment?.entries || []).map((entry) => [entry.candidate_id, entry]));
const criteria = new Set(data.cases.map((c) => c.manifest.criterion_id || c.id));
$("coverage").textContent = `${data.cases.length} examples · ${criteria.size} criteria · PHP ${stable.meta.php_version}`;
for (const column of columns) {
  const profile = profiles.get(column.profile), summary = profile.report.summary[column.tool];
  const row = node("tr");
  const tool = node("td", profile.report.meta.tools[column.tool].replace(" - PHP Static Analysis Tool", "").split("@")[0]);
  if (column.tool === "mago") tool.textContent = column.label;
  tool.title = `${profile.report.meta.tools[column.tool]}\nSHA256 ${profile.report.meta.tool_sha256[column.tool]}\nRef ${profile.ref}`;
  row.append(tool);
  const excluded = summary.divergence + summary.tool_error + summary.case_error + summary.skipped;
  for (const value of [`${summary.ok} / ${summary.judged}`, summary.false_positive, summary.false_negative, summary.mixed, excluded]) row.append(node("td", String(value)));
  $("versions").querySelector("tbody").append(row);
}
for (const domain of [...new Set(data.cases.map((c) => c.manifest.domain))].sort()) {
  const option = node("option", domain); option.value = domain; $("domain").append(option);
}
if (data.comparisons.length) {
  data.comparisons.forEach((p, index) => {
    const before = profiles.get(p.before), after = profiles.get(p.after);
    const option = node("option", `${before.kind === "release" ? before.ref : before.id} → ${after.kind === "release" ? after.ref : after.id}`);
    option.value = String(index); $("pair").append(option);
  });
  for (const [value, label] of [
    ["fixed", "Mago · improved"],
    ["regressed", "Mago · regressed"],
    ["not_comparable", "Mago · not comparable"],
  ]) {
    const option = node("option", label);
    option.value = value;
    $("finding").append(option);
  }
} else {
  const option = node("option", "No version comparison available");
  option.value = "";
  $("pair").append(option);
  $("pair").disabled = true;
}
const heading = node("tr");
const headerLabels = ["Case / domain", ...columns.map((c) => c.label)];
if (data.comparisons.length) headerLabels.push("Mago change");
for (const label of headerLabels) heading.append(node("th", label));
$("matrix").querySelector("thead").append(heading);

function render() {
  if (!pair() && ["fixed", "regressed", "not_comparable"].includes($("finding").value)) {
    $("finding").value = "all";
  }
  const query = $("search").value.trim().toLowerCase(), domain = $("domain").value, finding = $("finding").value;
  visible = data.cases.filter((c) => {
    if (query && !`${c.id} ${c.manifest.title}`.toLowerCase().includes(query)) return false;
    if (domain !== "all" && c.manifest.domain !== domain) return false;
    const verdicts = columns.map((column) => result(c.id, column)?.verdict);
    if (finding === "defects") return verdicts.some((v) => ["false_positive", "false_negative", "mixed"].includes(v));
    if (["false_positive", "false_negative"].includes(finding)) return verdicts.includes(finding) || verdicts.includes("mixed");
    if (finding === "divergence") return verdicts.includes("divergence");
    if (finding === "still_open") return isDefect(result(c.id, toolColumn("mago"))?.verdict);
    if (finding === "open_phpstan") return isDefect(result(c.id, toolColumn("phpstan"))?.verdict);
    if (finding === "open_psalm") return isDefect(result(c.id, toolColumn("psalm"))?.verdict);
    return finding === "all" || change(c.id) === finding;
  });
  if (!visible.some((c) => c.id === selected)) selected = visible[0]?.id || null;
  $("example").replaceChildren();
  for (const c of visible) {
    const option = node("option", c.manifest.title); option.value = c.id; $("example").append(option);
  }
  $("example").value = selected || "";
  $("example").disabled = !selected;
  const index = visible.findIndex((c) => c.id === selected);
  $("previous").disabled = index <= 0;
  $("next").disabled = index < 0 || index === visible.length - 1;
  const body = $("matrix").querySelector("tbody"); body.replaceChildren();
  for (const c of visible) {
    const row = node("tr", undefined, c.id === selected ? "selected" : "");
    const title = node("td"), button = node("button", c.manifest.title, "case-button");
    button.append(node("small", c.id)); button.onclick = () => showCase(c.id);
    title.append(button); row.append(title);
    for (const column of columns) {
      const cell = node("td"), measured = result(c.id, column);
      const label = badge(measured?.verdict); label.title = measured?.detail || (measured?.verdict === "ok" ? "Expectation met" : names[measured?.verdict] || "Not measured");
      cell.append(label); row.append(cell);
    }
    if (pair()) {
      const transition = change(c.id);
      row.append(node("td", names[transition] || transition, `transition ${transition}`));
    }
    body.append(row);
  }
  $("result-count").textContent = `${visible.length} of ${data.cases.length} examples${selected ? ` · Example ${index + 1}` : ""} · ${stable.meta.runtime_proven}/${runtimeChecks} executed runtime checks passed`;
  $("empty").hidden = visible.length !== 0;
  $("compatibility").replaceChildren();
  if (!pair()) {
    $("compatibility").append(node("p", "Only one Mago version was measured. No version comparison is available.", "problem"));
  } else if (pair().problems.length) {
    $("compatibility").append(node("p", `Versions are not comparable: ${pair().problems.join("; ")}`, "problem"));
  }
  $("case-detail").hidden = !selected;
  if (selected) renderCase(selected);
}

function showCase(id) {
  selected = id; render();
  $("case-detail").scrollIntoView({ block: "start" });
}

function sourceBlock(name, text) {
  const section = node("div", undefined, "source-file"), heading = node("div", undefined, "code-heading");
  const button = node("button", "Copy PHP"), status = node("span");
  status.setAttribute("role", "status");
  const pre = node("pre"), code = node("code", text); pre.append(code);
  button.onclick = async () => {
    try {
      await navigator.clipboard.writeText(text);
      status.textContent = "Copied.";
    } catch {
      const range = document.createRange(); range.selectNodeContents(code);
      const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      status.textContent = "Code selected. Press Ctrl+C or ⌘C.";
    }
  };
  heading.append(node("span", name), button, status); section.append(heading, pre);
  return section;
}

function diagnosticLabel(item) {
  const line = item.line ? `:${item.line}` : "";
  const tol = item.line && typeof item.line_tolerance === "number" && item.line_tolerance > 0
    ? ` ±${item.line_tolerance} lines`
    : "";
  return `${item.code}${line}${tol}`;
}

function renderCase(id) {
  const c = data.cases.find((item) => item.id === id), manifest = c.manifest;
  const detail = $("case-detail"); detail.replaceChildren(); detail.hidden = false;
  const title = node("h2", manifest.title); title.id = "detail-title"; detail.append(title);
  const identity = node("p", undefined, "meta case-id"), permalink = node("a", c.id);
  permalink.href = `#case=${encodeURIComponent(id)}`;
  identity.append(permalink, document.createTextNode(` · PHP ${manifest.php.min}+${manifest.php.max ? `, up to ${manifest.php.max}` : ""}`)); detail.append(identity);
  const fixture = Object.entries(c.files).filter(([name]) => name.endsWith(".php") && !name.startsWith("runtime/"));
  const composer = JSON.parse(c.files["composer.json"]);
  const dependencies = manifest.composer?.install ? Object.keys(composer.require).filter((name) => name !== "php") : [];
  const projectOnly = fixture.length !== 1 || Boolean(manifest.composer?.install);
  if (projectOnly) detail.append(node("p", dependencies.length
    ? `Local project required. This example depends on ${dependencies.join(", ")}; a standalone playground paste is incomplete.`
    : "Local project required. Copy each file separately; this example includes another file and cannot run as a single playground paste.", "project-note"));
  const playgrounds = node("p", undefined, "playgrounds");
  playgrounds.append(node("span", "Paste into:"));
  for (const [name, url] of [["PHPStan", "https://phpstan.org/try"], ["Psalm", "https://psalm.dev/"], ["Mago", "https://mago.carthage.software/latest/en/playground"]]) playgrounds.append(external(url, name));
  if (!projectOnly) detail.append(playgrounds);
  for (const [name, text] of fixture) detail.append(sourceBlock(name, text));
  detail.append(node("p", "Benchmark defaults: PHPStan level 9, Psalm errorLevel 1, Mago analyzer only. Match the PHP version and case configuration; playground versions and defaults can differ.", "meta"));
  const table = node("table", undefined, "result-table"), head = node("thead"), heading = node("tr"), body = node("tbody");
  for (const label of ["Tool", "Result", "Expected", "Observed"]) heading.append(node("th", label));
  head.append(heading); table.append(head, body);
  for (const column of columns) {
    const measured = result(id, column), expectation = manifest.expect[column.tool];
    const allowed = (expectation.allowed || []).map(diagnosticLabel).join(", ");
    const expected = expectation.mode === "clean" ? (allowed ? `Optional: ${allowed}` : "No diagnostic")
      : expectation.mode === "unsupported" ? "Out of scope"
      : (expectation.required || []).map(diagnosticLabel).join(", ") + (allowed ? `; optional: ${allowed}` : "");
    const unmeasured = !measured || ["tool_error", "case_error", "skipped"].includes(measured.verdict);
    const observed = unmeasured ? "Not measured" : measured.diagnostics.map(diagnosticLabel).join(", ") || "No diagnostic";
    const row = node("tr");
    for (const text of [column.label, names[measured?.verdict] || "Not measured", expected, observed]) row.append(node("td", text));
    body.append(row);
  }
  const scroll = node("div", undefined, "table-scroll"); scroll.append(table); detail.append(scroll);
  detail.append(node("p", "Results describe agreement with this case's baseline. FP/FN do not necessarily mean a tool defect; DIV is a documented scope difference.", "meta"));
  const evidence = node("details", undefined, "evidence"); evidence.append(node("summary", "Explanation, diagnostics and configuration"));
  evidence.append(node("h3", "Expected behavior"), node("p", manifest.ground_truth.statement));
  if (manifest.ground_truth.citation) evidence.append(external(manifest.ground_truth.citation, "Source"));
  if (manifest.notes) {
    const notes = node("details"); notes.append(node("summary", "Case notes"), node("p", manifest.notes)); evidence.append(notes);
  }
  const skipped = result(id, columns[0])?.verdict === "skipped";
  const runtimeVersion = (skipped
    ? manifest.php.max || manifest.php.min : stable.meta.php_version).split(".").slice(0, 2).join(".");
  const command = `python3 harness/bench.py run --php ${runtimeVersion} --case ${c.id}`;
  const reproduction = node("details");
  reproduction.append(node("summary", "Reproduce"), node("pre", `${command}\n# Use another Mago binary:\nBENCH_TOOL_MAGO=/path/to/mago ${command} --tool mago`));
  evidence.append(reproduction);
  const runtime = node("details"); runtime.append(node("summary", `Runtime check · PHP ${stable.meta.php_version}`));
  const proof = records.get("stable").get(c.id)?.runtime_proof;
  runtime.append(node("p", proof ? (proof.confirmed ? "Passed for the tested values, not all possible inputs." : "Failed. This case cannot judge tool behavior.") : skipped ? "Skipped on this PHP version." : "No runtime check provided."));
  runtime.append(node("pre", proof ? `${proof.stdout || ""}${proof.stderr || ""}\nExit: ${proof.exit_code}` : "Not measured"));
  const runtimeSource = node("details"); runtimeSource.append(node("summary", "Runtime source"), node("pre", c.files[manifest.ground_truth.runtime_script] || "No file provided."));
  runtime.append(runtimeSource); evidence.append(runtime);
  const configuration = node("details");
  configuration.append(node("summary", "Configuration and metadata"), node("pre", JSON.stringify(manifest, null, 2)));
  for (const [name, text] of Object.entries(c.files)) {
    if (["composer.json", "phpstan.neon", "psalm.xml", "mago.toml"].includes(name)) {
      configuration.append(node("h3", name), node("pre", text));
    }
  }
  evidence.append(configuration);
  for (const column of columns) {
    const measured = result(c.id, column), expectation = manifest.expect[column.tool];
    const section = node("details"), summary = node("summary", `${column.label} · ${names[measured?.verdict] || "Not measured"}`);
    section.append(summary, node("p", measured?.detail || (measured?.verdict === "ok" ? "Expectation met." : names[measured?.verdict] || "Not measured.")));
    if (expectation.reason) {
      const notes = node("details"); notes.append(node("summary", "Expectation notes"), node("p", expectation.reason)); section.append(notes);
    }
    if (expectation.citation) section.append(external(expectation.citation, "Diagnostic scope source"));
    section.append(node("h3", "Declared expectation"), node("pre", JSON.stringify(expectation, null, 2)));
    section.append(node("h3", "Measured diagnostics"), node("pre", JSON.stringify(measured, null, 2)));
    evidence.append(section);
  }
  detail.append(evidence);
  history.replaceState(null, "", location.pathname + location.search + `#case=${encodeURIComponent(id)}`);
}

for (const id of ["search", "domain", "finding", "pair"]) $(id).addEventListener(id === "search" ? "input" : "change", render);
$("reset").onclick = () => { $("search").value = ""; $("domain").value = "all"; $("finding").value = "all"; if (data.comparisons.length) $("pair").value = "0"; render(); };
$("example").onchange = () => { selected = $("example").value; render(); };
for (const [control, offset] of [["previous", -1], ["next", 1]]) $(control).onclick = () => {
  selected = visible[visible.findIndex((c) => c.id === selected) + offset].id; render();
};
$("download").onclick = () => {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
  const a = node("a"); a.href = url; a.download = "comparison.json"; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
$("catalog-heading").textContent = `Source coverage · ${assessments.size} of ${catalog.candidates.length} leads assessed`;
for (const item of catalog.candidates) {
  const assessment = assessments.get(item.id);
  const row = node("tr"); row.append(node("td", item.family), node("td", item.title), node("td", assessment?.status || "unreviewed"));
  const evidence = node("td");
  for (const id of assessment?.case_ids || []) {
    const button = node("button", id, "case-button");
    button.onclick = () => { $("reset").click(); showCase(id); };
    evidence.append(button);
  }
  if (assessment) {
    const explanation = node("details");
    explanation.append(node("summary", "Scope"), node("p", assessment.reason));
    evidence.append(explanation);
  }
  row.append(evidence);
  const source = node("td"); source.append(item.citation ? external(item.citation, `${item.path}:${item.line}`) : node("span", `${item.path} · local provenance only`));
  row.append(source); $("catalog").querySelector("tbody").append(row);
}
$("environment").textContent = `PHP ${stable.meta.php_version} · ${stable.meta.runner} / ${stable.meta.image} · Corpus SHA256 ${stable.meta.corpus_fingerprint}`;
$("timestamp").textContent = `Measured ${stable.meta.started}`;
if (location.hash.startsWith("#case=")) {
  try { selected = decodeURIComponent(location.hash.slice(6)); } catch { selected = null; }
}
render();
window.addEventListener("hashchange", () => {
  if (!location.hash) { selected = null; $("reset").click(); return; }
  if (!location.hash.startsWith("#case=")) return;
  try {
    const id = decodeURIComponent(location.hash.slice(6));
    if (data.cases.some((c) => c.id === id)) { $("reset").click(); showCase(id); }
  } catch { /* An invalid fragment leaves the current example unchanged. */ }
});
