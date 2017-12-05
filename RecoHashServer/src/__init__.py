#!flask/bin/python
from flask import Flask
from flask import request

import os, shutil
from dominate.tags import base
from flask import send_file, redirect, url_for, render_template, make_response

from flask_cors import CORS, cross_origin
from PIL import Image
from io import StringIO, BytesIO
import numpy as np
import pathlib


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:\\RecoHash\\RecoHashServer\\src\\imlocal\\'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:8080/"}})
model1 = None
model2 = None

@app.route('/')
def index():
    global model1, model2
    if model1 == None and model2 == None:
        import vggobject as vgg
        import resnetscene as resnet
        model1 = vgg
        model2 = resnet
    return "Hello, World!"


@app.route('/upload', methods=['POST', 'GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def upload():
    global model1, model2
    if request.method == 'POST':
        print('In upload now!')
        img = request.files['uploads[]']#.filename
        #print(img)
        #new_file_path = url_for('static', filename=img.filename)
        #print(new_file_path)
        new_file_path = app.config['UPLOAD_FOLDER'] + img.filename
        print(new_file_path)
        #windows_path = pathlib.Path(new_file_path).as_uri()
        img.save(new_file_path)
        insta_dict = {}
        twitter_list = list()
        if model1 == None and model2 == None:
            import vggobject as vgg
            import resnetscene as resnet
            model1 = vgg
            model2 = resnet
        import hashtag_synonyms as lemma
        import fetch_social_tags as social
        vgglist, is_face_present =  model1.predict(new_file_path)
        resnetresult = model2.predict(new_file_path)
        lemma_list = lemma.word_lemmas(vgglist[0])
        if len(resnetresult)> 0:
            lemma_list += lemma.word_lemmas(resnetresult[0])
        for tag in lemma_list:
            insta_dict = social.insta_hashtags(tag)
            twitter_list += social.tweet_hashtags(tag, insta_dict)
        #DEBUGGING
        print("Lemma list")
        for lemma in lemma_list:
            print(lemma+' ')
        print("Hashtag list")
        for hashtag in twitter_list:
            print(hashtag+' ')
        new_string = ""
        #new_string_2 = ""
        for i in twitter_list:
            new_string += '#' + i + ' '
        #for i in resnetresult:
         #   new_string_2 += i
        print(new_string)
    template = render_template('result.html', new_string = new_string)
    with open('result.html', 'w') as result_html:
        result_html.write(template)
    print('File written')
    shutil.copy('result.html', 'D:\\apache-tomcat-8.5.20\\webapps\\Server1\\views')
    print('File copied')
    #return template
    return redirect('http://localhost:8080/Server1/views/result.html')
        #return render_template('result.html', new_string = new_string)
        



@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response
            
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')