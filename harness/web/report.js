"use strict";

const data = JSON.parse(document.getElementById("report-data").textContent);
const $ = (id) => document.getElementById(id);
const names = {
  ok: "OK", false_positive: "FP", false_negative: "FN", mixed: "FP+FN",
  divergence: "Abw.", tool_error: "ERR", case_error: "BAD", skipped: "skip",
  fixed: "Behoben", regressed: "Regression", still_open: "Weiterhin offen",
  still_ok: "Weiterhin OK", not_comparable: "Nicht vergleichbar",
};
const profiles = new Map(data.profiles.map((p) => [p.id, p]));
const records = new Map(data.profiles.map((p) => [p.id, new Map(p.report.cases.map((c) => [c.case, c]))]));
const columns = [
  { id: "phpstan", label: "PHPStan", profile: "stable", tool: "phpstan" },
  { id: "psalm", label: "Psalm", profile: "stable", tool: "psalm" },
  ...data.profiles.map((p) => ({ id: p.id, label: p.label, profile: p.id, tool: "mago" })),
];
let selected = null;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function badge(verdict) { return node("span", names[verdict] || "Nicht gemessen", `badge ${verdict || "skipped"}`); }
function result(id, column) { return records.get(column.profile).get(id)?.results[column.tool]; }
function external(url, title) {
  const a = node("a", title);
  if (typeof url === "string" && url.startsWith("https://")) {
    a.href = url; a.target = "_blank"; a.rel = "noopener noreferrer";
  }
  return a;
}
function pair() { return data.comparisons[Number($("pair").value || 0)]; }
function change(id) { return pair()?.cases.find((row) => row.case === id)?.transition || "not_comparable"; }

const stable = profiles.get("stable").report;
const catalog = data.catalog || { target_criteria: 120, candidates: [] };
const criteria = new Set(data.cases.map((c) => c.manifest.criterion_id || c.id));
for (const [value, text] of [
  [criteria.size, `Kriterien gemessen · ${data.cases.length} Reproducer`],
  [catalog.target_criteria, "Ziel: unabhängige Kriterien vor Veröffentlichung"],
  [catalog.candidates.length, "Quellkandidaten · noch nicht bewertet"],
]) {
  const card = node("article"); card.append(node("strong", String(value)), node("span", text)); $("coverage").append(card);
}
for (const column of columns) {
  const profile = profiles.get(column.profile), summary = profile.report.summary[column.tool];
  const card = node("article", undefined, "version");
  card.append(node("h3", column.label), node("div", `${summary.ok} / ${summary.judged}`, "score"));
  card.append(node("p", "OK / gewertet · keine Gesamtnote"));
  card.append(node("p", `FP ${summary.false_positive} · FN ${summary.false_negative} · FP+FN ${summary.mixed}`));
  const excluded = summary.divergence + summary.tool_error + summary.case_error + summary.skipped;
  card.append(node("p", `${excluded} ausgeschlossen`));
  const source = node("p", profile.report.meta.tools[column.tool].replace(" - PHP Static Analysis Tool", "").split("@")[0], "source");
  source.title = `${profile.report.meta.tools[column.tool]}\nSHA256 ${profile.report.meta.tool_sha256[column.tool]}`;
  card.append(source); $("versions").append(card);
}
for (const domain of [...new Set(data.cases.map((c) => c.manifest.domain))].sort()) {
  const option = node("option", domain); option.value = domain; $("domain").append(option);
}
data.comparisons.forEach((p, index) => {
  const before = profiles.get(p.before), after = profiles.get(p.after);
  const option = node("option", `${before.kind === "release" ? before.ref : before.id} → ${after.kind === "release" ? after.ref : after.id}`);
  option.value = String(index); $("pair").append(option);
});
const heading = node("tr");
for (const label of ["Kriterium / Bereich", ...columns.map((c) => c.label), "Mago-Verlauf"]) heading.append(node("th", label));
$("matrix").querySelector("thead").append(heading);

