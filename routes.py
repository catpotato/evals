from flask import Flask, render_template, request, jsonify
from flaskext.markdown import Markdown
from processor import Processor

app = Flask(__name__)
markdown = Markdown(app)

@app.route('/')
def home():
	#q = Processor(Query((2016.5,2012.0), department, course, professor))
	return render_template('index.html')

@app.route('/about/')
def about():
	content = open("README.md", "r").read()
	return render_template('about.html', content=content)

@app.route('/compare')
def compare():
	return render_template('compare.html')

@app.route('/_send_query')
def send_query():
	department = request.args.get('department', False)
	course = request.args.get('course', False)
	professor = request.args.get('professor', False)

	print(department)
	print(course)
	print(professor)

	# TODO make injection attacks impossible!!!!

	return jsonify(Processor(Query((2016.5,2012.0), department, course, professor)))
