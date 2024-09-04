document.getElementById('setValueForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const key = document.getElementById('key').value;
    const value = document.getElementById('value').value;

    fetch('/set', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key, value }),
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => console.error('Erro:', error));
});

function fetchStudents() {
    fetch('/students')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function fetchViewAll() {
    window.location.href = '/view';
}

function fetchStudentsWithUpcomingActivities() {
    fetch('/students_with_upcoming_activities')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function fetchCoursesWithIncompleteActivities() {
    fetch('/courses_with_incomplete_activities')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function fetchAverageAgePerCourse() {
    fetch('/average_age_per_course')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function fetchOverdueActivitiesPerStudent() {
    fetch('/overdue_activities_per_student')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function fetchTop3CsStudents() {
    fetch('/top_3_cs_students')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function fetchCourseWithHighestOverdueRatio() {
    fetch('/course_with_highest_overdue_ratio')
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Erro:', error));
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
}

function updateSoftwareEngineeringActivities() {
    fetch('/update_software_engineering_activities', { method: 'POST' })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Erro:', error));
}
