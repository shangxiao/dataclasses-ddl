from datetime import date, datetime

import psycopg2
from dataclasses_ddl import (
    create_table,
    delete,
    insert,
    model_cursor_factory,
    select,
    update,
)

from .sample_classes import Company, Employee


def test_create():
    sql = create_table(Employee)
    assert sql == (
        'CREATE TABLE "employee" ('
        '"pk" SERIAL PRIMARY KEY, '
        '"company" INTEGER NOT NULL REFERENCES "company" ("pk"), '
        '"start_date" DATE NOT NULL, '
        '"last_login" TIMESTAMP NOT NULL, '
        '"name" VARCHAR, '
        '"num_days_leave" INTEGER NOT NULL DEFAULT 0, '
        "\"pay_grade\" VARCHAR NOT NULL DEFAULT 'JUNIOR' CHECK (\"pay_grade\" IN ('JUNIOR', 'INTERMEDIATE', 'SENIOR')), "
        '"remuneration" DECIMAL'
        ")"
    )


def test_insert():
    company = Company(name="ACME")
    company.pk = 1
    employee = Employee(company, date(2000, 1, 1), datetime(2019, 10, 1, 10))
    sql = insert(employee)
    assert (
        sql
        == """INSERT INTO "employee" ("company", "start_date", "last_login", "name", "num_days_leave", "pay_grade", "remuneration") VALUES (1, '2000-01-01'::date, '2019-10-01T10:00:00'::timestamp, NULL, 0, 'JUNIOR', NULL)"""
    )


def test_select():
    sql = select(Company, 1)
    assert sql == """SELECT "pk", "name" FROM "company" WHERE "pk" = 1"""


def test_update():
    company = Company(name="ACME")
    company.pk = 1
    sql = update(company, name="AJAX")
    assert sql == """UPDATE "company" SET "name" = 'AJAX'"""


def test_delete():
    company = Company(name="ACME")
    company.pk = 1
    sql = delete(company)
    assert sql == """DELETE FROM "company" WHERE "pk" = 1"""


def test_fetch_using_cursor_factory():
    with psycopg2.connect("dbname=dataclasses_orm") as conn:
        with conn.cursor(cursor_factory=model_cursor_factory(Company)) as cur:
            cur.execute("insert into company values (1, 'acme')")
            cur.execute("select * from company")

            result = cur.fetchone()

            assert isinstance(result, Company)
            assert result.pk == 1
            assert result.name == "acme"
            conn.rollback()


def test_fetch_using_cursor_factory_model_type_set_via_attribute():
    with psycopg2.connect("dbname=dataclasses_orm") as conn:
        with conn.cursor(cursor_factory=model_cursor_factory()) as cur:
            cur.execute("insert into company values (1, 'acme')")
            cur.model_type = Company
            cur.execute("select * from company")

            result = cur.fetchone()

            assert isinstance(result, Company)
            assert result.pk == 1
            assert result.name == "acme"
            conn.rollback()


def test_fetchall_using_cursor_factory():
    with psycopg2.connect("dbname=dataclasses_orm") as conn:
        with conn.cursor(cursor_factory=model_cursor_factory(Company)) as cur:
            cur.execute("insert into company values (1, 'acme'), (2, 'ajax')")
            cur.execute("select * from company")

            results = cur.fetchall()

            assert isinstance(results[0], Company)
            assert results[0].pk == 1
            assert results[0].name == "acme"
            assert isinstance(results[1], Company)
            assert results[1].pk == 2
            assert results[1].name == "ajax"
            conn.rollback()
