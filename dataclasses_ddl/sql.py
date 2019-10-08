from collections.abc import Iterable
from dataclasses import _MISSING_TYPE, Field, fields, is_dataclass
from decimal import Decimal
from enum import Enum
from itertools import chain

from psycopg2.extensions import adapt

from .helpers import Serial

"""
Non goals (as of yet):
 - field & table naming

Assumptions we can make:
 - Supplying a default None determines the nullability

Questions:
 - We could just explicitly set DEFAULT NULL for default None?
 - What determines a model?
  - mixin?
  - market decorator?
  - presence of something that can be categorised as a pk?
  - or do we only need this for something that fk-able?  (how necessary is a pk?)
  - what protocol do we use for pks?  single field called "pk"?  composite?  determined in field type? create a class / custom type called PrimaryKey?
 - auto pks or just leave it manual for now?
 - what kind of philosophy regarding validation are we going to use?
 - how to deal with pks?  Add to constructor or not?
 - how to deal with updates?  mutate the object?
 - validation?  also how does this work with mypy?
 - should just rely on a migration tool like Sqitch for DDL operations??
 - skeema looks nice in that it diffs create statements - but just works for mysql?
 - migra?  https://github.com/djrobstep/migra


A mixin could serve a few purposes:
 - Type recognition
 - Add pk automatically (want?)


Todo:
 - use composable sql: http://initd.org/psycopg/docs/sql.html, but needs a connection for it to format to a string?
 - enums
 - composite keys
 - check constraints
 - deal with auto-generated values / computed values
"""

DB_TYPE_MAP = {
    str: "VARCHAR",
    int: "INTEGER",
    Enum: "VARCHAR",
    Serial: "SERIAL",
    Decimal: "DECIMAL",
}
CONSTRAINT_MAP = {
    "not_null": "NOT NULL",
    "default": "DEFAULT {}",
    "pk": "PRIMARY KEY",
    "fk": 'REFERENCES {} ("pk")',
    "enum": "CHECK ({} IN ({}))",
}


def is_fk(field: Field) -> bool:
    return is_dataclass(field.type) and "pk" in field.type.__dataclass_fields__


def quote(identifier):
    # fixme
    return f'"{identifier}"'


def quote_value(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, Enum):
        return str(adapt(value.value))
    # xxx
    if is_dataclass(value):
        return str(adapt(value.pk))
    return str(adapt(value))


def constraint_map(constraint, value):
    sql = CONSTRAINT_MAP[constraint]
    if "{}" in sql:
        if isinstance(value, Iterable) and not isinstance(value, str):
            return sql.format(*value)
        else:
            return sql.format(value)
    return sql


def get_field_type(field: Field) -> type:
    if issubclass(field.type, Enum):
        return Enum

    if is_fk(field):
        fk_type = field.type.__dataclass_fields__["pk"].type
        return int if fk_type is Serial else fk_type

    return field.type


def column(field: Field) -> str:
    name = quote(field.name)

    field_type = get_field_type(field)
    db_type = DB_TYPE_MAP[field_type]

    constraint_details = {
        "not_null": field.default is not None and field.name != "pk",
        "default": (
            quote_value(field.default)
            if field.default is not None and type(field.default) != _MISSING_TYPE
            else False
        ),
        "pk": field.name == "pk",
        "fk": quote(field.name) if is_fk(field) else False,
        "enum": (
            (quote(field.name), ", ".join(quote_value(value) for value in field.type))
            if issubclass(field.type, Enum)
            else False
        ),
    }
    constraints = (
        constraint_map(constraint, value)
        for constraint, value in constraint_details.items()
        if value
    )

    return " ".join(chain((name, db_type), constraints))


def create_table(model_class):
    table_name = quote(model_class.__name__.lower())
    columns = (column(field) for field in fields(model_class))
    constraints = ""

    return f"CREATE TABLE {table_name} ({', '.join(columns)}){constraints}"


def insert(model_instance):
    table_name = quote(model_instance.__class__.__name__.lower())
    # fixme
    auto_fields = ["pk"]
    insertable_fields = [
        field for field in fields(model_instance) if field.name not in auto_fields
    ]
    column_names = (quote(field.name) for field in insertable_fields)
    values = (
        quote_value(getattr(model_instance, field.name)) for field in insertable_fields
    )
    return f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(values)})"


def select(model_class, pk):
    columns = (quote(field.name) for field in fields(model_class))
    table_name = quote(model_class.__name__.lower())
    return f"SELECT {', '.join(columns)} FROM {table_name} WHERE \"pk\" = {quote_value(pk)}"


def update(model_instance, **new_values):
    # TODO: if not supply new_values, then set everything on the model?  (ie allow mutation?)
    table_name = quote(model_instance.__class__.__name__.lower())
    fields_to_update = (
        field.name for field in fields(model_instance) if field.name in new_values
    )
    if not fields_to_update:
        # fixme
        raise Exception()
    set_expressions = (
        f"{quote(field_name)} = {quote_value(new_values[field_name])}"
        for field_name in fields_to_update
    )
    return f"UPDATE {table_name} SET {', '.join(set_expressions)}"


def delete(model_instance):
    table_name = quote(model_instance.__class__.__name__.lower())
    pk_value = quote_value(model_instance.pk)
    return f'DELETE FROM {table_name} WHERE "pk" = {pk_value}'
