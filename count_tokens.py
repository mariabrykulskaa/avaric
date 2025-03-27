def count_specific_tokens_in_file(filename):
    """
    Читает файл, разбивает его содержимое на слова (токены) и возвращает
    количество токенов 'di' и 'pron'.
    """
    with open(filename, "r", encoding="utf-8") as f:
        tokens = f.read().split()
    di_count = tokens.count("di")
    pron_count = tokens.count("pron")
    return di_count, pron_count

# Имена файлов с обработанными данными
file1 = "avaricsentlemmatoktolow1_num2.2.txt"
file2 = "avaricsentlemmatoktolow2_num2.2.txt"

# Подсчет токенов для каждого файла
di_count1, pron_count1 = count_specific_tokens_in_file(file1)
di_count2, pron_count2 = count_specific_tokens_in_file(file2)

print(f"Файл {file1}:")
print(f"  Количество токенов 'di': {di_count1}")
print(f"  Количество токенов 'pron': {pron_count1}\n")

print(f"Файл {file2}:")
print(f"  Количество токенов 'di': {di_count2}")
print(f"  Количество токенов 'pron': {pron_count2}\n")

print("Общее количество токенов:")
print(f"  'di': {di_count1 + di_count2}")
print(f"  'pron': {pron_count1 + pron_count2}")
