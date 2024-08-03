from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, SignUpForm
from .models import db, User

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the username and password from the form
        username = form.username.data
        password = form.password.data  # Assuming you have a password field in your form
        
        # Find the user in the database
        user = User.query.filter_by(username=username).first()
        
        if user :#and user.check_password(password):  # Ensure you have a method to verify the password
            #session['user_id'] = user.id  # Store user ID in session
            flash('Login successful for user {}'.format(username))
            return redirect(url_for('list_users'))  # Redirect to the user list
        else:
            flash('Invalid username or password')  # Flash message for invalid login

    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Create a new user
        user = User(username=form.username.data, email=form.email.data)
        # user.set_password(form.password.data)  # Assuming you have a method for hashing the password

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))  # Redirect to the login page after signing up

    return render_template('signup.html', title='Sign Up', form=form)  # Render the sign-up template

@app.route('/users')
def list_users():
    users = User.query.all()  # Query all users
    return render_template('users.html', users=users)  # Pass users to a template

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        flash('User name: {}, Age: {}, Field: {}, Location: {}, selfDescription: {}, Experience: {}, Strength: {}, Goals: {}'.format(
            form.name.data, form.age.data, form.field.data, form.location.data, form.selfDescription.data, form.experience.data, form.strength.data, form.goals.data))
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Information', form=form)