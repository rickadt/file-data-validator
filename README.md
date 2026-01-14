# Spreadsheet Validator

This is a web application for validating the format and data types of spreadsheets.

## Features

-   Upload spreadsheets in CSV or XLSX format.
-   Define validation rules for each spreadsheet, including:
    -   Column name
    -   Data type (STRING, INTEGER, FLOAT, DATE, BOOLEAN)
    -   Date format (e.g., DD/MM/AAAA)
    -   Required field
-   Validate uploaded files against the defined rules.
-   View a report of validation errors.
-   Download the error report as a PDF.
-   If the file is valid, it is saved with a unique ID and can be downloaded.
-   View and download previously saved, validated spreadsheets from the "Arquivos Salvos" page.

## Technologies Used

-   Python
-   Flask
-   SQLAlchemy
-   PostgreSQL
-   Docker
-   Pandas
-   FPDF

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd spreadsheet-validator
    ```

2.  **Start the PostgreSQL database:**
    ```bash
    docker-compose up -d
    ```

3.  **Install the dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Access the application:**
    Open your browser and go to `http://127.0.0.1:5000`.

## How to Use

1.  **Create a new spreadsheet configuration:**
    -   Go to the "Spreadsheets" page.
    -   Click on "Add Spreadsheet" and give it a name.

2.  **Add validation rules:**
    -   Click on "Add Rule" for the desired spreadsheet.
    -   Fill in the form with the column name, data type, date format (if applicable), and whether the column is required.

3.  **Upload a spreadsheet for validation:**
    -   Go to the "Upload" page.
    -   Choose the file and select the corresponding spreadsheet configuration.
    -   Click on "Upload and Validate".

4.  **View the report:**
    -   If there are errors, a report will be displayed.
    -   You can download the report as a PDF.

5.  **Download the validated file:**
    -   If the file is valid, you will be redirected to a success page with a unique ID for the file.
    -   You can use the provided link to download the validated file.
