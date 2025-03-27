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
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
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

    # Предположим, что лемма — это data['results'][0][0], 
    # и она существует всегда, когда слово «известно».
    # Если что-то пошло не так — бросим исключение, чтобы обработать в вызывающем коде.
    return data['results'][0][0]

def get_file_line_count(filename):
    """Возвращает количество строк в файле (0, если файл не существует)."""
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def process_file(input_file, output_file):
    """
    Считывает предложения из input_file и записывает лемматизированные
    предложения в output_file, продолжая с того места, где остановились.
    """

    # Сколько строк уже обработано (и записано) в выходной файл
    processed_lines = get_file_line_count(output_file)
    # Общее число строк во входном файле (для прогресса)
    total_lines = get_file_line_count(input_file)

    # Счётчики для подсчёта процента успешно лемматизированных слов
    total_words_processed = 0
    total_words_lemmatized = 0

    # Если в выходном файле уже есть строки, посчитаем,
    # сколько слов там было успешно лемматизировано.
    # Это позволит более точно показывать прогресс «успешных» слов при перезапуске.
    if processed_lines > 0:
        with open(output_file, 'r', encoding='utf-8') as fout:
            for line in fout:
                words_in_line = line.strip().split()
                total_words_processed += len(words_in_line)
                # "!!" считаем признаком неудачной лемматизации
                not_lemmatized = sum(w.startswith('!!') for w in words_in_line)
                total_words_lemmatized += (len(words_in_line) - not_lemmatized)

    # Открываем входной файл, читаем все строки
    with open(input_file, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()

    # Открываем выходной файл в режиме "дозаписи"
    with open(output_file, 'a', encoding='utf-8') as fout:
        # Обрабатываем строки, начиная с processed_lines
        for i, sentence in enumerate(lines[processed_lines:], start=processed_lines):
            sentence = sentence.strip()
            if not sentence:
                fout.write('\n')
                continue

            # Лемматизируем каждое слово
            words = sentence.split()
            lemmatized_words = []

            for w in words:
                total_words_processed += 1
                try:
                    lemma = getlemma(w)
                    # Если вернулась непустая лемма, считаем успехом
                    if lemma:
                        lemmatized_words.append(lemma)
                        total_words_lemmatized += 1
                    else:
                        # Если лемма пустая, считаем как не найденную
                        lemmatized_words.append('!!' + w)
                except Exception:
                    # Если при запросе что-то пошло не так (слово не найдено, ошибка сети и т.п.)
                    lemmatized_words.append('!!' + w)

            # Записываем в выходной файл лемматизированную строку
            fout.write(' '.join(lemmatized_words) + '\n')

            # Прогресс по строкам
            lines_done = i + 1
            progress_percent = lines_done / total_lines * 100 if total_lines else 100

            # Процент успешно лемматизированных слов
            success_rate = (total_words_lemmatized / total_words_processed * 100
                            if total_words_processed else 100)

            print(f"[{input_file}] Обработано строк: {lines_done}/{total_lines} "
                  f"({progress_percent:.2f}%). Успешная лемматизация слов: {success_rate:.2f}%.")

def main():
    process_file('avaricsent1.txt', 'avaricsentlemma1.txt')
    process_file('avaricsent2.txt', 'avaricsentlemma2.txt')

if __name__ == '__main__':
    main()
