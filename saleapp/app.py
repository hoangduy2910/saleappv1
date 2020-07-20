from flask import render_template,request
from saleapp import app
from saleapp import dal

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    #import pdb
    #pdb.set_trace()
    return render_template("products.html", products=dal.read_products(keyword=keyword))

@app.route("/products/<int:category_id>")
def products_by_category_id(category_id):
    return render_template("products.html", products=dal.read_products_by_category_id(category_id))

@app.route("/products/add", methods=["post", "get"])
def add_product():
    if request.method == "POST":
        print("123")
    return render_template("add-product.html")

if __name__ == "__main__":
    app.run(debug=True)