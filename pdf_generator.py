from reportlab.pdfgen import canvas
import json

def place_doc_title(c, content, design):
    """places the title at the location defined in design.json
    Args:
        c (canvas): canvas object from reportlab
        content (dict): Content of the style sheet from the content json-file
        design (dict): design and layout of the cheatsheet from the desgin json-file
    """
    x = design["doc title"]["x"]
    y = design["doc title"]["y"]
    size = design["doc title"]["size"]
    doc_title = content["document setup"]["doc title"]
    c.setFont("Helvetica-Bold", size)
    c.drawString(x,y,doc_title)

def gen_file_name(content):
    """Generates the name of the PDF-file from the "doc title" in the json file.
    Args:
        content (dict): content from the json file
    Returns:
        string: file_name of the pdf-file
    """
    doc_name = content["document setup"]["doc title"]
    file_name = doc_name+".pdf"
    return file_name

if __name__ == "__main__":
    with open("example.json") as content_file:  
        content = json.load(content_file)    
    with open(content["document setup"]["design file"]) as design_file:
        design = json.load(design_file)

    c = canvas.Canvas(filename = gen_file_name(content), pagesize=(841.89,595.27))
    c.translate(0,595.27) # moves the origin of the coordinates to the upper left corner
    place_doc_title(c, content, design)


    c.showPage()
    c.save()
