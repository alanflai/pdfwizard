# !/usr/bin/python

import fitz
import re

###
# Draw axes guides
###
def draw_axes_guides(page, W, H):
   # Draw a vertical line in the middle of the page
   page.draw_line((W/2,0), (W/2,H), color = (1,0,0), width=2, dashes="[4 3] 0")
   # Draw an horizontal line in the middle of the page
   page.draw_line((0,H/2), (W,H/2), color = (1,0,0), width=2, dashes="[4 3] 0")
   # Draw line in the upper left quarter
   page.draw_line((W/4,0), (W/4,H/2), color = (0,0,1), width=1, dashes="[4 3] 0")
   page.draw_line((0,H/4), (W/2,H/4), color = (0,0,1), width=1, dashes="[4 3] 0")
   # Draw lines eigth quadrant 
   page.draw_line((3*W/4,0), (3*W/4,H/2), color = (0,1,0), width=1, dashes="[4 3] 0")
   page.draw_line((W/2,H/4), (W,H/4), color = (0,1,0), width=1, dashes="[4 3] 0")
   page.draw_line((5*W/8,0), (5*W/8,H/4), color = (0,0,0), width=1, dashes="[4 3] 0")
   page.draw_line((W/2,H/8), (3*W/4,H/8), color = (0,0,0), width=1, dashes="[4 3] 0")

   # Draw x-axe trhough Gilbratrar Logo
   page.draw_line((0,75), (W,75), color = (0,1,0), width=1, dashes="[4 3] 0")
   page.draw_line((654,55), (W-20,55), color = (0,1,1), width=1, dashes="[4 3] 0")

###
# Insert image centered a given point and x-axes
###
def put_centered_image(page,image,point,width):
    
    height = width * image["aspect_ratio"]
    
    # Debug
    #print("Image W: %s" % width)
    #print("Image H: %s" % height)

    anchor_point = (point[0]-width/2,point[1])
    
    image_rectangle = fitz.Rect(anchor_point[0],anchor_point[1],
                             anchor_point[0] + width,
                             anchor_point[1] + height)
   

    # add the image
    page.insert_image(image_rectangle, filename=image["filename"])

    return height

# Write centered array of texts
def write_centered_texts(page, array_txt, centered_pos, font_size, font_type, inter_text, space_after):
   
    x_pos = centered_pos[0]
    y_pos = 0
   
    for text in array_txt:
        if y_pos == 0:
            y_pos = centered_pos[1]
        else:
            y_pos = y_pos + font_size + inter_text
        writext(page,text,(x_pos,y_pos),font_size, font_type)

    return y_pos + space_after


# writext: write some text into pdf
def writext(page,text,point,font_size, font_type):
    
    fontsize_to_use = font_size
    fontname_to_use = font_type #"Helvetica-Bold" #"Times-Bold"
    text_lenght = fitz.get_text_length(text, 
                                 fontname=fontname_to_use,
                                 fontsize=fontsize_to_use)

    rect_x1 = point[0]-text_lenght/2
    rect_y1 = point[1]
    rect_x2 = rect_x1 + text_lenght + 2  # needs marg
    rect_y2 = rect_y1 + fontsize_to_use + 2  # needs 

    rect = (rect_x1, rect_y1, rect_x2, rect_y2)

    rc = page.insert_textbox(rect, text,
                        fontsize=fontsize_to_use,
                        fontname=fontname_to_use,
                        align=1)

###
# export page to png
###
def export_page(input_file,prefix, page_number):
    # Open the pdf file
    doc = fitz.open(input_file)
    page = doc.load_page(int(page_number))  
    pix = page.get_pixmap()
  
    #m = fitz.Matrix(1, 1)
    #pix = page.get_pixmap(matrix=m,dpi=92)
    pix = page.get_pixmap()
    pix.save("%s-page-%d-.png" % (prefix, int(page_number)))
    doc.close()

###
# page_to_png
# -input params:
# obj_pdf_file  : object pdf file read
# page_number   : inter, page's number to export
# prefix        : string, the prefix to add to png file
# out_path      : string, output path
###
def page_to_png(obj_pdf_file, page_number, prefix, out_path):
    # Open the pdf file
    doc = obj_pdf_file
    page = doc.load_page(int(page_number))  
    pix = page.get_pixmap()

    pix = page.get_pixmap()
    pix.save("%s//%s-page-%d-.png" % (out_path,prefix, int(page_number+1)))

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
# Save page to svg file
###
def svg2file(filename, value):
    #open text file
    svg_file = open(filename, "w")
 
    #write string to file
    n = svg_file.write(value)
 
    #close file
    svg_file.close()
 
    print(n)
    return n

