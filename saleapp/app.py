from flask import render_template, request, redirect, url_for
from saleapp import app
from saleapp import dal

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    return render_template("products.html", products=dal.read_products(keyword=keyword))

@app.route("/products/<int:category_id>")
def products_by_category_id(category_id):
    return render_template("products.html", products=dal.read_products_by_category_id(category_id))

@app.route("/products/add", methods=["post", "get"])
def add_product():
    error_msg = None
    categories = dal.read_categories()

    if request.method == "POST":
        if dal.add_product(**dict(request.form)):
            return redirect(url_for('products'))
        else:
            error_msg = "Không thêm được sản phẩm. Vui lòng thử lại"

    return render_template("add-product.html", categories=categories, error_msg=error_msg)

@app.route("/products/update/<int:product_id>", methods=["post", "get"])
def update_product(product_id):
    error_msg = None
    product = dal.read_product_by_id(product_id)
    categories = dal.read_categories()

    if request.method == "POST":
        d = dict(request.form.copy())
        d["product_id"] = product_id
        if dal.update_product(**d):
            return redirect(url_for('products'))
        else:
            error_msg = "Không cập nhật được sản phẩm. Vui lòng thử lại"

    return render_template("update-product.html", product=product[0], categories=categories, error_msg=error_msg)

@app.route("/products/delete/<int:product_id>", methods=["post", "get"])
def delete_product(product_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)