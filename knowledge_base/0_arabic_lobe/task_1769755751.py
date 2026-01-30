import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any

# Define constants for Arabic NLP
ARABIC_NLP_CONFIG_PATH = Path("./arabic_nlp_config.json")
ARABIC_DATASET_DIR = Path("./arabic_datasets")
ARABIC_TRAINED_MODELS_DIR = Path("./arabic_trained_models")
ARABIC_KNOWLEDGE_BASE_DIR = Path("./arabic_knowledge_base")

class ArabicNLPProcessor:
    """
    A module designed to process and generate Arabic natural language.
    It handles tasks like text cleaning, tokenization, language detection,
    and potentially more advanced NLP operations in Arabic.
    """
    def __init__(self, config_path: Path = ARABIC_NLP_CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load_config()
        self.datasets_dir = Path(self.config.get("datasets_dir", str(ARABIC_DATASET_DIR)))
        self.trained_models_dir = Path(self.config.get("trained_models_dir", str(ARABIC_TRAINED_MODELS_DIR)))
        self.knowledge_base_dir = Path(self.config.get("knowledge_base_dir", str(ARABIC_KNOWLEDGE_BASE_DIR)))
        self._create_directories()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from a JSON file."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default configuration if file doesn't exist
            return {
                "datasets_dir": str(ARABIC_DATASET_DIR),
                "trained_models_dir": str(ARABIC_TRAINED_MODELS_DIR),
                "knowledge_base_dir": str(ARABIC_KNOWLEDGE_BASE_DIR),
                "language_model": "arabic_bert_base_cased",
                "tokenizer": "arabic_bert_base_cased"
            }

    def _save_config(self):
        """Saves current configuration to a JSON file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def _create_directories(self):
        """Ensures necessary directories for NLP operations exist."""
        self.datasets_dir.mkdir(parents=True, exist_ok=True)
        self.trained_models_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)

    def preprocess_text(self, text: str) -> str:
        """
        Performs basic preprocessing on Arabic text.
        This can include:
        - Removing diacritics (tashkeel).
        - Normalizing characters (e.g., alef variants).
        - Removing punctuation and non-Arabic characters.
        - Lowercasing (though less common for Arabic).
        """
        # Placeholder for actual Arabic text cleaning logic.
        # In a real implementation, this would involve libraries like `pyarabic` or custom regex.
        print(f"Preprocessing Arabic text: '{text[:50]}...'")
        processed_text = text.lower() # Example: simple lowercasing
        # Add more sophisticated cleaning steps here
        return processed_text

    def tokenize_arabic(self, text: str) -> list[str]:
        """
        Tokenizes Arabic text into words or sub-words.
        This would typically use a pre-trained Arabic tokenizer.
        """
        # Placeholder for actual tokenization logic.
        print(f"Tokenizing Arabic text: '{text[:50]}...'")
        tokens = text.split() # Example: simple whitespace tokenization
        # Replace with a proper Arabic tokenizer (e.g., from Hugging Face transformers)
        return tokens

    def detect_language(self, text: str) -> str:
        """
        Detects if the input text is Arabic.
        Returns 'arabic' or 'unknown'.
        """
        # Placeholder for actual language detection.
        # Libraries like `langdetect` or `fasttext` can be used.
        print(f"Detecting language for text: '{text[:50]}...'")
        if any('\u0600' <= char <= '\u06FF' for char in text):
            return "arabic"
        return "unknown"

    def generate_arabic_text(self, prompt: str, max_length: int = 50) -> str:
        """
        Generates Arabic text based on a given prompt using a trained language model.
        """
        # Placeholder for actual text generation logic.
        # This would involve loading a pre-trained Arabic language model and using it.
        print(f"Generating Arabic text for prompt: '{prompt[:50]}...'")
        # Example: simple repetition for demonstration
        generated_text = f"Generated Arabic response to: '{prompt}'"
        return generated_text

    def build_knowledge_base_entry(self, data: Dict[str, Any]) -> None:
        """
        Adds or updates an entry in the Arabic knowledge base.
        The structure of 'data' would depend on the specific knowledge base implementation.
        """
        entry_id = data.get("id")
        if not entry_id:
            print("Error: 'id' is required for knowledge base entries.")
            return

        entry_path = self.knowledge_base_dir / f"{entry_id}.json"
        try:
            with open(entry_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Knowledge base entry '{entry_id}' saved to {entry_path}")
        except Exception as e:
            print(f"Error saving knowledge base entry '{entry_id}': {e}")

    def cleanup_project(self):
        """
        Cleans up any temporary files or directories created by this module.
        """
        print("Cleaning up ArabicNLPProcessor resources...")
        # In a real scenario, this might involve removing trained models, cached data, etc.
        if self.knowledge_base_dir.exists():
            print(f"Removing knowledge base directory: {self.knowledge_base_dir}")
            shutil.rmtree(self.knowledge_base_dir)
        if self.datasets_dir.exists():
            print(f"Removing datasets directory: {self.datasets_dir}")
            shutil.rmtree(self.datasets_dir)
        if self.trained_models_dir.exists():
            print(f"Removing trained models directory: {self.trained_models_dir}")
            shutil.rmtree(self.trained_models_dir)
        if self.config_path.exists():
            print(f"Removing config file: {self.config_path}")
            self.config_path.unlink()

# Example Usage (demonstrates functionality without full NLP model implementation)
if __name__ == "__main__":
    print("--- Demonstrating ArabicNLPProcessor Module ---")

    # Initialize the processor
    arabic_nlp_processor = ArabicNLPProcessor()

    # --- Text Processing and Generation ---
    arabic_text_sample = "هذه جملة تجريبية باللغة العربية."
    print(f"\nOriginal Arabic text: {arabic_text_sample}")

    # Language Detection
    lang = arabic_nlp_processor.detect_language(arabic_text_sample)
    print(f"Detected language: {lang}")

    # Preprocessing
    processed_text = arabic_nlp_processor.preprocess_text(arabic_text_sample)
    print(f"Processed text: {processed_text}")

    # Tokenization
    tokens = arabic_nlp_processor.tokenize_arabic(processed_text)
    print(f"Tokens: {tokens}")

    # Text Generation
    generation_prompt = "اكتب لي قصة قصيرة عن الصحراء."
    generated_arabic = arabic_nlp_processor.generate_arabic_text(generation_prompt)
    print(f"Generated Arabic text: {generated_arabic}")

    # --- Knowledge Base Integration ---
    sample_kb_entry = {
        "id": "greeting_response_ar",
        "type": "response_template",
        "language": "ar",
        "content": {
            "default": "مرحباً بك!",
            "formal": "أهلاً وسهلاً بحضرتكم."
        },
        "tags": ["greeting", "welcome"]
    }
    arabic_nlp_processor.build_knowledge_base_entry(sample_kb_entry)

    # Demonstrate cleanup
    print("\n--- Running cleanup ---")
    arabic_nlp_processor.cleanup_project()
    print("--- ArabicNLPProcessor Module Demo Finished ---")