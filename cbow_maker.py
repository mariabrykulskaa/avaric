import io
from gensim.models import Word2Vec

IGNORE_TOKENS = {"pron", "pn", "di", "fam"}  # Множество "стоп-слов"

def load_corpus_filtered(fname):
    """
    Читает файл построчно, каждую строку разбивает на слова.
    Исключает слова, которые:
      - короче 3 символов,
      - входят в IGNORE_TOKENS (сравнение в нижнем регистре).
    Возвращает список списков слов (documents).
    """
    documents = []
    with io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore') as fin:
        for line in fin:
            raw_tokens = line.strip().split()
            filtered_tokens = [
                t for t in raw_tokens
                if len(t) >= 3 and t.lower() not in IGNORE_TOKENS
            ]
            if filtered_tokens:
                documents.append(filtered_tokens)
    return documents

def save_dictionary(fname, dictionary, shape):
    """
    Сохраняет словарь слов и их векторных представлений в текстовый файл.
    Первая строка: N D, где N – число слов, D – размерность векторов.
    Далее N строк: <слово> <v1> <v2> ... <vD>.
    """
    length, dimension = shape
    with io.open(fname, 'w', encoding='utf-8') as fout:
        fout.write(f"{length} {dimension}\n")
        for word in dictionary:
            vector_str = " ".join(map(str, dictionary[word]))
            fout.write(f"{word} {vector_str}\n")

# 1. Загружаем документы из двух файлов с учётом фильтрации
documents1 = load_corpus_filtered("avaricsent_prelast1.2.txt")
documents2 = load_corpus_filtered("avaricsent_prelast2.2.txt")

# 2. Объединяем всё в один список
documents = documents1 + documents2

# 3. Тренируем модель CBOW (sg=0) с нужными параметрами
model = Word2Vec(
    sentences=documents,
    vector_size=8,    # размерность векторов 8
    window=5,         # "окно" контекста
    min_count=2,      # игнорируем слова, которые встретились меньше 2 раз
    sg=0,             # CBOW
    workers=4,        # число потоков
    epochs=5          # число эпох
)

# 4. Извлекаем словарь {слово: вектор}
dictionary = {word: model.wv[word] for word in model.wv.key_to_index}

# 5. Сохраняем словарь в файл
save_dictionary("avaricsent_dictionary_cbow.txt", dictionary, (len(dictionary), 8))

print("CBOW-модель (dim=8, min_count=2) обучена и сохранена в avaricsent_dictionary_cbow.txt")
