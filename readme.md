# Queries Utilizadas no Sistema

## 1. Visualização Geral de Dados
- **Query**: `r.keys('*')`
- **Descrição**: Retorna todas as chaves armazenadas no Redis para exibir as informações contidas no banco.

## 2. Adicionar um Valor ao Redis
- **Query**: `r.set(key, value)`
- **Descrição**: Insere ou atualiza uma chave-valor no Redis para armazenar dados simples.

## 3. Adicionar Estudante à Lista
- **Query**: `r.rpush('students', value)`
- **Descrição**: Adiciona um estudante à lista de estudantes no Redis.

## 4. Obter Estudantes
- **Query**: `r.lrange('students', 0, -1)`
- **Descrição**: Retorna todos os estudantes cadastrados no Redis.

## 5. Obter Progresso do Estudante
- **Queries**: 
  - `r.lrange(f'student:{student_name}:courses', 0, -1)`
  - `r.scan_iter('activity:*')`
- **Descrição**: Retorna o progresso de um estudante em seus cursos, com atividades completas e incompletas.

## 6. Atividades Futuras de Estudantes
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Verifica as atividades que ainda não venceram e as associa aos estudantes.

## 7. Cursos com Atividades Incompletas
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Retorna os cursos que têm atividades incompletas no Redis.

## 8. Média de Idade por Curso
- **Queries**:
  - `r.lrange('courses', 0, -1)`
  - `r.lrange(f'student:{student}:courses', 0, -1)`
  - `r.hgetall(f'student:{student}:details')`
- **Descrição**: Calcula a média de idade dos estudantes em cada curso.

## 9. Atividades Atrasadas por Estudante
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Identifica atividades atrasadas e as associa aos estudantes responsáveis.

## 10. Top 3 Estudantes de Ciência da Computação por Atividades Concluídas
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Retorna os três estudantes de Ciência da Computação com mais atividades concluídas.

## 11. Curso com Maior Proporção de Atividades Atrasadas
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Calcula a proporção de atividades atrasadas para cada curso e identifica o curso com a maior taxa de atrasos.

## 12. Atividade Mais Atrasada por Curso e Número de Estudantes Atrasados
- **Query**: `r.scan_iter('activity:*')`
- **Descrição**: Retorna a atividade mais atrasada de cada curso e o número de estudantes atrasados.
