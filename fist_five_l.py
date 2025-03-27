from tqdm import tqdm

def get_global_good_words(filenames):
    """
    Собирает корректно отлемматизированные слова (без префикса "!!")
    из списка файлов.
    """
    good_words = []
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                tokens = line.strip().split()
                good_words.extend([token for token in tokens if not token.startswith("!!")])
    return good_words

def process_line(line, global_good_words):
    """
    Обрабатывает одну строку:
      - Делит строку на токены.
      - Если токен начинается с "!!" и его длина (без префикса) >= 5,
        ищет в общем списке слово, первые 5 символов которого совпадают.
      - При успешной замене увеличивает счётчик замен.
      - Возвращает обработанную строку и число произведённых замен.
    """
    tokens = line.split()
    new_tokens = []
    replacements = 0
    for token in tokens:
        if token.startswith("!!"):
            candidate = token[2:]  # убираем префикс "!!"
            if len(candidate) < 5:
                new_tokens.append(token)
            else:
                replacement = None
                for gw in global_good_words:
                    if len(gw) >= 5 and gw[:5] == candidate[:5]:
                        replacement = gw
                        break
                if replacement:
                    new_tokens.append(replacement)
                    replacements += 1
                else:
                    new_tokens.append(token)
        else:
            new_tokens.append(token)
    return " ".join(new_tokens), replacements

def process_file(input_filename, output_filename, global_good_words):
    """
    Читает входной файл, обрабатывает каждую строку с использованием
    глобального списка корректных слов, отображая прогресс с помощью tqdm,
    и записывает результат в выходной файл.
    Возвращает число произведённых замен в файле.
    """
    with open(input_filename, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
    
    processed_lines = []
    file_replacements = 0

    # Используем tqdm для отображения прогресса обработки строк
    for line in tqdm(lines, desc=f"Обработка {input_filename}", unit="строка"):
        processed_line, replacements = process_line(line.strip(), global_good_words)
        processed_lines.append(processed_line)
        file_replacements += replacements
    
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(processed_lines))
    
    return file_replacements

def main():
    input_files = ["avaricsent_prelast1.1.txt", "avaricsent_prelast2.1.txt"]
    # Собираем корректно отлемматизированные слова из обоих файлов
    global_good_words = get_global_good_words(input_files)
    
    total_replacements = 0
#    total_replacements += process_file("avaricsent_prelast1.1.txt", "avaricsent_prelast1.2.txt", global_good_words)
    total_replacements += process_file("avaricsent_prelast2.1.txt", "avaricsent_prelast2.2.txt", global_good_words)
    
    print(f"\nВсего успешно отлематизированных слов (замен): {total_replacements}")

if __name__ == "__main__":
    main()
