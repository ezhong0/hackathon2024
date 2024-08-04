from flask import render_template, flash, redirect, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from functools import wraps
from app.forms import LoginForm, SignUpForm, ProfileForm, PreferencesForm
from .models import db, User
from app.algorithm import *
import os
from werkzeug.utils import secure_filename
from PIL import Image

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define allowed file extensions
PHOTO_SIZE = 125

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in to access this page. User: 123123 Password: 123123')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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
            return redirect(url_for('swipes'))  # Redirect to swipes
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
    user = User.query.get(user_id)
    if not user:
        flash('Invalid user. Please sign up first.')
        return redirect(url_for('signup'))

    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.age = int(form.age.data)
        user.field = form.field.data
        user.location = form.location.data
<<<<<<< HEAD
        #update_user_location(user.id, user.location)
        user.self_description = form.self_description.data  # Corrected to match the form field name
=======
        user.self_description = form.self_description.data
>>>>>>> 74f780b6c9b732eb1003c3c121f8da8a0013f411
        user.experience = form.experience.data
        user.strength = form.strength.data
        user.goals = form.goals.data
        
<<<<<<< HEAD
        #db.session.commit()  # Save the updated user data to the database

        flash('Profile updated successfully! Please log in.')
        return redirect(url_for('preferences', user_id = user_id))

    return render_template('profile.html', title='Profile', form=form)

@app.route('/preferences/<int:user_id>', methods=['GET', 'POST'])
def preferences(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('Invalid user. Please sign up first.')
        return redirect(url_for('signup'))

    form = PreferencesForm(obj=user)

    if form.validate_on_submit():
        user.pAge = int(form.pAge.data)
        user.pField = form.pField.data
        user.pLocation = form.pLocation.data
        user.pLocation_lat, user.pLocation_lng = get_coordinates(user.pLocation)
        user.pGoals = form.pGoals.data
        user.pQualities = form.pQualities.data
        db.session.commit()
=======
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
>>>>>>> 74f780b6c9b732eb1003c3c121f8da8a0013f411

                # Crop and resize the image
                image = Image.open(file_path)
                image = crop_center(image, PHOTO_SIZE, PHOTO_SIZE)  # Crop and resize to 125x125 pixels
                image.save(file_path)

                user.profile_photo = url_for('static', filename='uploads/' + filename)
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('login'))

    return render_template('preferences.html', title='Preferences', form=form)

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

@app.route('/users')
@login_required
def list_users():
    users = User.query.all()  # Query all users
    current_user_id = session.get('user_id')  # Get the current user's ID from the session
    current_user = User.query.get(current_user_id)  # Fetch the current user from the database

    return render_template('users.html', users=users, current_user=current_user)  # Pass users and current user to the template

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.')
    return redirect(url_for('login'))  # Redirect to login page

@login_required
@app.route('/swipes')
def swipes():

    # Fetch the current user from the database
    current_id = 22 #hardcoded
    user = User.query.get(current_id)
    
    # Ensure the user exists
    if user is None:
        return "User not found", 404
    
    # Prepare user data for rendering
    user_data = {
        'name': user.name,
        'location': user.location,
        'description': user.self_description,
        'background': user.experience,
        'word1': user.strength,
        'word2': 'Innovative',
        'word3': 'Dedicated',
        'image_url': user.profile_photo,  # Include image URL in user data
    }
    
    return render_template('swipes.html', user=user_data)
