import os
from report_generation import find_and_move_file

# This is company specific test data and the report used is not included.

report_file = 'test_report.rpt'
username = os.getenv('JOBBOSS_UID')
password = os.getenv('JOBBOSS_PWD')
report_format = 'pdf'
parameters = [
    'Department: Mill',
    'Date: 2/6/2024'
]

find_and_move_file(report_file, username, password, report_format, parameters)
