import json

products_file_path = 'data/products.json'
resources_file_path = 'data/resources.json'


def load_products():
    try:
        with open(products_file_path, 'r') as file:
            products = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is empty/corrupted, start with an empty list
        products = []
    return products


def load_resources():
    with open(resources_file_path, 'r') as file:
        resources = json.load(file)
    return resources


def save_products(products):
    with open(products_file_path, 'w') as file:
        json.dump(products, file, indent=4)


def save_resources(resources):
    with open(resources_file_path, 'w') as file:
        json.dump(resources, file, indent=4)


def add_product(new_product):
    products = load_products()
    products.append(new_product)
    save_products(products)
