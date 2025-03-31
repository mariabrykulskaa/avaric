import numpy as np
from scipy.spatial.distance import cosine

# Загружаем npz-файл с эмбеддингами
data = np.load('avaricsent_dictionary_cbow_last.npz', allow_pickle=True)
words = data['words']
vectors = data['vectors']

# Создаем словарь: слово -> вектор
embeddings = {word: vectors[i] for i, word in enumerate(words)}

def print_top10(word):
    if word not in embeddings:
        raise ValueError(f"Слово '{word}' отсутствует в эмбеддингах")
    
    target_vector = embeddings[word]

    # Вычисляем косинусное расстояние до всех остальных слов
    similarities = {}
    for other_word, vector in embeddings.items():
        if other_word == word:
            continue
        similarities[other_word] = cosine(target_vector, vector)

    # Сортируем по возрастанию расстояния (наиболее похожие слова первыми)
    top_10 = sorted(similarities.items(), key=lambda x: x[1])[:10]

    # Выводим топ-10 слов
    for other_word, score in top_10:
        print(f"{other_word}: {score:.4f}")
    print()

word = 'яс'
print(f'Слово: {word}\n')
print_top10(word)
