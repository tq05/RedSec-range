# RedSec Range — Attack Worksheet

> **What this is.** A move-by-move worksheet for working the range *without* spoilers.
> For each challenge it tells you the **objective**, the **attack path** (the class of
> technique and roughly where to aim), and the **surface** to look at — but **not the
> payload and not the flag**. Think of it as the opening theory, not the engine line:
> enough to know what move to find, not the move itself.
>
> Stuck? `redsec hint <mod> <challenge>` gives graded hints (the last hint is usually
> close to the answer). The full answers live in **[SOLUTIONS.md](SOLUTIONS.md)** —
> use that only to check yourself. A visual map of the whole range is in
> **[OVERVIEW.md](OVERVIEW.md)**.
>
> **Setup.** Bring the range up (`./scripts/sandbox-up.sh`, or `redsec up <mod>`),
> then `range status` for the target URLs. Submit flags with
> `redsec submit <mod> <challenge> 'REDSEC{...}'`; for side-effect (oracle) challenges
> run the exploit and then `redsec verify <mod> <challenge>`.

Legend: **F** = recover a flag and submit it · **O** = cause a side effect the
verifier observes (the exfil sink / a privileged action) · **A** = submit a written
artifact. Difficulty: 🟢 beginner · 🟡 intermediate · 🔴 advanced · ⚫ expert.

---

## Module 01 — Introduction / First Contact
*Objective: run the core loop once — talk to a target, coax out a secret, submit it.*

| Challenge | | Diff | Attack path (no spoilers) | Surface |
|---|---|---|---|---|
| `first-contact` | F | 🟢 | The assistant holds a secret in its own instructions and has a rule not to reveal it. Get it to repeat its instructions back to you. | `POST /chat` |

**Why it works:** an LLM's "system" instructions are just text in its context with no
privileged status — a model with no real instruction hierarchy will recite them when
asked the right way. This is the seed of every later module.

---

## Module 02 — Reconnaissance
*Objective: fingerprint the AI and find what leaks before you attack. (OWASP LLM07/LLM02)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `fingerprint-model` | F | 🟢 | Identify the backing model/provider from what the app volunteers. Read the headers and the landing-page source, then follow the build-metadata trail it hints at. | response headers, `/`, a version endpoint |
| `enumerate-surfaces` | F | 🟢 | Find a route nobody linked. Ask what a crawler is told to avoid, then go exactly there. | `/robots.txt` → the disallowed path |
| `leak-config` | F | 🟡 | Make the app error out and over-share. Send the chat endpoint a body shape it doesn't expect and read the debug page. | `POST /chat` (malformed body) |

**Why it works:** AI apps leak like any web app — banners, build/version endpoints,
crawler files, verbose errors — plus AI-specific tells (model name, prompt version).
Recon decides which later attack is even possible.

---

## Module 03 — Attacking AI Agents
*Objective: exploit an over-trusting assistant ("Atlas") that retrieves context and calls tools. (LLM01/LLM02/LLM06/LLM07)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `sys-prompt-leak` | F | 🟢 | Direct prompt injection. Override the "never reveal" rule and have it print everything above your message. | `POST /chat` |
| `indirect-injection` | O | 🟡 | Don't talk to it — poison a store it silently reads each turn, so a normal turn carries your instruction. Make it mail its own system prompt out. | `POST /notes`, then any `/chat` |
| `tool-exfil` | O | 🟡 | Excessive agency. You can't read the API key, but the agent can and it can send mail anywhere — make it include the secret for you. | the `send_message` tool via `/chat` |
| `memory-poisoning` | O | 🔴 | Persistence. Put an instruction into long-term memory, then fire it from a *later, benign* turn with no attacker input in sight. | the `remember` tool, then a 2nd turn |

**Why it works:** the agent treats every channel — your message, retrieved notes,
memory, tool output — as equally trustworthy. Whoever writes to any channel writes
instructions. Indirect injection (poisoning a data source) is the key idea the rest of
the course builds on.

---

