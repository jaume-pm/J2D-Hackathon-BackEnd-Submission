from bson.objectid import ObjectId
from models.models import skins

# Constant percentage for calculating the sell price
SELL_PERCENTAGE = 0.6  # 60%

def get_sell_price(skin_id_str):
    """
    Calculate the sell price of a skin based on the constant percentage and the skin's price.

    Args:
        skin_id_str (str): The string representation of the ObjectId of the skin.

    Returns:
        float: The calculated sell price.
    """
    try:
        # Convert the string representation of ObjectId to ObjectId
        skin_id = ObjectId(skin_id_str)

        # Find the skin in the MongoDB collection
        skin = skins.find_one({"_id": skin_id})

        if not skin:
            raise ValueError("Skin not found")

        # Get the price from the skin document
        price = skin.get("price", 0.0)

        # Calculate the sell price
        sell_price = price * SELL_PERCENTAGE

        return sell_price

    except ValueError as ve:
        # Handle the case where the skin is not found or price is not a valid float
        raise ve