function render() {
  const query = $("search").value.trim().toLowerCase(), domain = $("domain").value, finding = $("finding").value;
  const visible = data.cases.filter((c) => {
    if (query && !`${c.id} ${c.manifest.title}`.toLowerCase().includes(query)) return false;
    if (domain !== "all" && c.manifest.domain !== domain) return false;
    const verdicts = columns.map((column) => result(c.id, column)?.verdict);
    if (finding === "defects") return verdicts.some((v) => ["false_positive", "false_negative", "mixed"].includes(v));
    if (["false_positive", "false_negative"].includes(finding)) return verdicts.includes(finding) || verdicts.includes("mixed");
    if (finding === "divergence") return verdicts.includes("divergence");
    return finding === "all" || change(c.id) === finding;
  });
  const body = $("matrix").querySelector("tbody"); body.replaceChildren();
  for (const c of visible) {
    const row = node("tr", undefined, c.id === selected ? "selected" : "");
    const title = node("td"), button = node("button", c.manifest.title, "case-button");
    button.append(node("small", c.id)); button.onclick = () => showCase(c.id);
    title.append(button); row.append(title);
    for (const column of columns) {
      const cell = node("td"), measured = result(c.id, column);
      const label = badge(measured?.verdict); label.title = measured?.detail || "Erwartung erfüllt";
      cell.append(label); row.append(cell);
    }
    row.append(node("td", names[change(c.id)], `transition ${change(c.id)}`)); body.append(row);
  }
  $("result-count").textContent = `${visible.length} von ${data.cases.length} gemessenen Fällen · PHP ${stable.meta.php_version} · ${stable.meta.runtime_proven}/${stable.meta.case_count} Laufzeitprüfungen bestanden`;
  $("empty").hidden = visible.length !== 0;
  $("compatibility").replaceChildren();
  if (pair()?.problems.length) $("compatibility").append(node("p", `Dieser Versionsvergleich ist nicht belastbar: ${pair().problems.join("; ")}`, "problem"));
  if (selected && !visible.some((c) => c.id === selected)) { selected = null; $("case-detail").hidden = true; }
}

