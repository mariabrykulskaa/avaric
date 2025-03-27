import re

# Списки окончаний для фамилий
new_suffixes = ["лы", "лу", "оглу", "сой", "гиль"]

# Традиционные окончания для коренных народов
# Лезгинские окончания для фамилий и патронимов
lezgin_surnames = ["ви", "ан", "ин"]
lezgin_patronymics = ["ар", "ер", "яр", "бур", "динбур"]

# Аварские окончания для фамилий и отчеств
avar_surnames = ["зул"]
avar_patronymics = ["ил", "ав", "ай", "сул", "вич","сул", "овас", "авас", "гун", "ов"]

# Объединяем все окончания в один список
suffixes = new_suffixes + lezgin_surnames + lezgin_patronymics + avar_surnames + avar_patronymics

# Чтобы корректно обрабатывать случаи, когда окончание может быть вложено в другое (например, "оглу" и "лу"),
# сортируем окончания по убыванию длины.
sorted_suffixes = sorted(set(suffixes), key=len, reverse=True)

def is_surname(word):
    """
    Проверяет, является ли слово фамилией по наличию одного из известных суффиксов.
    Сравнение проводится без учёта регистра.
    """
    lw = word.lower()
    for suf in sorted_suffixes:
        if lw.endswith(suf):
            return True
    return False

def replace_surname(match):
    """
    Функция для замены найденного слова.
    Если слово определяется как фамилия, возвращает токен "fam", иначе оставляет слово без изменений.
    """
    word = match.group(0)
    if is_surname(word):
        return "fam"
    else:
        return word

def process_file(input_file, output_file):
    """
    Читает содержимое файла, заменяет слова-фамилии на токен "fam" и записывает результат в новый файл.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Заменяем каждое слово, используя регулярное выражение.
    # Шаблон \b\w+\b находит отдельные слова.
    new_text = re.sub(r'\b\w+\b', replace_surname, text)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_text)

# Обрабатываем оба файла
files = [
    ("avaricsent_prelast1.txt", "avaricsent_prelast1.1.txt"),
    ("avaricsent_prelast2.txt", "avaricsent_prelast2.1.txt")
]

for input_file, output_file in files:
    process_file(input_file, output_file)
    print(f"Обработан файл {input_file} -> {output_file}")
