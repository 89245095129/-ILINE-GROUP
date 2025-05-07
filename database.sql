
-- Таблица должностей
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 5)
);

-- Таблица сотрудников
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position_id INTEGER NOT NULL REFERENCES positions(id),
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    manager_id INTEGER REFERENCES employees(id)
);

-- Индексы для ускорения поиска
CREATE INDEX idx_employees_position ON employees(position_id);
CREATE INDEX idx_employees_manager ON employees(manager_id);