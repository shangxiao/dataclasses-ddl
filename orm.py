#!/usr/bin/env python

from dataclasses_orm.sql import *
from tests.sample_classes import *

print(f'{create_table(Company)};')
print(f'{create_table(Employee)};')
