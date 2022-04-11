from fpdf import FPDF

def create_pdf(json):
    # Create default pdf setttings and add first page
    pdf = FPDF()
    pdf.set_font('Helvetica', '', 16)
    pdf.add_page()
    pdf.image('src/res/background.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '')
    pdf.set_text_color(255, 255, 255)