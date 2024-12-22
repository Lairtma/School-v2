import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QLineEdit, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt

# Пример данных для кабинетов
ROOMS_LIST = [
    {"number": "232", "capacity": "Вместимость - 0,5", "type": "Актовый"},
    {"number": "233", "capacity": "Вместимость - 0,5", "type": ""},
    {"number": "234", "capacity": "Вместимость - 0,5", "type": ""},
    {"number": "235", "capacity": "Вместимость - 0,5", "type": ""},
]


class RoomListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список кабинетов")
        self.setFixedSize(800, 500)  # Увеличил ширину окна для удобного размещения полей

        # Центральный виджет и макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")  # Цвет фона

        # Заголовок
        header_label = QLabel("Список кабинетов")
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
        main_layout.addWidget(header_label)

        # Список кабинетов
        self.room_list_widget = QListWidget()
        self.populate_room_list()
        main_layout.addWidget(self.room_list_widget)

        # Нижние кнопки
        bottom_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        add_button = QPushButton("Добавить")

        back_button.setFixedSize(120, 40)
        add_button.setFixedSize(120, 40)

        back_button.setStyleSheet(self.button_style())
        add_button.setStyleSheet(self.button_style())

        back_button.clicked.connect(self.go_back)
        add_button.clicked.connect(self.add_room)

        bottom_layout.addWidget(back_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(add_button)
        main_layout.addLayout(bottom_layout)

    def button_style(self):
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

    def populate_room_list(self):
        """Заполняем список кабинетов"""
        for room in ROOMS_LIST:
            item = QListWidgetItem()
            item_widget = QWidget()
            item_layout = QHBoxLayout()

            # Поля: номер, вместимость, тип кабинета
            room_number = QLabel(room["number"])
            room_number.setFixedSize(80, 30)  # Меньший размер для номера кабинета

            room_capacity = QLabel(room["capacity"])
            room_capacity.setFixedSize(200, 30)  # Широкое поле для вместимости

            room_type = QLabel(room["type"])
            room_type.setFixedSize(150, 30)  # Среднее поле для типа кабинета

            for label in (room_number, room_capacity, room_type):
                label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        background-color: #EDEDED;
                        padding: 5px;
                        border-radius: 5px;
                    }
                """)
                label.setAlignment(Qt.AlignCenter)

            # Кнопка "Удалить"
            delete_button = QPushButton("🗑️")
            delete_button.setFixedSize(40, 40)
            delete_button.setStyleSheet("border: none; font-size: 18px;")
            delete_button.clicked.connect(lambda _, r=room["number"]: self.delete_room(r))

            # Кнопка "Изменить"
            edit_button = QPushButton("✏️")
            edit_button.setFixedSize(40, 40)
            edit_button.setStyleSheet("border: none; font-size: 18px;")
            edit_button.clicked.connect(lambda _, r=room: self.edit_room(r))

            # Добавляем элементы в макет
            item_layout.addWidget(room_number)
            item_layout.addWidget(room_capacity)
            item_layout.addWidget(room_type)
            item_layout.addStretch()
            item_layout.addWidget(delete_button)
            item_layout.addWidget(edit_button)
            item_layout.setContentsMargins(0, 5, 0, 5)

            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.room_list_widget.addItem(item)
            self.room_list_widget.setItemWidget(item, item_widget)

    def delete_room(self, room_number):
        print(f"Удалён кабинет: {room_number}")

    def edit_room(self, room):
        """Диалоговое окно для редактирования данных кабинета"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Редактирование кабинета {room['number']}")

        layout = QFormLayout(dialog)

        room_number_input = QLineEdit(room["number"])
        room_capacity_input = QLineEdit(room["capacity"])
        room_type_input = QLineEdit(room["type"])

        layout.addRow("Номер кабинета:", room_number_input)
        layout.addRow("Вместимость:", room_capacity_input)
        layout.addRow("Тип кабинета:", room_type_input)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(lambda: self.save_edited_room(room, room_number_input, room_capacity_input, room_type_input, dialog))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edited_room(self, room, room_number_input, room_capacity_input, room_type_input, dialog):
        """Сохраняем изменённые данные"""
        room["number"] = room_number_input.text()
        room["capacity"] = room_capacity_input.text()
        room["type"] = room_type_input.text()
        print(f"Обновлено: {room['number']}, {room['capacity']}, {room['type']}")

        # Закрытие диалогового окна после сохранения изменений
        dialog.accept()

    def go_back(self):
        print("Назад")
        self.close()

    def add_room(self):
        print("Добавление нового кабинета")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomListWindow()
    window.show()
    sys.exit(app.exec_())
