# Created by Ajay Path
# Date July 2022

# This is the file used to run the application.
# This website is a demo site used for testing purposes and is hosted locally.
# The app uses the flask library to create the website and the look and function of the website is defined using the files:
# pages.py, base.html, style.css

import sqlite3
from flask import Flask, request, session, g, render_template
from pages import pages
import os

app = Flask(__name__)

app.register_blueprint(pages, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)


