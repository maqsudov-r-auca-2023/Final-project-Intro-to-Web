from flask import Flask, render_template, request, redirect, url_for, Response, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import csv

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.config['DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'  # Replace with a secure value for production

db = SQLAlchemy(app)


# -------------------
# Models
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    mood = db.Column(db.String(20), nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<MoodEntry {self.date} - {self.mood}, Intensity {self.intensity}, Tags: {self.tags}>'


# -------------------
# Login required decorator
# -------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("🔒 Please log in to access this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# -------------------
# Routes
# -------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("⚠️ Username already taken.")
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("✅ Account created! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash("✅ Logged in successfully!")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("👋 You have been logged out.")
    return redirect(url_for('index'))


@app.route('/entry/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    if request.method == 'POST':
        date = request.form['date']
        mood = request.form['mood']
        intensity = int(request.form['intensity'])
        notes = request.form['notes']
        tags = request.form.get('tags')

        entry = MoodEntry(date=date, mood=mood, intensity=intensity, notes=notes, tags=tags)
        db.session.add(entry)
        db.session.commit()
        flash("✅ Mood entry saved!")
        return redirect(url_for('dashboard'))

    return render_template('new_entry.html')


@app.route('/dashboard')
@login_required
def dashboard():
    entries = MoodEntry.query.order_by(MoodEntry.date.desc()).all()
    return render_template('dashboard.html', entries=entries)


@app.route('/entry/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = MoodEntry.query.get_or_404(id)
    if request.method == 'POST':
        entry.date = request.form['date']
        entry.mood = request.form['mood']
        entry.intensity = int(request.form['intensity'])
        entry.notes = request.form['notes']
        entry.tags = request.form.get('tags')
        db.session.commit()
        flash("✏️ Mood entry updated!")
        return redirect(url_for('dashboard'))
    return render_template('edit_entry.html', entry=entry)


@app.route('/entry/<int:id>/delete', methods=['POST'])
@login_required
def delete_entry(id):
    entry = MoodEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("🗑️ Mood entry deleted.")
    return redirect(url_for('dashboard'))


@app.route('/chart')
@login_required
def mood_chart():
    entries = MoodEntry.query.order_by(MoodEntry.date.asc()).all()
    dates = [entry.date for entry in entries]
    moods = [entry.mood for entry in entries]
    intensities = [entry.intensity for entry in entries]
    return render_template('chart.html', dates=dates, moods=moods, intensities=intensities)


@app.route('/export/csv')
@login_required
def export_csv():
    entries = MoodEntry.query.order_by(MoodEntry.date.asc()).all()

    def generate():
        data = [['Date', 'Mood', 'Intensity', 'Notes', 'Tags']]
        for e in entries:
            data.append([e.date, e.mood, str(e.intensity), e.notes or "", e.tags or ""])
        output = ""
        for row in data:
            output += ",".join(f'"{cell}"' for cell in row) + "\n"
        return output

    return Response(generate(), mimetype='text/csv', headers={
        "Content-Disposition": "attachment;filename=mood_entries.csv"
    })


@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)


if __name__ == '__main__':
    app.run(debug=True)
