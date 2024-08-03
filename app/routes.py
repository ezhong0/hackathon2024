from flask import current_app as app
from flask import Flask, render_template

@app.route('/')
def home():
    return render_template('base.html',title= "hello")


@app.route('/login')
def login():
    return render_template('base.html',title= "login")
