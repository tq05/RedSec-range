| `metadata-ssrf` | F | 🔴 | A server-side fetch has no allow-list. First discover the internal metadata address (recon), then make the server fetch its credentials for you. | `GET /debug/config`, `POST /fetch` |
| `open-inference-api` | F | 🟢 | A privileged route has no auth. The landing page lists the routes. | `/` → an admin route |
| `registry-secrets` | F | 🟡 | Secrets are committed into model metadata. List the models, read a model card. | `/registry/models`, model card |
| `crown-jewel-chain` | F | ⚫ **impossible** | The credential that easy SSRF returns is refused by a second internal service, and the fetcher now rejects literal credential headers. Reach the crown jewel through `POST /fetch` anyway. `/debug/config` does not name the second service. *(No walkthrough — answer sealed in `modules/09-infra-deployment/solution/SEALED.md`.)* | `POST /fetch` only |

**Why it works:** models run on ordinary, often over-privileged infrastructure — a
fetch primitive, an open port, or a leaky registry turns a model bug into a cloud
compromise. The impossible tier is the Capital One shape: the first credential is
not the one the crown jewel wants, and a guard that scans bytes is not a parser.
