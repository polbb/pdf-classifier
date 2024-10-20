
# PDF Classification API

## Introduction

This document outlines the development and deployment of a RESTful API service for classifying PDF files into two categories: **"document"** or **"powerpoint"**. The classification logic is encapsulated within the `pdf_classifier` module, while the API handles file uploads and returns classification results.

---

## Getting Started

### Clone the Repository

Begin by cloning this repository. Click the **"Use this template"** button at the top right to create a new private repository.

### Prerequisites

Ensure you have the following installed:
- Python 3.x (using Pyenv for version management is recommended)
- Poetry for dependency management

---

## Running Instructions

### Step 1: Install Dependencies

Navigate to the project directory and run the following command to install dependencies:

```bash
poetry install
```

### Step 2: Run the Server

Activate the virtual environment and run the FastAPI server using one of the following methods:

#### Option 1: Run with Hot Reload (Recommended for Development)

To enable automatic reloading of the server when changes are made to the code, use the following command:

```bash
poetry shell
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

This will allow you to see code changes immediately without manually restarting the server.

The server should now be running at `http://127.0.0.1:8000`.

#### Option 2: Run Without Hot Reload (Recommended for Production)

If you do not need the hot reload feature, you can run the server directly:

```bash
poetry shell
python api/main.py
```

This will start the server without automatic reloading, which is more suitable for production environments.

The server should now be running at `http://127.0.0.1:8000`.
### Step 3: API Endpoints

- **Upload PDF for Classification**: `POST /classify/`
  - Endpoint to upload a PDF and classify it.
  - Example Request:
    ```bash
    curl -X POST "http://127.0.0.1:8000/classify/" -F "file=@example.pdf"
    ```
  - Example Response:
    ```json
    {
      "filename": "example.pdf",
      "classification": "document"
    }
    ```

- **Retrieve Classification Results**: `GET /results/`
  - Endpoint to retrieve the classification results of previously uploaded PDFs.
  - Example Request:
    ```bash
    curl -X GET "http://127.0.0.1:8000/results/"
    ```
  - Example Response:
    ```json
    [
      {
        "filename": "example.pdf",
        "classification": "document",
        "timestamp": "2024-10-18T12:34:56.789Z"
      }
    ]
    ```

---

## Design Decisions

- **Framework**: The FastAPI framework was chosen due to its fast performance, ease of use, and built-in support for modern Python features (such as type hints and async functionality).
- **Classification Model**: A logistic regression model was used for simplicity. The goal was to balance interpretability and efficiency, given the requirements of the classification task.
- **In-Memory Storage**: For simplicity, classification results are stored in memory. For a production-ready version, a persistent database (e.g., SQLite or PostgreSQL) would be preferable.

---


## Future Improvements

- Add pagination to the `/results/` endpoint for scalability.
- Replace in-memory storage with a persistent database to handle more extensive datasets.
- Improve error handling for edge cases, such as corrupted or very large PDF files.

---