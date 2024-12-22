import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QLineEdit, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt

# Импортируем связь учитель-предмет
from axios_data import TEACHER_SUBJECTS


class TeacherSubjectWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учитель - предмет")
        self.setFixedSize(700, 500)  # Размер окна

        # Центральный виджет и основной макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")  # Цвет фона

        # Заголовок
        header_label = QLabel("Учитель - предмет")
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

        # Список учителей и предметов
        self.teacher_subject_list = QListWidget()
        self.populate_teacher_subject_list()
        main_layout.addWidget(self.teacher_subject_list)

        # Нижние кнопки
        bottom_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        add_button = QPushButton("Добавить")

        back_button.setFixedSize(120, 40)
        add_button.setFixedSize(120, 40)

        back_button.setStyleSheet(self.button_style())
        add_button.setStyleSheet(self.button_style())

        back_button.clicked.connect(self.go_back)
        add_button.clicked.connect(self.add_teacher_subject)

        bottom_layout.addWidget(back_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(add_button)
        main_layout.addLayout(bottom_layout)

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

    def populate_teacher_subject_list(self):
        """Заполняем список учителей и предметов"""
        for entry in TEACHER_SUBJECTS:
            item = QListWidgetItem()
            item_widget = QWidget()
            item_layout = QHBoxLayout()

            # Поля: учитель и предмет
            self.teacher_input = QLineEdit(entry["teacher"])
            self.teacher_input.setFixedSize(200, 40)
            self.teacher_input.setStyleSheet(self.input_style())

            self.subject_input = QLineEdit(entry["subject"])
            self.subject_input.setFixedSize(200, 40)
            self.subject_input.setStyleSheet(self.input_style())

            # Кнопка "Удалить"
            delete_button = QPushButton("🗑️")
            delete_button.setFixedSize(40, 40)
            delete_button.setStyleSheet("border: none; font-size: 18px;")
            delete_button.clicked.connect(lambda _, t=entry: self.delete_teacher_subject(t))

            # Кнопка "Изменить"
            edit_button = QPushButton("✏️")
            edit_button.setFixedSize(40, 40)
            edit_button.setStyleSheet("border: none; font-size: 18px;")
            edit_button.clicked.connect(lambda _, t=entry: self.edit_teacher_subject(t))

            # Добавляем элементы в макет
            item_layout.addWidget(self.teacher_input)
            item_layout.addWidget(self.subject_input)
            item_layout.addStretch()
            item_layout.addWidget(delete_button)
            item_layout.addWidget(edit_button)
            item_layout.setContentsMargins(0, 5, 0, 5)

            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.teacher_subject_list.addItem(item)
            self.teacher_subject_list.setItemWidget(item, item_widget)

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

    def delete_teacher_subject(self, entry):
        print(f"Удалена связь: {entry['teacher']} - {entry['subject']}")

    def edit_teacher_subject(self, entry):
        print(f"Редактирование связи: {entry['teacher']} - {entry['subject']}")
        self.open_edit_dialog(entry)

    def open_edit_dialog(self, entry):
        """Открытие диалогового окна для редактирования"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Изменить связь")
        dialog.setFixedSize(400, 300)

        layout = QFormLayout()

        # Поля для редактирования
        self.teacher_edit = QLineEdit(entry["teacher"])
        self.subject_edit = QLineEdit(entry["subject"])

        layout.addRow("Учитель:", self.teacher_edit)
        layout.addRow("Предмет:", self.subject_edit)

        # Кнопки для сохранения и отмены
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(lambda: self.save_edited_teacher_subject(entry))
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addRow(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edited_teacher_subject(self, entry):
        # Сохранение изменений
        new_teacher = self.teacher_edit.text()
        new_subject = self.subject_edit.text()
        print(f"Изменено на: {new_teacher} - {new_subject}")
        # Здесь можно добавить код для обновления данных в списке TEACHER_SUBJECTS
        self.close()

    def go_back(self):
        print("Назад")
        self.close()

    def add_teacher_subject(self):
        print("Добавление новой связи Учитель - предмет")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherSubjectWindow()
    window.show()
    sys.exit(app.exec_())
