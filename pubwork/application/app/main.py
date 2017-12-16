# coding = UTF-8

import re
import os
from flask import Flask, send_file
from dist.views import myapp, login_manager

SECRET_KEY = 'Another random secret key'

app = Flask(__name__)
app.register_blueprint(myapp)
app.secret_key = 'hard to guset'  # Change this!

login_manager.init_app(app)

app.run(debug=True,use_reloader=False,port=80)