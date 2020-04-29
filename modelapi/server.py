import os

from flask import Flask
from flask_restful import Api
from api_errors import api_errors

app = Flask(__name__)
api = Api(app, prefix='/api', errors=api_errors)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['PROPOGATE_EXCEPTIONS'] = True


@app.after_request
def add_cors(response):
    """Set CORS headers for each request. All domains are allowed in debug mode."""
    CORS_DOMAIN = "*" if os.environ.get('FLASK_DEBUG') else os.environ.get('FRONTEND_BASE_URL')
    response.headers.add('Access-Control-Allow-Origin', CORS_DOMAIN)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Max-Age', 86400)
    return response

# avoid circularity
import endpoints

api.add_resource(endpoints.Model, '/model')
