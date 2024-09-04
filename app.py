from flask import Flask, jsonify, request, render_template
import redis
from datetime import datetime

app = Flask(__name__)

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, db=0)

def populate_redis():
    # Check and populate students list if it does not exist
    if not r.exists('students'):
        students = ['Raissa', 'Tainara', 'Victor', 'Leandro', 'Joao']
        r.rpush('students', *students)
    
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
        'Leandro': {
            'email': 'leandro@gmail.com',
            'courses': ['Algorithms', 'Operating Systems', 'Database Systems', 'Artificial Intelligence'],
            'name': 'Leandro',
            'age': 21,
            'major': 'Computer Science'
        },
        'Joao': {
            'email': 'joao@gmail.com',
            'courses': ['Data Structures', 'Computer Networks', 'Database Systems', 'Artificial Intelligence'],
            'name': 'joao',
            'age': 22,
            'major': 'Computer Science'
        }
    }
    
    for student, details in student_details.items():
        if not r.exists(f'student:{student}:courses'):
            r.rpush(f'student:{student}:courses', *details['courses'])
        if not r.exists(f'student:{student}:details'):
            r.hset(f'student:{student}:details', mapping={
                'name': details['name'],
                'age': details['age'],
                'major': details['major'],
                'email': details['email']
            })

    activities = {
        'Binary Search Tree': {
            'subject': 'Data Structures',
            'due_date': '2024-09-15',
            'assigned_to': 'Joao',
            'status': 'open'
        },
        'Knapsack Problem': {
            'subject': 'Computer Networks',
            'due_date': '2024-09-12',
            'assigned_to': 'Leandro',
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
        }, 
    }

    for activity, details in activities.items():
        if not r.exists(f'activity:{activity}'):
            r.hset(f'activity:{activity}', mapping={
                'subject': details['subject'],
                'due_date': details['due_date'],
                'assigned_to': details['assigned_to'],
                'status': details['status']
            })

    r.delete('courses') 
    all_courses = set()  
    for student, details in student_details.items():
        all_courses.update(details['courses'])
    for course in all_courses:
        r.rpush('courses', course)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set', methods=['POST'])
def set_value():
    key = request.json.get('key')
    value = request.json.get('value')

    # Se a chave for "students", adicione o valor à lista de estudantes
    if key == 'students':
        r.rpush('students', value)
        return jsonify({"message": f"Estudante {value} adicionado à lista de estudantes"}), 200
    else:
        # Inserir um valor normal no Redis
        r.set(key, value)
        return jsonify({"message": f"Valor definido para {key}"}), 200


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
            items[key_str] = r.lrange(key, 0, -1)
        elif key_type == b'hash':
            items[key_str] = r.hgetall(key)
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

# Rotas para as queries específicas
@app.route('/students_with_upcoming_activities', methods=['GET'])
def students_with_upcoming_activities():
    students = get_students_with_upcoming_activities(r)
    return jsonify(students)

@app.route('/courses_with_incomplete_activities', methods=['GET'])
def courses_with_incomplete_activities():
    courses = get_courses_with_incomplete_activities(r)
    return jsonify(courses)

@app.route('/incomplete_activities_in_course/<course_name>', methods=['GET'])
def incomplete_activities_in_course(course_name):
    students = find_students_with_incomplete_activities_in_course(course_name)
    return jsonify(students)

@app.route('/average_age_per_course', methods=['GET'])
def average_age_per_course():
    course_ages = calculate_average_age_per_course()
    return jsonify(course_ages)

@app.route('/overdue_activities_per_student', methods=['GET'])
def overdue_activities_per_student():
    overdue_activities = find_overdue_activities_per_student()
    return jsonify(overdue_activities)

@app.route('/student_course_progress/<student_name>', methods=['GET'])
def student_course_progress(student_name):
    progress = get_student_course_progress(student_name)
    return jsonify(progress)

@app.route('/top_3_cs_students', methods=['GET'])
def top_3_cs_students():
    top_students = top_3_cs_students_by_completed_activities()
    return jsonify(top_students)

@app.route('/course_with_highest_overdue_ratio', methods=['GET'])
def course_with_highest_overdue_ratio():
    course = course_with_highest_overdue_ratio()
    return jsonify({'course': course})


@app.route('/most_overdue_activity_per_course_and_num_students', methods=['GET'])
def api_most_overdue_activity_per_course_and_num_students():
    result = most_overdue_activity_per_course_and_num_students()
    return jsonify(result)

