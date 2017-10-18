from flask import Flask, render_template, request
from flaskext.markdown import Markdown

app = Flask(__name__)
markdown = Markdown(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/about/')
def about():
	content = open("README.md", "r").read()
	return render_template('about.html', content=content)

@app.route('/compare')
def compare():
	return render_template('compare.html')
