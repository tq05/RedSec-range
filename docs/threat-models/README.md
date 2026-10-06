# Codex defensive threat-model workflow

The [Codex defensive threat models workflow](../../.github/workflows/codex-threat-models.yml)
produces one defensive threat model for every available RedSec catalog concept and
an [overview](OVERVIEW.md) that can be reviewed and kept in the repository.

Each model answers the design question that matters before a learner or attacker
reaches the flag path:

- What assets and trust boundaries exist?
- Which identities, data flows, protocol messages, tools, and infrastructure can be abused?
- Which preconditions make the abuse path possible?
- Which controls should be implemented before exposure?
- What should be logged, detected, and rehearsed?
- Which benign negative tests show that the controls fail closed?
- Which residual risks and evidence gaps remain?

The reports deliberately omit flags, secrets, payloads, commands, target endpoints,
and step-by-step exploitation. Runtime exploitability is **not verified—outside the
current scope**.

## Current committed assessment

The current [portfolio overview](OVERVIEW.md) and five range reports were produced
directly by a repository-aware Codex session using the same sanitized 110-concept
inventory, together with static inspection of the framework and deployment source.
No challenge, solution, target, or exploit was executed. This is a Codex defensive
static review, not a scan by the separately gated Codex Security product.

Use the [control-gap matrix](CONTROL-GAP-MATRIX.md) when you need the simple view:
component, threat, likely actor, controls in place, and controls missing. Follow its
range links for the complete per-challenge models.

Use [CHALLENGE-LINKS.md](CHALLENGE-LINKS.md) when you want one complete GitHub URL
for every individual challenge threat model.

The API-backed workflow remains the reproducible refresh path. It requires the
`codex-threat-models` GitHub environment and an `OPENAI_API_KEY` environment secret;
neither credential value is stored in the repository or generated reports.

## Security design

The workflow has two jobs with separate permissions:

1. `generate` has read-only repository permission and no GitHub write credential in
   the checkout. A repository-owned Python program sends only curated catalog,
   topology, taxonomy, and provenance metadata to the OpenAI Responses API. It does
   not send flags, hints, solutions, target source, or credentials. The API call has
   no tools and cannot execute repository content.
2. `publish` receives only the validated reports. It has permission to create a
   branch and pull request, but it does not receive `OPENAI_API_KEY`.

The model must return strict JSON. The generator rejects missing or duplicate
catalog keys, changed titles, unapproved evidence paths, excessive field lengths,
and common forms of operational payload content. It then renders five range reports,
five structured JSON files, an integrity manifest, and the portfolio overview.

Model output is review material rather than an approval decision. A maintainer must
confirm the architecture, controls, risk ratings, and evidence before merging.

## Configure it once

1. Create a dedicated OpenAI project or service account for this workflow.
2. Add its API key as the Actions environment secret `OPENAI_API_KEY` in a GitHub
   environment named `codex-threat-models`.
3. Protect that environment so only trusted maintainers and the `main` branch can
   use it. Do not expose the secret to pull-request workflows from forks.
4. Allow GitHub Actions to create pull requests for this repository. If repository
   policy forbids that permission, run with `publish_pull_request` disabled and
   download the private artifact instead.
5. In **Actions → Codex defensive threat models → Run workflow**, choose the model,
   reasoning effort, and whether the run should open a pull request.

The default model is `gpt-6-sol`. A run makes multiple batched API requests and can
incur OpenAI API charges. The workflow is manual-only so catalog changes do not spend
money automatically.

For organizations that prefer short-lived credentials, OpenAI supports GitHub
Actions workload identity federation. Configure exact repository, branch, and
`workflow_ref` claims before adapting this workflow to exchange GitHub OIDC tokens:
<https://developers.openai.com/api/docs/guides/workload-identity-federation/github-actions>.

## Outputs

When `publish_pull_request` is enabled, the workflow opens a pull request containing:

- `docs/threat-models/OVERVIEW.md` — coverage, portfolio priorities, usage sequence,
  and one indexed row per challenge.
- `docs/threat-models/CHALLENGE-LINKS.md` — one complete GitHub URL for every
  challenge's full threat model.
- `docs/threat-models/generated/<range>.md` — the full defensive reviews.
- `docs/threat-models/generated/data/<range>.json` — validated structured results.
- `docs/threat-models/generated/MANIFEST.json` — model, source revision, schema
  version, coverage totals, and output hashes.

If publishing is disabled, the same files are available as a private workflow
artifact for 30 days.

## Codex Security

The model-backed generator and **Codex Security** are related but distinct:

- This workflow uses the OpenAI Responses API to create catalog-wide threat models.
- Codex Security is a separately gated security-analysis product. Running its CLI or
  cloud scans requires Codex Security access.
- If Codex Security Review is connected to this repository, enable
  `request_codex_security_review`. The publish job will comment
  `@codex security review` on the generated pull request so the report changes and
  relevant repository context can receive an additional security review. The review
  runs only when the connected Codex workspace, account access, and repository policy
  accept the bot-authored request; a maintainer can post the same comment manually.

Codex Security Review is a pull-request review; it does not replace the catalog-wide
threat-model generation. Repository-wide Codex Security scans should be configured
separately in Codex Security Cloud or its CLI when the account has access. Official
OpenAI guidance: <https://developers.openai.com/blog/scaling-cyber-defenders-with-daybreak>.

## Local inspection without an API call

You can inspect the exact sanitized inventory and request bodies without a key:

```bash
python scripts/codex_threat_models.py inventory --output /tmp/redsec-inventory.json
python scripts/codex_threat_models.py generate \
  --results-dir /tmp/unused \
  --dry-run \
  --request-dir /tmp/redsec-threat-requests
```

Dry-run output contains the strict response schema and the same curated metadata the
workflow would send. It does not contact OpenAI.
