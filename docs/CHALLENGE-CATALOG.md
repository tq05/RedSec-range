# Challenge catalog by range

This file is generated from the built-in module manifests and
[`ranges/catalog.yaml`](../ranges/catalog.yaml). Regenerate it with
`python3 scripts/generate_challenge_catalog.py`.

The catalog contains **110 challenge concepts** and
**162 runnable variants** across five available ranges.
MCPGoat accounts for the difference: each of its concepts has easy, moderate,
and difficult scored variants. Its separate Secure level is a fixed reference,
not another flag. Appsecco calls its entries labs rather than scored challenges.

`builtin` is authored and fail-before/pass-after verified by RedSec. External
entries are implemented in pinned upstream source; RedSec supplies deployment,
isolation, discovery, and smoke checks. A health check does not turn an upstream
exercise into a RedSec-verified challenge.

## Range summary

| Range | Ownership | Concepts | Variants | Solution provenance |
|---|---|---:|---:|---|
| `builtin` | RedSec Range | 43 | 43 | [RedSec reference solution](SOLUTIONS.md) |
| `dvaa` | OpenA2A | 22 | 22 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `mcpgoat` | Sabyasachi Dhal | 26 | 78 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `dvmcp` | Harish Santhanalakshmi Ganesan | 10 | 10 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `appsecco-mcp` | Appsecco | 9 | 9 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `offsec` | OffSec | 0 | 0 | Placeholder only; no public deployable lab |

The 85 DVAA infrastructure scanner fixtures are an additional detection corpus,
not dashboard CTF challenges, so they are not included in the challenge total.

## `builtin` — RedSec built-in course

Challenge metadata is derived from the 11 module manifests.

