from flask import Flask, request, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if authenticate(data['username'], data['password']):
        return redirect(url_for('dashboard'))
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/dashboard')
def dashboard():
    user_info = {
        "name": "John Doe",
        "activities": ["Football", "Basketball"],
        "events": ["Match amical samedi", "Tournoi de tennis dimanche"]
    }
    return jsonify(user_info)

def authenticate(username, password):
    return True

if __name__ == '__main__':
    app.run(debug=True)
