# Queries Utilizadas no Sistema

## 1. Visualização Geral de Dados
- **Query**: `r.keys('*')`
- **Descrição**: Retorna todas as chaves armazenadas no Redis.
- **Função**: `view_all()`

## 2. Adicionar um Valor ao Redis
- **Query**: `r.set(key, value)`
- **Descrição**: Insere uma chave-valor no Redis.
- **Função**: `set_value()`

## 3. Adicionar Estudante à Lista
- **Query**: `r.rpush('students', value)`
- **Descrição**: Adiciona um estudante à lista `students` no Redis.
- **Função**: `set_value()` (quando a chave for `students`)

## 4. Obter Estudantes
- **Query**: `r.lrange('students', 0, -1)`
- **Descrição**: Retorna a lista de todos os estudantes.
- **Função**: `get_students()`

## 5. Obter Progresso do Estudante
- **Queries**:
  - `r.lrange(f'student:{student_name}:courses', 0, -1)` (para obter os cursos do estudante)
  - `r.scan_iter('activity:*')` (para verificar as atividades de cada curso do estudante)
- **Descrição**: Retorna o progresso do estudante (atividades completas e incompletas).
- **Função**: `get_student_course_progress(student_name)`

## 6. Atividades Futuras de Estudantes
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Varre todas as atividades e verifica quais têm datas de vencimento no futuro.
- **Função**: `get_students_with_upcoming_activities()`

## 7. Cursos com Atividades Incompletas
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Varre todas as atividades e verifica quais não estão concluídas, retornando os cursos com atividades incompletas.
- **Função**: `get_courses_with_incomplete_activities()`

## 8. Média de Idade por Curso
- **Queries**:
  - `r.lrange('courses', 0, -1)` (para obter os cursos)
  - `r.lrange(f'student:{student}:courses', 0, -1)` (para obter os cursos de cada estudante)
  - `r.hgetall(f'student:{student}:details')` (para obter a idade de cada estudante)
- **Descrição**: Calcula a média de idade dos estudantes por curso.
- **Função**: `calculate_average_age_per_course()`

## 9. Atividades Atrasadas por Estudante
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Varre todas as atividades para identificar as que estão atrasadas (data de vencimento no passado e não concluídas).
- **Função**: `find_overdue_activities_per_student()`

## 10. Top 3 Estudantes de Ciência da Computação por Atividades Concluídas
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Conta o número de atividades concluídas por estudante nos cursos de Ciência da Computação e retorna os três primeiros.
- **Função**: `top_3_cs_students_by_completed_activities()`

## 11. Curso com Maior Proporção de Atividades Atrasadas
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Calcula a proporção de atividades atrasadas para cada curso e retorna o curso com a maior proporção de atrasos.
- **Função**: `course_with_highest_overdue_ratio()`

## 12. Atividade Mais Atrasada por Curso e Número de Estudantes Atrasados
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Retorna a atividade mais atrasada em cada curso e o número de estudantes atrasados para essa atividade.
- **Função**: `most_overdue_activity_per_course_and_num_students()`
