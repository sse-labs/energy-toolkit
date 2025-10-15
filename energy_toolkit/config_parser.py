"""
Config_Parser component to deal with program definiton configs.
Offers methods for parsing and validating the config.
"""

import os
import yaml
import click


class ConfigParser:
    """Config parser class to parse and validate configurations of programs"""
    @staticmethod
    def parse(file: str) -> any:
        """Parse the given program definition file"""
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data
    @staticmethod
    def validate(data: any) -> int:
        """Validate the given parsed data"""

        if "programs" not in data:
            raise click.ClickException("Missing 'programs' key in datauration.")

        programs = data["programs"]

        # Check that 'programs' is a list
        if not isinstance(programs, list):
            raise click.ClickException("'programs' must be a list.")

        # Check that the list is not empty
        if len(programs) == 0:
            raise click.ClickException(
                "'programs' list must contain at least one entry."
            )

        # Validate each program
        for idx, program in enumerate(programs):
            if not isinstance(program, dict):
                raise click.ClickException(
                    f"Entry {idx} in 'programs' must be a dictionary."
                )

            # Check for 'executeable' key
            if "executeable" not in program:
                raise click.ClickException(f"Entry {idx} missing 'executeable' key.")

            exe_path = program["executeable"]
            if not isinstance(exe_path, str):
                raise click.ClickException(
                    f"'executeable' in entry {idx} must be a string."
                )

            # Check if the executable exists
            if not os.path.isfile(exe_path):
                raise click.ClickException(
                    f"Executable '{exe_path}' in entry {idx} does not exist."
                )

            # Optional: check 'args' and 'input'
            if "args" in program and not isinstance(program["args"], list):
                raise click.ClickException(f"'args' in entry {idx} must be a list.")
            if "input" in program and not isinstance(program["input"], str):
                raise click.ClickException(f"'input' in entry {idx} must be a string.")
