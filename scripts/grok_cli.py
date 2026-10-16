#!/usr/bin/env python3
"""grok — a small, self-contained Grok (xAI) CLI agent for the sandbox.

Provider-agnostic (any OpenAI-compatible chat API), zero third-party deps beyond
httpx. Two modes:

  grok "one-shot question"            # chat, print the answer
  grok                                # interactive REPL (blank line / Ctrl-D to exit)
  grok --agent "assess module 05 ..." # AGENT mode: Grok gets exec_shell + http_request
                                       #   tools and loops until done

Config (env or flags):
  XAI_API_KEY          required (or --api-key); for --provider openai use OPENAI_API_KEY
  --provider grok|openai|custom   default grok  (grok -> https://api.x.ai/v1)
  --base-url URL       override the API base
  --model NAME         default grok-4
  --max-steps N        agent tool-call budget (default 20)
  --confirm            agent mode: ask before running each shell command

AGENT MODE SAFETY: exec_shell runs real commands in THIS sandbox (an isolated,
ephemeral cloud VM), in the given --cwd. That is intentional — it is your sandbox —
but it means Grok can run arbitrary commands here. It cannot reach anything the
sandbox can't. Nothing is written outside the sandbox. Use chat mode if you only
want answers. Shell commands run with a scrubbed environment: API keys, tokens and
other credentials (including the model key) are removed, so lab content that
injects instructions into the agent cannot read them back out.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import httpx

PROVIDERS = {
    "grok": ("https://api.x.ai/v1", "XAI_API_KEY"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
    "custom": (None, "REDSEC_LLM_API_KEY"),
}

AGENT_TOOLS = [
    {"type": "function", "function": {
        "name": "exec_shell",
        "description": "Run a shell command in the sandbox and get its output.",
        "parameters": {"type": "object",
                       "properties": {"command": {"type": "string"}},
                       "required": ["command"]}}},
    {"type": "function", "function": {
        "name": "http_request",
        "description": "Make an HTTP request (e.g. to a lab target on localhost).",
        "parameters": {"type": "object", "properties": {
            "method": {"type": "string"}, "url": {"type": "string"},
            "headers": {"type": "object"}, "json_body": {"type": "object"}},
            "required": ["method", "url"]}}},
]


def api(base, key, model, messages, tools=None):
    payload = {"model": model, "messages": messages, "temperature": 0}
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    r = httpx.post(f"{base}/chat/completions",
                   headers={"Authorization": f"Bearer {key}"},
                   json=payload, timeout=180)
    if r.status_code != 200:
        sys.exit(f"API error {r.status_code}: {r.text[:300]}")
    return r.json()["choices"][0]["message"]


# Variable names that suggest a credential. The agent reads untrusted, injection-
# laden lab content, so its shell must not inherit anything it could exfiltrate.
_SECRET_MARKERS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL",
                   "AUTH", "SESSION", "COOKIE")


def _shell_env():
    return {k: v for k, v in os.environ.items()
            if not any(marker in k.upper() for marker in _SECRET_MARKERS)}


def run_tool(name, args, cwd, confirm=False):
    if name == "exec_shell":
        cmd = args.get("command", "")
        if confirm:
            try:
                answer = input(f"    run `{cmd}`? [y/N] ").strip().lower()
            except EOFError:
                answer = ""
            if answer not in {"y", "yes"}:
                return "operator declined to run this command"
        try:
            p = subprocess.run(["bash", "-lc", cmd], cwd=cwd, capture_output=True,
                               text=True, timeout=120, env=_shell_env())
            out = (p.stdout or "") + (p.stderr or "")
            return out[:6000] or "(no output)"
        except subprocess.TimeoutExpired:
            return "timeout after 120s"
    if name == "http_request":
        try:
            r = httpx.request(args.get("method", "GET"), args["url"],
                              headers=args.get("headers") or {},
                              json=args.get("json_body"), timeout=30)
            return f"HTTP {r.status_code}\n{r.text[:6000]}"
        except Exception as e:
            return f"request error: {e}"
    return f"unknown tool {name}"


def chat_once(base, key, model, prompt):
    msg = api(base, key, model,
              [{"role": "user", "content": prompt}])
    print(msg.get("content", "").strip())


def repl(base, key, model):
    history = [{"role": "system", "content": "You are Grok, a helpful assistant "
                "running in a developer sandbox. Be concise."}]
    print("grok REPL — blank line or Ctrl-D to exit")
    while True:
        try:
            line = input("grok> ").strip()
        except EOFError:
            break
        if not line:
            break
        history.append({"role": "user", "content": line})
        msg = api(base, key, model, history)
        history.append(msg)
        print(msg.get("content", "").strip())


def agent(base, key, model, task, cwd, max_steps, confirm=False):
    print(f"[agent mode] tools live in sandbox (cwd={cwd}). task: {task}\n")
    messages = [
        {"role": "system", "content":
         "You are Grok operating as an autonomous agent inside an isolated, "
         "ephemeral developer sandbox. You have exec_shell (run commands here) and "
         "http_request (reach local services). Work step by step toward the task; "
         "inspect output; stop when done and summarise what you found/did. Only the "
         "sandbox is reachable."},
        {"role": "user", "content": task}]
    for step in range(1, max_steps + 1):
        msg = api(base, key, model, messages, AGENT_TOOLS)
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        if msg.get("content"):
            print(f"[{step}] {msg['content'].strip()[:500]}")
        if not calls:
            break
        for tc in calls:
            fn = tc["function"]
            try:
                a = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                a = {}
            preview = (a.get("command") or a.get("url") or "")[:80]
            print(f"    -> {fn['name']}: {preview}")
            out = run_tool(fn["name"], a, cwd, confirm)
            messages.append({"role": "tool", "tool_call_id": tc["id"], "content": out})
    print("\n[agent done]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?", help="one-shot prompt; omit for REPL")
    ap.add_argument("--agent", metavar="TASK", help="run as an autonomous agent")
    ap.add_argument("--provider", choices=list(PROVIDERS), default="grok")
    ap.add_argument("--base-url")
    ap.add_argument("--model", default="grok-4")
    ap.add_argument("--api-key")
    ap.add_argument("--cwd", default=os.getcwd())
    ap.add_argument("--max-steps", type=int, default=20)
    ap.add_argument("--confirm", action="store_true",
                    help="agent mode: ask before running each shell command")
    a = ap.parse_args()
    default_base, key_env = PROVIDERS[a.provider]
    base = (a.base_url or default_base)
    if not base:
        sys.exit("--base-url required for --provider custom")
    key = a.api_key or os.environ.get(key_env, "")
    if not key:
        sys.exit(f"set {key_env} (or pass --api-key). e.g. export XAI_API_KEY=...")
    base = base.rstrip("/")
    if a.agent:
        agent(base, key, a.model, a.agent, a.cwd, a.max_steps, a.confirm)
    elif a.prompt:
        chat_once(base, key, a.model, a.prompt)
    else:
        repl(base, key, a.model)


if __name__ == "__main__":
    main()
