from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

def generate_certificate(nome_participante, data_inicio, hora_inicio, carga_horaria, codigo_autenticacao, nome_evento):
    
    reader = PdfReader("./assets/modelo_certificado.pdf")
    writer = PdfWriter()

    buffer = BytesIO()
    can = canvas.Canvas(buffer)

    pdfmetrics.registerFont(TTFont("SloopScript", "./assets/fonts/sloop-script.ttf"))
    can.setFont("SloopScript", 40)
    can.drawString(265, 280, nome_participante)

    can.setFont("Helvetica", 15)
    can.drawString(267, 143, data_inicio)
    can.drawString(369, 143, hora_inicio)
    can.drawString(579, 143, carga_horaria)
    
    can.setFont("Helvetica", 11)
    can.drawString(50, 520, codigo_autenticacao)
    can.setFont("Helvetica-Bold", 15)
    can.drawString(350, 182, nome_evento)
    
    can.save()
    buffer.seek(0)

    temp_pdf = PdfReader(buffer)
    for page in reader.pages:
        page.merge_page(temp_pdf.pages[0])
        writer.add_page(page)

    cert_temp = "./assets/certificado_temp.pdf"
    with open(cert_temp, "wb") as output_pdf:
        writer.write(output_pdf)

    return cert_temp