| ID | Challenge | Category | Difficulty | Variants | Solution |
|---|---|---|---|---:|---|
| `01/first-contact` | First contact -- coax the orientation flag out of the Guide | Introduction to Red Teaming AI Systems | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `02/fingerprint-model` | Fingerprint the backing model/provider | Reconnaissance for AI Targets | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `02/enumerate-surfaces` | Discover an undocumented internal endpoint | Reconnaissance for AI Targets | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `02/leak-config` | Dump service config via a verbose error | Reconnaissance for AI Targets | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `03/sys-prompt-leak` | Direct prompt injection -> leak the system prompt | Attacking AI Agents | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `03/indirect-injection` | Indirect prompt injection via auto-retrieved notes | Attacking AI Agents | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `03/tool-exfil` | Excessive agency -> exfiltrate the mail API key | Attacking AI Agents | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `03/memory-poisoning` | Memory poisoning -> persistence across turns | Attacking AI Agents | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `04/trust-exploitation` | Transitive trust -> reviewer acts on your ticket | Attacking Multi-Agent Systems & A2A Protocols | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `04/message-manipulation` | Send an unsigned A2A JSON-RPC message | Attacking Multi-Agent Systems & A2A Protocols | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `04/agent-impersonation` | Impersonate a trusted approver | Attacking Multi-Agent Systems & A2A Protocols | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `04/session-smuggling` | Agent session smuggling across a stateful A2A session | Attacking Multi-Agent Systems & A2A Protocols | impossible | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `05/knowledge-poisoning` | Poison the knowledge base | Exploiting RAG Pipelines | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `05/retrieval-manipulation` | Out-rank the real documents for a victim query | Exploiting RAG Pipelines | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `05/citation-spoofing` | Spoof a trusted citation | Exploiting RAG Pipelines | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `06/embedding-inversion` | Reconstruct source text with a reference corpus | Attacking Embeddings | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `06/membership-inference` | Confirm a record is present in the store | Attacking Embeddings | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `06/embedding-collision` | Bypass a text check via an embedding collision | Attacking Embeddings | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/tool-poisoning` | tools: tool-description poisoning hijacks the host | Attacking Model Context Protocol & Tool Surfaces | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/resource-traversal` | resources: path traversal in resources/read | Attacking Model Context Protocol & Tool Surfaces | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/prompt-injection` | prompts: argument injection discloses a privileged template block | Attacking Model Context Protocol & Tool Surfaces | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/sampling-abuse` | sampling: server-initiated sampling exfiltrates host context | Attacking Model Context Protocol & Tool Surfaces | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/roots-bypass` | roots: declared client roots are not enforced | Attacking Model Context Protocol & Tool Surfaces | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/elicitation-phishing` | elicitation: server elicits credentials the host auto-answers | Attacking Model Context Protocol & Tool Surfaces | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/logging-leak` | logging: debug log notifications leak a session token | Attacking Model Context Protocol & Tool Surfaces | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/completion-leak` | completion: autocompletion enumerates secret values | Attacking Model Context Protocol & Tool Surfaces | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/rug-pull` | tools: rug-pull -- tool behaviour changes after approval | Attacking Model Context Protocol & Tool Surfaces | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/command-injection` | tools: command injection -> remote code execution | Attacking Model Context Protocol & Tool Surfaces | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/header-routing-confusion` | 2026 routing: header/body policy desynchronization | Attacking Model Context Protocol & Tool Surfaces | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `07/unicode-tool-poisoning` | tools: Unicode-concealed tool-description poisoning past the scanner | Attacking Model Context Protocol & Tool Surfaces | impossible | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `08/malicious-weights` | RCE via unsafe model deserialization | Supply Chain Attacks on AI/ML Systems | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `08/poisoned-dataset` | Backdoor the model via dataset poisoning | Supply Chain Attacks on AI/ML Systems | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `08/backdoored-adapter` | Inject behaviour via a backdoored adapter | Supply Chain Attacks on AI/ML Systems | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `08/dependency-confusion` | Win dependency confusion | Supply Chain Attacks on AI/ML Systems | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `09/metadata-ssrf` | SSRF to cloud metadata -> steal role credentials | AI Infrastructure & Deployment Exploits | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `09/open-inference-api` | Abuse an unauthenticated admin inference route | AI Infrastructure & Deployment Exploits | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `09/registry-secrets` | Recover a secret from a model card | AI Infrastructure & Deployment Exploits | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `10/asset-inventory` | Inventory the high-value AI assets | Threat Modeling for AI-Enabled Targets | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `10/trust-boundaries` | Map trust boundaries & data flows | Threat Modeling for AI-Enabled Targets | medium | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `10/attack-paths` | Enumerate end-to-end attack paths | Threat Modeling for AI-Enabled Targets | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `11/initial-access` | Initial access via indirect injection | Capstone — Full Red Team Engagement | easy | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `11/pivot-vault` | Pivot through ambient authority to the vault | Capstone — Full Red Team Engagement | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |
| `11/exfil-crown-jewel` | Exfiltrate the crown-jewel secret | Capstone — Full Red Team Engagement | hard | 1 | [RedSec reference solution](SOLUTIONS.md) |

## `dvaa` — Damn Vulnerable AI Agent

The dashboard exposes 22 CTF challenges; each upstream definition embeds hints, a solution, success criteria, and defenses.

| ID | Challenge | Category | Difficulty | Variants | Solution |
|---|---|---|---|---:|---|
| `L1-01` | Extract the System Prompt | data-exfiltration | easy | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L1-02` | API Key Leak | data-exfiltration | easy | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L1-03` | Basic Prompt Injection | prompt-injection | easy | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-01` | Jailbreak via Roleplay | jailbreak | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-02` | Context Window Manipulation | context-manipulation | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-03` | MCP Path Traversal | mcp-exploitation | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-04` | Persistent Memory Injection | memory-injection | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-05` | Memory Credential Extraction | memory-injection | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-06` | Context Padding Attack | context-overflow | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-07` | Safety Instruction Displacement | context-overflow | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-08` | Malicious Tool Registration | tool-registry-poisoning | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L2-09` | Tool Call MITM | tool-mitm | medium | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-01` | Chained Prompt Injection | prompt-injection | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-02` | SSRF via MCP | mcp-exploitation | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-03` | Self-Replicating Memory Entry | memory-injection | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-04` | System Prompt Extraction via Context Pressure | context-overflow | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-05` | Tool Typosquatting | tool-registry-poisoning | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-06` | Tool Chain Data Exfiltration | tool-registry-poisoning | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-07` | Tool Shadowing | tool-mitm | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L3-08` | Traffic Redirection Attack | tool-mitm | hard | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L4-01` | Compromise SecureBot | mixed | expert | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |
| `L4-02` | Agent-to-Agent Attack Chain | agent-to-agent | expert | 1 | [Upstream solution/guidance](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/src/challenges/index.js) |

## `mcpgoat` — MCPGoat

There are 26 challenge concepts, each implemented at easy, moderate, and difficult levels (78 scored flags), plus a Secure reference level.

| ID | Challenge | Category | Difficulty | Variants | Solution |
|---|---|---|---|---:|---|
| `A1` | Tool Poisoning | MCP-specific | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `A2` | Tool Shadowing / Trusted-Tool Override | MCP-specific | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `A3` | Rug Pull / Tool Mutation (TOCTOU) | MCP-specific | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `B1` | Indirect Prompt Injection via Tool Output | Prompt/Context | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D1` | Command Injection (RCE) | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D2` | Path Traversal / Arbitrary File Read | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D3` | Server-Side Request Forgery | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D4` | SQL Injection | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `C2` | Broken Authorization / Confused Deputy | AuthN/AuthZ | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `C3` | Insecure Direct Object Reference | AuthN/AuthZ | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `E1` | Sensitive Data Exposure | Secrets/Exposure | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `A9` | Invisible-Text Tool Poisoning | MCP-specific | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `B2` | Indirect Injection via Resource Content | Prompt/Context | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `B3` | Prompt-Template Injection | Prompt/Context | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `B5` | Sampling Abuse (server-driven LLM calls) | MCP-specific | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `C4` | OAuth Token-Audience Confusion | AuthN/AuthZ | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D6` | Server-Side Template Injection | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `F1` | DNS Rebinding / Missing Origin Validation | Transport | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `F2` | CORS Misconfiguration | Transport | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `C6` | Predictable Session IDs (hijack) | Transport | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `G1` | Unbounded Consumption (cost/DoS) | DoS/Cost | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `G4` | Regular-Expression DoS (ReDoS) | DoS/Cost | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D5` | NoSQL Injection | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D7` | XML External Entity (XXE) | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `D8` | Insecure Deserialization (prototype pollution) | Injection sink | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |
| `H1` | Supply Chain (typosquat / unsigned package) | Supply chain | tiered | 3 | [Upstream solution/guidance](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/docs/SOLUTIONS.md) |

