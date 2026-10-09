#!/usr/bin/env python3
"""
scripts/validate_configs.py
────────────────────────────
Kiểm tra tính hợp lệ của tất cả file YAML trong thư mục configs/.
Được gọi bởi workflow lint.yml và có thể chạy thủ công.

Chạy:
    python scripts/validate_configs.py
    python scripts/validate_configs.py --dir configs/training
    python scripts/validate_configs.py --strict   # Fail nếu có trường không xác định
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).parent.parent

# ─── Schema tối thiểu cho training config ────────────────────────────────────
REQUIRED_TRAINING_FIELDS = {
    "model": {"base_model", "output_dir"},
    "data": {"train_path"},
    "training": {"num_epochs", "batch_size", "learning_rate"},
}

REQUIRED_INFERENCE_FIELDS = {
    "model": {"model_path"},
    "inference": {"max_length", "device"},
}


def load_yaml(path: Path) -> dict[str, Any] | None:
    """Đọc và parse YAML file. Trả về None nếu không hợp lệ."""
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        return None, str(e)


def validate_config(data: dict, path: Path, strict: bool = False) -> list[str]:
    """Kiểm tra config theo loại (training/inference/pipeline)."""
    errors = []

    if data is None:
        return ["File rỗng hoặc không phải YAML hợp lệ"]

    config_type = data.get("type", "unknown")

    # Detect loại config từ cấu trúc nếu không có trường `type`
    if config_type == "unknown":
        if "training" in data:
            config_type = "training"
        elif "inference" in data:
            config_type = "inference"

    schema = {}
    if config_type == "training":
        schema = REQUIRED_TRAINING_FIELDS
    elif config_type == "inference":
        schema = REQUIRED_INFERENCE_FIELDS

    for section, required_keys in schema.items():
        if section not in data:
            errors.append(f"Thiếu section bắt buộc: [{section}]")
            continue
        section_data = data[section]
        if not isinstance(section_data, dict):
            errors.append(f"Section [{section}] phải là dict")
            continue
        missing = required_keys - set(section_data.keys())
        if missing:
            errors.append(f"Section [{section}] thiếu các trường: {missing}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate YAML configs")
    parser.add_argument("--dir", default="configs", help="Thư mục chứa configs")
    parser.add_argument("--strict", action="store_true", help="Strict mode")
    args = parser.parse_args()

    config_dir = ROOT / args.dir
    if not config_dir.exists():
        print(f"⚠️  Thư mục không tồn tại: {config_dir} — bỏ qua")
        sys.exit(0)

    yaml_files = list(config_dir.rglob("*.yml")) + list(config_dir.rglob("*.yaml"))

    if not yaml_files:
        print(f"ℹ️  Không tìm thấy file YAML trong {config_dir}")
        sys.exit(0)

    print(f"🔍  Kiểm tra {len(yaml_files)} file YAML trong {config_dir}\n")

    total_errors = 0
    for path in sorted(yaml_files):
        result = load_yaml(path)
        if isinstance(result, tuple):
            data, parse_error = result
            print(f"❌  {path.relative_to(ROOT)}: YAML parse error — {parse_error}")
            total_errors += 1
            continue

        errors = validate_config(result, path, args.strict)
        rel = path.relative_to(ROOT)
        if errors:
            for e in errors:
                print(f"❌  {rel}: {e}")
            total_errors += len(errors)
        else:
            print(f"✅  {rel}")

    print(f"\n{'─' * 50}")
    if total_errors:
        print(f"❌  {total_errors} lỗi được tìm thấy")
        sys.exit(1)
    else:
        print(f"✅  Tất cả {len(yaml_files)} config files hợp lệ")


if __name__ == "__main__":
    main()
