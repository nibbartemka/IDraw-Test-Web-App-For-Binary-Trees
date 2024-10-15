import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# % УСПЕШНО ПРОЙДЕННЫХ ПО ОДНОМУ СТ/ШТ
def passed_one_st(ST_name, marks, is_ST, is_group, is_graph):
    passed_one_st_vis = []
    who_to_analyze_list = []

    # Проходимся по каждой группе/году
    for group in marks:
        # Считаем кол-во успешно пройденных для каждой группы
        count_passed = 0
        for mark in marks[group]:
            # Перерасчитываем для 100-балльной системы
            new_mark = mark[0] / mark[1] * 100
            if new_mark >= 60:
                count_passed += 1

        # Узнаём процент успешно пройденных
        passed = (count_passed) / len(marks[group]) * 100
        passed_one_st_vis.append(passed)

        who_to_analyze_list.append(group)

    fig, ax = plt.subplots()
    fig.set_size_inches(10,5)
    
    # График или диаграмма
    if is_graph:
        plt.plot(range(len(passed_one_st_vis)), passed_one_st_vis, marker='o')
    else:
        plt.bar(range(len(passed_one_st_vis)), passed_one_st_vis, edgecolor='black')

    plt.xticks(range(len(passed_one_st_vis)), who_to_analyze_list)
    plt.ylim(0, 110)
    plt.xlabel(f'{"Группа" if is_group else "Года"}')
    plt.ylabel('%')
    what_to_analyze = 'СТ' if is_ST else 'ШТ'
    who_to_analyze = 'групп' if is_group else 'годов'
    plt.title(f'% успешно пройденных {what_to_analyze} {ST_name} у {who_to_analyze} \n{", ".join(who_to_analyze_list)}')

    for i, passed_score in enumerate(passed_one_st_vis):
        plt.text(i, passed_score, f'{passed_score:.2f}', ha='center', va='bottom')

    plt.show()


# % УСПЕШНО ПРОЙДЕННЫХ ПО НЕСКОЛЬКИМ СТ/ШТ
def passed_many_st(ST_name, marks, is_ST, is_group, view, group_text):
    passed_many_st_vis = {}
    who_to_analyze_set = set()
    count_ST = 0

    # Проходимся по каждому СТ/ШТ
    for ST in marks:
        passed_many_st_vis[ST] = []
        count_ST += 1

        # Проходимся по каждой группе/году
        for group in marks[ST]:
            # Если группа/год не проходил(а) СТ/ШТ
            if len(marks[ST][group]) == 0:
                passed = 0
            else:
                # Считаем кол-во успешно пройденных для каждой группы
                count_passed = 0
                for mark in marks[ST][group]:
                    # Перерасчитываем для 100-балльной системы
                    new_mark = mark[0] / mark[1] * 100
                    if new_mark >= 60:
                        count_passed += 1
                # Узнаём % успешно пройденных
                passed = (count_passed) / len(marks[ST][group]) * 100

            passed_many_st_vis[ST].append(round(passed, 2))
            who_to_analyze_set.add(group)

    ind = np.arange(1, len(who_to_analyze_set) + 1)
    width = 1 / (count_ST + 1)

    fig, ax = plt.subplots()
    fig.set_size_inches(10,5)
    
    match view:
        case 'График':
            for ST in passed_many_st_vis:
                plt.plot(range(len(passed_many_st_vis[ST])), passed_many_st_vis[ST], marker='o', label=f'{ST}')

                for j, passed_score in enumerate(passed_many_st_vis[ST]):
                    plt.text(j, passed_score, f'{passed_score:.2f}', ha='center', va='bottom')
            
            plt.xticks(range(len(passed_many_st_vis[ST])), sorted(list(who_to_analyze_set)))
            plt.ylim(0, 110)
            plt.xlabel(f'{"Группа" if is_group else "Года"}')
            plt.ylabel('%')
            plt.legend(bbox_to_anchor=(1, 1))

        case 'Диаграмма':
            i = 1
            for ST in passed_many_st_vis:
                plt.bar(ind + (i - (count_ST + 1)/2) * width, passed_many_st_vis[ST], width, label=f'{ST}')
                
                for j, passed_score in enumerate(passed_many_st_vis[ST]):
                    plt.text(j + 1 + (i - (count_ST + 1)/2) * width, passed_score, f'{passed_score:.2f}', ha='center', va='bottom')
                
                i += 1
            
            plt.xticks(range(1, len(passed_many_st_vis[ST]) + 1), sorted(list(who_to_analyze_set)))
            plt.ylim(0, 110)
            plt.xlabel(f'{"Группа" if is_group else "Года"}')
            plt.ylabel('%')
            plt.legend(bbox_to_anchor=(1, 1))

        case 'Таблица':
            ax.axis('off')
            df = pd.DataFrame.from_dict(passed_many_st_vis)
            ax.table(cellText=df.values, colLabels=df.columns, rowLabels=sorted(list(who_to_analyze_set)), loc='center')
    
    what_to_analyze = 'СТ' if is_ST else 'ШТ'
    who_to_analyze = 'групп' if is_group else 'годов'
    plt.title(f'% успешно пройденных {what_to_analyze} {", ".join(ST_name)} у {who_to_analyze} \n{group_text}')
    plt.show()


