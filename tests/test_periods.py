from datetime import date

from planilhafinanceira.core.periods import Month, last_months

def test_shift_crosses_years():
    assert Month(2026, 1).shift(-1) == Month(2025, 12)
    assert Month(2026, 12).shift(1) == Month(2027, 1)
    assert Month(2026, 10).shift(-14) == Month(2025, 8)

def test_bounds():
    feb = Month(2028, 2) # ano bissexto
    assert feb.first_day == date(2028, 2, 1)
    assert feb.last_day == date(2028, 2, 29)
    assert feb.next_first_day == date(2028, 3, 1)
    assert feb.contains(date(2028, 2 ,29))
    assert not feb.contains(date(2028, 3, 1))

def test_labels_and_parse():
    m = Month.parse("2026-10")
    assert m.label == "outubro de 2026"
    assert m.short_label == "out"
    assert str(m) == "2026-10"

def test_last_months_oldest_first():
    assert last_months(Month(2026, 2), 3) == [Month(2025, 12), Month(2026, 1), Month(2026, 2)]