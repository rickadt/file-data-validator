from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.spreadsheet import Spreadsheet
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Helper function to check if current user is Admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin':
            flash('Você não tem permissão para acessar esta página de administração.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/users')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('admin/list_users.html', users=users)


@admin_bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        sector = request.form['sector']
        password = request.form['password']
        role = request.form.get('role', 'User')  # Default to 'User'

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('admin.add_user'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já registrado.', 'danger')
            return redirect(url_for('admin.add_user'))

        new_user = User(username=username, full_name=full_name, email=email, sector=sector, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Usuário "{username}" criado com sucesso!', 'success')
        return redirect(url_for('admin.list_users'))
    return render_template('admin/add_user.html')


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    spreadsheets = Spreadsheet.query.all()  # Fetch all spreadsheets for assignment

    if request.method == 'POST':
        user.username = request.form['username']
        user.full_name = request.form['full_name']
        user.email = request.form['email']
        user.sector = request.form['sector']
        user.role = request.form['role']
        if 'password' in request.form and request.form['password']:
            user.set_password(request.form['password'])

        # Update spreadsheet access
        selected_spreadsheet_ids = [int(sid) for sid in request.form.getlist('spreadsheets')]
        user.spreadsheets = [s for s in spreadsheets if s.id in selected_spreadsheet_ids]

        db.session.commit()
        flash(f'Usuário "{user.username}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.list_users'))

    # For GET request, pre-select current user's spreadsheets
    selected_spreadsheets = [s.id for s in user.spreadsheets]
    return render_template('admin/edit_user.html', user=user, spreadsheets=spreadsheets, selected_spreadsheets=selected_spreadsheets)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'Admin' and User.query.filter_by(role='Admin').count() == 1:
        flash('Não é possível excluir o último administrador.', 'danger')
        return redirect(url_for('admin.list_users'))

    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário "{user.username}" excluído com sucesso!', 'success')
    return redirect(url_for('admin.list_users'))
