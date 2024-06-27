from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from database import mongo

bookingblueprint = Blueprint('bookingblueprint', __name__)

@bookingblueprint.route('/', methods=['GET'])
def get_bookings():
    user_id = request.args.get('user_id')
    event_id = request.args.get('event_id')
    start = int(request.args.get('start', 0))
    limit = 20

    query = {}
    if user_id:
        query['user_id'] = user_id
    if event_id:
        query['event_id'] = event_id

    bookings = mongo.db.bookings.find(query).skip(start).limit(limit)

    booking_list = []
    for booking in bookings:
        booking_data = {
            'user_id': booking['user_id'],
            'event_id': booking['event_id'],
            'seats': booking['seats'],
            'booking_date': booking['booking_date']
        }
        booking_data['id'] = str(booking['_id'])
        booking_list.append(booking_data)
        
    return jsonify({'bookings': booking_list})


@bookingblueprint.route('/find', methods=['POST'])
def find_booking():
    id = request.json['id']
    booking = mongo.db.bookings.find_one({'_id': ObjectId(id)})
    if booking:
        response = {
            'user_id': booking['user_id'],
            'event_id': booking['event_id'],
            'seats': booking['seats'],
            'booking_date': booking['booking_date']
        }
        return jsonify(response)
    else:
        return jsonify({'message': 'Booking not found'})


@bookingblueprint.route('/addBooking', methods=['POST'])
def add_booking():
    user_id = request.json['user_id']
    event_id = request.json['event_id']
    seats = request.json['seats']
    booking_date = request.json['booking_date']

    mongo.db.bookings.insert_one({
        'user_id': user_id,
        'event_id': event_id,
        'seats': seats,
        'booking_date': booking_date
    })
    return jsonify({'message': 'Booking added successfully'})


@bookingblueprint.route('/updateBooking/<id>', methods=['PUT'])
def update_booking(id):
    booking = mongo.db.bookings.find_one({'_id': ObjectId(id)})
    if booking:
        mongo.db.bookings.update_one({'_id': ObjectId(id)}, {'$set': request.json})
        return jsonify({'message': 'Booking updated successfully'})
    else:
        return jsonify({'message': 'Booking not found'})


@bookingblueprint.route('/deleteBooking/<id>', methods=['DELETE'])
def delete_booking(id):
    booking = mongo.db.bookings.find_one({'_id': ObjectId(id)})
    if booking:
        mongo.db.bookings.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'Booking deleted successfully'})
    else:
        return jsonify({'message': 'Booking not found'})
