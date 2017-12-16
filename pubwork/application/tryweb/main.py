# coding = UTF-8

import re
import os
from flask_cors import CORS
from flask import Flask, send_file
from dist.views import myapp, login_manager
from dist.models import UPLOAD_FOLDER

SECRET_KEY = 'Another random secret key'

app = Flask(__name__)
CORS(app)
app.register_blueprint(myapp)
app.secret_key = 'hard to guset'  # Change this!
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

login_manager.init_app(app)

app.run(debug=True,use_reloader=False,port=80)