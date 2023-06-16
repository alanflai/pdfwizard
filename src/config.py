import json
from pathlib import Path
import fitz
import logging



INPUT_FILE = "input/config-1.json"
APP_NAME = "pdfwiz"

###
# get_config
# - input
#   configfile, string for the configution file path
# - output
#   object dictionary containing all configuration's info
###
def get_config(configfile):
  with open(configfile, 'r') as f:
    data = json.load(f)
  return data

###
# Help function
###
def help():
    text=[
            "Help of " + APP_NAME,
            "> python " + APP_NAME + ".py <filename>",
            "\tIf <filename> is a pdf file, the application prints to the scrreen\n\tall its META informations",
            "\tIf <filename> is a json file this is the configuration file for adding\n\timages and texts to a pdf file referenced by the configuration",
            "> python " + APP_NAME + ".py <filename>.pdf -annotation",
            "\tThis is the command to request the retrieval of all annotations from the \n\tpdf input file"
         ]
    for row in text:
        print(row)

###
# check_cli_inputs()
# Check if the cli inputs are ok and manage the less important functionalities
# - Input:
#       argv: array of command line input params
#       argc: integer, number of command line input params
# - Output:
#       cmd_obj: dictionary with this structure
#                   {
#                       "command": "help|meta|add|ann",
#                       "msg"    : "a message to print out",
#                       "data"   : { depending by the command }
#                   } 
###
def check_cli_inputs(argv,argc):

    match argc:
    
        case 0:
            # No input params, then print the help menu
            #help()
            cmd_obj = { 
                    "command": "help",
                    "msg": None,
                    "data": None
                }
            return cmd_obj

        case 1:
            # Manage error: type of input file (first param) i not supported
            if argv[1].endswith((".pdf", ".json")) == False:
                cmd_obj = { 
                        "command": "help",
                        "msg": "Error: the input file format is not supported!!!",
                        "data": None
                }
            # Manage error: input file (first param) doesn't exist
            elif Path(argv[1]).exists() == False:  
                cmd_obj = { 
                        "command": "help",
                        "msg": "Error: Input file does not exist",
                        "data": None
                }
            # Get meta information from input pdf file
            elif argv[1].endswith(".pdf"):
                # Check if the input file exists
                if Path(argv[1]).exists() == True:
                    cmd_obj = { 
                            "command": "meta",
                            "msg": None,
                            "data": {
                                "input": argv[1],
                            }
                        }
                else:
                    cmd_obj = { 
                            "command": "help",
                            "msg": "Error: inpu file " + argv[1] + "doesn't exist",
                        }
            # Add images and/or texts
            elif argv[1].endswith(".json"):
                cmd_obj = { 
                        "command": "add",
                        "msg": "Add images and/or texts to file: " + argv[1],
                        "data": {
                                    "input": argv[1],
                            }
                }
        
        case 2:
            # Annotation output to external file argv[1].txt
            if argv[1].endswith(".pdf") == True and argv[2] == "-annotations":
                cmd_obj = { 
                        "command": "ann",
                        "msg": "Get annotations and write to file: " + argv[1] + ".txt",
                        "data": {
                                    "input": argv[1],
                                    "output": argv[1] + ".txt"
                        }
                    }
                logging.debug("2 params PDF file and -annotations param")
                logging.debug(cmd_obj)

            else:
                cmd_obj = { 
                        "command": "help",
                        "msg": "Error: 2 params combination not supported",
                        "data": None
                    }
        case _:
            # Too many command line input params
            cmd_obj = { 
                    "command": "help",
                    "msg": "Error: wrong number of input parmeters",
                    "data": None
            }

    return cmd_obj

###
# Get info from input file
###
def get_info(input_file):
    
    # Open the pdf file
    doc = fitz.open(input_file)  
    page = doc.load_page(0)
    tot_pages = doc.page_count

    print("-----------------------")
    print("Number of pages in the document: %d" % tot_pages)
    print("-----------------------")
    print("Width in pixels of the page: %s " % page.rect.width)
    print("Height in pixels of the page: %s " % page.rect.height)
    print("-----------------------")
    
    metadata = doc.metadata
    print("File metadata:")
    
    for val in metadata:
        print("%s = %s" % (val, metadata[val]))

###
#  get_annotations
#  - Input
#    - path_file: string containing the pdf's full path
#  - Output:
#    - result: boolean, True if there aen any problem. Otherwise False
###
def get_annotations(path_file):
    logging.debug("path_fle: %s" % path_file)
    textfile = open(path_file + ".txt", "w")  # a simple text output for the extracted comments
    filename= path_file
    if not filename.endswith(".pdf"):
        logging.error("Il file non è un pdf!!!")
        return False
    doc = fitz.open(filename)
   
    textfile.write("Comments in PDF '%s'.\n" % doc.name)
    for page in doc:  # loop thru pages of current PDF
        output = ""
        n_annot = 0
        for n,annot in enumerate(page.annots()):  # loop thru freetext annots types=[fitz.PDF_ANNOT_TEXT]
            n_annot = n + 1
            text = annot.info["content"]  # extract the text
            output = output + "\n--- Nota #" + str(n+1) + " " + "-" * 10 + "\n" + str(text) + "\n"
       
        if n_annot > 0:
            textfile.write("Comments on page %s:\n" % str(page.number+1))
            textfile.write(output)
            textfile.write("=" * 20 + "\n")  # write end-of-page delimiter
    doc.close()
    textfile.close()
    return True


###
# Main to tes get_config function
###
if __name__ == "__main__":
  data = get_config(INPUT_FILE)
  print(data)
