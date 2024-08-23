Simple Flask pet store app

Running the app
 1. Activate the virtual environment
    - On Linux - source venv/bin/activate
    - On Windows - venv\Scripts\activate
 2. Install dependencies - pip install Flask Flask-SQLAlchemy

Initialize the database
 - Start by opening a Python shell in your project directory: type python
 - Create tables in the python shell
        from app import db, create_app
        app = create_app()
        with app.app_context():
        db.create_all()

Run the flask app
 - flask run or python run.py
# This should start your Flask app on http://127.0.0.1:5000/ by default.
