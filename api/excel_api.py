import pandas as pd
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook  
from openpyxl.cell.cell import MergedCell

# Подключение к базе данных SQLite
conn = sqlite3.connect("SchoolMAX.db")
query = """
SELECT
fio AS teacher_name,
s.weekday,
s.number_of_lesson,
c.name AS class_name
FROM
default_schedule s
JOIN
teacher t ON s.teacher_id = t.id
JOIN
class c ON s.class_id = c.id
ORDER BY
fio, s.weekday, s.number_of_lesson;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Подготовка данных
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
lesson_numbers = list(range(1, 10))
teacher_names = df['teacher_name'].unique()
columns = pd.MultiIndex.from_product([days_of_week, lesson_numbers], names=['День недели', '№ Урока'])
result_df = pd.DataFrame(columns=columns, index=teacher_names)

# Заполнение таблицы
for teacher in teacher_names:
    for day in days_of_week:
        for lesson_number in lesson_numbers:
            filtered_data = df[
                (df['teacher_name'] == teacher) &
                (df['weekday'] == days_of_week.index(day) + 1) &
                (df['number_of_lesson'] == lesson_number)
            ]
            class_name = filtered_data['class_name'].values
            result_df.loc[teacher, (day, lesson_number)] = ', '.join(class_name) if class_name.size > 0 else ''

# Сохранение в Excel
wb = Workbook()
ws = wb.active
ws.title = "Расписание учителей"

# Добавляем титульный заголовок
num_columns = len(result_df.columns) + 1 
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_columns)
title_cell = ws.cell(row=1, column=1)
title_cell.value = "Общее расписание учителей"
title_cell.font = Font(bold=True, size=14)
title_cell.alignment = Alignment(horizontal="center")


# Добавляем данные из DataFrame в Excel
for r_idx, row in enumerate(dataframe_to_rows(result_df, index=True, header=True), start=3):
    ws.append(row)

# Настраиваем авторазмер строк и столбцов
for col in ws.columns:
    max_length = 0
    if isinstance(col[0], MergedCell):
        continue
    col_letter = col[0].column_letter 
    for cell in col:
        if isinstance(cell, MergedCell): 
            continue
        if cell.value:
            max_length = max(max_length, len(str(cell.value).replace("\n", " ")))
    ws.column_dimensions[col_letter].width = max_length + 5  # Устанавливаем ширину столбца


# Добавляем жирные линии
thin = Side(border_style="thin", color="000000")

# 2. Жирные линии перед началом каждого дня недели
for day_idx, day in enumerate(days_of_week):
    start_col = day_idx * len(lesson_numbers) + 2 
    for cell in ws.iter_cols(min_col=start_col - 1, max_col=start_col - 1, min_row=3, max_row=ws.max_row):
        for c in cell:
            c.border = Border(right=thin)

# Объединение ячеек для дней недели
for day_idx, day in enumerate(days_of_week):
    start_col = day_idx * len(lesson_numbers) + 2
    end_col = start_col + len(lesson_numbers) - 1  
    ws.merge_cells(start_row=2, start_column=start_col, end_row=2, end_column=end_col)
    merged_cell = ws.cell(row=2, column=start_col)
    merged_cell.value = day
    merged_cell.alignment = Alignment(horizontal="center", vertical="center")
    merged_cell.font = Font(bold=True)


# Сохраняем файл
wb.save('teacher_schedule.xlsx')
print("Файл успешно сохранен")