import re

def process_line(line):
    # Заменяем все вхождения вида !!<<...>> на токен PN
    line = re.sub(r'«.*?»', 'pn', line)
    # Удаляем знаки препинания (. ! ? и т.п.) в конце предложения
    line = re.sub(r'[.?«!»]+$', '', line)
    return line

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile:
        # Читаем строки; каждое предложение — это отдельная строка
        lines = infile.readlines()
    
    # Применяем обработку к каждой строке (также убираем лишние пробелы по краям)
    processed_lines = [process_line(line.strip()) for line in lines if line.strip()]
    
    # Записываем обработанные строки в выходной файл
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in processed_lines:
            outfile.write(line + '\n')

if __name__ == '__main__':
    process_file('avaricsent1.txt', 'avaricsent1_pre.txt')
    process_file('avaricsent2.txt', 'avaricsent2_pre.txt')