function showCase(id) {
  selected = id; render();
  const c = data.cases.find((item) => item.id === id), manifest = c.manifest;
  const detail = $("case-detail"); detail.replaceChildren(); detail.hidden = false;
  const close = node("button", "Schließen ×", "close");
  close.onclick = () => { selected = null; detail.hidden = true; history.replaceState(null, "", location.pathname + location.search); render(); };
  detail.append(close, node("p", c.id, "eyebrow"));
  const title = node("h2", manifest.title); title.id = "detail-title"; detail.append(title);
  detail.append(node("p", `Bereich: ${manifest.domain} · Regelklasse: ${manifest.rule_class} · Basis: ${manifest.ground_truth.basis}`));
  detail.append(node("div", "Abstimmung offen: Dies ist die Erwartung des Benchmarks, keine Freigabe durch einen Tool-Maintainer.", "alignment"));
  detail.append(node("h3", "Welche Aussage wird geprüft?"), node("p", manifest.ground_truth.statement));
  if (manifest.notes) detail.append(node("p", manifest.notes));
  if (manifest.ground_truth.citation) detail.append(external(manifest.ground_truth.citation, "Quelle der Begründung ↗"));
  detail.append(node("h3", "Reproduzieren"), node("pre", `python3 harness/bench.py run --case ${c.id}\n# Für eine andere Mago-Version voranstellen:\nBENCH_TOOL_MAGO=/pfad/zu/mago python3 harness/bench.py run --case ${c.id} --tool mago`));
  const grid = node("div", undefined, "detail-grid"), code = node("div"), runtime = node("div");
  code.append(node("h3", "PHP-Reproducer"));
  const fixture = Object.entries(c.files).filter(([name]) => name.startsWith("src/") && name.endsWith(".php"));
  code.append(node("pre", fixture.map(([name, text]) => `// ${name}\n${text}`).join("\n")));
  const proof = records.get("stable").get(c.id)?.runtime_proof;
  runtime.append(node("h3", `Laufzeitkontrolle · PHP ${stable.meta.php_version}`));
  runtime.append(node("p", proof ? (proof.confirmed ? "Bestanden. Das belegt die ausgeführten Kontrollwerte, nicht alle möglichen Eingaben." : "Fehlgeschlagen. Dieser Fall darf keinen Analyzer bewerten.") : "Keine Laufzeitkontrolle hinterlegt."));
  runtime.append(node("pre", proof ? `${proof.stdout || ""}${proof.stderr || ""}\nExit: ${proof.exit_code}` : "Keine Messung"));
  const runtimeSource = node("details"); runtimeSource.append(node("summary", "Laufzeitprüfung ansehen"), node("pre", c.files[manifest.ground_truth.runtime_script] || "Keine Datei hinterlegt."));
  runtime.append(runtimeSource); grid.append(code, runtime); detail.append(grid);
  const configuration = node("details");
  configuration.append(node("summary", "Konfiguration und vollständige Metadaten"), node("pre", JSON.stringify(manifest, null, 2)));
  for (const [name, text] of Object.entries(c.files)) {
    if (["composer.json", "phpstan.neon", "psalm.xml", "mago.toml"].includes(name)) {
      configuration.append(node("h3", name), node("pre", text));
    }
  }
  detail.append(configuration);
  detail.append(node("h3", "Erwartung und tatsächlicher Befund je Analyzer"));
  for (const column of columns) {
    const measured = result(c.id, column), expectation = manifest.expect[column.tool];
    const section = node("details"), summary = node("summary", `${column.label} · ${names[measured?.verdict] || "Nicht gemessen"}`);
    section.append(summary, node("p", measured?.detail || "Die Messung entspricht der erklärten Erwartung."));
    if (expectation.reason) section.append(node("p", expectation.reason));
    if (expectation.citation) section.append(external(expectation.citation, "Beleg für den Diagnoseumfang ↗"));
    section.append(node("h3", "Deklarierte Erwartung"), node("pre", JSON.stringify(expectation, null, 2)));
    section.append(node("h3", "Gemessene Diagnosen"), node("pre", JSON.stringify(measured, null, 2)));
    detail.append(section);
  }
  history.replaceState(null, "", `#case=${encodeURIComponent(id)}`);
  detail.scrollIntoView({ behavior: "instant", block: "start" }); detail.focus({ preventScroll: true });
}

for (const id of ["search", "domain", "finding", "pair"]) $(id).addEventListener(id === "search" ? "input" : "change", render);
$("reset").onclick = () => { $("search").value = ""; $("domain").value = "all"; $("finding").value = "all"; $("pair").value = "0"; render(); };
$("download").onclick = () => {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
  const a = node("a"); a.href = url; a.download = "comparison.json"; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
$("catalog-heading").textContent = `${catalog.candidates.length} Quellkandidaten · noch nicht bewertet`;
for (const item of catalog.candidates) {
  const row = node("tr"); row.append(node("td", item.family), node("td", item.title), node("td", item.domain));
  const source = node("td"); source.append(item.citation ? external(item.citation, `${item.path}:${item.line}`) : node("span", `${item.path} · nur lokaler Herkunftsnachweis`));
  row.append(source); $("catalog").querySelector("tbody").append(row);
}
$("environment").textContent = `PHP ${stable.meta.php_version} · ${stable.meta.runner} / ${stable.meta.image} · Korpus SHA256 ${stable.meta.corpus_fingerprint}`;
$("timestamp").textContent = `Messstand ${stable.meta.started}`;
render();
if (location.hash.startsWith("#case=")) {
  const id = decodeURIComponent(location.hash.slice(6));
  if (data.cases.some((c) => c.id === id)) showCase(id);
}
