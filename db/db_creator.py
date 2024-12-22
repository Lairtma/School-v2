from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
import os

# Путь к базе данных
db_path = "../School.db"

# Удаляем файл базы данных, если он существует (для тестирования)
if os.path.exists(db_path):
    os.remove(db_path)

# Создание и настройка базы данных
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(db_path)

if not db.open():
    print("Не удалось открыть базу данных")
    sys.exit(1)
else:
    print("База данных открыта")

# Создание таблиц
query = QSqlQuery()


create_discipline_table = """
CREATE TABLE IF NOT EXISTS discipline (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(100)
);
"""

create_class_table = """
CREATE TABLE IF NOT EXISTS class (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(10),
    mini_group INTEGER,
    discipline_id INTEGER,
    FOREIGN KEY (discipline_id) REFERENCES discipline (id)
);
"""

create_teacher_table = """
CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(50),
    surname VARCHAR(50),
    lastname VARCHAR(50)
);
"""

create_teacher_and_discipline_table = """
CREATE TABLE IF NOT EXISTS teacher_and_discipline (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    discipline_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (discipline_id) REFERENCES discipline (id)
);
"""

create_room_table = """
CREATE TABLE IF NOT EXISTS room (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    capacity INTEGER,
    name VARCHAR(50)
);
"""

create_teacher_and_room_table = """
CREATE TABLE IF NOT EXISTS teacher_and_room (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    room_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (room_id) REFERENCES room (id)
);
"""

create_default_schedule_table = """
CREATE TABLE IF NOT EXISTS default_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    weekday INTEGER,
    number_of_lesson INTEGER,
    teacher_id INTEGER,
    room_id INTEGER,
    class_id INTEGER,
    discipline_id INTEGER,
    date_create DATETIME,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (room_id) REFERENCES room (id),
    FOREIGN KEY (class_id) REFERENCES class (id),
    FOREIGN KEY (discipline_id) REFERENCES discipline (id)
);
"""

create_changes_in_schedule_table = """
CREATE TABLE IF NOT EXISTS changes_in_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    number_of_lesson INTEGER,
    teacher_id INTEGER,
    room_id INTEGER,
    class_id INTEGER,
    discipline_id INTEGER,
    date_lesson DATE,
    date_change DATETIME,
    is_created_by_user BOOLEAN,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (room_id) REFERENCES room (id),
    FOREIGN KEY (class_id) REFERENCES class (id),
    FOREIGN KEY (discipline_id) REFERENCES discipline (id)
);
"""


# Выполнение запросов для создания таблиц
if not query.exec_(create_discipline_table):
    print("Ошибка создания таблицы create_discipline_table: ", query.lastError().text())

if not query.exec_(create_class_table):
    print("Ошибка создания таблицы create_class_table: ", query.lastError().text())

if not query.exec_(create_teacher_table):
    print("Ошибка создания таблицы create_teacher_table: ", query.lastError().text())

if not query.exec_(create_teacher_and_discipline_table):
    print("Ошибка создания таблицы create_teacher_and_discipline_table: ", query.lastError().text())

if not query.exec_(create_room_table):
    print("Ошибка создания таблицы create_room_table: ", query.lastError().text())

if not query.exec_(create_teacher_and_room_table):
    print("Ошибка создания таблицы create_teacher_and_room_table: ", query.lastError().text())

if not query.exec_(create_default_schedule_table):
    print("Ошибка создания таблицы create_default_schedule_table: ", query.lastError().text())

if not query.exec_(create_changes_in_schedule_table ):
    print("Ошибка создания таблицы create_changes_in_schedule_table : ", query.lastError().text())






# Убедитесь, что база данных открыта и создана. 

# Функция для выполнения SQL запросов
def execute_query(query_string):
    query.prepare(query_string)
    if not query.exec_():
        print(f"Ошибка выполнения запроса: {query_string} - {query.lastError().text()}")

# Заполнение таблицы predmet
insert_discipline = """
INSERT INTO discipline (name) VALUES 
('Математика'), 
('Физика'), 
('Химия'), 
('История');
"""
execute_query(insert_discipline)

# Заполнение таблицы class
insert_class = """
INSERT INTO class (name, mini_group, discipline_id) VALUES 
('10А', 1, 1), 
('10Б', 1, 1), 
('11А', 1, 1), 
('11Б', 1, 1);
"""
execute_query(insert_class)

# Заполнение таблицы prepod
insert_teacher = """
INSERT INTO teacher (name, surname, lastname) VALUES 
('Иван', 'Иванов', 'Иванович'), 
('Петр', 'Петров', 'Петрович'), 
('Сидор', 'Сидоров', 'Сидорович');
"""
execute_query(insert_teacher)

# Заполнение таблицы prepod_and_predmet
insert_teacher_and_discipline = """
INSERT INTO teacher_and_discipline (discipline_id, teacher_id) VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 1);
"""
execute_query(insert_teacher_and_discipline)

# Заполнение таблицы kabinet
insert_room = """
INSERT INTO room (capacity, name) VALUES 
(30, 'Аудитория 1'), 
(30, 'Аудитория 2'), 
(30, 'Лаборатория 1');
"""
execute_query(insert_room)

# Заполнение таблицы prepod_and_kabinet
insert_teacher_and_room = """
INSERT INTO teacher_and_room (room_id, teacher_id) VALUES 
(1, 1), 
(2, 2), 
(3, 3);
"""
execute_query(insert_teacher_and_room)

# Заполнение таблицы default_schedule
insert_default_schedule = """
INSERT INTO default_schedule (weekday, number_of_lesson, teacher_id, room_id, class_id, discipline_id, date_create) VALUES 
(1, 1, 1, 1, 1, 1, '2023-10-03 08:00:00'), 
(1, 2, 2, 2, 1, 2, '2023-10-03 09:00:00'), 
(2, 1, 1, 1, 2, 3, '2023-10-04 08:00:00'), 
(2, 2, 2, 2, 2, 4, '2023-10-04 09:00:00');
"""
execute_query(insert_default_schedule)

# Заполнение таблицы changes_in_schedule
insert_changes_in_schedule = """
INSERT INTO changes_in_schedule (number_of_lesson, teacher_id, room_id, class_id, discipline_id, date_lesson, date_change, is_created_by_user) VALUES 
(1, 1, 1, 1, 1, '2023-10-03', '2023-10-02 15:00:00', true), 
(2, 2, 2, 2, 2, '2023-10-04', '2023-10-03 15:00:00', false);
"""
execute_query(insert_changes_in_schedule)

print("База данных успешно заполнена")





# Закрываем базу данных
db.close()

print("База данных и таблицы успешно созданы!")