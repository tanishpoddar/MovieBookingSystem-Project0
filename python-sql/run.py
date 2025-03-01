from app import create_app
from app.utils.db_init import init_db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        init_db()  # Initialize sample data
    app.run(debug=True)