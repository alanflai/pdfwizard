### info how to get annotatios text from the pdf file from this web page
### https://github.com/pymupdf/PyMuPDF/issues/819

import fitz
import os
import logging
from pprint import pprint
import pdfutils as utils


### CONSTANT ###

PDF_FILE_PATH = ""
OUTPUT_FILE = "collected-comments.txt"
OUTPUT_PRESENTATION_PATH = ""
PNG_PAGE_FILE_TEMPLATE = "{path}\{prefix}-page-{page}-.png" 
IMG_LEFT = 200
IMG_TOP = 100
IMG_WIDTH = 600
IMG_HEIGTH = 600
PAR_TEXT_FONT = 10

INPUT_FILE = {
                "input1": {
                    "file_path": "C:\\ExtraJob\\Documents\\file1.pdf",
                    "out_path": ".\\Output\\File1-Report.ppt",
                    "csv_path": ".\\Output\\File1-Report.csv",
                    "tot_page": 160,
                    "title": "Annotazioni sezione tecnica documento file1",
                    "author": "",
                    "text_font_size": 28,
                    "page_size" : [1440, 1040]
                },
                "input2": {
                    "file_path": "C:\ExtraJob\Documents\File2.pdf",
                    "out_path": ".\Output\File2-Report.ppt",
                    "csv_path": ".\Output\File2-Report.csv",
                    "tot_page": 46,
                    "title": "Annotazioni documento File2",
                    "author": "",
                    "text_font_size": 16,
                    "page_size" : [1440, 1040]
                },
                "input3": {
                    "file_path": "C:\ExtraJob\Documents\File3.pdf",
                    "out_path": ".\Output\File3-Report.ppt",
                    "csv_path": ".\Output\File3-Report.csv",
                    "tot_page": 160,
                    "title": "Annotazioni sezione tecnica documento File3",
                    "author": "",
                    "text_font_size": 28,
                    "page_size" : [1440, 1040]
                },
}

####
# first_get_annotations()
####

def annotations_to_csv(file_path,ann_list):

    try:
        logging.info("Avvio creazione file CSV")
        textfile = open(file_path, "w", newline='')  

        textfile.write("Pagina, Annotazione, Impatto\n")

        for ann in ann_list:  # loop thru pages of current PDF
            #logging.info("annuncio: %s" % ann)
            page_number = ann["page"]
       
            for ann_item in ann["annotation"]:
                tmp = ann_item.replace("\n","_")
                sub_items = tmp.partition(";")
                textfile.write("%d\t %s \t %s\n" % (page_number, sub_items[0], sub_items[2])) 
                #logging.info("%d || %s || %s\n" % (page_number, sub_items[0], sub_items[2]))        
        textfile.close() 
    except Exception as e:
        logging.error("Errore produzione file CSV")


####
#   get_annotations()
#   -input params:
#    file_path  : string, pdf file path
#    start_page : integer, the starting page's number from which extract annotations
#    end_page   : integer, the starting page's number from which extract annotations
#   - output
#   annotation_vet  : vector of a dictionary containing one page's annotation 
####
def get_annotations(file_path,start_page, end_page):
    
    # First check whether input file is a pdf one
    if not file_path["file_path"].endswith(".pdf"):
        logging.error("[Error] Input file is not in pdf format!!!")
        return None
    try:
        doc = fitz.open(file_path["file_path"])
    except Exception as e:
       logging.error("[Error] Error with the input file (%s)!" % str(e))
       return None 

    # Output vector
    output = []
       
    for page in doc:  # loop through pages of current PDF
        page_annot = {
                        "page": "",
                        "image": "",
                        "annotation": [""]
                    }

        page_number = page.number + 1
        buffer = []
        n_annot = 0
            
        if page_number >= start_page and page_number <= end_page:
            
            for n,annot in enumerate(page.annots()):  
                # loop thru freetext annots types=[fitz.PDF_ANNOT_TEXT]
                text = annot.info["content"]  # extract the text
                if len(text) != 0:
                    n_annot = n_annot +1
                    buffer.append(str(text))                        
                else:
                    continue  
            if n_annot > 0:
                page_annot["page"] = page_number
                
                # Page sizes: Width & Height in pixeld
                file_path["page_size"]= [page.rect.width, page.rect.height]

                page_annot["annotation"] = buffer
                page_annot["image"] = PNG_PAGE_FILE_TEMPLATE.format(path=".\Output",
                                                                    prefix="tmp",
                                                                    page = page.number+1)
                output.append(page_annot)
                utils.page_to_png(doc,page.number,"tmp",".\Output")
    doc.close()
    
    return output

