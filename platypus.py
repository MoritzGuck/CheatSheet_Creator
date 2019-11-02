
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

Title = "Hello world"
pageinfo = "platypus example"

def myFirstPage(canvas, doc):
    canvas.saveState()
    #canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    #canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    #canvas.setFont('Times-Roman',9)
    #canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def go():
    doc = SimpleDocTemplate("phello.pdf")
    #Story = [Spacer(1,2*inch)]
    Story = []
    style = styles["Normal"]
    for i in range(30):
        bogustext = ("Rem quo est nemo dolor. \
            Asperiores tenetur ad ex asperiores. Optio hic non ipsa voluptatibus \
            omnis ipsum sapiente sunt. Corporis aperiam nulla quia ipsa vitae. Molestiae\
            et excepturi dicta optio ut iusto. Et ipsam sed itaque dolor non. Laborum \
            qui et odit quia qui iure nulla. Ut in cupiditate dolor odit. Animi \
            pariatur eligendi dolore ea optio. Quia quam vero sunt autem et quod.\
            Perferendis molestiae error omnis hic ratione. Placeat tempora et alias. \
            Laudantium pariatur sint natus accusamus dolores voluptatem. Excepturi quia vel deleniti voluptate. Eos autem aut beatae quisquam voluptates placeat. Est magni nobis eos quasi. Harum et aspernatur expedita. Culpa velit quis fuga laboriosam quis. Molestiae aut enim non illum magnam asperiores corporis sint. At illo voluptatem excepturi dolorum et. Officia praesentium impedit qui molestias tenetur. Cupiditate id qui minus neque delectus.")
        p = Paragraph(bogustext, style)
        Story.append(Paragraph("Title", style))
        Story.append(p)
        Story.append(Spacer(1,0.1*inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

if __name__ == "__main__":
    go()