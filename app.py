from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection parameters
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = 'db'  # Docker service name for the database

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Log file size from .env or default to 10MB
log_file_size = int(os.getenv('LOG_FILE_SIZE', 10485760))

# Set up logging
log_file_path = os.path.join(os.getcwd(), 'app.log')
handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=5)

# Define the formatter and set it for the handler
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)

# Add the handler to the app's logger
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

def test_db_connection():
    try:
        # Execute a simple query
        db.session.execute(text('SELECT 1'))
        app.logger.info("Connected to the database successfully.")
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")

@app.route('/')
def index():
    test_db_connection()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
