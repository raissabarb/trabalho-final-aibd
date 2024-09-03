from flask import Flask, render_template, jsonify
import redis
from datetime import datetime

app = Flask(__name__)

# Configuração da conexão Redis
r = redis.Redis(host='localhost', port=6379, db=0)

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
        assigned_to = activity_details[b'assigned_to'].decode('utf-8')
        subject = activity_details[b'subject'].decode('utf-8')
        if status != 'completed' and assigned_to in r.lrange(f'student:{assigned_to}:courses', 0, -1):
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
    course_ages = {}
    for course in courses:
        course = course.decode('utf-8')
        total_age = 0
        count = 0
        for student in r.lrange('students', 0, -1):
            student = student.decode('utf-8')
            if course in r.lrange(f'student:{student}:courses', 0, -1):
                student_details = r.hgetall(f'student:{student}:details')
                total_age += int(student_details[b'age'].decode('utf-8'))
                count += 1
        if count > 0:
            course_ages[course] = total_age / count
    return course_ages

def find_overdue_activities_per_student():
    today = datetime.today().strftime('%Y-%m-%d')
    overdue_activities = {}
    for activity in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity)
        due_date = activity_details[b'due_date'].decode('utf-8')
        assigned_to = activity_details[b'assigned_to'].decode('utf-8')
        if due_date < today:
            if assigned_to not in overdue_activities:
                overdue_activities[assigned_to] = []
            overdue_activities[assigned_to].append(activity.decode('utf-8'))
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
    course_overdue_ratios = {}

    for activity in r.scan_iter('activity:*'):
        activity_details = r.hgetall(activity)
        due_date = activity_details[b'due_date'].decode('utf-8')
        course = activity_details[b'subject'].decode('utf-8')
        if due_date < today:
            course_overdue_ratios[course] = course_overdue_ratios.get(course, 0) + 1

    for course, total_overdue in course_overdue_ratios.items():
        total_activities = len(r.lrange(f'activity:{course}:activities', 0, -1))  # Assumindo que você tem uma lista de atividades por curso
        course_overdue_ratios[course] /= total_activities

    return max(course_overdue_ratios, key=course_overdue_ratios.get)

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
