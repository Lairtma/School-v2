import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem, \
    QTableWidget, QLineEdit, QLabel, QDialog, QComboBox, QRadioButton, QLayout, QPushButton, QScrollArea
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QFont, QResizeEvent
from PyQt5.QtCore import Qt
from ui.axios_data_main import *
from datetime import datetime, timedelta, date
from api.school_api import PrepareInformationForMainPage


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("assets/mainWindow.ui", self)

        self.setWindowTitle("School Schedule for Konstantin")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.current_date_raw = datetime.now()
        self.update_date_text()
        #!!! - так обозначаются все новые правки

        # настройка меню бара
        self.menu_bar_export_to_excel_for_this_day.triggered.connect(self.export_to_excel_for_this_day)
        self.menu_bar_export_to_excel_for_week.triggered.connect(self.export_to_excel_for_week)
        self.menu_bar_import_from_excel.triggered.connect(self.import_from_excel)

        # настройка кнопок "следующий день" и "предыдущий день"
        self.pixmap = QPixmap("assets/arrow.png")
        mirrored_pixmap = self.pixmap.transformed(QTransform().scale(-1, 1))

        self.previous_day_button.setIcon(QIcon(mirrored_pixmap))
        self.previous_day_button.setIconSize(QtCore.QSize(32, 32))
        self.previous_day_button.setFixedSize(50, 50)

        self.next_day_button.setIcon(QIcon(self.pixmap))
        self.next_day_button.setIconSize(QtCore.QSize(32, 32))
        self.next_day_button.setFixedSize(50, 50)

        self.next_day_button.clicked.connect(self.next_day_button_clicked)
        self.previous_day_button.clicked.connect(self.previous_day_button_clicked)

        # настройка расположения кнопок

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.previous_day_button, alignment=Qt.AlignLeft)
        h_layout.addStretch()
        h_layout.addWidget(self.next_day_button, alignment=Qt.AlignRight)

        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addLayout(h_layout)
        v_layout.addStretch()

        central_widget.setLayout(v_layout)

        # настройка таблицы номера урока и времени его проведения

        self.table_lessons_time = QTableWidget(self)
        self.table_lessons_time.setRowCount(9)
        self.table_lessons_time.setColumnCount(1)
        self.table_lessons_time.setGeometry(70, 60, 200, self.height() - 60)

        self.table_lessons_time.verticalHeader().setVisible(False)
        self.table_lessons_time.horizontalHeader().setVisible(False)
        self.table_lessons_time.setFrameStyle(QTableWidget.NoFrame)
        self.table_lessons_time.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid black; 
            }
        """)
        self.font = QFont("Times New Roman ", self.height() // 50)

        for row in range(9):
            self.table_lessons_time.setRowHeight(row, 90)

        for row, text in enumerate(LESSONS_NUM_TIME):
            item = QTableWidgetItem(text)
            item.setFont(self.font)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_lessons_time.setItem(row, 0, item)

        self.table_lessons_time.cellClicked.connect(self.on_cell_clicked)

        # настройка таблицы уроков, кабинетов и учителей
        self.table_schedule = QTableWidget(self)
        self.table_schedule.setRowCount(9)
        self.table_schedule.setColumnCount(len(CLASSES_LIST))
        self.table_schedule.setFrameStyle(QTableWidget.NoFrame)
        self.table_schedule.verticalHeader().setVisible(False)
        self.table_schedule.setHorizontalHeaderLabels(CLASSES_LIST)


        self.table_schedule.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid black;  
            }
        """)

        

        self.set_lessons_main_table()
        self.table_schedule.cellClicked.connect(self.on_cell_clicked_table_schedule)

        # день недели дата

        self.date_label = QLineEdit(self)
        self.date_label.setText(self.date_text)
        self.date_label.setReadOnly(True)
        self.date_label.setFixedWidth(250)
        self.date_label.setAlignment(Qt.AlignCenter)

        self.date_label.setStyleSheet("""
            QLineEdit {
                background-color: #1F6467; 
                color: #FFFFFF;           
                font-size: 16px;          
                border-radius: 10px;  
                font-weight: bold;      
            }
        """)

    # день недели дата.расположние и таблицы номеров уроков

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        x_position = (self.width() - self.date_label.width()) // 2
        y_position = self.height() - self.date_label.height() - 5
        self.date_label.move(x_position, y_position)

        row_height = self.height() // 11 if self.height() // 11 < 90 else 90
        y_position = 30
        height_of_font = self.height() // 50 if self.height() // 50 < 16 else 16
        self.font = QFont("Times New Roman ", height_of_font)
        for row in range(self.table_lessons_time.rowCount()):
            self.table_lessons_time.setRowHeight(row, row_height)
            item = self.table_lessons_time.item(row, 0) 
            if item:
                item.setFont(self.font)
                self.table_lessons_time.setGeometry(70, y_position, 200, row_height * 9)
         
        vertical_scrollbar_height = self.table_schedule.verticalScrollBar().height()
        header_height = self.table_schedule.horizontalHeader().height()


        self.table_schedule.setGeometry(200, y_position - header_height, self.width() - 270, row_height * 9 + header_height + vertical_scrollbar_height)
        for row in range(9):
            self.table_schedule.setRowHeight(row, row_height)
            for col in range(self.table_schedule.columnCount()):
                item = self.table_schedule.item(row, col)
                if item:  
                    item.setFont(self.font)


    def resizeEvent_manual(self):
        height_of_font = self.height() // 50 if self.height() // 50 < 16 else 16
        self.font = QFont("Times New Roman ", height_of_font)
        for row in range(9):
            for col in range(self.table_schedule.columnCount()):
                item = self.table_schedule.item(row, col)
                if item:  
                    item.setFont(self.font)


    # функкции для меню бара

    def import_from_excel(self):
        print("import_from_excel")

    def export_to_excel_for_week(self):
        print("export_to_excel_for_week")

    def export_to_excel_for_this_day(self):
        print("export_to_excel_for_this_day")

    # функции для кнопок следующий - предыдущий
    def update_date_text(self):
        self.current_date = self.current_date_raw.strftime("%d.%m.%Y")
        self.current_day_of_week = self.current_date_raw.weekday()
        self.date_text = f"{WEEK_DAYS[self.current_day_of_week]} {self.current_date}"
        if hasattr(self, 'date_label'):
            self.date_label.setText(self.date_text)
        if hasattr(self, 'table_schedule'):
            self.set_lessons_main_table()

    def next_day_button_clicked(self):
        if self.current_day_of_week == 4:
            self.current_date_raw += timedelta(days=2)
        self.current_date_raw += timedelta(days=1)
        self.update_date_text()

    def previous_day_button_clicked(self):
        if self.current_day_of_week == 0:
            self.current_date_raw -= timedelta(days=2)
        self.current_date_raw -= timedelta(days=1)
        self.update_date_text()

    # заполнение главное таблицы
    # id любого предмета в таблице в БД должно быть col+row
    def set_lessons_main_table(self):
        data = PrepareInformationForMainPage(self.current_date_raw)  # self.current_day_of_week
        for col in range(len(CLASSES_LIST)):
            class_lessons = CLASSES_LIST[col]  # должен быть col а не 0
            for row in range(9):
                if row in data[class_lessons]:  # должен быть row а не 1
                    is_group_lesson = data[class_lessons][row]["group_lesson"]  # должен быть row а не 1
                    if is_group_lesson:
                        item = QTableWidgetItem(f"Групповое")
                    else:
                        subject = data[class_lessons][row]["title_lesson"] if data[class_lessons][row][
                                                                                "title_lesson"] is not None else ""
                        teacher = data[class_lessons][row]["teacher"] if data[class_lessons][row][
                                                                           "teacher"] is not None else ""
                        place = data[class_lessons][row]["places"] if data[class_lessons][row]["places"] is not None else ""
                        item = QTableWidgetItem(f"{subject}\n{teacher}\n{place}")
                else:
                    item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.table_schedule.setItem(row, col, item)
        self.resizeEvent_manual() 

    def on_cell_clicked_table_schedule(self, row, column):
        self.table_schedule.setCurrentCell(row, column)
        self.table_schedule.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #1F6467; 
                color: #FFFFFF;            
            }
            QTableWidget::item {
                border: 1px solid black; 
            }
        """)

        self.settings_of_lesson(row, column)

    # настройка урока диалоговое окно
    def settings_of_lesson(self, row, column):

        # наши первоначальные данные
        try:
            self.existing_data_about_lesson = PrepareInformationForMainPage(self.current_date_raw)[CLASSES_LIST[column]][row]
        # existing_data_about_lesson = LESSONS_TITLE_PLACE_TEACHER_CLASS[WEEK_DAYS[self.current_day_of_week]][CLASSES_LIST[column]][row]
        except Exception as e:
            self.existing_data_about_lesson = {'group_lesson': False, 'places': "", 'teacher': '', 'title_lesson': ''}

        # наши новые данные
        self.new_updating_data = self.existing_data_about_lesson
        self.our_subgr_exist = 0

        print(self.new_updating_data)

        self.setting_of_lesson_dialog = QDialog(self)
        self.setting_of_lesson_dialog.setWindowTitle("Действия")
        self.setting_of_lesson_dialog.resize(400, 600)
        self.setting_of_lesson_dialog.setStyleSheet("background-color: #1F6467; border-radius: 10px;")

        label_class_name = QLabel(self.setting_of_lesson_dialog)
        label_class_name.setStyleSheet("color: #FFFFFF;")
        label_class_name.setText(f"{CLASSES_LIST[column]}")
        label_class_name.setFont(QFont("Times New Roman", 18))

        label_class_date = QLabel(self.setting_of_lesson_dialog)
        label_class_date.setStyleSheet("color: #FFFFFF;")
        label_class_date.setText(f"{WEEK_DAYS[self.current_day_of_week]} {self.current_date}")
        label_class_date.setFont(QFont("Times New Roman", 18))

        label_class_num = QLabel(self.setting_of_lesson_dialog)
        label_class_num.setStyleSheet("color: #FFFFFF;")
        label_class_num.setText(f"Урок {row + 1}")
        label_class_num.setFont(QFont("Times New Roman", 18))

        # создание радио бокса по группам
        label_is_group = QLabel("По группам")
        label_is_group.setStyleSheet("font-size: 18px; color: #FFFFFF;")
        label_is_group.setAlignment(Qt.AlignCenter)

        self.radio_yes = QRadioButton("Да")
        self.radio_no = QRadioButton("Нет")

        self.radio_style_checked = ("""
            QRadioButton {
                font-size: 18px;
                color: #FFFFFF;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                background: lightgray;
            }
            QRadioButton::indicator:checked {
                background: #5E9EA0;  
            }
            QRadioButton:focus {
                outline: none;
                border: none;
            }
        """)

        self.radio_style_not_checked = ("""
            QRadioButton {
                font-size: 18px;
                color: #FFFFFF;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                background: lightgray;
            }
            QRadioButton::indicator:checked {
                background: #D9D9D9;  
            }

            QRadioButton:focus {
                outline: none;
                border: none;
            }
        """)
        if "group_lesson" in self.existing_data_about_lesson:
            if self.existing_data_about_lesson["group_lesson"]:
                self.radio_yes.setChecked(True)
                self.radio_yes.setStyleSheet(self.radio_style_checked)
            else:
                self.radio_no.setChecked(True)
                self.radio_no.setStyleSheet(self.radio_style_checked)

        self.radio_yes.toggled.connect(self.update_button_color_and_info)
        self.radio_no.toggled.connect(self.update_button_color_and_info)

        layout_h = QHBoxLayout()
        layout_h.addWidget(label_is_group)
        layout_h.addWidget(self.radio_yes)
        layout_h.addWidget(self.radio_no)

        # выпадающие списки.

        self.layout_v_for_lists = QVBoxLayout()

        # список предметов

        layout_for_lists_subj = QHBoxLayout()
        label_for_lesson = QLabel("Урок: ")
        label_for_lesson.setStyleSheet("font-size: 18px; color: #FFFFFF;")
        self.list_for_lesson = QComboBox()
        self.list_for_lesson.addItem(self.new_updating_data["title_lesson"])
        self.list_for_lesson.addItems(SUBJECTS_LIST)
        self.list_for_lesson.setFixedWidth(200)
        self.list_for_lesson.setFixedHeight(40)
        self.list_for_lesson.setStyleSheet("""
            QComboBox {
                background-color: #DCDCDC;
                font-size: 16px;
                border-radius: 5px;
                color: #000000;
            }
        """)
        self.list_for_lesson.currentIndexChanged.connect(self.lists_on_lesson_selected)

        layout_for_lists_subj.addWidget(label_for_lesson)
        layout_for_lists_subj.addWidget(self.list_for_lesson)

        # список учителей

        layout_for_lists_teachers = QHBoxLayout()
        label_for_teacher = QLabel("Учитель: ")
        label_for_teacher.setStyleSheet("font-size: 18px; color: #FFFFFF;")
        self.list_for_teacher = QComboBox()
        self.list_for_teacher.addItem(self.new_updating_data["teacher"])

        if 'type' in self.new_updating_data.keys():
            if self.new_updating_data['type'] in ["default", "change"]:
                if not self.new_updating_data['group_lesson']: # не групповой урок
                    self.list_for_teacher.addItems(self.teachers_of_current_subject(self.new_updating_data['title_lesson']))


        self.list_for_teacher.setFixedWidth(200)
        self.list_for_teacher.setFixedHeight(40)
        self.list_for_teacher.setStyleSheet("""
            QComboBox {
                background-color: #DCDCDC;
                font-size: 16px;
                border: none; /* Убираем обводку */
                border-radius: 5px;
                color: #000000;
            }
        """)

        self.list_for_teacher.currentIndexChanged.connect(self.list_for_teacher_selected)

        layout_for_lists_teachers.addWidget(label_for_teacher)
        layout_for_lists_teachers.addWidget(self.list_for_teacher)

        # список кабинетов

        layout_for_lists_rooms = QHBoxLayout()
        label_for_rooms = QLabel("Кабинет: ")
        label_for_rooms.setStyleSheet("font-size: 18px; color: #FFFFFF;")
        self.list_for_rooms = QComboBox()
        self.list_for_rooms.addItem(str(self.new_updating_data["places"]))
        self.list_for_rooms.addItems(self.free_places_for_num_lesson(self.current_date, row))
        self.list_for_rooms.setFixedWidth(200)
        self.list_for_rooms.setFixedHeight(40)
        self.list_for_rooms.setStyleSheet("""
            QComboBox {
                background-color: #DCDCDC;
                font-size: 16px;
                border-radius: 5px;
                color: #000000;
            }
        """)

        self.list_for_rooms.currentIndexChanged.connect(self.list_for_rooms_selected)

        layout_for_lists_rooms.addWidget(label_for_rooms)
        layout_for_lists_rooms.addWidget(self.list_for_rooms)

        # обьеденяем все лэйауты списков

        self.layout_v_for_lists.addLayout(layout_for_lists_subj)
        self.layout_v_for_lists.addLayout(layout_for_lists_teachers)
        self.layout_v_for_lists.addLayout(layout_for_lists_rooms)

        # кнокпи для манипуляции с действиями
        button_font = QFont("Times New Roman", 18)
        delete_button = QPushButton("Удалить урок")
        delete_button.setFont(button_font)
        delete_button.setFixedHeight(40)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #81A6A8;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #6A8B8E;
            }
        """)

        delete_button.clicked.connect(lambda: self.delete_button_clicked(row, column))

        delete_button_for_all = QPushButton("Удалить для расписания")
        delete_button_for_all.setFont(button_font)
        delete_button_for_all.setFixedHeight(40)
        delete_button_for_all.setStyleSheet("""
            QPushButton {
                background-color: #81A6A8;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #6A8B8E;
            }
        """)

        delete_button_for_all.clicked.connect(lambda: self.delete_for_schedule_button_clicked(row, column))

        save_button = QPushButton("Сохранить")
        save_button.setFont(button_font)
        save_button.setFixedHeight(50)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4F6A6D;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #3F5457;
            }
        """)

        save_button.clicked.connect(lambda: self.save_button_clicked(row, column))

        save_schedule_button = QPushButton("Сохранить для расписания")
        save_schedule_button.setFont(button_font)
        save_schedule_button.setFixedHeight(50)
        save_schedule_button.setStyleSheet("""
            QPushButton {
                background-color: #4F6A6D;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #3F5457;
            }
        """)

        save_schedule_button.clicked.connect(lambda: self.save_for_schedule_button_clicked(row, column))

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(label_class_name, alignment=Qt.AlignCenter)
        layout.addWidget(label_class_date, alignment=Qt.AlignCenter)
        layout.addWidget(label_class_num, alignment=Qt.AlignCenter)
        layout.addLayout(layout_h)  # радиобоксы
        layout.addLayout(self.layout_v_for_lists)  # списки
        layout.addWidget(delete_button)
        layout.addWidget(delete_button_for_all)
        layout.addWidget(save_button)
        layout.addWidget(save_schedule_button)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        container_widget = QWidget()
        container_widget.setFixedSize(350, 400)
        container_widget.setLayout(layout)

        self.update_button_color_and_info()

        main_layout = QVBoxLayout()
        main_layout.addWidget(container_widget, alignment=Qt.AlignTop | Qt.AlignCenter)

        print(self.new_updating_data)
        print(len(TEACHERS))
        print(len(SUBJECTS_LIST))
        self.setting_of_lesson_dialog.setLayout(main_layout)
        self.setting_of_lesson_dialog.exec_()

    def teachers_of_current_subject(self, subjet):
        print(SUBJECTS_AND_TEACHERS[subjet])
        return SUBJECTS_AND_TEACHERS[subjet]



    def free_places_for_num_lesson(self, date, num_lesson):
        print(f"{date} {num_lesson}")
        return list(map(str, PLACES))

    def update_button_color_and_info(self):
        self.radio_yes.setStyleSheet(self.radio_style_not_checked)
        self.radio_no.setStyleSheet(self.radio_style_not_checked)

        if self.radio_yes.isChecked():
            self.radio_yes.setStyleSheet(self.radio_style_checked)
            if "num_subgroups" not in self.existing_data_about_lesson:
                self.new_updating_data["group_lesson"] = True
                self.new_updating_data["num_subgroups"] = 2
                for i in range(1, self.new_updating_data["num_subgroups"] + 1):
                    self.new_updating_data[i] = {
                        "title_lesson": "",
                        "teacher": "",
                        "places": ""
                    }

                self.new_updating_data[1] = {
                    "title_lesson": self.list_for_lesson.currentText(),
                    "teacher": self.list_for_teacher.currentText(),
                    "places": self.list_for_rooms.currentText()
                }

            if self.our_subgr_exist == 0:
                self.add_layout_subgr()

        elif self.radio_no.isChecked():
            self.radio_no.setStyleSheet(self.radio_style_checked)
            self.new_updating_data["group_lesson"] = False
            if "num_subgroups" in self.new_updating_data: del self.new_updating_data["num_subgroups"]
            self.add_layout_subgr()

    def add_layout_subgr(self):
        if self.new_updating_data["group_lesson"]:
            self.our_subgr_exist = 1
            self.layout_for_lists_subgr = QHBoxLayout()
            label_for_subgr = QLabel("Подгруппа: ")
            label_for_subgr.setStyleSheet("font-size: 18px; color: #FFFFFF;")
            self.list_for_subgr = QComboBox()
            self.list_for_subgr.addItems([str(x + 1) for x in range(self.new_updating_data["num_subgroups"])])
            self.list_for_subgr.addItem("+")
            self.list_for_subgr.activated.connect(
                lambda index: self.on_subgroup_item_selected(self.list_for_subgr, index))
            self.list_for_subgr.setFixedWidth(200)
            self.list_for_subgr.setFixedHeight(40)
            self.list_for_subgr.setStyleSheet("""
                QComboBox {
                    background-color: #DCDCDC;
                    font-size: 16px;
                    border-radius: 5px;
                    color: #000000;
                }
            """)

            self.list_for_subgr.currentIndexChanged.connect(self.list_for_subgr_selected)

            self.layout_for_lists_subgr.addWidget(label_for_subgr)
            self.layout_for_lists_subgr.addWidget(self.list_for_subgr)
            self.layout_v_for_lists.insertLayout(0, self.layout_for_lists_subgr)
            self.list_for_subgr_selected()

        else:
            if hasattr(self,
                       "layout_for_lists_subgr") and self.layout_for_lists_subgr is not None and self.our_subgr_exist == 1:
                while self.layout_for_lists_subgr.count():
                    item = self.layout_for_lists_subgr.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

                self.layout_v_for_lists.removeItem(self.layout_for_lists_subgr)

                self.layout_for_lists_subgr.deleteLater()
                self.layout_for_lists_subgr = None

                self.our_subgr_exist = 0

    # добавление подгруппы по нажатию на +
    def on_subgroup_item_selected(self, combo_box, index):
        selected_item = combo_box.itemText(index)
        if selected_item == "+":
            self.add_new_subgroup()

    def add_new_subgroup(self):
        self.new_updating_data["num_subgroups"] += 1
        self.new_updating_data[self.new_updating_data["num_subgroups"]] = {
            "title_lesson": "",
            "teacher": "",
            "places": ""
        }
        new_item = str(self.new_updating_data["num_subgroups"])
        self.list_for_subgr.insertItem(self.list_for_subgr.count() - 1, new_item)
        self.list_for_subgr.setCurrentIndex(self.list_for_subgr.count() - 1)

    # список функция для обрабки того что выбрано в комбо боксах
    def lists_on_lesson_selected(self):
        if "num_subgroups" not in self.new_updating_data:
            self.new_updating_data["title_lesson"] = self.list_for_lesson.currentText()
            # self.list_for_subgr_selected()
        else:
            self.new_updating_data[int(self.list_for_subgr.currentText())][
                "title_lesson"] = self.list_for_lesson.currentText()

    def list_for_teacher_selected(self):
        if "num_subgroups" not in self.new_updating_data:
            self.new_updating_data["teacher"] = self.list_for_teacher.currentText()
            # self.list_for_subgr_selected()
        else:
            self.new_updating_data[int(self.list_for_subgr.currentText())][
                "teacher"] = self.list_for_teacher.currentText()

    def list_for_rooms_selected(self):
        if "num_subgroups" not in self.new_updating_data:
            self.new_updating_data["places"] = self.list_for_rooms.currentText()
            # self.list_for_subgr_selected()
        else:
            self.new_updating_data[int(self.list_for_subgr.currentText())]["places"] = self.list_for_rooms.currentText()

    def list_for_subgr_selected(self):
        if "num_subgroups" in self.new_updating_data and self.our_subgr_exist == 1:
            if self.list_for_subgr.currentText() != "+":
                self.list_for_lesson.setCurrentText(
                    self.new_updating_data[int(self.list_for_subgr.currentText())]["title_lesson"])
                self.list_for_teacher.setCurrentText(
                    self.new_updating_data[int(self.list_for_subgr.currentText())]["teacher"])
                self.list_for_rooms.setCurrentText(
                    self.new_updating_data[int(self.list_for_subgr.currentText())]["places"])

    # логика функций
    def delete_button_clicked(self, row, column):
        self.setting_of_lesson_dialog.close()
        del self.existing_data_about_lesson
        if self.new_updating_data.get("type") == "default":
            DefaultScheduleDeleteLessonById(self.new_updating_data["id"])
        elif self.new_updating_data.get("type") == "change":
            ChangeInScheduleDeleteById(self.new_updating_data["id"])
        del self.new_updating_data
        self.our_subgr_exist = 0
        self.set_lessons_main_table()

    def delete_for_schedule_button_clicked(self, row, column):
        print(f"{row} {column}")

    def save_button_clicked(self, row, column):
        class_id = ClassGetIdByName(CLASSES_LIST[column])
        self.setting_of_lesson_dialog.close()
        if self.new_updating_data != self.existing_data_about_lesson:
            if self.new_updating_data["type"] == "default":
                ChangeInScheduleAdd(row + 1, TeacherGetIdByName(self.new_updating_data["teacher"]),
                                         ClassRoomGetIdByName(self.new_updating_data["places"]), class_id,
                                         SubjectGetIdByName(self.new_updating_data["title_lesson"]),
                                        self.current_date_raw)
            elif self.new_updating_data.get("type") == "change":
                lesson = ChangeInScheduleChangeById(ChangeInScheduleGetByNumberClassDate(row + 1, class_id, self.current_date_raw),  row + 1, TeacherGetIdByName(self.new_updating_data["teacher"]),
                                         ClassRoomGetIdByName(self.new_updating_data["places"]), class_id,
                                         SubjectGetIdByName(self.new_updating_data["title_lesson"]),
                                        self.current_date_raw)
        print(self.new_updating_data)
        del self.new_updating_data
        del self.existing_data_about_lesson
        self.our_subgr_exist = 0
        self.set_lessons_main_table()
        self.update()

    def save_for_schedule_button_clicked(self, row, column):
        class_id = ClassGetIdByName(CLASSES_LIST[column])
        self.setting_of_lesson_dialog.close()
        if self.new_updating_data.get("id"):
            if self.new_updating_data["type"] == "change":
                ChangeInScheduleDeleteById(self.new_updating_data["id"])
            DefaultScheduleChangeLessonById(DefaultScheduleGetByWeekdayNumberClass(self.current_day_of_week + 1, row + 1, class_id), self.current_day_of_week + 1, row + 1, TeacherGetIdByName(self.new_updating_data["teacher"]), ClassRoomGetIdByName(self.new_updating_data["places"]), class_id, SubjectGetIdByName(self.new_updating_data["title_lesson"]))
        else:
            DefaultScheduleAddLesson(self.current_day_of_week + 1, row + 1, TeacherGetIdByName(self.new_updating_data["teacher"]), ClassRoomGetIdByName(self.new_updating_data["places"]), class_id, SubjectGetIdByName(self.new_updating_data["title_lesson"]))
        print(column, row)
        print(self.new_updating_data)
        self.set_lessons_main_table()
        self.update()

    # функция для нажатия на кнопку номера урока
    def on_cell_clicked(self, row, column):
        self.table_lessons_time.setCurrentCell(row, column)
        self.table_lessons_time.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #1F6467; 
                color: #FFFFFF;            
            }
            QTableWidget::item {
                border: 1px solid black; 
            }
        """)

        self.free_places_for_the_lessons_widget(LESSONS_NUM_TIME[row].split("\n")[0], row, column)

    # вывод свободных кабинетов
    def free_places_for_the_lessons_widget(self, num_lesson, row, column):

        self.free_places_dialog = QDialog(self)
        self.free_places_dialog.setWindowTitle("Свободные кабинеты")
        self.free_places_dialog.resize(300, 200)
        self.free_places_dialog.setStyleSheet("background-color: #1F6467; border-radius: 10px;")

        label_date_of_free_places = QLabel(self.free_places_dialog)
        label_date_of_free_places.setAlignment(Qt.AlignCenter)
        label_date_of_free_places.setStyleSheet("color: #FFFFFF;")
        label_date_of_free_places.setText(
            f"Дата: {WEEK_DAYS[self.current_day_of_week]} {self.current_date}\n Урок: {num_lesson}")
        label_date_of_free_places.setFont(QFont("Times New Roman", 18))

        free_rooms_label = QLabel(self.free_places_dialog)
        free_rooms_label.setAlignment(Qt.AlignCenter)
        free_rooms_label.setStyleSheet("color: #FFFFFF;")

        free_rooms_list = self.free_places_for_num_lesson(self.current_date, row+1)  # как то надо заполнить
        grouped_rooms = [
            ", ".join(map(str, free_rooms_list[i:i + 5]))
            for i in range(0, len(free_rooms_list), 5)
        ]
        formatted_rooms = "\n".join(grouped_rooms)
        free_rooms_label.setText(formatted_rooms)
        free_rooms_label.setFont(QFont("Times New Roman", 16))

        layout = QVBoxLayout()
        layout.addWidget(label_date_of_free_places)
        layout.addWidget(free_rooms_label)
        self.free_places_dialog.setLayout(layout)

        self.free_places_dialog.exec_()


# Главня задача - заняться масштабированием на любом дисплее



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())