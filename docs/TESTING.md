redsec doctor        # 11/11 modules load + checks resolve
redsec selftest      # 42/42 challenges: verify FAILS pre-exploit, PASSES post-exploit
pytest -q            # 26 unit + per-module integration tests (includes tests/test_m09_crown_chain.py)
```
That proves every challenge is solvable by its real exploit. For the **container**
path (real Docker, production images):
```bash
./scripts/build_base_image.sh          # or: REGISTRY=ghcr.io/you ./scripts/build_images.sh
python scripts/docker_run_all.py --real   # 39/39 container-backed challenges
```
