from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)  # ✅ Corrected

# Function to check login credentials
def check_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# *NEW: Route to serve the login page*
@app.route('/')
def show_login_page():
    return render_template('login.html')  # Renders the login.html page

# Route to handle login authentication
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from frontend
    username = data.get('username')
    password = data.get('password')

    if check_login(username, password):
        return jsonify({"status": "success", "message": "Login successful!"})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password!"})

# ✅ Corrected main block
if __name__ == '__main__':
    app.run(debug=True)
