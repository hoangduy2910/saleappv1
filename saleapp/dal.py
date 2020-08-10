from saleapp import app
import json
import os
import hashlib


def read_products(keyword=None, from_price=None, to_price=None):
    products = None
    with open(os.path.join(app.root_path, 'data/products.json'), encoding="utf-8") as f:
        products = json.load(f)

    if keyword:
        return [product for product in read_products() if product["name"].lower().find(keyword.lower()) >= 0]

    if from_price and to_price:
        return [product for product in read_products() if product["price"] >= from_price and product["price"] <= to_price]

    return products


def read_products_by_category_id(category_id):
    return [product for product in read_products() if product["category_id"] == category_id]


def read_product_by_id(product_id):
    return [product for product in read_products() if product["id"] == product_id]


def add_product(name, description, price, image, category_id):
    products = read_products()
    products.append({
        "id": len(products) + 1,
        "name": name,
        "description": description,
        "price": int(price),
        "image": image,
        "category_id": int(category_id)
    })
    return update_product_json(products)


def update_product(product_id, name, description, price, image, category_id):
    products = read_products()
    for product in products:
        if product["id"] == product_id:
            product["name"] = name
            product["description"] = description
            product["price"] = int(price)
            product["image"] = image
            product["category_id"] = int(category_id)
            break
    return update_product_json(products)


def delete_product(product_id):
    products = read_products()
    for index, product in enumerate(products):
        if product["id"] == product_id:
            del products[index]
            break
    return update_product_json(products)


def update_product_json(products):
    try:
        with open(os.path.join(app.root_path, 'data/products.json'), "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        return True
    except Exception as ex:
        return False


def read_categories():
    with open(os.path.join(app.root_path, 'data/categories.json'), encoding="utf-8") as f:
        return json.load(f)


def read_users():
    with open(os.path.join(app.root_path, 'data/users.json'), encoding="utf-8") as f:
        return json.load(f)


def add_user(name, username, password):
    users = read_users()
    user = {
        "id": len(users) + 1,
        "name": name,
        "username": username,
        "password": str(hashlib.md5(password.encode("utf-8")).hexdigest())
    }
    users.append(user)

    try:
        with open(os.path.join(app.root_path, 'data/users.json'), "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        return True
    except Exception as ex:
        return False


def check_login(username, password):
    users = read_users()
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())

    for u in users:
        if u["username"].strip() == username.strip() and u["password"] == password:
            return u

    return None