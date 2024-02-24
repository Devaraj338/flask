from flask import Flask,request
import mysql.connector

app = Flask(__name__)

# Database Connectivity
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='DEVA12345',
    database='flask'
)
cursor = db.cursor()

# Routes
@app.route('/')
def home():
    return "Welcome to the home page "

#get the all the users list
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM employee")
    users = cursor.fetchall()
    user_list = [{'id': user[0], 'name': user[1], 'city': user[2],'emailid': user[3]} for user in users]
    return {'users': user_list}

#get paticular user 
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM employee WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return {'user': {'id': user[0], 'name': user[1], 'city': user[2],'emailid':user[3]}}
    else:
        return {'ERROR': 'USER NOT FOUND'}, 404

#create new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    cursor.execute("INSERT INTO employee (name, city, emailid) VALUES ( %s, %s, %s)", (new_user['name'], new_user['city'],new_user['emailid']))
    db.commit()
    new_user_id = cursor.lastrowid
    return {'MESSAGE': 'USER CREATED SUCCESSFULLY', 'user_id': new_user_id}

# update 
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user_data = request.json
    cursor.execute("UPDATE employee SET name=%s, city=%s, emailid=%s WHERE id=%s",
                   (updated_user_data['name'], updated_user_data['city'],updated_user_data['emailid'], user_id))
    db.commit()
    if cursor.rowcount > 0:
        return {'MESSAGE': f'User with id {user_id} updated SUCCESSFULLY'}
    else:
        return {'ERROR': 'USER NOT FOUND'}, 404

#delete
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM employee WHERE id=%s", (user_id,))
    db.commit()
    if cursor.rowcount > 0:
        return {'MESSAGE': f'User with ID {user_id} DELETED SUCCESSFULLY'}
    else:
        return {'ERROR': 'USER NOT FOUND'}, 404

if __name__ == '__main__':
    app.run(debug=True)