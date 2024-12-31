import xml.etree.ElementTree as ET
import sqlite3
import numpy as np



def export_from_xml(db_name, xml_name):
    """Экспорт данных из XML файла"""
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        tables = [
            "teacher_and_discipline", "teacher_and_room", 
            "default_schedule", "changes_in_schedule"
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table};")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

        # Парсинг XML

        tree = ET.parse(xml_name)
        root = tree.getroot()

        discipline_classes_map = {} 
        class_grades = {}

        # Предметы

        all_subject_ids = {}
        cursor.execute("SELECT MAX(id) FROM discipline")
        max_subject_id = cursor.fetchone()[0] or 0
        subject_id = max_subject_id + 1

        for elem in root.findall("./subjects/subject"):
            xml_id = elem.get("id")
            name = elem.get("short")
            cursor.execute("SELECT id FROM discipline WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO discipline (id, name) VALUES (?, ?)", (subject_id, name))
                all_subject_ids[xml_id] = subject_id
                subject_id += 1
            else:
                current_id = result[0]
                all_subject_ids[xml_id] = current_id



        # Учителя

        all_teacher_ids = {}
        cursor.execute("SELECT MAX(id) FROM teacher")
        max_teacher_id = cursor.fetchone()[0] or 0
        teacher_id = max_teacher_id + 1

        for elem in root.findall("./teachers/teacher"):
            xml_id = elem.get("id")
            fio = elem.get("name")
            cursor.execute("SELECT id FROM teacher WHERE fio = ?", (fio,))
            result = cursor.fetchone()
            if result in None:
                cursor.execute("INSERT INTO teacher (fio) VALUES (?)", (fio,))
                all_teacher_ids[xml_id] = teacher_id
                teacher_id += 1
            else:
                current_id = result[0]
                all_teacher_ids[xml_id] = current_id



        # Аудитории

        all_classroom_ids = {}
        cursor.execute("SELECT MAX(id) FROM room")
        max_room_id = cursor.fetchone()[0] or 0
        classroom_id = max_room_id + 1

        for elem in root.findall("./classrooms/classroom"):
            id = elem.get("id")
            name = elem.get("name")
            if name == "БСЗ":
                capacity = 2.0
            elif name in ['301', '309', '310', '316', '320а']:
                capacity = 0.5
            else:
                capacity = 1.0
            cursor.execute("SELECT id FROM room WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO room (name, capacity) VALUES (?, ?)", (name, capacity))
                all_classroom_ids[xml_id] = classroom_id
                classroom_id += 1
            else:
                current_id = result[0]
                all_teacher_ids[xml_id] = current_id

         # Классы
        all_class_ids = {}
        cursor.execute("SELECT MAX(id) FROM class")
        max_class_id = cursor.fetchone()[0] or 0
        class_id = max_class_id + 1

        for elem in root.findall("./classes/class"):
            xml_id = elem.get("id")
            grade = elem.get("grade")
            class_grades[xml_id] = grade
            name = elem.get("name")
            cursor.execute("SELECT id FROM class WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO class (id, name) VALUES (?, ?)", (class_id, name))
                all_class_ids[xml_id] = class_id
                class_id += 1
            else:
                current_id = result[0]
                all_class_ids[xml_id] = current_id



        # Группы

        all_group_ids = {}
        cursor.execute("SELECT MAX(id) FROM group")
        max_group_id = cursor.fetchone()[0] or 0
        group_id = max_group_id + 1

        for elem in root.findall("./groups/group"):
            xml_id = elem.get("id")
            name = elem.get("name")
            cursor.execute("SELECT id FROM group WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO group (id, name) VALUES (?, ?)", (group_id, name))
                all_group_ids[xml_id] = group_id
                group_id += 1
            else:
                current_id = result[0]
                all_group_ids[xml_id] = current_id



        # Уроки

        lessons = {}
        for lesson in root.findall("./lessons/lesson"):
            lesson_id = lesson.get("id")
            # Разделяем массивы на списки
            subject_id = all_subject_ids.get(lesson.get("subjectid"))
            teacherids = [all_teacher_ids.get(tid) for tid in lesson.get("teacherids", "").split(",") if tid]
            classids = [all_class_ids.get(cid) for cid in lesson.get("classids", "").split(",") if cid]
            groupids = [all_group_ids.get(gid) for gid in lesson.get("groupids", "").split(",") if gid]
            lessons[lesson_id] = {
                "subjectid": subject_id,
                "teacherids": teacherids, 
                "classids": classids,
                "groupids": groupids
            }
            if subject_id:
                if subject_id not in discipline_classes_map:
                    discipline_classes_map[subject_id] = set()
                discipline_classes_map[subject_id].update(classids)




        # Карточки расписания
        for card in root.findall("./cards/card"):
            lessonid = card.get("lessonid")
            lesson_data = lessons.get(lessonid)

            if not lesson_data:
                continue

            weekday_binary = card.get("days")  # Например: "10000" для понедельника
            weekday = weekday_binary.find("1") + 1  # Конвертация в номер дня (1 = Понедельник)

            if weekday == 0:
                continue

            period = int(card.get("period"))  # Номер урока
            classroomids = [all_classroom_ids.get(cid) for cid in card.get("classroomids", "").split(",") if cid]

            # Вставка записей для каждой комбинации учителя, класса, группы и аудитории
            for teacher in lesson_data["teacherids"]:
                for cls in lesson_data["classids"]:
                    for grp in lesson_data["groupids"]:
                        for room in classroomids or [None]:  # Если аудитории нет, вставляем None
                            cursor.execute("""
                                INSERT INTO default_schedule (
                                    weekday, number_of_lesson, all_teacher_ids, room_id, class_id, mini_group, discipline_id
                                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                weekday,
                                period,
                                teacher,
                                room,
                                cls,
                                grp,
                                lesson_data["subjectid"]
                            ))
        # Обновление таблицы discipline с классами
        for discipline_id, class_grades_set in discipline_classes_map.items():
            # Преобразуем множество классов в строку, разделённую запятыми
            class_grades_str = ", ".join(map(str, sorted(class_grades_set)))
            cursor.execute("UPDATE discipline SET classes = ? WHERE id = ?", (class_grades_str, discipline_id))
            
    except Exception as e:
        print(f'ошибка: {e}')
        return -1
    finally:
        connection.commit()
        connection.close()