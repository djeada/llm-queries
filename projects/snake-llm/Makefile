SHELL := /bin/bash

-include .env

MODEL ?= qwen2.5:1.5b
PORT ?= 8000
PROXY_PORT ?= 8787
OLLAMA_URL ?= http://localhost:11434/api/chat
TIMEOUT_MS ?= 8000

.PHONY: help install-model models set-model proxy serve run restart test stop status

help:
	@echo "Snake LLM targets:"
	@echo "  make install-model   Pull the default Ollama model ($(MODEL))"
	@echo "  make models          List locally installed Ollama models"
	@echo "  make set-model       Persist MODEL=<name> into .env"
	@echo "  make proxy           Start the local LLM proxy on port $(PROXY_PORT)"
	@echo "  make serve           Serve the game on http://localhost:$(PORT)"
	@echo "  make run             Start proxy and web server in the background"
	@echo "  make restart         Stop and start with the current model/settings"
	@echo "  make test            Send a sample decision request to the proxy"
	@echo "  make status          Show background processes started by make run"
	@echo "  make stop            Stop background proxy/web server started by make run"
	@echo ""
	@echo "Override examples:"
	@echo "  make run MODEL=qwen3:4b PORT=8010 PROXY_PORT=8788"
	@echo "  make set-model MODEL=qwen3:4b && make install-model restart test"

install-model:
	ollama pull $(MODEL)

models:
	ollama list

set-model:
	@if [[ -z "$(MODEL)" ]]; then \
		echo "Usage: make set-model MODEL=qwen2.5:1.5b"; \
		exit 1; \
	fi
	@{ \
		echo "MODEL=$(MODEL)"; \
		echo "PORT=$(PORT)"; \
		echo "PROXY_PORT=$(PROXY_PORT)"; \
		echo "OLLAMA_URL=$(OLLAMA_URL)"; \
		echo "TIMEOUT_MS=$(TIMEOUT_MS)"; \
	} > .env
	@echo "Saved model/settings to .env"
	@cat .env

proxy:
	SNAKE_LLM_MODEL="$(MODEL)" \
	SNAKE_LLM_PORT="$(PROXY_PORT)" \
	OLLAMA_URL="$(OLLAMA_URL)" \
	SNAKE_LLM_TIMEOUT_MS="$(TIMEOUT_MS)" \
	node snake_llm_proxy.js

serve:
	python3 -m http.server $(PORT)

run:
	@mkdir -p .run
	@if [[ -f .run/proxy.pid ]] && kill -0 "$$(cat .run/proxy.pid)" 2>/dev/null; then \
		echo "Proxy already running with PID $$(cat .run/proxy.pid)"; \
	else \
		SNAKE_LLM_MODEL="$(MODEL)" \
		SNAKE_LLM_PORT="$(PROXY_PORT)" \
		OLLAMA_URL="$(OLLAMA_URL)" \
		SNAKE_LLM_TIMEOUT_MS="$(TIMEOUT_MS)" \
		node snake_llm_proxy.js > .run/proxy.log 2>&1 & \
		echo $$! > .run/proxy.pid; \
		echo "Started proxy on http://localhost:$(PROXY_PORT) with PID $$(cat .run/proxy.pid)"; \
	fi
	@if [[ -f .run/server.pid ]] && kill -0 "$$(cat .run/server.pid)" 2>/dev/null; then \
		echo "Web server already running with PID $$(cat .run/server.pid)"; \
	else \
		python3 -m http.server $(PORT) > .run/server.log 2>&1 & \
		echo $$! > .run/server.pid; \
		echo "Started web server on http://localhost:$(PORT) with PID $$(cat .run/server.pid)"; \
	fi
	@echo "Open http://localhost:$(PORT)"

restart: stop run

test:
	@curl -s -X POST "http://localhost:$(PROXY_PORT)/snake/decide" \
		-H 'Content-Type: application/json' \
		--data '{"gridSize":20,"head":{"x":10,"y":10},"snake":[{"x":10,"y":10}],"direction":"right","food":{"x":14,"y":10},"obstacles":[],"score":0,"level":1,"legalMoves":["up","down","right"]}' \
		&& echo

status:
	@if [[ -f .run/proxy.pid ]] && kill -0 "$$(cat .run/proxy.pid)" 2>/dev/null; then \
		echo "Proxy running: PID $$(cat .run/proxy.pid), http://localhost:$(PROXY_PORT)"; \
	else \
		echo "Proxy not running"; \
	fi
	@if [[ -f .run/server.pid ]] && kill -0 "$$(cat .run/server.pid)" 2>/dev/null; then \
		echo "Web server running: PID $$(cat .run/server.pid), http://localhost:$(PORT)"; \
	else \
		echo "Web server not running"; \
	fi

stop:
	@if [[ -f .run/proxy.pid ]] && kill -0 "$$(cat .run/proxy.pid)" 2>/dev/null; then \
		kill "$$(cat .run/proxy.pid)"; \
		echo "Stopped proxy PID $$(cat .run/proxy.pid)"; \
	fi
	@if [[ -f .run/server.pid ]] && kill -0 "$$(cat .run/server.pid)" 2>/dev/null; then \
		kill "$$(cat .run/server.pid)"; \
		echo "Stopped web server PID $$(cat .run/server.pid)"; \
	fi
	@rm -rf .run
