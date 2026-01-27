import os
import shutil
import re
from typing import List, Dict, Any

# Assume these directories are defined elsewhere or will be defined
# For demonstration, let's define them here.
KNOWLEDGE_BASE_DIR = "knowledge_base"
JAVA_PROJECT_DIR = "generated_java_project"
ARABIC_PARSED_DIR = "arabic_parsed_output"
SMALI_DIR = "smali_output"
APK_OUTPUT_DIR = "apk_output"


class ArabicSyntaxChecker:
    """
    A module to perform basic syntax checking on parsed Arabic text.
    This is a placeholder for more sophisticated grammatical and semantic analysis.
    """

    def __init__(self):
        # Simple patterns for demonstration. In a real scenario, these would be much more complex.
        self.verb_patterns = [r'\b(يقرأ|يكتب|يذهب|يأكل|يشرب)\b', r'\b(قرأ|كتب|ذهب|أكل|شرب)\b']
        self.noun_patterns = [r'\b(كتاب|قلم|بيت|طعام|ماء)\b', r'\b(الولد|البنت|الرجل|المرأة)\b']
        self.pronoun_patterns = [r'\b(هو|هي|هم|هن|أنا|أنت)\b']
        self.preposition_patterns = [r'\b(في|على|من|إلى|بـ)\b']

    def check_syntax(self, text: str) -> bool:
        """
        Performs a very basic syntax check on the Arabic text.
        Returns True if the text seems syntactically plausible, False otherwise.
        This is a simplified example.
        """
        # A very naive check: looks for at least one verb and one noun.
        has_verb = any(re.search(pattern, text, re.IGNORECASE) for pattern in self.verb_patterns)
        has_noun = any(re.search(pattern, text, re.IGNORECASE) for pattern in self.noun_patterns)
        has_pronoun = any(re.search(pattern, text, re.IGNORECASE) for pattern in self.pronoun_patterns)
        has_preposition = any(re.search(pattern, text, re.IGNORECASE) for pattern in self.preposition_patterns)

        # For this demo, we'll consider it "syntactically valid" if it has at least a verb and a noun.
        # In a real system, this would involve parsing and understanding sentence structure.
        return has_verb and has_noun

    def analyze_sentence_structure(self, sentence: str) -> Dict[str, List[str]]:
        """
        Attempts to identify basic parts of speech in a sentence.
        This is a highly simplified demonstration.
        """
        parts_of_speech = {
            "verbs": [],
            "nouns": [],
            "pronouns": [],
            "prepositions": [],
            "others": []
        }

        words = re.findall(r'\b\w+\b', sentence, re.IGNORECASE)

        for word in words:
            found = False
            if any(re.fullmatch(pattern, word, re.IGNORECASE) for pattern in self.verb_patterns):
                parts_of_speech["verbs"].append(word)
                found = True
            elif any(re.fullmatch(pattern, word, re.IGNORECASE) for pattern in self.noun_patterns):
                parts_of_speech["nouns"].append(word)
                found = True
            elif any(re.fullmatch(pattern, word, re.IGNORECASE) for pattern in self.pronoun_patterns):
                parts_of_speech["pronouns"].append(word)
                found = True
            elif any(re.fullmatch(pattern, word, re.IGNORECASE) for pattern in self.preposition_patterns):
                parts_of_speech["prepositions"].append(word)
                found = True

            if not found:
                parts_of_speech["others"].append(word)

        return parts_of_speech


