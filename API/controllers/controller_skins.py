from flask import jsonify, request
import json
from models.models import *

def get_skins_available():
    try:
        # Obtener todas las filas de la colección skins
        available_skins = list(skins.find({}, {'_id': 0}))

        return jsonify({"skins": available_skins}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def add_skins_to_db(skins_data):

    # Insert skins into the collection
    skins.insert_many(skins_data)

    return "Skins added successfully!"

def add_skins():
    try:
        # Check if the request contains a JSON file
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        skins_data = json.load(file)

        result = add_skins_to_db(skins_data)

        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
