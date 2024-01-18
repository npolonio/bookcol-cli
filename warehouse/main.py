from inventory import Inventory
from product import Product



def main():
    inventory = Inventory()

    while True:
        print("\nCommands:")
        print("1. list")
        print("2. add")
        print("3. delete")
        print("4. search")
        print("5. alter")
        print("6. exit")

        choice = input("Enter command: ")

        if choice == "list":
            inventory.list_products()
        elif choice == "add":
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            quantity = input("Enter product quantity: ")
            price = input("Enter product price: ")
            location = input("Enter product location: ")
            product = Product(product_id, name, quantity, price, location)
            inventory.add_product(product)
            print("Product added.")
        elif choice == "delete":
            product_id = input("Enter product ID to delete: ")
            inventory.delete_product(product_id)
        elif choice == "search":
            product_id = input("Enter product ID to search: ")
            inventory.search_product(product_id)
        elif choice == "alter":
            product_id = input("Enter product ID to alter: ")
            attribute = input("Enter attribute to alter: ")
            new_value = input("Enter new value: ")
            inventory.alter_product(product_id, attribute, new_value)
        elif choice == "exit":
            break
        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()
