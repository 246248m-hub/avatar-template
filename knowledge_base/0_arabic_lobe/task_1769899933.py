import os
import re
import shutil
from collections import defaultdict

# Assume necessary imports for other lobes are handled elsewhere or will be added.
# For this module, we'll focus on parsing and generating Arabic logic.

# --- Constants ---
# These would ideally be loaded from configuration or knowledge bases.
ARABIC_GRAMMAR_RULES = {
    "noun": {"singular", "plural", "dual"},
    "verb": {"past", "present", "imperative", "active", "passive"},
    "adjective": {},
    "preposition": {},
    "conjunction": {},
    "pronoun": {},
    "adverb": {},
    "interjection": {}
}

ARABIC_MORPHOLOGICAL_FEATURES = {
    "gender": {"masculine", "feminine"},
    "number": {"singular", "dual", "plural"},
    "person": {"1st", "2nd", "3rd"},
    "tense": {"past", "present"},
    "mood": {"indicative", "subjunctive", "jussive"},
    "voice": {"active", "passive"}
}

# --- Helper Functions ---

def tokenize_arabic(text):
    """Basic Arabic tokenizer using regex to split by words and punctuation."""
    words = re.findall(r'\b\w+\b', text, re.UNICODE)
    return words

def analyze_arabic_word(word):
    """
    Placeholder for a sophisticated Arabic morphological analyzer.
    In a real scenario, this would involve complex linguistic libraries
    or trained models. For demonstration, it returns a simplified structure.
    """
    # This is a highly simplified simulation. Real analysis is far more complex.
    analysis = {
        "lemma": word, # Default to word itself if no analysis
        "part_of_speech": "unknown",
        "features": {}
    }

    # Very basic heuristic-based analysis (demonstration only)
    if word.endswith('ون') and len(word) > 3: # Plural masculine suffix
        analysis["part_of_speech"] = "noun"
        analysis["features"] = {"number": "plural", "gender": "masculine"}
    elif word.endswith('ات') and len(word) > 3: # Plural feminine suffix
        analysis["part_of_speech"] = "noun"
        analysis["features"] = {"number": "plural", "gender": "feminine"}
    elif word.endswith('ة') and len(word) > 2: # Feminine singular suffix
        analysis["part_of_speech"] = "noun"
        analysis["features"] = {"gender": "feminine", "number": "singular"}
    elif word.endswith('ي') and len(word) > 2: # Masculine singular or possessive
        analysis["part_of_speech"] = "noun" # Or adjective/pronoun depending on context
        analysis["features"] = {"gender": "masculine", "number": "singular"}
    elif word.endswith('ت') and len(word) > 2: # Verb suffix (e.g., past tense 2nd person)
        analysis["part_of_speech"] = "verb"
        analysis["features"] = {"tense": "past"}
    elif word.startswith('ي') and len(word) > 2: # Present tense 3rd person masculine
        analysis["part_of_speech"] = "verb"
        analysis["features"] = {"tense": "present", "person": "3rd", "gender": "masculine"}
    elif word.startswith('ت') and len(word) > 2: # Present tense 2nd person or 3rd person feminine
        analysis["part_of_speech"] = "verb"
        analysis["features"] = {"tense": "present"}
    elif word.startswith('أ') and len(word) > 2: # Present tense 1st person singular
        analysis["part_of_speech"] = "verb"
        analysis["features"] = {"tense": "present", "person": "1st", "number": "singular"}
    elif word.startswith('ن') and len(word) > 2: # Present tense 1st person plural
        analysis["part_of_speech"] = "verb"
        analysis["features"] = {"tense": "present", "person": "1st", "number": "plural"}
    elif word in ["في", "على", "إلى", "من", "بـ"]:
        analysis["part_of_speech"] = "preposition"
    elif word in ["و", "فـ", "ثم"]:
        analysis["part_of_speech"] = "conjunction"

    # Default to noun if no other part of speech is strongly indicated
    if analysis["part_of_speech"] == "unknown":
        analysis["part_of_speech"] = "noun"

    return analysis

