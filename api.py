
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:DEVA12345@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Deva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Changed to String
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

@app.route('/')
def home():

  return "welcome to home page"

@app.route('/users', methods=['GET'])
def get_users():
    users = Deva.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify({'users': user_list})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Deva.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User Not Found'}), 404
    return jsonify({'user': user.to_dict()})
 
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if 'username' not in data or 'email' not in data:
        return jsonify({'message': 'Username and Email are required'}), 400
    
    new_user = Deva(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Deva.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Deva.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
