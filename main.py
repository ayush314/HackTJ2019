from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import json
from flask import redirect
from flaskext.mysql import MySQL #pip install flask-mysql
from werkzeug.utils import secure_filename
import os, sys, random
import json
import sys
from json import dumps
from elasticsearch import Elasticsearch

UPLOAD_FOLDER = 'D:/python/flask/homelessnessing/uploads'
okay_ext = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#mysql = MySQL()

#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 's7xye920kh'
#app.config['MYSQL_DATABASE_DB'] = 'basiclogin'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)

#conn = mysql.connect()

#DONE
#Check if there's an extension, and if it's valid
def file_okay(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in okay_ext

#DONE
#Check with the database if an email/password entry exists
'''
def verify_acc(email, password):
	
	cursor = conn.cursor()
	args = [email, password]
	cursor.callproc('getacc', args)

	res = cursor.fetchall()
	# print(email, password)
	print(res)
	return len(res) == 0
'''	
#DONE
#Home
@app.route('/')
def root():
	return render_template('About-Contact/startbootstrap-new-age-gh-pages/About-Contact.html')
	
#DONE
#Return the homeless-side info page
@app.route('/homeless_info')
def homeless_info():
	return render_template('homeless.html')


#Getting form data works
#DONE with sql
#Donor login page
@app.route('/donor_login', methods=['GET', 'POST'])
def donor_login():
    '''	if request.method == 'POST':
	#do some safe stuff here to make mal-stuff impossible
		username = request.form.get('username', '')
		password = request.form.get('password', '')
		email = request.form.get('email', '')
		
		if (verify_acc(email, password)):
			return redirect('/home_apparel')
		else:
			return render_template('/donor_login.html', failure='1')
		
	else:
    '''
    return redirect('/home_apparel')
		
def genRandomID():
	return random.randint(0, 100000000)
	
#DONE sql
#register a donor with values
@app.route('/donor_register', methods=['GET', 'POST'])
def donor_register():
    '''	if request.method == 'POST':
		username = request.form.get('username', '')
		password = request.form.get('password', '')
		email = request.form.get('email', '')

		cursor = conn.cursor()
		args = [username, password, email, str(genRandomID()), 0]
		cursor.callproc('register', args)
		
		print(args)
		return redirect('/home_apparel')
	else:
    '''
    return redirect('donor_register.html')
	
#DONE except for elastic
#New URL for accepting text & request from hardware
@app.route('/post_req', methods=['POST'])
def post_req():
  json = request.get_json()
  req_text = json['text']

  #if blank
  if (not req_text or req_text.strip() == ''):
    return jsonify({success: 'Error: No text'})

  #do magic with elastic - make entry into database

  return jsonify({success: 'Success!'})


@app.route('/send_test', methods=['POST','GET'])
def send_test():
    if request.method == 'POST':
        

        def indexRecord(record):
            es = Elasticsearch("10.150.0.5:9200")
            es.index(index="homelesdata",
                     doc_type="doc",
                     body=dumps(record))

        location = "Washington D.C."
        text = request.values['text']

        record = {"location": location, "text": text, "isAddressed": False}
        indexRecord(record)
        
        return "Welcome to the bullshit"
        render_template('About-Contact/startbootstrap-new-age-gh-pages/About-Contact.html')
    else:
        render_template('About-Contact/startbootstrap-new-age-gh-pages/About-Contact.html')
    
@app.route('/get_data_res', methods=['GET', 'POST'])
def get_data_res():
    tquery = request.args.get('other', '')
    if (tquery == ''):
        gquery = request.args.get('query', '')
        return render_template('HomePage/startbootstrap-shop-homepage-gh-pages/Data_Dump.html', query=gquery)
    else:
        es = Elasticsearch("10.150.0.5:9200")

        searchQuery = request.args.get('query', '')
        locations = []

        locations.append("Washington D.C.")

        body = {
                "query": {
                        "bool": {
                                "must": {
                                        "match": {
                                                "text": searchQuery
                                        }
                                },
                                "filter": {
                                    "bool": {
                                        "must" : [
                                                 { "terms" : {"location.keyword": locations}},
                                                 { "term" : {"isAddressed": False}}
                                              ]
                                    }
                                }
                        }
                }
        }
    
        res = es.search(index="homelesdata", body=body)
        print("Got %d hits:" % res['hits']['total'])
        val = []
        for hit in res['hits']['hits']:
            print(hit["_source"])
            val.append(jsonify(hit["_source"]))

        return val

@app.route('/home_apparel')
def home_apparel(): 
	return render_template('HomePage/startbootstrap-shop-homepage-gh-pages/Home-Apparel.html')
	
@app.route('/home_food')
def home_food(): 
	return render_template('HomePage/startbootstrap-shop-homepage-gh-pages/Home-Food.html')

@app.route('/home_misc')
def home_misc(): 
	return render_template('HomePage/startbootstrap-shop-homepage-gh-pages/Home-Miscellaneous.html')

@app.route('/get_info')
def get_info():
	return jsonify({'val': [['Apple', 'Rick', '5']]})
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)	

#<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	
#TODO
'''
For Sujay: sending the request from the hardware

#must use pip or some dragonboard magic to make things work
import requests 

#get audio file

#do ayush's magic - parse audio to text

_url = http://domain.com.domain.com.com/post_req
_params = {
  id: [id]
  text: [text]
  addressed: false
  user: ''
}

res = requests.get(url = _url, params = _params)

# print(res)

Ajax request/post requests:
Dragonboard (requests) -> Flask: as above
Frontend (donors: login) -> Flask: form
Frontend (donors: register) -> Flask: form
Frontend (donors: after login: get stuff) -> Flask:
$.ajax({
  type: 'POST',
  url: '\get_info',
  data: {email: getEmailFromCookies(), password: getPasswordFromCookies()}
  success: (data) => {
    document.write(data);
    /* format data into css */
  }
});
'''