####
#  eval_coord
#  - input params:
#    W          : integer, current pdf page's width
#    H          : integer, current pdf page's height
#    item       : dictionary containing coordinates
#    input_str  : inputt string containing algebric expression with item's coordinates
#  - output:
#    value      : integer, parsed input string value or an Exception if there are input file
#                 syntax errors  
####
def eval_coord(H,W,item, input_str):
    # patterns string
    pattern = "item_id=[0-9]*.[H, W]"
    index_pattern = "[0-9]+"
    dim_pattern = "[H,W]{1,1}"

    # Find all item object's reference, we expect only one
    output = re.findall(pattern,input_str)

    # Elaborate single or multiple item references into algebric expression string
    for var in output:
        
        #get index
        index = int(re.findall(index_pattern, var)[0])
    
        # get dimension variable
        dim = re.findall(dim_pattern,var)[0] # H or W dimension variable name

        try:        
            if dim != None:
                input_str = input_str.replace(var,str(item[index][dim]))
        except Exception as e:
            raise Exception("(err) value not already assigned (%s)" % str(e))

    if isinstance(input_str,str):
        try:
            output = eval(input_str)
        except:
            raise Exception("Error, coordinate expression wrong in config file!!!")
        return(output)
    else:
        return(input_str)

###
#  config_find_image
#  - input parameters:
#    config_file    : dictionary from config file reading
#    img_name       : string of the image's name
#
#   - output:
#     img           : image dictionary of the founded image or None if not found
###

def cofig_find_image(config_file, img_name):
    ref_img = ""
    for img in config_file["images"]:
        if img["image_name"] == img_name:
            return(img)
    return(None)

###
#  last_page_tot_img
###
def last_page_tot_img(config):
    tot_pages = len(config["pages"])
    print("Numero totale pagine: %d" % tot_pages)
    
    items_last_page = config["pages"][tot_pages-1]["items"]
    tot_images = 0

    for item in items_last_page:
        if item["item_type"] == "image":
            tot_images = tot_images +1
    print("Numero totale immagini nell'ultima pagina: %d" % tot_images)


####
#  eval_coord
#  - input params:
#    id_loop    : corrispondent itemid loop
#    array_coord: array string containing algebric expression with item's coordinates
#  - output:
#    True/False : True if there is a reference dipendece with others items  
####
def chek_ref(id_loop, array_coord):
    # patterns string
    pattern = "item_id=[0-9]*.[H, W]"
    index_pattern = "[0-9]+"
    
    # Loop on the x and y coordinates
    for input_str in array_coord:
        # Find all item object's reference
        if isinstance(input_str,str):
            output = re.findall(pattern,input_str)
            print("=== Check Id vs Index: %d - No item reference" % (id_loop))
        else:
            continue

        # Check if there is a reference with another item non just visited
        for var in output:
            #get index
            index = int(re.findall(index_pattern, var)[0])
            print("=== Check Id vs Index: %d - %d" % (id_loop, index))
            if(index > id_loop):
                return(True)

    return(False)

####
# item_update
# - Input parameters:
#   item            : current item information from configuration
#   config_file     : dictionary from config file reading
#   page_item       : current page dictionary from configuration
#   page            : object from reading current pdf page 
####
def item_update(item, config_file, page_item, page):

    # Page sizes: Width & Height in pixeld
    W = page.rect.width
    H = page.rect.height

    # Image items management
    if item["item_type"] == "image":
        ref_img = cofig_find_image(config_file, item["item_name"])
        if ref_img == None:
            raise Exception("(err) image reference not find into config file (%s)" % item["item_name"])

        print("(item %d) IMAGE item_center_point: %s, %s" % (item["item_id"], item["item_center_point"][0], 
                                                item["item_center_point"][1]))
        x = item["item_center_point"][0]
        y = item["item_center_point"][1]
        w = item["item_width"]

        try:
            if isinstance(x,str):
                x = eval_coord(H,W,page_item["items"], x)
                print("x: %d" % x)
            if isinstance(y,str):
                y = eval_coord(H,W,page_item["items"], y)
                print("y: %d" % y)
            if isinstance(w,str):
                w = eval(w)
                #print("w: %d" % w)
            
            item["H"] = put_centered_image(page,ref_img,(x,y),w)
            print("Altezza dell'item %s: %d" % (item["item_name"], item["H"]))
               
        except Exception as e:
            print("Error: %s" % str(e))  

    # Text items management   
    elif item["item_type"] == "text":
        print("(item %d) TEXT item_center_point: %s, %s" % (item["item_id"], item["item_center_point"][0], 
                item["item_center_point"][1]))
            
        x = item["item_center_point"][0]
        y = item["item_center_point"][1]

        try:
            if isinstance(x,str):
                x = eval_coord(H,W,page_item["items"], x)
                print("x: %d" % x)
            if isinstance(y,str):
                y = eval_coord(H,W,page_item["items"], y)
                print("y: %d" % y)

            item["H"] = write_centered_texts(page, 
                                             item["text"]["value"],
                                             (x, y),
                                             int(item["text"]["font_size"]), 
                                             item["text"]["font_name"],
                                             int(item["text"]["inter_text"]), 
                                             int(item["text"]["space_after"]))
            print("Altezza dell'item %s: %d" % (item["item_name"], item["H"]))
            
        except Exception as e:
            print("Error: %s" % str(e))

       
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

    # visited array
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