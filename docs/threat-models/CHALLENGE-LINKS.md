# Full links to every challenge threat model

This index links directly to the complete defensive threat model for each of
the **110 challenge concepts** and **162 declared variants** in the RedSec catalog.

| Range | Challenge | Title | Full GitHub link |
|---|---|---|---|
| `builtin` | `builtin/01/first-contact` | First contact -- coax the orientation flag out of the Guide | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-01-first-contact> |
| `builtin` | `builtin/02/fingerprint-model` | Fingerprint the backing model/provider | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-02-fingerprint-model> |
| `builtin` | `builtin/02/enumerate-surfaces` | Discover an undocumented internal endpoint | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-02-enumerate-surfaces> |
| `builtin` | `builtin/02/leak-config` | Dump service config via a verbose error | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-02-leak-config> |
| `builtin` | `builtin/03/sys-prompt-leak` | Direct prompt injection -> leak the system prompt | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-03-sys-prompt-leak> |
| `builtin` | `builtin/03/indirect-injection` | Indirect prompt injection via auto-retrieved notes | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-03-indirect-injection> |
| `builtin` | `builtin/03/tool-exfil` | Excessive agency -> exfiltrate the mail API key | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-03-tool-exfil> |
| `builtin` | `builtin/03/memory-poisoning` | Memory poisoning -> persistence across turns | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-03-memory-poisoning> |
| `builtin` | `builtin/04/trust-exploitation` | Transitive trust -> reviewer acts on your ticket | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-04-trust-exploitation> |
| `builtin` | `builtin/04/message-manipulation` | Send an unsigned A2A JSON-RPC message | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-04-message-manipulation> |
| `builtin` | `builtin/04/agent-impersonation` | Impersonate a trusted approver | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-04-agent-impersonation> |
| `builtin` | `builtin/04/session-smuggling` | Agent session smuggling across a stateful A2A session | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-04-session-smuggling> |
| `builtin` | `builtin/05/knowledge-poisoning` | Poison the knowledge base | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-05-knowledge-poisoning> |
| `builtin` | `builtin/05/retrieval-manipulation` | Out-rank the real documents for a victim query | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-05-retrieval-manipulation> |
| `builtin` | `builtin/05/citation-spoofing` | Spoof a trusted citation | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-05-citation-spoofing> |
| `builtin` | `builtin/06/embedding-inversion` | Reconstruct source text with a reference corpus | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-06-embedding-inversion> |
| `builtin` | `builtin/06/membership-inference` | Confirm a record is present in the store | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-06-membership-inference> |
| `builtin` | `builtin/06/embedding-collision` | Bypass a text check via an embedding collision | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-06-embedding-collision> |
| `builtin` | `builtin/07/tool-poisoning` | tools: tool-description poisoning hijacks the host | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-tool-poisoning> |
| `builtin` | `builtin/07/resource-traversal` | resources: path traversal in resources/read | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-resource-traversal> |
| `builtin` | `builtin/07/prompt-injection` | prompts: argument injection discloses a privileged template block | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-prompt-injection> |
| `builtin` | `builtin/07/sampling-abuse` | sampling: server-initiated sampling exfiltrates host context | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-sampling-abuse> |
| `builtin` | `builtin/07/roots-bypass` | roots: declared client roots are not enforced | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-roots-bypass> |
| `builtin` | `builtin/07/elicitation-phishing` | elicitation: server elicits credentials the host auto-answers | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-elicitation-phishing> |
| `builtin` | `builtin/07/logging-leak` | logging: debug log notifications leak a session token | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-logging-leak> |
| `builtin` | `builtin/07/completion-leak` | completion: autocompletion enumerates secret values | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-completion-leak> |
| `builtin` | `builtin/07/rug-pull` | tools: rug-pull -- tool behaviour changes after approval | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-rug-pull> |
| `builtin` | `builtin/07/command-injection` | tools: command injection -> remote code execution | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-command-injection> |
| `builtin` | `builtin/07/header-routing-confusion` | 2026 routing: header/body policy desynchronization | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-header-routing-confusion> |
| `builtin` | `builtin/07/unicode-tool-poisoning` | tools: Unicode-concealed tool-description poisoning past the scanner | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-07-unicode-tool-poisoning> |
| `builtin` | `builtin/08/malicious-weights` | RCE via unsafe model deserialization | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-08-malicious-weights> |
| `builtin` | `builtin/08/poisoned-dataset` | Backdoor the model via dataset poisoning | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-08-poisoned-dataset> |
| `builtin` | `builtin/08/backdoored-adapter` | Inject behaviour via a backdoored adapter | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-08-backdoored-adapter> |
| `builtin` | `builtin/08/dependency-confusion` | Win dependency confusion | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-08-dependency-confusion> |
| `builtin` | `builtin/09/metadata-ssrf` | SSRF to cloud metadata -> steal role credentials | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-09-metadata-ssrf> |
| `builtin` | `builtin/09/open-inference-api` | Abuse an unauthenticated admin inference route | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-09-open-inference-api> |
| `builtin` | `builtin/09/registry-secrets` | Recover a secret from a model card | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-09-registry-secrets> |
| `builtin` | `builtin/10/asset-inventory` | Inventory the high-value AI assets | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-10-asset-inventory> |
| `builtin` | `builtin/10/trust-boundaries` | Map trust boundaries & data flows | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-10-trust-boundaries> |
| `builtin` | `builtin/10/attack-paths` | Enumerate end-to-end attack paths | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-10-attack-paths> |
| `builtin` | `builtin/11/initial-access` | Initial access via indirect injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-11-initial-access> |
| `builtin` | `builtin/11/pivot-vault` | Pivot through ambient authority to the vault | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-11-pivot-vault> |
| `builtin` | `builtin/11/exfil-crown-jewel` | Exfiltrate the crown-jewel secret | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/builtin.md#builtin-11-exfil-crown-jewel> |
| `dvaa` | `dvaa/L1-01` | Extract the System Prompt | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l1-01> |
| `dvaa` | `dvaa/L1-02` | API Key Leak | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l1-02> |
| `dvaa` | `dvaa/L1-03` | Basic Prompt Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l1-03> |
| `dvaa` | `dvaa/L2-01` | Jailbreak via Roleplay | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-01> |
| `dvaa` | `dvaa/L2-02` | Context Window Manipulation | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-02> |
| `dvaa` | `dvaa/L2-03` | MCP Path Traversal | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-03> |
| `dvaa` | `dvaa/L2-04` | Persistent Memory Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-04> |
| `dvaa` | `dvaa/L2-05` | Memory Credential Extraction | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-05> |
| `dvaa` | `dvaa/L2-06` | Context Padding Attack | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-06> |
| `dvaa` | `dvaa/L2-07` | Safety Instruction Displacement | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-07> |
| `dvaa` | `dvaa/L2-08` | Malicious Tool Registration | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-08> |
| `dvaa` | `dvaa/L2-09` | Tool Call MITM | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l2-09> |
| `dvaa` | `dvaa/L3-01` | Chained Prompt Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-01> |
| `dvaa` | `dvaa/L3-02` | SSRF via MCP | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-02> |
| `dvaa` | `dvaa/L3-03` | Self-Replicating Memory Entry | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-03> |
| `dvaa` | `dvaa/L3-04` | System Prompt Extraction via Context Pressure | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-04> |
| `dvaa` | `dvaa/L3-05` | Tool Typosquatting | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-05> |
| `dvaa` | `dvaa/L3-06` | Tool Chain Data Exfiltration | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-06> |
| `dvaa` | `dvaa/L3-07` | Tool Shadowing | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-07> |
| `dvaa` | `dvaa/L3-08` | Traffic Redirection Attack | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l3-08> |
| `dvaa` | `dvaa/L4-01` | Compromise SecureBot | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l4-01> |
| `dvaa` | `dvaa/L4-02` | Agent-to-Agent Attack Chain | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvaa.md#dvaa-l4-02> |
| `mcpgoat` | `mcpgoat/A1` | Tool Poisoning | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-a1> |
| `mcpgoat` | `mcpgoat/A2` | Tool Shadowing / Trusted-Tool Override | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-a2> |
| `mcpgoat` | `mcpgoat/A3` | Rug Pull / Tool Mutation (TOCTOU) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-a3> |
| `mcpgoat` | `mcpgoat/B1` | Indirect Prompt Injection via Tool Output | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-b1> |
| `mcpgoat` | `mcpgoat/D1` | Command Injection (RCE) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d1> |
| `mcpgoat` | `mcpgoat/D2` | Path Traversal / Arbitrary File Read | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d2> |
| `mcpgoat` | `mcpgoat/D3` | Server-Side Request Forgery | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d3> |
| `mcpgoat` | `mcpgoat/D4` | SQL Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d4> |
| `mcpgoat` | `mcpgoat/C2` | Broken Authorization / Confused Deputy | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-c2> |
| `mcpgoat` | `mcpgoat/C3` | Insecure Direct Object Reference | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-c3> |
| `mcpgoat` | `mcpgoat/E1` | Sensitive Data Exposure | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-e1> |
| `mcpgoat` | `mcpgoat/A9` | Invisible-Text Tool Poisoning | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-a9> |
| `mcpgoat` | `mcpgoat/B2` | Indirect Injection via Resource Content | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-b2> |
| `mcpgoat` | `mcpgoat/B3` | Prompt-Template Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-b3> |
| `mcpgoat` | `mcpgoat/B5` | Sampling Abuse (server-driven LLM calls) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-b5> |
| `mcpgoat` | `mcpgoat/C4` | OAuth Token-Audience Confusion | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-c4> |
| `mcpgoat` | `mcpgoat/D6` | Server-Side Template Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d6> |
| `mcpgoat` | `mcpgoat/F1` | DNS Rebinding / Missing Origin Validation | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-f1> |
| `mcpgoat` | `mcpgoat/F2` | CORS Misconfiguration | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-f2> |
| `mcpgoat` | `mcpgoat/C6` | Predictable Session IDs (hijack) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-c6> |
| `mcpgoat` | `mcpgoat/G1` | Unbounded Consumption (cost/DoS) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-g1> |
| `mcpgoat` | `mcpgoat/G4` | Regular-Expression DoS (ReDoS) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-g4> |
| `mcpgoat` | `mcpgoat/D5` | NoSQL Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d5> |
| `mcpgoat` | `mcpgoat/D7` | XML External Entity (XXE) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d7> |
| `mcpgoat` | `mcpgoat/D8` | Insecure Deserialization (prototype pollution) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-d8> |
| `mcpgoat` | `mcpgoat/H1` | Supply Chain (typosquat / unsigned package) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/mcpgoat.md#mcpgoat-h1> |
| `dvmcp` | `dvmcp/01` | Basic Prompt Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-01> |
| `dvmcp` | `dvmcp/02` | Tool Poisoning | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-02> |
| `dvmcp` | `dvmcp/03` | Excessive Permission Scope | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-03> |
| `dvmcp` | `dvmcp/04` | Rug Pull Attack | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-04> |
| `dvmcp` | `dvmcp/05` | Tool Shadowing | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-05> |
| `dvmcp` | `dvmcp/06` | Indirect Prompt Injection | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-06> |
| `dvmcp` | `dvmcp/07` | Token Theft | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-07> |
| `dvmcp` | `dvmcp/08` | Malicious Code Execution | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-08> |
| `dvmcp` | `dvmcp/09` | Remote Access Control | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-09> |
| `dvmcp` | `dvmcp/10` | Multi-Vector Attack | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/dvmcp.md#dvmcp-10> |
| `appsecco-mcp` | `appsecco-mcp/filesystem-workspace-actions` | Filesystem Workspace Actions | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-filesystem-workspace-actions> |
| `appsecco-mcp` | `appsecco-mcp/indirect-prompt-injection` | Indirect Prompt Injection (stdio) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-indirect-prompt-injection> |
| `appsecco-mcp` | `appsecco-mcp/indirect-prompt-injection-remote` | Indirect Prompt Injection (HTTP+SSE) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-indirect-prompt-injection-remote> |
| `appsecco-mcp` | `appsecco-mcp/malicious-code-exec` | Malicious Code Execution | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-malicious-code-exec> |
| `appsecco-mcp` | `appsecco-mcp/malicious-tools` | Malicious Tools | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-malicious-tools> |
| `appsecco-mcp` | `appsecco-mcp/namespace-typosquatting` | Namespace Typosquatting | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-namespace-typosquatting> |
| `appsecco-mcp` | `appsecco-mcp/outdated-packages` | Outdated Packages | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-outdated-packages> |
| `appsecco-mcp` | `appsecco-mcp/secrets-pii` | Secrets and PII Exposure | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-secrets-pii> |
| `appsecco-mcp` | `appsecco-mcp/wikipedia-streamable` | Wikipedia (Streamable HTTP) | <https://github.com/tq05/RedSec-range/blob/main/docs/threat-models/generated/appsecco-mcp.md#appsecco-mcp-wikipedia-streamable> |

Runtime exploitability is **not verified—outside the current scope**.
