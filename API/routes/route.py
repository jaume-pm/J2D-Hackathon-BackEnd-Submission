from controllers.controller_skins import *

def routes_skins(app):
    app.route("/skins/available", methods=['GET'])(get_skins_available)