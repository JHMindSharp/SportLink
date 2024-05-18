from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.sportlink

@app.route('/')
def home():
    return jsonify(message="Welcome to SportLink")

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    db.users.insert_one(data)
    return jsonify(message="User created"), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return jsonify(user)

if __name__ == '__main__':
    socketio.run(app, debug=True)
