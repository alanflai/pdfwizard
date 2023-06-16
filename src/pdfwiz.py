# !/usr/bin/python

import fitz
import sys

from config import *
from pdfutils import *
import logging



###
# Main function
# usage
# > python pdfwiz.py <pdf_file_name>.pdf             ==> print out some pdf document's information
# > python pdfwiz.py <pdf_file_name>.pdf -annotatio  ==> extract annotation from the pdf documet
# > python pdfwiz.py <configuration_file.name>.json  ==> elaborate the input pdf file accordling 
#                                                        configuration into json file
###
def main(argv,argc):
   
    cmd = check_cli_inputs(argv,argc)
    msg = cmd["msg"]

    if cmd["data"] != None:
        input = cmd["data"]["input"]
    else:
        input = None

    match cmd["command"]:
        case "help":
            if msg != None:
                print(msg)
            help()

        case "meta":
            get_info(input)

        case "ann":
            get_annotations(input)

        case "add":

            print("The input file is the configuration file: %s" % input)

            # Read configuration file
            config_file = get_config(input)

            # Open the input file
            input_file = fitz.open(config_file["input_file"])
    
            # Loop over pages defined into the config file
            for page_item in config_file["pages"]:
                # Get the current page from the input file
                page = input_file[page_item["page_number"]-1]
                page_update(config_file, page_item, page)

            # Save output to file
            input_file.save(config_file["output_file"])

        case _:
            print("Error: wrong unkown situation")
    sys.exit()
    

#####################
# Application start #
#####################
if __name__ == "__main__":

    # Set loging level
    logging.basicConfig(level=logging.INFO)

    argv = sys.argv
    argc = len(sys.argv)-1
    main(argv,argc)
