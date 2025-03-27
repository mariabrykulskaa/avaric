def process_file(input_filename, output_filename):
    # Открываем входной и выходной файлы с кодировкой UTF-8
    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Убираем пробельные символы в начале и конце строки и разбиваем на слова
            words = line.strip().split()
            processed_words = []
            for word in words:
                # Если слово начинается с '!!', удаляем этот префикс
                if word.startswith("!!"):
                    word = word[2:]
                processed_words.append(word)
            # Собираем строку обратно и записываем в выходной файл
            processed_line = " ".join(processed_words)
            outfile.write(processed_line + "\n")

if __name__ == "__main__":
    process_file("avaricsent_prelast1.2.txt", "avaricsent_prelast1.3.txt")
    process_file("avaricsent_prelast2.2.txt", "avaricsent_prelast2.3.txt")
