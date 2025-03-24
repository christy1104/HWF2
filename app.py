from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

    # Add an admin user (if not exists)
    if not Admin.query.filter_by(username="MAIYU").first():
        hashed_password = bcrypt.generate_password_hash("ADMIN").decode("utf-8")
        new_admin = Admin(username="MAIYU", password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

# Route to Display Login Page
@app.route('/')
def login():
    return render_template('login.html')

# Route to Handle Login Form Submission
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = Admin.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session['admin'] = username
        flash("Login successful!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid username or password!", "danger")
        return redirect(url_for('login'))

# Admin Dashboard Route (After Login)
@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        return render_template('dashboard.html', username=session['admin'])
    else:
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
