import json
import csv
#зчитуємо json
with open('regional_tariffs.json', 'r') as file:
    tariffs = json.load(file)
#зчитуємо файл типу ЦеВеликіЯйця
with open('global_sales.csv', 'r') as file:
    reader = csv.DictReader(file)
    dict_of_sales = list(reader)

#чистимо словник від N/A
for key in tariffs:

    if tariffs[key] == "N/A":

        tariffs[key] = 0
        