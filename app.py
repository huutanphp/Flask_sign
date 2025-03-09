# Importing required functions 
from flask import Flask, request, render_template
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pypasser import reCaptchaV3
from bs4 import BeautifulSoup
import requests, re, random, string, base64, urllib.parse, json, time, os, sys, shutil, uuid, glob
import os.path

def resign(sellect,p12,password,mobileprovision,identifier='',name=''):
    session = requests.Session()
    res = session.get("https://sign.codevn.net")
    cookies = res.cookies['PHPSESSID']
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    token = soup.find('input', {'name': 'upload_token'}).get('value')
    url = 'https://sign.codevn.net/sign.php'
    #captcha = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcYo6AUAAAAAFjddWYMFHT4jG4bpH05zZWyNOKq&co=aHR0cHM6Ly9zaWduLmNvZGV2bi5uZXQ6NDQz&hl=en&v=zIriijn3uj5Vpknvt_LnfNbF&size=invisible&cb=7f2fvqmrk7v3'
    recaptcha_response = reCaptchaV3("https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcYo6AUAAAAAFjddWYMFHT4jG4bpH05zZWyNOKq&co=aHR0cHM6Ly9zaWduLmNvZGV2bi5uZXQ6NDQz&hl=en&v=zIriijn3uj5Vpknvt_LnfNbF&size=invisible&cb=t4ukpfmb9p2n")
    boundary = '----WebKitFormBoundary' \
                    + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    multipart_data = MultipartEncoder(
        fields={
            # plain text fields
            'sellect': sellect,
            'p12': (p12, open(p12, 'rb'), 'application/x-pkcs12'),
            'password': password,
            'mobileprovision':  (mobileprovision, open(mobileprovision, 'rb'), 'application/x-apple-aspen-mobileprovision'),
            'identifier': '',
            'name': '',
            'upload_token': token,#token,
            'recaptcha_response': recaptcha_response 
        }, boundary=boundary
    )
    headers = {
        'Host': 'sign.codevn.net',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'vi-VN,vi;q=0.9',
        'Origin': 'https://sign.codevn.net',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/125.0.6422.145 Mobile/15E148 Safari/604.1',
        'Connection': 'keep-alive',
        'Referer': 'https://sign.codevn.net/',
        'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
        'Cookie': f'PHPSESSID={cookies}'#res.cookies['PHPSESSID'],
    }
    response = session.post(url,
                             data=multipart_data,
                             headers=headers)

    return response.text
def create_link(content):
    id_sign = content.split("ipa=")[1].split('"')[0]
    link = f'itms-services://?action=download-manifest&url=https://sign.codevn.net/data/{id_sign}/codevndotnet.plist'
    headers = {
	    'Host': 'tinyurl.com',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
	    'Accept-Language': 'vi-VN,vi;q=0.9',
	    'Connection': 'keep-alive',
    }
    res = requests.get(f'https://tinyurl.com/api-create.php?url={link}', headers=headers)
    #response = requests.get(f'https://tinyurl.com/api-create.php?url={url}, headers=headers')
    return res.text

def isReadableFile(file_path, file_name):
    full_path = file_path + "/" + file_name
    try:
        if not os.path.exists(file_path):
            print("File path is invalid.")
            return False
        elif not os.path.isfile(full_path):
            print ("File does not exist.")
            return False
        elif not os.access(full_path, os.R_OK):
            print ("File cannot be read.")
            return False
        else:
            return True
    except IOError as ex:
        print ("I/O error({0}): {1}".format(ex.errno, ex.strerror))
    except Error as ex:
        print ("Error({0}): {1}".format(ex.errno, ex.strerror))
    return False

# Flask constructor 
app = Flask(__name__, template_folder='') 

# Root endpoint 
@app.route('/', methods=['GET']) 
def index(): 
	## Display the HTML form template 
	return render_template('index.html') 

# `read-form` endpoint 
@app.route('/read-form', methods=['POST']) 
def read_form(): 
	APP_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))
	print(APP_ROOT)
	sys.exit()
	filenames = str(uuid.uuid4().hex)[:8]
	target = os.path.join(APP_ROOT, 'tmp/'+filenames)
	if not os.path.isdir(target):
		os.mkdir(target)
	else:
		print("Could create upload directory: {}".format(target))
	print(request.files.getlist("file"))
	# Get the form data as Python ImmutableDict datatype 
	#for upload in re
	#s.filename	
	for file_sellect in request.files.getlist("ipa"):
		if file_sellect.filename != '':
			file_sellect.save(target +'/'+ file_sellect.filename)
	p12 = request.files.getlist("p12")
	mobileprovision = request.files.getlist("mobileprovision")
	data = request.form
	#select_file =  
	for file_p12 in p12:
		#print(file)
		file_p12.save(target +'/'+ file_p12.filename)
	p12_path = file_p12.filename
	for mov_file in mobileprovision:
		mov_file.save(target +'/'+ mov_file.filename)
	mov_path = mov_file.filename
	#all_file = glob.glob(target+'/*.mobileprovision')
	p12_check = isReadableFile(target, p12_path)
	mov_check = isReadableFile(target, mov_path)
	time.sleep(2)
	#print(target)
	if p12_check == True and mov_check == True:
		ipa_sign = resign(data['sellect'],target+'/'+p12_path,data['password'],target+'/'+mov_path)
		id_sign = ipa_sign.split("ipa=")[1].split('"')[0]
		if id_sign:
			result = create_link(ipa_sign)
		return result
	#file = glob.glob(target+'/*.ipa')
	#if file:
	#	data['sellect'] = file[0]
	#else:
	#	data['sellect']  = data['sellect']
	#return data['sellect']
	## Return the extracted information 
	#ipa_sign = resign(data['sellect'],all_file[0],data['password'],all_file[1])
	#id_sign = ipa_sign.split("ipa=")[1].split('"')[0]
	#if id_sign:
	#	result = create_link(ipa_sign)
	#else:
	#	result = ipa_sign
	#return ipa_sign
	#return p12_path
	

# Main Driver Function 
if __name__ == '__main__': 
	# Run the application on the local development server 
	app.run(debug=True)