# СРЕДНЯЯ ОЦЕНКА ПО ОДНОМУ СТ/ШТ
def avg_score_one_st(ST_name, marks, is_ST, is_group, is_graph):
    avg_score_one_st_vis = []
    who_to_analyze_list = []

    # Проходимся по каждой группе/году
    for group in marks:
        new_marks = []
        for mark in marks[group]:
            # Перерасчитываем для 100-балльной системы
            new_marks.append(mark[0] / mark[1] * 100)
        avg_score_one_st_vis.append(np.mean(new_marks))
        who_to_analyze_list.append(group)

    fig, ax = plt.subplots()
    fig.set_size_inches(10,5)

    # График или диаграмма
    if is_graph:
        plt.plot(range(len(avg_score_one_st_vis)), avg_score_one_st_vis, marker='o')
    else:
        plt.bar(range(len(avg_score_one_st_vis)), avg_score_one_st_vis, edgecolor='black')

    plt.xticks(range(len(avg_score_one_st_vis)), who_to_analyze_list)
    plt.ylim(0, 110)

    plt.xlabel(f'{"Группа" if is_group else "Года"}')
    plt.ylabel('Средняя оценка')
    what_to_analyze = 'СТ' if is_ST else 'ШТ'
    who_to_analyze = 'групп' if is_group else 'годов'
    plt.title(f'Средняя оценка за {what_to_analyze} {ST_name} у {who_to_analyze} \n{", ".join(who_to_analyze_list)}')

    for i, avg_score in enumerate(avg_score_one_st_vis):
        plt.text(i, avg_score, f'{avg_score:.2f}', ha='center', va='bottom')

    plt.show()


