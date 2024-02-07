import getopt
import glob
import os
import sys
import logging
import json
# from dataclasses import dataclass, asdict


# @dataclass
# class InventoryItem:
#     configFile: str
#     configurationID: float
#     configuratioData: int = 0



class Parser():
    """
    A class used to parse configuration file 
    and save data to json file.
    """

    def __init__(self, path_conf, numb_conf = 1, data = {}):
        self.path_conf = path_conf
        self.numb_conf = numb_conf
        self.data = data

        self.data["configurationFile"] = self.path_conf
        self.data["configurationID"] = self.numb_conf

    def find_config(self) -> (tuple[str, list[str]] | None):
        """
        Returns mode and path to file(s) or None
        if there's an error occured.
        """
        
        try:
            with open(self.path_conf, 'r') as f:
                file = f.read().split("\n")
                
                try:
                    index = file.index(f"#{self.numb_conf}")
                    mode = file[index+1].replace("#mode: ", "")
                    path = file[index+2].replace("#path: ", "").split(", ")

                    new_data = {"mode": mode, "path": path}
                    self.data["configuratioData"] = new_data

                    return mode, path
                
                except ValueError as err:
                    print(f"There are only {round(len(file)/4)} positions in the config.")
                    return logger.error(err.args[0])
        
        except OSError as err:
            print("Make sure that the request is correct.")
            return logger.error(err.args[1])

    def parse_file(self):
        print(json.dumps(self.data))

    def save_json(self):
        print("implement me")

# for filename in glob.glob(os.path.join(path_conf, '*.*')):
#    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
#       # do your stuff
#       print(filename)
#       print(f.read())


if __name__ == "__main__":
    logger = logging.getLogger('logger')

    path = sys.argv[1]
    numb = int(sys.argv[2])

    parser = Parser(path, numb)

    try:
        mode, path = parser.find_config()
        parser.parse_file()
    except TypeError as err:
        print(err)