class ArabicNLPProcessor:
    """
    This module is responsible for processing Arabic text,
    including parsing, understanding structure, and preparing it
    for code generation.
    """

    def __init__(self, knowledge_base_dir: str):
        self.knowledge_base_dir = knowledge_base_dir
        self.syntax_checker = ArabicSyntaxChecker()
        if not os.path.exists(self.knowledge_base_dir):
            os.makedirs(self.knowledge_base_dir)
        if not os.path.exists(ARABIC_PARSED_DIR):
            os.makedirs(ARABIC_PARSED_DIR)

    def parse_arabic_text(self, text: str) -> Dict[str, Any]:
        """
        Parses the Arabic text, performs basic syntax checks,
        and extracts structural information.
        Returns a dictionary containing parsed data.
        """
        parsed_data = {
            "original_text": text,
            "is_syntactically_valid": self.syntax_checker.check_syntax(text),
            "sentence_structure": {},
            "potential_actions": [] # Placeholder for identifying actions
        }

        if parsed_data["is_syntactically_valid"]:
            # Split into sentences for more granular analysis (basic split by .)
            sentences = text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    parsed_data["sentence_structure"][sentence] = self.syntax_checker.analyze_sentence_structure(sentence)
                    # Placeholder: Identify potential actions from verbs
                    if parsed_data["sentence_structure"][sentence]["verbs"]:
                        parsed_data["potential_actions"].extend(parsed_data["sentence_structure"][sentence]["verbs"])

        # Save the parsed data
        filename = os.path.join(ARABIC_PARSED_DIR, f"parsed_{hash(text)}.json")
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        print(f"Saved parsed data to {filename}")

        return parsed_data

    def extract_ui_elements(self, parsed_data: Dict[str, Any]) -> List[str]:
        """
        Extracts potential UI element descriptions from the parsed Arabic text.
        This is a simplified extraction based on common Arabic words associated with UI.
        """
        ui_keywords = [
            "زر", "button", "شاشة", "screen", "نص", "text", "صورة", "image",
            "حقل", "field", "قائمة", "list", "مربع", "box", "إدخال", "input"
        ]
        extracted_elements = []
        for sentence, structure in parsed_data.get("sentence_structure", {}).items():
            words = re.findall(r'\b\w+\b', sentence, re.IGNORECASE)
            for word in words:
                if word.lower() in ui_keywords:
                    extracted_elements.append(word)
        # Also look for explicit mentions in the original text
        for keyword in ui_keywords:
            if keyword in parsed_data["original_text"]:
                extracted_elements.append(keyword)

        # Remove duplicates and return
        return list(set(extracted_elements))

    def extract_functionality_requests(self, parsed_data: Dict[str, Any]) -> List[str]:
        """
        Extracts descriptions of desired functionality from the parsed Arabic text.
        This is a simplified extraction based on verbs and context.
        """
        # Currently, this uses the 'potential_actions' identified during parsing.
        # A more advanced version would use more specific keywords and contextual analysis.
        return parsed_data.get("potential_actions", [])

    def get_contextual_information(self, text: str) -> Dict[str, Any]:
        """
        Retrieves relevant context or knowledge from the knowledge base
        based on the input text.
        This is a placeholder for a real knowledge retrieval system.
        """
        context_info = {}
        # Example: Look for files in the knowledge base that might match keywords in the text
        keywords = re.findall(r'\b\w+\b', text.lower())
        for filename in os.listdir(self.knowledge_base_dir):
            if filename.endswith(".txt"): # Assuming knowledge base files are text
                with open(os.path.join(self.knowledge_base_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if any(keyword in content for keyword in keywords):
                        context_info[filename] = content[:100] + "..." # Snippet of content
                        break # Just take the first match for simplicity
        return context_info

    def finalize_processing(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs any final processing or structuring of the parsed data
        before it's passed to the next module.
        """
        # For now, just return the parsed data as is.
        return parsed_data


def demonstrate_arabic_nlp_processor(prompt: str):
    """
    Demonstrates the ArabicNLPProcessor module.
    """
    print(f"\n--- Demonstrating Arabic NLP Processor with prompt: '{prompt}' ---")
    nlp_processor = ArabicNLPProcessor(KNOWLEDGE_BASE_DIR)

    # 1. Parse the Arabic text
    parsed_result = nlp_processor.parse_arabic_text(prompt)
    print("\nParsed Data:")
    import json
    print(json.dumps(parsed_result, indent=4, ensure_ascii=False))

    # 2. Extract UI Elements
    ui_elements = nlp_processor.extract_ui_elements(parsed_result)
    print(f"\nExtracted UI Elements: {ui_elements}")

    # 3. Extract Functionality Requests
    functionality_requests = nlp_processor.extract_functionality_requests(parsed_result)
    print(f"\nExtracted Functionality Requests: {functionality_requests}")

    # 4. Get Contextual Information (using the original prompt for now)
    context = nlp_processor.get_contextual_information(prompt)
    print(f"\nContextual Information: {context}")

    # 5. Finalize Processing
    final_processed_data = nlp_processor.finalize_processing(parsed_result)
    print("\nFinal Processed Data (same as parsed for this demo):")
    print(json.dumps(final_processed_data, indent=4, ensure_ascii=False))

    print("\n--- Arabic NLP Processor Demo Finished ---")


if __name__ == "__main__":
    # Create dummy knowledge base file for demonstration
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "button_info.txt"), "w", encoding="utf-8") as f:
        f.write("هذه معلومات حول الأزرار في واجهات المستخدم. الزر هو عنصر تفاعلي.")

    # Example Arabic prompts
    test_prompt_arabic_1 = "أنشئ شاشة تحتوي على زر مكتوب عليه 'تسجيل الدخول' وحقل نصي لإدخال اسم المستخدم."
    test_prompt_arabic_2 = "أريد برنامج يقرأ رسالة نصية ويعرضها على الشاشة."
    test_prompt_arabic_3 = "عرض صورة باسم 'logo.png' في أعلى الشاشة."
    test_prompt_arabic_4 = "هذا نص عربي غير مكتمل."

    demonstrate_arabic_nlp_processor(test_prompt_arabic_1)
    demonstrate_arabic_nlp_processor(test_prompt_arabic_2)
    demonstrate_arabic_nlp_processor(test_prompt_arabic_3)
    demonstrate_arabic_nlp_processor(test_prompt_arabic_4)

    # Clean up generated directories
    print("\n--- Cleaning up generated directories ---")
    if os.path.exists(ARABIC_PARSED_DIR):
        shutil.rmtree(ARABIC_PARSED_DIR)
        print(f"Removed directory: {ARABIC_PARSED_DIR}")
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        # shutil.rmtree(KNOWLEDGE_BASE_DIR) # Keep KB for potential future runs
        # print(f"Removed directory: {KNOWLEDGE_BASE_DIR}")
        pass # Don't remove KB for potential future runs
    print("\n--- Arabic NLP Processor Module Demo Finished ---")