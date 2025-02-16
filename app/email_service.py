import datetime
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import FROM_EMAIL, PASSWORD


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
    attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
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
