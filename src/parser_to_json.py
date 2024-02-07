import getopt
import glob
import os
import sys
import logging
import json
import datetime


class Parser():
    """
    A class used to parse configuration file 
    and save data to json file.
    """

    def __init__(self, path_conf, numb_conf = 1):
        self.path_conf = path_conf
        self.numb_conf = numb_conf

        self.data = {}
        self.mode = ""
        self.path = []

        self.data["configurationFile"] = self.path_conf
        self.data["configurationID"] = self.numb_conf

    def find_config(self) -> bool:
        """
        Returns True if mode and path to file(s) find successfully
        or False if there's an error occured.
        """
        
        try:
            with open(self.path_conf, "r") as f:
                file = f.read().split("\n")

                try:
                    index = file.index(f"#{self.numb_conf}")
                    self.mode = file[index+1].replace("#mode: ", "")
                    paths = file[index+2].replace("#path: ", "")
                    self.path = paths.split(", ")

                    new_data = {"mode": self.mode, "path": paths}
                    self.data["configuratioData"] = new_data

                    return True
                
                except ValueError as err:
                    logger.error(f"There are only {round(len(file)/4)} positions in the config.\n"
                                  + err.args[0])
                    return False
        
        except OSError as err:
            logger.error("Make sure that the request is correct.\n" + err.args[1])
            return False
        
    def choose_mode(self) -> None:
        if self.mode == "dir":
            filenames = glob.glob(self.path[0] + "/*")
            self.parse_files(filenames)
        else:
            self.parse_files(self.path)
        
    def parse_files(self, filenames: list[str]) -> None:

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
        self.save_json()

    def save_json(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        name = f"../data{date}.json"
        with open(name, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=3)
        json_path = os.path.abspath(name)
        print("Созданный файл находится по адресу: " + json_path)

if __name__ == "__main__":
    logger = logging.getLogger('logger')

    path = sys.argv[1]
    numb = int(sys.argv[2])

    parser = Parser(path, numb)
    ok = parser.find_config()
    if ok:
        parser.choose_mode()
