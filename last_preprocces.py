import re

def process_file(input_filename, output_filename):
    # Читаем содержимое файла (предполагается кодировка utf-8)
    with open(input_filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Удаляем все вхождения символа «
    text = text.replace("«", "")
    
    # Задаем список токенов
    tokens = ["pron", "pn", "di", "fam"]
    # Создаем регулярное выражение:
    # \b – граница слова
    # (?=\S*?(pron|pn|di|fam)) – проверяет, что внутри слова содержится один из токенов (захватывая первый найденный)
    # \S+ – само слово (последовательность непробельных символов)
    pattern = r'\b(?=\S*?(pron|pn|di|fam))\S+\b'
    
    # Функция замены: возвращает только захваченный токен
    text = re.sub(pattern, lambda m: m.group(1), text)
    
    # Записываем результат в выходной файл
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text)

# Обработка первого файла
process_file("avaricsentlast1.txt", "avaricsentlast1.1.txt")
# Обработка второго файла
process_file("avaricsentlast2.txt", "avaricsentlast2.1.txt")
