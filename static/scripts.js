document.getElementById('addStudentForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // A chave é sempre 'students'
    const key = 'students';
    const studentName = document.getElementById('student-name').value;

    // Enviar a requisição POST para o backend com o estudante
    fetch('/set', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key, value: studentName }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        // Opcional: exibir uma mensagem de sucesso ou limpar o formulário
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

function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar.style.display === "none" || sidebar.style.display === "") {
        sidebar.style.display = "block";
    } else {
        sidebar.style.display = "none";
    }
}

function displayResults(data) {
    const resultsBody = document.getElementById('results-body');
    resultsBody.innerHTML = ''; // Limpa qualquer conteúdo anterior

    // Itera sobre os dados recebidos e insere as linhas na tabela
    for (const [course, age] of Object.entries(data)) {
        const row = document.createElement('tr');
        const courseCell = document.createElement('td');
        const ageCell = document.createElement('td');
        
        courseCell.textContent = course;
        ageCell.textContent = age;

        row.appendChild(courseCell);
        row.appendChild(ageCell);
        resultsBody.appendChild(row);
    }
}

function fetchMostOverdueActivityPerCourse() {
    fetch('/most_overdue_activity_per_course_and_num_students')
        .then(response => response.json())
        .then(data => displayMostOverdueActivityPerCourse(data))
        .catch(error => console.error('Erro:', error));
}

function displayMostOverdueActivityPerCourse(data) {
    const resultsBody = document.getElementById('results-body');
    resultsBody.innerHTML = ''; // Limpa o conteúdo anterior

    for (const [course, details] of Object.entries(data)) {
        const row = document.createElement('tr');

        const courseCell = document.createElement('td');
        const activityCell = document.createElement('td');
        const dueDateCell = document.createElement('td');
        const studentsCell = document.createElement('td');

        courseCell.textContent = course;
        activityCell.textContent = details.activity;
        dueDateCell.textContent = details.due_date;
        studentsCell.textContent = details.overdue_students;

        row.appendChild(courseCell);
        row.appendChild(activityCell);
        row.appendChild(dueDateCell);
        row.appendChild(studentsCell);

        resultsBody.appendChild(row);
    }
}

function fetchStudentCourseProgress(studentName) {
    fetch(`/student_course_progress/${studentName}`)
        .then(response => response.json())
        .then(data => displayStudentProgress(data))  // Função que exibe o progresso
        .catch(error => console.error('Erro:', error));
}

// Função para carregar os estudantes no select ao carregar a página
function loadStudents() {
    fetch('/students')
        .then(response => response.json())
        .then(data => {
            const studentSelect = document.getElementById('student-select');
            studentSelect.innerHTML = '';  // Limpar qualquer opção existente

            // Criar opção para cada estudante
            data.forEach(student => {
                const option = document.createElement('option');
                option.value = student;
                option.textContent = student;
                studentSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar estudantes:', error));
}

// Chamar a função quando a página carregar
window.onload = loadStudents;


function fetchSelectedStudentProgress() {
    const studentSelect = document.getElementById('student-select');
    const studentName = studentSelect.value;  // Obter o nome do estudante selecionado

    if (studentName) {
        fetch(`/student_course_progress/${studentName}`)
            .then(response => response.json())
            .then(data => displayStudentProgress(data))  // Exibir os resultados na tabela
            .catch(error => console.error('Erro ao buscar progresso:', error));
    } else {
        console.error('Nenhum estudante selecionado');
    }
}


function displayStudentProgress(data) {
    const resultsBody = document.getElementById('results-body');
    resultsBody.innerHTML = '';  // Limpar conteúdo anterior

    for (const [course, progress] of Object.entries(data)) {
        const row = document.createElement('tr');

        const courseCell = document.createElement('td');
        const completedCell = document.createElement('td');
        const incompleteCell = document.createElement('td');

        courseCell.textContent = course;
        completedCell.textContent = progress.completed;
        incompleteCell.textContent = progress.incomplete;

        row.appendChild(courseCell);
        row.appendChild(completedCell);
        row.appendChild(incompleteCell);

        resultsBody.appendChild(row);
    }
}

function showStudentProgressContainer() {
    // Exibir o contêiner de seleção de estudante
    document.getElementById('student-progress-container').style.display = 'block';

    // Carregar a lista de estudantes no select
    loadStudents();
}

function loadStudents() {
    fetch('/students')
        .then(response => response.json())
        .then(data => {
            const studentSelect = document.getElementById('student-select');
            studentSelect.innerHTML = '';  // Limpar opções existentes

            // Criar uma opção para cada estudante
            data.forEach(student => {
                const option = document.createElement('option');
                option.value = student;
                option.textContent = student;
                studentSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar estudantes:', error));
}

function fetchSelectedStudentProgress() {
    const studentSelect = document.getElementById('student-select');
    const studentName = studentSelect.value;  // Obter o nome do estudante selecionado

    if (studentName) {
        fetch(`/student_course_progress/${studentName}`)
            .then(response => response.json())
            .then(data => displayStudentProgress(data))  // Exibir o progresso na tabela
            .catch(error => console.error('Erro ao buscar progresso:', error));
    } else {
        console.error('Nenhum estudante selecionado');
    }
}

// Função para exibir o contêiner de progresso do estudante
function showStudentProgressContainer() {
    hideAllContainers();  // Ocultar outros contêineres quando o progresso do estudante for exibido
    document.getElementById('student-progress-container').style.display = 'block';
    loadStudents();  // Carregar a lista de estudantes no select
}

// Função para ocultar o contêiner de progresso do estudante e outros
function hideAllContainers() {
    document.getElementById('student-progress-container').style.display = 'none';
}

// Função para exibir o contêiner de progresso do estudante
function showStudentProgressContainer() {
    hideAllContainers();  // Ocultar outros contêineres quando o progresso do estudante for exibido
    document.getElementById('student-progress-container').style.display = 'block';
    loadStudents();  // Carregar a lista de estudantes no select
}

// Função para ocultar o contêiner de progresso do estudante e outros
function hideAllContainers() {
    document.getElementById('student-progress-container').style.display = 'none';
}
