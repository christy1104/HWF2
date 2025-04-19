from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = "your_secret_key"

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -----------------------------
# Extensions
# -----------------------------
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# -----------------------------
# Models
# -----------------------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

# -----------------------------
# Initial Setup
# -----------------------------
with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username="MAIYU").first():
        hashed_password = bcrypt.generate_password_hash("ADMIN").decode("utf-8")
        new_admin = Admin(username="MAIYU", password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = Admin.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        flash("Invalid username or password!", "danger")
        return redirect(url_for('login'))

    session['admin'] = username
    flash("Login successful!", "success")
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if session.get('admin'):
        return render_template('dashboard.html', username=session['admin'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# -----------------------------
# Mentor Management
# -----------------------------
@app.route('/contact')
def contact():
    mentors = Mentor.query.all()
    return render_template('contact.html', mentors=mentors)

@app.route('/add_mentor', methods=['GET', 'POST'])
def add_mentor():
    if not session.get('admin'):
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        phone = request.form['phone']
        description = request.form['description']
        image = request.files.get('image')

        image_filename = None
        if image and image.filename:
            safe_name = secure_filename(image.filename)
            image_filename = f"mentor_{safe_name}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_mentor = Mentor(
            name=name,
            position=position,
            phone=phone,
            description=description,
            image=f"uploads/{image_filename}" if image_filename else None
        )

        db.session.add(new_mentor)
        db.session.commit()
        flash("Mentor added successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('add_mentor.html')

@app.route('/update_mentor/<int:mentor_id>', methods=['GET', 'POST'])
def update_mentor(mentor_id):
    if not session.get('admin'):
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    mentor = Mentor.query.get_or_404(mentor_id)

    if request.method == 'POST':
        mentor.name = request.form['name']
        mentor.position = request.form['position']
        mentor.phone = request.form['phone']
        mentor.description = request.form['description']

        image = request.files.get('image')
        if image and image.filename:
            safe_name = secure_filename(image.filename)
            image_filename = f"mentor_{mentor_id}_{safe_name}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            mentor.image = f"uploads/{image_filename}"

        db.session.commit()
        flash("Mentor details updated successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('update_mentor.html', mentor=mentor)

# -----------------------------
# Gallery Management
# -----------------------------
@app.route('/gallery')
def gallery():
    images = GalleryImage.query.all()
    return render_template('gallery.html', images=images)

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if not session.get('admin'):
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['image']
        if file and file.filename:
            safe_name = secure_filename(file.filename)
            filename = f"gallery_{safe_name}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_image = GalleryImage(filename=f"uploads/{filename}")
            db.session.add(new_image)
            db.session.commit()
            flash("Image added to gallery!", "success")
            return redirect(url_for('gallery'))

    return render_template('add_image.html')

@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    if not session.get('admin'):
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    image = GalleryImage.query.get_or_404(image_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(image.filename))

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

    db.session.delete(image)
    db.session.commit()
    flash("Image deleted from gallery!", "success")
    return redirect(url_for('gallery'))

# -----------------------------
# Static Pages
# -----------------------------
@app.route('/about')
def about():
    return render_template('about.html')

# -----------------------------
# Run Server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
