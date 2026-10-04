# Hooking up another LLM (Grok, OpenAI, local) — two integration points

The range has two independent places a real model can plug in. They answer two
different questions.

| | Target-side | Attacker-side |
|---|---|---|
| **Question** | "How does the vulnerable app behave with a real model behind it?" | "Can an autonomous agent find & demonstrate the weakness?" |
| **What the model is** | the brain of the vulnerable app | the assessor attacking the lab |
| **How** | `REDSEC_LLM_BACKEND` env on the target | `scripts/agent_solver.py --provider` |
| **Default** | deterministic mock (reproducible, offline) | n/a (opt-in) |

Both are provider-agnostic: anything exposing an **OpenAI-compatible
`/chat/completions`** works — Grok (x.ai), OpenAI, or a local server
(ollama/vLLM/LiteLLM). x.ai is reachable from this sandbox (verified); you only need
a key.

---

## Attacker-side: Grok as an autonomous assessor

`scripts/agent_solver.py` hands a challenge to the model — objective, the live
target URLs, and an `http_request` tool — and loops: the model probes/exploits the
target, and after each step the **real verifier** runs. Solved = a recovered flag or
an observed side-effect in the sink.

```bash
# bring the range up first (see interactive-sandbox.md)
./scripts/sandbox-up.sh

# Grok attempts one challenge
XAI_API_KEY=sk-...  python scripts/agent_solver.py 07 resource-traversal \
    --provider grok --model grok-4

# Grok attempts a whole module (all its challenges)
XAI_API_KEY=sk-...  python scripts/agent_solver.py 07 --provider grok --model grok-4

# score the entire range with Grok
for m in 01 02 03 04 05 06 07 08 09 11; do
  XAI_API_KEY=sk-... python scripts/agent_solver.py $m --provider grok --model grok-4
done
```

Other providers:

```bash
OPENAI_API_KEY=sk-... python scripts/agent_solver.py 02 --provider openai --model gpt-4.1
# local / self-hosted / any OpenAI-compatible endpoint:
python scripts/agent_solver.py 02 --provider custom \
    --base-url http://host:11434/v1 --model llama3.1 --api-key x
```

Flags: `--max-steps N` (default 12), `--model`, `--base-url`, `--api-key` (else read
from `XAI_API_KEY` / `OPENAI_API_KEY` / `REDSEC_LLM_API_KEY`).

**Safety scoping.** The `http_request` tool is hard-restricted to the running
range's own loopback targets (read from `~/.redsec/range.json`); the agent is told,
and enforced, to touch nothing else. Point it only at the lab.

**Self-test (no key needed).** The harness is verified end-to-end with a local
OpenAI-compatible stub that drives all three verifier types:

```bash
python -m uvicorn scripts._fake_llm_stub:app --port 8085 &
python scripts/agent_solver.py 02 fingerprint-model --provider custom \
    --base-url http://127.0.0.1:8085/v1 --model stub --api-key x
```

This is also the pattern for building **your own harness**: any loop that calls an
OpenAI-compatible API with the two tools (`http_request` scoped to the lab,
`submit_flag`) and then calls the verifier — `redsec.verify.runner.run_challenge` —
is a valid assessor. `agent_solver.py` is ~150 lines; fork it.

---

## Target-side: a real model inside the vulnerable app

By default the LLM-backed targets use the deterministic mock
(`redsec/mockllm/engine.py`) so challenges are reproducible and free. To make a
target *think* with Grok instead, set these env vars on that target and restart it:

```
REDSEC_LLM_BACKEND=openai
REDSEC_LLM_BASE_URL=https://api.x.ai/v1
REDSEC_LLM_MODEL=grok-4
REDSEC_LLM_API_KEY=sk-...
```

With the persistent range, add them to the module's target env (edit the target's
`env:` in `module.yaml`, or re-run the target container with `-e`). The
vulnerabilities are properties of the *application* (how it assembles context and
wires tools), so they remain exploitable against a real model — just
non-deterministically, which is why the mock is the default for teaching and CI.

> Combining both sides — Grok as the assessor against targets that are themselves
> Grok-backed — turns the range into a live **model-vs-model AI-security eval**.