@app.route('/students')
def get_all_students():
    students = r.lrange('students', 0, -1)
    students = [student.decode('utf-8') for student in students]
    return jsonify(students), 200


def get_students_with_upcoming_activities(redis_client):
    today = datetime.today().strftime('%Y-%m-%d')
    students = {}
    for activity in redis_client.scan_iter('activity:*'):
        activity_details = redis_client.hgetall(activity)
        due_date = activity_details[b'due_date'].decode('utf-8')
        assigned_to = activity_details[b'assigned_to'].decode('utf-8')
        if due_date > today:
            if assigned_to not in students:
                students[assigned_to] = []
            students[assigned_to].append(activity.decode('utf-8'))
    return students

def get_courses_with_incomplete_activities(redis_client):
    courses = redis_client.lrange('courses', 0, -1)
    courses = [course.decode('utf-8') for course in courses]
    incomplete_courses = set()
    for activity in redis_client.scan_iter('activity:*'):
        activity_details = redis_client.hgetall(activity)
        status = activity_details[b'status'].decode('utf-8')
        subject = activity_details[b'subject'].decode('utf-8')
        if status != 'completed':
            incomplete_courses.add(subject)
    return list(filter(lambda course: course in incomplete_courses, courses))

def find_students_with_incomplete_activities_in_course(course_name):
    students_in_course = set()
    for student in r.lrange('students', 0, -1):
        student = student.decode('utf-8')
        if course_name in r.lrange(f'student:{student}:courses', 0, -1):
            students_in_course.add(student)

    students_with_incomplete_activities = set()
    for activity in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity)
        if activity_details[b'subject'].decode('utf-8') == course_name and activity_details[b'status'].decode('utf-8') != 'completed':
            students_with_incomplete_activities.add(activity_details[b'assigned_to'].decode('utf-8'))

    return list(students_in_course - students_with_incomplete_activities)

def calculate_average_age_per_course():
    courses = r.lrange('courses', 0, -1)
    courses = [course.decode('utf-8') for course in courses]
    print(f'Courses: {courses}')
    
    course_ages = {}
    for course in courses:
        total_age = 0
        count = 0
        students = r.lrange('students', 0, -1)
        students = [student.decode('utf-8') for student in students]
        for student in students:
            student_courses = r.lrange(f'student:{student}:courses', 0, -1)
            student_courses = [course.decode('utf-8') for course in student_courses]
            if course in student_courses:
                student_details = r.hgetall(f'student:{student}:details')
                student_details = {k.decode('utf-8'): v.decode('utf-8') for k, v in student_details.items()}
                total_age += int(student_details.get('age', 0))
                count += 1
        if count > 0:
            course_ages[course] = round(total_age / count)
        else:
            course_ages[course] = 0  
        print(f'Course: {course}, Average Age: {course_ages.get(course, "N/A")}')
    return course_ages

def find_overdue_activities_per_student():
    today = datetime.today().strftime('%Y-%m-%d')
    overdue_activities = {}
    for activity_key in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity_key)
        due_date = activity_details[b'due_date'].decode('utf-8')
        assigned_to = activity_details[b'assigned_to'].decode('utf-8')
        status = activity_details[b'status'].decode('utf-8')

        if due_date < today and status == 'not completed':
            if assigned_to not in overdue_activities:
                overdue_activities[assigned_to] = []
            overdue_activities[assigned_to].append(activity_key.decode('utf-8'))
    
    return overdue_activities

def get_student_course_progress(student_name):
    student_courses = r.lrange(f'student:{student_name}:courses', 0, -1)
    course_progress = {}
    for course in student_courses:
        course = course.decode('utf-8')
        completed = 0
        incomplete = 0
        for activity in r.scan_iter('activity:*'):
            activity_details = r.hgetall(activity)
            if activity_details[b'subject'].decode('utf-8') == course and activity_details[b'assigned_to'].decode('utf-8') == student_name:
                if activity_details[b'status'].decode('utf-8') == 'completed':
                    completed += 1
                else:
                    incomplete += 1
        course_progress[course] = {'completed': completed, 'incomplete': incomplete}
    return course_progress

