# pokemon/utils.py
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP_SSL
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from django.http import HttpResponseRedirect
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def split_long_text(description, max_line_length=50):
    lines = []
    current_line = []

    for word in description.split():
        if len(' '.join(current_line + [word])) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return '\n'.join(lines)

def create_pdf(pokemon_name, abilities):
    pdf_filename = f"{pokemon_name}_abilities.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    story = []

    col_widths = [120, 400]
    font_size = 10

    table_data = [['Ability Name', 'Description']]
    table_data.extend(abilities)

    table = Table(table_data, colWidths=col_widths, style=[
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', font_size),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('BACKGROUND', (0, 1), (-1, -1), (0.85, 0.85, 0.85)),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])

    table = KeepTogether(table)
    story.append(Paragraph(f"{pokemon_name} Abilities:", styles["Normal"]))
    story.append(table)

    doc.build(story)
    return pdf_filename
