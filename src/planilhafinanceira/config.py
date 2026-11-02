from __future__ import annotations

from pathlib import Path

from platformdirs import user_data_path

from planilhafinanceira import APP_NAME

PACKAGE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = PACKAGE_DIR / "resources"
FONTS_DIR = RESOURCES_DIR / "fonts"


def data_dir() -> Path:
    """Windows: C:\\Users\\<você>\\AppData\\Local\\PlanilhaFinanceira"""
    path = user_data_path(APP_NAME, appauthor=False)
    path.mkdir(parents=True, exist_ok=True)
    return path

def default_db_path(demo: bool = False) -> Path:
    return data_dir() / ("planilhafinanceira-demo.db" if demo else "planilhafinanceira.db")