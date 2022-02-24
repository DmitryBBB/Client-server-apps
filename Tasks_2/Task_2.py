# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
# количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
# каждого параметра.
import json

from chardet import detect

with open('orders.json', 'rb') as f:
    CONTENT = f.read()
ENCODING = detect(CONTENT)['encoding']
print(ENCODING)


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json') as f:
        dict_json = json.load(f)
        print(dict_json)
        dict_json['orders'].append({
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date,
        })
    with open('orders.json', 'w') as f:
        json.dump(dict_json, f, indent=4, ensure_ascii=False)


write_order_to_json('Лада', 20, 1200000, 'Vasily', '09.02.2022')
