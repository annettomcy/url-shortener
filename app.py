from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    #render template to show html page here, from templates folder
    return render_template('home.html')

#routes only allow get, we have to explicitly specify other methods
@app.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
    #using jinja to pass variable code, this is a get request and as seen in url, variable code has the value we need
        return render_template('your_url.html', code=request.form['code'])
    #we use .args for get and .form for post
    else:
    #anyone using get will be sent to home page
        return redirect('/')
