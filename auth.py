from flask import Blueprint, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    hashed_pw = generate_password_hash(password)

    if User.query.filter_by(email=email).first():
        return "User already exists", 409

    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    return redirect(url_for('dashboard'))

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    return "Invalid credentials", 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))
