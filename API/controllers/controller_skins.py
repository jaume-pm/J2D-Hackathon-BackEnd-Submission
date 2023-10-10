from flask import jsonify, request
from models.models import *

def get_skins_available():
    try:
        # Obtener todas las filas de la colección skins
        available_skins = list(skins.find({}, {'_id': 0}))

        return jsonify({"skins": available_skins}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500