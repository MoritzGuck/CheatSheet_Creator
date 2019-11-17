from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,BaseDocTemplate, TableStyle, PageTemplate, Paragraph, Table, Spacer, Frame
from reportlab.lib.units import inch
import json
import argparse

# global document variables
styles = getSampleStyleSheet()
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
        doc (string): Title of the document
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
        content (Dict): paragraphs containing title and content of the paragraphs
    Returns:
        story (List): list of paragraph objects that are than used to fill the object
    """
    story = []
    for paragraph_obj  in content["paragraphs"]:
        if "table" in paragraph_obj.keys():
            paragraph = define_table_paragraph(paragraph_obj["title"], format_table_content(paragraph_obj["table"], gl_design["table style"]), gen_table_style(gl_design["table style"]))
        elif "text" in paragraph_obj.keys():
            paragraph = define_text_paragraph(paragraph_obj["title"], paragraph_obj["text"])
        story.append(paragraph[0])
        story.append(paragraph[1])
    return story

def define_text_paragraph(title, text):
    """Put together title and text of a paragraph
    Args:
        title (string): Title of the paragraph
        text (string): Text of the paragraph
    Returns:
        list: paragraph-object for title, paragraph-object for text
    """
    paragraph_title = Paragraph(title, styles["Heading2"])
    paragraph_text = Paragraph(text, styles["Normal"])
    return [paragraph_title, paragraph_text]

def gen_table_style(table_style_specs): # TODO get rid of either this function or format_table_styles
    """generates table_style object according to the specifications of ReportLab
    Args:
        table_style_spec (Dict): table style specifications from design.json
    Returns:
        style_list (list): table_style object
    """
    style_list = TableStyle()
    if table_style_specs["grid lines"] == True:
        style_list.add("GRID", (0,0), (-1,-1), 0.5, color_dict[table_style_specs["grid color"]])
    if "font left column" in table_style_specs.keys():
        style_list.add("FONTNAME", (0,0), (0,-1), table_style_specs["font left column"])
    if "font right column" in table_style_specs.keys():
        style_list.add("FONTNAME", (1,0), (1,-1), table_style_specs["font right column"])
    return style_list

def format_table_content(table_content, table_style_specs): # TODO get rid of either this function or gen_table_style
    """Format the content of the separate table cells via paragraph styles
    Args:
        table_content (Dict): Unformatted table content
        table_style_spec (Dict): table style specifications from design.json
    Returns:
        table_content (Dict): The same content, but now within Paragraphs
    """
    n_rows = len(table_content)
    n_cols = len(table_content[0])
    for row_idx in range(0, n_rows):
        for col_idx in range(0, n_cols):
            if "font left column" in table_style_specs.keys() and col_idx == 0:
                current_style = styles["Normal"]
                current_style.fontName = table_style_specs["font left column"]
                table_content[row_idx][col_idx] = Paragraph(table_content[row_idx][col_idx], current_style)
            if "font right column" in table_style_specs.keys() and col_idx == n_cols-1:
                current_style = styles["Normal"]
                current_style.fontName = table_style_specs["font right column"]
                table_content[row_idx][col_idx] = Paragraph(table_content[row_idx][col_idx], current_style)
    return table_content

def define_table_paragraph(title, table_content, table_style):
    """Put together title and text of a paragraph
    Args:
        title (string): Title of the paragraph
        text (string): Text of the paragraph
        table_style (Reportlab tablestyle): Table style object from Reportlab according to specifications in design.json
    Returns:
        list: paragraph-object for title, paragraph-object for text
    """
    paragraph_title = Paragraph(title, styles["Heading2"])
    # TODO Clean up the mess with format_table_content and gen_table_styles. If table_styles cannot overwrite the paragraph styles, make one function with 2 outputs.
    paragraph_table = Table(table_content, style=table_style) 
    paragraph_table.hAlign = "LEFT"
    return [paragraph_title, paragraph_table]

def gen_file_name(title):
    """Generates the name of the PDF-file from the "doc title" in the json file.
    Args:
        title (string): title of the file according to content.json 
    Returns:
        string: file_name of the pdf-file
    """
    file_name = title+".pdf"
    return file_name

def page_template(page_width, page_height, n_cols, first_page = False):
    """defines the page template for the cheat sheet
    Args:
        page_width (int): width of the shee in img points
        page_height (int): height of the sheet in img points
        n_cols (int): number of columns in the file
        first_page (bool, optional): defines, if it is the first page - if yes, than there is additional space for header. Defaults to False.
    Returns:
        page_template (Reportlab PageTemplate): page template object
    """
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
    # parse arguments:
    parser = argparse.ArgumentParser(description="create combinations of shapelets")
    parser.add_argument("--contentfile", required=False,
                        help="relative path and name of contentfile.json", default="content.json")
    args = parser.parse_args()

    # open files:
    with open(args.contentfile) as content_file:  
        content = json.load(content_file)    
    with open(content["document setup"]["design file"]) as design_file:
        design = json.load(design_file)

    # set up cheat sheet
    gl_doc_setup = content["document setup"]
    gl_design = design
    first_page_template = page_template(841.89,595.27, 3, True)
    doc = BaseDocTemplate(filename=gen_file_name(content["document setup"]["doc title"]), pagesize=(841.89,595.27), pageTemplates=[first_page_template])
    
    story = merge_paragraphs_from_content(content)
    doc.build(story)


