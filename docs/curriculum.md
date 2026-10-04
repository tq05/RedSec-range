# Curriculum & taxonomy mapping

RedSec Range follows the structure of OffSec's **AI-300 / OSAI ("Advanced AI Red
Teaming")** syllabus, and maps every module to the **OWASP LLM Top 10 (2025)**, the
emerging **OWASP MCP Top 10**, and **MITRE ATLAS**. **43 challenges across 11
modules, all complete and tested** (8650 pts). See `AI300-COVERAGE.md` for the
public-syllabus traceability and course-quality contract.

> This table mirrors the module manifests (`redsec list`), so it stays in sync.
> **ATLAS IDs are indicative** — verify against the current
> [ATLAS matrix](https://atlas.mitre.org/). Not affiliated with OffSec.

| # | Module | Status | OWASP LLM | OWASP MCP | MITRE ATLAS | Chal | Pts |
|---|---|---|---|---|---|---|---|
| 01 | Introduction to Red Teaming AI Systems | ✅ | LLM07 | - | AML.T0051 | 1 | 50 |
| 02 | Reconnaissance for AI Targets | ✅ | LLM07, LLM02 | - | AML.T0002, AML.T0040 | 3 | 400 |
| 03 | Attacking AI Agents | ✅ | LLM01, LLM02, LLM06, LLM07 | - | AML.T0051, AML.T0054, AML.T0057 | 4 | 750 |
| 04 | Attacking Multi-Agent Systems & A2A | ✅ | LLM01, LLM06 | - | AML.T0051, AML.T0054 | 4 | 1100 |
| 05 | Exploiting RAG Pipelines | ✅ | LLM01, LLM08 | - | AML.T0020, AML.T0051 | 3 | 550 |
| 06 | Attacking Embeddings | ✅ | LLM08, LLM02 | - | AML.T0024, AML.T0043 | 3 | 650 |
| 07 | Attacking MCP & Tool Surfaces | ✅ | LLM01, LLM02, LLM06 | MCP01-05 | AML.T0051, AML.T0054, AML.T0053 | 12 | 2500 |
| 08 | Supply Chain Attacks on AI/ML | ✅ | LLM03, LLM04 | - | AML.T0010, AML.T0018, AML.T0020 | 4 | 850 |
| 09 | AI Infrastructure & Deployment | ✅ | LLM02 | - | AML.T0040, AML.T0024 | 3 | 600 |
| 10 | Threat Modeling for AI Targets | ✅ | - | - | - | 3 | 450 |
| 11 | Capstone — Full Engagement | ✅ | LLM01, LLM02, LLM06 | - | AML.T0051, AML.T0024 | 3 | 750 |

## OWASP LLM Top 10 (2025) reference

| ID | Name | Primary modules |
|----|------|-----------------|
| LLM01 | Prompt Injection | 03, 04, 05, 07, 11 |
| LLM02 | Sensitive Information Disclosure | 02, 03, 06, 07, 09, 11 |
| LLM03 | Supply Chain | 08 |
| LLM04 | Data & Model Poisoning | 08 |
| LLM05 | Improper Output Handling | 03, 07 (via tool execution) |
| LLM06 | Excessive Agency | 03, 04, 07, 11 |
| LLM07 | System Prompt Leakage | 02, 03 |
| LLM08 | Vector & Embedding Weaknesses | 05, 06 |
| LLM09 | Misinformation | 05 (citation spoofing) |
| LLM10 | Unbounded Consumption | — (surface noted; no dedicated challenge yet) |

## Suggested learning path

1. **01 → 02** — orientation and recon (what you're attacking, how to find it).
2. **03** — the foundational module: prompt injection, indirect injection,
   excessive agency, memory. *Fully implemented; do this first in the lab.*
3. **05, 06, 04** — where the untrusted text comes from: retrieval, embeddings,
   other agents (all variations on injection/trust).
4. **07** — MCP & tool surfaces: versioned 2025 matrix plus 2026 routing. *Fully implemented.*
5. **08, 09** — the artifacts and infrastructure around the model.
6. **10** — turn it into structured analysis (threat modeling).
7. **11** — the capstone: chain it all in a realistic engagement.

Progress is tracked locally (`redsec score`); points are indicative difficulty
weights, not a leaderboard.
