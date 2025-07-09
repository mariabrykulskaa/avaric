import numpy as np

def txt_to_npy(input_txt: str, output_npy: str):
    """
    Читает текстовый файл эмбеддингов и сохраняет словарь word->vector в .npy.
    """
    with open(input_txt, 'r', encoding='utf-8') as f:
        total, dim = map(int, f.readline().split())
        words = []
        vectors = np.empty((total, dim), dtype=np.float32)
        for i, line in enumerate(f):
            parts = line.rstrip().split()
            words.append(parts[0])
            vectors[i] = np.fromiter(parts[1:], dtype=np.float32, count=dim)

    # собираем словарь
    word2vec = {word: vectors[idx] for idx, word in enumerate(words)}

    # сохраняем словарь в .npy (pickle внутри)
    np.save(output_npy, word2vec)
    print(f"Сохранено словарь из {len(word2vec)} слов в '{output_npy}'")

if __name__ == '__main__':
    txt_to_npy(
        input_txt="avaricsent_dictionary_cbow_last.txt",
        output_npy="final_avaric_dict.npy"
    )
