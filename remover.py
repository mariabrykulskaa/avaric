def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            words = line.strip().split()
            if len(words) < 3:
                continue
            processed_words = []
            for word in words:
                if word.startswith("!!"):
                    word = word[2:]
                processed_words.append(word)
            processed_line = " ".join(processed_words)
            outfile.write(processed_line + "\n")

if __name__ == "__main__":
    process_file("avaricsent_prelast1.1.txt", "avaricsentlast1.txt")
    process_file("avaricsent_prelast2.1.txt", "avaricsentlast2.txt")
