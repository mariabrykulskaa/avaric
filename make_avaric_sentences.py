import PyPDF2
import re

def extract_sentences_from_pdf(pdf_path):
    text = ""

    # Шаг 1: Извлекаем текст из PDF
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    # Шаг 2: Разбиваем на предложения по символам . ? !
    sentences = re.split(r'[.?!]+', text)

    result = []
    for s in sentences:
        s = s.strip()
        # Удаляем символы перевода строки
        s = s.replace('\n', ' ')
        # Удаляем всю пунктуацию: оставляем только буквы, цифры и пробелы
        s = re.sub(r'[^\w\s]', '', s)
        # Убираем лишние пробелы между словами
        s = re.sub(r'\s+', ' ', s)
        # Фильтруем: оставляем предложения, в которых больше двух слов
        words = s.split()
        if len(words) > 2:
            result.append(s)

    return result

if __name__ == "__main__":
    pdf_path = "Gamzatov_10tom.pdf"  # Укажите путь к вашему PDF-файлу
    sentences = extract_sentences_from_pdf(pdf_path)

    # Запись обработанных предложений в файл output.txt
    with open("output.txt", "w", encoding="utf-8") as out_file:
        for sent in sentences:
            out_file.write(sent + "\n")
