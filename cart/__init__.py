# import json

# import products
# from cart import dao
# from products import Product


# class Cart:
#     def __init__(self, id: int, username: str, contents: list[Product], cost: float):
#         self.id = id
#         self.username = username
#         self.contents = contents
#         self.cost = cost

#     def load(data):
#         return Cart(data['id'], data['username'], data['contents'], data['cost'])


# def get_cart(username: str) -> list:
#     cart_details = dao.get_cart(username)
#     if cart_details is None:
#         return []
    
#     items = []
#     for cart_detail in cart_details:
#         contents = cart_detail['contents']
#         evaluated_contents = eval(contents)  
#         for content in evaluated_contents:
#             items.append(content)
    
#     i2 = []
#     for i in items:
#         temp_product = products.get_product(i)
#         i2.append(temp_product)
#     return i2

    


# def add_to_cart(username: str, product_id: int):
#     dao.add_to_cart(username, product_id)


# def remove_from_cart(username: str, product_id: int):
#     dao.remove_from_cart(username, product_id)

# def delete_cart(username: str):
#     dao.delete_cart(username)




import json
import products
from cart import dao
from products import Product
from flask_caching import Cache

# Initialize Flask-Caching
cache = Cache(config={'CACHE_TYPE': 'simple'})


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


@cache.cached(timeout=60, key_prefix='cart_')
def get_cart(username: str) -> list:
    """
    Optimized function to get the cart of a user.
    - Avoids `eval` and uses `json.loads` to safely load contents.
    - Fetches product details in bulk to minimize database/API calls.
    """
    try:
        # Fetch cart details from the DAO
        cart_details = dao.get_cart(username)
        if cart_details is None:
            return []
        
        items = []
        for cart_detail in cart_details:
            contents = cart_detail['contents']
            try:
                # Safely decode the JSON string into a list
                evaluated_contents = json.loads(contents)
            except json.JSONDecodeError:
                # Skip invalid cart content
                continue

            # Collect all items in the cart
            for content in evaluated_contents:
                items.append(content)

        # Batch fetch product details
        products_to_fetch = list(set(items))  # Remove duplicates if any
        i2 = products.get_products_batch(products_to_fetch)
        return i2
    except Exception as e:
        # Log error and return an empty list or handle it as needed
        print(f"Error fetching cart for user {username}: {str(e)}")
        return []


def add_to_cart(username: str, product_ids: list):
    """
    Optimized function to add multiple products to a cart in a batch.
    """
    try:
        dao.add_to_cart_batch(username, product_ids)
    except Exception as e:
        # Handle error in adding products
        print(f"Error adding products to cart: {str(e)}")


def remove_from_cart(username: str, product_ids: list):
    """
    Optimized function to remove multiple products from a cart in a batch.
    """
    try:
        dao.remove_from_cart_batch(username, product_ids)
    except Exception as e:
        # Handle error in removing products
        print(f"Error removing products from cart: {str(e)}")


def delete_cart(username: str):
    """
    Optimized function to delete a user's entire cart.
    """
    try:
        dao.delete_cart(username)
    except Exception as e:
        # Handle error in deleting cart
        print(f"Error deleting cart for user {username}: {str(e)}")


# Example of DAO functions that should be optimized similarly:
# You should implement batch versions of DAO methods like add_to_cart_batch, remove_from_cart_batch, etc.

# In the `dao` module, implement batch methods as shown below:
# (For example, dao.add_to_cart_batch should take a list of product_ids and add them all at once)

# dao.py
# def add_to_cart_batch(username: str, product_ids: list):
#     # Implement batch add logic (e.g., bulk insert into database)
#     pass
# 
# def remove_from_cart_batch(username: str, product_ids: list):
#     # Implement batch remove logic (e.g., bulk delete from database)
#     pass
