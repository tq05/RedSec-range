# Codex defensive threat-model overview

No Codex-generated portfolio has been committed yet. Run the manual
[Codex defensive threat models workflow](../../.github/workflows/codex-threat-models.yml)
to generate validated reports for all **110 challenge concepts** and **162 declared
variants**. With publishing enabled, the workflow will replace this page and open a
reviewable pull request containing the five range reports, structured JSON, and an
integrity manifest.

The output will describe assets, trust boundaries, high-level abuse paths, controls
to implement before exposure, detection and response, benign validation, and
residual risk. It will not include flags, secrets, payloads, commands, or
step-by-step exploitation.

Runtime exploitability is **not verified—outside the current scope**.
