from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory, send_file
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from models import db
from models.spreadsheet import Spreadsheet, File
from models.user import User
from config import Config
from blueprints.spreadsheet import spreadsheet_bp
from blueprints.auth import auth_bp
from utils.validator import validate_spreadsheet
from utils.report_generator import generate_pdf_report
import pandas as pd
import os
import shutil
import io

import re # Import the regular expression module
from sqlalchemy import func # Import func for max

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PERMANENT_STORAGE'] = 'permanent_storage'
app.config['SECRET_KEY'] = 'your_secret_key_here' # TODO: Change this to a strong secret key

db.init_app(app)
app.register_blueprint(spreadsheet_bp)
app.register_blueprint(auth_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Define the login view

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required # Protect this route
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        spreadsheet_id = request.form['spreadsheet_id']
        if file:
            spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
            
            # Permission check
            if current_user not in spreadsheet.users:
                flash('Você não tem permissão para fazer upload para esta planilha.', 'danger')
                return redirect(url_for('upload_file'))

            filename = file.filename
            
            # Filename validation
            if spreadsheet.filename_pattern:
                try:
                    if not re.match(spreadsheet.filename_pattern, filename):
                        errors = [f"O nome do arquivo '{filename}' não corresponde ao padrão esperado: '{spreadsheet.filename_pattern}'"]
                        return render_template('report.html', errors=errors, filename=filename, spreadsheet_id=spreadsheet_id)
                except re.error:
                    errors = [f"Padrão de nome de arquivo inválido configurado: '{spreadsheet.filename_pattern}'"]
                    return render_template('report.html', errors=errors, filename=filename, spreadsheet_id=spreadsheet_id)


            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            errors = validate_spreadsheet(filepath, spreadsheet.rules)

            if errors:
                return render_template('report.html', errors=errors, filename=filename, spreadsheet_id=spreadsheet_id)
            else:
                # Determine the next version
                latest_version = db.session.query(func.max(File.version)).filter(
                    File.spreadsheet_id == spreadsheet_id,
                    File.filename == filename
                ).scalar()
                
                new_version = (latest_version or 0) + 1

                new_file = File(filename=filename, spreadsheet_id=spreadsheet_id, version=new_version)
                db.session.add(new_file)
                db.session.commit()

                permanent_path = os.path.join(app.config['PERMANENT_STORAGE'], new_file.id)
                shutil.move(filepath, permanent_path)
                
                return render_template('success.html', file_id=new_file.id)

    spreadsheets = current_user.spreadsheets # Only show accessible spreadsheets
    return render_template('upload.html', spreadsheets=spreadsheets)

@app.route('/report/download/<int:spreadsheet_id>/<filename>')
@login_required # Protect this route
def download_report(spreadsheet_id, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
    
    # Permission check
    if current_user not in spreadsheet.users:
        flash('Você não tem permissão para baixar relatórios desta planilha.', 'danger')
        return redirect(url_for('index')) # Redirect to a safe place

    errors = validate_spreadsheet(filepath, spreadsheet.rules)
    
    pdf_content = generate_pdf_report(errors, filename)
    
    return send_file(
        io.BytesIO(pdf_content),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'{filename}_report.pdf'
    )

@app.route('/download/<file_id>')
@login_required # Protect this route
def download_file(file_id):
    file_record = File.query.get_or_404(file_id)
    
    # Permission check
    if current_user not in file_record.spreadsheet.users:
        flash('Você não tem permissão para baixar este arquivo.', 'danger')
        return redirect(url_for('saved_files')) # Redirect to saved files page

    return send_from_directory(app.config['PERMANENT_STORAGE'], file_id, as_attachment=True, download_name=file_record.filename)

@app.route('/saved_files')
@login_required # Protect this route
def saved_files():
    # Only show files from spreadsheets the current user has access to
    accessible_spreadsheets_ids = [s.id for s in current_user.spreadsheets]
    files = File.query.filter(File.spreadsheet_id.in_(accessible_spreadsheets_ids)).all()
    return render_template('saved_files.html', files=files)

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)