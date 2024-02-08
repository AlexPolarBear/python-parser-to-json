import sys
import json
import logging
from os import path
from enum import Enum
from glob import glob
from datetime import datetime


class Mode(Enum):
    dir = "dir"
    files = "files"


class Parser():
    """
    A class used to parse configuration file 
    and save data to json file.
    """

    def __init__(self, path_conf: str, numb_conf = 1):
        self.path_conf = path_conf
        self.numb_conf = numb_conf

        self.data = {}
        self.data["configurationFile"] = self.path_conf
        self.data["configurationID"] = self.numb_conf

        self.mode: Mode()
        self.path: list

        self.find_config()


    def find_config(self) -> None:
        """
        Init mode and path to file(s) if successfully
        or return exception if there's an error occured.
        """
        
        try:
            with open(self.path_conf, "r") as f:
                file = f.read().split("\n")

                index = file.index(f"#{self.numb_conf}")
                self.mode = Mode[file[index+1].replace("#mode: ", "")]
                paths = file[index+2].replace("#path: ", "")
                self.path = paths.split(", ")

                new_data = {"mode": self.mode.value, "path": paths}
                self.data["configuratioData"] = new_data
                
        except ValueError as err:
            logger.error(f"There are only {round(len(file)/4)} positions in the config.\n"
                         + err.args[0])
        
        except OSError as err:
            logger.error("Make sure that the request is correct.\n" + err.args[1])
        
    def parse_files(self) -> None:
        """
        Parse file(s) and saves the data in the json format.
        """

        if self.mode == Mode.dir:
            filenames = glob(self.path[0] + "/*")
        else:
            filenames = self.path
        
        filenames.sort()
        output_data = {}
        for i, file in enumerate(filenames):
            with open(file, "r") as f:
                lines = f.readlines()
                for j, line in enumerate(lines):
                    if str(j+1) not in output_data:
                        output_data[str(j+1)] = {}
                    output_data[str(j+1)][str(i+1)] = line.strip()
        
        max_lines = max(map(int, output_data.keys()))
        for line_num in range(1, max_lines+1):
            for file_num in range(1, len(filenames)+1):
                if str(file_num) not in output_data.get(str(line_num), {}):
                    output_data[str(line_num)][str(file_num)] = ""
        
        sorted_data = {key: dict(sorted(value.items())) for key,
                       value in sorted(output_data.items(),key=lambda x: int(x[0]))}
        self.data["out"] = sorted_data

    def save_json(self):
        """
        Create and save json file.
        """

        date = datetime.now().strftime('%Y-%m-%d_%H-%M')
        name = f"../data{date}.json"
        with open(name, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=3)
        json_path = path.abspath(name)
        print("Созданный файл находится по адресу: " + json_path)


if __name__ == "__main__":
    logger = logging.getLogger('logger')

    path_conf = sys.argv[1]
    numb_conf = int(sys.argv[2])

    parser = Parser(path_conf, numb_conf)
    parser.parse_files()
    parser.save_json()
