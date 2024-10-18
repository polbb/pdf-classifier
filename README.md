# Python Coding Challenge

## Introduction

Welcome to the PDF Classifier Coding Challenge! In this take-home assignment, you'll build a RESTful API service that classifies PDF files into two categories: **"document"** or **"powerpoint"**. Your classification logic should be encapsulated within the `pdf_classifier` module, while the API will handle file uploads and return classification results.

---

## Getting Started

### Clone the Repository

Begin by cloning this repository. Click the **"Use this template"** button at the top right to create a new **private** repository:

![Clone Repository](image.png)

Once your repository is set up, navigate to the settings and invite `tomwhale` and `MAlGIaT` as collaborators. This will allow us to review your solution within the private repository:

![Invite Collaborators](image-1.png)

---

## Prerequisites

Make sure you have the following installed:

- **Python 3.x** (using Pyenv for version management is recommended)
- **Poetry** for dependency management

---

## Assignment Instructions

### 1. Project Overview

- **Objective**: Develop a **RESTful API service** that classifies PDF files as either **"document"** or **"powerpoint"**.
- **Functional Programming**: Emphasise a functional programming approach with a focus on **immutability**.
- **Module Structure**: Place the classification logic within the `pdf_classifier` module.
- **API Endpoints**:
  - **Upload Endpoint**: Allow users to upload a PDF and receive its classification.
  - **Retrieve Endpoint**: Fetch classification results for previously uploaded PDFs.

### 2. API Requirements

- Use any Python web framework, such as **FastAPI**, **Flask**, or **Django**.
- Ensure your API endpoints adhere to RESTful principles.
- Implement comprehensive error handling and validate all inputs.
- Incorporate logging for significant events and errors.

### 3. Code Quality

- Follow **PEP 8** style guidelines.
- Use type hints.
- (Optional) Develop both unit and integration tests to ensure your code functions correctly.

### 4. Deliverables

Ensure your submission includes the following:

- **Codebase**: Well-structured and organised.
- (Optional) **Tests**: Unit and integration tests that demonstrate your code works as intended.
- **Documentation**:
  - Explanation of your design decisions.
  - Instructions on how to run the application.
  - API usage guide.
- **README**: A concise summary of your approach.

### 5. Evaluation Criteria

Your submission will be evaluated based on:

- **Code Quality**: Cleanliness, readability, and adherence to best practices.
- **API Design**: Compliance with RESTful principles and logical structuring.
- **Error Handling**: Robustness and clarity of error messages.
- (Optional) **Testing**: Coverage and effectiveness of your unit and integration tests.
- **Documentation**: Clarity and completeness of your instructions and API usage guides.

---

Happy coding!
