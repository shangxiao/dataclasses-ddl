from distutils.core import setup

setup(
    name="dataclasses-ddl",
    version="0.1.0",
    author_email="shang.xiao.sanders@gmail.com",
    packages=["dataclasses_ddl"],
    python_requires='>3.7.0',
    install_requires=['psycopg2'],
)
