"""import modules"""
import subprocess
from datetime import datetime, timedelta
import os
import shutil
from typing import List, Optional


# Disable pylint warnings for too many arguments and too many instance attributes.
# This is simply the amount of arguments that crystal reports ninja takes.
class CrystalReport:  # pylint: disable=too-many-instance-attributes
    """Class to run Crystal Reports via python subprocesses using Crystal Reports Ninja.

    Attributes:
        report_file (str): The path to the report file (.rpt) to be executed. Only required param.
        output_filename (Optional[str]): The filename for the output file. If not provided,
            the report's output will default to "[report_file]-[yyyymmddHHmmss].[report_format]".
        report_format (Optional[str]): Intended file format to be exported.(i.e. pdf, doc, xls).
            If you wish to print Crystal Reports to a printer, simply "-E print" instead of
            specifying file format.
        printer_name (Optional[str]): Name of the printer where the report should be printed.
            Only relevant if printing the report directly.
        num_copies (Optional[int]): The number of copies to print. Relevant only if printing.
        server_name (Optional[str]): The database server for the report.
            Often, this will be included in the .rpt file.
        database_name (Optional[str]): The database name to use for the report. Again, often this
            will be included in the .rpt file.
        username (Optional[str]): The username for database access.
        password (Optional[str]): The password for database access.
        parameters (Optional[List[str]]): A list of parameters to pass to the report,
            formatted as 'name:value'.
        create_log (bool): Whether to create a log file. Defaults to False. Log will be placed in
            the same directory as the CrystalReportsNinja.exe file.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 report_file: str,
                 output_filename: Optional[str] = None,
                 report_format: Optional[str] = None,
                 printer_name: Optional[str] = None,
                 num_copies: Optional[str] = None,
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
        """Run the Crystal Report using Crystal Reports Ninja using the provided parameters."""
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
            if value is not None:
                command.extend([flag, value])
        if self.parameters:
            for param in self.parameters:
                command.extend(['-a', param])
        if self.create_log:
            command.append('-l')

        try:
            print(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command,
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print("Command executed successfully.")
            print(f"Output: {result.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Error output: {e.stderr.decode()}")

    @staticmethod
    def find_and_move_file(report_format: str,
                           time_tolerance: Optional[int] = 5,
                           file_destination: Optional[str] = "reports"):
        """Find files with the specified format and move them to
         the specified directory if they are within the time"""

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
                    os.makedirs(file_destination, exist_ok=True)
                    shutil.move(file_path, os.path.join(cwd, file_destination, file))
