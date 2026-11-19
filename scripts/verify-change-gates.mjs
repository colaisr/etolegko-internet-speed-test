#!/usr/bin/env node
/**
 * Гейты OpenSpec change (шаг verify) для Gloom. Без зависимостей: нужен только Node.
 *
 * Использование:
 *   node scripts/verify-change-gates.mjs --change <slug>             все пять гейтов
 *   node scripts/verify-change-gates.mjs --change <slug> --archive   + все задачи закрыты и в tasks.md есть группа ProductDocs
 *   node scripts/verify-change-gates.mjs --change <slug> --gate qa   один гейт
 *   --root <dir>   корень репозитория (по умолчанию текущий каталог; нужен для самопроверки)
 *
 * Гейты лежат в openspec/changes/<slug>/gates/<имя>.json (их пишет оркестратор /verify-change по ответам агентов).
 * Порядок стадий: spec-verify → code-reviewer ∥ security-reviewer → qa → docs-sync.
 * Каждый следующий гейт не может быть «старше» предыдущего (reviewed_at): после правки кода стадии проходят заново.
 * Контракт и формат JSON — ProjectDocs/roles/openspec-gates.md.
 */

import { existsSync, readFileSync, realpathSync } from "node:fs";
import { join, posix, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const GATES = ["spec-verify", "code-reviewer", "security-reviewer", "qa", "docs-sync"];

/** Гейт → гейты, после которых он должен быть пройден. */
const AFTER = {
  "spec-verify": [],
  "code-reviewer": ["spec-verify"],
  "security-reviewer": ["spec-verify"],
  qa: ["code-reviewer", "security-reviewer"],
  "docs-sync": ["qa"],
};

const MIN_WAIVER_LENGTH = 20;

function parseArgs(argv) {
  const args = { archive: false, root: process.cwd() };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--archive") args.archive = true;
    else if (argv[i] === "--change" && argv[i + 1]) args.change = argv[++i];
    else if (argv[i] === "--gate" && argv[i + 1]) args.gate = argv[++i];
    else if (argv[i] === "--root" && argv[i + 1]) args.root = resolve(argv[++i]);
  }
  return args;
}

/** slug активного change; `archive` — каталог архива, а не change. */
export function isValidSlug(slug) {
  return /^[a-z0-9][a-z0-9-]*$/.test(slug) && slug !== "archive";
}

function loadGate(root, slug, name) {
  const rel = `openspec/changes/${slug}/gates/${name}.json`;
  const file = join(root, rel);
  if (!existsSync(file)) return { error: `нет файла ${rel}` };
  let data;
  try {
    data = JSON.parse(readFileSync(file, "utf8"));
  } catch (e) {
    return { error: `${rel}: не JSON (${e.message})` };
  }
  if (data === null || typeof data !== "object" || Array.isArray(data)) {
    return { error: `${rel}: ожидается JSON-объект` };
  }
  return { data };
}

/** Общие поля и вердикт. Возвращает причину отказа или null. */
function checkCommon(name, slug, d) {
  if (d.gate !== name) return `поле gate должно быть "${name}"`;
  if (d.change !== slug) return `поле change должно быть "${slug}"`;
  if (typeof d.reviewed_at !== "string" || Number.isNaN(Date.parse(d.reviewed_at))) {
    return "reviewed_at: нужна дата в формате ISO";
  }
  if (d.verdict === "pass") return null;
  if (d.verdict === "waived" && name === "docs-sync") {
    if (typeof d.waiver_reason !== "string" || d.waiver_reason.trim().length < MIN_WAIVER_LENGTH) {
      return `waived требует waiver_reason не короче ${MIN_WAIVER_LENGTH} символов (почему бизнес-изменений нет)`;
    }
    return null;
  }
  return `verdict "${d.verdict}": нужен "pass"${name === "docs-sync" ? ' (или "waived" с причиной)' : ""}`;
}

/** Путь страницы ProductDocs: относительный, внутри ProductDocs/, .md, не шаблон. */
function invalidDocPath(raw) {
  if (typeof raw !== "string" || !raw.trim()) return "пустой путь";
  const unified = raw.trim().replace(/\\/g, "/");
  if (unified.startsWith("/") || /^[a-zA-Z]:/.test(unified) || unified.split("/").includes("..")) {
    return "путь должен быть относительным и без «..»";
  }
  const n = posix.normalize(unified);
  if (!n.startsWith("ProductDocs/")) return "страница должна лежать в ProductDocs/";
  if (!n.endsWith(".md")) return "ожидается файл .md";
  if (n === "ProductDocs/_template.md") return "шаблон не считается страницей";
  return null;
}

