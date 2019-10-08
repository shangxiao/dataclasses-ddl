import pytest
from psycopg2 import connect

from .sample_classes import Company, Employee


@pytest.fixture
def cursor():
    connection = connect(dbname="project_x", user="davidsanders")
    cursor = connection.cursor()
    yield cursor
    connection.rollback()


def test_create(cursor):
    company_sql = create_table(Company)
    cursor.execute(company_sql)
    employee_sql = create_table(Employee)
    cursor.execute(employee_sql)


@pytest.mark.skip
def test_insert_with_db(cursor):
    company = Company(name="ACME")
    company.pk = 1
    employee = Employee(company)
    sql = insert(employee)
    cursor.execute(sql)


@pytest.mark.skip
def test_get_with_db(cursor):
    cursor.execute(create_table(Company))
    cursor.execute("INSERT INTO company (pk, name) VALUES (1, 'acme')")
    fetch_sql = fetch(Company, 1)
    cursor.execute(fetch_sql)
    result = cursor.fetchone()


    assert company.pk == 1
    assert company.name == "acme"
