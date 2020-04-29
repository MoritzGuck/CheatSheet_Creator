from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,BaseDocTemplate, TableStyle, PageTemplate, Paragraph, Table, Spacer, Frame
from reportlab.lib.units import inch
import json
import argparse
import re
import yaml


def open_file(file_name):
    """open files
    Args:
        file_name (str): name of input file
    Raises:
        TypeError: [description]
    Returns:
        [type]: [description]
    """
    if re.match(r'\w+.yml$|\w+.yaml$|\w+.json$', file_name):
        with open(file_name) as file:
            dictionary = yaml.load(file, Loader=yaml.FullLoader)
    else:
        raise TypeError("wrong file type. please use .json, .yml or .yaml files.") # TODO this could also just be a missing file
    return dictionary

def gen_file_name(output_path, title):
    """Generates the name of the PDF-file from the "doc title" in the json file.
    Args:
        output_path (string): relative output path 
        title (string): title of the file according to content.json 
    Returns:
        string: file_name of the pdf-file
    """
    file_name = output_path + title + ".pdf"
    return file_name

class Document:
    def __init__(self, document, design):
        self.doc_metdata = document["document setup"]
        self.content = document["paragraphs"] 
        self.design = design
        self.styles = getSampleStyleSheet() 
        # color converter
        self.color_dict = {
            "grey": colors.grey,
            "black": colors.black,
            "darkblue": colors.darkblue
        }

    def place_doc_title(self, canvas, doc):
        """places the title at the location defined in design.json Args:
            canvas (Canvas): canvas object from reportlab
            doc (string): Title of the document
        """
        x = self.design["doc title"]["x"]
        y = self.design["doc title"]["y"]
        size = self.design["doc title"]["size"]
        doc_title = self.doc_metdata["doc title"]
        # Place title:
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(x, y, doc_title)
        canvas.restoreState()

    def merge_paragraphs_from_content(self):
        """Concatenate the paragraphs defined in the content file
        Args:
            content (Dict): paragraphs containing title and content of the paragraphs
        Returns:
            story (List): list of paragraph objects that are than used to fill the object
        """
        story = []
        for paragraph_obj  in self.content:
            if "table" in paragraph_obj.keys():
                table_obj = self.format_table_content(paragraph_obj["table"], self.design["table style"])
                paragraph = self.define_table_paragraph(paragraph_obj["title"], table_obj)
            elif "text" in paragraph_obj.keys():
                paragraph = self.define_text_paragraph(paragraph_obj["title"], paragraph_obj["text"])
            story.append(paragraph[0])
            story.append(paragraph[1])
        return story

    def define_text_paragraph(self, title, text):
        """Put together title and text of a paragraph
        Args:
            title (string): Title of the paragraph
            text (string): Text of the paragraph
        Returns:
            list: paragraph-object for title, paragraph-object for text
        """
        title_style = self.styles["Heading2"]
        title_style.fontSize = self.design["par style"]["font-size title"]
        paragraph_title = Paragraph(title, title_style)
        text_style = self.styles["Normal"]
        text_style.fontSize = self.design["par style"]["font-size text"]
        paragraph_text = Paragraph(text, text_style)
        return [paragraph_title, paragraph_text]

    def format_table_content(self, table_content, table_style_specs): # TODO: might be better to fetch the table_style_specs (via design) directly from the document object
        """Format the content of the separate table cells via paragraph styles
        Args:
            table_content (Dict): Unformatted table content
            table_style_spec (Dict): table style specifications from design.json
        Returns:
            table_content (Dict): The same content, but now within Paragraphs
        """
        # Define grid 
        table_style = TableStyle()
        if table_style_specs["grid lines"] == True:
            table_style.add("GRID", (0, 0), (-1, -1), 0.5, self.color_dict[table_style_specs["grid color"]])
        # add the content and format text
        n_rows = len(table_content)
        n_cols = len(table_content[0])
        content_style = self.styles["Normal"] # every cell is a paragraph with its style
        content_style.fontSize = table_style_specs["font-size"]
        for row_idx in range(0, n_rows):
            for col_idx in range(0, n_cols):
                if "font left column" in table_style_specs.keys() and col_idx == 0:
                    content_style.fontName = table_style_specs["font left column"]
                if "font right column" in table_style_specs.keys() and col_idx == n_cols-1:
                    content_style.fontName = table_style_specs["font right column"]
                table_content[row_idx][col_idx] = Paragraph(table_content[row_idx][col_idx], content_style)
        table = Table(table_content, style=table_style)
        return Table(table_content, style=table_style) # table_content, style_list

    def define_table_paragraph(self, title, table):
        """Put together title and text of a paragraph
        Args:
            title (string): Title of the paragraph
            table (Reportlab table_obj): contains the formatted table
        Returns:
            list: paragraph-object for title, paragraph-object for text
        """
        paragraph_title = Paragraph(title, self.styles["Heading2"])
        paragraph_title.fontSize = self.design["par style"]["font-size title"]
        table.hAlign = "LEFT"
        return [paragraph_title, table]

    def page_template(self, page_width, page_height, n_cols, first_page = False):
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

        page_template = PageTemplate(frames=[page_frame_left, page_frame_middle, page_frame_right], onPage=self.place_doc_title) 
        return page_template

    
if __name__ == "__main__":
    # parse arguments:
    parser = argparse.ArgumentParser(description="create combinations of shapelets")
    parser.add_argument("--c", required=False, help="relative path and name of contentfile.json", default="content.json")
    parser.add_argument("--o", required=False, help="relative path to output folder", default="./pdfs/")
    args = parser.parse_args()

    # open files:
    document = open_file(args.c) # open content file
    design = open_file(document["document setup"]["design file"])

    # set up cheat sheet
    doc_obj = Document(document, design)

    first_page_template = doc_obj.page_template(841.89,595.27, 3, True)
    output_doc = BaseDocTemplate(filename=gen_file_name(args.o, document["document setup"]["doc title"]), pagesize=(841.89,595.27), pageTemplates=[first_page_template])
    
    story = doc_obj.merge_paragraphs_from_content()
    output_doc.build(story)


