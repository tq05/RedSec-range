# Module 02 — Reconnaissance for AI Targets

> **Target:** `saas` (InitrodeAI front-end). **Maps to:** AI-300 Module 2 · OWASP
> LLM07, LLM02 · MITRE ATLAS AML.T0002, AML.T0040.

## 1. Idea

You cannot attack what you cannot see. Before any injection or exploit, map the AI
attack surface: which model/provider is behind a feature, what endpoints exist
(including the ones nobody linked), and what metadata leaks for free. AI apps leak
in the same boring ways as any web app — headers, build endpoints, crawler files,
and verbose error pages — plus a few AI-specific ones (model/provider tells,
prompt-version strings, guardrail metadata).

## 2. Start the range

```bash
redsec up 02            # start the target in the background
redsec info 02
```

(Use `redsec dev 02` instead if you want it in the foreground. Stop later with
`redsec down 02`.)

## 3. Walkthrough

> Replace `URL` with the target URL printed by `redsec up` (default
> `http://127.0.0.1:9020`).

### 3.1 `fingerprint-model` — find the model (LLM07)
Look at headers and page source first, then follow the trail:

```bash
URL=http://127.0.0.1:9020
curl -si $URL/ | grep -i x-powered-by        # leaks the stack + model
curl -s  $URL/ | grep -i '<!--'              # a comment points to build metadata
curl -s  $URL/api/version                    # model, provider, and debug_token
redsec submit 02 fingerprint-model 'REDSEC{...}'
```

### 3.2 `enumerate-surfaces` — find the hidden route
Crawler files advertise what the site tries to hide:

```bash
curl -s $URL/robots.txt                       # Disallow: /v1/internal/
curl -s $URL/v1/internal/                      # unauthenticated -> flag
redsec submit 02 enumerate-surfaces 'REDSEC{...}'
```

### 3.3 `leak-config` — verbose error (LLM02)
Send the chat endpoint something it doesn't expect and read the debug error:

```bash
curl -s $URL/chat -H 'content-type: application/json' \
  -d '{"message": {"not":"a string"}}'         # 500 with a config dump
redsec submit 02 leak-config 'REDSEC{...}'
```

Verify everything and tear down:

```bash
redsec verify 02       # re-checks submitted flags / oracles
redsec down 02
```

## 4. Defenses

- Strip stack/model banners (`X-Powered-By`); don't expose build/version endpoints
  publicly; authenticate "internal" routes (and don't rely on robots.txt as a
  control — it advertises, it doesn't protect).
- Disable debug error pages in production; return generic errors and log details
  server-side. Never put secrets in config that an error page can render.
- Treat model/provider identity and prompt-version strings as information an
  attacker will use to tailor payloads (later modules).
