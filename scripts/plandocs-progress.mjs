#!/usr/bin/env node
/**
 * Прогресс PlanDocs: статус каждого раздела и число открытых вопросов. Без зависимостей.
 *
 * Использование:
 *   node scripts/plandocs-progress.mjs              таблица по всем разделам
 *   node scripts/plandocs-progress.mjs --stubs      только заглушки
 *   node scripts/plandocs-progress.mjs --root <dir> корень репозитория (по умолчанию текущий каталог)
 *
 * Статус берётся из первой строки «**Статус:** …» файла (первое слово): заглушка, черновик, актуален.
 * Открытые вопросы считаются по строкам таблицы в разделе, заголовок которого содержит «Открытые вопросы».
 */

import { readdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const args = process.argv.slice(2);
const root = args.includes("--root") ? resolve(args[args.indexOf("--root") + 1]) : process.cwd();
const onlyStubs = args.includes("--stubs");
const dir = join(root, "PlanDocs");

function statusOf(text) {
  const m = text.match(/\*\*Статус:\*\*\s*([^\s.,;:(]+)/i);
  if (!m) return "без статуса";
  const word = m[1].toLowerCase();
  if (word.startsWith("заглушк")) return "заглушка";
  if (word.startsWith("черновик")) return "черновик";
  if (word.startsWith("актуал")) return "актуален";
  return word;
}

function openQuestions(text) {
  const lines = text.split(/\r?\n/);
  const start = lines.findIndex((l) => /^##\s+.*Открытые вопросы/i.test(l));
  if (start === -1) return 0;
  let end = lines.findIndex((l, i) => i > start && /^##\s/.test(l));
  if (end === -1) end = lines.length;
  const rows = lines.slice(start + 1, end).filter((l) => l.trim().startsWith("|"));
  // заголовок таблицы и разделитель не считаем
  return Math.max(0, rows.length - 2);
}

const files = readdirSync(dir)
  .filter((f) => /^\d\d-.*\.md$/.test(f))
  .sort();

const rows = files.map((f) => {
  const text = readFileSync(join(dir, f), "utf8");
  return { file: f, num: f.slice(0, 2), status: statusOf(text), open: openQuestions(text) };
});

const shown = onlyStubs ? rows.filter((r) => r.status === "заглушка") : rows;
console.log("№   Статус       Вопросов  Файл");
for (const r of shown) {
  console.log(`${r.num}  ${r.status.padEnd(11)}  ${String(r.open).padStart(7)}  ${r.file}`);
}

const count = (s) => rows.filter((r) => r.status === s).length;
const total = rows.reduce((a, r) => a + r.open, 0);
console.log(
  `\nРазделов: ${rows.length}; актуальных: ${count("актуален")}; черновиков: ${count("черновик")}; ` +
    `заглушек: ${count("заглушка")}; открытых вопросов: ${total}`,
);
