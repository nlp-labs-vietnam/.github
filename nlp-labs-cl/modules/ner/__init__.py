"""
modules/ner/__init__.py
NER module — Nhận dạng thực thể đặc thù cho domain Solar/Energy
"""

from .ner import SolarNERExtractor

__all__ = ["SolarNERExtractor", "run"]


def run(config: dict) -> dict:
    """Entry point cho pipeline runner."""
    extractor = SolarNERExtractor(config)
    return extractor.process_batch(config.get("input_path", ""))
