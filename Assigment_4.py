import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
#зчитую json
with open('regional_tariffs.json', 'r') as file:
    tariffs = json.load(file)
#зчитую файл типу ЦеВеликіЯйця
with open('global_sales.csv', 'r') as file:
    reader = csv.DictReader(file)
    dict_of_sales = list(reader)

#чистю словник від N/A
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

#рахую чистий прибуток і додаю нову колонку в наш ліст компрехеншн
for row in dict_of_sales:
    region = row["region"]
    tariff = float(tariffs[region])
    revenue = float(row["revenue"])
    net_profit = revenue - (revenue * (tariff / 100))
    row["net_profit"] = round(net_profit,2)
#записую новий файл
fieldnames = list(dict_of_sales[0].keys())
with open('cleaned_sales_updated.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dict_of_sales)
print("Оновлений ЦеВеликіЯйця.файл успішно збережений до файлу - 'cleaned_sales_updated.csv'")

#сортую чистий прибуток по категоріям

profit_in_category = {}

for row in dict_of_sales:

    category = row["product_category"]
    profit = row["net_profit"]

    if category in profit_in_category:
        profit_in_category[category] += profit
    else:
        profit_in_category[category] = profit

#### print("Сумарний прибуток за категоріями:")
# print(profit_in_category)

#рахую середнє по категоріям
average_profit = sum(profit_in_category.values()) / len(profit_in_category)
#використовую лямбда фукцію для сортування топ категорій
top_categories = dict(filter(lambda item: item[1] > average_profit, profit_in_category.items()))

#Створюю пустий ліст, як буфер для діставання данних у потрібному порядку(спочатку значення, а тоді категоря, аби можна було нормально відсортувати)
profit_list = []
for category in top_categories:
    profit = top_categories[category]
    profit_list.append([profit, category])
#Сортую цей буферний ліст
profit_list.sort(reverse=True)
#Словник для фінального варіанту
sorted_top_categories = {}
for znachennya in profit_list:
    profit = znachennya[0]
    category = znachennya[1]
    sorted_top_categories[category] = profit

# print(sorted_top_categories)


#пишу це у новий JEsusCrist file
with open('top_categories.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_top_categories, file, indent=4)

print("Топ категорії успішно збережено у 'top_categories.json' (JEsusCrist) ")


#Visualisation!!!!
# перетворюю наш відсортований словник на список пар,
# а потім передаємо у датафраме.
# вказую назви колонок
df = pd.DataFrame(list(sorted_top_categories.items()), columns=['Product Category', 'Net Profit'])
# збільшую всі індекси на 1
df.index += 1
# виводю красиву таблицю на екран
print("\nТаблиця топ категорій:")
print(df)

categories = list(sorted_top_categories.keys())
profits = list(sorted_top_categories.values())

# cтворюю чистий листок з конкретними розмірами
fig, aboba = plt.subplots(figsize=(10, 10))

# малюю стовпчики
aboba.bar(categories, profits, color="green", edgecolor="black", zorder=8)

# додаю заголовки та підписи через set_
aboba.set_title("Чистий прибуток за топ-категоріями", fontsize=20, fontweight="bold")
aboba.set_xlabel("Категорії товарів", fontsize=15)
aboba.set_ylabel("Прибуток", fontsize=15)

# сітка
aboba.grid(axis='y', linestyle=':', alpha=1, zorder=3)

# нахиляю підписи категорій
aboba.tick_params(axis='x', rotation=44)

# автоматичне вирівнювання відступів
fig.tight_layout()

# у мене не вийшло через plt.show, тому довелось виводити окремим файлом картинку з графіком, можливо це через лінукс, я не зміг розібратися
plt.savefig('chart_top_categories.png', dpi=200)
print("Графік успішно збережено у файл 'chart_top_categories.png'")