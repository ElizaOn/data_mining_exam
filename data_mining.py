import re

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

response = requests.get('https://www.luxoft-training.ru/timetable/', verify=False)
parser = BeautifulSoup(response.text)
learning_streams_div = parser.find('div', {'class': 'simple-select category-picker'})
learning_streams_li = learning_streams_div.findAll('li')

learning_streams = []

for li in learning_streams_li:
    learning_streams.append(li.text)

courses = parser.findAll('div', {'class': 'cat-info'})

course_names = []
course_prices = []
course_streams = []

learning_streams_amount = len(learning_streams)

course_stream_amounts = [0] * learning_streams_amount #массив, количество элементов которого равняется количетсву направлений,
#каждый элемент этого массива инициализируем нулем [0, 0, 0, 0] где каждый 0 - это одно из направлений


def get_course_attribute(attribute):
    matches_attributes = [line for line in course.text.split('\n') if f"\'{attribute}\' => " in line]
    match_atrribute = matches_attributes.pop(0)
    return re.sub(rf"('|,|=>|{attribute})", "", match_atrribute).strip()


for course in courses:
    course_names.append(get_course_attribute('name'))
    course_prices.append(get_course_attribute('price'))
    course_streams.append(get_course_attribute('cat_name'))

    for i in range(learning_streams_amount):
        if course.text.__contains__(learning_streams[i]):
            course_stream_amounts[i] += 1
            break

result_array = {'Name': course_names,
                'Price, rub': course_prices,
                'Stream': course_streams}

table = pd.DataFrame(result_array)
table.index += 1
table.to_csv('table.csv', encoding='utf-8-sig')
table.to_excel("table.xlsx", index=False)
print(tabulate(table, headers='keys', tablefmt='psql'))

plt.figure(dpi=100)
plt.pie(course_stream_amounts, labels=learning_streams, autopct='%.f%%', pctdistance=0.8)
plt.axis('equal')
plt.show()