## Module 04 — Multi-Agent Systems & A2A
*Objective: exploit trust between cooperating agents (planner → reviewer). (LLM01/LLM06)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `trust-exploitation` | O | 🔴 | Transitive injection. The lowest-trust input (a ticket) rides the planner's plan into the reviewer, which acts on it. Smuggle an action in through the ticket. | `POST /submit` |
| `message-manipulation` | O | 🔴 | The inter-agent bus is unauthenticated. Forge a message straight to the reviewer. | `POST /bus/send` |
| `agent-impersonation` | O | 🔴 | No attestation on identity. Register yourself as a trusted agent, then approve your own malicious action. | `POST /agents/register` → `/approve` |
| `session-smuggling` | O | ⚫ **impossible** | A guard now rejects any single session turn carrying the directive token. Smuggle it across a **stateful A2A session** so it only forms when the victim concatenates turns. *(No walkthrough — answer sealed in `modules/04-multi-agent-a2a/solution/SEALED.md`.)* | `POST /session/{id}/turn` ×N → `/session/{id}/deliver` |

**Why it works:** every agent-to-agent message is an injection channel, and agents
treat each other's output as trusted input. One foothold propagates; identity is
assumed, not proven. The impossible tier models **agent session smuggling** (Unit42):
the guard inspects each turn in isolation, but the victim acts on the concatenation.

---

## Module 05 — RAG Pipelines
*Objective: compromise a retrieval-augmented chatbot. (LLM01/LLM08)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `knowledge-poisoning` | O | 🟡 | Ingest a document whose body carries an instruction; trigger it with a question that retrieves it. | `POST /ingest`, then `/chat` |
| `retrieval-manipulation` | O | 🔴 | Your payload only lands if it's retrieved. Beat the real documents for the victim's query against a naive term-frequency ranker. | `POST /ingest` (then query) |
| `citation-spoofing` | O | 🔴 | You control the source metadata and it's shown as a citation. Make attacker content appear under an authoritative-looking source. | `POST /ingest` `source` field |

**Why it works:** RAG is indirect injection with a retrieval step — win retrieval and
you win the injection, and "grounded" output makes users trust it more.

---

## Module 06 — Attacking Embeddings
*Objective: treat embeddings as lossy encodings whose structure leaks. (LLM08/LLM02)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `embedding-inversion` | F | ⚫ | Stored vectors are exposed. Reconstruct the source text of a secret record from its vector. | `GET /records`, `POST /decode` |
| `membership-inference` | F | 🔴 | Decide whether a specific record is in the store by how the distance behaves for an exact candidate. | `POST /embed`, `POST /search` |
| `embedding-collision` | F | 🔴 | A text check is enforced on the embedding, which ignores word order. Craft a *different* text that embeds identically to the banned one. | `GET /protected`, `POST /collide` |

**Why it works:** "we only store embeddings" is not a privacy control — embeddings
invert, similarity reveals membership, and lossy encodings collide.

---

## Module 07 — MCP & Tool Surfaces (the 8-vector matrix)
*Objective: one flaw per MCP protocol primitive, plus rug-pull and RCE. (LLM01/02/06, MCP01-05)*

| Challenge | | Diff | Primitive | Attack path | Surface |
|---|---|---|---|---|---|
| `tool-poisoning` | O | 🔴 | tools | A tool *description* carries hidden instructions the host folds into its context. You send nothing malicious — just talk to the host and let it act. | `tools/list`, then host `POST /chat` |
| `resource-traversal` | F | 🟡 | resources | The resource reader joins your URI onto a base dir with no normalization. Escape it. | `resources/read` |
| `prompt-injection` | F | 🟡 | prompts | A template appends a privileged block for privileged-looking arguments. Claim to be one. | `prompts/get` (`persona` arg) |
| `sampling-abuse` | O | 🔴 | sampling | A server tool asks the host to run *its own* model over host context, then exfiltrates the result. Trigger it through the host. | host `POST /use_tool` (research) |
| `roots-bypass` | F | 🟡 | roots | The client declared a root; the server never enforces it. Read outside it (hint: absolute paths). | `tools/call` read_file |
| `elicitation-phishing` | O | 🔴 | elicitation | The server asks the user for a credential at runtime; the host auto-answers from its own secrets. Trigger the flow. | host `POST /use_tool` (setup_account) |
| `logging-leak` | F | 🟢 | logging | Turn verbosity up and the server over-shares in its logs. | `logging/setLevel` → any call |
| `completion-leak` | F | 🟢 | completion | Argument autocompletion is backed by the secret store. Complete the right field. | `completion/complete` |
| `rug-pull` | F | 🟡 | tools | What you approve isn't what you get. List the tools again after "approval." | `tools/list` (twice) |
| `command-injection` | F | 🔴 | tools→RCE | A tool shells out with your input. Inject a second command. | `tools/call` run_diagnostic |

