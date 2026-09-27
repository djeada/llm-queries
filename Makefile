SHELL := /bin/bash

.PHONY: help check check-content check-evals check-projects check-links generate freshness

help:
	@echo "llm-queries maintenance targets:"
	@echo "  make check           Run repository, eval-runner, and project checks"
	@echo "  make generate        Refresh generated catalog and health reports"
	@echo "  make freshness       Enforce review deadlines for current content"
	@echo "  make check-evals     Validate and regression-test executable eval specs"
	@echo "  make check-projects  Run checks for runnable projects"
	@echo "  make check-links     Check external Markdown links (networked)"

check: check-content check-evals check-projects

check-content:
	python3 -m py_compile scripts/repo_check.py scripts/run_evals.py scripts/compare_eval_reports.py scripts/check_external_links.py
	python3 scripts/repo_check.py

check-evals:
	python3 scripts/run_evals.py evaluations/specs/core.jsonl
	@tmp_dir="$(mktemp -d)"; trap 'rm -rf "$tmp_dir"' EXIT; \
	python3 scripts/run_evals.py evaluations/specs/core.jsonl \
		--responses evaluations/fixtures/core-passing-responses.jsonl \
		--label baseline \
		--meta runtime=fixture \
		--output "$tmp_dir/baseline.json" \
		--min-pass-rate 1; \
	python3 scripts/run_evals.py evaluations/specs/core.jsonl \
		--responses evaluations/fixtures/core-passing-responses.jsonl \
		--label candidate \
		--meta runtime=fixture \
		--output "$tmp_dir/candidate.json" \
		--min-pass-rate 1; \
	python3 scripts/compare_eval_reports.py \
		"$tmp_dir/baseline.json" "$tmp_dir/candidate.json" \
		--require-same-spec

check-projects:
	$(MAKE) -C projects/snake-llm check

check-links:
	python3 scripts/check_external_links.py

generate:
	python3 scripts/repo_check.py --write-generated

freshness:
	python3 scripts/repo_check.py --strict-freshness
