import os
import json
import re

# Constants for Arabic language processing
ARABIC_STOP_WORDS = set([
    "في", "من", "إلى", "على", "عن", "الب", "ال", "و", "ف", "ثم", "أو", "أم",
    "بل", "لا", "لكن", "إن", "أن", "كأن", "لكن", "حتى", "أي", "حيث", "إذ",
    "إذا", "لو", "لما", "ب", "ك", "ل", "يا", "أيها", "أيتها", "أيها", "أي",
    "أنا", "نحن", "أنت", "أنتم", "أنتن", "هو", "هي", "هم", "هن", "هذا", "هذه",
    "هؤلاء", "ذلك", "تلك", "أولئك", "الذي", "التي", "اللذان", "اللتان",
    "الذين", "اللواتي", "اللائي", "ما", "من", "كيف", "متى", "أين", "كم", "ماذا"
])

class ArabicNLPProcessor:
    """
    A class to handle natural language processing tasks specifically for Arabic.
    This includes tokenization, stop word removal, and basic grammatical analysis
    for generating structured output suitable for code generation.
    """

    def __init__(self, knowledge_base_dir="knowledge_base"):
        """
        Initializes the ArabicNLPProcessor.

        Args:
            knowledge_base_dir (str): Directory to store language-related data.
        """
        self.knowledge_base_dir = knowledge_base_dir
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        self.arabic_stopwords_path = os.path.join(self.knowledge_base_dir, "arabic_stopwords.txt")
        self._load_stopwords()

    def _load_stopwords(self):
        """Loads Arabic stop words from a file, or creates one if it doesn't exist."""
        if not os.path.exists(self.arabic_stopwords_path):
            with open(self.arabic_stopwords_path, 'w', encoding='utf-8') as f:
                for word in ARABIC_STOP_WORDS:
                    f.write(word + '\n')
        with open(self.arabic_stopwords_path, 'r', encoding='utf-8') as f:
            self.arabic_stopwords = set([line.strip() for line in f if line.strip()])

    def tokenize_arabic(self, text):
        """
        Tokenizes Arabic text, splitting by common delimiters and spaces,
        and removing punctuation.

        Args:
            text (str): The Arabic text to tokenize.

        Returns:
            list: A list of tokens (words).
        """
        # Remove common Arabic punctuation
        text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
        # Split by spaces
        tokens = text.split()
        return tokens

    def remove_stopwords(self, tokens):
        """
        Removes Arabic stop words from a list of tokens.

        Args:
            tokens (list): A list of Arabic word tokens.

        Returns:
            list: A list of tokens with stop words removed.
        """
        return [token for token in tokens if token.lower() not in self.arabic_stopwords]

    def preprocess_arabic(self, text):
        """
        Performs basic preprocessing on Arabic text: tokenization and stop word removal.

        Args:
            text (str): The Arabic text to preprocess.

        Returns:
            list: A list of preprocessed tokens.
        """
        tokens = self.tokenize_arabic(text)
        preprocessed_tokens = self.remove_stopwords(tokens)
        return preprocessed_tokens

    def extract_intent_and_entities(self, preprocessed_tokens):
        """
        A simplified method to extract potential intents and entities from preprocessed tokens.
        This is a placeholder for more sophisticated NLP techniques (e.g., Named Entity Recognition,
        Intent Classification). For demonstration, it will look for keywords.

        Args:
            preprocessed_tokens (list): A list of preprocessed Arabic tokens.

        Returns:
            dict: A dictionary containing 'intent' and 'entities'.
                  'intent' is a string representing the user's goal.
                  'entities' is a list of identified entities.
        """
        intent = "unknown"
        entities = []

        # Simplified intent recognition based on keywords
        if "إنشاء" in preprocessed_tokens or "بناء" in preprocessed_tokens or "إنشاء تطبيق" in " ".join(preprocessed_tokens):
            intent = "create_app"
        elif "عرض" in preprocessed_tokens or "إظهار" in preprocessed_tokens:
            intent = "display_data"
        elif "تعديل" in preprocessed_tokens or "تحديث" in preprocessed_tokens:
            intent = "update_data"

        # Simplified entity extraction (e.g., nouns that follow certain keywords)
        # This is highly basic and needs significant improvement for real-world use.
        keywords_for_entities = ["اسم", "عنوان", "رسالة", "زر", "قائمة"]
        for i, token in enumerate(preprocessed_tokens):
            if token in keywords_for_entities:
                # Look for the next significant word as an entity value
                if i + 1 < len(preprocessed_tokens) and preprocessed_tokens[i+1] not in self.arabic_stopwords:
                    entities.append({"type": token, "value": preprocessed_tokens[i+1]})
                elif i + 1 < len(preprocessed_tokens): # if the next is a stopword, try to find the next non-stopword
                    for j in range(i + 1, len(preprocessed_tokens)):
                        if preprocessed_tokens[j] not in self.arabic_stopwords:
                            entities.append({"type": token, "value": preprocessed_tokens[j]})
                            break

        # Attempt to extract app names if intent is create_app
        if intent == "create_app":
            app_name_candidates = [t for t in preprocessed_tokens if t not in ARABIC_STOP_WORDS and t not in ["إنشاء", "تطبيق", "اسم"]]
            if app_name_candidates:
                entities.append({"type": "app_name", "value": " ".join(app_name_candidates)})

        return {"intent": intent, "entities": entities}

    def generate_structured_output(self, text):
        """
        Processes Arabic text to generate a structured output suitable for code generation.

        Args:
            text (str): The raw Arabic natural language input.

        Returns:
            dict: A dictionary representing the structured interpretation of the input,
                  including intent and identified entities.
        """
        preprocessed_tokens = self.preprocess_arabic(text)
        structured_data = self.extract_intent_and_entities(preprocessed_tokens)
        return structured_data

    def save_structured_data(self, structured_data, filename="structured_output.json"):
        """
        Saves the structured data to a JSON file.

        Args:
            structured_data (dict): The data to save.
            filename (str): The name of the file to save to.
        """
        filepath = os.path.join(self.knowledge_base_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, ensure_ascii=False, indent=4)
        return filepath

