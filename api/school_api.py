from datetime import datetime, date
import sqlite3

path_to_db = "School.db"

def PrepareInformationForMainPage(date):
    schedule = dict()
    all_classes = ClassGetAll()
    for clas in all_classes:
        schedule[clas] = dict()
    defaultSchedule = DefaultScheduleGetLessonByWeekday(date.weekday() + 1)
    changeSchedule = ChangesInScheduleGetLessonByDate(date)
    for default in defaultSchedule:
        class_name = ClassGetById(default[5])[1]
        place = ClassRoomGetById(default[4])[2]
        teacher = TeacherGetById(default[3])[1]
        subject = SubjectGetById(default[7])[1]
        if class_name in schedule:
            schedule[class_name][default[2] - 1] = {"group_lesson": False, "places": place, "teacher": teacher,
                                                "title_lesson": subject, "id": default[0], "type": "default"}
        else:
            schedule[class_name] = dict()
            schedule[class_name][default[2] - 1] = {"group_lesson": False, "places": place, "teacher": teacher,
                                                "title_lesson": subject, "id": default[0], "type": "default"}
    for default in changeSchedule:
        class_name = ClassGetById(default[4])[1]
        place = ClassRoomGetById(default[3])[2]
        teacher = TeacherGetById(default[2])[1]
        subject = SubjectGetById(default[6])[1]
        if class_name in schedule:
            schedule[class_name][default[1] - 1] = {"group_lesson": False, "places": place, "teacher": teacher,
                                                "title_lesson": subject, "id": default[0], "type": "change"}
        else:
            schedule[class_name] = dict()
            schedule[class_name][default[1] - 1] = {"group_lesson": False, "places": place, "teacher": teacher,
                                                "title_lesson": subject, "id": default[0], "type": "change"}
    return schedule

def ClassGetIdByName(name: str):
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM class WHERE name = ?", (name,))
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names[0]
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def DefaultScheduleGetByWeekdayNumberClass(weekday:int, number: int, class_id: int):
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM default_schedule WHERE number_of_lesson = ? and class_id = ? and weekday = ?", (number, class_id, weekday))
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names[0]
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def ChangeInScheduleGetByNumberClassDate(number: int, class_id: int, date_of_lesson: date):
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        date_lesson_str = date_of_lesson.strftime('%Y-%m-%d')
        cursor.execute("SELECT id FROM changes_in_schedule WHERE DATE(date_lesson) = ? and number_of_lesson = ? and class_id = ?", (date_lesson_str, number, class_id))
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names[0]
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()


def SubjectGetIdByName(name: str):
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM discipline WHERE name = ?", (name,))
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names[0]
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def TeacherGetIdByName(name: str):
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM teacher WHERE fio = ?", (name,))
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names[0]
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def ClassRoomGetIdByName(name: str):
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM room WHERE name = ?", (name,))
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names[0]
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def ClassRoomGetAll() -> list:
    """Получить список всех имен комнат из таблицы room"""
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT name FROM room")
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def ClassGetAll() -> list:
    """Получить список всех имен комнат из таблицы room"""
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT name FROM class")
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def ClassGetById(id: int) -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM class WHERE id = ?", (id,))
    lessons = cursor.fetchall()
    connection.close()
    return lessons[0]

def SubjectGetById(id: int) -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM discipline WHERE id = ?", (id,))
    lessons = cursor.fetchall()
    connection.close()
    return lessons[0]

def SubjectGetAll() -> list:
    """Получить список всех имен комнат из таблицы room"""
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT name FROM discipline")
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def TeacherGetAll() -> list:
    """Получить список всех имен комнат из таблицы room"""
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT fio FROM teacher")
        names = [row[0] for row in cursor.fetchall()]  # Извлекаем все строки и берем первый элемент каждой строки
        return names
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []
    finally:
        connection.close()

def ClassRoomGetById(id: int) -> list:
    if id == None:
        return [0, 0, "неопределено"]
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM room WHERE id = ?", (id,))
    lessons = cursor.fetchall()
    connection.close()
    return lessons[0]

def DefaultScheduleAddLesson(weekday: int, number_of_lesson: int, teacher_id: int, classroom_id: int, class_id: int,
                             subject_id: int) -> int:
    if not weekday:
        return -1
    if not number_of_lesson:
        return -1
    if not teacher_id:
        return -1
    if not classroom_id:
        return -1
    if not class_id:
        return -1
    if not subject_id:
        return -1
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO default_schedule (weekday, number_of_lesson, teacher_id, room_id, class_id, discipline_id) VALUES (?, ?, ?, ?, ?, ?)",
        (weekday, number_of_lesson, teacher_id, classroom_id, class_id, subject_id))
    connection.commit()
    last_inserted_id = cursor.lastrowid
    connection.close()
    return last_inserted_id  # id созданного урока


