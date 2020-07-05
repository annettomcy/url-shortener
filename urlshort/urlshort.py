from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

#Took app creation code from here to init.py to facilitate blueprints
bp = Blueprint('urlshort',__name__)


@bp.route('/')
def home():
    #render template to show html page here, from templates folder
    return render_template('home.html', codes=session.keys())

#routes only allow get, we have to explicitly specify other methods
@bp.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={}
        #when user fills the form we want to first check if it is a file or a url
        #checking for duplicate keys or else it will overwrite the url in urls.json
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                #loaded the urls.json file into urls
                urls = json.load(urls_file)

        #checking if entered shortener is in the keys
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/annet/Desktop/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        #only move on if it works, if so create a urls.json file and add the urls dictionary into it
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            #saving to cookie
            session[request.form['code']] = True
        #using jinja to pass variable code, this is a get request and as seen in url, variable code has the value we need
        return render_template('your_url.html', code=request.form['code'])
        #we use .args for get and .form for post
    else:
    #anyone using get will be sent to home page
        #name of function in url_for
        return redirect(url_for('urlshort.home'))

#look for any string after / and put it in code
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                #to check if url or file
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
#now when the user puts/theirshortname they will be redirected to their url
                else:
                    return redirect(url_for('static',filename='user_files/' + urls[code]['file']))
    #error message
    return abort(404)

#custom error page
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    #jsonify takes any list or dictionary and changes it into json
    return jsonify(list(session.keys()))