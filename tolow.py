def process_line(line):
    # Переводим строку в нижний регистр
    return line.lower()

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    # Обрабатываем каждую строку
    processed_lines = [process_line(line) for line in lines]
    
    # Записываем результат в выходной файл
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.writelines(processed_lines)

if __name__ == '__main__':
    process_file('avaricsentlemmatok1.txt', 'avaricsentlemmatoktolow1.txt')
    process_file('avaricsentlemmatok2.txt', 'avaricsentlemmatoktolow2.txt')
