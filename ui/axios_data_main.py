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

SUBJECTS_AND_TEACHERS = {
    SUBJECTS_LIST[key]:[
            TEACHERS[key % len(TEACHERS)],
            TEACHERS[(key + 1) % len(TEACHERS)]
        ] for key in range(len(SUBJECTS_LIST))
}




TEACHERS_LIST = TEACHERS # зачем??
ROOMS_LIST = ["232", "233", "234", "235"] # зачем??

PLACES = ClassRoomGetAll()
PLACES.append("")


LESSONS_TITLE_PLACE_TEACHER_CLASS = {
    WEEK_DAYS[1]: # день недели
    {
        CLASSES_LIST[0]: # класс
        { 
            1: # номер урока
                {
                "group_lesson" : False,
                "title_lesson" : SUBJECTS_LIST[0],
                "teacher" : TEACHERS[0],
                "places" : ""
                },
            2: 
                {
                    "group_lesson" : True,
                    "num_subgroups" : 2,
                    1: {
                        "title_lesson" : SUBJECTS_LIST[1],
                        "teacher" : TEACHERS[1],
                        "places" : PLACES[0]
                    },
                    2: {
                        "title_lesson" : SUBJECTS_LIST[2],
                        "teacher" : TEACHERS[2],
                        "places" : PLACES[1]
                    },
                }
        }
    },
}