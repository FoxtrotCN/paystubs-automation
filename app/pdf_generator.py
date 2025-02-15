import datetime
import json
import os
import smtplib
from io import BytesIO
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from reportlab.lib.colors import Color

from config.settings import FROM_EMAIL, PASSWORD

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

fields_translation = {
    "english": [
        'Gross Salary',
        'Gross Payment',
        'Net Payment',
        'Health Insurance',
        'Social Security',
        'Taxes',
        'Others',
        'Paystub Payment',
        'Period'
    ]
}


def generate_pdf_and_send_email(employees, country=None):
    sent_emails = []
    if country == "USA":
        for employee in employees:
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            logo_path = "../data/logos/LOGO-ATDEV.png"
            if os.path.exists(logo_path):
                pdf.setFillColor(Color(0.2, 0.4, 0.8))
                logo_x = 50
                logo_y = height - 120
                logo_width = 180
                logo_height = 60
                pdf.rect(logo_x, logo_y, logo_width, logo_height, fill=True)
                pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(width / 2, height - 150, f"Paystub  - {employee['full_name']}")

            pdf.setFont("Helvetica", 12)
            details = [
                ["Employee:", employee['full_name']],
                ["Position:", employee['position']],
                ["Pay Period:", employee['period']],
                ["Email:", employee['email']]
            ]

            salary_details = [
                [fields_translation["english"][0], employee['gross_salary']],
                [fields_translation["english"][1], employee['gross_payment']],
                [fields_translation["english"][2], employee['net_payment']],
                [fields_translation["english"][3], employee['health_discount_amount']],
                [fields_translation["english"][4], employee['social_discount_amount']],
                [fields_translation["english"][5], employee['taxes_discount_amount']],
                [fields_translation["english"][6], employee['other_discount_amount']]
            ]

            def create_table(data, x, y):
                table = Table(data, colWidths=[150, 200])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('TOPPADDING', (0, 0), (-1, 0), 6),
                ]))
                table.wrapOn(pdf, width, height)
                table.drawOn(pdf, x, y)

            create_table(details, 50, height - 250)
            create_table(salary_details, 50, height - 450)

            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(width / 2, 50, f"Date: {datetime.date.today()}")

            pdf.save()

            buffer.seek(0)
            pdf_content = buffer.getvalue()
            buffer.close()

            email_info = send_email(employee['email'], pdf_content,
                                    f"paystub{employee['full_name'].replace(' ', '_')}.pdf")
            sent_emails.append(email_info)

        return json.dumps(sent_emails)

    else:
        for employee in employees:
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            logo_path = "../data/logos/LOGO-ATDEV.png"
            if os.path.exists(logo_path):
                pdf.drawImage(logo_path, 50, height - 120, width=180, height=60, preserveAspectRatio=True,
                              mask='auto')

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(width / 2, height - 150, f"Comprobante de Pago - {employee['full_name']}")

            pdf.setFont("Helvetica", 12)
            details = [
                ["Empleado:", employee['full_name']],
                ["Posicion:", employee['position']],
                ["Periodo:", employee['period']],
                ["Correo Electronico:", employee['email']]
            ]

            salary_details = [
                ["Salario Bruto:", employee['gross_salary']],
                ["Pago Bruto:", employee['gross_payment']],
                ["Pago Neto:", employee['net_payment']],
                ["Descuento Salud:", employee['health_discount_amount']],
                ["Descuento Social:", employee['social_discount_amount']],
                ["Descuento Impuestos:", employee['taxes_discount_amount']],
                ["Otros Descuentos:", employee['other_discount_amount']]
            ]

            def create_table(data, x, y):
                table = Table(data, colWidths=[150, 200])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('TOPPADDING', (0, 0), (-1, 0), 6),
                ]))
                table.wrapOn(pdf, width, height)
                table.drawOn(pdf, x, y)

            create_table(details, 50, height - 250)
            create_table(salary_details, 50, height - 450)

            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(width / 2, 50, f"Fecha: {datetime.date.today()}")

            pdf.save()

            buffer.seek(0)
            pdf_content = buffer.getvalue()
            buffer.close()

            email_info = send_email(employee['email'], pdf_content,
                                    f"comprobante_{employee['full_name'].replace(' ', '_')}.pdf")
            sent_emails.append(email_info)

        return json.dumps(sent_emails)


def send_email(to_email, pdf_content, filename):
    sent_emails = []
    from_email = FROM_EMAIL
    password = PASSWORD

    msg = MIMEMultipart()
    msg['From'] = Header(from_email, 'utf-8')
    msg['To'] = Header(to_email, 'utf-8')
    msg['Subject'] = Header("Comprobante de Pago", 'utf-8')
    body = "Adjunto encontraras tu comprobante de pago."

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

        sent_emails.append({
            "email": to_email,
            "sent_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

    return sent_emails
