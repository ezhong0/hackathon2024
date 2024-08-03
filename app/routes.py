from flask import render_template, flash, redirect, url_for, session  # Import session
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
        
        if user:  # and user.check_password(password):  # Verify the password
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
        user = User(username=form.username.data, email=form.email.data)
        # user.set_password(form.password.data)  # Assuming you have a method for hashing the password

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('profile'))  # Redirect to the profile page after signing up

    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/users')
def list_users():
    users = User.query.all()  # Query all users
    return render_template('users.html', users=users)  # Pass users to a template

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')  # Get the user ID from the session
    if not user_id:
        flash('Please log in to access your profile.')
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user = User.query.get(user_id)  # Fetch the user from the database
    form = ProfileForm(obj=user)  # Pre-fill the form with existing user data

    if form.validate_on_submit():
        user.name = form.name.data
        user.age = int(form.age.data)  # Convert Decimal to int
        user.field = form.field.data
        user.location = form.location.data
        user.self_description = form.selfDescription.data
        user.experience = form.experience.data
        user.strength = form.strength.data
        user.goals = form.goals.data
        
        db.session.commit()  # Save the updated user data to the database

        flash('Profile updated successfully!')
        return redirect(url_for('login'))

    return render_template('profile.html', title='Profile', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.')
    return redirect(url_for('login'))  # Redirect to login page
