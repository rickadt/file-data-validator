from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.spreadsheet import Spreadsheet, ValidationRule, DataType
from models.user import User # Import User model

spreadsheet_bp = Blueprint('spreadsheet', __name__)

@spreadsheet_bp.route('/spreadsheets')
@login_required
def list_spreadsheets():
    # Only show spreadsheets the current user has access to
    spreadsheets = current_user.spreadsheets
    return render_template('spreadsheets/list.html', spreadsheets=spreadsheets)

@spreadsheet_bp.route('/spreadsheets/add', methods=['GET', 'POST'])
@login_required
def add_spreadsheet():
    users = User.query.all() # Fetch all users
    if request.method == 'POST':
        name = request.form['name']
        filename_pattern = request.form.get('filename_pattern') # Get filename pattern
        selected_users_ids = request.form.getlist('users') # Get list of selected user IDs
        
        spreadsheet = Spreadsheet(name=name, filename_pattern=filename_pattern)
        
        # Add selected users to the spreadsheet
        for user_id in selected_users_ids:
            user = User.query.get(user_id)
            if user:
                spreadsheet.users.append(user)
        
        db.session.add(spreadsheet)
        db.session.commit()
        flash('Planilha adicionada com sucesso!', 'success')
        return redirect(url_for('spreadsheet.list_spreadsheets'))
    return render_template('spreadsheets/add.html', users=users)

@spreadsheet_bp.route('/spreadsheets/<int:spreadsheet_id>/rules/add', methods=['GET', 'POST'])
@login_required
def add_rule(spreadsheet_id):
    spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
    # Check if current user has access to this spreadsheet
    if current_user not in spreadsheet.users:
        flash('Você não tem permissão para adicionar regras a esta planilha.', 'danger')
        return redirect(url_for('spreadsheet.list_spreadsheets'))

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
        flash('Regra adicionada com sucesso!', 'success')
        return redirect(url_for('spreadsheet.list_spreadsheets'))
    return render_template('spreadsheets/add_rule.html', spreadsheet=spreadsheet, data_types=DataType)
