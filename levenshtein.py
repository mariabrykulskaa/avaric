import os
from functools import lru_cache

# Здесь укажите нужный алфавит. Если текст на кириллице, можно использовать следующий:
ALPHABET = 'абвггiдежзийккiлмнопрстуфххiцччiшщэюяАБВГГӀДЕЖЗИЙККӀЛМНОПРСТУФХХӀЦЧЧӀШЩЭЮЯ'
# Список специальных токенов, которые не требуется заменять
SPECIAL_TOKENS = {"pn", "di", "pron"}

@lru_cache(maxsize=None)
def levenshtein_distance(s1, s2):
    """
    Вычисляет расстояние Левенштейна между строками s1 и s2.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def build_dictionary(sent_path, lemma_path):
    """
    Читает два файла (предложения и леммы) построчно и строит словарь вида {слово: лемма},
    добавляя только пары, где лемма не начинается с '!!'.
    """
    dictionary = {}
    with open(sent_path, 'r', encoding='utf-8') as f_sent, \
         open(lemma_path, 'r', encoding='utf-8') as f_lemma:
        for line_sent, line_lemma in zip(f_sent, f_lemma):
            words_sent = line_sent.strip().split()
            words_lemma = line_lemma.strip().split()
            for w_s, w_l in zip(words_sent, words_lemma):
                if not w_l.startswith("!!"):
                    dictionary[w_s] = w_l
    return dictionary


def count_lines(file_path):
    """Подсчитывает количество строк в файле."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


def generate_neighbors(word, alphabet=ALPHABET):
    """
    Генерирует все слова, расстояние редактирования до которых равно 1.
    Операции: удаление, замена и вставка символа.
    """
    neighbors = set()
    # Удаления
    for i in range(len(word)):
        neighbors.add(word[:i] + word[i+1:])
    # Замены
    for i in range(len(word)):
        for c in alphabet:
            if c != word[i]:
                neighbors.add(word[:i] + c + word[i+1:])
    # Вставки
    for i in range(len(word) + 1):
        for c in alphabet:
            neighbors.add(word[:i] + c + word[i:])
    return neighbors


def fix_lemmas(sent_path, lemma_path, output_path, dictionary):
    """
    Обрабатывает файлы с предложениями и леммами, исправляя те леммы, которые начинаются с '!!'.
    Если лемма начинается с '!!', генерируются все варианты слова с расстоянием 1 и проверяется,
    есть ли совпадение среди ключей словаря. Если кандидат найден – лемма заменяется.
    
    Специальные токены (pn, di, pron) остаются без изменений.
    
    Реализована возможность продолжить обработку с того места, где остановились.
    Возвращает (total_words, good_lemmas, corrected_count) для текущего запуска.
    """
    processed_lines_existing = 0
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            processed_lines_existing = sum(1 for _ in f)
    
    total_lines = count_lines(sent_path)
    
    total_words = 0
    good_lemmas = 0
    corrected_count = 0
    processed_lines_new = 0  # строки, обработанные в этом запуске
    
    # Преобразуем ключи словаря в set для быстрого поиска
    dictionary_keys = set(dictionary.keys())
    
    with open(sent_path, 'r', encoding='utf-8') as f_sent, \
         open(lemma_path, 'r', encoding='utf-8') as f_lemma, \
         open(output_path, 'a', encoding='utf-8') as f_out:
        
        # Пропускаем уже обработанные строки
        for _ in range(processed_lines_existing):
            next(f_sent, None)
            next(f_lemma, None)
        
        for line_sent, line_lemma in zip(f_sent, f_lemma):
            words_sent = line_sent.strip().split()
            words_lemma = line_lemma.strip().split()
            new_lemma_line = []
            
            for w_s, w_l in zip(words_sent, words_lemma):
                total_words += 1
                # Если токен является специальным, оставляем его без изменений
                if w_s in SPECIAL_TOKENS:
                    new_lemma_line.append(w_s)
                    good_lemmas += 1
                # Если лемма уже корректная, просто добавляем её
                elif not w_l.startswith("!!"):
                    new_lemma_line.append(w_l)
                    good_lemmas += 1
                else:
                    # Если лемма начинается с "!!", пытаемся найти подходящего кандидата
                    neighbors = generate_neighbors(w_s)
                    candidates = dictionary_keys.intersection(neighbors)
                    if candidates:
                        # Берём произвольного кандидата (например, первый)
                        best_key = next(iter(candidates))
                        corrected_lemma = dictionary[best_key]
                        new_lemma_line.append(corrected_lemma)
                        good_lemmas += 1
                        corrected_count += 1
                    else:
                        new_lemma_line.append(w_l)
            
            f_out.write(" ".join(new_lemma_line) + "\n")
            
            processed_lines_new += 1
            total_processed = processed_lines_existing + processed_lines_new
            if processed_lines_new % 10 == 0 or total_processed == total_lines:
                progress = total_processed / total_lines * 100
                print(f"Обработано строк: {total_processed}/{total_lines} ({progress:.2f}%). "
                      f"Исправлено слов (в этом запуске): {corrected_count}")
    
    return total_words, good_lemmas, corrected_count


def main():
    # Строим словарь по парам файлов
    dict1 = build_dictionary("avaricsentlemmatoktolow1_num2.2.txt", "avaricsentlemmatoktolow1_num2.3.txt")
    dict2 = build_dictionary("avaricsentlemmatoktolow2_num2.2.txt", "avaricsentlemmatoktolow2_num2.3.txt")
    
    # Объединяем словари (при совпадении ключей, лемма из второго перезаписывает первую)
    dict_combined = dict1.copy()
    for k, v in dict2.items():
        dict_combined[k] = v
    
    print("Обработка файла avaricsent1.txt ...")
    total_1, good_1, corrected_1 = fix_lemmas("avaricsentlemmatoktolow1_num2.2.txt", 
                                              "avaricsentlemmatoktolow1_num2.3.txt", 
                                              "avaricsent_prelast1.txt",
                                              dict_combined)
    
    print("Обработка файла avaricsent2.txt ...")
    total_2, good_2, corrected_2 = fix_lemmas("avaricsentlemmatoktolow2_num2.2.txt", 
                                              "avaricsentlemmatoktolow2_num2.3.txtt", 
                                              "avaricsent_prelast2.txt",
                                              dict_combined)
    
    total_all = total_1 + total_2
    good_all = good_1 + good_2
    corrected_all = corrected_1 + corrected_2
    percent = 100.0 * good_all / total_all if total_all > 0 else 0.0
    
    print("\nОбработка завершена!")
    print(f"В этом запуске обработано слов: {total_all}")
    print(f"Хорошо отлемматизированных (после исправлений): {good_all}")
    print(f"Общее количество исправленных слов (в этом запуске): {corrected_all}")
    print(f"Процент корректных лемм: {percent:.2f} %")


if __name__ == "__main__":
    main()
