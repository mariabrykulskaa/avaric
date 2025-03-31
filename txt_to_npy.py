import numpy as np

def txt_to_npy(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        # Считываем первую строку с количеством записей и размерностью векторов
        header = f.readline().strip()
        num_entries, vector_size = map(int, header.split())
        
        # Инициализируем список для слов и массив для векторов
        words = []
        vectors = np.empty((num_entries, vector_size), dtype=np.float32)
        
        for i, line in enumerate(f):
            parts = line.strip().split()
            if len(parts) != vector_size + 1:
                raise ValueError(f"Ошибка в строке {i+2}: ожидается {vector_size + 1} элементов, получено {len(parts)}")
            word = parts[0]
            vec = list(map(float, parts[1:]))
            words.append(word)
            vectors[i] = vec

    # Сохраняем данные в формате npz с именованными полями
    np.savez(output_filename, words=words, vectors=vectors)
    
if __name__ == '__main__':
    txt_to_npy('avaricsent_dictionary_cbow_last.txt', 'avaricsent_dictionary_cbow_last.npz')
