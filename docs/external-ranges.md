# Built-in and external ranges

RedSec has a catalog of independently deployable training ranges. The RedSec
curriculum is the `builtin` range. External projects retain their own source,
license, documentation, challenge model, and release cadence; RedSec supplies a
thin deployment adapter instead of copying their challenges into this repository.

```bash
redsec ranges list
redsec ranges enable dvaa mcpgoat dvmcp appsecco-mcp
redsec ranges up
redsec ranges status
```

`redsec ranges enable --all` selects every available range. The `offsec` catalog
entry is a disabled placeholder: it has no source or runtime adapter and cannot be
enabled unless OffSec publishes and licenses an automatable lab interface.

## Included integrations

| ID | Upstream | Runtime | Main access |
|----|----------|---------|-------------|
| `builtin` | RedSec Range | Per-module Docker networks | `range status`, ports 9010–9112 |
| `dvaa` | [Damn Vulnerable AI Agent](https://github.com/opena2a-org/damn-vulnerable-ai-agent) | One upstream container | dashboard `http://127.0.0.1:9000` |
| `mcpgoat` | [MCPGoat](https://github.com/SabyasachiDhal/MCPGoat) | One upstream container | control/MCP `http://127.0.0.1:7332` |
| `dvmcp` | [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) | One upstream container, ten services | host ports 19001–19010 |
| `appsecco-mcp` | [Vulnerable MCP Servers Lab](https://github.com/appsecco/vulnerable-mcp-servers-lab) | RedSec adapter container | SSE `:13000`, Streamable HTTP `:18000`, seven stdio entrypoints |
| `offsec` | Future OffSec lab | Placeholder | unavailable |

DVMCP is remapped from upstream ports 9001–9010 to 19001–19010 because 9010 is
already used by built-in module 01. The protocols and container ports are unchanged.

## Infrastructure and isolation

All selected ranges run on the same Docker-capable host: a laptop, Codespace, or
private Fly Machine. Each external project has a dedicated container and an
independent Docker network. The built-in range continues to use one network per
course module. This allows all projects to run at once without merging their
processes, filesystems, dependencies, or lifecycle.

External networks are created with Docker's `--internal` setting, so deliberately
vulnerable targets cannot reach the internet by default. Host ports bind to
`127.0.0.1` outside Fly and remain private Codespaces ports. If a lab exercise
requires outbound content, recreate the selected ranges explicitly:

```bash
redsec ranges up appsecco-mcp --allow-egress
```

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
