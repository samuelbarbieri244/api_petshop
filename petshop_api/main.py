from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)


SECRET_KEY = 'sua_chave_secreta'


products = [
    {
        "id": 1,
        "product_name": "Coleira",
        "product_description": "Coleira para cachorro de pequeno porte",
        "product_price": 23.90,
        "product_photo": "https://example.com/coleira.jpg",
        "stock_quantity": 26
    },
    {
        "id": 2,
        "product_name": "Ração Premium",
        "product_description": "Ração para cães de médio porte",
        "product_price": 85.50,
        "product_photo": "https://example.com/racao.jpg",
        "stock_quantity": 15
    },
    {
        "id": 3,
        "product_name": "Brinquedo",
        "product_description": "Brinquedo para gato",
        "product_price": 19.99,
        "product_photo": "https://example.com/brinquedo.jpg",
        "stock_quantity": 40
    }
]


def token_required(f):
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token de acesso é necessário!'}), 403
        try:

            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return jsonify({'message': 'Token inválido!'}), 403
        return f(*args, **kwargs)
    return decorator


def generate_token():
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'exp': expiration_time}, SECRET_KEY, algorithm="HS256")
    return token


@app.route('/login', methods=['POST'])
def login():
    token = generate_token()
    return jsonify({'token': token})


@app.route('/products', methods=['GET'])
@token_required
def get_products():
    return jsonify(products)


@app.route('/products/<int:id>', methods=['GET'])
@token_required
def get_product_by_id(id):
    product = next((prod for prod in products if prod['id'] == id), None)
    if product:
        return jsonify(product)
    return jsonify({'message': 'Produto não encontrado!'}), 404


@app.route('/products', methods=['GET'])
@token_required
def get_products_by_price_asc():
    if 'preco_asc' in request.args and request.args['preco_asc'] == 'true':
        sorted_products = sorted(products, key=lambda x: x['product_price'])
        return jsonify(sorted_products)
    return jsonify({'message': 'Parâmetro "preco_asc" é necessário para esta rota.'}), 400


@app.route('/products', methods=['GET'])
@token_required
def get_products_by_price_desc():
    if 'preco_desc' in request.args and request.args['preco_desc'] == 'true':
        sorted_products = sorted(products, key=lambda x: x['product_price'], reverse=True)
        return jsonify(sorted_products)
    return jsonify({'message': 'Parâmetro "preco_desc" é necessário para esta rota.'}), 400


@app.route('/products', methods=['GET'])
@token_required
def get_products_by_description():
    if 'description_part' in request.args:
        description_part = request.args['description_part'].lower()
        filtered_products = [prod for prod in products if description_part in prod['product_description'].lower()]
        return jsonify(filtered_products)
    return jsonify({'message': 'Parâmetro "description_part" é necessário para esta rota.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