/** docs-sync (pass): страницы ProductDocs существуют и содержат slug change в журнале обновлений. */
function checkDocsSync(root, slug, d) {
  if (d.verdict !== "pass") return null;
  if (!Array.isArray(d.pages) || d.pages.length === 0) {
    return "pages: нужен непустой список обновлённых страниц ProductDocs";
  }
  for (const raw of d.pages) {
    const bad = invalidDocPath(raw);
    if (bad) return `pages: ${raw}: ${bad}`;
    const abs = join(root, posix.normalize(raw.trim().replace(/\\/g, "/")));
    if (!existsSync(abs)) return `pages: нет файла ${raw}`;
    if (!readFileSync(abs, "utf8").includes(slug)) {
      return `pages: в ${raw} нет "${slug}" (добавьте строку в «Журнал обновлений» страницы)`;
    }
  }
  if (!d.pages.some((p) => !String(p).endsWith("README.md"))) {
    return "pages: обновлён только индекс; нужна хотя бы одна страница раздела";
  }
  return null;
}

/** Проверка tasks.md для archive. Возвращает причину отказа или null. */
function checkTasksForArchive(root, slug) {
  const rel = `openspec/changes/${slug}/tasks.md`;
  const file = join(root, rel);
  if (!existsSync(file)) return `нет файла ${rel}`;
  const text = readFileSync(file, "utf8");
  const open = text.split(/\r?\n/).filter((l) => /^\s*[-*]\s+\[ \]/.test(l));
  if (open.length > 0) return `не закрыто задач: ${open.length} (первая: ${open[0].trim()})`;
  if (!/ProductDocs/.test(text)) return "в tasks.md нет группы задач «ProductDocs» (обновить бизнес-страницу)";
  return null;
}

/** Результаты по гейтам; порядок и свежесть проверяются по reviewed_at. */
export function validateChangeGates(root, slug, onlyGate, { archive = false } = {}) {
  const names = onlyGate ? [onlyGate] : GATES;
  const results = [];
  const times = {};

  // Для проверки порядка всегда читаем все гейты, даже если выбран один.
  const loaded = {};
  for (const name of GATES) loaded[name] = loadGate(root, slug, name);

  for (const name of names) {
    const { data, error } = loaded[name];
    if (error) {
      results.push({ gate: name, ok: false, detail: error });
      continue;
    }
    const reason = checkCommon(name, slug, data) || (name === "docs-sync" ? checkDocsSync(root, slug, data) : null);
    if (reason) {
      results.push({ gate: name, ok: false, detail: reason });
      continue;
    }
    times[name] = Date.parse(data.reviewed_at);
    results.push({ gate: name, ok: true });
  }

  // Порядок: гейт не может быть старше того, после которого он идёт.
  for (const result of results) {
    if (!result.ok) continue;
    for (const dep of AFTER[result.gate]) {
      const depData = loaded[dep].data;
      if (!depData || !Number.isFinite(Date.parse(depData.reviewed_at))) continue;
      if (times[result.gate] < Date.parse(depData.reviewed_at)) {
        result.ok = false;
        result.detail = `reviewed_at раньше, чем у ${dep}: гейт устарел, пройдите стадию заново`;
        break;
      }
    }
  }

  if (archive) {
    const reason = checkTasksForArchive(root, slug);
    results.push(reason ? { gate: "tasks", ok: false, detail: reason } : { gate: "tasks", ok: true });
  }
  return results;
}

function main() {
  const { change, gate, archive, root } = parseArgs(process.argv.slice(2));
  const usage = `Использование: node scripts/verify-change-gates.mjs --change <slug> [--archive] [--gate ${GATES.join("|")}] [--root <dir>]`;
  if (!change) {
    console.error(usage);
    process.exit(1);
  }
  if (!isValidSlug(change)) {
    console.error(`Недопустимый slug "${change}": kebab-case, без путей, не "archive".`);
    process.exit(1);
  }
  if (gate && !GATES.includes(gate)) {
    console.error(`Неизвестный --gate "${gate}". Допустимо: ${GATES.join(" | ")}`);
    process.exit(1);
  }
  if (!existsSync(join(root, "openspec/changes", change))) {
    console.error(`Нет change openspec/changes/${change}`);
    process.exit(1);
  }

  const results = validateChangeGates(root, change, gate, { archive });
  let failed = false;
  for (const r of results) {
    if (r.ok) console.log(`  ok    ${r.gate}`);
    else {
      failed = true;
      console.error(`  FAIL  ${r.gate}: ${r.detail}`);
    }
  }
  if (failed) {
    console.error(`verify-change-gates FAIL — ${change}${archive ? " (archive)" : ""}`);
    process.exit(1);
  }
  console.log(`verify-change-gates OK — ${change}${archive ? " (archive)" : ""} (${results.map((r) => r.gate).join(", ")})`);
}

let isEntry = false;
try {
  isEntry = import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href;
} catch {
  isEntry = false;
}
if (isEntry) main();
