import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QDialog, QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt

# Пример данных для классов
CLASSES_LIST = ["1А", "10A ИТ", "10A СЭ", "2Б"]

class ClassListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список классов")
        self.setFixedSize(600, 500)  # Фиксированный размер окна

        # Центральный виджет и основной макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet("background-color: #6BA4A4;")  # Цвет фона

        # Заголовок
        header_label = QLabel("Список классов")
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

        # Список классов
        self.class_list_widget = QListWidget()
        self.populate_class_list()
        main_layout.addWidget(self.class_list_widget)

        # Нижние кнопки
        bottom_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        add_button = QPushButton("Добавить")

        back_button.setFixedSize(120, 40)
        add_button.setFixedSize(120, 40)

        back_button.setStyleSheet(self.button_style())
        add_button.setStyleSheet(self.button_style())

        back_button.clicked.connect(self.go_back)
        add_button.clicked.connect(self.add_class)

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

    def populate_class_list(self):
        for class_name in CLASSES_LIST:
            item = QListWidgetItem()
            item_widget = QWidget()
            item_layout = QHBoxLayout()

            # Название класса
            class_label = QLabel(class_name)
            class_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    background-color: #EDEDED;
                    padding: 10px;
                    border-radius: 10px;
                }
            """)
            class_label.setAlignment(Qt.AlignCenter)
            class_label.setFixedSize(250, 40)

            # Кнопка "Удалить"
            delete_button = QPushButton("🗑️")  # Иконка-корзина
            delete_button.setFixedSize(40, 40)
            delete_button.setStyleSheet("border: none; font-size: 18px;")
            delete_button.clicked.connect(lambda _, name=class_name: self.delete_class(name))

            # Кнопка "Изменить"
            edit_button = QPushButton("✏️")  # Иконка-карандаш
            edit_button.setFixedSize(40, 40)
            edit_button.setStyleSheet("border: none; font-size: 18px;")
            edit_button.clicked.connect(lambda _, name=class_name: self.edit_class(name))

            # Добавляем элементы в макет
            item_layout.addWidget(class_label)
            item_layout.addStretch()
            item_layout.addWidget(delete_button)
            item_layout.addWidget(edit_button)
            item_layout.setContentsMargins(0, 5, 0, 5)
            item_widget.setLayout(item_layout)

            item.setSizeHint(item_widget.sizeHint())
            self.class_list_widget.addItem(item)
            self.class_list_widget.setItemWidget(item, item_widget)

    def delete_class(self, class_name):
        print(f"Удалён класс: {class_name}")

    def edit_class(self, class_name):
        """Диалоговое окно для редактирования класса"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Редактирование класса: {class_name}")

        layout = QFormLayout(dialog)

        # Поле для нового названия класса
        class_name_input = QLineEdit(class_name)
        layout.addRow("Название класса:", class_name_input)

        # Кнопка для сохранения изменений
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(lambda: self.save_edited_class(class_name, class_name_input.text(), dialog))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edited_class(self, old_name, new_name, dialog):
        """Сохраняем изменённое название класса"""
        if new_name:
            index = CLASSES_LIST.index(old_name)
            CLASSES_LIST[index] = new_name
            print(f"Обновлено название класса: {old_name} -> {new_name}")
        dialog.accept()

    def go_back(self):
        print("Назад")
        self.close()

    def add_class(self):
        print("Добавление нового класса")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassListWindow()
    window.show()
    sys.exit(app.exec_())
