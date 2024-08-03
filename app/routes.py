from app import app
from flask import Flask, render_template

@routes('/')
def home():
    return render_template('base.html')
