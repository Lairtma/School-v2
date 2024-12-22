import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

class TablesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Таблицы")
        self.setFixedSize(400, 500)  # Размер окна

        # Основной виджет и макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setStyleSheet("background-color: #6BA4A4;")  # Фон окна
        central_widget.setLayout(layout)

        # Заголовок
        header_label = QLabel("Таблицы")
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
        layout.addWidget(header_label)

        # Создание кнопок и привязка их к отдельным функциям
        self.add_button(layout, "Список учителей", self.show_teachers_list)
        self.add_button(layout, "Список кабинетов", self.show_rooms_list)
        self.add_button(layout, "Список предметов", self.show_subjects_list)
        self.add_button(layout, "Список классов", self.show_classes_list)
        self.add_button(layout, "Учителя - предметы", self.show_teachers_subjects)
        self.add_button(layout, "Учителя - кабинеты", self.show_teachers_rooms)

        # Отступ перед кнопкой "Назад"
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка "Назад" (увеличенный размер)
        back_button = QPushButton("Назад")
        back_button.setFixedSize(300, 60)  # Увеличенный размер
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #1F6467;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #154A4D;
            }
        """)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

    # Функция для добавления кнопок
    def add_button(self, layout, text, function):
        button = QPushButton(text)
        button.setFixedHeight(50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #85C8C4;
                color: black;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #6BA4A4;
                color: white;
            }
        """)
        button.clicked.connect(function)  # Привязка функции
        layout.addWidget(button)

    # Отдельные функции для каждой кнопки
    def show_teachers_list(self):
        print("Список учителей")

    def show_rooms_list(self):
        print("Список кабинетов")

    def show_subjects_list(self):
        print("Список предметов")

    def show_classes_list(self):
        print("Список классов")

    def show_teachers_subjects(self):
        print("Учителя - предметы")

    def show_teachers_rooms(self):
        print("Учителя - кабинеты")

    def go_back(self):
        print("Назад")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TablesWindow()
    window.show()
    sys.exit(app.exec_())
