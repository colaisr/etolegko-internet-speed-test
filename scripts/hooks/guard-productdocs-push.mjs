#!/usr/bin/env node
/**
 * Замок ProductDocs перед `git push`.
 * Git: .githooks/pre-push
 * Агент: Cursor beforeShellExecution + Claude PreToolUse (Bash).
 */

import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { verifyAll } from "../verify-productdocs.mjs";
import { allow, deny, parseHookInput, runHook } from "./hook-io.mjs";

const ZERO = "0".repeat(40);

function git(root, ...args) {
  return spawnSync("git", args, { cwd: root, encoding: "utf8" });
}

function filesForRefRange(root, remoteSha, localSha) {
  if (localSha === ZERO) return [];
  let out;
  if (remoteSha === ZERO) {
    out = git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", localSha);
  } else {
    out = git(root, "diff", "--name-only", remoteSha, localSha);
  }
  if (out.status !== 0) return [];
  return out.stdout.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
}

function filesAheadOfUpstream(root) {
  const upstream = git(root, "rev-parse", "--abbrev-ref", "@{upstream}");
  if (upstream.status !== 0) {
    const head = git(root, "diff", "--name-only", "HEAD");
    return head.stdout.split(/\r?\n/).filter(Boolean);
  }
  const diff = git(root, "diff", "--name-only", "@{upstream}..HEAD");
  return diff.stdout.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
}

function collectFromPrePushStdin(root, stdin) {
  const all = new Set();
  for (const line of stdin.split(/\r?\n/)) {
    const parts = line.trim().split(/\s+/);
    if (parts.length < 4) continue;
    const [, localSha, , remoteSha] = parts;
    for (const f of filesForRefRange(root, remoteSha, localSha)) all.add(f);
  }
  return [...all];
}

function runVerify(root, changedFiles) {
  const result = verifyAll(root, changedFiles);
  if (result.ok) return null;
  return (
    "push заблокирован: ProductDocs не актуален.\n" +
    result.errors.map((e) => `  • ${e}`).join("\n") +
    "\nЗапустите: node scripts/verify-productdocs.mjs"
  );
}

function mainGitHook(root) {
  const stdin = readFileSync(0, "utf8");
  const files = collectFromPrePushStdin(root, stdin);
  const msg = runVerify(root, files.length ? files : filesAheadOfUpstream(root));
  if (msg) {
    process.stderr.write(`${msg}\n`);
    process.exit(1);
  }
  process.exit(0);
}

function agentHandler(input) {
  const { isCursor, command, root } = parseHookInput(input);
  if (!/\bgit\s+push\b/.test(command)) {
    allow(isCursor);
    return;
  }
  const files = filesAheadOfUpstream(root);
  const msg = runVerify(root, files);
  if (msg) deny(isCursor, msg);
  allow(isCursor);
}

const scriptPath = fileURLToPath(import.meta.url);
if (process.argv.includes("--git-pre-push")) {
  const root = git(process.cwd(), "rev-parse", "--show-toplevel");
  mainGitHook(root.status === 0 ? root.stdout.trim() : process.cwd());
} else {
  runHook(scriptPath, agentHandler);
}