####
#  list_annotations()
####
def list_annotaions(ann_list):
    output = ""
    for i,item in enumerate(ann_list):
        output = output + "({index}) {ann}\n".format(index=i, ann=item)
    return output


####
# make_presentation()
#### 
def make_presentation(file_path,ann_list,title,author,font_size, page_size):
    # Creating powerpoint presentations using the python-pptx package

    from pptx import Presentation
    from pptx.util import Pt, Inches
    from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
    
    # Page ratio
    ratio = page_size[1]/page_size[0]
    logging.info("Page ratio (%d/%d): %f" % (page_size[1], page_size[0], ratio))

    # Create the Presentation object
    X = Presentation()
    X.slide_height = Pt(page_size[1])
    X.slide_width = Pt(page_size[0] * 1.5)

    # Create the presentation's front page
    layout = X.slide_layouts[0]
    first_slide = X.slides.add_slide(layout)
    first_slide.shapes.title.text = title 
    first_slide.placeholders[1].text = author
    X.save(file_path)
    
    # Set layout for the following slides
    second_layout = X.slide_layouts[5]

    # Creates following slides using annotations'list
    for item in ann_list:
        
        current_slide = X.slides.add_slide(second_layout)
        current_slide.shapes.title.text = "Note pagina #" + str(item["page"]) + " (#ann: " + str(len(item["annotation"])) + ")"
        
        # Add annotations'paragraf
        textbox = current_slide.shapes.add_textbox(Pt(page_size[0]), Pt(IMG_TOP),Pt(page_size[0]*0.5), Pt(page_size[1]*0.8)) 
        textframe = textbox.text_frame
        textframe.word_wrap = True
        textframe.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
        paragraph = textframe.add_paragraph()
        paragraph.text = list_annotaions(item["annotation"])
        paragraph.font.size = Pt(font_size)

        # Add image
        pic = current_slide.shapes.add_picture(item["image"], 
                                               Pt(10), 
                                               Pt(100), 
                                               Pt(page_size[0]*0.9),
                                               Pt(page_size[1]*0.9))

        pic.click_action.hyperlink.address = item["image"]
        X.save(file_path)


####
# Main
####

if __name__ == "__main__":
    # Setting level for logging tracing
    logging.basicConfig(level=logging.INFO)

    input_file = "input3"

    PDF_FILE_PATH = INPUT_FILE[input_file]["file_path"]
    OUTPUT_PRESENTATION_PATH = INPUT_FILE[input_file]["out_path"]
    title = INPUT_FILE[input_file]["title"]
    author = INPUT_FILE[input_file]["author"]
    font_size = INPUT_FILE[input_file]["text_font_size"]
   
    out = get_annotations(INPUT_FILE[input_file],1, 160)
    if out != None:
        #pprint(out)
        logging.info("page size %s" % str(INPUT_FILE[input_file]["page_size"]))
        logging.info("Avvio produzione report CSV")
        annotations_to_csv(INPUT_FILE[input_file]["csv_path"],out)
        logging.info("Avvio produzione PPT")
        make_presentation(OUTPUT_PRESENTATION_PATH, out, title, author, font_size,INPUT_FILE[input_file]["page_size"])


