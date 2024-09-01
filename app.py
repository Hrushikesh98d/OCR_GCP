from flask import Flask, request, render_template, send_from_directory
from google.oauth2 import service_account
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError

import os
import mimetypes
import logging

# Set environment variable for Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/Hrushikesh/Desktop/Trade_Sun_Project/OCR_GCP/service-account-key.json"

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO)

def process_document_sample(file_content, processor_id, mime_type):
    project_id = "842588065610"
    location = "us"

    try:
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)
        name = client.processor_path(project_id, location, processor_id)

        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request_obj = documentai.ProcessRequest(name=name, raw_document=raw_document, field_mask="entities")
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

        if document_file:
            file_content = document_file.read()
            mime_type, _ = mimetypes.guess_type(document_file.filename)

            if mime_type is None:
                logging.error("Unsupported file type")
                return "Unsupported file type", 400

            logging.info(f"File content length: {len(file_content)} bytes")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], document_file.filename)
            with open(file_path, 'wb') as f:
                f.write(file_content)

            entities = process_document_sample(file_content, processor_id, mime_type)
            file_url = f"/uploads/{document_file.filename}"
            return render_template('results.html', entities=entities, file_url=file_url)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