def top_3_cs_students_by_completed_activities():
    cs_courses = {'Algorithms', 'Operating Systems', 'Database Systems', 'Artificial Intelligence', 'Data Structures', 'Computer Networks', 'Software Engineering'}
    student_completed_activities = {}

    for activity in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity)
        if activity_details[b'subject'].decode('utf-8') in cs_courses and activity_details[b'status'].decode('utf-8') == 'completed':
            student = activity_details[b'assigned_to'].decode('utf-8')
            student_completed_activities[student] = student_completed_activities.get(student, 0) + 1

    sorted_students = sorted(student_completed_activities.items(), key=lambda x: x[1], reverse=True)
    return sorted_students[:3]

def course_with_highest_overdue_ratio():
    today = datetime.today().strftime('%Y-%m-%d')
   
    course_overdue_counts = {}
    course_total_counts = {}
    
    for activity in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity)
        due_date = activity_details[b'due_date'].decode('utf-8')
        course = activity_details[b'subject'].decode('utf-8')
        
        if due_date < today:
            course_overdue_counts[course] = course_overdue_counts.get(course, 0) + 1
    
        course_total_counts[course] = course_total_counts.get(course, 0) + 1
    
    course_overdue_ratios = {}
    for course in course_total_counts:
        total_activities = course_total_counts[course]
        overdue_activities = course_overdue_counts.get(course, 0)
        if total_activities > 0:
            course_overdue_ratios[course] = overdue_activities / total_activities
    
    if course_overdue_ratios:
        return max(course_overdue_ratios, key=course_overdue_ratios.get)
    else:
        return None

print(course_with_highest_overdue_ratio())

def most_overdue_activity_per_course_and_num_students():
    today = datetime.today().strftime('%Y-%m-%d')
    course_activities = {}

    # Encontrar atividades atrasadas
    for activity_key in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity_key)
        due_date = activity_details.get(b'due_date', b'').decode('utf-8')
        course = activity_details.get(b'subject', b'').decode('utf-8')
        status = activity_details.get(b'status', b'').decode('utf-8')
        assigned_to = activity_details.get(b'assigned_to', b'').decode('utf-8')
        
        if due_date < today and status == 'not completed':
            if course not in course_activities:
                course_activities[course] = {}
            if (due_date, activity_key.decode('utf-8')) not in course_activities[course]:
                course_activities[course][(due_date, activity_key.decode('utf-8'))] = []
            course_activities[course][(due_date, activity_key.decode('utf-8'))].append(assigned_to)

    most_overdue_activities = {}
    for course, activities in course_activities.items():
        # Ordena as atividades pela data de vencimento
        sorted_activities = sorted(activities.keys(), key=lambda x: x[0])
        most_overdue_activity = sorted_activities[0]
        
        # Alunos atrasados na atividade mais atrasada
        overdue_students = activities[most_overdue_activity]
        
        most_overdue_activities[course] = {
            'activity': most_overdue_activity[1],
            'due_date': most_overdue_activity[0],
            'overdue_students': len(overdue_students),
            'students': overdue_students
        }

    return most_overdue_activities


def most_overdue_activity_per_course_and_num_students():
    courses = r.lrange('courses', 0, -1)
    course_overdue_activity_count = {}

    for course in courses:
        course = course.decode('utf-8')
        max_overdue_days = -1
        most_overdue_activity = None
        most_overdue_students_count = 0
        
        for activity in r.scan_iter('activity:*'):
            activity_details = r.hgetall(activity)
            if activity_details[b'subject'].decode('utf-8') == course:
                due_date = datetime.strptime(activity_details[b'due_date'].decode('utf-8'), '%Y-%m-%d')
                status = activity_details[b'status'].decode('utf-8')
                if status == 'not completed':
                    overdue_days = (datetime.today() - due_date).days
                    if overdue_days > max_overdue_days:
                        max_overdue_days = overdue_days
                        most_overdue_activity = activity.decode('utf-8')
                        most_overdue_students_count = 1  # Reseta o contador para a nova atividade mais atrasada
                    elif overdue_days == max_overdue_days:
                        most_overdue_students_count += 1  # Conta mais um aluno para a mesma atividade mais atrasada
        
        if most_overdue_activity:
            course_overdue_activity_count[course] = {
                'activity': most_overdue_activity,
                'students_count': most_overdue_students_count
            }
    
    return course_overdue_activity_count


if __name__ == "__main__":
    populate_redis()  # Povoar o Redis ao iniciar a aplicação
    app.run(host='0.0.0.0', port=5000)