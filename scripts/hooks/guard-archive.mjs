#!/usr/bin/env node
/**
 * Замок на archive OpenSpec change.
 *
 * Хук перед shell-командой агента: Claude Code (PreToolUse, matcher Bash) и Cursor (beforeShellExecution).
 * Если команда переносит openspec/changes/<slug> в openspec/changes/archive/ (mv, git mv)
 * или запускает `openspec archive <slug>`, хук запускает
 * `node scripts/verify-change-gates.mjs --change <slug> --archive` и блокирует команду при fail.
 * Любая другая команда пропускается сразу.
 */

import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { allow, deny, parseHookInput, runHook } from "./hook-io.mjs";

const SLUG = "[a-z0-9][a-z0-9-]*";

/** slug, если команда архивирует change; "" — архивирует, но slug не определён; null — не про archive. */
export function archivedSlug(command) {
  const cli = command.match(new RegExp(`\\bopenspec\\s+archive\\s+(?:-\\S+\\s+)*["']?(${SLUG})`));
  if (cli) return cli[1];
  if (!/changes\/archive/.test(command) || !/(^|[\s;&|(])(git\s+)?mv\s/.test(command)) return null;
  for (const m of command.matchAll(new RegExp(`openspec/changes/(${SLUG})`, "g"))) {
    if (m[1] !== "archive") return m[1];
  }
  return "";
}

function main(input) {
  const { isCursor, command, root } = parseHookInput(input);

  const slug = archivedSlug(command);
  if (slug === null) allow(isCursor);
  if (slug === "") {
    deny(
      isCursor,
      "archive заблокирован: не удалось определить slug change в команде. " +
        "Перенесите openspec/changes/<slug> явным путём.",
    );
  }

  // Скрипт ищем рядом с хуком, а не относительно корня: так проверка не зависит от того, откуда запущена команда.
  const script = fileURLToPath(new URL("../verify-change-gates.mjs", import.meta.url));
  const run = spawnSync(process.execPath, [script, "--change", slug, "--archive", "--root", root], {
    cwd: root,
    encoding: "utf8",
  });
  if (run.status === 0) allow(isCursor);
  deny(
    isCursor,
    `archive ${slug} заблокирован: verify-change-gates --archive не прошёл.\n` +
      `${run.stdout ?? ""}${run.stderr ?? ""}`.trimEnd() +
      "\nСначала /verify-change, затем закрыть задачи в tasks.md (включая группу ProductDocs).",
  );
}

runHook(import.meta.url, main);
