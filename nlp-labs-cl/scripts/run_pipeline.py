#!/usr/bin/env python3
"""
scripts/run_pipeline.py
────────────────────────
Script chạy toàn bộ NLP pipeline theo thứ tự:
  tokenizer → embedding → ner (tuỳ chọn)

Chạy:
    python scripts/run_pipeline.py --config configs/pipeline/solar-qa.yml
    python scripts/run_pipeline.py --config configs/pipeline/solar-qa.yml --dry-run
    python scripts/run_pipeline.py --modules tokenizer,embedding --input data/raw/
"""

import argparse
import importlib
import time
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).parent.parent
MODULE_ORDER = ["tokenizer", "embedding", "ner"]


def load_pipeline_config(config_path: Path) -> dict[str, Any]:
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_module(module_name: str, config: dict, dry_run: bool = False) -> dict:
    """Nạp và chạy một module NLP."""
    print(f"\n{'─' * 50}")
    print(f"▶  Module: {module_name}")
    print(f"{'─' * 50}")

    if dry_run:
        print(f"   [DRY RUN] Bỏ qua thực thi")
        return {"status": "skipped", "module": module_name}

    start = time.time()
    try:
        mod = importlib.import_module(f"modules.{module_name}")
        result = mod.run(config.get(module_name, {}))
        elapsed = time.time() - start
        print(f"✅  {module_name} hoàn thành trong {elapsed:.2f}s")
        return {"status": "success", "module": module_name, "elapsed": elapsed, **result}
    except Exception as e:
        print(f"❌  {module_name} thất bại: {e}")
        return {"status": "error", "module": module_name, "error": str(e)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy NLP pipeline")
    parser.add_argument("--config", required=True, help="Đường dẫn đến pipeline config YAML")
    parser.add_argument("--modules", help="Danh sách modules cần chạy, phân cách bởi dấu phẩy")
    parser.add_argument("--dry-run", action="store_true", help="Kiểm tra config mà không thực thi")
    parser.add_argument("--input", help="Override đường dẫn input data")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌  Config không tồn tại: {config_path}")
        raise SystemExit(1)

    config = load_pipeline_config(config_path)

    if args.input:
        config.setdefault("data", {})["input_path"] = args.input

    modules = args.modules.split(",") if args.modules else MODULE_ORDER
    modules = [m.strip() for m in modules if m.strip() in MODULE_ORDER]

    print("=" * 60)
    print("  NLP Labs Vietnam — Pipeline Runner")
    print(f"  Config: {config_path.name}")
    print(f"  Modules: {' → '.join(modules)}")
    if args.dry_run:
        print("  Mode: DRY RUN")
    print("=" * 60)

    results = []
    for module in modules:
        result = run_module(module, config, dry_run=args.dry_run)
        results.append(result)
        if result["status"] == "error":
            print(f"\n❌  Pipeline dừng tại module: {module}")
            raise SystemExit(1)

    print("\n" + "=" * 60)
    success = sum(1 for r in results if r["status"] == "success")
    print(f"  ✅  Pipeline hoàn thành: {success}/{len(results)} modules")
    total_time = sum(r.get("elapsed", 0) for r in results)
    print(f"  ⏱️  Tổng thời gian: {total_time:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
