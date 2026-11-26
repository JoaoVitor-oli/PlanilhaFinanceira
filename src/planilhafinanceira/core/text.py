from __future__ import annotations

import unicodedata


def sort_key(text: str) -> str:
    """Ordena ignorando acentos e maiúsculas ("Água" antes de "Banco")."""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch)).casefold()

def plural(count: int, singular: str, plural_form: str | None = None) -> str:
    word = singular if count == 1 else (plural_form or singular + "s")
    return f"{count} {word}"

def count_text(count: int, singular: str = "lançamento") -> str:
    return f"nenhum {singular}" if count == 0 else plural(count, singular)