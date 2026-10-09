# ─────────────────────────────────────────────────────────────────────────────
# Makefile — nlp-labs-cl
# Developer shortcuts. Chạy `make help` để xem tất cả lệnh.
# ─────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
PYTHON        := python3
PIP           := $(PYTHON) -m pip
PYTEST        := $(PYTHON) -m pytest
MODULE        ?= all

.PHONY: help setup setup-module lint format typecheck test test-module \
        test-cov validate-configs pipeline docker-build docker-up docker-down clean

# ─── Help ─────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  NLP Labs Vietnam — nlp-labs-cl"
	@echo "  ─────────────────────────────────────────"
	@echo "  Sử dụng: make <target> [MODULE=tokenizer|embedding|ner]"
	@echo ""
	@echo "  Setup:"
	@echo "    setup             Cài đặt toàn bộ môi trường phát triển"
	@echo "    setup-module      Cài dependencies cho một module (MODULE=...)"
	@echo ""
	@echo "  Chất lượng code:"
	@echo "    lint              Chạy Ruff linter"
	@echo "    format            Format code với Black"
	@echo "    typecheck         Kiểm tra types với Mypy"
	@echo ""
	@echo "  Kiểm thử:"
	@echo "    test              Chạy toàn bộ test suite"
	@echo "    test-module       Chạy tests cho một module (MODULE=...)"
	@echo "    test-cov          Chạy tests với coverage report"
	@echo ""
	@echo "  Configs & Pipeline:"
	@echo "    validate-configs  Kiểm tra tất cả YAML configs"
	@echo "    pipeline          Chạy solar-qa pipeline mẫu"
	@echo ""
	@echo "  Docker:"
	@echo "    docker-build      Build tất cả Docker base images"
	@echo "    docker-up         Khởi động dev stack (JupyterLab + ChromaDB + API)"
	@echo "    docker-down       Dừng dev stack"
	@echo ""
	@echo "  Dọn dẹp:"
	@echo "    clean             Xóa cache và artifacts"
	@echo ""

# ─── Setup ────────────────────────────────────────────────────────────────────
setup:
	$(PYTHON) scripts/build_env.py --skip-tests
	@echo "✅  Setup hoàn thành. Chạy 'make test' để kiểm tra."

setup-module:
	$(PYTHON) scripts/build_env.py --module $(MODULE) --skip-tests

# ─── Chất lượng code ──────────────────────────────────────────────────────────
lint:
	ruff check . --output-format=concise
	@echo "✅  Lint passed"

format:
	black .
	ruff check . --fix
	@echo "✅  Format hoàn thành"

format-check:
	black --check --diff .
	ruff check .

typecheck:
	mypy modules/ --ignore-missing-imports --pretty
	@echo "✅  Type check passed"

# ─── Kiểm thử ─────────────────────────────────────────────────────────────────
test:
	$(PYTEST) modules/ tests/ -v --tb=short -q

test-module:
	$(PYTEST) modules/$(MODULE)/tests/ -v --tb=short

test-cov:
	$(PYTEST) modules/ \
		--cov=modules \
		--cov-report=html:htmlcov \
		--cov-report=term-missing \
		--cov-fail-under=70
	@echo "✅  Coverage report tại: htmlcov/index.html"

test-fast:
	$(PYTEST) modules/ -q --tb=no -m "not slow"

# ─── Configs & Pipeline ───────────────────────────────────────────────────────
validate-configs:
	$(PYTHON) scripts/validate_configs.py --dir configs/
	@echo "✅  Configs hợp lệ"

pipeline:
	$(PYTHON) scripts/run_pipeline.py \
		--config configs/pipeline/solar-qa.yml \
		--dry-run

# ─── Docker ───────────────────────────────────────────────────────────────────
docker-build:
	$(PYTHON) scripts/build_env.py --docker --skip-tests

docker-up:
	cd docker && docker compose up -d
	@echo "✅  Dev stack đang chạy:"
	@echo "    JupyterLab : http://localhost:8888"
	@echo "    API        : http://localhost:8000"
	@echo "    ChromaDB   : http://localhost:8001"

docker-down:
	cd docker && docker compose down

docker-logs:
	cd docker && docker compose logs -f

# ─── Dọn dẹp ──────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "coverage*.xml" -delete 2>/dev/null || true
	@echo "✅  Clean hoàn thành"

# ─── CI shortcuts (dùng trong pipeline) ──────────────────────────────────────
ci-lint: format-check typecheck
ci-test: test-cov
ci-all: ci-lint ci-test validate-configs
