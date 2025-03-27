import re

def process_line(line):
    # Разбиваем строку на слова по пробельным символам
    tokens = line.split()
    processed_tokens = []
    for token in tokens:
        # Если слово содержит хотя бы одну цифру, заменяем его на токен "числительное"
        if re.search(r'\d', token):
            processed_tokens.append("di")
        else:
            processed_tokens.append(token)
    # Собираем обратно предложение
    return " ".join(processed_tokens)

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    # Обрабатываем каждую строку
    processed_lines = [process_line(line.strip()) for line in lines]
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in processed_lines:
            outfile.write(line + "\n")

if __name__ == '__main__':
    process_file('avaricsentlemmatoktolow1.txt', 'avaricsentlemmatoktolow1_num.txt')
    process_file('avaricsentlemmatoktolow2.txt', 'avaricsentlemmatoktolow2_num.txt')
