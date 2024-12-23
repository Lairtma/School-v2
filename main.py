from ui.main import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
from api.excel_api import export_from_xml

db_name = "School.db"
xml_name = "fff.xml"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())