def generate_arabic_phrase(parsed_structure):
    """
    Generates an Arabic phrase from a structured representation.
    This is a simplified generative process.
    """
    # This is a highly simplified simulation. Real generation is far more complex.
    phrase_parts = []
    for item in parsed_structure:
        if isinstance(item, str):
            phrase_parts.append(item)
        elif isinstance(item, dict):
            word_components = []
            # Prioritize verb generation if it's a verb
            if item.get("part_of_speech") == "verb":
                verb_stem = item.get("lemma", "فعل")
                features = item.get("features", {})
                # Apply suffixes/prefixes based on features (highly simplified)
                if features.get("tense") == "past":
                    if features.get("person") == "1st" and features.get("number") == "singular":
                        word_components.append(f"{verb_stem}تُ")
                    elif features.get("person") == "2nd" and features.get("number") == "singular" and features.get("gender") == "masculine":
                        word_components.append(f"{verb_stem}تَ")
                    elif features.get("person") == "3rd" and features.get("gender") == "masculine":
                        word_components.append(verb_stem)
                    else:
                        word_components.append(f"{verb_stem} فعل") # Generic past
                elif features.get("tense") == "present":
                    if features.get("person") == "1st" and features.get("number") == "singular":
                        word_components.append(f"أ{verb_stem}")
                    elif features.get("person") == "3rd" and features.get("gender") == "masculine":
                        word_components.append(f"ي{verb_stem}")
                    else:
                        word_components.append(f"ت{verb_stem} فعل") # Generic present
                else:
                    word_components.append(verb_stem) # Default verb stem
            elif item.get("part_of_speech") == "noun":
                noun_stem = item.get("lemma", "اسم")
                features = item.get("features", {})
                if features.get("number") == "plural" and features.get("gender") == "masculine":
                    word_components.append(f"{noun_stem}ون")
                elif features.get("number") == "plural" and features.get("gender") == "feminine":
                    word_components.append(f"{noun_stem}ات")
                elif features.get("gender") == "feminine" and features.get("number") == "singular":
                    word_components.append(f"{noun_stem}ة")
                else:
                    word_components.append(noun_stem)
            elif item.get("part_of_speech") == "preposition":
                word_components.append(item.get("lemma", "حرف جر"))
            elif item.get("part_of_speech") == "conjunction":
                word_components.append(item.get("lemma", "حرف عطف"))
            else:
                word_components.append(item.get("lemma", "كلمة")) # Fallback

            phrase_parts.append("".join(word_components))
    return " ".join(phrase_parts)


