"""The utils.py class."""

import json


class Utils:
    """Represent a Utils."""

    @staticmethod
    def write_to_file(file_path, file_content):
        """Write to file."""
        with open(file_path, "w") as f:
            json.dump(file_content, f)

    @staticmethod
    def read_from_file(file_path):
        """Read from file."""
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def print_dict_table(data, title="My Table"):
        """Print title."""
        print(f"\n{title}")

        """Calculate column width."""
        key_width = max(len(str(k)) for k in data.keys())
        val_width = max(len(str(v)) for v in data.values())

        """Print column names."""
        print(f"{'Key'.ljust(key_width)} | {'Value'.ljust(val_width)}")
        print("-" * (key_width + val_width + 3))

        """Print data."""
        for key, value in data.items():
            print(f"{str(key).ljust(key_width)} | {str(value).ljust(val_width)}\n")
