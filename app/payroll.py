import csv
import io
from datetime import datetime

from app.pdf_generator import generate_pdf_and_send_email


from flask import jsonify, render_template

from config import settings

employees = []

def parse_csv_data(csv_data):
    try:
        csv_decoded_raw_data = csv_data.decode("utf-8")
        csv_file = io.StringIO(csv_decoded_raw_data)
        csv_file_reader = csv.DictReader(csv_file)

        for row in csv_file_reader:
            employees.append(row)

    except Exception as e:
        raise ValueError(f"Error parsing csv data: {e}")

    return employees



