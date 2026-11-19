#!/usr/bin/env node
/**
 * Проверка актуальности ProductDocs.
 *
 *   node scripts/verify-productdocs.mjs              — структура индекса и журналов
 *   node scripts/verify-productdocs.mjs --push-files <file>  — один путь на строку (stdin ок)
 *
 * Перед push: если в коммите менялись legko/ или openspec/specs/, должны меняться и ProductDocs/ (не только README).
 */

import { existsSync, readFileSync, readdirSync, realpathSync } from "node:fs";
import { join, posix } from "node:path";

const CODE_PREFIXES = ["legko/", "openspec/specs/"];
const DOCS_PREFIX = "ProductDocs/";
const SLUG_IN_JOURNAL = /\|\s*[a-z0-9][a-z0-9-]*\s*\|/;
const CHANGE_HEADER = /\*\*Change:\*\*\s+[a-z0-9][a-z0-9-]*/;

export function listProductDocPages(root) {
  const dir = join(root, "ProductDocs");
  return readdirSync(dir)
    .filter((f) => f.endsWith(".md") && f !== "README.md" && f !== "_template.md")
    .map((f) => `ProductDocs/${f}`);
}

export function checkStructure(root) {
  const errors = [];
  const readmePath = join(root, "ProductDocs/README.md");
  if (!existsSync(readmePath)) {
    return { ok: false, errors: ["нет ProductDocs/README.md"] };
  }
  const readme = readFileSync(readmePath, "utf8");
  if (/страниц разделов нет/.test(readme) && /00-product-overview/.test(readme)) {
    errors.push("ProductDocs/README.md: шапка говорит «страниц нет», но индекс не пуст");
  }

  for (const rel of listProductDocPages(root)) {
    const abs = join(root, rel);
    const body = readFileSync(abs, "utf8");
  const base = posix.basename(rel);
    if (!readme.includes(`(${base})`) && !readme.includes(base)) {
      errors.push(`${rel}: нет строки в ProductDocs/README.md §3`);
    }
    if (!body.includes("## Журнал обновлений")) {
      errors.push(`${rel}: нет раздела «Журнал обновлений»`);
    } else if (!SLUG_IN_JOURNAL.test(body.split("## Журнал обновлений")[1] ?? "")) {
      errors.push(`${rel}: в журнале нет slug change`);
    }
    if (!CHANGE_HEADER.test(body.slice(0, 800))) {
      errors.push(`${rel}: в шапке нет **Change:** <slug>`);
    }
  }
  return { ok: errors.length === 0, errors };
}

export function checkPushFileSet(changedFiles) {
  const normalized = changedFiles.filter(Boolean).map((p) => p.replace(/\\/g, "/"));
  const codeTouched = normalized.some((f) => CODE_PREFIXES.some((pre) => f.startsWith(pre)));
  const docsTouched = normalized.some(
    (f) => f.startsWith(DOCS_PREFIX) && !f.endsWith("ProductDocs/README.md"),
  );
  if (!codeTouched) {
    return { ok: true, skipped: "нет изменений в legko/ или openspec/specs/" };
  }
  if (!docsTouched) {
    return {
      ok: false,
      errors: [
        "В push есть правки legko/ или openspec/specs/, но нет изменений в ProductDocs/*.md " +
          "(кроме README). Обновите бизнес-описание и журнал change.",
      ],
    };
  }
  return { ok: true };
}

export function verifyAll(root, changedFiles = []) {
  const structure = checkStructure(root);
  const push = changedFiles.length ? checkPushFileSet(changedFiles) : { ok: true };
  const errors = [...(structure.errors ?? []), ...(push.errors ?? [])];
  return { ok: structure.ok && push.ok, errors, structure, push };
}

function readFilesFromArgv(argv) {
  const idx = argv.indexOf("--push-files");
  if (idx === -1) return [];
  const rest = argv.slice(idx + 1).filter((a) => !a.startsWith("--"));
  if (rest.length > 0) return rest;
  try {
    return readFileSync(0, "utf8")
      .split(/\r?\n/)
      .map((l) => l.trim())
      .filter(Boolean);
  } catch {
    return [];
  }
}

function main() {
  const root = process.cwd();
  const pushFiles = readFilesFromArgv(process.argv.slice(2));
  const result = verifyAll(root, pushFiles);
  if (result.ok) {
    console.log("verify-productdocs OK");
    if (result.push.skipped) console.log(`  (${result.push.skipped})`);
    process.exit(0);
  }
  for (const e of result.errors) console.error(`  FAIL: ${e}`);
  console.error("verify-productdocs FAIL");
  process.exit(1);
}

import { pathToFileURL } from "node:url";

let isEntry = false;
try {
  isEntry = import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href;
} catch {
  /* импорт */
}
if (isEntry) main();