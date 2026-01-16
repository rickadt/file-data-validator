from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.spreadsheet import Spreadsheet, ValidationRule, DataType
from models.user import User # Import User model
from functools import wraps # Import wraps for decorator

spreadsheet_bp = Blueprint('spreadsheet', __name__)

# Helper function to check if current user is Admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin':
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@spreadsheet_bp.route('/spreadsheets')
@admin_required # Only Admin can list/manage all spreadsheets
def list_spreadsheets():
    # Admin can see all spreadsheets
    spreadsheets = Spreadsheet.query.all() # Changed from current_user.spreadsheets
    return render_template('spreadsheets/list.html', spreadsheets=spreadsheets)

@spreadsheet_bp.route('/spreadsheets/add', methods=['GET', 'POST'])
@admin_required # Only Admin can add spreadsheets
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


@spreadsheet_bp.route('/spreadsheets/<int:spreadsheet_id>/edit', methods=['GET', 'POST'])
@admin_required # Only Admin can edit spreadsheets
def edit_spreadsheet(spreadsheet_id):
    spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
    # No need to check spreadsheet.users here, as only Admin can access this route
    
    users = User.query.all()  # Fetch all users for selection

    if request.method == 'POST':
        spreadsheet.name = request.form['name']
        spreadsheet.filename_pattern = request.form.get('filename_pattern')

        # Update assigned users
        selected_users_ids = [int(uid) for uid in request.form.getlist('users')]
        spreadsheet.users = [user for user in users if user.id in selected_users_ids]

        db.session.commit()
        flash('Planilha atualizada com sucesso!', 'success')
        return redirect(url_for('spreadsheet.list_spreadsheets'))

    # For GET request, pre-select current users
    selected_users = [user.id for user in spreadsheet.users]
    return render_template('spreadsheets/edit.html', spreadsheet=spreadsheet, users=users, selected_users=selected_users)


@spreadsheet_bp.route('/spreadsheets/<int:spreadsheet_id>/rules/add', methods=['GET', 'POST'])
@admin_required # Only Admin can add rules
def add_rule(spreadsheet_id):
    spreadsheet = Spreadsheet.query.get_or_404(spreadsheet_id)
    # No need to check spreadsheet.users here, as only Admin can access this route

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

@spreadsheet_bp.route('/spreadsheets/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
@admin_required # Only Admin can edit rules
def edit_rule(rule_id):
    rule = ValidationRule.query.get_or_404(rule_id)
    # No need to check rule.spreadsheet.users here, as only Admin can access this route

    if request.method == 'POST':
        rule.column_name = request.form['column_name']
        rule.data_type = DataType[request.form['data_type']]
        rule.date_format = request.form.get('date_format')
        rule.required = 'required' in request.form
        db.session.commit()
        flash('Regra atualizada com sucesso!', 'success')
        return redirect(url_for('spreadsheet.list_spreadsheets'))
    return render_template('spreadsheets/edit_rule.html', rule=rule, spreadsheet=rule.spreadsheet, data_types=DataType)

@spreadsheet_bp.route('/spreadsheets/rules/<int:rule_id>/delete', methods=['POST'])
@admin_required # Only Admin can delete rules
def delete_rule(rule_id):
    rule = ValidationRule.query.get_or_404(rule_id)
    # No need to check rule.spreadsheet.users here, as only Admin can access this route

    db.session.delete(rule)
    db.session.commit()
    flash('Regra excluída com sucesso!', 'success')
    return redirect(url_for('spreadsheet.list_spreadsheets'))
