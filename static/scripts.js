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
