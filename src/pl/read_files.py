import json

PRODUCTS_FILE_PATH = 'data/products.json'
RESOURCES_FILE_PATH = 'data/resources.json'


def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is empty/corrupted, start with an empty list
        return []


def save_json_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def add_data_item(file_path, new_item):
    data = load_json_data(file_path)
    data.append(new_item)
    save_json_data(file_path, data)


def load_products():
    return load_json_data(PRODUCTS_FILE_PATH)


def load_resources():
    return load_json_data(RESOURCES_FILE_PATH)


def add_product(new_product):
    add_data_item(PRODUCTS_FILE_PATH, new_product)


def add_resource(new_resource):
    add_data_item(RESOURCES_FILE_PATH, new_resource)


def add_resource_to_product(product_name, resource_name, quantity):
    products = load_products()

    for product in products:
        if product['name'] == product_name:
            # Found the product, now add the resource
            new_resource = {"name": resource_name, "quantity": str(quantity)}

            # Check if the resource already exists
            found = False
            for resource in product['resources_needed']:
                if resource['name'] == resource_name:
                    # Update quantity if resource exists
                    resource['quantity'] = str(int(resource['quantity']) + quantity)
                    found = True
                    break

            if not found:
                # Resource doesn't exist, add new one
                product['resources_needed'].append(new_resource)

            break  # Stop the loop once the product is found and updated

    save_json_data(PRODUCTS_FILE_PATH, products)