# СРЕДНЯЯ ОЦЕНКА ПО НЕСКОЛЬКИМ СТ/ШТ
def avg_score_many_st(ST_name, marks, is_ST, is_group, view, group_text):
    avg_score_many_st_vis = {}
    who_to_analyze_set = set()
    count_ST = 0

    # Проходимся по каждому СТ/ШТ
    for ST in marks:
        avg_score_many_st_vis[ST] = []
        count_ST += 1

        # Проходимся по каждой группе/году
        for group in marks[ST]:
            # Если группа/год не проходил(а) СТ/ШТ
            if len(marks[ST][group]) == 0:
                avg_score_many_st_vis[ST].append(0)
            else:
                new_marks = []
                for mark in marks[ST][group]:
                    # Перерасчитываем для 100-балльной системы
                    new_marks.append(mark[0] / mark[1] * 100)
                # Узнаём среднюю оценку
                avg_score_many_st_vis[ST].append(round(np.mean(new_marks), 2))

            who_to_analyze_set.add(group)

    ind = np.arange(1, len(who_to_analyze_set) + 1)
    width = 1 / (count_ST + 1)

    fig, ax = plt.subplots()
    fig.set_size_inches(10,5)

    match view:
        case 'График':
            for ST in avg_score_many_st_vis:
                plt.plot(range(len(avg_score_many_st_vis[ST])), avg_score_many_st_vis[ST], marker='o', label=f'{ST}')

                for j, avg_score in enumerate(avg_score_many_st_vis[ST]):
                    plt.text(j, avg_score, f'{avg_score:.2f}', ha='center', va='bottom')
            
            plt.xticks(range(len(avg_score_many_st_vis[ST])), sorted(list(who_to_analyze_set)))
            plt.ylim(0, 110)
            plt.xlabel(f'{"Группа" if is_group else "Года"}')
            plt.ylabel('Средняя оценка')
            plt.legend(bbox_to_anchor=(1, 1))

        case 'Диаграмма':
            i = 1
            for ST in avg_score_many_st_vis:
                plt.bar(ind + (i - (count_ST + 1)/2) * width, avg_score_many_st_vis[ST], width, label=f'{ST}')

                for j, avg_score in enumerate(avg_score_many_st_vis[ST]):
                    plt.text(j + 1 + (i - (count_ST + 1)/2) * width, avg_score, f'{avg_score:.2f}', ha='center', va='bottom')
                i += 1

            plt.xticks(range(1, len(avg_score_many_st_vis[ST]) + 1), sorted(list(who_to_analyze_set)))
            plt.ylim(0, 110)
            plt.xlabel(f'{"Группа" if is_group else "Года"}')
            plt.ylabel('Средняя оценка')
            plt.legend(bbox_to_anchor=(1, 1))

        case 'Таблица':
            ax.axis('off')
            df = pd.DataFrame.from_dict(avg_score_many_st_vis)
            df = df.fillna('-')
            ax.table(cellText=df.values, colLabels=df.columns, rowLabels=sorted(list(who_to_analyze_set)), loc='center')

    what_to_analyze = 'СТ' if is_ST else 'ШТ'
    who_to_analyze = 'групп' if is_group else 'годов'
    plt.title(f'Средняя оценка за {what_to_analyze} {", ".join(ST_name)} у {who_to_analyze} \n{group_text}')
    plt.show()


# КОЛ-ВО ОЦЕНОК ПО ОДНОМУ СТ/ШТ
def count_score_one_st(ST_name, marks, is_ST, is_group, is_graph):
    who_to_analyze_list = []
    count_scores = {}
    count_group = 0

    # Проходимся по каждой группе/году
    for group in marks:
        count_scores[group] = [0, 0, 0, 0, 0]
        count_group += 1
        who_to_analyze_list.append(group)

        # Считаем кол-во оценок для каждой группы
        for mark in marks[group]:
            # Перерасчитываем для 100-балльной системы
            new_mark = mark[0] / mark[1] * 100
            if new_mark >= 0 and new_mark <= 20:
                count_scores[group][0] += 1
            elif new_mark >= 21 and new_mark <= 40:
                count_scores[group][1] += 1
            elif new_mark >= 41 and new_mark <= 60:
                count_scores[group][2] += 1
            elif new_mark >= 61 and new_mark <= 80:
                count_scores[group][3] += 1
            elif new_mark >= 81 and new_mark <= 100:
                count_scores[group][4] += 1

    # До 6, так как 5 оценок
    ind = np.arange(1, 6)
    width = 1 / (count_group + 1)

    fig, ax = plt.subplots()
    fig.set_size_inches(15,5)

    if is_graph:
        for group in count_scores:
            plt.plot(range(len(count_scores[group])), count_scores[group], marker='o', label=f'{group}')

            for j, count in enumerate(count_scores[group]):
                plt.text(j, count, f'{count:.2f}', ha='center', va='bottom')

        x_ticks = range(5)
        x_labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
        plt.xticks (ticks=x_ticks, labels=x_labels)

    else:
        i = 1
        for group in count_scores:
            plt.bar(ind + (i - (count_group + 1)/2) * width, count_scores[group], width, label=f'{group}')

            for j, count in enumerate(count_scores[group]):
                plt.text(j + 1 + (i - (count_group + 1)/2) * width, count, f'{count:.2f}', ha='center', va='bottom')
            i += 1

        x_ticks = range(1, 6)
        x_labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
        plt.xticks (ticks=x_ticks, labels=x_labels)

    plt.xlabel('Оценка')
    plt.ylabel('Кол-во студентов')
    what_to_analyze = 'СТ' if is_ST else 'ШТ'
    who_to_analyze = 'групп' if is_group else 'годов'
    plt.title(f'Кол-во оценок за {what_to_analyze} {ST_name} у {who_to_analyze} \n{", ".join(who_to_analyze_list)}')
    plt.legend(bbox_to_anchor=(1, 1))
    plt.show()