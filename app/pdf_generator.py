import datetime
import json
import os
import unicodedata
from io import BytesIO

from reportlab.lib.colors import Color

from app.email_service import send_email
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

country_configuration = {
    "USA": {
        "translations": {
            "employee": "Employee",
            "position": "Position",
            "pay_period": "Payroll Period",
            "email": "Email",
            "gross_salary": "Gross Salary",
            "gross_payment": "Gross Payment",
            "net_payment": "Net Payment",
            "health_discount": "Health Discount",
            "social_discount": "Social Discount",
            "taxes_discount": "Taxes Discount",
            "other_discount": "Other Discount",
        },
        "filename_format": "paystub_{}.pdf",
        "company_logo_path": "../data/LOGO-ATDEV.png",
        "default_logo_path": "../data/default.png",
        "title": "Paystub"
    },
    "do": {
        "translations": {
            "employee": "Empleado",
            "position": "Cargo",
            "pay_period": "Periodo de Pago",
            "email": "Correo Electronico",
            "gross_salary": "Salario Bruto",
            "gross_payment": "Pago Bruto",
            "net_payment": "Pago Neto",
            "health_discount": "Descuento de Salud",
            "social_discount": "Descuento Seguro Social",
            "taxes_discount": "Descuento de Impuestos",
            "other_discount": "Otros Descuentos",
        },
        "filename_format": "comprobante_{}.pdf",
        "company_logo_path": "../data/LOGO-ATDEV.png",
        "default_logo_path": "../data/default.png",
        "title": "Comprobante de Pago"
    }
}

def generate_pdf(employee, details, salary_details, company):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    logo_path = "data/logos/default.png"

    if company == "atdev":
        logo_path = "data/logos/LOGO-ATDEV.png"

    if os.path.exists(logo_path):
        pdf.setFillColor(Color(0.2, 0.4, 0.8))
        logo_x = 50
        logo_y = height - 120
        logo_width = 180
        logo_height = 60
        pdf.rect(logo_x, logo_y, logo_width, logo_height, fill=True)
        pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True,
                      mask='auto')

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - 150, f"Paystub  - {employee['full_name']}")

    pdf.setFont("Helvetica", 12)

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

    return pdf_content

def generate_pdf_and_send_email(employees, country=None, company=None):
    sent_emails = []
    config = country_configuration.get(country, country_configuration[country])
    for employee in employees:
            details = [
                [config["translations"]["employee"], employee['full_name']],
                [config["translations"]["position"], employee['position']],
                [config["translations"]["pay_period"], employee['period']],
                [config["translations"]["email"], employee['email']]
            ]

            salary_details = [
                [config["translations"]["gross_salary"], employee['gross_salary']],
                [config["translations"]["gross_payment"], employee['gross_payment']],
                [config["translations"]["net_payment"], employee['net_payment']],
                [config["translations"]["health_discount"], employee['health_discount_amount']],
                [config["translations"]["social_discount"], employee['social_discount_amount']],
                [config["translations"]["taxes_discount"], employee['taxes_discount_amount']],
                [config["translations"]["other_discount"], employee['other_discount_amount']]
            ]

            pdf_content = generate_pdf(employee, details, salary_details, company)
            file_name = config["filename_format"].format(employee['full_name'].replace(" ", "_"))
            file_name = unicodedata.normalize("NFKD", file_name).encode("ascii", "ignore").decode('utf-8')
            email_info = send_email(employee['email'], pdf_content, file_name)
            sent_emails.append(email_info)

    return json.dumps(sent_emails)


