from flask import Blueprint, jsonify, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc, func
from models import db
from models.spreadsheet import File, Spreadsheet
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/files', methods=['GET'])
@login_required
def get_all_files():
    accessible_spreadsheets_ids = [s.id for s in current_user.spreadsheets]
    
    files = File.query.filter(
        File.spreadsheet_id.in_(accessible_spreadsheets_ids)
    ).order_by(File.upload_timestamp.desc()).all()

    output = []
    for file in files:
        output.append({
            'id': file.id,
            'filename': file.filename,
            'spreadsheet_name': file.spreadsheet.name,
            'version': file.version,
            'upload_timestamp': file.upload_timestamp.isoformat(),
            'download_url': url_for('download_file', file_id=file.id, _external=True)
        })
    return jsonify(output)

@api_bp.route('/files/latest', methods=['GET'])
@login_required
def get_latest_file():
    accessible_spreadsheets_ids = [s.id for s in current_user.spreadsheets]

    latest_file = File.query.filter(
        File.spreadsheet_id.in_(accessible_spreadsheets_ids)
    ).order_by(File.upload_timestamp.desc()).first()

    if not latest_file:
        return jsonify({'message': 'Nenhum arquivo encontrado.'}), 404
    
    output = {
        'id': latest_file.id,
        'filename': latest_file.filename,
        'spreadsheet_name': latest_file.spreadsheet.name,
        'version': latest_file.version,
        'upload_timestamp': latest_file.upload_timestamp.isoformat(),
        'download_url': url_for('download_file', file_id=latest_file.id, _external=True)
    }
    return jsonify(output)

@api_bp.route('/files/latest_version/<string:filename>', methods=['GET'])
@login_required
def get_latest_version_of_file(filename):
    accessible_spreadsheets_ids = [s.id for s in current_user.spreadsheets]

    latest_version_file = File.query.filter(
        File.spreadsheet_id.in_(accessible_spreadsheets_ids),
        File.filename == filename
    ).order_by(File.version.desc()).first()

    if not latest_version_file:
        return jsonify({'message': f"Nenhuma versão do arquivo '{filename}' encontrada."}), 404
    
    output = {
        'id': latest_version_file.id,
        'filename': latest_version_file.filename,
        'spreadsheet_name': latest_version_file.spreadsheet.name,
        'version': latest_version_file.version,
        'upload_timestamp': latest_version_file.upload_timestamp.isoformat(),
        'download_url': url_for('download_file', file_id=latest_version_file.id, _external=True)
    }
    return jsonify(output)

# The /api/files/download/<file_id> can directly reuse the existing /download/<file_id> route
# from app.py, as it already has authentication and sends the file. If direct download via
# /api endpoint is strictly needed, a separate one could be created here.
# For now, I'll rely on the existing 'download_file' route for actual file serving.
