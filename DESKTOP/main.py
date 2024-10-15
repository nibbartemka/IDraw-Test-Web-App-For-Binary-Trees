import tkinter as tk
from PIL import Image, ImageTk

from vars import *

from evaluation_of_test_result import EvaluationOfTestResult
from test_quality_assessment import TestQualityAssessment

# Главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        btn_frame = tk.Frame(bg='#FFFFFF')
        btn_frame.grid(row=0, column=0)


        # Загрузка изображения и присвоение к test_quality_label
        test_quality_photo = ImageTk.PhotoImage(Image.open("Кнопки/Оценка_качества_теста.png"))
        test_quality_label = tk.Label(btn_frame, bg='#FFFFFF')
        test_quality_label.image = test_quality_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        test_quality_label.configure(image=test_quality_photo)
        test_quality_label.grid(sticky='we', pady=10)

        # Привязываем событие нажатия на картинку к вызову self.open_test_quality
        test_quality_label.bind('<Button-1>', lambda event: self.open_test_quality())


        # Загрузка изображения и присвоение к test_result_label
        test_result_photo = ImageTk.PhotoImage(Image.open("Кнопки/Оценка_результатов_тестируемых.png"))
        test_result_label = tk.Label(btn_frame, bg='#FFFFFF')
        test_result_label.image = test_result_photo  # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
        test_result_label.configure(image=test_result_photo)
        test_result_label.grid(sticky='we', pady=10)

        # Привязываем событие нажатия на картинку к вызову self.open_test_result
        test_result_label.bind('<Button-1>', lambda event: self.open_test_result())


    # Открытие оценки качества теста
    def open_test_quality(self):
        TestQualityAssessment()
    
    # Открытие оценки результатов тестируемых
    def open_test_result(self):
        EvaluationOfTestResult()



if __name__ == '__main__':
    app = Main(root)
    app.grid()
    root.title('ЯDraw')
    root.state('zoomed')
    root.resizable(False, False)
    root.config(bg='#FFFFFF')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()