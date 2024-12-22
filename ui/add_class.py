import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt


class AddClassWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить класс")
        self.setFixedSize(600, 400)  # Размер окна

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")

        # Заголовок
        header_label = QLabel("Добавить класс")
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

        # Поле ввода названия класса
        form_layout = QHBoxLayout()
        name_label = QLabel("Название")
        name_label.setAlignment(Qt.AlignLeft)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
            }
        """)

        self.name_input = QLineEdit()
        self.name_input.setFixedSize(250, 30)
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #EDEDED;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addStretch()
        central_layout.addLayout(form_layout)

        # Кнопки "Назад" и "Сохранить"
        button_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        save_button = QPushButton("Сохранить")

        back_button.setFixedSize(120, 40)
        save_button.setFixedSize(120, 40)

        back_button.setStyleSheet(self.button_style())
        save_button.setStyleSheet(self.button_style())

        back_button.clicked.connect(self.go_back)
        save_button.clicked.connect(self.save_class)

        button_layout.addWidget(back_button)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        central_layout.addStretch()
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

    def save_class(self):
        class_name = self.name_input.text()
        if class_name:
            print(f"Класс '{class_name}' добавлен!")
        else:
            print("Поле названия класса пустое.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddClassWindow()
    window.show()
    sys.exit(app.exec_())
