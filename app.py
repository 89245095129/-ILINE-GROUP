
import psycopg2
from tabulate import tabulate
import click

# Настройки подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'database': 'employee_db',
    'user': 'postgres',
    'password': 'пароль'
}

@click.group()
def cli():
    pass

@cli.command()
def generate():
    """Сгенерировать тестовые данные"""
    from generate_data import generate_data
    generate_data()

@cli.command()
@click.option('--level', type=int, help='Уровень должности')
def list(level):
    """Список сотрудников"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    query = """
        SELECT e.id, e.first_name, e.last_name, p.title, e.hire_date, e.salary 
        FROM employees e
        JOIN positions p ON e.position_id = p.id
    """
    
    if level:
        query += f" WHERE p.level = {level}"
    
    cursor.execute(query)
    employees = cursor.fetchall()
    
    print(tabulate(
        employees,
        headers=['ID', 'Имя', 'Фамилия', 'Должность', 'Дата приема', 'Зарплата'],
        tablefmt='psql'
    ))
    
    conn.close()

@cli.command()
@click.argument('employee_id', type=int)
def tree(employee_id):
    """Показать иерархию сотрудника"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""
        WITH RECURSIVE hierarchy AS (
            SELECT id, first_name, last_name, position_id, manager_id, 0 AS level
            FROM employees WHERE id = %s
            UNION ALL
            SELECT e.id, e.first_name, e.last_name, e.position_id, e.manager_id, h.level + 1
            FROM employees e
            JOIN hierarchy h ON e.manager_id = h.id
        )
        SELECT h.id, h.first_name, h.last_name, p.title, h.level
        FROM hierarchy h
        JOIN positions p ON h.position_id = p.id
        ORDER BY h.level
    """, (employee_id,))
    
    for emp in cursor.fetchall():
        print("    " * emp[4] + f"{emp[0]}: {emp[1]} {emp[2]} ({emp[3]})")
    
    conn.close()

if __name__ == '__main__':
    cli()