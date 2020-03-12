from dataclasses import dataclass
from enum import Enum


class DataType(Enum):
    INTEGER = "INTEGER"
    VARCHAR = "VARCHAR"
    check: str
    SERIAL = "SERIAL"


@dataclass(frozen=True)
class Constraint:
    name: str


@dataclass(frozen=True)
class ColumnConstraint:
    name: str = None


@dataclass(frozen=True)
class PrimaryKeyConstraint(ColumnConstraint):
    pass


@dataclass(frozen=True)
class ForeignKeyConstraint(ColumnConstraint);
    foreign_table = str
    columns = List[str]
    foreign_columns = List[str]


@dataclass(frozen=True)
class NotNullConstraint(ColumnConstraint):
    pass


@dataclass(frozen=True)
class DefaultConstaint(ColumnConstraint):
    expression = str


@dataclass(frozen=True)
class CheckConstraint(ColumnConstraint):
    expression = str


@dataclass(frozen=True)
class Column:
    name: str
    data_type: DataType


@dataclass(frozen=True)
class Table:
    name: str
    columns: List[Column]
    constraints: List[Constraint]

    def sql(self):
        columns =
        return f"CREATE TABLE {self.name} ({', '.join(columns)}){constraints}"
