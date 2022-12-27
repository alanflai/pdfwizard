# !/usr/bin/python

import fitz
import sys

from config import *
from pdfutils import *


###
# Main function
# usage
# > python pdfwiz.py <pdf_file_name>.pdf             ==> print out some pdf document's information
# > python pdfwiz.py <pdf_file_name>.pdf -annotatio  ==> extract annotation from the pdf documet
# > python pdfwiz.py <configuration_file.name>.json  ==> elaborate the input pdf file accordling 
#                                                        configuration into json file
###
def main(argv,argc):
   
    if check_cli_inputs(argv,argc) == False:
        exit()
    
    print("The input file is the configuration file: %s" % argv[1])

    # Read configuration file
    config_file = get_config(argv[1])

    # Open the input file
    input_file = fitz.open(config_file["input_file"])
    
    # Loop over pages defined into the config file
    for page_item in config_file["pages"]:
        # Get the current page from the input file
        page = input_file[page_item["page_number"]-1]
        page_update(config_file, page_item, page)

    # Save output to file
    input_file.save(config_file["output_file"])
       
###
# page_update
# - Input parameters:
#   config_file     : dictionary from config file reading
#   page_item       : current page dictionary from configuration
#   page            : object from reading current pdf page 
###
def page_update(config_file, page_item, page):

    # Page sizes: Width & Height in pixeld
    W = page.rect.width
    H = page.rect.height

    # Clear the pdf status
    page.clean_contents()

    print("--- Page # %d Updating ------------" % page_item["page_number"])

    # visited arrya
    visited = [False] * len(page_item["items"])
  
    # queue
    queue = []

    # Loop over page's items
    for id, item in enumerate(page_item["items"]):
        # There is a reference with an unvisited item
        if chek_ref(id, item["item_center_point"]):
            queue.append(id)
            print("[Add Queue] item id: %d - nome: %s" % (id,item["item_name"]))
            continue
        else:
            print("=== No reference Check id %d con item %s " %(id,item["item_name"]))
        try:
            item_update(item, config_file, page_item, page)
        except Exception as e:
            print(str(e))
       
    # queue's element elaboration         
    while queue:
        q_item = queue.pop(0)
        item = page_item["items"][q_item]
        print("[POP Queue] item id: %d - nome: %s" % (id,item["item_name"]))
        item_update(item, config_file, page_item, page)

#####################
# Application start #
#####################
if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)-1
    main(argv,argc)
