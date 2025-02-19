from flask import Flask, request, jsonify
from config.settings import API_USER, API_PASSWORD
from app.payroll import parse_csv_data
from app.pdf_generator import generate_pdf_and_send_email
import json

app = Flask(__name__)


@app.route("/process", methods=["GET", "POST"])
def process_paystubs():
    # Query params to be used later to make the PDF
    credentials = request.args.get("credentials")
    country = request.args.get("country", default="do")
    company = request.args.get("company", default="")

    if not credentials:
        return jsonify({"error": "No credentials provided"}), 400

    user, password = credentials.split()

    if user != API_USER or password != API_PASSWORD:
        return jsonify({"success": False, "message": "user or password incorrect."}), 401

    if request.method == "POST":
        employees = parse_csv_data(request.get_data())
        sent_emails = generate_pdf_and_send_email(employees, country, company)

        return jsonify({"success": True, "sent_emails": json.loads(sent_emails)}), 200

    return jsonify({"success": True, "params": {"country": country, "company": company}}), 200


if __name__ == "__main__":
    app.run(debug=True)
