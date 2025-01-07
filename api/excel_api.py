import xml.etree.ElementTree as ET
import sqlite3



def export_from_xml(db_name, xml_name):
    """Экспорт данных из XML файла"""
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        tables = [
            "default_schedule"
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
            if result is None:
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

        for elem in root.findall("./groups/group"):
            xml_id = elem.get("id")
            name = elem.get("name")
            all_group_ids[xml_id] = name

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

            weekday_binary = card.get("days")
            weekday = weekday_binary.find("1") + 1
            if weekday == 0:
                continue

            period = int(card.get("period"))

            teacher_ids = lesson_data["teacherids"]
            group_ids = lesson_data["groupids"]
            class_ids = lesson_data["classids"]

            
            if not teacher_ids or not group_ids or not class_ids:                                                                       # Проверяем, что списки не пустые
                print(f"Ошибка: один из списков пуст (учителя, группы или классы) для урока {lessonid}")
                continue
            if len(class_ids) == 1 and len(group_ids) == 1 and len(teacher_ids) == 1:
                cls = class_ids[0]
                grs = group_ids[0]
                trs = teacher_ids[0]
                cursor.execute("""
                            INSERT INTO default_schedule (
                                weekday, number_of_lesson, teacher_id, room_id, class_id, mini_group, discipline_id
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                            weekday,
                            period,
                            trs,  
                            None,  
                            cls,
                            grs,  
                            lesson_data["subjectid"]
                        ))
            elif len(class_ids) == 1 and len(group_ids) == 1 and len(teacher_ids) > 1:
                # if group_ids[0] != 'Весь класс': print(lessonid)
                subgroups = [f"{i + 1} группа" for i in range(len(teacher_ids))]
                cls = class_ids[0]
                for i in range(len(teacher_ids)):
                    cursor.execute("""
                        INSERT INTO default_schedule (
                            weekday, number_of_lesson, teacher_id, room_id, class_id, mini_group, discipline_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                        weekday,
                        period,
                        teacher_ids[i],  
                        None,  
                        cls,
                        subgroups[i],  
                        lesson_data["subjectid"]
                    ))
            elif len(class_ids) == len(group_ids) and len(teacher_ids) == 1:
                trs = teacher_ids[0]
                for i in range(len(class_ids)):
                    cls = class_ids[i]
                    cursor.execute("""
                        INSERT INTO default_schedule (
                            weekday, number_of_lesson, teacher_id, room_id, class_id, mini_group, discipline_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                        weekday,
                        period,
                        trs, 
                        None,  
                        cls,
                        group_ids[i],  
                        lesson_data["subjectid"]
                    ))
            elif len(class_ids) == len(group_ids) and  len(teacher_ids) > 1:
                subgroups = [f"{i + 1} группа" for i in range(len(teacher_ids))]
                for i in range(len(class_ids)):
                    cls = class_ids[i]
                    for j in range(len(teacher_ids)):
                        trs = teacher_ids[j]
                        cursor.execute("""
                        INSERT INTO default_schedule (
                            weekday, number_of_lesson, teacher_id, room_id, class_id, mini_group, discipline_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                        weekday,
                        period,
                        trs, 
                        None,  
                        cls,
                        subgroups[j],  
                        lesson_data["subjectid"]
                    ))
            else:
                # Обработка случая, если длины class_ids и group_ids не совпадают
                if len(class_ids) == 1 and len(class_ids) < len(group_ids):
                    for i in range(len(group_ids)):
                        cls = class_ids[0]
                        grs = group_ids[i]
                        teacher_id = teacher_ids[0] if teacher_ids else None  #там всегда 1 учитель
                        cursor.execute("""
                            INSERT INTO default_schedule (
                                weekday, number_of_lesson, teacher_id, room_id, class_id, mini_group, discipline_id
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            weekday,
                            period,
                            teacher_id,
                            None,  # Аудитория, если не указана, записывается как NULL
                            cls,
                            grs,
                            lesson_data["subjectid"]
                        ))
                    # Повторяем классы для соответствия количеству групп
                elif len(class_ids) > len(group_ids):
                    print(f"Ошибка: длины классов ({len(class_ids)}) и групп ({len(group_ids)}) не совпадают для урока {lessonid}")
                    continue
                else:
                    print(lessonid)
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