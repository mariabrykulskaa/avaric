import numpy as np

# Загружаем файл
arr = np.load("final_avaric_dict.npy", allow_pickle=True)

# Сам объект лежит внутри scalar-array, поэтому .item()
word2vec = arr.item()

print(type(arr))                   # <class 'numpy.ndarray'>
print(arr.dtype, arr.shape)       # object, ()
print(type(word2vec))             # <class 'dict'>
print("Слов в словаре:", len(word2vec))

for i, (word, vec) in enumerate(word2vec.items()):
#    if i >= 5:
#        break
    print(f"{i+1:>2}. {word!r}:")
    print(vec)  # сам numpy-массив, shape == (80,)
    print()     
