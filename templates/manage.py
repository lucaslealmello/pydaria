from app import app, db
from app.models import Product

@app.cli.command()
def add_product():
    """Adiciona um produto ao banco de dados."""
    name = input("Nome do produto: ")
    price = float(input("Preço do produto: "))
    description = input("Descrição do produto: ")

    product = Product(name=name, price=price, description=description)
    db.session.add(product)
    db.session.commit()

    print("Produto adicionado com sucesso.")
