import pytest

from planilhafinanceira.core.money import(
    MINUS,
    NBSP,
    format_compact,
    parse_brl,
    to_input_text,
)

@pytest.mark.parametrize(
    ("text", "cents"),
    [
        ("1.234,56", 123456),
        ("R$ 1.234,56", 123456),
        ("1234,5", 123450),
        ("1234.56", 123456),  # colado na planilha em inglês
        ("1.234", 123400),    # ponto como milhar
        ("12", 1200),
        ("0,01", 1),
        ("-12,30", -1230),
        (" 45,999 ", 4600),   # arrendonda meio para cima
    ],
)

def test_parse_brl(text, cents):
    assert parse_brl(text) == cents

@pytest.mark.parametrize("text", ["", "   ", "abc", "1,2,3"])
def test_parse_brl_rejects_garbage(text):
    with pytest.raises(ValueError):
        parse_brl(text)

def test_format_brl():
    assert format_brl(123456) == f"R${NBSP}1.234,56"
    assert format_brl(5) == f"R${NBSP}0,05"
    assert format_brl(-1230) == f"{MINUS}R${NBSP}12,30"
    assert format_brl(1230, sign=True) == f"+R${NBSP}12,30"

def test_round_trip():
    for cents in [0, 1, 99, 100, 123456, 987654321]:
        assert parse_brl(format_brl(cents)) == cents
        assert parse_brl(to_input_text(cents)) == cents

def test_format_compact():
    assert format_compact(85_000) == f"R${NBSP}850"
    assert format_compact(520_000) == f"R${NBSP}5,2 mil"