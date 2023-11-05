import json
from flask import jsonify, request
from bson.objectid import ObjectId
from models.models import *  # Importing necessary models
from utilities.getters import *  # Importing custom getter functions
from utilities.economy import *

def get_skins_available():
    try:
        # Retrieve available skins from the MongoDB collection
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
    try:
        # Retrieve user ID from the JSON data in the request
        json_data = request.get_json()
        user_id = get_user_id(json_data)

        # Find the user in the MongoDB collection
        user = users.find_one({"_id": user_id})

        # Return an error response if the user is not found
        if not user:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

        # Extract information about skins owned by the user
        user_owned_skins = user.get("owned_skins", [])
        user_skin_info = []

        for owned_skin in user_owned_skins:
            skin_id = owned_skin.get("skin_id")
            skin = skins.find_one({"_id": skin_id})
            
            # Add skin information to the user_skin_info list
            if skin:
                user_skin_info.append({
                    "_id": str(skin_id),
                    "name": skin.get("name"),
                    "color": owned_skin.get("color"),
                    "rarity": skin.get("rarity")
                })

        # Return the information about user-owned skins as a JSON response
        return jsonify({"result": "ok", "skins": user_skin_info}), 200

    except ValidationError as e:
        # Handle validation errors and return an error response
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500


def change_skin_color():
    try:
        # Retrieve data from the JSON data in the request
        json_data = request.get_json()
        user_id = get_user_id(json_data)
        skin_id = get_skin_id(json_data)
        color = get_skin_color(json_data)

        # Find the user in the MongoDB collection
        user = users.find_one({"_id": user_id})

        # Return an error response if the user is not found
        if not user:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404
        
        try:
            # Update the color of the specified skin for the user
            result = users.update_one(
                {'_id': user_id, 'owned_skins.skin_id': ObjectId(skin_id)},
                {'$set': {'owned_skins.$.color': color}}
            )

            # Return an error response if no matching skin is found
            if result.matched_count == 0:
                return jsonify({"error": "No matching skin found"}), 404
            else:
                # Return a success response if the operation is successful
                return jsonify({"result": "ok"}), 200

        except Exception as e:
            # Handle exceptions related to the update operation
            return jsonify({"error": f"Error updating skin color: {str(e)}"}), 500

    except ValidationError as e:
        # Handle validation errors and return an error response
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected exceptions and return an error response
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def sell_skin(skin_id):
    try:
        # Retrieve data from the JSON data in the request
        json_data = request.get_json()
        user_id = get_user_id(json_data)
        sell_price = get_sell_price(skin_id)

        # Find the user in the MongoDB collection
        user = users.find_one({"_id": user_id})

        # Return an error response if the user is not found
        if not user:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

        try:
            user_balance = user.get("balance")

            # Attempt to sell the specified skin for the user
            result = users.update_one(
                {'_id': user_id, 'owned_skins.skin_id': ObjectId(skin_id)},
                {
                    '$set': {'balance': user_balance + sell_price},
                    '$pull': {'owned_skins': {'skin_id': ObjectId(skin_id)}}
                }
            )

            # Return an error response if no matching skin is found
            if result.matched_count == 0:
                return jsonify({"error": "The user does not own the skin"}), 404
            else:
                # Return a success response if the operation is successful
                return jsonify({"result": "ok"}), 200

        except Exception as e:
            # Handle exceptions related to selling the skin
            return jsonify({"error": f"Error selling skin: {str(e)}"}), 500

    except ValidationError as e:
        # Handle validation errors and return an error response
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected exceptions and return an error response
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def get_skin_info(skin_id):
    try:
        # Find the skin with the provided ID in the MongoDB collection
        skin = skins.find_one({"_id": ObjectId(skin_id)})

        # Return an error response if the skin is not found
        if not skin:
            return jsonify({"error": f"No skin found with ID: {skin_id}"}), 404

        # Convert ObjectId to string for the "_id" field
        skin["_id"] = str(skin["_id"])

        # Return all information about the skin as a JSON response
        return jsonify({"result": "ok", "skin": skin}), 200

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500


def buy_skin():
    try:
        # Retrieve data from the JSON data in the request
        json_data = request.get_json()
        user_id = get_user_id(json_data)
        skin_id = get_skin_id(json_data)

        # Find the user in the MongoDB collection
        user = users.find_one({"_id": user_id})

        # Return an error response if the user is not found
        if not user:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

        try:
            # Check if user already owns the skin
            if any(owned_skin['skin_id'] == skin_id for owned_skin in user.get('owned_skins', [])):
                return jsonify({"error": "User already owns the skin"}), 400

            # Find the skin details in the MongoDB collection
            skin = skins.find_one({"_id": ObjectId(skin_id)})

            # Check if the user has enough balance to buy the skin
            skin_price = skin.get("price")
            user_balance = user.get("balance")
            if user_balance < skin_price:
                return jsonify({"error": "Insufficient balance"}), 400

            # Deduct the skin price from the user's balance and add the skin to owned_skins
            users.update_one(
                {"_id": user_id},
                {"$inc": {"balance": -skin_price}, "$push": {"owned_skins": {"skin_id": ObjectId(skin_id), "color": skin.get("color")}}}
            )

            # Return a success response
            return jsonify({"result": "ok"}), 200

        except Exception as e:
            # Handle exceptions related to buying the skin
            return jsonify({"error": f"Error buying skin: {str(e)}"}), 500
        
    except ValidationError as e:
        # Handle validation errors and return an error response
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected exceptions and return an error response
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
