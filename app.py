from flask import Flask, jsonify, request, render_template
import redis

app = Flask(__name__)

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, db=0)

def populate_redis():
    # Verifica se a lista 'estudantes' já existe
    if not r.exists('estudantes'):
        # Adiciona os nomes à lista 'estudantes'
        estudantes = ['Enzo', 'Raissa', 'Tainara', 'Victor', 'Gabriel', 'Pedro']
        r.rpush('estudantes', *estudantes)
        print("Lista 'estudantes' criada com sucesso!")
    else:
        print("Lista 'estudantes' já existe.")

@app.route('/')
def index():
    return "Hello, Redis with Flask!"

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

@app.route('/students')
def get_students():
    students = r.lrange('estudantes', 0, -1)
    students = [student.decode('utf-8') for student in students]
    return jsonify(students), 200

if __name__ == "__main__":
    populate_redis()  # Chama a função para povoar o Redis ao iniciar a aplicação
    app.run(host='0.0.0.0', port=5000)
