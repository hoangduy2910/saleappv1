from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from saleapp import app, dal, utils, decorator


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
@decorator.login_required
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
@decorator.login_required
def update_product(product_id):
    error_msg = None
    product = dal.read_product_by_id(product_id)
    categories = dal.read_categories()

    if request.method == "POST":
        d = dict(request.form.copy())
        d["product_id"] = product_id
        if dal.update_product(**d):
            return redirect(url_for('products', product_id=product_id))
        else:
            error_msg = "Không cập nhật được sản phẩm. Vui lòng thử lại"

    return render_template("update-product.html", product=product[0], categories=categories, error_msg=error_msg)


@app.route("/api/product/<int:product_id>", methods=["delete"])
@decorator.login_required
def delete_product(product_id):
    if dal.delete_product(product_id):
        return jsonify({"status": 200, "product_id": product_id})
    else:
        return jsonify({"status": 500, "error_msg": "Xóa sản phẩm thất bại. Vui lòng thử lại sau"})


@app.route("/products/export")
@decorator.login_required
def export_products():
    p = utils.export_products()
    return send_file(filename_or_fp=p)


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dal.check_login(username=username, password=password)

        if user:
            session["user"] = user

            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for('index'))
        else:
            err_msg = "Đăng nhập thất bại. Vui lòng kiểm tra lại tài khoản hoặc mật khẩu !!!"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None
    return redirect(url_for('index'))


@app.route("/register", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password.strip() != confirm.strip():
            err_msg = "Mật khẩu không khớp"
        else:
            if dal.add_user(name=name, username=username, password=password):
                return redirect(url_for("login"))
            else:
                err_msg = "Đăng ký thất bại"

    return render_template("register.html", err_msg=err_msg)

if __name__ == "__main__":
    app.run(debug=True)