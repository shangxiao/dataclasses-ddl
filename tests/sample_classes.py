from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto

from dataclasses_ddl import Serial


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class PayGrade(AutoName):
    JUNIOR = auto()
    INTERMEDIATE = auto()
    SENIOR = auto()


@dataclass
class Company:
    pk: Serial = field(
        init=False, default=None
    )  # specify both init=False and default=None so we don't get an attribute error
    name: str


@dataclass
class Employee:
    pk: Serial = field(init=False, default=None)
    company: Company
    name: str = None
    num_days_leave: int = 0
    pay_grade: PayGrade = PayGrade.JUNIOR
    remuneration: Decimal = None
