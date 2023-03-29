from flask import Flask
from flask import render_template

appl = Flask(__name__)


@appl.route('/')
def index():
    return render_template("index.html")

