from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory, send_file
from models import db
from models.spreadsheet import Spreadsheet, File
from config import Config
from blueprints.spreadsheet import spreadsheet_bp
from utils.validator import validate_spreadsheet
from utils.report_generator import generate_pdf_report
import pandas as pd
import os
import shutil
import io

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PERMANENT_STORAGE'] = 'permanent_storage'

db.init_app(app)
app.register_blueprint(spreadsheet_bp)

def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        spreadsheet_id = request.form['spreadsheet_id']
        if file:
            spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            errors = validate_spreadsheet(filepath, spreadsheet.rules)

            if errors:
                return render_template('report.html', errors=errors, filename=filename, spreadsheet_id=spreadsheet_id)
            else:
                new_file = File(filename=filename, spreadsheet_id=spreadsheet_id)
                db.session.add(new_file)
                db.session.commit()

                permanent_path = os.path.join(app.config['PERMANENT_STORAGE'], new_file.id)
                shutil.move(filepath, permanent_path)
                
                return render_template('success.html', file_id=new_file.id)

    spreadsheets = db.session.query(Spreadsheet).all()
    return render_template('upload.html', spreadsheets=spreadsheets)

@app.route('/report/download/<int:spreadsheet_id>/<filename>')
def download_report(spreadsheet_id, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
        
    errors = validate_spreadsheet(filepath, spreadsheet.rules)
    
    pdf_content = generate_pdf_report(errors, filename)
    
    return send_file(
        io.BytesIO(pdf_content),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'{filename}_report.pdf'
    )

@app.route('/download/<file_id>')
def download_file(file_id):
    file_record = File.query.get_or_404(file_id)
    return send_from_directory(app.config['PERMANENT_STORAGE'], file_id, as_attachment=True, download_name=file_record.filename)

@app.route('/saved_files')
def saved_files():
    files = File.query.all()
    return render_template('saved_files.html', files=files)

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)