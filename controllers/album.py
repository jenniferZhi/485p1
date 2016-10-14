from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
import hashlib
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

def picidCreated(albumid, filename):
	m = hashlib.md5()
	m.update(str(albumid))
	m.update(filename)
	return m.hexdigest()

ALLOWED_EXTENSIONS = set(['png','jpg','bmp','gif'])

def allowed_file(filename):
   	return '.' in filename and \
   		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




album = Blueprint('album', __name__, template_folder='templates')

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	options = {
		"edit": True
	}
	if request.method != 'POST' and request.method !='GET':
			return abort(404)
	db = connect_to_database()
	cur = db.cursor()
	
	if request.method == 'GET':
		test_albumid = request.args.get('albumid', 'default_value')

		cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
		results_search_album = cur.fetchall()
		flag = 0
		for item in results_search_album:
			if item['albumid'] == int(test_albumid):
				flag = 1
		if flag == 0:
			return abort(404) 
	
	elif request.method == 'POST':
		op = request.form.get('op', 'default_value')
		test_albumid = request.form.get('albumid', 'default_value')
		test_picid = request.form.get('picid', 'default_value')
		if op == 'add':
			if 'file' not in request.files:
				return redirect(request.url)
			file = request.files['file']

			if file.filename == '':
				return redirect(request.url)

			if file and allowed_file(file.filename):
				
				filename = secure_filename(file.filename)
				fileformat = os.path.splitext(filename)[1]	
				fileformat = fileformat[1:]
				

				picid = picidCreated(test_albumid, filename)

				cur.execute("SELECT MAX(sequencenum) FROM Contain")
				sequencenum = cur.fetchall()
				sequencenum = sequencenum[0]['MAX(sequencenum)']
				sequencenum = int(sequencenum) + 1

				cur.execute("INSERT INTO Photo (picid, format) VALUES ('%s', '%s')" %(picid, fileformat))
				cur.execute("INSERT INTO Contain (sequencenum, albumid, picid) VALUES ('%d','%s', '%s')" %(long(sequencenum), test_albumid, picid))

				filename = picid+'.'+fileformat

				file.save(os.path.join('./static/images/', filename))

		elif op == 'delete':
	
			cur.execute("SELECT format FROM Photo WHERE picid='"+test_picid+"'")
			formats = cur.fetchall()
			picformat = formats[0]['format']
		
			cur.execute("DELETE FROM Photo WHERE picid='%s'" %test_picid)
			fname = test_picid+'.'+picformat
			os.system("cd static/images && rm '%s'" %fname)

	cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
	results_album = cur.fetchall()
	test_title = results_album[0]['title']

	cur.execute("SELECT * FROM Contain WHERE albumid='%s'" %test_albumid)
	results_contain = cur.fetchall()
	
	cur.execute("SELECT * FROM Photo WHERE picid IN (SELECT picid FROM Contain WHERE albumid = '"+test_albumid+"')")
	results_photo = cur.fetchall()
	
	return render_template('album.html', album_title = test_title, albumid = long(test_albumid), Photo = results_photo, **options)

@album.route('/album', methods = ['GET', 'POST'])
def album_route():
	options = {
		"edit": False
	}
	if request.method != 'POST' and request.method !='GET':
		return abort(404)
	test_albumid = request.args.get('albumid', 'default_value')
	
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
	results_search_album = cur.fetchall()
	flag = 0
	for item in results_search_album:
		if item['albumid'] == int(test_albumid):
			flag = 1
	if flag == 0:
		return abort(404) 


	dbSearch = connect_to_database()
	curSearch = dbSearch.cursor()
	curSearch.execute("SELECT title FROM Album WHERE albumid='%s'" %test_albumid)
	results_title = curSearch.fetchall()

	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT * FROM Contain WHERE albumid = '%s'" %test_albumid)
	results_contain = cur.fetchall()

	cur.execute("SELECT * FROM Photo WHERE picid IN (SELECT picid FROM Contain WHERE albumid = '"+test_albumid+"')")
	results_photo = cur.fetchall()

	return render_template('album.html', album_title = results_title[0]['title'],albumid = test_albumid, Photo = results_photo, **options)

