import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

# Пример данных для учителей и кабинетов
TEACHERS_LIST = ["Иванов А.П.", "Петров Б.В.", "Сидоров С.Д."]
ROOMS_LIST = ["232", "233", "234", "235"]

class TeacherRoomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учитель - Кабинет")
        self.setFixedSize(600, 400)

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")

        # Заголовок
        header_label = QLabel("Учитель - Кабинет")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                background-color: #1F6467;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        central_layout.addWidget(header_label)

        # Поля для выбора учителя и кабинета
        form_layout = QVBoxLayout()

        self.teacher_combobox = self.create_form_row("Учитель:", TEACHERS_LIST)
        self.room_combobox = self.create_form_row("Кабинет:", ROOMS_LIST)

        form_layout.addLayout(self.teacher_combobox)
        form_layout.addLayout(self.room_combobox)
        central_layout.addLayout(form_layout)

        # Пространство перед кнопками
        central_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки "Назад" и "Сохранить"
        button_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        save_button = QPushButton("Сохранить")

        back_button.setFixedSize(120, 40)
        save_button.setFixedSize(120, 40)

        back_button.setStyleSheet(self.button_style())
        save_button.setStyleSheet(self.button_style())

        back_button.clicked.connect(self.go_back)
        save_button.clicked.connect(self.save_teacher_room)

        button_layout.addWidget(back_button)
        button_layout.addStretch()
        button_layout.addWidget(save_button)

        central_layout.addLayout(button_layout)

    def button_style(self):
        """Стиль для кнопок"""
        return """
            QPushButton {
                background-color: #1F6467;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #154A4D;
            }
        """

    def create_form_row(self, label_text, items):
        """Создает строку с меткой и выпадающим списком"""
        row_layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setFixedWidth(100)  # Одинаковая ширина для меток
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("font-size: 16px; color: white;")

        combobox = QComboBox()
        combobox.addItems(items)
        combobox.setFixedSize(350, 30)  # Одинаковый размер для выпадающих списков
        combobox.setStyleSheet(self.combo_style())

        row_layout.addStretch()
        row_layout.addWidget(label)
        row_layout.addWidget(combobox)
        row_layout.addStretch()

        return row_layout

    def combo_style(self):
        """Стиль для выпадающих списков"""
        return """
            QComboBox {
                background-color: #EDEDED;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #1F6467;
            }
        """

    def save_teacher_room(self):
        teacher = self.teacher_combobox.itemAt(1).widget().currentText()
        room = self.room_combobox.itemAt(1).widget().currentText()
        print(f"Учитель: {teacher} назначен в кабинет: {room}")

    def go_back(self):
        print("Назад")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherRoomWindow()
    window.show()
    sys.exit(app.exec_())
