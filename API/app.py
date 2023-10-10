from flask import Flask
from routes.route import *


app = Flask(__name__)

routes_skins(app)