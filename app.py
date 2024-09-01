from flask import Flask, jsonify, request, render_template
import redis

app = Flask(__name__)

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, db=0)

def populate_redis():
    # Check and populate students list if it does not exist
    if not r.exists('students'):
        students = ['Raissa', 'Tainara', 'Victor', 'Gabriel', 'Pedro']
        r.rpush('students', *students)
        print("List 'students' created with success!")
    else:
        print("List 'students' already exists.")
    
    # Define student details including email, courses, and absence
    student_details = {
        'Raissa': {
            'email': 'raissa@gmail.com',
            'courses': ['Algorithms', 'Operating Systems', 'Database Systems', 'Artificial Intelligence'],
            'name': 'Raissa',
            'age': 21,
            'major': 'Computer Science'
        },
        'Tainara': {
            'email': 'tainara@gmail.com',
            'courses': ['Algorithms', 'Database Systems', 'Software Engineering'],
            'name': 'Tainara',
            'age': 22,
            'major': 'Computer Science'
        },
        'Victor': {
            'email': 'victor@gmail.com',
            'courses': ['Data Structures', 'Database Systems', 'Software Engineering'],
            'name': 'Victor',
            'age': 23,
            'major': 'Computer Engineering'
        },
        'Gabriel': {
            'email': 'gabriel@gmail.com',
            'courses': ['Algorithms', 'Operating Systems', 'Database Systems', 'Artificial Intelligence'],
            'name': 'Gabriel',
            'age': 21,
            'major': 'Computer Science'
        },
        'Pedro': {
            'email': 'pedro@gmail.com',
            'courses': ['Data Structures', 'Computer Networks', 'Database Systems', 'Artificial Intelligence'],
            'name': 'Pedro',
            'age': 22,
            'major': 'Computer Science'
        }
    }
    
    for student, details in student_details.items():
        
        # Check if the student's courses list already exists
        if not r.exists(f'student:{student}:courses'):
            r.rpush(f'student:{student}:courses', *details['courses'])
            print(f"Courses for student {student} created with success!")

        # Check if the student's detailed info hash exists
        if not r.exists(f'student:{student}:details'):
            r.hset(f'student:{student}:details', mapping={
                'name': details['name'],
                'age': details['age'],
                'major': details['major'],
                'email': details['email']
            })
            print(f"Detailed info for student {student} created with success!")

    activities = {
        'Binary Search Tree': {
            'subject': 'Data Structures',
            'due_date': '2024-09-15',
            'assigned_to': 'Pedro',
            'status': 'open'
        },
        'Knapsack Problem': {
            'subject': 'Computer Networks',
            'due_date': '2024-09-12',
            'assigned_to': 'Gabriel',
            'status': 'open'
        },
        'Final Activity': {
            'subject': 'Software Engineering',
            'due_date': '2024-09-17',
            'assigned_to': 'Victor',
            'status': 'open'
        },
        'Shell in C': {
            'subject': 'Operating Systems',
            'due_date': '2024-09-01',
            'assigned_to': 'Raissa',
            'status': 'completed'
        },
        'Knn': {
            'subject': 'Artificial Intelligence',
            'due_date': '2024-08-10',
            'assigned_to': 'Raissa',
            'status': 'not completed'
        },
        'MariaDB': {
            'subject': 'Database Systems',
            'due_date': '2024-08-29',
            'assigned_to': 'Tainara',
            'status': 'completed'
        }
    }

    for activity, details in activities.items():
        if not r.exists(f'activity:{activity}'):
            r.hset(f'activity:{activity}', mapping={
                'subject': details['subject'],
                'due_date': details['due_date'],
                'assigned_to': details['assigned_to'],
                'status': details['status']
            })
            print(f"Activity {activity} created with success!")

    # Activity Hashes
    r.delete('activities') 
    for activity in activities.keys():
        r.rpush('activities', f'{activity}')
        if not r.exists(f'{activity}'):
            r.hset(f'activity:{activity}', mapping={
                'subject': activities[activity]['subject'],
                'due_date': activities[activity]['due_date'],
                'assigned_to': activities[activity]['assigned_to'],
                'status': activities[activity]['status']
            })
            print(f"Activity {activity} created with success!")

    # Courses
    all_courses = set()  
    for student, details in student_details.items():
        all_courses.update(details['courses'])
    r.delete('courses') 
    for course in all_courses:
        r.rpush('courses', course)
    
    print("Courses list created with success!")


@app.route('/')
def index():
    return "Hello, Redis with Flask!"

@app.route('/set', methods=['POST'])
def set_value():
    key = request.json.get('key')
    value = request.json.get('value')
    r.set(key, value)
    return jsonify({"message": f"Value set for {key}"}), 200

@app.route('/view')
def view_all():
    keys = r.keys('*')
    items = {}
    
    for key in keys:
        key_str = key.decode('utf-8')
        key_type = r.type(key)
        
        if key_type == b'string':
            items[key_str] = r.get(key).decode('utf-8')
        elif key_type == b'list':
            items[key_str] = r.lrange(key, 0, -1)  # Obtem todos os itens da lista
        elif key_type == b'hash':
            items[key_str] = r.hgetall(key)  # Obtem todos os campos e valores do hash
        else:
            items[key_str] = f"Cannot display type: {key_type.decode('utf-8')}"
    
    return render_template('view.html', items=items)


@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    value = r.get(key)
    if value:
        return jsonify({key: value.decode('utf-8')}), 200
    return jsonify({"message": "Key not found"}), 404

@app.route('/students')
def get_students():
    students = r.lrange('students', 0, -1)
    students = [student.decode('utf-8') for student in students]
    return jsonify(students), 200

if __name__ == "__main__":
    populate_redis()  # Chama a função para povoar o Redis ao iniciar a aplicação
    app.run(host='0.0.0.0', port=5000)
