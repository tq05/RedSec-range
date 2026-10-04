**open-inference-api** — `REDSEC{infra_unauthenticated_inference_admin}` → `curl -s $APP/v1/admin`
**registry-secrets** — `REDSEC{infra_secret_in_model_registry}` → `curl -s $APP/registry/models/initrode/MLmodel`

**crown-jewel-chain** (impossible, flag) — **answer intentionally withheld.** The
credential from `metadata-ssrf` is not accepted by the second service. The solution
is sealed in `modules/09-infra-deployment/solution/SEALED.md`. `redsec selftest 09`
proves the reference exploit works, and it only needs the appserver.
