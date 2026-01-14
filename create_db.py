from app import app, db, create_tables

with app.app_context():
    create_tables()
    print("Database tables created.")
