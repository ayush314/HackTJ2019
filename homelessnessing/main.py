from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import json
from werkzeug.utils import secure_filename
import os, sys


UPLOAD_FOLDER = 'D:/python/flask/homelessnessing/uploads'
okay_ext = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#DONE
#Check if there's an extension, and if it's valid
def file_okay(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in okay_ext

#DONE
#Home
@app.route('/')
def root():
	return render_template('home.html') #FIX THIS AFTER TESTING LOGIN - send home.html
	
#DONE
#Return the homeless-side info page
@app.route('/homeless_info')
def homeless_info():
	return render_template('homeless.html')

#GET, POST - Return the audio submit page
#POST - Receive the uploaded audio file
@app.route('/postaudio', methods=['GET', 'POST'])
def post_audio():
	if request.method == 'POST':
		if 'file' not in request.files:
			return render_template('audio.html', error='No file')
			
		file = request.files['file']
		
		if file.filename == '':
			return render_template('audio.html', error='No selected file')
			
		if file and file_okay(file):
			good_filename = secure_filename(file.filename)
			
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
		#Ayush voice to text part
		requester_name = #Ayush part
		
		keyword = #Ayush part
		return render_template('upload_audio.html', success='okay')
	else:
		return render_template('upload_audio.html')

#DONE
#Send the donor-side information page
@app.route('/donor_info')
def donor_info():
	return render_template('info.html')
	
#Getting form data works
#TODO make the database query
#Donor login page
@app.route('/donor_login', methods=['GET', 'POST'])
def donor_login():
	if request.method == 'POST':
		username = request.form.get('username', '')
		password = request.form.get('password', '')
		
		#database magic
		
		return render_template('home.html')
	
	
if __name__ == '__main__':
    app.run(debug=True)
	
#<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	
#TODO
