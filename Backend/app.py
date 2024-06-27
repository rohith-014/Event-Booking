from flask import Flask, jsonify
from database import mongo
from EventService.eventblueprint import eventblueprint
from BookingService.bookingblueprint import bookingblueprint
from UserService.userblueprint import userblueprint

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"]=os.environ.get('MONGO_URI')
mongo.init_app(app)

# Register blueprints here
app.register_blueprint(eventblueprint, url_prefix='/events')
app.register_blueprint(bookingblueprint, url_prefix='/bookings')
app.register_blueprint(userblueprint, url_prefix='/users')

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

if __name__ == '__main__':
    print(os.environ.get('MONGO_URI'))
    app.run(debug=True, host='0.0.0.0', port=5000)