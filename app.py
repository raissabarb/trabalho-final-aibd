from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def index():
    return "Coloca o front Gabriel"

@app.route('/set', methods=['POST'])
def set_value():
    key = request.json.get('key')
    value = request.json.get('value')
    r.set(key, value)
    return jsonify({"message": f"Value set for {key}"}), 200

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    value = r.get(key)
    if value:
        return jsonify({key: value.decode('utf-8')}), 200
    return jsonify({"message": "Key not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
