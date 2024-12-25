from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
import os

# Путь к базе данных
db_path = "School.db"

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
    name VARCHAR(100),
    classes VARCHAR(500)
);
"""

create_class_table = """
CREATE TABLE IF NOT EXISTS class (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name VARCHAR(10)
);
"""

create_teacher_table = """
CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    fio VARCHAR(50)
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
    capacity FLOAT,
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
    mini_group VARCHAR(50),
    discipline_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (room_id) REFERENCES room (id),
    FOREIGN KEY (class_id) REFERENCES class (id),
    FOREIGN KEY (discipline_id) REFERENCES discipline (id)
);
"""

create_schedule_w_changes_table = """
CREATE TABLE IF NOT EXISTS schedule_w_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    weekday INTEGER,
    number_of_lesson INTEGER,
    teacher_id INTEGER,
    room_id INTEGER,
    class_id INTEGER,
    mini_group VARCHAR(50),
    discipline_id INTEGER,
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
    mini_group VARCHAR(50),
    discipline_id INTEGER,
    date_lesson DATE,
    id_in_default_schedule INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
    FOREIGN KEY (room_id) REFERENCES room (id),
    FOREIGN KEY (class_id) REFERENCES class (id),
    FOREIGN KEY (discipline_id) REFERENCES discipline (id),
    FOREIGN KEY (id_in_default_schedule) REFERENCES default_schedule (id)
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

if not query.exec_(create_schedule_w_changes_table):
    print("Ошибка создания таблицы create_schedule_w_changes_table : ", query.lastError().text())

if not query.exec_(create_changes_in_schedule_table ):
    print("Ошибка создания таблицы create_changes_in_schedule_table : ", query.lastError().text())


db.close()

print("База данных и таблицы успешно созданы!")