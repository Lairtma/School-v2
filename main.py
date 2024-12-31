from api.excel_api import export_from_xml
import _sqlite3
from ui.main import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
db_name = "School.db"
xml_name = "fff.xml"

if __name__ == '__main__':
    
    export_from_xml(db_name, xml_name)  # Экспортируем данные из XML
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())