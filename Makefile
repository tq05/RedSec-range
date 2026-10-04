.PHONY: help install test doctor selftest validate-k8s lint-helm build-images clean

help:          ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n",$$1,$$2}'

install:       ## Install the framework (editable) + dev deps
	pip install -e ".[dev]" kubernetes-validate

test:          ## Run unit + integration tests
	pytest -q

doctor:        ## Validate every module loads and resolves its checks
	redsec doctor

selftest:      ## Prove every complete module is solvable (fail -> pass)
	redsec selftest

validate-k8s:  ## Validate rendered Kubernetes manifests offline
	python scripts/validate_manifests.py

lint-helm:     ## Lint the Helm chart (requires helm)
	helm lint deploy/helm/redsec-module

build-images:  ## Build all container images (requires Docker)
	./scripts/build_images.sh

clean:         ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist *.egg-info .pytest_cache
