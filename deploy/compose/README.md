# Local development

You do **not** need Docker or docker-compose to run a module locally. The CLI runs
targets as plain processes:

```bash
redsec dev 03      # starts the module's targets with uvicorn; Ctrl-C to stop
```

This is the recommended local path: it needs no images, resolves peer URLs and the
sink automatically, and is what `redsec selftest` uses.

Use Docker/Kubernetes ([../../docs/kubernetes.md](../../docs/kubernetes.md)) when you
want a shared range, realistic isolation (NetworkPolicies), or a multi-student
deployment. Build images with `../../scripts/build_images.sh`.

(If you specifically want docker-compose for a module, generate one from the
`targets` in its `module.yaml`; a generator is a welcome contribution.)
