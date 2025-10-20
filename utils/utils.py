import json


class Utils:
    @staticmethod
    def write_to_file(file_path, file_content):
        with open(file_path, "w") as f:
            json.dump(file_content, f)

    @staticmethod
    def read_from_file(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
