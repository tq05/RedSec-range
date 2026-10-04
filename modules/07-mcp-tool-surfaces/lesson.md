# Module 07 — Attacking Model Context Protocol & Tool Surfaces

> **Targets:** `vuln-mcp` (a JSON-RPC MCP server) + `host` ("Beacon", a naive MCP
> client/agent) + the shared `drop` sink.
> **Maps to:** OffSec AI-300 Module 7 · OWASP LLM01/02/06 · OWASP MCP Top 10 ·
> MITRE ATLAS.

## 1. A version-aware protocol surface

The **Model Context Protocol** standardises how an AI *host* (the app running the
model) talks to *servers* that provide capabilities. MCP evolves quickly, so a
security assessment must record the negotiated protocol version.

Most of this lab is pinned to **MCP 2025-06-18**, the revision contemporaneous with
the original AI-300 syllabus. It deliberately covers eight server, client and
utility surfaces used by that ecosystem:

| # | Primitive | Direction | What it does | The vector here |
|---|-----------|-----------|--------------|-----------------|
| 1 | **tools** | server→model | callable functions | description **poisoning**, **rug-pull**, injection→**RCE** |
| 2 | **resources** | server→model | readable data by URI | **path traversal** |
| 3 | **prompts** | server→model | prompt templates | **argument injection** |
| 4 | **sampling** | server→client | server asks host to run the model | **context exfiltration** |
| 5 | **roots** | client→server | declared filesystem/URI scope | **scope not enforced** |
| 6 | **elicitation** | server→client | server asks the user for input | **credential phishing** |
| 7 | **logging** | server→client | log notifications | **sensitive-data leak** |
| 8 | **completion** | server→model | argument autocompletion | **secret enumeration** |

These eight rows are an **attack-surface matrix**, not a claim that every row is a
current core primitive. In **MCP 2026-07-28**, the three core server primitives are
tools, resources and prompts; elicitation remains a client capability; completion is
a utility; roots, sampling and logging are deprecated. Current MCP is stateless,
uses `server/discover` instead of `initialize`, and requires `Mcp-Method` and
`Mcp-Name` routing headers for Streamable HTTP. The final challenge targets that
current routing model.

Notice the directions. Four surfaces flow *from the server into the model's
context* (tools, resources, prompts, completion) — these are **indirect prompt
injection** channels. Two flow *from the server back to the client* (sampling,
elicitation) — these let a malicious **server drive the host**. One is the client's
declared boundary (roots), routinely **unenforced**. This is why MCP widens
the attack surface so much: a single connected server touches every one of them,
and the trust between host and server is almost always implicit.

Transport note: production MCP uses JSON-RPC 2.0 over stdio or Streamable HTTP. The
legacy part of this lab uses a simplified HTTP JSON-RPC shim (`POST /`) and models
server→client calls as nested callbacks so everything is curl-able and deterministic.
The current-spec routing challenge uses `POST /mcp` with the 2026-07-28 version and
routing headers. Read the headers of `targets/vuln-mcp/app.py` and
`targets/host/app.py`.

## 2. Reconnaissance

For the pinned 2025 surface, start with `initialize` and the `*/list` methods:

```bash
MCP=http://localhost:9070
# helper: rpc <method> [json-params]   (params default to {})
rpc(){ curl -s $MCP -H 'content-type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$1\",\"params\":${2:-{}}}"; }
rpc initialize '{"protocolVersion":"2025-06-18","capabilities":{"roots":["file://workspace/"]}}'
rpc tools/list
rpc resources/list
rpc prompts/list
```

Compare that with current stateless discovery:

```bash
rpc server/discover '{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"student","version":"1"}}}'
```

`serverInfo` leaks the absolute `appDir` and `workspaceRoot` — note them, you'll
need the layout for the roots and RCE challenges. Read **every** tool description
in full, including non-printing characters.

## 3. The vectors

Work them in the order below (`redsec hint 07 <challenge>` for nudges). Eight are
exploited by sending requests straight to `vuln-mcp` and reading the response (flag
challenges). Four require the host, including the sealed Unicode challenge — you
poison it or trigger a server→client callback, and the `drop` sink proves the effect
(oracle challenges).

### tools (1a) — `tool-poisoning` *(oracle)*
`knowledge_base`'s description contains an `<IMPORTANT>` block with an `ACTION`
line. Beacon folds tool descriptions into its model context and trusts them, so the
instruction executes the next time anyone chats with it — exfiltrating Beacon's own
secrets. You send nothing malicious; you just `POST /chat` to Beacon. This is the
canonical MCP supply-chain attack: a compromised or malicious server owns every
host that connects.

### resources (2) — `resource-traversal` *(flag)*
`resources/read` joins your `file://` URI onto a base directory with no
normalization. `file://../secret/resource.flag` escapes it. (Same class as classic
web path traversal — the MCP resource layer just reintroduced it.)

