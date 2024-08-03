from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash  # Import hashing functions
from app import app
from app.forms import LoginForm, SignUpForm, ProfileForm
from .models import db, User

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):  # Verify the password
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful for user {}'.format(username))
            return redirect(url_for('list_users'))  # Redirect to the user list
        else:
            flash('Invalid username or password')

    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        
        if existing_user:
            if existing_user.username == form.username.data:
                flash('Username already taken. Please choose a different one.')
            elif existing_user.email == form.email.data:
                flash('Email already registered. Please use a different one or log in.')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)  # Hash the password
            )

            db.session.add(user)
            db.session.commit()

            flash('Congratulations, you are now registered! Please complete your profile.')
            return redirect(url_for('profile', user_id=user.id))  # Pass user ID to the profile creation

    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.get(user_id)  # Fetch the user from the database
    if not user:
        flash('Invalid user. Please sign up first.')
        return redirect(url_for('signup'))

    form = ProfileForm(obj=user)  # Pre-fill the form with existing user data

    if form.validate_on_submit():
        user.name = form.name.data
        user.age = int(form.age.data)  # Convert Decimal to int
        user.field = form.field.data
        user.location = form.location.data
        user.self_description = form.self_description.data  # Corrected to match the form field name
        user.experience = form.experience.data
        user.strength = form.strength.data
        user.goals = form.goals.data
        
        db.session.commit()  # Save the updated user data to the database

        flash('Profile updated successfully! Please log in.')
        return redirect(url_for('login'))

    return render_template('profile.html', title='Profile', form=form)

@app.route('/users')
def list_users():
    users = User.query.all()  # Query all users
    return render_template('users.html', users=users)  # Pass users to a template

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.')
    return redirect(url_for('login'))  # Redirect to login page
