from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():

	db = connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT username FROM User')
	results_username = cur.fetchall()
    
	return render_template("index.html", test=results_username)