class ArabicLogicLobe:
    """
    This lobe focuses on parsing natural language Arabic input
    and generating structured representations that can be used
    to construct functional code or logic.
    """
    def __init__(self):
        self.name = "ArabicLogicLobe"
        # In a real system, this would load NLP models, grammar rules, etc.
        print(f"--- {self.name} initialized ---")

    def parse_arabic_to_structure(self, natural_language_arabic):
        """
        Parses Arabic natural language into a structured representation.
        This structure can then be interpreted by other lobes (e.g., code generation).
        """
        print(f"Parsing Arabic: '{natural_language_arabic}'")
        tokens = tokenize_arabic(natural_language_arabic)
        parsed_elements = []
        for token in tokens:
            analysis = analyze_arabic_word(token)
            # For demonstration, we simplify: if it's a verb with specific features,
            # or a noun with specific features, we retain that information.
            # More complex sentences would require syntactic parsing (POS tagging, dependency parsing).
            if analysis["part_of_speech"] in ARABIC_GRAMMAR_RULES:
                parsed_elements.append(analysis)
            else:
                # If it's not a recognized part of speech by our simple analyzer,
                # we treat it as a literal string for now.
                parsed_elements.append(token)
        print(f"Parsed structure: {parsed_elements}")
        return parsed_elements

    def generate_arabic_logic_from_structure(self, structured_data):
        """
        Generates Arabic natural language from a structured representation.
        This can be used to confirm understanding or generate instructions.
        """
        print(f"Generating Arabic logic from structure: {structured_data}")
        if not structured_data:
            return "لا يوجد منطق لتوليده."

        # The `structured_data` here is expected to be a list of dictionaries
        # or strings, similar to what `parse_arabic_to_structure` outputs.
        generated_phrase = generate_arabic_phrase(structured_data)
        print(f"Generated Arabic logic: '{generated_phrase}'")
        return generated_phrase

    def interpret_command_for_apk(self, arabic_command):
        """
        Interprets an Arabic command specifically for APK generation.
        This is where domain-specific logic for APK features would reside.
        """
        print(f"Interpreting Arabic command for APK: '{arabic_command}'")
        parsed_structure = self.parse_arabic_to_structure(arabic_command)

        # --- Domain-specific interpretation for APK generation ---
        apk_intent = {
            "action": None,
            "elements": []
        }

        # Basic interpretation: look for keywords related to app creation or modification.
        if any(word in arabic_command for word in ["إنشاء", "بناء", "تصميم", "إنشئ"]):
            apk_intent["action"] = "create_apk"
        elif any(word in arabic_command for word in ["تعديل", "تغيير", "تحديث"]):
            apk_intent["action"] = "modify_apk"
        elif any(word in arabic_command for word in ["قائمة", "عرض", "عرض كل"]):
            apk_intent["action"] = "list_elements"
        elif any(word in arabic_command for word in ["زر", "شاشة", "حقل", "نص"]):
            # Extract elements described in the command
            for item in parsed_structure:
                if isinstance(item, dict):
                    if item.get("part_of_speech") == "noun":
                        apk_intent["elements"].append({"type": "ui_element", "name": item.get("lemma", "عنصر")})
                    elif item.get("part_of_speech") == "verb":
                        apk_intent["elements"].append({"type": "action", "description": item.get("lemma", "فعل")})
                else:
                    # Treat other tokens as descriptive text if they are nouns or adjectives
                    if item.lower() not in ["و", "في", "على", "لـ", "ال", "من"]: # Ignore common connectors/articles
                         if not any(e.get("name") == item for e in apk_intent["elements"]): # Avoid adding duplicates
                            apk_intent["elements"].append({"type": "description", "value": item})

        # Example: "إنشاء تطبيق بسيط يعرض نص 'مرحباً بالعالم'"
        if "تطبيق بسيط" in arabic_command and "يعرض نص" in arabic_command:
            match = re.search(r"يعرض نص '(.*?)'", arabic_command)
            if match:
                apk_intent["elements"].append({"type": "ui_element", "name": "TextView", "text": match.group(1)})
                if "create_apk" not in [e["type"] for e in apk_intent["elements"]]:
                    apk_intent["action"] = "create_apk"


        # Example: "أضف زر 'موافق' إلى الشاشة"
        if "أضف زر" in arabic_command and "إلى الشاشة" in arabic_command:
            match_button = re.search(r"أضف زر '(.*?)' إلى الشاشة", arabic_command)
            if match_button:
                apk_intent["action"] = "modify_apk"
                apk_intent["elements"].append({"type": "ui_element", "name": "Button", "text": match_button.group(1)})

        # Example: "قم بتعريف متغير باسم 'counter' وقيمته الأولية صفر"
        if "قم بتعريف متغير" in arabic_command:
            match_var = re.search(r"باسم '(.*?)' وقيمته الأولية (.*?)$", arabic_command)
            if match_var:
                apk_intent["action"] = "define_variable"
                apk_intent["elements"].append({"type": "variable", "name": match_var.group(1), "initial_value": match_var.group(2)})

        print(f"Interpreted APK intent: {apk_intent}")
        return apk_intent


    def reconstruct_arabic_from_intent(self, apk_intent):
        """
        Reconstructs an Arabic description from the interpreted intent.
        This is useful for feedback or confirmation.
        """
        print(f"Reconstructing Arabic from intent: {apk_intent}")
        if not apk_intent or not apk_intent.get("action"):
            return "لا يمكن إعادة بناء الوصف."

        description_parts = []
        action = apk_intent.get("action", "عمل")
        elements = apk_intent.get("elements", [])

        if action == "create_apk":
            description_parts.append("إنشاء تطبيق")
        elif action == "modify_apk":
            description_parts.append("تعديل التطبيق")
        elif action == "define_variable":
            description_parts.append("تعريف متغير")

        if elements:
            element_descriptions = []
            for element in elements:
                if element.get("type") == "ui_element":
                    if element.get("name") == "TextView":
                        element_descriptions.append(f"يعرض النص '{element.get('text', 'نص فارغ')}'")
                    elif element.get("name") == "Button":
                        element_descriptions.append(f"زر '{element.get('text', 'زر')}'")
                    else:
                        element_descriptions.append(f"عنصر واجهة مستخدم '{element.get('name', 'مجهول')}'")
                elif element.get("type") == "variable":
                    element_descriptions.append(f"متغير اسمه '{element.get('name', 'مجهول')}' وقيمته '{element.get('initial_value', 'فارغة')}'")
                elif element.get("type") == "description":
                    element_descriptions.append(f"وصف '{element.get('value', '')}'")
                elif element.get("type") == "action":
                    element_descriptions.append(f"فعل '{element.get('description', 'غير محدد')}'")

            if element_descriptions:
                if action in ["create_apk", "modify_apk"]:
                    description_parts.append(" مع " + " و ".join(element_descriptions))
                else:
                    description_parts.append(" يتضمن " + " و ".join(element_descriptions))

        reconstructed_text = "".join(description_parts)
        print(f"Reconstructed Arabic: '{reconstructed_text}'")
        return reconstructed_text

    def execute(self, natural_language_input):
        """
        Main execution method for the ArabicLogicLobe.
        Parses input and can optionally generate structured output or reconstructive text.
        """
        print(f"\n--- Executing {self.name} ---")
        parsed_structure = self.parse_arabic_to_structure(natural_language_input)
        reconstructed_text = self.reconstruct_arabic_from_intent(self.interpret_command_for_apk(natural_language_input))
        print(f"Parsed structure: {parsed_structure}")
        print(f"Reconstructed Arabic from interpreted intent: {reconstructed_text}")

        # The primary output for integration would be the interpreted intent
        return self.interpret_command_for_apk(natural_language_input)

