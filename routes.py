from flask import Flask, render_template
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
