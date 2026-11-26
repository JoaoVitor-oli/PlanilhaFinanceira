from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

MONTH_NAMES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
MONTH_SHORT = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
WEEKDAY_SHORT = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

@dataclass(frozen=True, order=True)
class Month:
    year: int
    month: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= 12:
            raise ValueError(f"Mês inválido: {self.month}")

    # --- construtores ---
    @classmethod
    def today(cls) -> Month:
        return cls.from_date(date.today())

    @classmethod
    def from_date(cls, d: date) -> Month:
        return cls(d.year, d.month)
    
    @classmethod
    def parse(cls, text: str) -> Month:
        year, month = text.split("-")
        return cls(int(year), int(month))

    # --- limites ---
    @property
    def first_day(self) -> date:
        return date(self.year, self.month, 1)

    @property
    def next_first_day(self) -> date:
        """Primeiro dia do mês seguinte (limite exclusivo nas consultas)."""
        return self.shift(1).first_day

    @property
    def last_day(self) -> date:
        return self.next_first_day - timedelta(days=1)
    
    def contains(self, d: date) -> bool:
        return self.first_day <= d < self.next_first_day

    # --- navegação ---
    def shift(self, months: int) -> Month:
        index = self.year * 12 + (self.month - 1) + months
        return Month(index // 12, index % 12 + 1)

    def is_current(self) -> bool:
        return self == Month.today()

    # --- texto ---
    @property
    def name(self) -> str:
        return MONTH_NAMES[self.month - 1]
    
    @property
    def label(self) -> str:
        return f"{self.name} de {self.year}"

    @property
    def short_label(self) -> str:
        return MONTH_SHORT[self.month - 1]

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}"

def last_months(end: Month, count: int) -> list[Month]:
    """Os `count` meses terminando em `end`, do mais antigo para o mais novo."""
    return [end.shift(-offset) for offset in range(count - 1, -1, -1)]

def format_long(d: date) -> str:
    weekday = WEEKDAY_SHORT[d.weekday()]
    return f"{weekday}, {d.day} de {MONTH_NAMES[d.month - 1]} de {d.year}"
    