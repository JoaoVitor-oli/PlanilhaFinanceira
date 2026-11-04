from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

MINUS = "\N{MINUS SIGN}"     # sinal de menos tipográfico (mais largo que o hífen)
NBSP = "\N{NO-BREAK SPACE}"   # espaço que não quebra linha entre "R$" e o número



def parse_brl(text: str) -> int:
    """Converte texto digitado em centavos. Levanta ValueError com mensagem para a tela."""
    raw = text
    s = text.strip().replace("R$", "").replace(" ", "").replace(NBSP, "").replace(MINUS, "-")
    if not s:
        raise ValueError("Informe um valor.")

    negative = s.startswith("-")
    s = s.lstrip("+-")

    if "," in s:
        # Formato brasileiro: ponto separa milhar, vírgula separa centavos.
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") == 1 and len(s.split(".")[1]) <= 2:
        # "1234.56": provavelmente colado de outro lugar; o ponto é decimal.
        pass
    else:
        # "1.234" ou "1.234.567": os pontos são separadores de milhar.
        s = s.replace(".", "")

    try:
        value = Decimal(s)

    except InvalidOperation:
        raise ValueError(f"“{raw.strip()}” não é um valor válido.") from None

    cents = int((value * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return -cents if negative else cents


def format_brl(cents: int, *, sign: bool = False, symbol: bool = True) -> str:
    """123456 -> "R$ 1.234,56". sign=True mostra "+" nos positivos (útil em extratos)."""
    whole, frac = divmod(abs(cents), 100)
    body = f"{whole:,}".replace(",", ".") + f",{frac:02d}"
    prefix = f"R${NBSP}" if symbol else ""
    if cents < 0:
        return f"{MINUS}{prefix}{body}"
    if sign and cents > 0:
        return f"+{prefix}{body}"
    return f"{prefix}{body}"


def format_compact(cents: int) -> str:
    """Versão curta para eixos de gráfico: "R$ 850", "R$ 5,2 mil", "R$ 1,3 mi"."""
    value = abs(cents) / 100
    if value >= 1_000_000:
        text = f"{value / 1_000_000:.1f}".replace(".", ",").removesuffix(",0") + " mi"
    elif value >= 1_000:
        text = f"{value / 1_000:.1f}".replace(".", ",").removesuffix(",0") + " mil"
    else:
        text = f"{value:.0f}"
    return f"{MINUS if cents < 0 else ''}R${NBSP}{text}"


def to_input_text(cents: int) -> str:
    """Formato para campos de edição, sem "R$": "1.234,56"."""
    return format_brl(cents, symbol=False).replace(MINUS, "-")
    