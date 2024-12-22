import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt


class AddRoomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить кабинет")
        self.setFixedSize(600, 400)  # Размер окна

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")

        # Заголовок
        header_label = QLabel("Добавить кабинет")
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

        # Формы ввода с ровным выравниванием
        form_layout = QVBoxLayout()

        self.room_number_input = self.create_form_row("Номер:")
        self.capacity_input = self.create_form_row("Вместимость:")
        self.room_name_input = self.create_form_row("Название:")

        form_layout.addLayout(self.room_number_input)
        form_layout.addLayout(self.capacity_input)
        form_layout.addLayout(self.room_name_input)
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
        save_button.clicked.connect(self.save_room)

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

    def create_form_row(self, label_text):
        """Создает строку с меткой и полем ввода"""
        row_layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setFixedWidth(120)  # Фиксированная ширина для всех меток
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
            }
        """)

        input_field = QLineEdit()
        input_field.setFixedSize(300, 30)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #EDEDED;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        row_layout.addStretch()
        row_layout.addWidget(label)
        row_layout.addWidget(input_field)
        row_layout.addStretch()

        return row_layout

    def go_back(self):
        print("Назад")

    def save_room(self):
        print("Кабинет сохранен!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddRoomWindow()
    window.show()
    sys.exit(app.exec_())