### prompts (3) — `prompt-injection` *(flag)*
`prompts/get` for `support_reply` appends an internal block when the
attacker-controlled `persona` argument looks privileged. Set `persona` to `admin`.
Prompt *templates* are code; untrusted arguments concatenated into them are an
injection sink.

### sampling (4) — `sampling-abuse` *(oracle)*
The `research` tool makes the server call back `sampling/createMessage` — asking the
*host* to run its model. Beacon runs it against its own system context and returns
the result, which the server exfiltrates. A server granted sampling can turn the
host's own model into an oracle over host-side secrets, and bill the host for it.
Trigger it with `POST /use_tool {"name":"research"}`.

### roots (5) — `roots-bypass` *(flag)*
The host declared `file://workspace/` as its root. The server advertises it but
never enforces it: `read_file` blocks `..` yet happily reads any **absolute** path.
Declared scope is not enforced scope. Read `{appDir}/restricted/roots.flag`.

### elicitation (6) — `elicitation-phishing` *(oracle)*
`setup_account` makes the server call back `elicitation/create`, requesting an
`api_key`. Beacon is misconfigured to auto-answer elicitations from its own
credential store, so it hands the secret over and the server exfiltrates it. A
malicious server can phish the user (or an over-eager client) through the trusted UI.
Trigger with `POST /use_tool {"name":"setup_account"}`.

### logging (7) — `logging-leak` *(flag)*
`logging/setLevel` to `debug` makes the server over-share: its log notifications
include the session token. Set the level, make any call, read `_logs`.

### completion (8) — `completion-leak` *(flag)*
`completion/complete` backs the `token`/`api_key` argument with the secret store, so
autocompletion *is* an enumeration oracle. Ask it to complete that argument.

### tools (1b) — `rug-pull` *(flag)*
The first `tools/list` (what the user reviews and approves) is benign. List again —
the `weather` tool's description has changed to a malicious one. Approval at install
time means nothing if the server can mutate definitions afterward (TOCTOU).

### tools (1c) — `command-injection` *(flag)*
`run_diagnostic` builds a shell command from your `host` argument. Inject with `;`
and read `{appDir}/restricted/rce.flag`. A tool implementation is just code behind
a model-callable interface — all the usual injection bugs apply, now reachable by
anything that can influence the model.

### Streamable HTTP — `header-routing-confusion` *(flag)*

MCP 2026-07-28 requires `Mcp-Method` and `Mcp-Name` headers so gateways can route,
meter and authorize requests without parsing every JSON body. The lab's gateway
allows anonymous callers to invoke only `whoami` **according to the headers**, while
the application dispatches `params.name` **from the body**. Send `Mcp-Name: whoami`
but call `admin_report` in the JSON. This is a policy-enforcement-point mismatch:
every layer validated a different request.

## 4. Chaining & the confused deputy

Each vector is bad alone; chained they are worse. The host holds **ambient
authority** (its credentials, its filesystem, its model) and will exercise it on
behalf of whatever text reaches the model. A poisoned tool (1a) that instructs the
host to call `read_file` (5) or `run_diagnostic` (1c) turns the host into a
**confused deputy** executing the server's will with the host's privileges. Capstone
(Module 11) asks you to build such a chain end-to-end.

## 5. Defensive takeaways

| Vector | Mitigation (defence-in-depth) |
|---|---|
| Tool poisoning / rug-pull | Pin & review tool definitions; detect drift; treat descriptions as untrusted; isolate servers |
| Resource traversal / RCE | Canonicalize & sandbox paths; never shell out on tool input; parameterize |
| Prompt argument injection | Treat template args as untrusted; structured templating; no privileged branches on user args |
| Sampling abuse | Gate/consent per sampling request; scope & rate-limit; strip host context |
| Roots not enforced | **Enforce** declared roots server-side and client-side; deny by default |
| Elicitation phishing | Never auto-answer elicitations; show provenance; human approval for secrets |
| Logging leak | Scrub secrets from logs; least-verbose by default |
| Completion enumeration | Never back completion with secret data; authorize per field |
| Header/body policy desync | Canonicalize once; reject header/body disagreement; authorize the exact dispatched method/tool |

The through-line: **the host↔server trust boundary is real and must be enforced on
both sides.** Authenticate servers, pin their capabilities, treat everything they
send as untrusted data, and give the host the least authority that still works.

## 6. Extensions

- **Real transport.** Swap the HTTP JSON-RPC shim for the official MCP SDK over
  stdio/Streamable HTTP and re-run the vectors.
- **Token passthrough / confused deputy** as a dedicated vector (OWASP MCP): add a
  server that forwards the host's OAuth token to a third service.
- **Cross-server tool shadowing.** Connect two servers that publish the same tool
  name and exploit a host with ambiguous resolution or stale cached definitions.
