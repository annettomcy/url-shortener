from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    #to safely pass messages for flash
    app.secret_key = 'h242nr2j42j32332321wd'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app