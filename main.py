import subprocess
from datetime import datetime, timedelta
import os
import shutil

report_file = 'test_report.rpt'
username = os.getenv('JOBBOSS_UID')
password = os.getenv('JOBBOSS_PWD')
report_format = 'pdf'
parameters = [
    'Department: Mill',
    'Date: 2/6/2024'
]


def run_crystal_report(_report_file, _username, _password, _report_format, _parameters):
    command = [
        r'.\CrystalReportsNinja.exe',  # Path to the executable
        '-F', report_file,  # Report file
        '-U', username,  # Username
        '-P', password,  # Password
        '-E', report_format  # Export format
    ]
    for param in parameters:
        command.append('-a')
        command.append(param)

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully.")
        print(f"Output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr.decode()}")


def within_time_tolerance(_file_path):
    now = datetime.now()
    time_tolerance_negative = (now - timedelta(minutes=5)).timestamp()
    time_tolerance_positive = (now + timedelta(minutes=5)).timestamp()
    return time_tolerance_negative < os.path.getmtime(_file_path) < time_tolerance_positive


def find_and_move_file(_report_file, _username, _password, _report_format, _parameters):
    run_crystal_report(_report_file, _username, _password, _report_format, _parameters)
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(_report_format):
            file_path = os.path.join(cwd, file)
            if within_time_tolerance(file_path):
                shutil.move(file_path, os.path.join(cwd, "reports", file))


find_and_move_file(report_file, username, password, report_format, parameters)
