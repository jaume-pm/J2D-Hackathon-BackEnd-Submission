from controllers.controller_skins import *

def routes_skins(app):
    app.route("/skins/available", methods=['GET'])(get_skins_available)
    # app.route("/skins/buy", methods=['POST'])()
    # app.route("/skins/myskins", methods=['GET'])()
    # app.route("/skins/color", methods=['PUT'])()
    # app.route("/skins/delete/{id}", methods=['DELETE'])()
    # app.route("/skin/getskin/{id}", methods=['GET'])()
    app.route('/add_skins', methods=['POST'])(add_skins)

