from dataclasses_ddl import create_table, delete, insert, select, update

from .sample_classes import Company, Employee


def test_create():
    sql = create_table(Employee)
    assert sql == (
        'CREATE TABLE "employee" ('
        '"pk" SERIAL PRIMARY KEY, '
        '"company" INTEGER NOT NULL REFERENCES "company" ("pk"), '
        '"name" VARCHAR, '
        '"num_days_leave" INTEGER NOT NULL DEFAULT 0, '
        "\"pay_grade\" VARCHAR NOT NULL DEFAULT 'JUNIOR' CHECK (\"pay_grade\" IN ('JUNIOR', 'INTERMEDIATE', 'SENIOR')), "
        '"remuneration" DECIMAL'
        ")"
    )


def test_insert():
    company = Company(name="ACME")
    company.pk = 1
    employee = Employee(company)
    sql = insert(employee)
    assert (
        sql
        == """INSERT INTO "employee" ("company", "name", "num_days_leave", "pay_grade", "remuneration") VALUES (1, NULL, 0, 'JUNIOR', NULL)"""
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
