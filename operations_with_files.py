# записать результаты в указанный файл:
def save_data_to_file(filename, data):
    with open(filename, 'w', encoding='utf8') as f:
        print(data, file=f)


# добавить строки в указанный файл:
def append_data_to_file(filename, data):
    with open(filename, 'a+', encoding='utf8') as f:
        print(data, file=f)