# --- DEMONSTRATION SECTION ---
# This part is for demonstrating the functionality of ArabicNLPProcessor.
# It should not be included in the final integrated module code unless specifically
# requested for testing purposes.

def demonstrate_arabic_nlp_processor():
    """
    Demonstrates the ArabicNLPProcessor functionality.
    """
    print("\n--- Initiating ArabicNLPProcessor Demonstration ---")
    nlp_processor = ArabicNLPProcessor()

    # Test cases
    test_prompts = [
        "أريد إنشاء تطبيق أندرويد جديد باسم 'حاسبتي الذكية'",
        "قم بإنشاء تطبيق لمتابعة المهام",
        "اعرض لي قائمة المستخدمين",
        "حدث معلومات الاتصال",
        "ما هي وظيفة هذا الزر؟",
        "أريد بناء تطبيق لمشاركة الصور"
    ]

    for i, prompt in enumerate(test_prompts):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Original Arabic Prompt: '{prompt}'")

        # Preprocessing
        preprocessed = nlp_processor.preprocess_arabic(prompt)
        print(f"Preprocessed Tokens: {preprocessed}")

        # Extracting intent and entities
        structured_output = nlp_processor.extract_intent_and_entities(preprocessed)
        print(f"Structured Output: {structured_output}")

        # Saving structured data
        saved_path = nlp_processor.save_structured_data(structured_output, filename=f"structured_output_{i+1}.json")
        print(f"Saved structured data to: {saved_path}")

    print("\n--- ArabicNLPProcessor Demonstration Finished ---")

# If you want to run the demonstration when this script is executed directly:
if __name__ == "__main__":
    demonstrate_arabic_nlp_processor()