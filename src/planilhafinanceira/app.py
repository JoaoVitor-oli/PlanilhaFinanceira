from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QLabel

from planilhafinanceira import APP_NAME
from planilhafinanceira.config import data_dir


def main() -> int:
    app = QApplication(sys.argv)
    janela = QLabel(f"{APP_NAME} em construção. Dados em: {data_dir()}")
    janela.resize(560, 140)
    janela.show()
    return app.exec()