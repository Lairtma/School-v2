import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QLineEdit, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt

# Импортируем список предметов
from axios_data import SUBJECTS_LIST


class SubjectListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список предметов")
        self.setFixedSize(600, 500)  # Размер окна

        # Центральный виджет и основной макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")  # Цвет фона

        # Заголовок
        header_label = QLabel("Список предметов")
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

        # Список предметов
        self.subject_list_widget = QListWidget()
        self.populate_subject_list()
        main_layout.addWidget(self.subject_list_widget)

        # Нижние кнопки
        bottom_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        add_button = QPushButton("Добавить")

        back_button.setFixedSize(120, 40)
        add_button.setFixedSize(120, 40)

        back_button.setStyleSheet(self.button_style())
        add_button.setStyleSheet(self.button_style())

        back_button.clicked.connect(self.go_back)
        add_button.clicked.connect(self.add_subject)

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

    def populate_subject_list(self):
        """Заполняем список предметов"""
        for subject in SUBJECTS_LIST:
            item = QListWidgetItem()
            item_widget = QWidget()
            item_layout = QHBoxLayout()

            # Поля: предмет
            self.subject_input = QLineEdit(subject)
            self.subject_input.setFixedSize(200, 40)
            self.subject_input.setStyleSheet(self.input_style())

            # Кнопка "Удалить"
            delete_button = QPushButton("🗑️")
            delete_button.setFixedSize(40, 40)
            delete_button.setStyleSheet("border: none; font-size: 18px;")
            delete_button.clicked.connect(lambda _, s=subject: self.delete_subject(s))

            # Кнопка "Изменить"
            edit_button = QPushButton("✏️")
            edit_button.setFixedSize(40, 40)
            edit_button.setStyleSheet("border: none; font-size: 18px;")
            edit_button.clicked.connect(lambda _, s=subject: self.edit_subject(s))

            # Добавляем элементы в макет
            item_layout.addWidget(self.subject_input)
            item_layout.addStretch()
            item_layout.addWidget(delete_button)
            item_layout.addWidget(edit_button)
            item_layout.setContentsMargins(0, 5, 0, 5)

            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.subject_list_widget.addItem(item)
            self.subject_list_widget.setItemWidget(item, item_widget)

    def input_style(self):
        """Стиль для редактируемых полей"""
        return """
            QLineEdit {
                font-size: 16px;
                background-color: #EDEDED;
                padding: 5px;
                border-radius: 5px;
            }
        """

    def delete_subject(self, subject_name):
        print(f"Удалён предмет: {subject_name}")

    def edit_subject(self, subject_name):
        print(f"Редактирование предмета: {subject_name}")
        self.open_edit_dialog(subject_name)

    def open_edit_dialog(self, subject_name):
        """Открытие диалогового окна для редактирования"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Изменить предмет")
        dialog.setFixedSize(400, 300)

        layout = QFormLayout()

        # Поле для редактирования предмета
        self.subject_edit = QLineEdit(subject_name)
        self.subject_edit.setFixedSize(250, 30)
        layout.addRow("Предмет:", self.subject_edit)

        # Кнопки для сохранения и отмены
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(lambda: self.save_edited_subject(subject_name))
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addRow(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edited_subject(self, subject_name):
        # Сохранение изменений
        new_subject = self.subject_edit.text()
        print(f"Изменено на: {new_subject}")
        # Здесь можно добавить код для обновления данных в списке SUBJECTS_LIST
        self.close()

    def go_back(self):
        print("Назад")
        self.close()

    def add_subject(self):
        print("Добавление нового предмета")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubjectListWindow()
    window.show()
    sys.exit(app.exec_())
