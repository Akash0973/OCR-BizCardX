# OCR Card Reader

This is a Python script that uses OCR (Optical Character Recognition) to extract information from business card images and store them in a MySQL database. It utilizes the pytesseract library for text recognition and the mysql-connector-python library for interacting with the database.

## Prerequisites

- Python 3
- pytesseract library
- PIL (Python Imaging Library) library
- mysql-connector-python library
- Tesseract OCR engine (installed separately, see instructions below)
- MySQL server (running locally or on a remote host)

## Installation

1. Clone this repository to your local machine.
2. Install the required Python libraries by running the following command in your terminal or command prompt: pip install -r requirements.txt
3. Install the Tesseract OCR engine by following the instructions provided at [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
4. Update the database connection details in the script (`host`, `user`, `password`, `db_name`) to match your MySQL server configuration.

## Usage

1. Run the script using the following command in the command prompt: streamlit run app.py
2. The script will prompt you to upload a business card image (PNG or JPG format).
3. After uploading the image, the script will perform OCR on the image and extract relevant information such as company name, name, designation, phone numbers, email, website, area, city, state, and pincode.
4. You can review and update the extracted information in the provided input fields.
5. Click the "Add to Database" button to store the information in the MySQL database.
6. The script also provides options to update or delete existing records in the database.
