class Inventory:
    def __init__(self):
        self.inventory_list = []

    def add_product(self, product):
        self.inventory_list.append(product)

    def list_products(self):
        for product in self.inventory_list:
            print(product.__dict__)

    def delete_product(self, product_id):
        for product in self.inventory_list:
            if product.get_id() == product_id:
                self.inventory_list.remove(product)
                print(f"Product with ID {product_id} deleted.")
                return
        print(f"Product with ID {product_id} not found.")

    def search_product(self, product_id):
        for product in self.inventory_list:
            if product.get_id() == product_id:
                print(product.__dict__)
                return
        print(f"Product with ID {product_id} not found.")

    
    def alter_product(self, product_id, attribute, new_value):
        for product in self.inventory_list:
            if product.get_id() == product_id:
                # Using getattr and setattr to dynamically access and modify attributes
                setter_method = f"set_{attribute}"
                if hasattr(product, setter_method) and callable(getattr(product, setter_method, None)):
                    getattr(product, setter_method)(new_value)
                    print(f"Attribute {attribute} of Product with ID {product_id} altered.")
                    return
                else:
                    print(f"Attribute {attribute} is not alterable.")
                    return
        print(f"Product with ID {product_id} not found.")