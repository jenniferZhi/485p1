from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods = ['GET', 'POST'])
def pic_route():
	
	if request.method != 'POST' and request.method !='GET':
		return abort(404)
	
	picid = request.args.get('picid', 'default_value')
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT * FROM Photo WHERE picid='%s'" %picid)
	results_search_photo = cur.fetchall()
	flag = 0
	for item in results_search_photo:
		if item['picid'] == picid:
			flag = 1
	if flag == 0:
		return abort(404)

	test_picid = request.args.get('picid', 'default_value')

	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT * FROM Contain WHERE picid='%s'" %test_picid)
	results_search = cur.fetchall()
	
	cur.execute("SELECT * FROM Photo WHERE picid='%s'" %test_picid)
	results_photo = cur.fetchall()
	format = results_photo[0]['format'] 

	test_albumid = results_search[0]['albumid']

	cur.execute("SELECT * FROM Contain WHERE albumid='%s'" %test_albumid)
	test_contain_selected = cur.fetchall()

	return render_template('pic.html', albumid = test_albumid, picid =test_picid, format = format, Contain = test_contain_selected)

