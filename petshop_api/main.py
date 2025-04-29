from flask import Flask, render_template

app = Flask(__name__)

products = [
    {"id": 1, "product_name": "Coleira", "product_description": "Coleira para cachorro de pequeno porte",
     "product_price": 23.90, "product_photo": "coleira.jpg", "stock_quantity": 26},
    # ... (todos os outros produtos)
    {"id": 50, "product_name": "Luz UV para aquário", "product_description": "Iluminação e esterilização para aquários",
     "product_price": 72.00, "product_photo": "luz-aquario.jpg", "stock_quantity": 11}
]


@app.route('/')
def index():
    return render_template("index.html", products=products)


if __name__ == '__main__':
    app.run(debug=True)