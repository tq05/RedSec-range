# RedSec Range — Visual Overview

A one-page map of the range: the learning path, the AI attack surface each module
targets, the MCP 8-vector matrix, the capstone kill chain, and how the framework fits
together. Diagrams are Mermaid and render on GitHub. Pair this with
[WORKSHEET.md](WORKSHEET.md) (no spoilers) and [SOLUTIONS.md](SOLUTIONS.md) (answers).

## Learning path

```mermaid
flowchart LR
  subgraph FOUND["Foundations"]
    M01["01 Intro<br/>first contact"] --> M02["02 Recon<br/>fingerprint & leak"]
  end
  subgraph CORE["Core attack surfaces"]
    M03["03 Agents<br/>injection · agency · memory"]
    M05["05 RAG<br/>poison · retrieval · citation"]
    M06["06 Embeddings<br/>invert · MIA · collision"]
    M04["04 Multi-agent<br/>trust · forge · impersonate"]
    M07["07 MCP<br/>8-vector matrix + RCE"]
  end
  subgraph SYS["Systems around the model"]
    M08["08 Supply chain<br/>pickle RCE · backdoors"]
    M09["09 Infra<br/>SSRF · open API · secrets"]
  end
  M10["10 Threat modeling<br/>assets · boundaries · paths"]
  M11["11 Capstone<br/>injection → pivot → exfil"]

  M02 --> M03 --> M05 --> M06
  M03 --> M04
  M03 --> M07
  M06 --> M08 --> M09
  M07 --> M09
  M09 --> M10 --> M11
  M04 --> M11
  M07 --> M11
```

## The AI attack surface (what each module hits)

```mermaid
flowchart TB
  user["Untrusted input<br/>(user, web, files)"]
  subgraph APP["LLM application / agent"]
    prompt["System prompt<br/>& secrets"]
    model["Model"]
    tools["Tools<br/>(ambient authority)"]
    memory["Memory"]
  end
  subgraph DATA["Knowledge & data"]
    rag["RAG corpus<br/>& retriever"]
    emb["Embeddings<br/>/ vector store"]
  end
  subgraph EXT["Connected systems"]
    mcp["MCP servers"]
    agents["Other agents (A2A)"]
  end
  subgraph PLAT["Platform"]
    supply["Model/data/deps<br/>supply chain"]
    infra["Infra: metadata,<br/>inference API, registry"]
  end

  user -->|"01,02,03 direct injection"| model
  rag -->|"05 indirect injection"| model
  memory -->|"03 persistence"| model
  emb -->|"06 inversion / MIA"| DATA
  mcp -->|"07 poisoning / confused deputy"| tools
  agents -->|"04 transitive trust"| model
  model --> tools
  tools -->|"03,11 excessive agency → exfil"| EXT
  supply -->|"08 before deploy"| model
  infra -->|"09 SSRF / secrets"| PLAT
```

## Module 07 — the MCP 8-vector matrix

Eight protocol primitives, each with one deliberate flaw (plus rug-pull and RCE).
Direction shows why each is exploitable.

```mermaid
flowchart LR
  subgraph S2M["server → model  (injection channels)"]
    t["tools<br/>► poisoning / rug-pull / RCE"]
    r["resources<br/>► path traversal"]
    p["prompts<br/>► argument injection"]
    c["completion<br/>► secret enumeration"]
  end
  subgraph S2C["server → client  (drive the host)"]
    sa["sampling<br/>► context exfiltration"]
    el["elicitation<br/>► credential phishing"]
  end
  subgraph CLI["client-declared / side channel"]
    ro["roots<br/>► not enforced"]
    lo["logging<br/>► sensitive-data leak"]
  end
  t --> HOST["Naive MCP host<br/>(ambient secrets + model)"]
  sa --> HOST
  el --> HOST
```

| # | Primitive | Vector | Verify |
|---|-----------|--------|--------|
| 1 | tools | description poisoning · rug-pull · command-injection RCE | oracle / flag |
| 2 | resources | path traversal | flag |
| 3 | prompts | argument injection | flag |
| 4 | sampling | server-initiated context exfiltration | oracle |
| 5 | roots | declared scope not enforced | flag |
| 6 | elicitation | credential phishing (host auto-answers) | oracle |
| 7 | logging | sensitive-data leak at debug | flag |
| 8 | completion | secret enumeration via autocomplete | flag |

## Capstone kill chain (Module 11)

```mermaid
sequenceDiagram
  actor Att as Attacker
  participant Notes as Notes store
  participant Asst as Assistant (ambient authority)
  participant Vault as Internal vault
  participant Sink as Exfil sink
  Att->>Notes: poison a note (ACTION line)
  Note over Asst: benign user turn reads notes as trusted
  Asst->>Sink: initial-access (proof of control)
  Att->>Notes: note → report_record "public"
  Asst->>Vault: pivot-vault (deputy reads record)
  Vault-->>Asst: record
  Att->>Notes: note → report_record "crown"
  Asst->>Vault: fetch crown jewel
  Asst->>Sink: exfil-crown-jewel (full compromise)
```

## Framework architecture

```mermaid
flowchart TB
  cli["redsec CLI / range / assess / grok"]
  subgraph MOD["modules/NN-slug (declarative)"]
    y["module.yaml<br/>objectives · hints · verify"]
    l["lesson.md"]
    tg["targets/ (vulnerable apps)"]
    so["solution/solve.py"]
  end
  subgraph FW["redsec/ package"]
    eng["mockllm (deterministic LLM)"]
    ver["verify (flag · oracle · artifact)"]
    dep["deploy (local · docker · k8s)"]
    drop["drop sink (oracle)"]
  end
  cli --> MOD
  cli --> FW
  tg --> eng
  tg -->|"exfil"| drop
  so -->|"exploit"| tg
  ver -->|"flag / reads sink"| drop
  ver -->|"fail→pass gate"| so
```

## Run paths (same modules everywhere)

```mermaid
flowchart LR
  repo["modules + redsec/"]
  repo --> local["redsec dev/up<br/>(local processes)"]
  repo --> docker["sandbox-up.sh + range<br/>(persistent Docker)"]
  repo --> check["docker_run_all.py<br/>(ephemeral check)"]
  repo --> k8s["kind-up.sh + helm<br/>(Kubernetes)"]
  local --> verify["redsec selftest / verify<br/>42/42"]
  docker --> verify
  check --> verify
  k8s --> verify
```

> Note on isolation: the deliberately-vulnerable RCE/SSRF/deserialization modules
> (07, 08, 09) are best run via the **Docker or Kubernetes** paths, which contain
> them; bare local-process mode has no isolation. See
> [SECURITY.md](../SECURITY.md) and [kubernetes.md](kubernetes.md).
