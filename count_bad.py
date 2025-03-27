import collections

def process_file(file_path, counter):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Разбиваем строку на отдельные слова (предполагается, что слова разделены пробелами)
            words = line.strip().split()
            for word in words:
                if word.startswith('!!'):
                    # Удаляем два первых символа "!!" и приводим к нижнему регистру (если нужно)
                    cleaned_word = word[2:].lower()
                    counter[cleaned_word] += 1

def main():
    counter = collections.Counter()
    files = ['avaricsent_prelast1.1.txt', 'avaricsent_prelast2.1.txt']
    for file in files:
        process_file(file, counter)
    
    # Сортировка по убыванию частоты
    sorted_words = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    with open('output.txt', 'w', encoding='utf-8') as out_file:
        for word, count in sorted_words:
            out_file.write(f"{word} {count}\n")

if __name__ == '__main__':
    main()
