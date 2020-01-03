import requests
import json
import pprint
from statistics import mean
from math import floor, ceil

skills = {}
sum_of_skills = 0
sum_item = 0
salary = []
requirements = []


url = 'https://api.hh.ru/vacancies'
vacancy = input('Введите название вакансии : ')
if not vacancy:
    vacancy = 'python developer'
area = input('Введите название региона : ')
if not area:
    area = '1'

params = {
    'text': vacancy,
    'area': area
    }

result = requests.get(url, params=params).json()
items = result['items']
found = result['found']
pages = result['pages']

for current_page in range(1, pages):
    params['page'] = current_page

    #print(len(items))
    for item in items:
        url = item['url']
        result = requests.get(url).json()
        if result['key_skills']:
            sum_item += 1
        if result['salary']:
            val = item['salary']
            salary.append(val['from'])
        for skill in result['key_skills']:
            if skill['name'] in skills:
                skills[skill['name']] += 1
            else:
                skills[skill['name']] = 1
            sum_of_skills += 1
        result_sort = sorted(skills.items(), key=lambda x: x[1], reverse=True)
        average_salary = round(sum(salary) / len(salary), 2)
        print(f'Всего найдено {found} вакансий', '\n')
        # items = result['item']
        # print(len(items))

        for key, val in result_sort:
            for_file = {'name': key, 'count': val, 'percent': round(val / sum_of_skills * 100, 2)}
            requirements.append(for_file)
            file_name = str(vacancy)
            file = {'keywords': vacancy, 'count': sum_of_skills,
                    'requirements': requirements}
            print(key, 'требуется в', round(val / sum_item * 100, 2), '%', 'найденных вакансий')
            #print('Всего упоминаний:', val)
            print('Это', round(val / sum_of_skills * 100, 2), '%', 'среди всех ключевых навыков', '\n')
            print('Средняя зарплата от:', average_salary)
            #print(current_page)
        # with open(file_name + '.json', 'w', encoding='utf-8') as f:
        #     json.dump(file, f, ensure_ascii=False)