def DefaultScheduleGetLessonById(id: int) -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM default_schedule WHERE id = ?", (id,))
    lessons = cursor.fetchall()
    connection.close()
    return lessons

def DefaultScheduleGetLessonByWeekday(weekday: int) -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM default_schedule WHERE weekday = ?", (weekday,))
    lessons = cursor.fetchall()
    connection.close()
    return lessons


def DefaultScheduleGetLessons() -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM default_schedule")
    lessons = cursor.fetchall()
    connection.close()
    return lessons


def DefaultScheduleChangeLessonById(id: int, weekday: int = None, number_of_lesson: int = None, teacher_id: int = None,
                                    classroom_id: int = None, class_id: int = None, subject_id: int = None) -> bool:
    lesson = DefaultScheduleGetLessonById(id)[0]
    if not weekday:
        weekday = lesson[1]
    if not number_of_lesson:
        number_of_lesson = lesson[2]
    if not teacher_id:
        teacher_id = lesson[3]
    if not classroom_id:
        classroom_id = lesson[4]
    if not class_id:
        class_id = lesson[5]
    if not subject_id:
        subject_id = lesson[6]
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE default_schedule SET weekday = ?, number_of_lesson = ?, teacher_id = ?, room_id = ?, class_id = ?, discipline_id = ?, date_create = ? WHERE id = ?",
        (weekday, number_of_lesson, teacher_id, classroom_id, class_id, subject_id, datetime.now(), id))
    connection.commit()
    connection.close()
    return True  # удалось поменять или нет


def DefaultScheduleDeleteLessonById(id: int) -> bool:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM default_schedule WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return True  # удалось удалить или нет


def TeacherAdd(fio: str) -> int:
    """Добавление нового учителя"""
    if not fio:
        return -1
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO teacher (fio)  VALUES (?)",(fio,))
        id = cursor.lastrowid
        connection.commit()
        connection.close()
        return id  # id добавленного учителя
    except Exception as e:
        print(f"Ошибка: {e}")
        return -1

def TeacherGetById(id: int) -> int:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM teacher WHERE id = ?", (id,))
        teachers = cursor.fetchall()
        return teachers[0]
    except Exception as e:
        print(f"Ошибка: {e}")
        return []
    finally:
        connection.close()


def TeacherChangeById(id: int, fio: str) -> bool:
    """Изменение информации об учителе"""
    table_name = "teacher"
    try:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        query = f"UPDATE {table_name} SET fio = ? WHERE id = ?"
        cursor.execute(query, (fio, id))
        connection.commit()
        connection.close()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Ошибка обновления предмета: {e}")
        return False


def TeacherDeleteById(id: int) -> bool:
    """Удаление учителя"""
    table_name = "teacher"
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()

    try:
        cursor.execute(f'DELETE FROM {table_name} WHERE id = ?', (id,))
        connection.commit()
        connection.close()
        return True # удалось удалить или нет
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def SubjectAdd(name: str) -> int:
    table_name = "discipline"
    """Добавление нового предмета в таблицу."""
    if not name:
        return -1  # Возвращаем -1, если имя не указано
    try:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} (name) VALUES (?)", (name,))
        id = cursor.lastrowid  # Получаем ID добавленной строки
        connection.commit()
        connection.close()
        return id
    except Exception as e:
        print(f"Ошибка добавления предмета: {e}")
        return -1

def SubjectChangeById(id: int, name: str) -> bool:
    table_name = "discipline"
    """Обновление названия предмета по ID."""
    if not id or not name:
        return False
    try:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        query = f"UPDATE {table_name} SET name = ? WHERE id = ?"
        cursor.execute(query, (name, id))
        connection.commit()
        connection.close()
        return cursor.rowcount > 0  # Возвращаем True, если строки были обновлены
    except Exception as e:
        print(f"Ошибка обновления предмета: {e}")
        return False


def SubjectDeleteById(id: int) -> bool:
    """Удаление предмета по ID."""
    table_name = "discipline"
    if not id:
        return False
    try:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        query = f"DELETE FROM {table_name} WHERE id = ?"
        cursor.execute(query, (id,))
        connection.commit()
        connection.close()
        return cursor.rowcount > 0  # Возвращаем True, если строки были удалены
    except Exception as e:
        print(f"Ошибка удаления предмета: {e}")
        return False


def ClassRoomAdd(name: str, capacity: float=None) -> int:
    if not capacity:
        capacity = 1
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO room (name, capacity) VALUES (?, ?)", (name, capacity))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return -1
    finally:
        connection.close()


def ClassRoomChangeById(id: int, name: str, capacity: float) -> bool:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE room SET name = ?, capacity = ? WHERE id = ?", (name, capacity, id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return False
    finally:
        connection.close()


