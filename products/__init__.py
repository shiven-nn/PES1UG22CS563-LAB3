# from products import dao


# class Product:
#     def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.cost = cost
#         self.qty = qty

#     def load(data):
#         return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


# def list_products() -> list[Product]:
#     products = dao.list_products()
#     result = []
#     for product in products:
#         result.append(Product.load(product))
    
#     return result



# def get_product(product_id: int) -> Product:
#     return Product.load(dao.get_product(product_id))


# def add_product(product: dict):
#     dao.add_product(product)


# def update_qty(product_id: int, qty: int):
#     if qty < 0:
#         raise ValueError('Quantity cannot be negative')
#     dao.update_qty(product_id, qty)






from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


def list_products() -> list[Product]:
    # Use list comprehension for cleaner and potentially faster execution
    return [Product.load(product) for product in dao.list_products()]


def get_product(product_id: int) -> Product:
    # Directly return the loaded product
    return Product.load(dao.get_product(product_id))


def add_product(product: dict):
    # Check if the product already exists (assuming dao has a method to check if product exists)
    if dao.get_product(product['id']) is not None:
        raise ValueError(f"Product with ID {product['id']} already exists.")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    # We could include a check here to ensure the product exists before updating the quantity
    product = dao.get_product(product_id)
    if product is None:
        raise ValueError(f"Product with ID {product_id} does not exist.")
    dao.update_qty(product_id, qty)
