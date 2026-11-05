ROPS_HOME ?= /Users/nifemi/researchops

reproduce: run analyze claims lint preflight

run:
	rops-run grid .

analyze:
	@for f in $$(ls analysis/*.py 2>/dev/null | grep -v '/figures\.py$$' | sort); do \
		echo "== $$f"; PYTHONPATH=$(ROPS_HOME) python3 $$f || exit 1; \
	done

claims:
	rops-claims build .

lint:
	rops-lint paper/paper.md

preflight:
	rops-preflight .

guard:
	rops-guard check .
