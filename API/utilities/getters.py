from flask import jsonify, request
from bson import ObjectId

class ValidationError(Exception):
    pass

def get_skin_id(json_data):
    skin_id = json_data.get("skin_id")
    if not skin_id:
        raise ValidationError("Skin ID not provided")
    return ObjectId(skin_id)

def get_skin_name(json_data):
    name = json_data.get("name")
    if not name:
        raise ValidationError("Skin name not provided")
    return name

def get_skin_price(json_data):
    price = json_data.get("price")
    if not price:
        raise ValidationError("Skin price not provided")
    return price

def get_skin_color(json_data):
    color = json_data.get("color")
    if not color:
        raise ValidationError("Skin color not provided")
    return color

def get_skin_rarity(json_data):
    rarity = json_data.get("rarity")
    if not rarity:
        raise ValidationError("Skin rarity not provided")
    return rarity

def get_user_id(json_data):
    user_id = json_data.get("user_id")
    if not user_id:
        raise ValidationError("User ID not provided")
    return ObjectId(user_id)

def get_username(json_data):
    username = json_data.get("username")
    if not username:
        raise ValidationError("Username not provided")
    return username

def get_email(json_data):
    email = json_data.get("email")
    if not email:
        raise ValidationError("Email not provided")
    return email

def get_password(json_data):
    password = json_data.get("password")
    if not password:
        raise ValidationError("Password not provided")
    return password

def get_balance(json_data):
    balance = json_data.get("balance")
    if balance is None:
        raise ValidationError("Balance not provided")
    return balance

def get_owned_skins(json_data):
    owned_skins = json_data.get("owned_skins", [])
    if not isinstance(owned_skins, list):
        raise ValidationError("Invalid format for owned_skins")
    return owned_skins
