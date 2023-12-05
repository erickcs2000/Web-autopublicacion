from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from models import db, Users
import bcrypt

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="El usuario ya existe en la base de datos.")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('register.html', error=None)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password, user.password.encode('utf-8')):
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for('home'))  
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")

    return render_template('login.html', error=None)

@auth_blueprint.route('/signout')
def signout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))
