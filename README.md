# Trade Sun

## Author
Hrushikesh Dandge

# Google Document AI Flask Web Application

This is a Flask web application that uses Google Document AI to extract entities from uploaded documents (e.g., PDFs). The extracted information is displayed as labels on a results page. The app uses Google Cloud's Document AI to process the documents and return structured data.

## Features

- Upload a document (PDF) through the web interface.
- Extract entities like dates, names, or custom labels using Google Document AI.
- Display extracted entities in a user-friendly results page.

## Prerequisites

### 1. Google Cloud Setup
- A Google Cloud account.
- Enable the **Document AI API** in your Google Cloud project.
- Create a **Document AI Processor** and note down its `processor_id`.
- Create a **Service Account** with Document AI access and download the JSON key file.

### 2. Install Google Cloud SDK (Optional but recommended)
- To interact with Google Cloud services locally, install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

### 3. Install Python 3.x

Make sure Python 3.x is installed on your system. You can check the version by running:

```bash
python3 --version
```

# Installation

### 1.Clone the Repository

```bash 
git clone https://github.com/your-username/document-ai-flask-app.git
cd document-ai-flask-app
```



### 2. Set Up the Environment

Install the required dependencies:

```bash 
pip install -r requirements.txt
```
### 3.Set Up Environment Variables

Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to your Google Cloud service account key file:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

Replace /path/to/your/service-account-key.json with the actual path to your Google Cloud service account key file.



### 4. Configure the Processor ID

Open the app.py file and set your Google Cloud project ID and processor ID:

```bash
project_id = "your-project-id"
processor_id = "your-processor-id"
```

# Run application

```bash 
python app.py
```