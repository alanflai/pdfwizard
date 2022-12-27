import json
from pathlib import Path
import fitz
import os


INPUT_FILE = "config-ICE.json" #"config-SHI.json"
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
            "pdfadd help",
            "> python pdfadd.py filename",
            "If filename is the pdf file, all the pdf file information will be printed as output",
            "If file name is the expected json file configuration, the pdf file will be elaborated accordigly to it"
         ]
    for row in text:
        print(row)

###
# check_cli_inputs()
# Check if the cli inputs are ok and manage the less important functionalities
###

def check_cli_inputs(argv,argc):
    if argc == 0:
        help()
        return False

    if argc > 2 :
        print("Error: wrong number of input parmeters")
        help()
        return False

    if argc == 2:
        if argv[1].endswith(".pdf") == True and argv[2] == "-annotations":
            print("Get annotations and write to file: %s" % (argv[1] + ".txt"))
            get_annotations(argv[1])
            return False

    if Path(argv[1]).exists() == False:  
        print("Input file does not exist")
        help()
        return False
        
    if argv[1].endswith((".pdf", ".json")) == False:
         print("Error: the input file format is not correct!!!")
         help()
         return False
    
    if argv[1].endswith(".pdf"):
       get_info(argv[1])
       return False

    return True

###
# Get info from input file
###
def get_info(input_file):
    
    # Open the pdf file
    doc = fitz.open(input_file)  
    page = doc.load_page(0)
    tot_pages = doc.page_count

    print("-----------------------")
    print("Numero pagine del documento: %d" % tot_pages)
    print("-----------------------")
    print("Larghezza pixels pagine: %s " % page.rect.width)
    print("Altezza pixels pagine: %s " % page.rect.height)
    #print("Larghezza pixels pagine: %s " % page.mediabox.width)
    #print("Altezza pixels pagine: %s " % page.mediabox.height)
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
    print("path_fle: %s" % path_file)
    textfile = open(path_file + ".txt", "w")  # a simple text output for the extracted comments
    filename= path_file
    if not filename.endswith(".pdf"):
        print("Il file non è un pdf!!!")
        return False
    doc = fitz.open(filename)
   
    textfile.write("Comments in PDF '%s'.\n" % doc.name)
    for page in doc:  # loop thru pages of current PDF
        output = ""
        n_annot = 0
        for n,annot in enumerate(page.annots(
        )):  # loop thru freetext annots types=[fitz.PDF_ANNOT_TEXT]
            n_annot = n
            text = annot.info["content"]  # extract the text
            output = output + "\n--- Nota #" + str(n+1) + " " + "-" * 10 + "\n" + str(text)
            output = output + "\n" + "-" * 22 + "\n"  # write delimiter
       
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
