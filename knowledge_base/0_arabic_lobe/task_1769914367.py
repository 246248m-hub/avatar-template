import os
import json
import re

# Assume these are defined in other lobes or globally
# KNOWLEDGE_BASE_DIR = "path/to/knowledge_base"
# ARABIC_VOCABULARY = {...} # Loaded from a file or defined

class ArabicSyntaxAnalyzer:
    """
    Analyzes Arabic text to understand its grammatical structure and identify key components
    for code generation. This is a simplified representation.
    """
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        # In a real scenario, this would involve more complex NLP techniques like:
        # - Part-of-Speech (POS) tagging
        # - Named Entity Recognition (NER) for variables, functions, etc.
        # - Dependency parsing to understand relationships between words
        # - Morphological analysis for root extraction and inflection

    def parse_sentence(self, sentence: str) -> dict:
        """
        Parses an Arabic sentence and extracts structured information.
        Returns a dictionary representing the parsed sentence.
        """
        print(f"Parsing Arabic sentence: '{sentence}'")
        parsed_data = {
            "original_sentence": sentence,
            "tokens": [],
            "entities": [],
            "structure": None,
            "intent": None
        }

        # Simplified tokenization and basic pattern matching
        words = re.findall(r'\b\w+\b', sentence, re.UNICODE)
        parsed_data["tokens"] = words

        # Basic entity recognition (e.g., identifying common programming terms)
        for word in words:
            if word in ["إنشاء", "تطبيق", "وظيفة", "متغير", "قائمة", "زر"]:
                parsed_data["entities"].append({"text": word, "type": "CODE_ELEMENT"})
            elif word in ["اسم", "عنوان", "لون"]:
                parsed_data["entities"].append({"text": word, "type": "ATTRIBUTE"})
            elif word in ["هو", "هي", "يكون"]:
                parsed_data["entities"].append({"text": word, "type": "VERB"})

        # Very basic structure identification (e.g., imperative sentences)
        if words and words[0] in ["أنشئ", "قم بإنشاء", "ابني"]:
            parsed_data["structure"] = "IMPERATIVE_COMMAND"
            parsed_data["intent"] = "CREATE_APP_COMPONENT"

        print(f"Parsed data: {json.dumps(parsed_data, indent=2, ensure_ascii=False)}")
        return parsed_data

    def analyze_code_request(self, natural_language_request: str) -> dict:
        """
        Analyzes a natural language request for creating or modifying APK components.
        """
        print(f"Analyzing Arabic code request: '{natural_language_request}'")
        # In a more advanced system, this would involve a pipeline of NLP tasks.
        # For this example, we'll just call parse_sentence and add more context.

        parsed_request = self.parse_sentence(natural_language_request)

        # Further analysis to determine specific component type, attributes, and actions
        component_type = None
        component_name = None
        attributes = {}

        if parsed_request["intent"] == "CREATE_APP_COMPONENT":
            for entity in parsed_request["entities"]:
                if entity["type"] == "CODE_ELEMENT":
                    component_type = entity["text"]
                elif entity["type"] == "ATTRIBUTE":
                    # This is highly simplified; would need context to map attribute to value
                    pass

            # Attempt to extract component name (e.g., "تطبيق اسمه 'حاسبة'")
            name_match = re.search(r'(?:اسم|تسمية)\s+([\w\s]+?)(?:،|\.|$)', natural_language_request, re.UNICODE)
            if name_match:
                component_name = name_match.group(1).strip()
                # Further cleaning of the name if it includes quotes or other noise
                component_name = re.sub(r'^[\'"]|[\'"]$', '', component_name)


            # Populate component_type with more specific identifiers if possible
            if component_type == "تطبيق":
                component_type = "Application"
            elif component_type == "وظيفة":
                component_type = "Function"
            elif component_type == "متغير":
                component_type = "Variable"
            elif component_type == "قائمة":
                component_type = "List"
            elif component_type == "زر":
                component_type = "Button"
            else:
                component_type = "UnknownComponent" # Default for unhandled types

            analysis_result = {
                "component_type": component_type,
                "component_name": component_name,
                "attributes": attributes,
                "parsed_structure": parsed_request
            }
            print(f"Analysis result: {json.dumps(analysis_result, indent=2, ensure_ascii=False)}")
            return analysis_result
        else:
            print("Request intent not recognized for code generation.")
            return {"error": "Unrecognized intent for code generation."}

# --- Dummy Vocabulary for Demonstration ---
# In a real scenario, this would be loaded and much more comprehensive.
DUMMY_ARABIC_VOCABULARY = {
    "verbs": ["إنشاء", "أنشئ", "قم بإنشاء", "ابني", "يكون", "هو", "هي"],
    "nouns": ["تطبيق", "وظيفة", "متغير", "قائمة", "زر", "اسم", "عنوان", "لون"],
    "prepositions": ["في", "على", "لـ"],
    "conjunctions": ["و", "ثم"],
    "keywords": ["اسم", "عنوان", "لون", "قيمة"]
}

def demo_arabic_syntax_analyzer():
    """
    Demonstrates the ArabicSyntaxAnalyzer module.
    """
    print("\n--- Initiating Lobe 3_arabic_parser_lobe ---")

    # Instantiate the analyzer with the dummy vocabulary
    analyzer = ArabicSyntaxAnalyzer(DUMMY_ARABIC_VOCABULARY)

    # Test cases for natural language requests
    test_requests = [
        "أنشئ تطبيق اسمه 'مرحبا بالعالم'",
        "قم بإنشاء وظيفة لحساب المجموع",
        "أريد متغير اسمه 'العداد' قيمته 0",
        "أنشئ زر مكتوب عليه 'اضغط هنا'",
        "تطبيق جديد بعنوان 'تطبيق الخدمات'"
    ]

    generated_analysis_results = {}
    for i, request in enumerate(test_requests):
        analysis = analyzer.analyze_code_request(request)
        generated_analysis_results[f"request_{i+1}"] = analysis
        print(f"\n--- Analysis for Request {i+1} Finished ---")

    print("\n--- Lobe 3_arabic_parser_lobe Demo Finished ---")
    return generated_analysis_results

if __name__ == "__main__":
    # This block is for local testing of the Lobe 3 module in isolation.
    # It would not be part of the final integrated system execution flow.
    print("Running Lobe 3 demo...")
    analysis_results = demo_arabic_syntax_analyzer()
    print("\n--- Lobe 3 Demo Complete. Returned Analysis Results: ---")
    print(json.dumps(analysis_results, indent=2, ensure_ascii=False))