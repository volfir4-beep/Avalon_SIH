from flask import Flask, render_template, request, redirect, url_name
import sqlite3

app = Flask(__name__)

# Optional: Helper function to connect to a SQLite database if needed later
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route 1: Your Landing Page
@app.route('/')
def index():
    # Looks inside the 'templates' folder for index.html
    return render_template('index.html')

# Route 2: Your Friend's Login/Signup Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Example of how you will handle form data and SQL later
        # username = request.form['username']
        # password = request.form['password']
        # conn = get_db_connection()
        # conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        # conn.commit()
        # conn.close()
        pass 
        
    return render_template('login.html')

if __name__ == '__main__':
    # Runs the application in debug mode for active development
    app.run(debug=True)