import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))  # Path to the directory of the current file
PRODUCTS_FILE_PATH = os.path.join(dir_path, "data/products.json")
RESOURCES_FILE_PATH = os.path.join(dir_path, "data/resources.json")
HUMAN_MACHINE_TIME_FILE_PATH = os.path.join(dir_path, "data/human_machine_time.json")



def load_json_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        print(f"Error reading {file_path}: {ex}")
        # If the file does not exist or is empty/corrupted, start with an empty list
        return []


def save_json_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def add_data_item(file_path, new_item):
    data = load_json_data(file_path)
    item_index = next((index for (index, d) in enumerate(data) if d['name'] == new_item['name']), None)

    if item_index is not None:
        # If item exists, update it
        data[item_index] = new_item
    else:
        # If item does not exist, append it
        data.append(new_item)
    save_json_data(file_path, data)

def add_work_time_item(file_path, new_item):
    data = load_json_data(file_path)
    data.append(new_item)
    save_json_data(file_path, data)


def load_products():
    return load_json_data(PRODUCTS_FILE_PATH)


def load_resources():
    return load_json_data(RESOURCES_FILE_PATH)
def load_human_machine_time():
    return load_json_data(HUMAN_MACHINE_TIME_FILE_PATH)


def add_product(new_product):
    add_data_item(PRODUCTS_FILE_PATH, new_product)


def add_resource(new_resource):
    add_data_item(RESOURCES_FILE_PATH, new_resource)

def add_human_machine_time(new_resource):
    add_work_time_item(HUMAN_MACHINE_TIME_FILE_PATH, new_resource)



def add_resource_to_product(product_name, resource_name, quantity):
    products = load_products()

    for product in products:
        if product["name"] == product_name:
            # Found the product, now add the resource
            new_resource = {"name": resource_name, "quantity": quantity}

            # Check if the resource already exists
            found = False
            for resource in product["resources_needed"]:
                if resource["name"] == resource_name:
                    # Update quantity if resource exists
                    resource["quantity"] = (int(resource["quantity"]) + quantity)
                    found = True
                    break

            if not found:
                # Resource doesn't exist, add new one
                product["resources_needed"].append(new_resource)

            break  # Stop the loop once the product is found and updated

    save_json_data(PRODUCTS_FILE_PATH, products)


def delete_item_from_json(file_path, item_name):
    items = load_json_data(file_path)
    items = [item for item in items if item.get('name') != item_name]
    save_json_data(file_path, items)


def delete_resource_from_json(resource_name):
    delete_item_from_json(RESOURCES_FILE_PATH, resource_name)


def delete_product_from_json(product_name):
    delete_item_from_json(PRODUCTS_FILE_PATH, product_name)

def delete_human_machine_time_from_json(product_name):
    delete_item_from_json(HUMAN_MACHINE_TIME_FILE_PATH,product_name)