**Why it works:** MCP exposes eight primitive surfaces and the host↔server trust is
usually implicit. Four primitives feed untrusted server content into the model
(injection channels); two let a malicious server drive the host (confused deputy); one
(roots) is the only declared boundary and it's unenforced. See
[OVERVIEW.md](OVERVIEW.md) for the matrix diagram.

---

## Module 08 — Supply Chain
*Objective: compromise artifacts before deployment. (LLM03/LLM04)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `malicious-weights` | O | 🔴 | A model artifact is deserialized unsafely on load. Ship one that runs code on load and phones the sink. | `POST /load` |
| `poisoned-dataset` | F | 🔴 | Training data is unvalidated. Map a rare trigger token to a privileged label, then invoke it. | `POST /train`, `POST /predict` |
| `backdoored-adapter` | F | 🔴 | Adapters are merged unaudited. Hide a trigger in one, then fire it. | `POST /merge_adapter`, `/predict` |
| `dependency-confusion` | F | 🔴 | The resolver prefers the highest version across indices. Publish a higher-versioned clash of an internal name. | `POST /public/publish`, `/resolve` |

**Why it works:** weights, data, adapters and dependencies are trusted artifacts that
are rarely verified end-to-end — the cheapest place to compromise a model is before it
runs.

---

## Module 09 — Infrastructure & Deployment
*Objective: attack the platform under the model. (LLM02)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `metadata-ssrf` | F | 🔴 | A server-side fetch has no allow-list. First discover the internal metadata address (recon), then make the server fetch its credentials for you. | `GET /debug/config`, `POST /fetch` |
| `open-inference-api` | F | 🟢 | A privileged route has no auth. The landing page lists the routes. | `/` → an admin route |
| `registry-secrets` | F | 🟡 | Secrets are committed into model metadata. List the models, read a model card. | `/registry/models`, model card |

**Why it works:** models run on ordinary, often over-privileged infrastructure — a
fetch primitive, an open port, or a leaky registry turns a model bug into a cloud
compromise.

---

## Module 10 — Threat Modeling *(written, not exploited)*
*Objective: turn hands-on findings into structured analysis. Submit a markdown artifact per challenge.*

| Challenge | | Diff | What to produce |
|---|---|---|---|
| `asset-inventory` | A | 🟡 | List the high-value assets: model, prompts/system-prompt, secrets, tools, data (RAG/memory/embeddings), agents. |
| `trust-boundaries` | A | 🟡 | Mark every place untrusted data meets the model, and the host↔server boundary. Name why each is untrusted. |
| `attack-paths` | A | 🔴 | Chain ≥3 module vectors into ranked end-to-end paths, referencing the techniques. |

Submit with `redsec verify 10 <challenge> --artifact-file FILE.md`.

---

## Module 11 — Capstone *(chain it all)*
*Objective: initial access → pivot → exfiltrate the crown jewel. (LLM01/02/06)*

| Challenge | | Diff | Attack path | Surface |
|---|---|---|---|---|
| `initial-access` | O | 🔴 | Reuse Module 03/05: poison the notes store the assistant trusts; a benign turn fires your implant. | `POST /notes`, then `/chat` |
| `pivot-vault` | O | ⚫ | The assistant can read an internal vault you can't. Drive its tool to fetch a vault record — your confused-deputy pivot. | the `report_record` tool |
| `exfil-crown-jewel` | O | ⚫ | Same pivot, the crown record. The assistant's ambient authority exfiltrates it. | `report_record` (crown) |

**Why it works:** no single bug wins — you chain an injection foothold with the
assistant's ambient authority over a sensitive system (a classic confused deputy).

---

### Scoring your run
`redsec score` shows solved/points per module. Total available: **41 challenges**.
When you finish a module, read its `lesson.md` "Defenses" section — the point of the
range is to learn the fix, not just the exploit.
