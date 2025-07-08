from flask import Flask, render_template, redirect, url_for, request, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import csv
import io
from datetime import datetime
from models import db, User, Wine, Tasting

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/data/winesocial_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('register'))
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    wines_tasted = Tasting.query.filter_by(user_id=current_user.id).count()
    favorite_region = None
    # Calculate favorite region
    regions = db.session.query(Wine.region, db.func.count(Wine.region)).join(Tasting).filter(Tasting.user_id == current_user.id).group_by(Wine.region).order_by(db.func.count(Wine.region).desc()).all()
    if regions:
        favorite_region = regions[0][0]
    return render_template('dashboard.html', wines_tasted=wines_tasted, favorite_region=favorite_region)

# Additional routes and logic will be added here for wines, diary, analyses, gallery, etc.

from forms import WineForm
from models import Wine
from flask import abort

@app.route('/wines')
@login_required
def wine_catalog():
    wines = Wine.query.filter_by(user_id=current_user.id).all()
    return render_template('wine_catalog.html', wines=wines)

@app.route('/wines/add', methods=['GET', 'POST'])
@login_required
def add_wine():
    form = WineForm()
    if form.validate_on_submit():
        wine = Wine(
            user_id=current_user.id,
            name=form.name.data,
            year=form.year.data,
            type=form.type.data,
            region=form.region.data,
            alcohol=form.alcohol.data,
            price=form.price.data,
            producer=form.producer.data
        )
        db.session.add(wine)
        db.session.commit()
        flash('Wine added successfully.')
        return redirect(url_for('wine_catalog'))
    return render_template('wine_form.html', form=form, title='Add Wine')

@app.route('/wines/edit/<int:wine_id>', methods=['GET', 'POST'])
@login_required
def edit_wine(wine_id):
    wine = Wine.query.get_or_404(wine_id)
    if wine.user_id != current_user.id:
        abort(403)
    form = WineForm(obj=wine)
    if form.validate_on_submit():
        wine.name = form.name.data
        wine.year = form.year.data
        wine.type = form.type.data
        wine.region = form.region.data
        wine.alcohol = form.alcohol.data
        wine.price = form.price.data
        wine.producer = form.producer.data
        db.session.commit()
        flash('Wine updated successfully.')
        return redirect(url_for('wine_catalog'))
    return render_template('wine_form.html', form=form, title='Edit Wine')

@app.route('/wines/delete/<int:wine_id>', methods=['POST', 'GET'])
@login_required
def delete_wine(wine_id):
    wine = Wine.query.get_or_404(wine_id)
    if wine.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        db.session.delete(wine)
        db.session.commit()
        flash('Wine deleted successfully.')
        return redirect(url_for('wine_catalog'))
    return render_template('confirm_delete.html', item=wine, item_type='Wine')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
