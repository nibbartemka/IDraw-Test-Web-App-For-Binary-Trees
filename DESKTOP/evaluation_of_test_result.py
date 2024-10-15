import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk

from vars import *
from get_data_from_db import *
from display_graphs import *

class EvaluationOfTestResult(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_evaluation_of_test_result()
    
    def init_evaluation_of_test_result(self):
        self.title('Оценка результатов тестируемых')
        self.state('zoomed')
        self.resizable(False, False)
        self.config(bg='#FFFFFF')

        self.grab_set()
        self.focus_set()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

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

        choice_frame = tk.Frame(self, bd=10, bg='#FFFFFF')
        choice_frame.grid(row=1, column=0, sticky='wen')

        info_frame = tk.Frame(self, bd=10, bg='#FFFFFF')
        info_frame.grid(row=1, column=2, sticky='en', padx=10)

        # Загрузка изображения и присвоение к info_label
        info_photo = ImageTk.PhotoImage(Image.open("Текст/Инфо.png"))
        info_label = tk.Label(info_frame, bg='#FFFFFF')
        info_label.image = info_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        info_label.configure(image=info_photo)
        info_label.grid(row=0, column=0, sticky='w')

        # Создаем пользовательский шрифт
        custom_font = font.Font(family="Golos", size=12)

        # Сброс переменных для выбора групп и годов
        def reset_group_year_vars():
            group_var.set([])
            year_var.set([])
            group_selected_var.set([])
            year_selected_var.set([])
        
        # Сброс переменных для выбора СТ и ШТ
        def reset_ST_SHT_vars():
            ST_var.set([])
            SHT_var.set([])
            ST_selected_var.set([])
            SHT_selected_var.set([])

        # Сокрытие виджетов для выбора какие СТ/ШТ анализировать
        def del_number_to_analyze():
            number_to_analyze_ST_label.grid_forget()
            number_to_analyze_SHT_label.grid_forget()
            number_to_analyze_combobox.grid_forget()
            number_to_analyze_frame.grid_forget()
            ST_label.grid_forget()
            frame_number_listbox.grid_forget()
            add_ST_label.grid_forget()
            del_ST_label.grid_forget()
            ST_selected_label.grid_forget()
            frame_selected_number_listbox.grid_forget()
            SHT_label.grid_forget()
            add_SHT_label.grid_forget()
            del_SHT_label.grid_forget()
            SHT_selected_label.grid_forget()
        
        # Сокрытие виджетов для выбора какие группы/года анализировать
        def del_who_to_analyze():
            who_to_analyze_label.grid_forget()
            btn_group.grid_forget()
            btn_year.grid_forget()
            who_to_analyze_frame.grid_forget()
            group_label.grid_forget()
            year_label.grid_forget()
            frame_listbox.grid_forget()
            group_selected_label.grid_forget()
            year_selected_label.grid_forget()
            frame_selected_listbox.grid_forget()
            add_group_label.grid_forget()
            del_group_label.grid_forget()
            add_year_label.grid_forget()
            del_year_label.grid_forget()
        
        # Сокрытие виджетов для выбора вида и кнопки Показать
        def del_view():
            view_label.grid_forget()
            view_combobox.grid_forget()
            analyze_label.grid_forget()


        # После выбора что выводить выводится следующий виджет
        def bind_what_to_draw(event):
            del_number_to_analyze()
            del_who_to_analyze()
            del_view()

            cur_analyze.set('')
            cur_view.set('')
            reset_group_year_vars()
            reset_ST_SHT_vars()

            what_to_analyze_label.grid(row=2, column=0, sticky='w', pady=5)
            analyze_combobox.grid(row=3, column=0, columnspan=2, sticky='w')


        # Загрузка изображения и присвоение к what_to_draw_label
        what_to_draw_photo = ImageTk.PhotoImage(Image.open("Текст/Что_вывести.png"))
        what_to_draw_label = tk.Label(choice_frame, bg='#FFFFFF')
        what_to_draw_label.image = what_to_draw_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        what_to_draw_label.configure(image=what_to_draw_photo)
        what_to_draw_label.grid(row=0, column=0, sticky='w', pady=5)

        cur_draw = tk.StringVar()
        draw_values = ['% успешно пройденных по одному СТ/ШТ', '% успешно пройденных по нескольким СТ/ШТ', 'Средняя оценка по одному СТ/ШТ', 'Средняя оценка по нескольким СТ/ШТ', 'Кол-во оценок по одному СТ/ШТ']
        draw_combobox = ttk.Combobox(choice_frame, textvariable=cur_draw, width=50, values=draw_values, font=custom_font)
        draw_combobox.grid(row=1, column=0, columnspan=2, sticky='w')
        draw_combobox.bind('<<ComboboxSelected>>', bind_what_to_draw)


        # После выбора что анализировать выводится следующий виджет
        def bind_what_to_analyze(event):
            del_who_to_analyze()
            del_view()

            cur_number_analyze.set('')
            cur_view.set('')
            reset_group_year_vars()
            reset_ST_SHT_vars()

            if 'одному' in cur_draw.get():
                number_to_analyze_frame.grid_forget()
                number_to_analyze_ST_label.grid_forget()
                number_to_analyze_SHT_label.grid_forget()

                number_to_analyze_combobox.grid(row=5, column=0, columnspan=2, sticky='w')

                # Заполнение данными в зависимости от выбора, что анализировать
                if cur_analyze.get() == 'Сеанс тестирования':
                    number_to_analyze_ST_label.grid(row=4, column=0, sticky='w', pady=5)
                    number_to_analyze_combobox['values'] = get_ST()

                elif cur_analyze.get() == 'Шаблон тестирования':
                    number_to_analyze_SHT_label.grid(row=4, column=0, sticky='w', pady=5)
                    number_to_analyze_combobox['values'] = get_SHT()
                

            elif 'нескольким' in cur_draw.get():
                number_to_analyze_ST_label.grid_forget()
                number_to_analyze_SHT_label.grid_forget()
                number_to_analyze_combobox.grid_forget()

                number_to_analyze_frame.grid(row=4, column=0, sticky='w')

                if cur_analyze.get() == 'Сеанс тестирования':
                    SHT_label.grid_forget()
                    SHT_listbox.pack_forget()
                    frame_number_listbox.grid_forget()
                    add_SHT_label.grid_forget()
                    del_SHT_label.grid_forget()
                    SHT_selected_label.grid_forget()
                    SHT_selected_listbox.pack_forget()
                    frame_selected_number_listbox.grid_forget()

                    ST_var.set(get_ST())
                    
                    ST_label.grid(row=0, column=0, sticky='w', pady=5)
                    frame_number_listbox.grid(row=1, rowspan=2, column=0, sticky='w')
                    ST_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
                    scroll_number.config(command=ST_listbox.yview)
                    scroll_number.pack(side=tk.RIGHT, fill=tk.Y)

                    add_ST_label.grid(row=1, column=1, sticky='w', padx=10)
                    del_ST_label.grid(row=2, column=1, sticky='w', padx=10)

                    ST_selected_label.grid(row=0, column=2, sticky='w', pady=5)
                    frame_selected_number_listbox.grid(row=1, rowspan=2, column=2, sticky='w')
                    ST_selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
                    scroll_number_selected.config(command=ST_selected_listbox.yview)
                    scroll_number_selected.pack(side=tk.RIGHT, fill=tk.Y)
                
                elif cur_analyze.get() == 'Шаблон тестирования':
                    ST_label.grid_forget()
                    ST_listbox.pack_forget()
                    frame_number_listbox.grid_forget()
                    add_ST_label.grid_forget()
                    del_ST_label.grid_forget()
                    ST_selected_label.grid_forget()
                    ST_selected_listbox.pack_forget()
                    frame_selected_number_listbox.grid_forget()

                    SHT_var.set(get_SHT())

                    SHT_label.grid(row=0, column=0, sticky='w', pady=5)
                    frame_number_listbox.grid(row=1, rowspan=2, column=0, sticky='w')
                    SHT_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
                    scroll_number.config(command=SHT_listbox.yview)
                    scroll_number.pack(side=tk.RIGHT, fill=tk.Y)

                    add_SHT_label.grid(row=1, column=1, sticky='w', padx=10)
                    del_SHT_label.grid(row=2, column=1, sticky='w', padx=10)

                    SHT_selected_label.grid(row=0, column=2, sticky='w', pady=5)
                    frame_selected_number_listbox.grid(row=1, rowspan=2, column=2, sticky='w')
                    SHT_selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
                    scroll_number_selected.config(command=SHT_selected_listbox.yview)
                    scroll_number_selected.pack(side=tk.RIGHT, fill=tk.Y)


        # Загрузка изображения и присвоение к what_to_analyze_label
        what_to_analyze_photo = ImageTk.PhotoImage(Image.open("Текст/Что_анализировать.png"))
        what_to_analyze_label = tk.Label(choice_frame, bg='#FFFFFF')
        what_to_analyze_label.image = what_to_analyze_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        what_to_analyze_label.configure(image=what_to_analyze_photo)

        cur_analyze = tk.StringVar()
        analyze_combobox = ttk.Combobox(choice_frame, textvariable=cur_analyze, width=25, font=custom_font)
        analyze_combobox['values'] = ['Сеанс тестирования', 'Шаблон тестирования']
        analyze_combobox.bind('<<ComboboxSelected>>', bind_what_to_analyze)


        # После выбора какой ст/шт анализировать выводится следующий виджет
        def bind_number_to_analyze(event):
            del_who_to_analyze()
            del_view()

            cur_view.set('')
            reset_group_year_vars()
            reset_ST_SHT_vars()
            
            who_to_analyze_label.grid(row=6, column=0, sticky='w', pady=5)
            btn_group.grid(row=7, column=0, sticky='w')
            btn_year.grid(row=7, column=1, sticky='w')

            if cur_analyze.get() == 'Сеанс тестирования':
                btn_year['state'] = 'disabled'
            elif cur_analyze.get() == 'Шаблон тестирования':
                btn_year['state'] = 'normal'


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
        number_to_analyze_combobox = ttk.Combobox(choice_frame, textvariable=cur_number_analyze, width=35, font=custom_font)
        number_to_analyze_combobox.bind('<<ComboboxSelected>>', bind_number_to_analyze)

        # Фрэйм для красивого вывода при выборе нескольких СТ/ШТ
        number_to_analyze_frame = tk.Frame(choice_frame, bg='#FFFFFF')
        number_to_analyze_frame.columnconfigure(0, weight=1)
        number_to_analyze_frame.columnconfigure(2, weight=1)

        # Загрузка изображения и присвоение к ST_label
        ST_photo = ImageTk.PhotoImage(Image.open("Текст/Выберите_СТ.png"))
        ST_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        ST_label.image = ST_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        ST_label.configure(image=ST_photo)

        # Загрузка изображения и присвоение к SHT_label
        SHT_photo = ImageTk.PhotoImage(Image.open("Текст/Выберите_ШТ.png"))
        SHT_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        SHT_label.image = SHT_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        SHT_label.configure(image=SHT_photo)

        ST_var = tk.Variable()
        SHT_var = tk.Variable()

        # Фрэймы для вывода listbox с scrollbar
        frame_number_listbox = tk.Frame(number_to_analyze_frame, bg='#FFFFFF')
        frame_number_listbox.columnconfigure(0, weight=1)
        scroll_number = tk.Scrollbar(frame_number_listbox, orient=tk.VERTICAL)
        
        frame_selected_number_listbox = tk.Frame(number_to_analyze_frame, bg='#FFFFFF')
        frame_selected_number_listbox.columnconfigure(0, weight=1)
        scroll_number_selected = tk.Scrollbar(frame_selected_number_listbox, orient=tk.VERTICAL)

        # listbox для выбора СТ
        ST_listbox = tk.Listbox(frame_number_listbox, listvariable=ST_var, selectmode=tk.EXTENDED, height=5, width=35, font=custom_font)
        ST_listbox.config(yscrollcommand=scroll_number.set)

        # Загрузка изображения и присвоение к ST_selected_label
        ST_selected_photo = ImageTk.PhotoImage(Image.open("Текст/Выбранные_СТ.png"))
        ST_selected_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        ST_selected_label.image = ST_selected_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        ST_selected_label.configure(image=ST_selected_photo)
        # listbox для выбранных СТ
        ST_selected_var = tk.Variable(value=[])
        ST_selected_listbox = tk.Listbox(frame_selected_number_listbox, listvariable=ST_selected_var, selectmode=tk.EXTENDED, height=5, width=35, font=custom_font)
        ST_selected_listbox.config(yscrollcommand=scroll_number_selected.set)

        # listbox для выбора ШТ
        SHT_listbox = tk.Listbox(frame_number_listbox, listvariable=SHT_var, selectmode=tk.EXTENDED, height=5, font=custom_font)
        SHT_listbox.config(yscrollcommand=scroll_number.set)

        # Загрузка изображения и присвоение к SHT_selected_label
        SHT_selected_photo = ImageTk.PhotoImage(Image.open("Текст/Выбранные_ШТ.png"))
        SHT_selected_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        SHT_selected_label.image = SHT_selected_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        SHT_selected_label.configure(image=SHT_selected_photo)
        # listbox для выбранных ШТ
        SHT_selected_var = tk.Variable(value=[])
        SHT_selected_listbox = tk.Listbox(frame_selected_number_listbox, listvariable=SHT_selected_var, selectmode=tk.EXTENDED, height=5, font=custom_font)
        SHT_selected_listbox.config(yscrollcommand=scroll_number_selected.set)


        # Показать выбор кого анализировать
        def show_who_to_analyze():
            del_who_to_analyze()
            del_view()

            cur_view.set('')
            reset_group_year_vars()
            
            who_to_analyze_label.grid(row=6, column=0, sticky='w', pady=5)
            btn_group.grid(row=7, column=0, sticky='w')
            btn_year.grid(row=7, column=1, sticky='w')

            if cur_analyze.get() == 'Сеанс тестирования':
                btn_year['state'] = 'disabled'
            elif cur_analyze.get() == 'Шаблон тестирования':
                btn_year['state'] = 'normal'


        # Добавление в listbox выбранных СТ
        def add_selected_ST():
            select = list(ST_listbox.curselection())
            select.reverse()
            # ST_list необходим для упорядоченного вывода СТ
            ST_list = list(ST_selected_var.get())
            for i in select:
                ST_list.append(ST_listbox.get(i))
                ST_listbox.delete(i)

            ST_selected_listbox.delete(0, tk.END)
            for ST in sorted(ST_list):
                ST_selected_listbox.insert(tk.END, ST)

            # Если не выбран ни один СТ, то скрываем выбор кого анализировать
            if len(ST_selected_var.get()) == 0:
                del_who_to_analyze()
                del_view()
                cur_view.set('')
                reset_group_year_vars()
            else:
                show_who_to_analyze()

        # Удаление из listbox выбранных СТ
        def del_selected_ST():
            select = list(ST_selected_listbox.curselection())
            select.reverse()
            # ST_list необходим для упорядоченного вывода СТ
            ST_list = list(ST_var.get())
            for i in select:
                ST_list.append(ST_selected_listbox.get(i))
                ST_selected_listbox.delete(i)

            ST_listbox.delete(0, tk.END)
            for ST in sorted(ST_list):
                ST_listbox.insert(tk.END, ST)

            # Если не выбран ни один СТ, то скрываем выбор кого анализировать
            if len(ST_selected_var.get()) == 0:
                del_who_to_analyze()
                del_view()
                cur_view.set('')
                reset_group_year_vars()
            else:
                show_who_to_analyze()


        # Добавление в listbox выбранных ШТ
        def add_selected_SHT():
            select = list(SHT_listbox.curselection())
            select.reverse()

            # SHT_list необходим для упорядоченного вывода ШТ
            SHT_list = list(SHT_selected_var.get())
            for i in select:
                SHT_list.append(SHT_listbox.get(i))
                SHT_listbox.delete(i)

            SHT_selected_listbox.delete(0, tk.END)
            for SHT in sorted(SHT_list):
                SHT_selected_listbox.insert(tk.END, SHT)

            # Если не выбран ни один ШТ, то скрываем выбор кого анализировать
            if len(SHT_selected_var.get()) == 0:
                del_who_to_analyze()
                del_view()
                cur_view.set('')
                reset_group_year_vars()
            else:
                show_who_to_analyze()

        # Удаление из listbox выбранных ШТ
        def del_selected_SHT():
            select = list(SHT_selected_listbox.curselection())
            select.reverse()

            # SHT_list необходим для упорядоченного вывода ШТ
            SHT_list = list(SHT_var.get())
            for i in select:
                SHT_list.append(SHT_selected_listbox.get(i))
                SHT_selected_listbox.delete(i)

            SHT_listbox.delete(0, tk.END)
            for SHT in sorted(SHT_list):
                SHT_listbox.insert(tk.END, SHT)

            # Если не выбран ни один ШТ, то скрываем выбор кого анализировать
            if len(SHT_selected_var.get()) == 0:
                del_who_to_analyze()
                del_view()
                cur_view.set('')
                reset_group_year_vars()
            else:
                show_who_to_analyze()


        # Кнопки для выбора СТ
        # Загрузка изображения и присвоение к add_ST_label
        add_ST_photo = ImageTk.PhotoImage(Image.open("Кнопки/Добавить.png"))
        add_ST_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        add_ST_label.image = add_ST_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        add_ST_label.configure(image=add_ST_photo)

        # Привязываем событие нажатия на картинку к вызову add_selected_ST
        add_ST_label.bind('<Button-1>', lambda event: add_selected_ST())

        # Загрузка изображения и присвоение к del_ST_label
        del_ST_photo = ImageTk.PhotoImage(Image.open("Кнопки/Удалить.png"))
        del_ST_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        del_ST_label.image = del_ST_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        del_ST_label.configure(image=del_ST_photo)

        # Привязываем событие нажатия на картинку к вызову del_selected_ST
        del_ST_label.bind('<Button-1>', lambda event: del_selected_ST())

        # Кнопки для выбора ШТ
        # Загрузка изображения и присвоение к add_SHT_label
        add_SHT_photo = ImageTk.PhotoImage(Image.open("Кнопки/Добавить.png"))
        add_SHT_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        add_SHT_label.image = add_SHT_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        add_SHT_label.configure(image=add_SHT_photo)

        # Привязываем событие нажатия на картинку к вызову add_selected_SHT
        add_SHT_label.bind('<Button-1>', lambda event: add_selected_SHT())

        # Загрузка изображения и присвоение к del_SHT_label
        del_SHT_photo = ImageTk.PhotoImage(Image.open("Кнопки/Удалить.png"))
        del_SHT_label = tk.Label(number_to_analyze_frame, bg='#FFFFFF')
        del_SHT_label.image = del_SHT_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        del_SHT_label.configure(image=del_SHT_photo)

        # Привязываем событие нажатия на картинку к вызову del_selected_SHT
        del_SHT_label.bind('<Button-1>', lambda event: del_selected_SHT())


        # Если выбраны группы
        def select_group():
            year_label.grid_forget()
            year_listbox.pack_forget()
            frame_listbox.grid_forget()
            year_selected_label.grid_forget()
            year_selected_listbox.pack_forget()
            frame_selected_listbox.grid_forget()
            add_group_label.grid_forget()
            del_group_label.grid_forget()
            add_year_label.grid_forget()
            del_year_label.grid_forget()

            del_view()

            cur_view.set('')
            reset_group_year_vars()

            who_to_analyze_frame.grid(row=8, column=0, columnspan=2, sticky='w')

            group_label.grid(row=0, column=0, sticky='w', pady=5)
            frame_listbox.grid(row=1, rowspan=2, column=0, sticky='w')
            group_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
            scroll.config(command=group_listbox.yview)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

            add_group_label.grid(row=1, column=1, sticky='w', padx=10)
            del_group_label.grid(row=2, column=1, sticky='w', padx=10)

            group_selected_label.grid(row=0, column=2, sticky='w', pady=5)
            frame_selected_listbox.grid(row=1, rowspan=2, column=2, sticky='w')
            group_selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
            scroll_selected.config(command=group_selected_listbox.yview)
            scroll_selected.pack(side=tk.RIGHT, fill=tk.Y)

            if 'одному' in cur_draw.get():
                # Заполнение данными в зависимости от выбора, что анализировать
                if cur_analyze.get() == 'Сеанс тестирования':
                    ST_id = cur_number_analyze.get()
                    ST_id = ST_id[ST_id.find('(') + 1 : ST_id.find(')')]
                    # Вызов метода по получению групп из бд, которые проходили СТ. Передаётся id СТ
                    group_var.set(get_groups_ST([ST_id]))

                elif cur_analyze.get() == 'Шаблон тестирования':
                    # Вызов метода по получению групп из бд, которые проходили ШТ. Передаётся id ШТ
                    group_var.set(get_groups_SHT([cur_number_analyze.get()]))
            
            elif 'нескольким' in cur_draw.get():
                if cur_analyze.get() == 'Сеанс тестирования':
                    ST_id_list = []
                    for ST in ST_selected_var.get():
                        ST_id = ST[ST.find('(') + 1 : ST.find(')')]
                        ST_id_list.append(ST_id)

                    group_var.set(get_groups_ST(ST_id_list))
                elif cur_analyze.get() == 'Шаблон тестирования':
                    group_var.set(get_groups_SHT(SHT_selected_var.get()))

        # Если выбраны года
        def select_year():
            group_label.grid_forget()
            group_listbox.pack_forget()
            frame_listbox.grid_forget()
            group_selected_label.grid_forget()
            group_selected_listbox.pack_forget()
            frame_selected_listbox.grid_forget()
            add_group_label.grid_forget()
            del_group_label.grid_forget()
            add_year_label.grid_forget()
            del_year_label.grid_forget()

            del_view()

            cur_view.set('')
            reset_group_year_vars()
            
            who_to_analyze_frame.grid(row=8, column=0, columnspan=2, sticky='w')

            year_label.grid(row=0, column=0, sticky='w', pady=5)
            frame_listbox.grid(row=1, rowspan=2, column=0, sticky='w')
            year_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
            scroll.config(command=year_listbox.yview)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

            add_year_label.grid(row=1, column=1, sticky='w', padx=10)
            del_year_label.grid(row=2, column=1, sticky='w', padx=10)

            year_selected_label.grid(row=0, column=2, sticky='w', pady=5)
            frame_selected_listbox.grid(row=1, rowspan=2, column=2, sticky='w')
            year_selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
            scroll_selected.config(command=year_selected_listbox.yview)
            scroll_selected.pack(side=tk.RIGHT, fill=tk.Y)

            if 'одному' in cur_draw.get():
                # Вызов метода по получению годов из бд, в которые проходили ШТ. Передаётся номер ШТ
                year_var.set(get_years_SHT([cur_number_analyze.get()]))
            
            elif 'нескольким' in cur_draw.get():
                year_var.set(get_years_SHT(SHT_selected_var.get()))


        # Загрузка изображения и присвоение к who_to_analyze_label
        who_to_analyze_photo = ImageTk.PhotoImage(Image.open("Текст/Кого_анализировать.png"))
        who_to_analyze_label = tk.Label(choice_frame, bg='#FFFFFF')
        who_to_analyze_label.image = who_to_analyze_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        who_to_analyze_label.configure(image=who_to_analyze_photo)
        
        selected_who_to_analyze = tk.StringVar()
        btn_group = tk.Radiobutton(choice_frame, bg='#FFFFFF', text='Группы', value='Группы', variable=selected_who_to_analyze, command=select_group, font=custom_font)
        btn_year = tk.Radiobutton(choice_frame, bg='#FFFFFF', text='Года', value='Года', variable=selected_who_to_analyze, command=select_year, font=custom_font)

        # Фрэйм для красивого вывода
        who_to_analyze_frame = tk.Frame(choice_frame, bg='#FFFFFF')
        who_to_analyze_frame.columnconfigure(0, weight=1)
        who_to_analyze_frame.columnconfigure(2, weight=1)

        # Загрузка изображения и присвоение к group_label
        group_photo = ImageTk.PhotoImage(Image.open("Текст/Выберите_группы.png"))
        group_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        group_label.image = group_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        group_label.configure(image=group_photo)

        # Загрузка изображения и присвоение к year_label
        year_photo = ImageTk.PhotoImage(Image.open("Текст/Выберите_года.png"))
        year_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        year_label.image = year_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        year_label.configure(image=year_photo)

        group_var = tk.Variable()
        year_var = tk.Variable()

        # Фрэймы для вывода listbox с scrollbar
        frame_listbox = tk.Frame(who_to_analyze_frame, bg='#FFFFFF')
        frame_listbox.columnconfigure(0, weight=1)
        scroll = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL)
        
        frame_selected_listbox = tk.Frame(who_to_analyze_frame, bg='#FFFFFF')
        frame_selected_listbox.columnconfigure(0, weight=1)
        scroll_selected = tk.Scrollbar(frame_selected_listbox, orient=tk.VERTICAL)

        # listbox для выбора групп
        group_listbox = tk.Listbox(frame_listbox, listvariable=group_var, selectmode=tk.EXTENDED, height=5, font=custom_font)
        group_listbox.config(yscrollcommand=scroll.set)

        # Загрузка изображения и присвоение к group_selected_label
        group_selected_photo = ImageTk.PhotoImage(Image.open("Текст/Выбранные_группы.png"))
        group_selected_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        group_selected_label.image = group_selected_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        group_selected_label.configure(image=group_selected_photo)
        # listbox для выбранных групп
        group_selected_var = tk.Variable(value=[])
        group_selected_listbox = tk.Listbox(frame_selected_listbox, listvariable=group_selected_var, selectmode=tk.EXTENDED, height=5, font=custom_font)
        group_selected_listbox.config(yscrollcommand=scroll.set)

        # listbox для выбора годов
        year_listbox = tk.Listbox(frame_listbox, listvariable=year_var, selectmode=tk.EXTENDED, height=5, font=custom_font)
        year_listbox.config(yscrollcommand=scroll.set)

        # Загрузка изображения и присвоение к year_selected_label
        year_selected_photo = ImageTk.PhotoImage(Image.open("Текст/Выбранные_года.png"))
        year_selected_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        year_selected_label.image = year_selected_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        year_selected_label.configure(image=year_selected_photo)
        # listbox для выбранных годов
        year_selected_var = tk.Variable(value=[])
        year_selected_listbox = tk.Listbox(frame_selected_listbox, listvariable=year_selected_var, selectmode=tk.EXTENDED, height=5, font=custom_font)
        year_selected_listbox.config(yscrollcommand=scroll.set)
        
        # Показать выбор вида анализа
        def show_view():
            del_view()
            view_label.grid(row=9, column=0, sticky='w', pady=5)
            if 'нескольким' in cur_draw.get() and 'Таблица' not in values_view_combobox:
                values_view_combobox.append('Таблица')
            elif 'одному' in cur_draw.get() and 'Таблица' in values_view_combobox:
                values_view_combobox.remove('Таблица')

            view_combobox['values'] = values_view_combobox
            view_combobox.grid(row=10, column=0, sticky='w')
            analyze_label.grid(row=11, column=0, sticky='w', pady=5)


        # Добавление в listbox выбранных групп
        def add_selected_group():
            select = list(group_listbox.curselection())
            select.reverse()
            
            # group_list необходим для упорядоченного вывода групп
            group_list = list(group_selected_var.get())
            for i in select:
                group_list.append(group_listbox.get(i))
                group_listbox.delete(i)

            group_selected_listbox.delete(0, tk.END)
            for group in sorted(group_list):
                group_selected_listbox.insert(tk.END, group)

            # Если не выбран ни одна группа, то скрываем выбор вида анализа
            if len(group_selected_var.get()) == 0:
                del_view()
            else:
                show_view()

        # Удаление из listbox выбранных групп
        def del_selected_group():
            select = list(group_selected_listbox.curselection())
            select.reverse()
            
            # group_list необходим для упорядоченного вывода групп
            group_list = list(group_var.get())
            for i in select:
                group_list.append(group_selected_listbox.get(i))
                group_selected_listbox.delete(i)

            group_listbox.delete(0, tk.END)
            for group in sorted(group_list):
                group_listbox.insert(tk.END, group)

            # Если не выбран ни одна группа, то скрываем выбор вида анализа
            if len(group_selected_var.get()) == 0:
                del_view()
            else:
                show_view()


        # Добавление в listbox выбранных годов
        def add_selected_year():
            select = list(year_listbox.curselection())
            select.reverse()
            
            # year_list необходим для упорядоченного вывода групп
            year_list = list(year_selected_var.get())
            for i in select:
                year_list.append(year_listbox.get(i))
                year_listbox.delete(i)

            year_selected_listbox.delete(0, tk.END)
            for year in sorted(year_list):
                year_selected_listbox.insert(tk.END, year)

            # Если не выбран ни один год, то скрываем выбор вида анализа
            if len(year_selected_var.get()) == 0:
                del_view()
            else:
                show_view()

        # Удаление из listbox выбранных годов
        def del_selected_year():
            select = list(year_selected_listbox.curselection())
            select.reverse()
            
            # year_list необходим для упорядоченного вывода групп
            year_list = list(year_var.get())
            for i in select:
                year_list.append(year_selected_listbox.get(i))
                year_selected_listbox.delete(i)

            year_listbox.delete(0, tk.END)
            for year in sorted(year_list):
                year_listbox.insert(tk.END, year)

            # Если не выбран ни один год, то скрываем выбор вида анализа
            if len(year_selected_var.get()) == 0:
                del_view()
            else:
                show_view()


        # Кнопки для выбора групп
        # Загрузка изображения и присвоение к add_group_label
        add_group_photo = ImageTk.PhotoImage(Image.open("Кнопки/Добавить.png"))
        add_group_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        add_group_label.image = add_group_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        add_group_label.configure(image=add_group_photo)

        # Привязываем событие нажатия на картинку к вызову add_selected_group
        add_group_label.bind('<Button-1>', lambda event: add_selected_group())

        # Загрузка изображения и присвоение к del_group_label
        del_group_photo = ImageTk.PhotoImage(Image.open("Кнопки/Удалить.png"))
        del_group_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        del_group_label.image = del_group_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        del_group_label.configure(image=del_group_photo)

        # Привязываем событие нажатия на картинку к вызову del_selected_group
        del_group_label.bind('<Button-1>', lambda event: del_selected_group())

        # Кнопки для выбора годов
        # Загрузка изображения и присвоение к add_year_label
        add_year_photo = ImageTk.PhotoImage(Image.open("Кнопки/Добавить.png"))
        add_year_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        add_year_label.image = add_year_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        add_year_label.configure(image=add_year_photo)

        # Привязываем событие нажатия на картинку к вызову add_selected_year
        add_year_label.bind('<Button-1>', lambda event: add_selected_year())

        # Загрузка изображения и присвоение к del_year_label
        del_year_photo = ImageTk.PhotoImage(Image.open("Кнопки/Удалить.png"))
        del_year_label = tk.Label(who_to_analyze_frame, bg='#FFFFFF')
        del_year_label.image = del_year_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        del_year_label.configure(image=del_year_photo)

        # Привязываем событие нажатия на картинку к вызову del_selected_year
        del_year_label.bind('<Button-1>', lambda event: del_selected_year())


        # Загрузка изображения и присвоение к view_label
        view_photo = ImageTk.PhotoImage(Image.open("Текст/Вид.png"))
        view_label = tk.Label(choice_frame, bg='#FFFFFF')
        view_label.image = view_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        view_label.configure(image=view_photo)

        cur_view = tk.StringVar()
        values_view_combobox = ['График', 'Диаграмма']
        view_combobox = ttk.Combobox(choice_frame, textvariable=cur_view, width=25, font=custom_font)


        # Проверка, проходил(а) ли группа/год СТ/ШТ
        def check_null_marks(marks):
            group_ST = {}
            res_list = []

            for ST in marks:
                for group in marks[ST]:
                    if group not in group_ST:
                        group_ST[group] = []
                    # Если группа/год не проходила СТ/ШТ, то записываем номер
                    if len(marks[ST][group]) == 0:
                        group_ST[group].append(ST)

            for group in group_ST:
                if len(group_ST[group]) == 0:
                    res_list.append(group)
                else:
                    ST_list = []
                    for ST in group_ST[group]:
                        ST_list.append(str(ST))
                    res_list.append(f'{group} (не пройден {", ".join(ST_list)})')


            return ", ".join(res_list)


        def get_params_to_display(is_one):
            if cur_analyze.get() == 'Сеанс тестирования':
                is_ST = True
                is_group = True
                if is_one:
                    ST_id = cur_number_analyze.get()
                    ST_id = ST_id[ST_id.find('(') + 1 : ST_id.find(')')]

                    marks = get_marks_groups_one_ST(ST_id, group_selected_var.get())
                else:
                    ST_id_list = []
                    for ST in ST_selected_var.get():
                        ST_id = ST[ST.find('(') + 1 : ST.find(')')]
                        ST_id_list.append(ST_id)

                    marks = get_marks_groups_many_ST(ST_id_list, group_selected_var.get())
            
            elif cur_analyze.get() == 'Шаблон тестирования':
                is_ST = False
                if selected_who_to_analyze.get() == 'Группы':
                    is_group = True
                    if is_one:
                        marks = get_marks_groups_one_SHT(cur_number_analyze.get(), group_selected_var.get())
                    else:
                        marks = get_marks_groups_many_SHT(SHT_selected_var.get(), group_selected_var.get())

                elif selected_who_to_analyze.get() == 'Года':
                    is_group = False
                    if is_one:
                        marks = get_marks_years_one_SHT(cur_number_analyze.get(), year_selected_var.get())
                    else:
                        marks = get_marks_years_many_SHT(SHT_selected_var.get(), year_selected_var.get())

            return marks, is_ST, is_group

        def display_graphs():
            match cur_draw.get():
                case '% успешно пройденных по одному СТ/ШТ':
                    marks, is_ST, is_group = get_params_to_display(True)
                    is_graph = True if cur_view.get() == 'График' else False
                    passed_one_st(cur_number_analyze.get(), marks, is_ST, is_group, is_graph)

                case '% успешно пройденных по нескольким СТ/ШТ':
                    marks, is_ST, is_group = get_params_to_display(False)
                    group_text = check_null_marks(marks)
                    if is_ST:
                        names = ST_selected_var.get()
                    else:
                        names = []
                        for SHT in SHT_selected_var.get():
                            names.append(str(SHT))
                    passed_many_st(names, marks, is_ST, is_group, cur_view.get(), group_text)

                case 'Средняя оценка по одному СТ/ШТ':
                    marks, is_ST, is_group = get_params_to_display(True)
                    is_graph = True if cur_view.get() == 'График' else False
                    avg_score_one_st(cur_number_analyze.get(), marks, is_ST, is_group, is_graph)
                    
                case 'Средняя оценка по нескольким СТ/ШТ':
                    marks, is_ST, is_group = get_params_to_display(False)
                    group_text = check_null_marks(marks)
                    if is_ST:
                        names = ST_selected_var.get()
                    else:
                        names = []
                        for SHT in SHT_selected_var.get():
                            names.append(str(SHT))
                    avg_score_many_st(names, marks, is_ST, is_group, cur_view.get(), group_text)
                    
                case 'Кол-во оценок по одному СТ/ШТ':
                    marks, is_ST, is_group = get_params_to_display(True)
                    is_graph = True if cur_view.get() == 'График' else False
                    count_score_one_st(cur_number_analyze.get(), marks, is_ST, is_group, is_graph)


        # Загрузка изображения и присвоение к analyze_label
        analyze_photo = ImageTk.PhotoImage(Image.open("Кнопки/Показать.png"))
        analyze_label = tk.Label(choice_frame, bg='#FFFFFF')
        analyze_label.image = analyze_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        analyze_label.configure(image=analyze_photo)

        # Привязываем событие нажатия на картинку к вызову display_graphs
        analyze_label.bind('<Button-1>', lambda event: display_graphs())


        # Очистка всех виджетов
        def del_all():
            what_to_analyze_label.grid_forget()
            analyze_combobox.grid_forget()

            del_number_to_analyze()
            del_who_to_analyze()
            del_view()

            cur_draw.set('')
            cur_view.set('')
            reset_group_year_vars()


        # Загрузка изображения и присвоение к del_label
        del_photo = ImageTk.PhotoImage(Image.open("Кнопки/Очистить.png"))
        del_label = tk.Label(choice_frame, bg='#FFFFFF')
        del_label.image = del_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        del_label.configure(image=del_photo)
        del_label.grid(row=11, column=2, padx=5, pady=5)

        # Привязываем событие нажатия на картинку к вызову del_all
        del_label.bind('<Button-1>', lambda event: del_all())