import os
from crystal_report import CrystalReport

# This is company specific test data and the report used is not included.

report_file = 'test_report.rpt'
username = os.getenv('JOBBOSS_UID')
password = os.getenv('JOBBOSS_PWD')
report_format = 'pdf'
parameters = [
    'Department: Mill',
    'Date: 2/6/2024'
]


print(CrystalReport('test_report.rpt',
                    username=username,
                    password=password,
                    report_format=report_format,
                    parameters=parameters
                    ).run_crystal_report())

CrystalReport.find_and_move_file(report_format)
