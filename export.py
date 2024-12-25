import xml.etree.ElementTree as ET
import sqlite3 
db_name = "school.db"
xml_name = "fff (2).xml"
def export_from_xml(db_name, xml_name):
    """ЭКСПОРТ ДАННЫХ ИЗ КАКОЙ-ТО ХУЙНИ НЕПОНЯТНО ПОЧЕМУ CRYYYYY"""

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()


    tree = ET.parse('xml_name')
    root = tree.getroot()

    #предметы
    subject_id = {}
    subject_count = 1
    for elem in root.findall("./subjects/subject"):
        id = elem.get("id")
        subject_id[id] = subject_count
        subject_count += 1 
        name = elem.get("name")
        cursor.execute("INSERT INTO discipline (name) VALUES (?)", (name,))
    
    #учителя
    teacher_id = {}
    teacher_count = 1
    for elem in root.findall("./teachers/teacher"):
        id = elem.get("id")
        teacher_id[id] = teacher_count
        teacher_count += 1
        fio = elem.get("name")
        cursor.execute("INSERT INTO teacher (fio) VALUES (?)", (fio,))
    
    #аудитории
    classroom_id = {}
    classroom_count = 1
    for elem in root.findall("./classrooms/classroom"):
        id = elem.get("id")
        classroom_id[id] = classroom_count
        classroom_count += 1
        name = elem.get("name")
        if name == "БСЗ": capacity = 2.0
        elif name in ['301', '309', '310', '316', '320а']: capacity = 0.5
        else: capacity = 1.0
        cursor.execute("INSERT INTO room (name, capacity) VALUES (?, ?)", (name, capacity,))
    
    #классы
    class_id = {}
    class_count = 1
    for elem in root.findall("./classes/class"):
        id = elem.get("id")
        class_id[id] = class_count
        class_count += 1
        name = elem.get("name")
        cursor.execute("INSERT INTO class (name) VALUES (?)", (name,))
    
    #группы, пока предположительно только для поля mini_group 
    # group = {
    #     "id" : mini_group
    # }
    group = {}
    for elem in root.findall("./groups/group"):
        id = elem.get("id")
        group[id] = elem.get("name")
    
    #Я устал 
    lessons = {}
    for lesson in root.findall("./lessons/lesson"):
        lessons[lesson.get("id")] = {
            "subjectid": subject_id.get(lesson.get("subjectid")),
            "teacherids": teacher_id.get(lesson.get("teacherids")),
            "classids": class_id.get(lesson.get("classids")),
            "groupids": group.get(lesson.get("groupids"))
        }
    
    # Парсинг card и связывание с lesson
    schedule_entries = []
    for card in root.findall("./card"):
        lessonid = card.get("lessonid")
        lesson_data = lessons.get(lessonid)

        if not lesson_data:
            # Пропускаем card, если нет связанного lesson
            continue

        weekday_binary = card.get("days")  # Например: "10000" для понедельника
        weekday = weekday_binary.find("1") + 1  # Конвертация в номер дня (1 = Понедельник)

        # Проверка, если weekday невалиден
        if weekday == 0:
            continue

        period = int(card.get("period"))  # Номер урока
        classroomids = classroom_id.get(card.get("classroomids"))  # ID аудитории

        # Формируем запись для default_schedule
        schedule_entries.append({
            "weekday": weekday,
            "number_of_lesson": period,
            "teacher_id": lesson_data["teacherids"],
            "room_id": classroomids,
            "class_id": lesson_data["classids"],
            "mini_group": lesson_data["groupids"],
            "discipline_id": lesson_data["subjectid"]
        })