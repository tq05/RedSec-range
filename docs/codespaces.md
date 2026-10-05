# Run RedSec Range in GitHub Codespaces

GitHub Codespaces is the default cloud path for RedSec Range. It gives each
learner a private, disposable development machine with Docker, the course CLI,
all built-in container targets, browser port forwarding, and SSH access. A Fly.io account is not
required.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tq05/RedSec-range?quickstart=1)

## Start the range

1. Sign in to GitHub and open the button above, or choose **Code → Codespaces →
   Create codespace on main** in the repository.
2. Use the recommended 4-core, 8 GB machine when GitHub offers a machine choice.
3. Wait for the terminal to print `RedSec Range is ready`. The first build pulls
   dependencies and creates the shared target image, so later starts are faster.

The devcontainer starts the complete built-in range automatically. Check it with:

```bash
range status
redsec lesson 01
redsec hint 01 first-contact
range solve 01
```

The worksheet in [`WORKSHEET.md`](WORKSHEET.md) contains attack paths without
answers. Use `range solve <module>` when you want to run the reference exploit and
verifier.

## Use Claude, Codex, or another model harness

The simplest setup is to run the harness inside the Codespace. Open its terminal,
install and authenticate your preferred Codex or Claude CLI, and start it from the
repository root. Node.js LTS is already installed for JavaScript-based harnesses.
[`AGENTS.md`](../AGENTS.md) and [`CLAUDE.md`](../CLAUDE.md) tell repository-aware
agents how to inspect and operate the range. Useful commands are:

```bash
range status
range solve 07
range shell 07 vuln-mcp
assess 07 --provider openai --model <model>
```

The course and deterministic reference exploits need no model key. To run the
autonomous assessor, add `OPENAI_API_KEY`, `XAI_API_KEY`, or
`REDSEC_LLM_API_KEY` as a [Codespaces secret](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-secrets-for-your-codespaces), then rebuild or restart the Codespace. Never commit API keys.

### Where commands execute

Creating a Codespace does not automatically tunnel an existing ChatGPT, Codex, or
Claude sandbox into it. The model's tool calls execute wherever its harness runs:

- A harness started in the Codespace executes directly on the attacking machine.
- An external harness needs GitHub CLI authentication and outbound SSH access. It
  can use `./scripts/codespaces-connect.sh range status` for a remote command or
  `./scripts/codespaces-connect.sh` for an interactive shell.
- A repository connector that can read or write GitHub files does not by itself
  provide terminal access to the Codespace.

The helper selects the most recently used Codespace for this repository. Set
`REDSEC_CODESPACE=<name>` to select one explicitly. Each call creates an
authenticated SSH connection; it does not expose the challenge ports publicly.

## Connect over SSH

The browser terminal works immediately. For a local terminal, install the GitHub
CLI, authenticate once, and connect to the Codespace:

```bash
gh auth login
gh codespace ssh -R tq05/RedSec-range
```

Run `gh codespace list` first if you have more than one Codespace and want to pick
one explicitly. SSH access is authenticated by GitHub and is available only to the
Codespace owner.

## Open a target in the browser

Open the **Ports** tab in the Codespace. The devcontainer labels each challenge
port and GitHub forwards it on demand. Ports are private to your GitHub account by
default; keep them private because every target is deliberately vulnerable.

| Port | Module or service |
|------|-------------------|
| 9010–9060 | Modules 01–06 |
| 9070–9071 | Module 07 MCP server and host |
| 9080 | Module 08 |
| 9090–9091 | Module 09 app and metadata service |
| 9110, 9112 | Module 11 assistant and vault |

`range status` shows the precise target names and URLs. Module 10 is an
artifact-scored threat-model exercise and has no HTTP target.

## Start fewer modules

The default starts every container-backed module. For a smaller session:

```bash
range down-all
./scripts/sandbox-up.sh 04 07
```

You can also create a Codespaces secret named `REDSEC_MODULES` with space-separated
two-digit IDs such as `04 07`; future starts will bring up only those modules.

`builtin` is the default range. To start external integrations alongside it, set
the `REDSEC_RANGES` Codespaces secret or enable them interactively:

```bash
redsec ranges enable dvaa mcpgoat dvmcp appsecco-mcp
redsec ranges up
redsec ranges status
redsec ranges challenges
```

See [the external ranges guide](external-ranges.md) for isolation, ports, stdio MCP
entrypoints, individual updates, and the complete challenge/solution catalog.

## Stop or delete the Codespace

Stop the Codespace when you finish so it stops consuming compute quota. Delete it
when you no longer need its stored files. Codespaces usage is subject to the quota
and billing rules on your GitHub plan; the creation screen shows the selected
machine and any billable cost.

If startup fails, run `./scripts/codespaces-up.sh` in the repository root and read
the first failing command. `docker info`, `.venv/bin/redsec doctor`, and
`range status` isolate Docker, installation, and target startup problems.

Use [the Fly.io workflow](deploy-fly.md) when you need a dedicated machine outside
Codespaces, a longer compute deadline, or Fly-specific testing.
