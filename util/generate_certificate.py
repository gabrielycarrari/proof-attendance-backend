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

    # Define a fonte e tamanho inicial para o nome do participante
    font = "SloopScript"
    font_size = 40
    can.setFont(font, font_size)

    # Calcula a largura do texto do nome do participante
    text_width_participante = can.stringWidth(nome_participante, font, font_size)
    
    # Define o intervalo de 200 a 600
    min_x = 200
    max_x = 600
    available_width = max_x - min_x

    # Ajusta o tamanho da fonte se o texto do nome do participante for maior que o espaço disponível
    if text_width_participante > available_width:
        scale_factor = available_width / text_width_participante
        font_size = font_size * scale_factor
        can.setFont(font, font_size)
        text_width_participante = can.stringWidth(nome_participante, font, font_size)  # Recalcula a largura com o novo tamanho

    # Centraliza o nome do participante dentro do intervalo [200, 600]
    x_position_participante = min_x + (available_width - text_width_participante) / 2
    can.drawString(x_position_participante, 280, nome_participante)

    # Para o nome do evento
    # Define o intervalo de 200 a 600 para o nome do evento
    font_evento = "Helvetica-Bold"
    font_size_evento = 15
    can.setFont(font_evento, font_size_evento)

    # Calcula a largura do texto do nome do evento
    text_width_evento = can.stringWidth(nome_evento, font_evento, font_size_evento)

    # Ajusta o tamanho da fonte se o texto do nome do evento for maior que o espaço disponível
    if text_width_evento > available_width:
        scale_factor_evento = available_width / text_width_evento
        font_size_evento = font_size_evento * scale_factor_evento
        can.setFont(font_evento, font_size_evento)
        text_width_evento = can.stringWidth(nome_evento, font_evento, font_size_evento)  # Recalcula a largura com o novo tamanho

    # Centraliza o nome do evento dentro do intervalo [200, 600]
    x_position_evento = min_x + (available_width - text_width_evento) / 2
    can.drawString(x_position_evento, 182, nome_evento)

    can.setFont("Helvetica", 15)
    can.drawString(267, 143, data_inicio)
    can.drawString(369, 143, hora_inicio)
    can.drawString(580, 143, carga_horaria.__str__())
    
    can.setFont("Helvetica", 10)
    can.drawString(50, 520, codigo_autenticacao)
    
    can.save()
    buffer.seek(0)

    temp_pdf = PdfReader(buffer)
    for page in reader.pages:
        page.merge_page(temp_pdf.pages[0])
        writer.add_page(page)
    
    final_pdf_buffer = BytesIO()
    writer.write(final_pdf_buffer) 
    final_pdf_buffer.seek(0)  

    return final_pdf_buffer.read()