def ClassRoomDeleteById(id: int) -> bool:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM room WHERE id = ?", (id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return False
    finally:
        connection.close()


def TeacherAndClassRoomAdd(classroom_id: int, teacher_id: int) -> int:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO teacher_and_room (room_id, teacher_id) VALUES (?, ?)", (classroom_id, teacher_id))
        teacher_and_room_add = cursor.fetchall()
        last_inserted_id = cursor.lastrowid
        return last_inserted_id
    except Exception as e:
        print(f"Ошибка: {e}")
        return -1
    finally:
        connection.close()


import sqlite3

def TeacherAndClassRoomChangeById(id: int, classroom_id: int, teacher_id: int) -> bool:
    try:
        with sqlite3.connect(path_to_db) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE teacher_and_room SET room_id = ?, teacher_id = ? WHERE id = ?",
                (classroom_id, teacher_id, id),
            )
            connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        connection.close()


def TeacherAndClassRoomDeleteById(id: int) -> bool:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM teacher_and_room WHERE id = ?", (id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        connection.close()


def ChangesInScheduleGetLessonById(id: int) -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM changes_in_schedule WHERE id = ?", (id,))
        lessons = cursor.fetchall()
        return lessons
    except Exception as e:
        print(f"Ошибка: {e}")
        return []
    finally:
        connection.close()


def ChangesInScheduleGetLessonByDate(date_lesson: date) -> list:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        # Преобразуем date_lesson в строку формата 'YYYY-MM-DD'
        date_lesson_str = date_lesson.strftime('%Y-%m-%d')

        cursor.execute("SELECT * FROM changes_in_schedule WHERE DATE(date_lesson) = ?", (date_lesson_str,))
        lessons = cursor.fetchall()
        return lessons
    except Exception as e:
        print(f"Ошибка: {e}")
        return []
    finally:
        connection.close()


def ChangeInScheduleAdd(number_of_lesson: int, teacher_id: int, classroom_id: int, class_id: int, subject_id: int,
                        lesson_date: date, mini_group, id_in_default: int) -> int:
    if (
            not number_of_lesson or not teacher_id or not classroom_id or not class_id or not subject_id or not lesson_date):
        return -1
    else:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO changes_in_schedule ("
                           "number_of_lesson, "
                           "teacher_id, "
                           "room_id, "
                           "class_id, "
                           "discipline_id, "
                           "date_lesson, "
                           "mini_group, "
                           "id_in_default_schedule)"
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (
                               number_of_lesson,
                               teacher_id,
                               classroom_id,
                               class_id,
                               subject_id,
                               lesson_date,
                               mini_group,
                               id_in_default,
                               ))
            connection.commit()
            last_inserted_id = cursor.lastrowid
            return last_inserted_id
        except Exception as e:
            print(f"Ошибка: {e}")
            return -1
        finally:
            connection.close()


def ChangeInScheduleChangeById(id: int,
                               number_of_lesson: int = None,
                               teacher_id: int = None,
                               classroom_id: int = None,
                               class_id: int = None,
                               subject_id: int = None,
                               lesson_date: date = None) -> bool:
    lesson = ChangesInScheduleGetLessonById(id)[0]
    if number_of_lesson is None:
        number_of_lesson = lesson[1]
    if teacher_id is None:
        teacher_id = lesson[2]
    if classroom_id is None:
        classroom_id = lesson[3]
    if class_id is None:
        class_id = lesson[4]
    if subject_id is None:
        subject_id = lesson[6]
    if lesson_date is None:
        lesson_date = lesson[7]

    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE changes_in_schedule "
                       "SET number_of_lesson = ?, "
                       "teacher_id = ?, "
                       "room_id = ?, "
                       "class_id = ?, "
                       "discipline_id = ?, "
                       "date_lesson = ? WHERE id = ?",
                       (
                           number_of_lesson,
                           teacher_id,
                           classroom_id,
                           class_id,
                           subject_id,
                           lesson_date,
                           id,
                       ))
        connection.commit()
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        connection.close()


def ChangeInScheduleDeleteById(id: int) -> bool:
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM changes_in_schedule WHERE id = ?", (id,))
        if cursor.rowcount > 0:
            connection.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        connection.close()


def ClassRoomGetEmpty(number_of_lesson: int, lesson_date: date) -> list:
    return []  # возвращает список пустых аудиторий в конкретный день и номер урока


def ClassRoomReCalculate(number_of_lesson: int, lesson_date: date) -> bool:
    return True  # пересчитывает кабинеты для уроков в определённый урок и день


if __name__ == "__main__":
    PrepareInformationForMainPage(date(2024, 12, 17))