# Built-in and external ranges

RedSec has a catalog of independently deployable training ranges. The RedSec
curriculum is the `builtin` range. External projects retain their own source,
license, documentation, challenge model, and release cadence; RedSec supplies a
thin deployment adapter instead of copying their challenges into this repository.

```bash
redsec ranges list
redsec ranges challenges
redsec ranges enable dvaa mcpgoat dvmcp appsecco-mcp
redsec ranges up
redsec ranges status
```

`redsec ranges enable --all` selects every available range. The `offsec` catalog
entry is a disabled placeholder: it has no source or runtime adapter and cannot be
enabled unless OffSec publishes and licenses an automatable lab interface.

## Included integrations

Each external range is the work of its original authors. RedSec uses it under that
project's license and fetches it at a pinned revision. Its source is not vendored
here. See [THIRD-PARTY-NOTICES.md](../THIRD-PARTY-NOTICES.md) for copyright notices
and the pinned revisions.

| ID | Upstream | Author(s) | License | Concepts / variants | Runtime | Solutions |
|----|----------|-----------|---------|--------------------:|---------|-----------|
| `builtin` | RedSec Range | RedSec Range | Apache-2.0 | 43 / 43 | Per-module Docker networks | RedSec `SOLUTIONS.md` + runnable exploits |
| `dvaa` | [Damn Vulnerable AI Agent](https://github.com/opena2a-org/damn-vulnerable-ai-agent) | OpenA2A | Apache-2.0 | 22 / 22 | One upstream container; dashboard `:9000` | Embedded in pinned challenge definitions |
| `mcpgoat` | [MCPGoat](https://github.com/SabyasachiDhal/MCPGoat) | Sabyasachi Dhal | MIT | 26 / 78 | One upstream container; control/MCP `:7332` | Trainer guide + attacker client |
| `dvmcp` | [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) | Harish Santhanalakshmi Ganesan | MIT (declared in README) | 10 / 10 | One upstream container, ten services on `19001–19010` | Ten detailed upstream guides |
| `appsecco-mcp` | [Vulnerable MCP Servers Lab](https://github.com/appsecco/vulnerable-mcp-servers-lab) | Appsecco | MIT | 9 labs / 9 | Adapter container; SSE `:13000`, HTTP `:18000`, seven stdio entries | Per-lab README guidance |
| `offsec` | Future OffSec lab | OffSec | proprietary; not included | 0 / 0 | Placeholder | unavailable |

The [complete generated catalog](CHALLENGE-CATALOG.md) lists every challenge. The
CLI provides the same data as a table or JSON:

```bash
redsec ranges challenges
redsec ranges challenges mcpgoat --json
```

The challenge list describes each committed pinned revision. A locally updated
range can move beyond that baseline; `redsec ranges status` reports both revisions
and warns when its curriculum metadata may be stale.

DVMCP is remapped from upstream ports 9001–9010 to 19001–19010 because 9010 is
already used by built-in module 01. The protocols and container ports are unchanged.

## Infrastructure and isolation

All selected ranges run on the same Docker-capable host: a laptop, Codespace, or
private Fly Machine. Each external project has a dedicated target container and
independent Docker networks. The built-in range continues to use one network per
course module. This allows all projects to run at once without merging their
processes, filesystems, dependencies, or lifecycle.

The target container joins only a Docker `--internal` network, so deliberately
vulnerable code cannot reach the internet by default. A small read-only RedSec TCP
gateway joins that internal network and a host-access bridge, forwarding only the
ports declared in the catalog. Host ports bind to `127.0.0.1` outside Fly and
remain private Codespaces ports. The gateway offers no general-purpose proxy. If a
lab exercise requires outbound content, recreate the selected ranges explicitly:

```bash
redsec ranges up appsecco-mcp --allow-egress
```

Appsecco's `malicious-code-exec`, `malicious-tools`, `secrets-pii`, and
`wikipedia-streamable` labs contain tools that call public services. Enable egress
only when exercising those outbound tools. The other Appsecco labs and all adapter
startup checks run on the internal network without egress.

This adapter release does not force external projects into Kubernetes. They do not
publish compatible charts or health/lifecycle contracts, and placing unrelated
vulnerable projects in one namespace would weaken isolation. The built-in course
retains its Helm/kind path. A future Kubernetes driver should give each external
range its own namespace, NetworkPolicy, release, and pinned image; it can still use
one shared cluster without sharing a namespace.

## Independent updates

[`ranges/catalog.yaml`](../ranges/catalog.yaml) pins every default source to a full
Git commit. First start fetches only that revision and builds a local image. This
makes a fresh setup reproducible even when an upstream default branch changes.

Update one installed range without changing the others:

```bash
redsec ranges update mcpgoat
redsec ranges update dvaa appsecco-mcp
```

`update` fetches that project's configured default branch, rebuilds its image, and
restarts only that range when it is running. The resulting local revision appears
in `redsec ranges status`. Updating the committed default for every user is a
reviewed change to `ranges/catalog.yaml` and its adapter CI.

## Appsecco stdio MCP servers

The Appsecco repository contains two network servers and seven stdio servers. List
and launch the stdio entries through the persistent adapter container:

```bash
redsec ranges entrypoints appsecco-mcp
redsec ranges launch appsecco-mcp malicious-tools
redsec ranges launch appsecco-mcp filesystem-workspace-actions
```

An MCP-capable model client can use RedSec itself as the stdio command:

```json
{
  "mcpServers": {
    "appsecco-malicious-tools": {
      "command": "redsec",
      "args": ["ranges", "launch", "appsecco-mcp", "malicious-tools"]
    }
  }
}
```

The other external projects expose network protocols and can be reached from a
harness running on the same attacking machine using the URLs from
`redsec ranges status`.

## Codespaces and Fly.io

Codespaces starts `builtin` by default. To make a profile start automatically,
create a Codespaces secret such as:

```text
REDSEC_RANGES=builtin dvaa mcpgoat dvmcp appsecco-mcp
```

For Fly.io, choose the same profile when creating the private Machine:

```bash
./deploy/fly/up.sh --ranges "builtin dvaa mcpgoat dvmcp appsecco-mcp" --ttl 120
./deploy/fly/exec.sh redsec ranges status
./deploy/fly/proxy.sh 7332
```

External sources and built images live in ignored RedSec state on that machine.
Destroying the Codespace or Fly app removes them with the disposable environment.

## Verification and solution provenance

`builtin` alone has RedSec's fail-before/pass-after contract. The external CI path
builds pinned sources together, starts their adapters, checks declared ports and
entrypoints, and tests network isolation. DVAA and MCPGoat also ship substantial
native validation; DVMCP ships solution guides; Appsecco ships demonstrator
payloads. RedSec does not describe a responding external container as proof that
every upstream challenge has been solved. See [TESTING.md](TESTING.md).
