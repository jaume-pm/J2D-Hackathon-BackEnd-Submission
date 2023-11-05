from flask import jsonify, request
from models.models import *  # Importing necessary models
from bson.objectid import ObjectId  # Importing ObjectId from bson module
from utilities.getters import *  # Importing custom getter functions
from utilities.economy import *

def get_skins_available():
    """
    Retrieves available skins from the MongoDB collection and returns them as a JSON response.

    Returns:
        JSON: {"result": "ok", "skins": available_skins}
    """
    try:
        # Retrieve all skins from the MongoDB collection
        available_skins = list(skins.find({}))

        # Convert ObjectId to string for each document
        for skin in available_skins:
            skin['_id'] = str(skin['_id'])

        # Return the list of available skins as a JSON response
        return jsonify({"result": "ok", "skins": available_skins}), 200

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500


def add_skins():
    """
    Adds skins to the MongoDB collection based on the provided JSON file in the request.

    Returns:
        JSON: {"result": "ok"} if successful, {"error": str(e)} if there's an error.
    """
    try:
        # Check if the request contains a JSON file
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file provided"}), 400

        # Load skins data from the provided JSON file
        file = request.files['file']
        skins_data = json.load(file)

        # Insert the skins data into the MongoDB collection
        skins.insert_many(skins_data)

        # Return a success response
        return jsonify({"result": "ok"}), 200

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500


def get_user_skins_info():
    """
    Retrieves information about skins owned by a user from the MongoDB collection.

    Returns:
        JSON: {"result": "ok", "skins": user_skin_info} if successful,
              {"error": f"No user found with ID: {user_id}"} if the user is not found,
              {"error": str(e)} if there's an error.
    """
    try:
        # Retrieve user ID from the JSON data in the request
        json_data = request.get_json()
        user_id = get_user_id(json_data)

        # Find the user in the MongoDB collection
        user = users.find_one({"_id": user_id})

        if user:
            # Extract information about skins owned by the user
            user_owned_skins = user.get("owned_skins", [])
            user_skin_info = []

            for owned_skin in user_owned_skins:
                skin_id = owned_skin.get("skin_id")
                skin = skins.find_one({"_id": skin_id})
                if skin:
                    user_skin_info.append({
                        "_id": str(skin_id),
                        "name": skin.get("name"),
                        "color": owned_skin.get("color"),
                        "rarity": skin.get("rarity")
                    })

            # Return the information about user-owned skins as a JSON response
            return jsonify({"result": "ok", "skins": user_skin_info}), 200

        else:
            # Return an error response if the user is not found
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500

def change_skin_color():
    """
    Changes the color of a skin owned by a user in the MongoDB collection.

    Returns:
        JSON: {"result": "ok"} if successful,
              {"error": "No matching skin found"} if no matching skin is found,
              {"error": str(e)} if there's an error.
    """
    try:
        # Retrieve data from the JSON data in the request
        json_data = request.get_json()
        user_id = get_user_id(json_data)
        skin_id = get_skin_id(json_data)
        color = get_skin_color(json_data)

        # Find the user in the MongoDB collection
        user = users.find_one({"_id": user_id})

        if user:
            try:
                # Update the color of the specified skin for the user
                result = users.update_one(
                    {'_id': user_id, 'owned_skins.skin': skin_id},
                    {'$set': {'owned_skins.$.color': color}}
                )

                if result.matched_count == 0:
                    # Return an error response if no matching skin is found
                    return jsonify({"error": "No matching skin found"}), 404
                else:
                    # Return a success response if the operation is successful
                    return jsonify({"result": "ok"}), 200

            except Exception as e:
                # Handle exceptions related to the update operation
                return jsonify({"error": f"Error updating skin color: {str(e)}"}), 500
        else:
            # Return an error response if the user is not found
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

    except ValidationError as e:
        # Handle validation errors and return an error response
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected exceptions and return an error response
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    

def sell_skin(skin_id):
    try:
        json_data = request.get_json()
        user_id = get_user_id(json_data)
        sell_price = get_sell_price(skin_id)

        user = users.find_one({"_id": user_id})

        if user:
            try:
                user_balance = user.get("balance")

                print(f"Attempting to sell skin_id: {skin_id} for user_id: {user_id}")

                result = users.update_one(
                    {'_id': user_id, 'owned_skins.skin': ObjectId(skin_id)},
                    {
                        '$set': {'balance': user_balance + sell_price},
                        '$pull': {'owned_skins': {'skin': ObjectId(skin_id)}}
                    }
                )

                print(f"Modified count: {result.modified_count}, Matched count: {result.matched_count}")

                if result.matched_count == 0:
                    return jsonify({"error": "The user does not own the skin"}), 404
                else:
                    return jsonify({"result": "ok"}), 200

            except Exception as e:
                return jsonify({"error": f"Error selling skin: {str(e)}"}), 500
        else:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

from bson import ObjectId
from flask import jsonify

def get_skin_info(skin_id):
    try:
        # Convert the skin_id string to ObjectId
        skin_id_obj = ObjectId(skin_id)

        # Find the skin with the provided ID
        skin = skins.find_one({"_id": skin_id_obj})

        # Check if the skin exists
        if skin:
            # Convert ObjectId to string for the "_id" field
            skin["_id"] = str(skin["_id"])

            # Return all information about the skin as a JSON response
            return jsonify({"result": "ok", "skin": skin}), 200
        else:
            # Return an error response if the skin is not found
            return jsonify({"error": f"No skin found with ID: {skin_id}"}), 404

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500

