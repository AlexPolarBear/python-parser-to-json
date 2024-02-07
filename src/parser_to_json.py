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

    def parse_file(self) -> None:
        i = 1
        outuput_data = {}
        for file in self.path:
            with open(file, "r") as f:
                inside = f.read().split("\n")
                inside_data = {}
                ii = 1
                for one in inside:
                    inside_data[ii] = one
                    ii += 1
            outuput_data[i] = inside_data
            i += 1
        print(outuput_data)
        # print(json.dumps(self.data))
        self.data["out"] = outuput_data
        self.save_json()

    def save_json(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        with open(f"../data{date}.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=3)


if __name__ == "__main__":
    logger = logging.getLogger('logger')

    path = sys.argv[1]
    numb = int(sys.argv[2])

    parser = Parser(path, numb)
    ok = parser.find_config()
    if ok:
        parser.parse_file()
