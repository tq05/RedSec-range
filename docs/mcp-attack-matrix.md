# The version-aware MCP attack matrix

The Model Context Protocol (MCP) standardises how an AI **host** (the app running
the model) connects to **servers** that provide capabilities. Host and server
negotiate protocol features, and each capability or transport decision is an attack
surface. The original matrix is pinned to **MCP 2025-06-18** and covers eight server,
client and utility surfaces used by that ecosystem. Module 07 ships one concrete,
verifiable vector per surface, plus rug-pull, RCE and a current-spec Streamable HTTP
policy-desynchronization challenge.

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

## Current protocol delta (2026-07-28)

The matrix above remains useful for assessing deployed and legacy MCP systems, but
it is not the current taxonomy of core primitives. In MCP 2026-07-28:

- **tools, resources and prompts** are the three core server primitives;
- **elicitation** remains a client capability and uses Multi Round-Trip Requests;
- **completion** remains a utility;
- **roots, sampling and logging are deprecated**, so assess them where older
  clients and servers still negotiate them;
- the protocol core is stateless, `server/discover` replaces the old handshake,
  and Streamable HTTP requires `Mcp-Method`/`Mcp-Name` routing headers.

The `header-routing-confusion` challenge targets that last change: a gateway
authorizes the routing headers while the application dispatches the JSON body. The
attacker claims the harmless `whoami` tool in `Mcp-Name` but calls the restricted
`admin_report` tool in `params.name`. The mitigation is a single canonical request
representation and a hard rejection when header and body identities disagree.

## Why this framing beats an ad-hoc list

Prior vulnerable-MCP projects enumerate a grab-bag of ~10 challenges. Organising by
the **protocol surface** makes the attack model legible:

- **Four surfaces flow server→model** (tools, resources, prompts, completion) —
  these are *indirect prompt-injection channels*: untrusted server content enters
  the model's context.
- **Two legacy/client surfaces flow server→client** (sampling, elicitation) — these let a malicious
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
Information Disclosure, LLM06 Excessive Agency). The
lab's `tools` vector covers poisoning/rug-pull/RCE; `roots`/`resources` cover the
confined-access failures; `sampling`/`elicitation` cover server→client abuse.

## Transport note (faithfulness)

Real MCP uses JSON-RPC 2.0 over stdio or Streamable HTTP. The pinned 2025 lab speaks
JSON-RPC over plain HTTP and models server→client calls as nested callbacks to stay
curl-able and deterministic; it does not claim wire-level conformance. The 2026
routing challenge uses the current protocol version and required routing headers at
`POST /mcp`. An extension is to swap the shim for an official Tier 1 SDK and rerun
the same security assertions.

## Extensions

- **Token passthrough / confused deputy** as a dedicated vector (server forwards
  the host's OAuth token to a third service).
- **Tool shadowing / cross-server** name collisions between two connected servers.
