import re

def count_unique_words(files):
    unique_words = set()
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read().lower()  # Приводим текст к нижнему регистру для унификации
            # Находим все слова (буквенно-цифровые последовательности)
            words = re.findall(r'\b\w+\b', text)
            unique_words.update(words)
    return len(unique_words)

files = ['avaricsent_prelast1.2.txt', 'avaricsent_prelast2.2.txt']
result = count_unique_words(files)
print("Общее количество разных слов:", result)
