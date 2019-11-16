from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,BaseDocTemplate, TableStyle, PageTemplate, Paragraph, Table, Spacer, Frame
from reportlab.lib.units import inch
import json
styles = getSampleStyleSheet()

# global document variables
gl_design = {}
gl_doc_setup = {} 

# color converter
color_dict = {
    "grey":colors.grey,
    "black":colors.black,
    "darkblue":colors.darkblue
}

def place_doc_title(canvas, doc):
    """places the title at the location defined in design.json
    Args:
        canvas (Canvas): canvas object from reportlab
        doc_title (string): Title of the document
        x (int): x coordinate
        y (int): y coordinate
    """
    x = gl_design["doc title"]["x"]
    y = gl_design["doc title"]["y"]
    size = gl_design["doc title"]["size"]
    doc_title = gl_doc_setup["doc title"]
    
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(x,y,doc_title)
    canvas.restoreState()

def merge_paragraphs_from_content(content):
    """Concatenate the paragraphs defined in the content file
    Args:
        canvas (canvas object): canvas object from reportlab
        content (Dict): paragraphs containing title and content of the paragraphs
    Returns:
        list: list of paragraph objects that are than used to fill the object
    """
    story = []
    for paragraph_obj  in content["paragraphs"]:
        if "table" in paragraph_obj.keys():
            paragraph = define_table_paragraph(paragraph_obj["title"], paragraph_obj["table"], gen_table_style(gl_design["table style"]))
        elif "text" in paragraph_obj.keys():
            paragraph = define_text_paragraph(paragraph_obj["title"], paragraph_obj["text"])
        story.append(paragraph[0])
        story.append(paragraph[1])
    return story

def define_text_paragraph(title, text):
    """Put together title and text of a paragraph
    Args:
        canvas (Canvas): canvas object from reportlab
        title (string): Title of the paragraph
        text (string): Text of the paragraph
    Returns:
        list: paragraph-object for title, paragraph-object for text
    """
    paragraph_title = Paragraph(title, styles["Heading2"])
    paragraph_text = Paragraph(text, styles["Normal"])
    return [paragraph_title, paragraph_text]

def gen_table_style(table_style_specs):
    style_list = TableStyle()
    if table_style_specs["grid lines"] == True:
        style_list.add("GRID", (0,0), (-1,-1), 0.5, color_dict[table_style_specs["grid color"]])
    if "font left column" in table_style_specs.keys():
        style_list.add("FONTNAME", (0,0), (0,-1), table_style_specs["font left column"])
    if "font right column" in table_style_specs.keys():
        style_list.add("FONTNAME", (1,0), (1,-1), table_style_specs["font right column"])
    return style_list

def define_table_paragraph(title, table_content, table_style):
    """Put together title and text of a paragraph
    Args:
        canvas (Canvas): canvas object from reportlab
        title (string): Title of the paragraph
        text (string): Text of the paragraph
    Returns:
        list: paragraph-object for title, paragraph-object for text
    """
    paragraph_title = Paragraph(title, styles["Heading2"])
    for row_idx in range(0,len(table_content)):
        for col_idx in range(0, len(table_content[row_idx])):
            table_content[row_idx][col_idx] = Paragraph(table_content[row_idx][col_idx], styles["Normal"]) # TODO make paragraph styles as defined in designx.isdisjoint(y)
    paragraph_table = Table(table_content, style=table_style) # TODO table style is not able to overwrite paragraph styles
    paragraph_table.hAlign = "LEFT"
    return [paragraph_title, paragraph_table]

def gen_file_name(title):
    """Generates the name of the PDF-file from the "doc title" in the json file.
    Args:
        content (dict): content from the json file
    Returns:
        string: file_name of the pdf-file
    """
    file_name = title+".pdf"
    return file_name

def page_template(page_width, page_height, n_cols, first_page = False):
    left_margin = 20
    right_margin = 20
    top_margin = 20
    bottom_margin = 20
    spacer_betw_cols = 20
    first_page_top_spacer = 40
    col_width = (page_width-left_margin-right_margin-spacer_betw_cols*2)/n_cols
    col_height = page_height - top_margin - bottom_margin
    if first_page:
         col_height = col_height - first_page_top_spacer
    page_frame_left = Frame(x1 = left_margin, y1 = bottom_margin, width = col_width, height = col_height, id=None, showBoundary=0)
    page_frame_middle = Frame(left_margin+col_width+spacer_betw_cols, bottom_margin, col_width, col_height, id=None, showBoundary=0)
    page_frame_right = Frame(left_margin+2*col_width+2*spacer_betw_cols, bottom_margin, col_width, col_height, id=None, showBoundary=0)

    page_template = PageTemplate(frames=[page_frame_left, page_frame_middle, page_frame_right], onPage=place_doc_title) 
    return page_template

if __name__ == "__main__":
    with open("example.json") as content_file:  
        content = json.load(content_file)    
    with open(content["document setup"]["design file"]) as design_file:
        design = json.load(design_file)

    gl_doc_setup = content["document setup"]
    gl_design = design
    first_page_template = page_template(841.89,595.27, 3, True)
    doc = BaseDocTemplate(filename=gen_file_name(content["document setup"]["doc title"]), pagesize=(841.89,595.27), pageTemplates=[first_page_template])

    #c = canvas.Canvas(filename = "phello.pdf", pagesize=(841.89,595.27))
    #c.translate(0,595.27) # moves the origin of the coordinates to the upper left corner
    #c.showPage()
    #c.save()

    #place_doc_title(first_page_template, content["document setup"]["doc title"], design["doc title"]["x"], design["doc title"]["y"])
    
    story = merge_paragraphs_from_content(content)
    doc.build(story)


