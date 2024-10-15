import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk

import pandas as pd
import numpy as np

from vars import *
from get_data_from_db import *

class TestQualityAssessment(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_evaluation_of_test_result()
    
    def init_evaluation_of_test_result(self):
        self.title('Оценка качества теста')
        self.state('zoomed')
        self.resizable(False, False)
        self.config(bg='#FFFFFF')

        self.grab_set()
        self.focus_set()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        # Создаем пользовательский шрифт
        custom_font = font.Font(family="Golos", size=12)
        
        back_frame = tk.Frame(self, bd=10, bg='#FFFFFF')
        back_frame.grid(row=0, column=0, columnspan=2, sticky='we')

        # Загрузка изображения и присвоение к back_label
        back_photo = ImageTk.PhotoImage(Image.open("Кнопки/Назад.png"))
        back_label = tk.Label(back_frame, bg='#FFFFFF')
        back_label.image = back_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        back_label.configure(image=back_photo)
        back_label.grid()

        # Привязываем событие нажатия на картинку к вызову self.destroy()
        back_label.bind('<Button-1>', lambda event: self.destroy())


        # Фрэйм для выбора параметров
        choice_frame = tk.Frame(self, bd=10, bg='#FFFFFF')
        choice_frame.grid(row=1, column=0, sticky='wen')

        # Фрэйм для подсказки
        help_frame = tk.Frame(self, bd=10, bg='#FFFFFF')
        help_frame.grid(row=1, column=1, sticky='en')


        def resize_frame(event):
            # Растягиваем frame на всю площадь canvas
            canvas.itemconfig(frame_id, width=event.width)

        # Отдельный фрэйм, чтобы был скроллбар
        main_frame = tk.Frame(self, bg='#FFFFFF')
        main_frame.grid(row=2, column=0, columnspan=2, sticky='wesn')

        canvas = tk.Canvas(main_frame, bd=0, bg="#FFFFFF")
        frame= tk.Frame(canvas, background="#FFFFFF")
        vsb = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Функция привязки изменения размера Canvas
        canvas.bind('<Configure>', resize_frame)

        frame_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)

        stud_task_frame = tk.Frame(frame, bd=10, bg='#FFFFFF')
        corr_frame = tk.Frame(frame, bd=10, bg='#FFFFFF')

        stud_task_frame.grid_columnconfigure(0, weight=1)
        stud_task_frame.grid_columnconfigure(1, weight=0)
        corr_frame.grid_columnconfigure(0, weight=1)
        corr_frame.grid_columnconfigure(1, weight=0)

        # Фрэйм для изначальной таблицы
        table_frame = tk.Frame(stud_task_frame, bd=10, bg='#FFFFFF')

        # Фрэйм для отсортированной таблицы
        sorted_table_frame = tk.Frame(stud_task_frame, bd=10, bg='#FFFFFF')

        # Фрэйм для корреляционной таблицы
        correlation_table_frame = tk.Frame(corr_frame, bd=10, bg='#FFFFFF')

        # Фрэйм для рекомендаций
        info_frame = tk.Frame(stud_task_frame, bd=10, bg='#FFFFFF')

        good_stud_frame = tk.Frame(info_frame, bd=10)
        bad_stud_frame = tk.Frame(info_frame, bd=10)
        good_task_frame = tk.Frame(info_frame, bd=10)
        bad_task_frame = tk.Frame(info_frame, bd=10)
        dif_frame = tk.Frame(info_frame, bd=10)
        variation_frame = tk.Frame(info_frame, bd=10)

        # Фрэйм для рекомендаций по корреляциям
        corr_info_frame = tk.Frame(corr_frame, bd=10, bg='#FFFFFF')

        big_koef_frame = tk.Frame(corr_info_frame, bd=10)
        small_koef_frame = tk.Frame(corr_info_frame, bd=10)

        # Текст рекомендаций
        good_stud_label = tk.Label(good_stud_frame, font=custom_font)
        bad_stud_label = tk.Label(bad_stud_frame, font=custom_font)
        good_task_label = tk.Label(good_task_frame, font=custom_font)
        bad_task_label = tk.Label(bad_task_frame, font=custom_font)
        dif_label = tk.Label(dif_frame, font=custom_font)
        variation_label = tk.Label(variation_frame, font=custom_font)
        big_koef_label = tk.Label(big_koef_frame, font=custom_font)
        small_koef_label = tk.Label(small_koef_frame, font=custom_font)

        # Фрэйм для итога
        result_frame = tk.Frame(frame, bd=10)

        # Текст итога
        result_label = tk.Label(result_frame, text='ИТОГ', font=custom_font)
        reconsider_label = tk.Label(result_frame, text='Следует пересмотреть', font=custom_font)
        result_stud_label = tk.Label(result_frame, font=custom_font)
        task_stud_label = tk.Label(result_frame, font=custom_font)
        result_dif_label = tk.Label(result_frame, font=custom_font)
        result_variation_label = tk.Label(result_frame, font=custom_font)
        result_big_koef_label = tk.Label(result_frame, font=custom_font)
        result_small_koef_label = tk.Label(result_frame, font=custom_font)

        # Таблицы
        tree = ttk.Treeview(table_frame)
        vert_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        horiz_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        sorted_tree = ttk.Treeview(sorted_table_frame)
        sorted_vert_scrollbar = ttk.Scrollbar(sorted_table_frame, orient="vertical", command=sorted_tree.yview)
        sorted_horiz_scrollbar = ttk.Scrollbar(sorted_table_frame, orient="horizontal", command=sorted_tree.xview)
        correlation_tree = ttk.Treeview(correlation_table_frame)
        correlation_vert_scrollbar = ttk.Scrollbar(correlation_table_frame, orient="vertical", command=correlation_tree.yview)
        correlation_horiz_scrollbar = ttk.Scrollbar(correlation_table_frame, orient="horizontal", command=correlation_tree.xview)
        

        # Загрузка изображения и присвоение к help_label
        help_photo = ImageTk.PhotoImage(Image.open("Текст/Подсказка.png"))
        help_label = tk.Label(help_frame, bg='#FFFFFF')
        help_label.image = help_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        help_label.configure(image=help_photo)

        def reset_number_to_analyze():
            number_to_analyze_ST_label.grid_forget()
            number_to_analyze_SHT_label.grid_forget()
            number_analyze_combobox.grid_forget()
            analyze_label.grid_forget()

            cur_number_analyze.set('')

        def reset_all():
            help_label.grid_forget()
            stud_task_frame.grid_forget()
            corr_frame.grid_forget()
            table_frame.grid_forget()
            tree.pack_forget()
            vert_scrollbar.pack_forget()
            horiz_scrollbar.pack_forget()
            sorted_table_frame.grid_forget()
            sorted_tree.pack_forget()
            sorted_vert_scrollbar.pack_forget()
            sorted_horiz_scrollbar.pack_forget()
            correlation_table_frame.grid_forget()
            correlation_tree.pack_forget()
            correlation_vert_scrollbar.pack_forget()
            correlation_horiz_scrollbar.pack_forget()
            info_frame.grid_forget()
            good_stud_frame.grid_forget()
            bad_stud_frame.grid_forget()
            good_task_frame.grid_forget()
            bad_task_frame.grid_forget()
            dif_frame.grid_forget()
            variation_frame.grid_forget()
            corr_info_frame.grid_forget()
            big_koef_frame.grid_forget()
            small_koef_frame.grid_forget()
            good_stud_label.grid_forget()
            bad_stud_label.grid_forget()
            good_task_label.grid_forget()
            bad_task_label.grid_forget()
            dif_label.grid_forget()
            variation_label.grid_forget()
            big_koef_label.grid_forget()
            small_koef_label.grid_forget()
            result_frame.grid_forget()
            result_label.grid_forget()
            reconsider_label.grid_forget()
            result_stud_label.grid_forget()
            task_stud_label.grid_forget()
            result_dif_label.grid_forget()
            result_variation_label.grid_forget()
            result_big_koef_label.grid_forget()
            result_small_koef_label.grid_forget()


        # После выбора что анализировать выводится следующий виджет
        def bind_what_to_analyze(event):
            reset_number_to_analyze()
            reset_all()

            number_analyze_combobox.grid(row=1, column=1, sticky='w', padx=20)

            # Заполнение данными в зависимости от выбора, что анализировать
            if cur_analyze.get() == 'Сеанс тестирования':
                number_to_analyze_ST_label.grid(row=0, column=1, sticky='w', padx=20)
                number_analyze_combobox['values'] = get_ST()

            elif cur_analyze.get() == 'Шаблон тестирования':
                number_to_analyze_SHT_label.grid(row=0, column=1, sticky='w', padx=20)
                number_analyze_combobox['values'] = get_SHT()


        # Загрузка изображения и присвоение к what_to_analyze_label
        what_to_analyze_photo = ImageTk.PhotoImage(Image.open("Текст/Что_анализировать.png"))
        what_to_analyze_label = tk.Label(choice_frame, bg='#FFFFFF')
        what_to_analyze_label.image = what_to_analyze_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        what_to_analyze_label.configure(image=what_to_analyze_photo)
        what_to_analyze_label.grid(row=0, column=0, sticky='w')

        cur_analyze = tk.StringVar()
        analyze_values = ['Сеанс тестирования', 'Шаблон тестирования']
        analyze_combobox = ttk.Combobox(choice_frame, textvariable=cur_analyze, width=25, values=analyze_values, font=custom_font)
        analyze_combobox.grid(row=1, column=0, sticky='w', padx= 5)
        analyze_combobox.bind('<<ComboboxSelected>>', bind_what_to_analyze)


        # После выбора какой ст/шт анализировать выводится кнопка
        def bind_number_to_analyze(event):
            reset_all()

            analyze_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)


        # Загрузка изображения и присвоение к number_to_analyze_ST_label
        number_to_analyze_ST_photo = ImageTk.PhotoImage(Image.open("Текст/Выберите_сеанс_тестирования.png"))
        number_to_analyze_ST_label = tk.Label(choice_frame, bg='#FFFFFF')
        number_to_analyze_ST_label.image = number_to_analyze_ST_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        number_to_analyze_ST_label.configure(image=number_to_analyze_ST_photo)

        # Загрузка изображения и присвоение к number_to_analyze_SHT_label
        number_to_analyze_SHT_photo = ImageTk.PhotoImage(Image.open("Текст/Выберите_шаблон_тестирования.png"))
        number_to_analyze_SHT_label = tk.Label(choice_frame, bg='#FFFFFF')
        number_to_analyze_SHT_label.image = number_to_analyze_SHT_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        number_to_analyze_SHT_label.configure(image=number_to_analyze_SHT_photo)

        cur_number_analyze = tk.StringVar()
        number_analyze_combobox = ttk.Combobox(choice_frame, textvariable=cur_number_analyze, width=35, font=custom_font)
        number_analyze_combobox.bind('<<ComboboxSelected>>', bind_number_to_analyze)


        # Вычисление коэффициента корреляции Пирсона
        def calculate_pirson(new_df, df, x, i, j, num_stud):
            sumxy = 0
            sumx = 0
            sumy = 0
            for index, row in new_df.iterrows():
                sumxy += round(row[x] * row.iloc[j], 4)
                # Суммируются возведённые в квадрат баллы за тестовое задание
                sumx += round(row[x] ** 2, 4)
                sumy += round(row.iloc[j] ** 2, 4)

            # Получение вариации тестовых заданий
            pjx = df.iloc[df.index.get_loc('pj'), i]
            pjy = df.iloc[df.index.get_loc('pj'), j]

            # Вычисление числителя
            numerator  = round(sumxy - (num_stud * pjx * pjy), 4)

            # Вычисление выражения под корнем
            sqrtx = round((sumx - (num_stud * (pjx ** 2))), 4)
            sqrty = round((sumy - (num_stud * (pjy ** 2))), 4)

            # Вычисление знаменателя
            denominator = round(np.sqrt(sqrtx * sqrty), 4)

            # Вычисление коэффициента корреляции Пирсона
            pirs = round(numerator / denominator, 4)

            return pirs

        def analyze():
            if cur_analyze.get() == 'Сеанс тестирования':
                stud_task_frame.grid(row=1, column=0, sticky='wen')
                corr_frame.grid(row=2, column=0, sticky='wen')

                table_frame.grid(row=1, column=0, sticky='wen')
                sorted_table_frame.grid(row=2, column=0, sticky='wen')
                info_frame.grid(row=1, rowspan=2, column=1, sticky='wen', padx=10, pady=10)
                
                correlation_table_frame.grid(row=1, column=0, sticky='wen')
                corr_info_frame.grid(row=1, column=1, sticky='wen')
                
                result_frame.grid(row=3, column=0, sticky='wesn', padx=10, pady=10)

                help_label.grid(row=0, column=0, sticky='w')

                ST_id = cur_number_analyze.get()
                ST_id = ST_id[ST_id.find('(') + 1 : ST_id.find(')')]
                marks = get_marks_ST(ST_id)
                data = {}
                tasks = []
                ind = ''
                first_id = marks[0][0]
                num_stud = 0
                task_difficulty = {}

                text_good_stud = ''
                text_bad_stud = ''
                text_good_task = ''
                text_bad_task = ''

                text_result_stud = ''
                text_result_dif = ''
                text_result_var = ''
                text_result_big_koef = ''
                text_result_small_koef = ''

                for mark in marks:
                    if mark[0] != ind:
                        data[mark[0]] = []
                        ind = mark[0]
                        num_stud += 1
                        
                    data[mark[0]].append(round(mark[1], 2))
                    if ind == first_id:
                        tasks.append(mark[2])
                        task_difficulty[mark[2]] = mark[3]
                

                print(data)
                print(tasks)
                print(num_stud)
                
                print(task_difficulty)

                df = pd.DataFrame(data=data, index=tasks)
                df.loc['Xi'] = (df.sum())
                df = df.T
                df.loc['Rj'] = (df.sum())
                df.loc['Rj', 'Xi'] = np.nan
                print(df)


                # Создание таблицы
                for item in tree.get_children():
                    tree.delete(item)
                tree['columns'] = tuple(df.columns)

                # Вертикальный скролл
                vert_scrollbar.pack(side="right", fill="y")
                tree.configure(yscrollcommand=vert_scrollbar.set)

                # Горизонтальный скролл
                horiz_scrollbar.pack(side="bottom", fill="x")
                tree.configure(xscrollcommand=horiz_scrollbar.set)

                # Добавление заголовков столбцов
                tree.column('#0', anchor='c')
                for col in df.columns:
                    tree.column(col, anchor='e')
                tree.heading('#0', text='')
                for col in df.columns:
                    tree.heading(col, text=col)

                # Заполнение таблицы данными из DataFrame с округлением
                for index, row in df.fillna('').iterrows():
                    values = []
                    for value in row:
                        if isinstance(value, (int, float)):
                            value = round(value, 3)
                            values.append(str(value))
                        else:
                            values.append(str(value))
                    tree.insert('', 'end', text=str(index), values=tuple(values))

                # Размещение таблицы и скроллбаров в окне
                tree.pack(side="left", fill="both", expand=True)
                vert_scrollbar.pack(side="right", fill="y")
                horiz_scrollbar.pack(side="bottom", fill="x")
                

                i = num_stud
                j = len(tasks)
                ind_good_stud_label = set()
                ind_bad_stud_label = set()
                ind_good_task_label = set()
                ind_bad_task_label = set()
                for _ in range(i*j):
                    # Какие студенты выполнили все задания / не выполнили ни одно задание
                    ind_good_stud = []
                    ind_bad_stud = []
                    for index, row in df.iterrows():
                        good_stud = 0
                        bad_stud = 0
                        # Смотрим, как прошёл студент каждое задание
                        for score in row[:-1]:
                            if index == 'Rj':
                                break
                            # Если прошёл отлично
                            if score >= 0.8:
                                good_stud += 1
                            # Если не прошёл
                            elif score < 0.6:
                                bad_stud += 1

                        # Если студент прошёл все задания отлично, запоминаем его
                        if good_stud == len(tasks):
                            ind_good_stud.append(index)
                            ind_good_stud_label.add(index)
                        # Если студент не прошёл ни одно задание, запоминаем его
                        elif bad_stud == len(tasks):
                            ind_bad_stud.append(index)
                            ind_bad_stud_label.add(index)

                    # Студенты, выполнившие все задания
                    if len(ind_good_stud) >= 1:
                        # Расчёт нового Rj
                        for ind in ind_good_stud:
                            row_values = df.loc[ind, :]
                            df.loc['Rj'] = df.loc['Rj'] - row_values
                        
                        # Удаление студентов
                        df = df.drop(ind_good_stud)
                        num_stud -= len(ind_good_stud)

                    # Студенты, не выполнившие ни одно задание
                    if len(ind_bad_stud) >= 1:
                        # Расчёт нового Rj
                        for ind in ind_bad_stud:
                            row_values = df.loc[ind, :]
                            df.loc['Rj'] = df.loc['Rj'] - row_values

                        # Удаление студентов
                        df = df.drop(ind_bad_stud)
                        num_stud -= len(ind_bad_stud)
                    
                    # Какие задания выполнили все студенты / не выполнил ни один студент
                    ind_good_task = []
                    ind_bad_task = []
                    for col in df.columns[:-1]:
                        good_task = 0
                        bad_task = 0
                        # Смотрим, как прошёл задание каждый студент
                        for index, score in df[col].items():
                            if index == 'Rj':
                                break
                            # Если прошёл отлично
                            if score >= 0.8:
                                good_task += 1
                            # Если не прошёл
                            elif score < 0.6:
                                bad_task += 1

                        # Если все студенты прошли задание отлично, запоминаем задание
                        if good_task == num_stud:
                            ind_good_task.append(col)
                            ind_good_task_label.add(str(col))
                        # Если ни один студент не прошёл задание, запоминаем задание
                        elif bad_task == num_stud:
                            ind_bad_task.append(col)
                            ind_bad_task_label.add(str(col))

                    # Задания, которые выполнили все студенты
                    if len(ind_good_task) >= 1:
                        # Расчёт нового Xi
                        for ind in ind_good_task:
                            col_values = df.loc[:, ind]
                            df['Xi'] = df['Xi'] - col_values

                            # Удаление заданий
                            del df[ind]
                            tasks.remove(ind)
                            del task_difficulty[ind]

                    # Задания, которые не выполнил ни один студент
                    if len(ind_bad_task) >= 1:
                        # Расчёт нового Xi
                        for ind in ind_bad_task:
                            col_values = df.loc[:, ind]
                            df['Xi'] = df['Xi'] - col_values

                            # Удаление заданий
                            del df[ind]
                            tasks.remove(ind)
                            del task_difficulty[ind]


                # Рекомендации по студентам, выполнивших все задания
                if len(ind_good_stud_label) > 1:
                    text_good_stud = f'Испытуемые {", ".join(sorted(list(ind_good_stud_label)))} успешно выполнили все задания теста. \nТест не дает информации об испытуемых, за исключением того, \nчто для них все задания слишком легкие.'
                    
                elif len(ind_good_stud_label) == 1:
                    text_good_stud = f'Испытуемый {list(ind_good_stud_label)[0]} успешно выполнил все задания теста. \nТест не дает информации об испытуемом, за исключением того, \nчто для него все задания слишком легкие.'
                
                if text_good_stud != '':
                    good_stud_label['text'] = text_good_stud
                    good_stud_frame.grid(row=0, column=0, sticky='we', pady=5)
                    good_stud_label.grid(row=0, column=0, sticky='w')
                
                # Рекомендации по студентам, не выполнивших ни одно задание
                if len(ind_bad_stud_label) > 1:
                    text_bad_stud += f'Испытуемые {", ".join(sorted(list(ind_bad_stud_label)))} не прошли ни одно задание теста. \nТест не дает информации об испытуемых, за исключением того, \nчто для них все задания слишком сложные.'

                elif len(ind_bad_stud_label) == 1:
                    text_bad_stud += f'Испытуемый {list(ind_bad_stud_label)[0]} не прошёл ни одно задание теста. \nТест не дает информации об испытуемом, за исключением того, \nчто для него все задания слишком сложные.'

                if text_bad_stud != '':
                    bad_stud_label['text'] = text_bad_stud
                    bad_stud_frame.grid(row=1, column=0, sticky='we', pady=5)
                    bad_stud_label.grid(row=0, column=0, sticky='w')

                # Рекомендации по заданиям, которые выполнили все студенты
                if len(ind_good_task_label) > 1:
                    text_good_task = f'Шаблоны тестовых заданий {", ".join(sorted(list(ind_good_task_label)))} успешно выполнили все испытуемые. \nЭти задания не позволяют дифференцировать испытуемых.'
                    
                elif len(ind_good_task_label) == 1:
                    text_good_task = f'Шаблон тестового задания {list(ind_good_task_label)[0]} успешно выполнили все испытуемые. \nЭто задание не позволяет дифференцировать испытуемых.'
                
                if text_good_task != '':
                    good_task_label['text'] = text_good_task
                    good_task_frame.grid(row=2, column=0, sticky='we', pady=5)
                    good_task_label.grid(row=0, column=0, sticky='w')

                # Рекомендации по заданиям, которые не выполнил ни один студент
                if len(ind_bad_task_label) > 1:
                    text_bad_task += f'Шаблоны тестовых заданий {", ".join(sorted(list(ind_bad_task_label)))} не прошли ни один испытуемый. \nЭти задания не позволяют дифференцировать испытуемых.'

                elif len(ind_bad_task_label) == 1:
                    text_bad_task += f'Шаблон тестового задания {list(ind_bad_task_label)[0]} не прошёл ни один испытуемый. \nЭто задание не позволяет дифференцировать испытуемых.'
                    
                if text_bad_task != '':
                    bad_task_label['text'] = text_bad_task
                    bad_task_frame.grid(row=3, column=0, sticky='we', pady=5)
                    bad_task_label.grid(row=0, column=0, sticky='w')


                # Вычитание и деление на кол-во студентов
                df.loc['pj'] = (df.loc['Rj'] / num_stud)
                df.loc['qj'] = (1 - df.loc['pj'])
                df.loc['pjqj'] = (df.loc['pj'] * df.loc['qj'])

                # Сортировка столбцов по убыванию значений в строке Rj
                df = df.sort_values('Rj', axis=1, ascending=False)
                # Сортировка строк по убыванию значений в столбце Xi
                df = df.sort_values('Xi', ascending=False)

                df = df.fillna('')
                print(df)


                # Создание отсортированной таблицы
                for item in sorted_tree.get_children():
                    sorted_tree.delete(item)
                sorted_tree['columns'] = tuple(df.columns)

                # Вертикальный скролл
                sorted_vert_scrollbar.pack(side="right", fill="y")
                sorted_tree.configure(yscrollcommand=sorted_vert_scrollbar.set)

                # Горизонтальный скролл
                sorted_horiz_scrollbar.pack(side="bottom", fill="x")
                sorted_tree.configure(xscrollcommand=sorted_horiz_scrollbar.set)

                # Добавление заголовков столбцов
                sorted_tree.column('#0', anchor='c')
                for col in df.columns:
                    sorted_tree.column(col, anchor='e')
                sorted_tree.heading('#0', text='')
                for col in df.columns:
                    sorted_tree.heading(col, text=col)

                # Заполнение таблицы данными из DataFrame с округлением
                for index, row in df.iterrows():
                    values = []
                    for value in row:
                        if isinstance(value, (int, float)):
                            value = round(value, 3)
                            values.append(str(value))
                        else:
                            values.append(str(value))
                    sorted_tree.insert('', 'end', text=str(index), values=tuple(values))

                # Размещение таблицы и скроллбаров в окне
                sorted_tree.pack(side="left", fill="both", expand=True)
                sorted_vert_scrollbar.pack(side="right", fill="y")
                sorted_horiz_scrollbar.pack(side="bottom", fill="x")


                ind_dif = []
                # Если сложность задания не соответсвует действительности, то запоминаем задание
                for task in task_difficulty:
                    if round(df.loc['qj', task], 2) > task_difficulty[task] + 0.1 or round(df.loc['qj', task], 2) < task_difficulty[task] - 0.1:
                        ind_dif.append(tuple([task, task_difficulty[task], round(df.loc['qj', task], 2)]))

                # Рекомендации по ШТЗ, у которых необходимо изменить сложность
                if len(ind_dif) == 1:
                    dif_label['text'] = f'У шаблона тестового задания {ind_dif[0][0]} \nследует изменить сложность (с {ind_dif[0][1]} на [{round(ind_dif[0][2] - 0.1, 2)}, {round(ind_dif[0][2] + 0.1, 2)}]).'
                    dif_frame.grid(row=4, column=0, sticky='we', pady=5)
                    dif_label.grid(row=0, column=0, sticky='w')
                elif len(ind_dif) > 1:
                    num_task_list = []
                    dif_task_list = []
                    for ind in ind_dif:
                        num_task_list.append(str(ind[0]))
                        dif_task_list.append(f'(у {ind[0]} с {ind[1]} на [{round(ind[2] - 0.1, 2)}, {round(ind[2] + 0.1, 2)}])')
                    dif_task_text = '\n'.join(dif_task_list)
                    dif_label['text'] = f'У шаблонов тестовых заданий {", ".join(num_task_list)} следует изменить сложность \n {dif_task_text}.'
                    dif_frame.grid(row=4, column=0, sticky='we', pady=5)
                    dif_label.grid(row=0, column=0, sticky='w')
                

                ind_var = []
                # Если вариация меньше 0,1, то запоминаем задание
                for task in tasks:
                    if round(df.loc['pjqj', task], 2) < 0.1:
                        ind_var.append(str(task))

                # Рекомендации по ШТЗ, у которых маленькая вариация
                if len(ind_var) == 1:
                    variation_label['text'] = f'Вариация (дисперсия) тестовых баллов у шаблона тестового \nзадания {ind_var[0]} слишком мала. Шаблон тестового задания не может \nдифференцировать студентов по их уровню подготовленности.'
                    variation_frame.grid(row=5, column=0, sticky='we', pady=5)
                    variation_label.grid(row=0, column=0, sticky='w')
                elif len(ind_var) > 1:
                    variation_label['text'] = f'Вариация (дисперсия) тестовых баллов у шаблонов тестовых \nзаданий {", ".join(ind_var)} слишком мала. Шаблоны тестовых заданий не могут \nдифференцировать студентов по их уровню подготовленности.'
                    variation_frame.grid(row=5, column=0, sticky='we', pady=5)
                    variation_label.grid(row=0, column=0, sticky='w')


                # Корреляционная таблица
                tasks = df.columns[:-1]
                print(tasks)

                new_data = {}

                for i in tasks:
                    new_data[i] = [0 for _ in tasks]
                print(new_data)

                # Получаем список всех столбцов, кроме последнего
                cols = df.columns[:-1].tolist()

                # Создаем новый DataFrame, используя эти столбцы
                new_df = df.loc[~df.index.isin(['Rj', 'pj', 'qj', 'pjqj']), cols]

                print(new_df)

                # Вычисление коэффициента корреляции Пирсона для каждого задания
                for i, x in enumerate(tasks):
                    new_data[x][i] = 1
                    for j in range(i+1, len(tasks)):
                        new_data[x][j] = calculate_pirson(new_df, df, x, i, j, num_stud)
                    
                    for j in range(i):
                        new_data[x][j] = calculate_pirson(new_df, df, x, i, j, num_stud)

                print(new_data)

                pirs_df = pd.DataFrame(data=new_data, index=tasks)
                print(pirs_df)
                

                # Создание таблицы
                for item in correlation_tree.get_children():
                    correlation_tree.delete(item)
                correlation_tree['columns'] = tuple(pirs_df.columns)

                # Вертикальный скролл
                correlation_vert_scrollbar.pack(side="right", fill="y")
                correlation_tree.configure(yscrollcommand=correlation_vert_scrollbar.set)

                # Горизонтальный скролл
                correlation_horiz_scrollbar.pack(side="bottom", fill="x")
                correlation_tree.configure(xscrollcommand=correlation_horiz_scrollbar.set)

                # Добавление заголовков столбцов
                correlation_tree.column('#0', anchor='c')
                for col in pirs_df.columns:
                    correlation_tree.column(col, anchor='e')
                correlation_tree.heading('#0', text='')
                for col in pirs_df.columns:
                    correlation_tree.heading(col, text=col)

                # Заполнение таблицы данными из DataFrame с округлением
                for index, row in pirs_df.fillna('').iterrows():
                    values = []
                    for value in row:
                        if isinstance(value, (int, float)):
                            value = round(value, 3)
                            values.append(str(value))
                        else:
                            values.append(str(value))
                    correlation_tree.insert('', 'end', text=str(index), values=tuple(values))

                # Размещение таблицы и скроллбаров в окне
                correlation_tree.pack(side="left", fill="both", expand=True)
                correlation_vert_scrollbar.pack(side="right", fill="y")
                correlation_horiz_scrollbar.pack(side="bottom", fill="x")


                # Перебор коэффициентов корреляции
                big_koef = []
                small_koef = {}
                for i, row in pirs_df.iterrows():
                    small_koef[i] = 0
                    for j, koef in row.items():
                        if i != j and koef > 0.3 and sorted([i, j]) not in big_koef:
                            big_koef.append(sorted([i, j]))
                        elif koef < 0:
                            small_koef[i] += 1

                # Рекомендации по ШТЗ, у которых корреляция слишком высокая
                if len(big_koef) == 1:
                    big_koef_label['text'] = f'Корреляция заданий {big_koef[0][0]} и {big_koef[0][1]} слишком высокая (> 0.3), задания дублируют друг друга.'
                    big_koef_frame.grid(row=6, column=0, sticky='we', pady=5)
                    big_koef_label.grid(row=0, column=0, sticky='w')
                elif len(big_koef) > 1:
                    big_koef_text = []
                    for pair in big_koef:
                        pair_str = [str(task) for task in pair]
                        big_koef_text.append(" и ".join(pair_str))
                    big_koef_text = "\n".join(big_koef_text)

                    big_koef_label['text'] = f'Корреляция заданий \n {big_koef_text} \n слишком высокая (> 0.3), задания дублируют друг друга.'
                    big_koef_frame.grid(row=6, column=0, sticky='we', pady=5)
                    big_koef_label.grid(row=0, column=0, sticky='w')

                # Если у задания отрицательная корреляция с большим кол-вом других заданий, то запоминаем его
                small_koef_list = []
                for task in small_koef:
                    if small_koef[task] >= len(tasks) / 2:
                        small_koef_list.append(str(task))
                
                # Рекомендации по ШТЗ, у которых отрицательная корреляция
                if len(small_koef_list) == 1:
                    small_koef_label['text'] = f'Шаблон тестового задания {small_koef_list[0]} отрицательно коррелирует с большим \nколичеством других заданий. Это означает, что исход ответов на него \nпротивоположен результатам по другим заданиям. По всей вероятности, \nу такого задания имеются грубые ошибки в содержании и (или) оформлении.'
                    small_koef_frame.grid(row=7, column=0, sticky='we', pady=5)
                    small_koef_label.grid(row=0, column=0, sticky='w')
                    
                elif len(small_koef_list) > 1:
                    small_koef_label['text'] = f'Шаблоны тестовых заданий {", ".join(small_koef_list)} отрицательно коррелируют с большим \nколичеством других заданий. Это означает, что исход ответов на них \nпротивоположен результатам по другим заданиям. По всей вероятности, \nу таких заданий имеются грубые ошибки в содержании и (или) оформлении.'
                    small_koef_frame.grid(row=7, column=0, sticky='we', pady=5)
                    small_koef_label.grid(row=0, column=0, sticky='w')
                

                # Итог
                result_label.grid(row=0, column=0, sticky='w')

                res_list = []
                for ind in list(ind_good_stud_label):
                    stud = get_stud(ind)
                    res_list.append(f'испытуемого {ind} {stud[0][0]} {stud[0][1]} ({stud[0][2]})')
                for ind in list(ind_bad_stud_label):
                    stud = get_stud(ind)
                    res_list.append(f'испытуемого {ind} {stud[0][0]} {stud[0][1]} ({stud[0][2]})')
                
                text_result_stud = '\n'.join(res_list)

                if text_result_stud != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_stud_label['text'] = text_result_stud
                    result_stud_label.grid(row=2, column=0, sticky='w')


                res_list = []
                for ind in sorted(list(ind_good_task_label)):
                    res_list.append(f'шаблон тестового задания {ind} (все испытуемые прошли)')
                for ind in sorted(list(ind_bad_task_label)):
                    res_list.append(f'шаблон тестового задания {ind} (ни один из испытуемых прошёл)')
                 
                text_result_task = '\n'.join(res_list)

                if text_result_task != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    task_stud_label['text'] = text_result_task
                    task_stud_label.grid(row=3, column=0, sticky='w')
                

                res_list = []
                for ind in ind_dif:
                    res_list.append(f'шаблон тестового задания {ind[0]} (изменить сложность)')

                text_result_dif = '\n'.join(res_list)

                if text_result_dif != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_dif_label['text'] = text_result_dif
                    result_dif_label.grid(row=4, column=0, sticky='w')


                res_list = []
                for ind in ind_var:
                    res_list.append(f'шаблон тестового задания {ind} (вариация мала)')

                text_result_var = '\n'.join(res_list)

                if text_result_var != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_variation_label['text'] = text_result_var
                    result_variation_label.grid(row=5, column=0, sticky='w')
                

                res_list = []
                for ind in big_koef:
                    res_list.append(f'шаблоны тестовых заданий {ind[0]} и {ind[1]} (корреляция > 0.3)')

                text_result_big_koef = '\n'.join(res_list)

                if text_result_big_koef != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_big_koef_label['text'] = text_result_big_koef
                    result_big_koef_label.grid(row=6, column=0, sticky='w')
                

                res_list = []
                for ind in small_koef_list:
                    res_list.append(f'шаблон тестового задания {ind} (отрицательная корреляция)')

                text_result_small_koef = '\n'.join(res_list)

                if result_small_koef_label != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_small_koef_label['text'] = text_result_small_koef
                    result_small_koef_label.grid(row=7, column=0, sticky='w')


                canvas.update_idletasks() 
                canvas.configure(scrollregion=canvas.bbox("all"))


            elif cur_analyze.get() == 'Шаблон тестирования':
                corr_frame.grid(row=0, column=0, sticky='wen')
                correlation_table_frame.grid(row=0, column=0, sticky='wen')
                corr_info_frame.grid(row=0, column=1, sticky='wen')
                
                result_frame.grid(row=1, column=0, sticky='wesn', padx=10, pady=10)

                SHT_id = cur_number_analyze.get()
                marks = get_marks_SHT(SHT_id)
                data = {}
                tasks = []
                ind = ''
                first_id = marks[0][0]
                num_stud = 0

                text_result_big_koef = ''
                text_result_small_koef = ''

                for mark in marks:
                    if mark[0] != ind:
                        data[mark[0]] = []
                        ind = mark[0]
                        num_stud += 1
                        
                    data[mark[0]].append(round(mark[1], 2))
                    if ind == first_id:
                        tasks.append(mark[2])
                

                print(data)
                print(tasks)
                print(num_stud)
                

                df = pd.DataFrame(data=data, index=tasks)
                df.loc['Xi'] = (df.sum())
                df = df.T
                df.loc['Rj'] = (df.sum())
                df.loc['Rj', 'Xi'] = np.nan
                print(df)

                # Вычитание и деление на кол-во студентов
                df.loc['pj'] = (df.loc['Rj'] / num_stud)
                df.loc['qj'] = (1 - df.loc['pj'])
                df.loc['pjqj'] = (df.loc['pj'] * df.loc['qj'])

                # Сортировка столбцов по убыванию значений в строке Rj
                df = df.sort_values('Rj', axis=1, ascending=False)
                # Сортировка строк по убыванию значений в столбце Xi
                df = df.sort_values('Xi', ascending=False)

                df = df.fillna('')
                print(df)


                # Корреляционная таблица
                tasks = df.columns[:-1]
                print(tasks)

                new_data = {}

                for i in tasks:
                    new_data[i] = [0 for _ in tasks]
                print(new_data)

                # Получаем список всех столбцов, кроме последнего
                cols = df.columns[:-1].tolist()

                # Создаем новый DataFrame, используя эти столбцы
                new_df = df.loc[~df.index.isin(['Rj', 'pj', 'qj', 'pjqj']), cols]

                print(new_df)

                # Вычисление коэффициента корреляции Пирсона для каждого задания
                for i, x in enumerate(tasks):
                    new_data[x][i] = 1
                    for j in range(i+1, len(tasks)):
                        new_data[x][j] = calculate_pirson(new_df, df, x, i, j, num_stud)
                    
                    for j in range(i):
                        new_data[x][j] = calculate_pirson(new_df, df, x, i, j, num_stud)

                print(new_data)

                pirs_df = pd.DataFrame(data=new_data, index=tasks)
                print(pirs_df)


                # Создание таблицы
                for item in correlation_tree.get_children():
                    correlation_tree.delete(item)
                correlation_tree['columns'] = tuple(pirs_df.columns)

                # Вертикальный скролл
                correlation_vert_scrollbar.pack(side="right", fill="y")
                correlation_tree.configure(yscrollcommand=correlation_vert_scrollbar.set)

                # Горизонтальный скролл
                correlation_horiz_scrollbar.pack(side="bottom", fill="x")
                correlation_tree.configure(xscrollcommand=correlation_horiz_scrollbar.set)

                # Добавление заголовков столбцов
                correlation_tree.column('#0', anchor='c')
                for col in pirs_df.columns:
                    correlation_tree.column(col, anchor='e')
                correlation_tree.heading('#0', text='')
                for col in pirs_df.columns:
                    correlation_tree.heading(col, text=col)

                # Заполнение таблицы данными из DataFrame с округлением
                for index, row in pirs_df.fillna('').iterrows():
                    values = []
                    for value in row:
                        if isinstance(value, (int, float)):
                            value = round(value, 3)
                            values.append(str(value))
                        else:
                            values.append(str(value))
                    correlation_tree.insert('', 'end', text=str(index), values=tuple(values))

                # Размещение таблицы и скроллбаров в окне
                correlation_tree.pack(side="left", fill="both", expand=True)
                correlation_vert_scrollbar.pack(side="right", fill="y")
                correlation_horiz_scrollbar.pack(side="bottom", fill="x")
                

                # Перебор коэффициентов корреляции
                big_koef = []
                small_koef = {}
                for i, row in pirs_df.iterrows():
                    small_koef[i] = 0
                    for j, koef in row.items():
                        if i != j and koef > 0.3 and sorted([i, j]) not in big_koef:
                            big_koef.append(sorted([i, j]))
                        elif koef < 0:
                            small_koef[i] += 1

                # Рекомендации по ШТЗ, у которых корреляция слишком высокая
                if len(big_koef) == 1:
                    big_koef_label['text'] = f'Корреляция заданий {big_koef[0][0]} и {big_koef[0][1]} слишком высокая (> 0.3), задания дублируют друг друга.'
                    big_koef_frame.grid(row=0, column=0, sticky='we', pady=5)
                    big_koef_label.grid(row=0, column=0, sticky='w')
                elif len(big_koef) > 1:
                    big_koef_text = []
                    for pair in big_koef:
                        pair_str = [str(task) for task in pair]
                        big_koef_text.append(" и ".join(pair_str))
                    big_koef_text = "\n".join(big_koef_text)
                    
                    big_koef_label['text'] = f'Корреляция заданий \n {big_koef_text} \n слишком высокая (> 0.3), задания дублируют друг друга.'
                    big_koef_frame.grid(row=0, column=0, sticky='we', pady=5)
                    big_koef_label.grid(row=0, column=0, sticky='w')

                # Если у задания отрицательная корреляция с большим кол-вом других заданий, то запоминаем его
                small_koef_list = []
                for task in small_koef:
                    if small_koef[task] >= len(tasks) / 2:
                        small_koef_list.append(str(task))
                
                # Рекомендации по ШТЗ, у которых отрицательная корреляция
                if len(small_koef_list) == 1:
                    small_koef_label['text'] = f'Шаблон тестового задания {small_koef_list[0]} отрицательно коррелирует с большим \nколичеством других заданий. Это означает, что исход ответов на него \nпротивоположен результатам по другим заданиям. По всей вероятности, \nу такого задания имеются грубые ошибки в содержании и (или) оформлении.'
                    small_koef_frame.grid(row=1, column=0, sticky='we', pady=5)
                    small_koef_label.grid(row=0, column=0, sticky='w')
                    
                elif len(small_koef_list) > 1:
                    small_koef_label['text'] = f'Шаблоны тестовых заданий {", ".join(small_koef_list)} отрицательно коррелируют с большим \nколичеством других заданий. Это означает, что исход ответов на них \nпротивоположен результатам по другим заданиям. По всей вероятности, \nу таких заданий имеются грубые ошибки в содержании и (или) оформлении.'
                    small_koef_frame.grid(row=1, column=0, sticky='we', pady=5)
                    small_koef_label.grid(row=0, column=0, sticky='w')
                

                # Итог
                result_label.grid(row=0, column=0, sticky='w')

                res_list = []
                for ind in big_koef:
                    res_list.append(f'шаблоны тестовых заданий {ind[0]} и {ind[1]} (корреляция > 0.3)')

                text_result_big_koef = '\n'.join(res_list)

                if text_result_big_koef != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_big_koef_label['text'] = text_result_big_koef
                    result_big_koef_label.grid(row=2, column=0, sticky='w')
                

                res_list = []
                for ind in small_koef_list:
                    res_list.append(f'шаблон тестового задания {ind} (отрицательная корреляция)')

                text_result_small_koef = '\n'.join(res_list)

                if result_small_koef_label != '':
                    reconsider_label.grid(row=1, column=0, sticky='w')
                    result_small_koef_label['text'] = text_result_small_koef
                    result_small_koef_label.grid(row=3, column=0, sticky='w')


                canvas.update_idletasks() 
                canvas.configure(scrollregion=canvas.bbox("all"))




        # Загрузка изображения и присвоение к analyze_label
        analyze_photo = ImageTk.PhotoImage(Image.open("Кнопки/Анализировать.png"))
        analyze_label = tk.Label(choice_frame, bg='#FFFFFF')
        analyze_label.image = analyze_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        analyze_label.configure(image=analyze_photo)

        # Привязываем событие нажатия на картинку к вызову analyze
        analyze_label.bind('<Button-1>', lambda event: analyze())


        # Очистка всех виджетов
        def del_all():
            reset_number_to_analyze()
            reset_all()

            cur_analyze.set('')


        # Загрузка изображения и присвоение к del_label
        del_photo = ImageTk.PhotoImage(Image.open("Кнопки/Очистить.png"))
        del_label = tk.Label(choice_frame, bg='#FFFFFF')
        del_label.image = del_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        del_label.configure(image=del_photo)
        del_label.grid(row=2, column=1, sticky='w', padx=10, pady=5)

        # Привязываем событие нажатия на картинку к вызову del_all
        del_label.bind('<Button-1>', lambda event: del_all())