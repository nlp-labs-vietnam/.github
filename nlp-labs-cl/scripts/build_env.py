#!/usr/bin/env python3
"""
scripts/build_env.py
────────────────────
Script chuẩn bị môi trường phát triển đồng bộ cho toàn bộ thành viên.
Tự động phát hiện OS, kiểm tra prerequisites, cài dependencies.

Chạy:
    python scripts/build_env.py
    python scripts/build_env.py --module tokenizer
    python scripts/build_env.py --docker          # Build Docker images local
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_PYTHON = (3, 10)
MODULES = ["tokenizer", "embedding", "ner"]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Chạy command và hiển thị output theo thời gian thực."""
    print(f"\n▶  {' '.join(cmd)}")
    return subprocess.run(cmd, check=check)


def check_prerequisites() -> None:
    """Kiểm tra các công cụ cần thiết đã được cài đặt."""
    errors = []

    # Python version
    major, minor = sys.version_info[:2]
    if (major, minor) < REQUIRED_PYTHON:
        errors.append(
            f"Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ cần thiết, "
            f"hiện tại: {major}.{minor}"
        )

    # Git
    if not shutil.which("git"):
        errors.append("Git chưa được cài đặt")

    # Docker (tuỳ chọn)
    if not shutil.which("docker"):
        print("⚠️  Docker chưa được cài đặt — bỏ qua các bước Docker")

    if errors:
        for e in errors:
            print(f"❌  {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅  Python {major}.{minor} — OK")
    print(f"✅  Git {subprocess.check_output(['git', '--version']).decode().strip()} — OK")
    print(f"✅  OS: {platform.system()} {platform.release()}")


def install_dependencies(module: str | None = None) -> None:
    """Cài đặt pip dependencies."""
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # Root requirements
    root_req = ROOT / "requirements.txt"
    if root_req.exists():
        run([sys.executable, "-m", "pip", "install", "-r", str(root_req)])

    dev_req = ROOT / "requirements-dev.txt"
    if dev_req.exists():
        run([sys.executable, "-m", "pip", "install", "-r", str(dev_req)])

    # Module-specific
    targets = [module] if module else MODULES
    for mod in targets:
        mod_req = ROOT / "modules" / mod / "requirements.txt"
        if mod_req.exists():
            print(f"\n📦  Cài đặt dependencies cho module: {mod}")
            run([sys.executable, "-m", "pip", "install", "-r", str(mod_req)])


def build_docker_images() -> None:
    """Build tất cả Docker base images."""
    if not shutil.which("docker"):
        print("⚠️  Docker không có — bỏ qua", file=sys.stderr)
        return

    images = [
        ("build-env-base", ROOT / "docker" / "build-env-base"),
        ("dev-env-base",   ROOT / "docker" / "dev-env-base"),
        ("run-env-base",   ROOT / "docker" / "run-env-base"),
    ]

    for tag, ctx in images:
        full_tag = f"ghcr.io/nlp-labs-vietnam/nlp-labs-cl/{tag}:local"
        run(["docker", "build", "-t", full_tag, str(ctx)])
        print(f"✅  {full_tag} — built")


def run_tests(module: str | None = None) -> None:
    """Chạy test suite để xác nhận môi trường hoạt động."""
    targets = [f"modules/{module}/tests"] if module else ["tests/", "modules/"]
    run([sys.executable, "-m", "pytest", *targets, "-v", "--tb=short", "-q"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chuẩn bị môi trường phát triển nlp-labs-cl"
    )
    parser.add_argument("--module", choices=MODULES, help="Chỉ cài deps cho một module cụ thể")
    parser.add_argument("--docker", action="store_true", help="Build Docker base images")
    parser.add_argument("--skip-tests", action="store_true", help="Bỏ qua bước chạy tests")
    args = parser.parse_args()

    print("=" * 60)
    print("  NLP Labs Vietnam — Chuẩn bị môi trường phát triển")
    print("=" * 60)

    check_prerequisites()
    install_dependencies(args.module)

    if args.docker:
        build_docker_images()

    if not args.skip_tests:
        run_tests(args.module)

    print("\n" + "=" * 60)
    print("  ✅  Môi trường đã sẵn sàng!")
    print("=" * 60)


if __name__ == "__main__":
    main()
