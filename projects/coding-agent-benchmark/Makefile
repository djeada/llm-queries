SHELL := /bin/bash

.PHONY: help check list

help:
	@echo "coding-agent-benchmark targets:"
	@echo "  make check  Validate benchmark seeds and golden solutions"
	@echo "  make list   List benchmark cases"

check:
	python3 -m py_compile benchmark.py cases/*/evaluator.py
	python3 benchmark.py self-test

list:
	python3 benchmark.py list
