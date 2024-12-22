import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt


class AddSubjectWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить предмет")
        self.setFixedSize(600, 400)  # Размер окна

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")

        # Заголовок
        header_label = QLabel("Добавить предмет")
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

        # Поле ввода "Название"
        form_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        name_label.setFixedWidth(100)
        name_label.setStyleSheet("font-size: 16px; color: white;")

        self.name_input = QLineEdit()
        self.name_input.setFixedSize(300, 30)
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #EDEDED;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        form_layout.addStretch()
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addStretch()
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
        save_button.clicked.connect(self.save_subject)

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

    def go_back(self):
        print("Назад")

    def save_subject(self):
        subject_name = self.name_input.text()
        if subject_name:
            print(f"Предмет '{subject_name}' сохранен!")
        else:
            print("Поле 'Название' не должно быть пустым.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddSubjectWindow()
    window.show()
    sys.exit(app.exec_())
