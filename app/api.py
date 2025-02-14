from flask import Flask, request, jsonify
from flask import request

from config.settings import API_USER, API_PASSWORD
from payroll import parse_csv_data

import csv
import io

app = Flask(__name__)

@app.route("/process", methods=["GET", "POST"])
def process_paystubs():
    # Query params will use later to make the PDF
    credentials = request.args.get("credentials")
    country = request.args.get("country", default="do")
    company = request.args.get("company", default="")

    if not credentials:
        return jsonify({"error": "No credentials provided"}), 400

    user, password = credentials.split()

    if user != API_USER or password != API_PASSWORD:
        return jsonify({"success": False, "message": "user or password incorrect."}), 401

    if request.method == "POST":
        parse_csv_data(request.get_data())


    return jsonify({"success": True, "params": {"country": country, "company": company}}), 200



if __name__ == "__main__":
    app.run()
    app.run(debug=True)