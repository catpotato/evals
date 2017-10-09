import json, mechanize, urllib2, cookielib
from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy as sqlalch
import evaluation

years = [2014, 2013, 2012, 2011]
semmesters = [10,30]
departments = ['AFS', 'AGS', 'ART', 'AS', 'ASIA', 'BIOL', 'CE', 'CHE', 'CHEM', 'CHN', 'CL', 'CLSS', 'CM', 'CS', 'DOC', 'ECE', 'ECON', 'EDC', 'EGRS', 'ENG', 'ES', 'EVST', 'FAMS', 'FLL', 'FREN', 'FYS', 'GEOL', 'GERM', 'GOVT', 'GRK', 'HIST', 'IA', 'JAPN', 'LAT', 'MATH', 'ME', 'MS', 'NER', 'PHIL', 'PHYS', 'PSTD', 'PSYC', 'REL', 'RSS', 'SPAN', 'THTR', 'WGS']

def get_question_data(question, soup):

    header = soup.find(text=question)
    #print( header.parent.parent.parent)
    data_container = header.parent.parent.parent.find(class_ = 'questionDataContainer')
    data = data_container.find_all(class_ = 'col-xs-4')

    final_data = []
    #print(data)
    for datum in data:
        #print(float(datum.get_text()[:-2])/100)
        final_data.append(float(datum.get_text()[:-2])/100)

    return final_data

if __name__ == '__main__':

    engine = create_engine('sqlite:///data.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    # login

    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)

    br.open("https://fac-eval.lafayette.edu")

    br.select_form(nr=1)
    br.form['username'] = # nice try
    br.form['password'] = # boyo

    br.submit()

    for year in years:
        for semmester in semmesters:
            for department in departments:
                # make soup
                dept_url = 'https://fac-eval.lafayette.edu/fetch/' + str(year) + str(semmester) + '/' + department
                soup = BeautifulSoup(br.open(dept_url).read(), 'html5lib')

                for tag in soup.find_all(class_ = 'topic_link_group_link'):

                    # visit page and make soup
                    course_url = 'https://fac-eval.lafayette.edu' + tag['href']
                    if( (str(course_url) == 'https://fac-eval.lafayette.edu/evals/view/58a4aab454666c0ffb2d40b2') or (str(course_url) == 'https://fac-eval.lafayette.edu/evals/view/58a4aab454666c0ffb2d40b1')):
                        break
                    eval_soup = BeautifulSoup(br.open(course_url), 'html5lib')

                    # setup new evaluation
                    evaluation = Evaluation()

                    # year
                    evaluation.year = year

                    # semmester
                    evaluation.semmester = semmester

                    # course and section
                    raw_course = eval_soup.find_all(href = '#')[0].get_text()
                    try:
                        course, section = raw_course.replace(department + ' ', '').split("-")
                    except ValueError:
                        course, section = raw_course.replace(department + ' ', '').split(" ")
                    evaluation.course = course

                    # section
                    evaluation.section = section

                    # dept
                    evaluation.dept = department

                    # professor
                    raw_heading = eval_soup.find_all(class_ = 'page_heading')[0].get_text()
                    full_name = raw_heading.replace(raw_course, '')[1:]
                    try:
                        evaluation.professor = full_name[:full_name.index(",")]
                    except ValueError:
                        break

                    # responses
                    temp_soup = eval_soup.find(text='What grade do you expect in this course? ')
                    try:
                        responses_div = temp_soup.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
                    except AttributeError:
                        break
                    evaluation.responses = responses_div.find_all(class_ = 'statistics_callout_figure')[0].get_text()

                    # grades
                    evaluation.set_grades(get_question_data('What grade do you expect in this course? ',eval_soup))

                    # effectiveness
                    evaluation.set_effectiveness(get_question_data('The instructor\'s effectiveness in teaching the subject matter was: ',eval_soup))

                    # uniqueify
                    evaluation.uniqueify()

                    #print(evaluation)
                    session = Session()
                    session.add(evaluation)
                    try:
                        session.commit()
                    except sqlalch.exc.IntegrityError:
                        print("already there bud")
