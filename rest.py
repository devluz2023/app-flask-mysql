from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a proper secret key
jwt = JWTManager(app)

# Configuration for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model definition
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Item {self.name}>'

# Function to generate a JWT token
def generate_token(data):
    token = create_access_token(identity=data)
    return token

# Controller for token generation
@app.route('/token', methods=['POST'])
def generate_token_endpoint():
    data = request.json
    token = generate_token(data)
    return jsonify({'token': token})

# Controller with authentication requirement
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_endpoint():
    return jsonify({'message': 'You have accessed a protected resource'})

# CRUD Operations

# Create an item
@app.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.json
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created', 'item': {'id': new_item.id, 'name': new_item.name, 'description': new_item.description}})



@app.route('/', methods=['GET'])
def hello_world():
    print("hello world!")
    return "Hello, World!"

# Read all items
@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])

# Read a single item
@app.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

# Update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    data = request.json
    item = Item.query.get_or_404(item_id)
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'message': 'Item updated', 'item': {'id': item.id, 'name': item.name, 'description': item.description}})

# Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8085)
