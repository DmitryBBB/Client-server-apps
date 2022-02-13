# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
# второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число
# с юникод-символом, отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
# При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить
# возможность работы с юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
import yaml

MY_DICT = {
    '1': [1, 'world', 3, 'python'],
    '2': 2,
    '3': {2: '$', 1: '€'},
}


def recording_data_yaml(data):
    with open('file.yaml', 'w', encoding='utf-8') as f_n:
        yaml.dump(data, f_n, default_flow_style=True, allow_unicode=True)
    with open('file.yaml', encoding='utf-8') as f_n:
        print(f_n.read())


recording_data_yaml(MY_DICT)

with open('file.yaml', 'r', encoding='utf-8') as f_out:
    DATA_OUT = yaml.load(f_out, Loader=yaml.SafeLoader)

print(MY_DICT == DATA_OUT)