# --- Example Usage ---
if __name__ == "__main__":
    # Instantiate the lobe
    arabic_lobe = ArabicLogicLobe()

    # --- Test Case 1: Simple Parsing ---
    print("\n--- Test Case 1: Basic Arabic Parsing ---")
    arabic_text_1 = "أنا أريد بناء تطبيق يعرض رسالة ترحيب."
    structure_1 = arabic_lobe.parse_arabic_to_structure(arabic_text_1)
    print(f"Input: '{arabic_text_1}'\nOutput Structure: {structure_1}\n")

    # --- Test Case 2: Parsing and Intent Interpretation ---
    print("\n--- Test Case 2: Intent Interpretation for APK ---")
    arabic_command_1 = "إنشاء تطبيق بسيط يعرض نص 'مرحباً بالعالم'"
    intent_1 = arabic_lobe.execute(arabic_command_1)
    print(f"Command: '{arabic_command_1}'\nInterpreted Intent: {intent_1}\n")

    arabic_command_2 = "أضف زر 'حفظ' إلى الشاشة الرئيسية."
    intent_2 = arabic_lobe.execute(arabic_command_2)
    print(f"Command: '{arabic_command_2}'\nInterpreted Intent: {intent_2}\n")

    arabic_command_3 = "قم بتعريف متغير باسم 'user_count' وقيمته الأولية 10"
    intent_3 = arabic_lobe.execute(arabic_command_3)
    print(f"Command: '{arabic_command_3}'\nInterpreted Intent: {intent_3}\n")

    # --- Test Case 3: Reconstructing Arabic from Intent ---
    print("\n--- Test Case 3: Reconstructing Arabic from Intent ---")
    sample_intent_1 = {
        "action": "create_apk",
        "elements": [
            {"type": "ui_element", "name": "TextView", "text": "مرحباً بك!"},
            {"type": "ui_element", "name": "Button", "text": "ابدأ"}
        ]
    }
    reconstructed_1 = arabic_lobe.reconstruct_arabic_from_intent(sample_intent_1)
    print(f"Intent: {sample_intent_1}\nReconstructed: '{reconstructed_1}'\n")

    sample_intent_2 = {
        "action": "define_variable",
        "elements": [
            {"type": "variable", "name": "app_version", "initial_value": "1.0"}
        ]
    }
    reconstructed_2 = arabic_lobe.reconstruct_arabic_from_intent(sample_intent_2)
    print(f"Intent: {sample_intent_2}\nReconstructed: '{reconstructed_2}'\n")

    # --- Test Case 4: Generating Arabic Logic from Structure (less common for this lobe's primary use case, but for completeness) ---
    print("\n--- Test Case 4: Generating Arabic from Structure ---")
    # This is a simplified structure, not directly from the current parsing output
    # but demonstrating the generation capability.
    structure_for_generation = [
        {"lemma": "فعل", "part_of_speech": "verb", "features": {"tense": "past", "person": "3rd", "gender": "masculine"}},
        {"lemma": "بيت", "part_of_speech": "noun", "features": {"gender": "masculine", "number": "singular"}},
        {"lemma": "كبير", "part_of_speech": "adjective"} # Assuming adjective handling
    ]
    generated_phrase = arabic_lobe.generate_arabic_logic_from_structure(structure_for_generation)
    print(f"Input Structure: {structure_for_generation}\nGenerated Arabic: '{generated_phrase}'\n")

    # --- Placeholder for next logical step ---
    print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---")