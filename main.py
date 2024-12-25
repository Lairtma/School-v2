from api.excel_api import export_from_xml
import _sqlite3
from ui.main import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
db_name = "School.db"
xml_name = "fff.xml"

if __name__ == '__main__':
    try:
        connection = _sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        # Удаление всех записей
        tables = [
            "room", "discipline", "class", "teacher", 
            "teacher_and_discipline", "teacher_and_room", 
            "default_schedule", "changes_in_schedule"
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table};")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

        connection.commit()  # Применяем изменения
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        connection.close()  # Закрываем соединение

    export_from_xml(db_name, xml_name)  # Экспортируем данные из XML
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())