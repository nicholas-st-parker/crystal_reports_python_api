import subprocess
from datetime import datetime, timedelta
import os
import shutil
from typing import List, Optional


class CrystalReport:
    def __init__(self,
                 report_file: str,
                 output_filename: Optional[str] = None,
                 report_format: Optional[str] = None,
                 printer_name: Optional[str] = None,
                 num_copies: Optional[int] = None,
                 server_name: Optional[str] = None,
                 database_name: Optional[str] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 parameters: Optional[List[str]] = None,
                 create_log: Optional[bool] = False) -> None:
        self.report_file = report_file
        self.output_filename = output_filename
        self.report_format = report_format
        self.printer_name = printer_name
        self.num_copies = num_copies
        self.server_name = server_name
        self.database_name = database_name
        self.username = username
        self.password = password
        self.parameters = parameters if parameters else []
        self.create_log = create_log

    def run_crystal_report(self):
        command = [
            r'.\CrystalReportsNinja\bin\CrystalReportsNinja.exe',
            '-F', self.report_file,
        ]
        optional_params = {
            '-O': self.output_filename,
            '-E': self.report_format,
            '-N': self.printer_name,
            '-C': self.num_copies,
            '-S': self.server_name,
            '-D': self.database_name,
            '-U': self.username,
            '-P': self.password,
        }
        for flag, value in optional_params.items():
            if value:
                command.extend([flag, value])
        if self.parameters:
            for param in self.parameters:
                command.extend(['-a', param])
        if self.create_log:
            command.append('-l')

        try:
            print(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Command executed successfully.")
            print(f"Output: {result.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Error output: {e.stderr.decode()}")

    @staticmethod
    def find_and_move_file(report_format: str,
                           time_tolerance: Optional[int] = 5,
                           file_destination: Optional[str] = "reports"):

        def within_time_tolerance(_file_path: str) -> bool:
            now = datetime.now()
            time_tolerance_negative = (now - timedelta(minutes=time_tolerance)).timestamp()
            time_tolerance_positive = (now + timedelta(minutes=time_tolerance)).timestamp()
            return time_tolerance_negative < os.path.getmtime(file_path) < time_tolerance_positive

        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.endswith(report_format):
                file_path = os.path.join(cwd, file)
                if within_time_tolerance(file_path):
                    shutil.move(file_path, os.path.join(cwd, file_destination, file))
