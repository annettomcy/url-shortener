from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
#to safely pass messages for flash
app.secret_key = 'h242nr2j42j32332321wd'
@app.route('/')
def home():
    #render template to show html page here, from templates folder
    return render_template('home.html')

#routes only allow get, we have to explicitly specify other methods
@app.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={}
        #when user fills the form we wnt to first check if it is a file or a url
        #checking for duplicate keys or else it will overwrite the url in urls.jon
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                #loaded the urls.json file into urls
                urls = json.load(urls_file)

        #checking if entered shortener is in the keys
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/annet/Desktop/url-shortener/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        #only move on if it works, if so create a urls.json file and add the urls dictionary into it
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
        #using jinja to pass variable code, this is a get request and as seen in url, variable code has the value we need
        return render_template('your_url.html', code=request.form['code'])
        #we use .args for get and .form for post
    else:
    #anyone using get will be sent to home page
        #name of function in url_for
        return redirect(url_for('home'))
