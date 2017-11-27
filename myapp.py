from flask import Flask, url_for, request, make_response, escape, session, redirect
import requests
from flask import render_template
import json
import time
import datetime
import arrow


BASE_URL = 'http://www.peanutslog.com'


app = Flask(__name__)
app.secret_key = 'jflsdjfldsjflsdjflksdjflksdjflkdsj'

@app.route('/')
def index():
	if 'user_token' in session:
		return render_template('edit.html', logged_in=True)
	else:
		return render_template('edit.html', logged_in=False)


@app.route('/user/login', methods=['POST'])
def userLogin():
	phone = request.form['phone']
	password = request.form['password']
	param = {'u': phone, 'p': password, 't': 1}
	r = requests.post(BASE_URL + '/Iosapi/User/login', data=param)
	j = json.loads(r.text)
	if j['rcode'] == 200:
		session['user_token'] = j['ftoken']
		session['user_info'] =  {'name':j['udata']['name'], 'avatar':j['udata']['avatar']}
		return redirect(url_for('index'))
		# return render_template('edit.html', logged_in=True)
		# return json.dumps({"code":200, 'html':render_template('edit.html', logged_in=True), 'msg':'logged in', 'info':{'name':j['udata']['name'], 'avatar':j['udata']['avatar']}})
	else:
		session.pop('user_token', None)
		session.pop('user_info', None)
		return redirect(url_for('index'))
		# return render_template('edit.html', logged_in=False)
		# return json.dumps({"code":400, 'html':'', 'msg':'password or phone error', 'info':{}})


@app.route('/user/info/', methods=['POST', 'GET'])
def userInfo():
	if 'user_info' in session:
		return json.dumps(session['user_info'])
	else:
		return ''

@app.route('/user/logout/')
def logout():
    session.pop('user_token', None)
    return redirect(url_for('index'))
    # return render_template('edit.html', logged_in=False)

@app.route('/diary/publish/', methods=['POST'])
def publisDiary():
	text = request.form['content']
	html = request.form['html_content']
	now = arrow.now()
	param = [{'weatherTime':now.format('YYYY-MM-DD'),
			 'tag_time_stamp': now.timestamp,
			 'encn': '1',
			 'tag_time': now.format('YYYYMMDDHHmmss'),
			 'week': now.format('d'),
			 'address': '',
			 'time': now.format('HH:mm'),
			 'enorcn': '',
			 'photoTime': now.format('YYYY-MM-DD HH:mm:ss'),
			 'facilities': '',
			 'latitude': '39.956259,116.316232',
			 'scale': '',
			 'timeslot': '3',
			 'sticker': '',
			 'childIds': '',
			 'map_private': '1',
			 'city': '',
			 'weather': '1454',
			 'tagid': '240707',
			 'gid': '',
			 'minTem': '1',
			 'sid': '',
			 'maxTem': '10',
			 'title': '',
			 'introduction': text,
			 'introduction_html': html,
			 'show_time': '1',
			 'type': '3',
			 'img': '',
			 'star': '0',
			 'guid': '',
			 'star_2': '',
			 'tagid_2': '',
			 'tag_time_stamp_2': '',
			 'id': '',
			 'photoIds': '',
			 'saveTitle': '1',
			 'time_diff': '28800',
			 't_id': '',
			 'm_id': '',
			 'e_id': '',
			 }]

	data = {'data': json.dumps(param), 'ft': session['user_token'], 'save_title': '1', 'version': '40200'}
	r = requests.post(BASE_URL + '/Iosapi/Photos/addContent', data=data)
	return r.text



if __name__ == '__main__':
	app.debug = True
	app.run()