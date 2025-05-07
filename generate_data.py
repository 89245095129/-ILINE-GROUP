
import psycopg2
from faker import Faker
import random

# Настройки подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'database': 'employee_db',
    'user': 'postgres',
    'password': 'пароль'
}

fake = Faker('ru_RU')

def generate_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Очищаем таблицы
    cursor.execute("TRUNCATE TABLE employees, positions RESTART IDENTITY CASCADE")
    
    # Добавляем должности
    positions = [
        ("Генеральный директор", 1),
        ("Директор департамента", 2),
        ("Руководитель отдела", 3),
        ("Менеджер проекта", 4),
        ("Специалист", 5)
    ]
    
    for title, level in positions:
        cursor.execute("INSERT INTO positions (title, level) VALUES (%s, %s)", 
                      (title, level))
    
    # Генерируем CEO (без руководителя)
    cursor.execute(
        "INSERT INTO employees (first_name, last_name, position_id, hire_date, salary) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (fake.first_name(), fake.last_name(), 1, fake.date_between('-10y'), 300000)
    )
    ceo_id = cursor.fetchone()[0]
    
    # Генерируем остальных сотрудников (50 000)
    for i in range(50000):
        level = random.choices([2,3,4,5], weights=[0.05,0.15,0.3,0.5])[0]
        salary = round(random.uniform(30000, 300000), 2)
        
        cursor.execute(
            "INSERT INTO employees (first_name, last_name, position_id, hire_date, salary, manager_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (fake.first_name(), fake.last_name(), level, fake.date_between('-5y'), salary, ceo_id)
        )
    
    conn.commit()
    conn.close()
    print("Данные успешно сгенерированы!")

if __name__ == "__main__":
    generate_data()