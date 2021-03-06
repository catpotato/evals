from os import urandom
from flask import Flask, render_template, request, jsonify
from flaskext.markdown import Markdown
from processor import Processor
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from processor import Processor
from query import Query
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)
csrf = CSRFProtect(app)
markdown = Markdown(app)
csrf.init_app(app)
app.secret_key = urandom(24).encode('hex')

class ProfessorForm(FlaskForm):
	department = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'department'})
	course = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'course number'})
	professor = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'professor'})

@app.route('/')
def home():

	return render_template('index.html', data = Processor(Query()).get_processed_data_for_table())

@app.route('/about/')
def about():
	content = open("README.md", "r").read()
	return render_template('about.html', content=content)

@app.route('/compare/', methods=['GET', 'POST'])
def compare():
	form = ProfessorForm()

	if form.validate_on_submit():
		data = _process_query(department=form.department.data, course=form.course.data, professor=form.professor.data).get_processed_data()
		print(data)

	return render_template('compare.html', form=form)

# you send a department and course, it gives you back info with a professor and gpa preview
@app.route('/_get_preview', methods=['GET', 'POST'])
def _get_departments():
	period = request.args.get('period', None)
	department = request.args.get('department', None)
	course = request.args.get('course', None)
	return jsonify(Processor(Query(period=period, department=department, course=course)).get_preview())


@app.route('/_process_query')
def _process_query(department=None, period=None, course=None, professor=None):
	return Processor(Query(period=period, department=department, course=course, professor=professor))

if __name__ == '__main__':
    app.debug = True
    app.run()
