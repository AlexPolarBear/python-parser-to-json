import getopt
import glob
import os
import sys
import logging

logger = logging.getLogger('logger')
 
path_conf = sys.argv[1]
numb_conf = sys.argv[2]

# argv = sys.argv[1:]
# try:
#     options, args = getopt.getopt(argv, "p:n:",
#                                   ["path_conf = """, 
#                                    "numb_conf = """])
# except:
#     print("Error Message ")
 
# for name, value in options:
#     if name in ['-p', '--path']:
#         path_conf = value
#     elif name in ['-n', '--numb']:
#         numb_conf = value
 
# print(path_conf + " " + numb_conf)

# print(path_conf)
# print(numb_conf)
try:
    with open(path_conf, 'r') as f:
        file = f.read().split("\n")
        try:
            index = file.index(f"#{numb_conf}")
            mode = file[index+1].replace("#mode: ", "")
            path = file[index+2].replace("#path: ", "").split(", ")
        except ValueError as err:
            print(f"There are only {round(len(file)/4)} positions in the config.")
            logger.error(err.args[0])
except OSError as err:
    print("Make sure that the request is correct.")
    logger.error(err.args[1])

# for filename in glob.glob(os.path.join(path_conf, '*.*')):
#    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
#       # do your stuff
#       print(filename)
#       print(f.read())