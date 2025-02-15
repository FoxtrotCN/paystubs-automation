import csv
import io



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



