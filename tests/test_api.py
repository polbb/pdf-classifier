import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_upload_valid_pdf():
    '''Test uploading a valid PDF file'''
    with open('tests/test_pdfs/doc_sample_valid.pdf', 'rb') as pdf_file:
        response = client.post('/classify/', files={'file': pdf_file})
    assert response.status_code == 200
    assert 'classification' in response.json()
    assert response.json()['classification'] == 'document'


def test_upload_valid_ppt():
    '''Test uploading a valid PPT file'''
    with open('tests/test_pdfs/ppt_sample_valid.pdf', 'rb') as ppt_file:
        response = client.post('/classify/', files={'file': ppt_file})
    assert response.status_code == 200
    assert 'classification' in response.json()
    assert response.json()['classification'] == 'powerpoint'


def test_upload_non_pdf_file():
    '''Test uploading a non-PDF file (should fail)'''
    response = client.post(
        '/classify/',
        files={
            'file': (
                'invalid.txt',
                b'invalid content')})
    assert response.status_code == 422


def test_upload_corrupted_pdf():
    '''Test uploading a corrupted PDF file'''
    with open('tests/test_pdfs/corrupted.pdf', 'rb') as corrupted_pdf:
        response = client.post('/classify/', files={'file': corrupted_pdf})
    assert response.status_code == 500  # Assuming a 500 error if the PDF is corrupted
    assert 'detail' in response.json()


def test_retrieve_results_after_upload():
    '''Test retrieving classification results after PDFs have been uploaded and classified'''
    with open('tests/test_pdfs/doc_sample_valid.pdf', 'rb') as pdf_file:
        client.post('/classify/', files={'file': pdf_file})

    response = client.get('/results/')
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert 'classification' in response.json()[0]
