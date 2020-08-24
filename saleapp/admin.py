from saleapp import db, admin
from saleapp.models import Category, Product, User
from flask_admin.contrib.sqla import ModelView


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))
