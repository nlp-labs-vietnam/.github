"""
src/core/logging.py
────────────────────
Cấu hình logging chuẩn cho toàn bộ ứng dụng.
Xuất JSON logs khi production, pretty logs khi debug.
"""

import logging
import sys

from src.core.config import settings


def setup_logging() -> None:
    """Khởi tạo logging với format phù hợp theo môi trường."""
    level = getattr(logging, settings.LOG_LEVEL, logging.INFO)

    if settings.DEBUG:
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        datefmt = "%H:%M:%S"
    else:
        # JSON-friendly format để dễ parse bởi log aggregators (Loki, CloudWatch)
        fmt = (
            '{"time":"%(asctime)s","level":"%(levelname)s",'
            '"logger":"%(name)s","msg":"%(message)s"}'
        )
        datefmt = "%Y-%m-%dT%H:%M:%S"

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # Tắt bớt noise từ thư viện bên ngoài
    for noisy in ("httpx", "httpcore", "urllib3", "chromadb.telemetry"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        "Logging initialized — level=%s debug=%s", settings.LOG_LEVEL, settings.DEBUG
    )
