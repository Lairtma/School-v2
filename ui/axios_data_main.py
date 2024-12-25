from api.school_api import *

LESSONS_NUM_TIME = [
            "1\n8:00–8:45", "2\n8:55–9:40", "3\n9:55–10:40",
            "4\n10:55–11:40", "5\n12:00–12:45", "6\n12:55–13:40",
            "7\n13:50–14:35", "8\n14:45–15:30", "9\n15:40–16:25"
        ]

CLASSES_LIST = ClassGetAll()

WEEK_DAYS = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье"
        ]

SUBJECTS_LIST = SubjectGetAll()

TEACHERS = TeacherGetAll()

TEACHERS_LIST = TEACHERS
ROOMS_LIST = ["232", "233", "234", "235"]

PLACES = ClassRoomGetAll()
PLACES.append("")

