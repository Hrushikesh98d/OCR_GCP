import os
from dotenv import load_dotenv

from flask import Flask, request, render_template
from google.oauth2 import service_account
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError
import logging


# LOADING ENVIRONMENT VARIABLES
load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

def process_document_sample(file_content, processor_id, mime_type="application/pdf", field_mask="entities"):

    try:
        credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

        opts = ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)
        name = client.processor_path(PROJECT_ID, LOCATION, processor_id)

        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request_obj = documentai.ProcessRequest(name=name, raw_document=raw_document, field_mask=field_mask)
        result = client.process_document(request=request_obj)
        document = result.document

        entities = [(entity.type_, entity.mention_text) for entity in document.entities]
        return entities
    except GoogleAPIError as e:
        logging.error(f"An error occurred: {e}")
        return [("Error", str(e))]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        document_file = request.files['document_file']
        processor_id = request.form['processor_type']

        print(document_file, document_file.filename)

        if document_file:
            file_content = document_file.read()
            entities = process_document_sample(file_content, processor_id)
            return render_template('results.html', pdf_path=document_file.filename, entities=entities)

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
