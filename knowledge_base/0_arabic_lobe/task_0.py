import os

def build_arabic_lobe(vocab_file_path: str, output_dir: str = "knowledge_base/0_arabic_lobe"):
    """
    Parses a large Arabic vocabulary file and stores it in the specified output directory.

    Args:
        vocab_file_path: The path to the input Arabic vocabulary file.
        output_dir: The directory where the parsed vocabulary will be stored.
                    Defaults to "knowledge_base/0_arabic_lobe".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    arabic_words = set()
    try:
        with open(vocab_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:  # Ensure the line is not empty
                    arabic_words.add(word)
    except FileNotFoundError:
        print(f"Error: Vocabulary file not found at {vocab_file_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the vocabulary file: {e}")
        return

    # Save the vocabulary to a file in the output directory
    output_file_path = os.path.join(output_dir, "arabic_vocabulary.txt")
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for word in sorted(list(arabic_words)):
                f.write(word + '\n')
        print(f"Successfully built Arabic Lobe. Stored {len(arabic_words)} words in {output_file_path}")
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")

if __name__ == '__main__':
    # Example Usage:
    # 1. Create a dummy vocabulary file for demonstration
    dummy_vocab_path = "arabic_vocab.txt"
    with open(dummy_vocab_path, "w", encoding="utf-8") as f:
        f.write("السلام عليكم\n")
        f.write("العربية\n")
        f.write("اللغة\n")
        f.write("العالم\n")
        f.write("سلام\n")
        f.write("لغة\n")
        f.write("سلام\n") # Duplicate to test set behavior

    # 2. Call the function to build the Arabic Lobe
    build_arabic_lobe(dummy_vocab_path)

    # 3. Clean up the dummy file (optional)
    # os.remove(dummy_vocab_path)
    # os.remove("knowledge_base/0_arabic_lobe/arabic_vocabulary.txt")
    # os.rmdir("knowledge_base/0_arabic_lobe")