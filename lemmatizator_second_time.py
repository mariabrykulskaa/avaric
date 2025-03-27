import os
import requests

def getlemma(avar_word):
    """
    Возвращает лемму для аварского слова (str).
    Если не найдена, либо возникает ошибка, выбрасывает исключение.
    """
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://avar.me/',
        'sec-ch-ua': '"Chromium";v="130", "YaBrowser";v="24.12", "Not?A_Brand";v="99", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36'),
    }

    params = {
        'lang': 'AV-RU',
        'reqw': avar_word,
        'task': 'result',
    }

    response = requests.get(
        'https://avar.me/api/',
        params=params,
        headers=headers,
        timeout=10  # на случай долгих ответов
    )
    data = response.json()

    # Предположим, что лемма — это data['results'][0][0]
    return data['results'][0][0]

def get_file_line_count(filename):
    """Возвращает количество строк в файле (0, если файл не существует)."""
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def process_file(input_file, output_file):
    """
    Считывает предложения из input_file и записывает обработанные предложения в output_file,
    обрабатывая только слова, начинающиеся с "!!". Для таких слов:
      - удаляет префикс "!!"
      - отправляет запрос getlemma с очищенным словом
      - заменяет слово леммой (если получена непустая лемма)
    Остальные слова остаются без изменений.
    """
    processed_lines = get_file_line_count(output_file)
    total_lines = get_file_line_count(input_file)

    # Счётчики для статистики по успешно обработанным словам (только для слов с "!!")
    total_words_processed = 0
    total_words_lemmatized = 0

    # Чтение всех строк входного файла
    with open(input_file, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()

    # Открываем выходной файл в режиме дозаписи
    with open(output_file, 'a', encoding='utf-8') as fout:
        # Обработка строк, начиная с уже обработанных
        for i, sentence in enumerate(lines[processed_lines:], start=processed_lines):
            sentence = sentence.strip()
            if not sentence:
                fout.write('\n')
                continue

            words = sentence.split()
            processed_words = []

            for w in words:
                # Если слово начинается с "!!", обрабатываем его
                if w.startswith('!!'):
                    total_words_processed += 1
                    clean_word = w[2:]
                    try:
                        lemma = getlemma(clean_word)
                        if lemma:
                            processed_words.append(lemma)
                            total_words_lemmatized += 1
                        else:
                            # Если лемма пустая, оставляем исходное слово
                            processed_words.append(w)
                    except Exception:
                        # При ошибке оставляем исходное слово
                        processed_words.append(w)
                else:
                    # Слова без "!!" оставляем без изменений
                    processed_words.append(w)

            # Запись обработанной строки в выходной файл
            fout.write(' '.join(processed_words) + '\n')

            # Отображение прогресса
            lines_done = i + 1
            progress_percent = lines_done / total_lines * 100 if total_lines else 100
            success_rate = (total_words_lemmatized / total_words_processed * 100
                            if total_words_processed else 100)

            print(f"[{input_file}] Обработано строк: {lines_done}/{total_lines} "
                  f"({progress_percent:.2f}%). Успешная лемматизация слов: {success_rate:.2f}%.")

def main():
    process_file('avaricsentlemmatoktolow2_num2.0.txt', 'avaricsentlemmatoktolow2_num2.1.txt')

if __name__ == '__main__':
    main()
