# PSFnetwork blog production pipeline - operator task runner
#
# Common commands. Run `make help` to see this list.
# All commands assume a venv at .venv created from requirements.txt.

VENV := .venv/bin
PY := $(VENV)/python

.PHONY: help setup test lint lint-staged check-drive list-blog status humanize-status

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

setup:  ## Create venv and install pinned dependencies
	python3 -m venv .venv
	$(VENV)/pip install -r requirements.txt
	@echo "venv ready. Activate with: source .venv/bin/activate"

test:  ## Run the pytest suite
	$(VENV)/pytest tests/ -v

lint:  ## Run check-rules.py against the default scope (README, checklist/, workflow/, brand/)
	$(PY) workflow/check-rules.py

lint-staged:  ## Run check-rules.py against git-staged .md files
	$(PY) workflow/check-rules.py --staged

lint-all:  ## Run check-rules.py against every .md file in the repo
	$(PY) workflow/check-rules.py $$(find . -name '*.md' -not -path './.git/*' -not -path './.venv/*')

check-drive:  ## Verify the Drive token works and list the operator's drive root
	$(PY) workflow/drive_cli.py health

list-blog:  ## Show every blog slug with its current stage
	@for d in blog/*/; do \
		slug=$$(basename $$d); \
		stage=$$(jq -r '.stage // "(no state)"' $$d/pipeline-state.json 2>/dev/null || echo "(no state)"); \
		printf "  %-50s %s\n" "$$slug" "$$stage"; \
	done

humanize-status:  ## Show which slugs have a v2 humanized draft
	@for d in blog/*/; do \
		slug=$$(basename $$d); \
		if [ -f $$d/draft-v2-humanized.md ]; then \
			printf "  v2  %s\n" "$$slug"; \
		else \
			printf "  v1  %s\n" "$$slug"; \
		fi \
	done

brief-preflight:  ## Verify a brief is ready for Stage 2. Usage: make brief-preflight SLUG=<slug>
	@if [ -z "$(SLUG)" ]; then echo "Usage: make brief-preflight SLUG=<slug>"; exit 2; fi
	$(PY) workflow/brief_preflight.py blog/$(SLUG)/brief.md

meta-qa:  ## Stage 11 sub-step: scan operational artifacts against checklist/meta-qa.md
	$(PY) workflow/check-rules.py README.md ROADMAP.md $$(find checklist workflow brand -name '*.md')

status: lint list-blog humanize-status  ## One-shot repo health snapshot
