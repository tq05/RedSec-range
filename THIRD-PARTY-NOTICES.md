# Third-party ranges and credits

RedSec Range brings several independently maintained, deliberately vulnerable
training labs together in one place. The labs below are the work of their original
authors. All credit for their challenges, targets, and solution guides belongs to
them. RedSec includes only labs whose license permits this use.

## How upstream work is used

- **Not vendored.** Upstream source is not copied into this repository. When an
  operator enables a range, `redsec ranges` fetches the upstream repository at the
  pinned revision below and builds it locally (see
  [ranges/catalog.yaml](ranges/catalog.yaml)).
- **RedSec adds** only a thin adapter: pinning, container builds, network isolation,
  challenge indexing, and smoke checks. Files under [`ranges/adapters/`](ranges/adapters/)
  are RedSec's own Apache-2.0 code.
- **Upstream licenses still apply** to the fetched source and to everything built from it.
- **Solutions stay upstream.** RedSec links to each project's own solution guides at
  the pinned revision instead of republishing them.

## Integrated ranges

| Range ID | Project | Original author(s) | License | Pinned revision |
|---|---|---|---|---|
| `dvaa` | [Damn Vulnerable AI Agent](https://github.com/opena2a-org/damn-vulnerable-ai-agent) | OpenA2A | [Apache-2.0](https://github.com/opena2a-org/damn-vulnerable-ai-agent/blob/faf3fb172ef526d12db0eb5377701549693118a6/LICENSE) | `faf3fb172ef526d12db0eb5377701549693118a6` |
| `mcpgoat` | [MCPGoat](https://github.com/SabyasachiDhal/MCPGoat) | Sabyasachi Dhal | [MIT](https://github.com/SabyasachiDhal/MCPGoat/blob/80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed/LICENSE), © 2026 Sabyasachi Dhal | `80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed` |
| `dvmcp` | [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) | Harish Santhanalakshmi Ganesan | MIT, [declared in the README](https://github.com/harishsg993010/damn-vulnerable-MCP-server/blob/79734c19f5104cd11486c90926d245560f53befa/README.md#license) (the pinned revision has no LICENSE file) | `79734c19f5104cd11486c90926d245560f53befa` |
| `appsecco-mcp` | [Vulnerable MCP Servers Lab](https://github.com/appsecco/vulnerable-mcp-servers-lab) | Appsecco | [MIT](https://github.com/appsecco/vulnerable-mcp-servers-lab/blob/47b7f2082261136b667daa7be9273698e66e479e/LICENSE), © 2025 Appsecco | `47b7f2082261136b667daa7be9273698e66e479e` |

These projects are not affiliated with RedSec Range and do not endorse it. Report
bugs in a lab's challenges to that lab's own repository.

## Not included

- **OffSec** (`offsec`) is a disabled placeholder. No OffSec content, labs, or
  materials are included, because no public license allows it. The public AI-300
  syllabus is used only as a structural reference, and RedSec Range is not
  affiliated with OffSec.

## References

The built-in curriculum is RedSec's own work. It draws on, and cites, these
publicly available references. None of their text or data is redistributed here:

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/) and the emerging OWASP MCP Top 10 (OWASP Foundation)
- [Cloud Security Alliance](https://cloudsecurityalliance.org/) MCP attack-surface analysis
- [MITRE ATLAS](https://atlas.mitre.org/) (The MITRE Corporation)

## Adding a range

Add a new external range only when its license permits fetching and building it
this way. Record its maintainer, license, and pinned revision in
`ranges/catalog.yaml`, and add a row to the table above.
