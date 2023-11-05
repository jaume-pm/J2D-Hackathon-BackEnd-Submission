from controllers.controller_skins import *

def routes_skins(app):
    app.route("/skins/available", methods=['GET'])(get_skins_available)
    # app.route("/skins/buy", methods=['POST'])()
    app.route("/skins/myskins", methods=['GET'])(get_user_skins_info)
    app.route("/skins/color", methods=['PUT'])(change_skin_color)
    app.route("/skins/delete/<skin_id>", methods=['DELETE'])(sell_skin)
    app.route("/skin/getskin/<skin_id>", methods=['GET'])(get_skin_info)
    app.route('/add_skins', methods=['POST'])(add_skins)
    