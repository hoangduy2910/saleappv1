from saleapp import dal, app
import csv
import os

def export_products():
  products = dal.read_products()
  p = os.path.join(app.root_path, 'data/products.csv')
  with open(p, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "description", "price", "image", "category_id"])
    writer.writeheader()
    for pro in products:
      writer.writerow(pro)

  return p