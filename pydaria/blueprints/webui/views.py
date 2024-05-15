from pydaria.models import Product 
from flask import abort, render_template

def index():
    products = Product.query.all()
    if product is None:
        abort(404, "Produtos não encontrado")
    print(products)
    return render_template("index.html", products=products)
 

def product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        abort(404, "Produto não encontrado")
    return render_template("product.html", product=product)
