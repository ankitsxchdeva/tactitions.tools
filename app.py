from flask import Flask, jsonify, render_template
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Database configuration
db_config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', 5432)
}

def get_db_connection():
    return psycopg2.connect(**db_config)

# Endpoint to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to serve the Tactician data
@app.route('/api/companions', methods=['GET'])
def get_companions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, icon_path FROM companions")
    companions = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert the fetched data to a list of dictionaries
    companions_list = [{"name": row[0], "icon_path": row[1]} for row in companions]

    return jsonify(companions_list)

if __name__ == '__main__':
    app.run(debug=True)
