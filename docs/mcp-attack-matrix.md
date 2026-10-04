# The 8-vector MCP attack matrix

The Model Context Protocol (MCP) standardises how an AI **host** (the app running
the model) connects to **servers** that provide capabilities. Host and server
negotiate a set of **primitives**, and *each primitive is an attack surface*. There
are eight — this is the "8-way protocol" the range is organised around. Module 07
ships one concrete, verifiable vector per primitive (plus rug-pull and RCE).

| # | Primitive | Direction | Purpose | Vector in the lab | Verified by |
|---|-----------|-----------|---------|-------------------|-------------|
| 1 | tools | server→model | model-callable functions | description **poisoning** (hidden instructions hijack the host); **rug-pull**; shell **command-injection → RCE** | oracle / flag |
| 2 | resources | server→model | data readable by URI | **path traversal** in `resources/read` | flag |
| 3 | prompts | server→model | parameterised prompt templates | **argument injection** discloses a privileged template block | flag |
| 4 | sampling | server→client | server asks the host to run the model | server-initiated **context exfiltration** (harvests host system prompt/secrets) | oracle |
| 5 | roots | client→server | client-declared scope boundary | declared roots advertised but **not enforced** server-side | flag |
| 6 | elicitation | server→client | server requests input from the user | **credential phishing** via a host that auto-answers | oracle |
| 7 | logging | server→client | log notifications | **sensitive-data leak** (session token) at debug level | flag |
| 8 | completion | server→model | argument autocompletion | **secret enumeration** (completion backed by secret store) | flag |

## Why this framing beats an ad-hoc list

Prior vulnerable-MCP projects enumerate a grab-bag of ~10 challenges. Organising by
the **protocol surface** makes the attack model legible:

- **Four primitives flow server→model** (tools, resources, prompts, completion) —
  these are *indirect prompt-injection channels*: untrusted server content enters
  the model's context.
- **Two flow server→client** (sampling, elicitation) — these let a malicious
  **server drive the host**, turning the host's model/credentials into the
  attacker's tools (classic confused deputy).
- **One is the client's only declared boundary** (roots) — and it is routinely
  **unenforced**.
- **Logging** is a side channel that leaks or can be injected.

A single connected server touches all of them, and the host↔server trust is almost
always implicit. That is the core lesson.

## Mapping to published taxonomies

These vectors align with the **OWASP MCP Top 10** themes and the Cloud Security
Alliance's MCP attack-surface analysis — tool poisoning, confused deputy, token
passthrough, SSRF via tool connectors, rogue server registration, rug pulls, tool
shadowing — and with **OWASP LLM Top 10** (LLM01 Prompt Injection, LLM02 Sensitive
Information Disclosure, LLM06 Excessive Agency, LLM08 Vector/Embedding issues). The
lab's `tools` vector covers poisoning/rug-pull/RCE; `roots`/`resources` cover the
confined-access failures; `sampling`/`elicitation` cover server→client abuse.

## Transport note (faithfulness)

Real MCP uses JSON-RPC 2.0 over stdio or Streamable HTTP, and sampling/elicitation
are genuine *server→client* requests. The lab speaks JSON-RPC over plain HTTP and
performs the server→client calls as nested HTTP POSTs to a callback URL the host
advertises at `initialize`. The **method semantics and every vulnerability are
faithful**; only the framing is simplified so everything is `curl`-able and the
verifier can be deterministic. An extension (see the module lesson) is to swap the
HTTP shim for the official MCP SDK over stdio and re-run the vectors.

## Extensions

- **Unicode concealment** of the tool-poisoning payload (invisible tag characters
  that render blank in review but reach the model).
- **Token passthrough / confused deputy** as a dedicated vector (server forwards
  the host's OAuth token to a third service).
- **Tool shadowing / cross-server** name collisions between two connected servers.