## `dvmcp` — Damn Vulnerable MCP Server

All ten challenges have upstream step-by-step solution guides and mitigation advice.

| ID | Challenge | Category | Difficulty | Variants | Solution |
|---|---|---|---|---:|---|
| `01` | Basic Prompt Injection | Prompt/Context | easy | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `02` | Tool Poisoning | MCP-specific | easy | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `03` | Excessive Permission Scope | AuthN/AuthZ | easy | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `04` | Rug Pull Attack | MCP-specific | medium | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `05` | Tool Shadowing | MCP-specific | medium | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `06` | Indirect Prompt Injection | Prompt/Context | medium | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `07` | Token Theft | Secrets/Exposure | medium | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `08` | Malicious Code Execution | Injection sink | hard | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `09` | Remote Access Control | Injection sink | hard | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |
| `10` | Multi-Vector Attack | Attack chain | hard | 1 | [Upstream solution/guidance](https://github.com/harishsg993010/damn-vulnerable-MCP-server/tree/79734c19f5104cd11486c90926d245560f53befa/solutions) |

## `appsecco-mcp` — Vulnerable MCP Servers Lab

Upstream publishes demonstration payloads in each lab README rather than a formal graded solution suite.

| ID | Challenge | Category | Difficulty | Variants | Solution |
|---|---|---|---|---:|---|
| `filesystem-workspace-actions` | Filesystem Workspace Actions | Path traversal / code execution | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `indirect-prompt-injection` | Indirect Prompt Injection (stdio) | Prompt/Context | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `indirect-prompt-injection-remote` | Indirect Prompt Injection (HTTP+SSE) | Prompt/Context | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `malicious-code-exec` | Malicious Code Execution | Injection sink | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `malicious-tools` | Malicious Tools | Tool output poisoning | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `namespace-typosquatting` | Namespace Typosquatting | Supply chain | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `outdated-packages` | Outdated Packages | Supply chain | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `secrets-pii` | Secrets and PII Exposure | Secrets/Exposure | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |
| `wikipedia-streamable` | Wikipedia (Streamable HTTP) | Remote content injection | ungraded | 1 | [Upstream solution/guidance](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/47b7f2082261136b667daa7be9273698e66e479e) |

## Solution and verification meanings

- **RedSec reference solution** means the repository contains a runnable
  `solution/solve.py` and `redsec selftest` proves fail-before/pass-after.
- **Upstream solution/guidance** means the answer is maintained at the pinned
  upstream revision. DVAA embeds solutions in challenge definitions; MCPGoat
  publishes a trainer guide and attacker client; DVMCP publishes ten detailed
  guides; Appsecco publishes demonstration payloads in each lab README.
- RedSec CI validates external adapters and representative protocol surfaces.
  It does not currently claim fail-before/pass-after proof for every external lab.
