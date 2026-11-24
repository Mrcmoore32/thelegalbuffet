// Search simulation for Topic #113 — replicates assets/js/search.js
// scoring exactly (norm + score + content-first ordering) and runs it
// against the built search-index.json. Usage: node verify_llc_search.js
const fs = require("fs");
const path = require("path");

const idx = JSON.parse(
  fs.readFileSync(path.join(__dirname, "..", "assets", "search-index.json"), "utf8")
);

function norm(s) {
  return (s || "").toLowerCase().replace(/[^a-z0-9\s]/g, " ");
}
function score(entry, words) {
  let s = 0;
  const h = norm(entry.h), t = norm(entry.t), p = norm(entry.p);
  for (const w of words) {
    if (!w) continue;
    if (h.indexOf(w) !== -1) s += 5;
    else if (p.indexOf(w) !== -1) s += 2;
    else if (t.indexOf(w) !== -1) s += 1;
    else return -1;
  }
  return s;
}
function runSearch(q) {
  const words = norm(q).split(/\s+/);
  const content = [], helper = [];
  for (const e of idx) {
    const s = score(e, words);
    if (s <= 0) continue;
    if (e.a === "helper") { helper.push({ e, s }); continue; }
    content.push({ e, s });
  }
  content.sort((a, b) => b.s - a.s);
  helper.sort((a, b) => b.s - a.s);
  return content.concat(helper);
}

let failures = 0;
function check(name, ok, detail) {
  console.log((ok ? "PASS " : "FAIL ") + name + (ok ? "" : " — " + detail));
  if (!ok) failures++;
}

const llc = runSearch("LLC");
const llcNew = llc.filter(r => (r.e.a || "").startsWith("forming-an-llc-in-"));
check('"LLC" returns all 50 new state entries', llcNew.length === 50, `got ${llcNew.length}`);
check('"LLC" top result is a new Forming-an-LLC entry',
  llc.length > 0 && (llc[0].e.a || "").startsWith("forming-an-llc-in-"),
  llc.length ? llc[0].e.h : "no results");
console.log(`  "LLC" total results: ${llc.length}; new entries: ${llcNew.length}; top 3:`);
llc.slice(0, 3).forEach(r => console.log(`    [${r.s}] ${r.e.h} (${r.e.u}#${r.e.a})`));

const mn = runSearch("forming an LLC minnesota");
check('"forming an LLC minnesota" top result is the Minnesota entry',
  mn.length > 0 && mn[0].e.a === "forming-an-llc-in-minnesota",
  mn.length ? `${mn[0].e.h} (${mn[0].e.u}#${mn[0].e.a})` : "no results");
console.log(`  "forming an LLC minnesota" total results: ${mn.length}; top 3:`);
mn.slice(0, 3).forEach(r => console.log(`    [${r.s}] ${r.e.h} (${r.e.u}#${r.e.a})`));

const old = runSearch("LLC");
const sbbHits = old.filter(r => (r.e.a || "").startsWith("small-business-basics-in-"));
console.log(`  "LLC" results pointing at Small Business Basics sections: ${sbbHits.length}`);

if (failures) { console.log(`${failures} FAILURES`); process.exit(1); }
console.log("SEARCH SIMULATION PASSED");
