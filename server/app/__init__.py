from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Needed to send/receive http requests instead of https to localhost

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')