from app.api import app
from unittest.mock import MagicMock, create_autospec

from app.payroll import parse_csv_data
from app.pdf_generator import generate_pdf_and_send_email


def test_process_no_credentials():
    response = app.test_client().get('/process')

    assert response.status_code == 400
    assert response.json.get('error') == 'No credentials provided'


def test_process_invalid_credentials():
    response = app.test_client().get('/process?credentials=invalid+credentials')

    assert response.status_code == 401
    assert response.json.get('success') == False
    assert response.json.get('message') == 'user or password incorrect.'


def test_process_pdf():
    response = app.test_client().post('/process?credentials=atdevadmin+atdevadmin123&company=atdev&country=USA')

    assert response.status_code == 200
    assert response.json.get('success') == True
    create_autospec(parse_csv_data, return_value=[])
    create_autospec(generate_pdf_and_send_email, return_value=[])
    assert response.json.get('sent_emails') == []