from flask import Blueprint, request, jsonify
from database import mongo

userblueprint = Blueprint('userblueprint', __name__)

@userblueprint.route('/', methods=['GET'])
def get_users():
    search_param = request.args.get('search')
    id= request.args.get('id',False)
    start = int(request.args.get('start', 0))
    limit = 20
    if search_param:
        users = mongo.db.users.find({
            '$or': [
                {'name': {'$regex': search_param, '$options': 'i'}},
                {'description': {'$regex': search_param, '$options': 'i'}}
            ]
        }).skip(start).limit(limit)
    else:
        users = mongo.db.users.find().skip(start).limit(limit)

    user_list = []
    for user in users:
        user_data = {
            'name': user['name'],
            'email': user['email'],
            'location': user['location'],
            'joined_date': user['joined_date'],
            'description': user['description'],
            'events_attended': user['events_attended']
        }
        if id:
            user_data['id'] = str(user['_id'])
        user_list.append(user_data)
    return jsonify({'users': user_list})

@userblueprint.route('/find', methods=['POST'])
def find_user():
    id= request.json['id']
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        response = {
            'name': user['name'],
            'email': user['email'],
            'location': user['location'],
            'joined_date': user['joined_date'],
            'description': user['description'],
            'events_attended': user['events_attended']
        }
        return jsonify(response)
    else:
        return jsonify({'message': 'User not found'})

@userblueprint.route('/addUser', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    location = request.json['location']
    joined_date = request.json['joined_date']
    description = request.json['description']
    events_attended = request.json['events_attended']
    mongo.db.users.insert_one({
        'name': name,
        'email': email,
        'location': location,
        'joined_date': joined_date,
        'description': description,
        'events_attended': events_attended
    })
    return jsonify({'message': 'User added successfully'})

@userblueprint.route('/updateUser/<id>', methods=['PUT'])
def update_user(id):
    user = mongo.db.users.find_one({'_id': id})
    if user:
        mongo.db.users.update_one({'_id': id}, {'$set': request.json})
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@userblueprint.route('/deleteUser/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one({'_id': id})
    if user:
        mongo.db.users.delete_one({'_id': id})
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'})