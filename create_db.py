from app import app, db, create_tables
from models.user import User # Import User model

with app.app_context():
    create_tables()
    print("Database tables created.")

    # Check if admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        new_admin = User(username='admin', email='admin@local', sector='Administration', role='Admin')
        new_admin.set_password('admin') # Set password for admin
        db.session.add(new_admin)
        db.session.commit()
        print("Default admin user created: admin/admin")
    else:
        print("Admin user already exists.")
