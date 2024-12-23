import xml.etree.ElementTree as ET
import sqlite3




def export_from_xml(db_name, xml_name):
    """Экспорт данных из XML файла"""

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Парсинг XML
    tree = ET.parse(xml_name)
    root = tree.getroot()

    # Предметы
    subject_id = {}
    subject_count = 1
    for elem in root.findall("./subjects/subject"):
        id = elem.get("id")
        subject_id[id] = subject_count
        subject_count += 1
        name = elem.get("name")
        cursor.execute("INSERT INTO discipline (name) VALUES (?)", (name,))

    # Учителя
    teacher_id = {}
    teacher_count = 1
    for elem in root.findall("./teachers/teacher"):
        id = elem.get("id")
        teacher_id[id] = teacher_count
        teacher_count += 1
        fio = elem.get("name")
        cursor.execute("INSERT INTO teacher (fio) VALUES (?)", (fio,))

    # Аудитории
    classroom_id = {}
    classroom_count = 1
    for elem in root.findall("./classrooms/classroom"):
        id = elem.get("id")
        classroom_id[id] = classroom_count
        classroom_count += 1
        name = elem.get("name")
        if name == "БСЗ":
            capacity = 2.0
        elif name in ['301', '309', '310', '316', '320а']:
            capacity = 0.5
        else:
            capacity = 1.0
        cursor.execute("INSERT INTO room (name, capacity) VALUES (?, ?)", (name, capacity,))

    # Классы
    class_id = {}
    class_count = 1
    for elem in root.findall("./classes/class"):
        id = elem.get("id")
        class_id[id] = class_count
        class_count += 1
        name = elem.get("name")
        cursor.execute("INSERT INTO class (name) VALUES (?)", (name,))

    # Группы
    group = {}
    for elem in root.findall("./groups/group"):
        id = elem.get("id")
        group[id] = elem.get("name")

    # Уроки
    lessons = {}
    for lesson in root.findall("./lessons/lesson"):
        lesson_id = lesson.get("id")
        # Разделяем массивы на списки
        subjectid = subject_id.get(lesson.get("subjectid"))
        teacherids = [teacher_id.get(tid) for tid in lesson.get("teacherids", "").split(",") if tid]
        classids = [class_id.get(cid) for cid in lesson.get("classids", "").split(",") if cid]
        groupids = [group.get(gid) for gid in lesson.get("groupids", "").split(",") if gid]

        lessons[lesson_id] = {
            "subjectid": subjectid,
            "teacherids": teacherids,
            "classids": classids,
            "groupids": groupids
        }

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
        classroomids = [classroom_id.get(cid) for cid in card.get("classroomids", "").split(",") if cid]

        # Вставка записей для каждой комбинации учителя, класса, группы и аудитории
        for teacher in lesson_data["teacherids"]:
            for cls in lesson_data["classids"]:
                for grp in lesson_data["groupids"]:
                    for room in classroomids or [None]:  # Если аудитории нет, вставляем None
                        cursor.execute("""
                            INSERT INTO default_schedule (
                                weekday, number_of_lesson, teacher_id, room_id, class_id, mini_group, discipline_id
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

    # Сохранение изменений и закрытие подключения
    connection.commit()
    connection.close()
