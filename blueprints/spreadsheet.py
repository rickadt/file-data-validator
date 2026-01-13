from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.spreadsheet import Spreadsheet, ValidationRule, DataType

spreadsheet_bp = Blueprint('spreadsheet', __name__)

@spreadsheet_bp.route('/spreadsheets')
def list_spreadsheets():
    spreadsheets = Spreadsheet.query.all()
    return render_template('spreadsheets/list.html', spreadsheets=spreadsheets)

@spreadsheet_bp.route('/spreadsheets/add', methods=['GET', 'POST'])
def add_spreadsheet():
    if request.method == 'POST':
        name = request.form['name']
        spreadsheet = Spreadsheet(name=name)
        db.session.add(spreadsheet)
        db.session.commit()
        return redirect(url_for('spreadsheet.list_spreadsheets'))
    return render_template('spreadsheets/add.html')

@spreadsheet_bp.route('/spreadsheets/<int:spreadsheet_id>/rules/add', methods=['GET', 'POST'])
def add_rule(spreadsheet_id):
    spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
    if request.method == 'POST':
        column_name = request.form['column_name']
        data_type = request.form['data_type']
        date_format = request.form.get('date_format')
        required = 'required' in request.form
        rule = ValidationRule(
            spreadsheet_id=spreadsheet_id,
            column_name=column_name,
            data_type=DataType[data_type],
            date_format=date_format,
            required=required
        )
        db.session.add(rule)
        db.session.commit()
        return redirect(url_for('spreadsheet.list_spreadsheets'))
    return render_template('spreadsheets/add_rule.html', spreadsheet=spreadsheet, data_types=DataType)
