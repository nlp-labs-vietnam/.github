#!/usr/bin/env python3
"""
.github/actions/validate-nlp-data/validate_data.py
────────────────────────────────────────────────────
Script kiểm tra chất lượng dữ liệu NLP đầu vào.
Được gọi bởi custom action validate-nlp-data/action.yml.

Hỗ trợ định dạng:
  - JSONL : {"query": "...", "positive": "...", "negative": "..."}
  - CSV   : có cột text, label (tuỳ chọn)
  - YAML  : file cấu hình (delegate sang validate_configs.py)
  - auto  : tự phát hiện theo extension

Chạy:
    python validate_data.py --data-path data/train.jsonl --format jsonl
    python validate_data.py --data-path data/ --format auto --max-samples 500
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

# ─── Validators theo định dạng ────────────────────────────────────────────────


def _validate_jsonl(path: Path, max_samples: int) -> dict[str, Any]:
    """Kiểm tra file JSONL: mỗi dòng là một JSON object hợp lệ."""
    total = valid = invalid = 0
    errors: list[str] = []
    empty_text = 0

    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if max_samples and total >= max_samples:
                break
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                obj = json.loads(line)
                if not isinstance(obj, dict):
                    invalid += 1
                    errors.append(f"Dòng {lineno}: không phải JSON object")
                    continue

                # Kiểm tra trường text phổ biến
                text_fields = {"text", "query", "sentence", "sentence1", "content"}
                found = text_fields & set(obj.keys())
                if found:
                    for field in found:
                        val = obj[field]
                        if not val or not str(val).strip():
                            empty_text += 1

                valid += 1
            except json.JSONDecodeError as e:
                invalid += 1
                errors.append(f"Dòng {lineno}: JSON parse error — {e.msg}")

    validity_rate = valid / total if total else 0.0
    return {
        "format": "jsonl",
        "total_samples": total,
        "valid_samples": valid,
        "invalid_samples": invalid,
        "empty_text_fields": empty_text,
        "validity_rate": validity_rate,
        "errors": errors[:20],  # Giới hạn 20 lỗi đầu tiên
        "passed": invalid == 0,
    }


def _validate_csv(path: Path, max_samples: int) -> dict[str, Any]:
    """Kiểm tra file CSV: header hợp lệ, không có ô rỗng ở cột text."""
    total = valid = invalid = 0
    errors: list[str] = []
    missing_text = 0

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return {
                "format": "csv",
                "total_samples": 0,
                "valid_samples": 0,
                "invalid_samples": 0,
                "validity_rate": 0.0,
                "errors": ["File CSV không có header"],
                "passed": False,
            }

        text_cols = [c for c in reader.fieldnames if c.lower() in {"text", "query", "content", "sentence"}]

        for rowno, row in enumerate(reader, 2):
            if max_samples and total >= max_samples:
                break
            total += 1

            row_valid = True
            for col in text_cols:
                val = row.get(col, "").strip()
                if not val:
                    missing_text += 1
                    row_valid = False
                    errors.append(f"Dòng {rowno}: cột '{col}' rỗng")

            if row_valid:
                valid += 1
            else:
                invalid += 1

    validity_rate = valid / total if total else 0.0
    return {
        "format": "csv",
        "total_samples": total,
        "valid_samples": valid,
        "invalid_samples": invalid,
        "missing_text_cells": missing_text,
        "validity_rate": validity_rate,
        "errors": errors[:20],
        "passed": invalid == 0,
    }


def _auto_detect_format(path: Path) -> str:
    suffix = path.suffix.lower()
    mapping = {".jsonl": "jsonl", ".json": "jsonl", ".csv": "csv",
               ".yml": "yaml", ".yaml": "yaml"}
    return mapping.get(suffix, "jsonl")


def validate_file(path: Path, fmt: str, max_samples: int) -> dict[str, Any]:
    if fmt == "auto":
        fmt = _auto_detect_format(path)

    if fmt == "jsonl":
        return _validate_jsonl(path, max_samples)
    if fmt == "csv":
        return _validate_csv(path, max_samples)
    # yaml → delegate to validate_configs.py behaviour (just parse check)
    try:
        import yaml  # noqa: PLC0415
        with open(path, encoding="utf-8") as f:
            yaml.safe_load(f)
        return {"format": "yaml", "total_samples": 1, "valid_samples": 1,
                "invalid_samples": 0, "validity_rate": 1.0, "errors": [], "passed": True}
    except Exception as e:
        return {"format": "yaml", "total_samples": 1, "valid_samples": 0,
                "invalid_samples": 1, "validity_rate": 0.0,
                "errors": [str(e)], "passed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate NLP data files")
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--schema-path", default="")
    parser.add_argument("--format", default="auto")
    parser.add_argument("--max-samples", type=int, default=1000)
    parser.add_argument("--fail-on-warning", default="false")
    parser.add_argument("--output-file", default="/tmp/validation-report.json")
    args = parser.parse_args()

    data_path = Path(args.data_path)

    # Thu thập danh sách file cần kiểm tra
    if data_path.is_dir():
        exts = {".jsonl", ".json", ".csv", ".yml", ".yaml"}
        files = [f for f in sorted(data_path.rglob("*")) if f.suffix.lower() in exts]
    elif data_path.exists():
        files = [data_path]
    else:
        print(f"⚠️  Đường dẫn không tồn tại: {data_path} — bỏ qua")
        report = {"total_samples": 0, "valid_samples": 0, "invalid_samples": 0,
                  "validity_rate": 1.0, "files": [], "passed": True}
        Path(args.output_file).write_text(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0)

    # Kiểm tra từng file
    all_results = []
    for f in files:
        result = validate_file(f, args.format, args.max_samples)
        result["file"] = str(f)
        all_results.append(result)
        status = "✅" if result["passed"] else "❌"
        print(f"{status}  {f.name}: {result['valid_samples']}/{result['total_samples']} hợp lệ "
              f"({result['validity_rate']:.1%})")
        for err in result.get("errors", [])[:5]:
            print(f"     ⚠  {err}")

    # Tổng hợp
    total = sum(r["total_samples"] for r in all_results)
    valid = sum(r["valid_samples"] for r in all_results)
    invalid = sum(r["invalid_samples"] for r in all_results)
    overall_passed = all(r["passed"] for r in all_results)

    summary = {
        "total_samples": total,
        "valid_samples": valid,
        "invalid_samples": invalid,
        "validity_rate": valid / total if total else 1.0,
        "files_checked": len(all_results),
        "files": all_results,
        "passed": overall_passed,
    }

    Path(args.output_file).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n{'─' * 50}")
    print(f"{'✅' if overall_passed else '❌'}  Tổng: {valid}/{total} mẫu hợp lệ "
          f"({summary['validity_rate']:.1%})")

    if not overall_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
