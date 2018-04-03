import json
import string
import datetime

import dateparser
from flask import Flask
from flask import render_template
from flask import request

from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ['like', 'has gone']

def format_date(userdate):
	date = dateparser.parse(userdate)
	try:
		return datetime.datetime.strftime(date,"%Y-%d-%m")
	except TypeError:
		return None

def sanitize_string(userinput):
	whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
	return ''.join(filter(lambda x: x in whitelist, userinput))

@app.route('/')
def home(error_message=None):
	try:
		crimes = DB.get_all_crimes()
		crimes_json = json.dumps(crimes)
	except Exception as e:
		print(e)
		data = None
	return render_template('home.html',
						 	data=crimes_json,
						 	categories=categories,
						 	error_message=error_message)


@app.route('/submitplace', methods=['POST'])
def submitcrime():
	category = request.form.get("category")
	if category not in categories:
		return home()

	date = format_date(request.form.get("date"))
	if not date:
		return home("Invalid date. Please use yyyy-mm-dd format")

	try:
		latitude = float(request.form.get("latitude"))
		longitude = float(request.form.get("longitude"))
	except ValueError:
		return home()
	description = sanitize_string(request.form.get("description"))
	DB.add_crime(category, date, latitude, longitude, description)
	return home()

if __name__ == '__main__':
	app.run(debug=True,port=5000)

