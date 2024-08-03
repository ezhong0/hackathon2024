from flask import current_app as app
from flask import Flask, render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.forms import ProfileForm

# from .models.db import db, User

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        flash('User name: {}, Age: {}, Field: {}, Location: {}, selfDescription: {}, Experience: {}, Strength: {}, Goals: {}'.format(
            form.name.data, form.age.data, form.field.data, form.location.data, form.selfDescription.data, form.experience.data, form.strength.data, form.goals.data))
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Information', form=form)



# @app.route('/users')
# def list_users():
#     users = User.query.all()  # Query all users
#     return render_template('users.html', users=users)  # Pass users to a template


@app.route('/register')
def register():
    return render_template('register.html')
