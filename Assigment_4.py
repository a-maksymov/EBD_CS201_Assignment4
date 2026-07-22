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


#Прочистив увесь ліст оф компрехеншн, від N\A, і перевів числові значення у числа
for lines in dict_of_sales:
    if lines["quantity"] == "N/A":
        lines["quantity"] = 0
    if lines["revenue"] == "N/A":
        lines["revenue"] = 0
    lines["quantity"] = int(lines["quantity"])
    lines["revenue"] = float(lines["revenue"])

#рахуємо чистий прибуток і додаємо нову колонку
for row in dict_of_sales:
    region = row["region"]
    tariff = float(tariffs[region])
    revenue = row["revenue"]
    net_profit = revenue - (revenue * (tariff / 100))
    row["net_profit"] = round(net_profit,2)
#записуємо новий файл
fieldnames = list(dict_of_sales[0].keys())
with open('cleaned_sales_updated.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dict_of_sales)

#сортуємо чистий прибуток по категоріям

profit_in_category = {}

for row in dict_of_sales:

    category = row["product_category"]
    profit = row["net_profit"]

    if category in profit_in_category:
        profit_in_category[category] += profit
    else:
        profit_in_category[category] = profit

print("Сумарний прибуток за категоріями:")
print(profit_in_category)

#рахуємо середнє по категоріям
average_profit = sum(profit_in_category.values()) / len(profit_in_category)
#Використовуємо лямбда фукції для сортування топ категорій
top_categories = dict(filter(lambda item: item[1] > average_profit, profit_in_category.items()))

#Створюємо пустий ліст, як буфер для діставання данних у потрібному порядку(спочатку значення, а тоді категоря, аби можна було нормально відсортувати)
profit_list = []
for category in top_categories:
    profit = top_categories[category]
    profit_list.append([profit, category])
#Сортуємо цей буферний ліст
profit_list.sort(reverse=True)
#Словник для фінального варіанту
sorted_top_categories = {}
for znachennya in profit_list:
    profit = znachennya[0]
    category = znachennya[1]
    sorted_top_categories[category] = profit

print(sorted_top_categories)


#пишемо це у новий JEsusCrist file
with open('top_categories.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_top_categories, file, indent=4)

print("Топ категорії успішно збережено у 'top_categories.json'")