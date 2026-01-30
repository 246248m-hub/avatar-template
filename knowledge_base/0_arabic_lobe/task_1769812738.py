import os
import shutil
import json
import re

class ArabicNLPProcessor:
    """
    Processes Arabic text for natural language understanding and generation,
    aiming to contribute to APK generation from natural language prompts.
    """

    def __init__(self, knowledge_base_dir="knowledge_base"):
        """
        Initializes the ArabicNLPProcessor.

        Args:
            knowledge_base_dir (str): Directory to store and load knowledge.
        """
        self.knowledge_base_dir = knowledge_base_dir
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        self.language_models = {}  # Placeholder for potential language models

    def _load_knowledge(self, filename):
        """
        Loads knowledge from a JSON file.

        Args:
            filename (str): The name of the JSON file.

        Returns:
            dict: The loaded knowledge, or an empty dict if the file doesn't exist.
        """
        filepath = os.path.join(self.knowledge_base_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_knowledge(self, filename, data):
        """
        Saves knowledge to a JSON file.

        Args:
            filename (str): The name of the JSON file.
            data (dict): The data to save.
        """
        filepath = os.path.join(self.knowledge_base_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def analyze_arabic_text(self, text):
        """
        Analyzes Arabic text to extract meaning, intent, and entities.
        This is a simplified example. In a real scenario, this would involve
        advanced NLP techniques like POS tagging, NER, dependency parsing, etc.

        Args:
            text (str): The Arabic text to analyze.

        Returns:
            dict: A dictionary containing analysis results (e.g., intent, entities).
        """
        analysis_results = {"original_text": text, "intent": None, "entities": []}

        # Simplified intent detection based on keywords
        if re.search(r"إنشاء تطبيق|صنع برنامج|بناء تطبيق", text):
            analysis_results["intent"] = "create_app"
        elif re.search(r"تحديث بيانات|تعديل معلومات", text):
            analysis_results["intent"] = "update_data"
        elif re.search(r"عرض قائمة|إظهار تفاصيل", text):
            analysis_results["intent"] = "display_list"

        # Simplified entity extraction (e.g., app names, feature names)
        app_name_match = re.search(r"تطبيق اسمه (.+?)(?: و|،|$)", text)
        if app_name_match:
            analysis_results["entities"].append({"type": "app_name", "value": app_name_match.group(1).strip()})

        feature_matches = re.findall(r"ميزة (.+?)(?: و|،|$)", text)
        for feature in feature_matches:
            analysis_results["entities"].append({"type": "feature", "value": feature.strip()})

        return analysis_results

    def generate_arabic_response(self, analysis_results):
        """
        Generates a natural language Arabic response based on analysis results.

        Args:
            analysis_results (dict): The results from text analysis.

        Returns:
            str: A generated Arabic response.
        """
        response_parts = []
        original_text = analysis_results.get("original_text", "")
        intent = analysis_results.get("intent")
        entities = analysis_results.get("entities", [])

        if intent == "create_app":
            app_name_entity = next((e for e in entities if e["type"] == "app_name"), None)
            app_name = app_name_entity["value"] if app_name_entity else "التطبيق الجديد"
            response_parts.append(f"بالتأكيد، سأقوم بإنشاء تطبيق اسمه \"{app_name}\".")

            features = [e["value"] for e in entities if e["type"] == "feature"]
            if features:
                response_parts.append(f"سأضيف له الميزات التالية: {', '.join(features)}.")
            else:
                response_parts.append("هل هناك ميزات محددة تود إضافتها؟")

        elif intent == "update_data":
            response_parts.append("فهمت، سأقوم بتحديث البيانات المطلوبة.")
            # More detailed response generation based on specific data entities would go here

        elif intent == "display_list":
            response_parts.append("حسناً، سأعرض لك القائمة المطلوبة.")
            # More detailed response generation based on specific list entities would go here

        else:
            response_parts.append(f"لم أفهم طلبك بشكل كامل بخصوص \"{original_text}\". هل يمكنك التوضيح؟")

        return " ".join(response_parts)

    def extract_apk_requirements(self, text):
        """
        Extracts potential APK requirements from Arabic natural language.
        This function aims to bridge NLP analysis with APK generation needs.

        Args:
            text (str): The Arabic text prompt.

        Returns:
            dict: A dictionary representing structured APK requirements.
        """
        analysis = self.analyze_arabic_text(text)
        requirements = {
            "apk_name": None,
            "features": [],
            "dependencies": [],
            "ui_elements": [],
            "backend_needs": [],
            "language": "Arabic", # Default to Arabic if not specified
            "original_prompt": text
        }

        # Map identified entities to structured requirements
        app_name_entity = next((e for e in analysis["entities"] if e["type"] == "app_name"), None)
        if app_name_entity:
            requirements["apk_name"] = app_name_entity["value"]

        for entity in analysis["entities"]:
            if entity["type"] == "feature":
                requirements["features"].append(entity["value"])
            # Add mappings for other entity types as they are defined

        # Further NLP processing to infer dependencies, UI, backend needs etc.
        # This part requires more sophisticated language understanding.
        if "تسجيل دخول" in text or "حساب مستخدم" in text:
            requirements["features"].append("User Authentication")
            requirements["dependencies"].append("Firebase Authentication") # Example
            requirements["backend_needs"].append("User database")

        if "عرض خريطة" in text or "موقع جغرافي" in text:
            requirements["features"].append("Map Display")
            requirements["dependencies"].append("Google Maps SDK") # Example
            requirements["ui_elements"].append("MapView")

        if "قائمة" in text or "جدول" in text:
            requirements["ui_elements"].append("ListView") # Example

        # If no explicit app name, derive one from prompt or set a default
        if not requirements["apk_name"]:
            # Simple heuristic: take first few words related to app creation
            app_creation_keywords = ["تطبيق", "برنامج"]
            words = text.split()
            for i, word in enumerate(words):
                if word in app_creation_keywords and i + 1 < len(words):
                    requirements["apk_name"] = f"{words[i+1]}App"
                    break
            if not requirements["apk_name"]:
                requirements["apk_name"] = "GeneratedApp"


        return requirements

    def generate_code_skeleton(self, requirements):
        """
        Generates a basic code skeleton for an Android APK based on requirements.
        This is a high-level placeholder for code generation.

        Args:
            requirements (dict): Structured APK requirements.

        Returns:
            str: A string representing the code skeleton (e.g., Java/Kotlin code).
        """
        apk_name = requirements.get("apk_name", "GeneratedApp")
        features = requirements.get("features", [])
        language = requirements.get("language", "Arabic") # Use this for code generation language preference

        # Placeholder for actual code generation logic
        code_skeleton = f"// Basic Android APK skeleton for: {apk_name}\n"
        code_skeleton += f"// Generated based on Arabic prompt analysis.\n"
        code_skeleton += f"// Target Language: {language}\n\n"
        code_skeleton += f"public class {apk_name.replace(' ', '')}Activity extends AppCompatActivity {{\n\n"
        code_skeleton += f"    @Override\n"
        code_skeleton += f"    protected void onCreate(Bundle savedInstanceState) {{\n"
        code_skeleton += f"        super.onCreate(savedInstanceState);\n"
        code_skeleton += f"        setContentView(R.layout.{apk_name.lower().replace(' ', '_')}_activity);\n\n"
        code_skeleton += f"        // Initialize UI elements and features\n"

        for feature in features:
            code_skeleton += f"        // Implement logic for feature: {feature}\n"
            # Example: if "Login" in feature:
            # code_skeleton += f"        setupLoginScreen();\n"

        code_skeleton += f"    }}\n"
        code_skeleton += f"}}\n"

        return code_skeleton

    def generate_arabic_text_from_intent(self, intent_data):
        """
        Generates Arabic text based on structured intent data.
        This is the inverse of analyze_arabic_text.

        Args:
            intent_data (dict): Structured data representing an intent.
                                Example: {"intent": "create_app", "app_name": "My Notes", "features": ["add_notes", "view_notes"]}

        Returns:
            str: Generated Arabic text.
        """
        intent = intent_data.get("intent")
        response_parts = []

        if intent == "create_app":
            app_name = intent_data.get("app_name", "تطبيق جديد")
            features = intent_data.get("features", [])
            response_parts.append(f"أرغب في إنشاء تطبيق اسمه \"{app_name}\"")
            if features:
                feature_str = ", ".join(features)
                response_parts.append(f"مع ميزات مثل: {feature_str}")
            response_parts.append("من فضلك.")

        elif intent == "display_info":
            entity_type = intent_data.get("entity_type", "المعلومات")
            entity_name = intent_data.get("entity_name", "")
            response_parts.append(f"أريد عرض {entity_type}")
            if entity_name:
                response_parts.append(f"لـ \"{entity_name}\"")
            response_parts.append(".")

        else:
            response_parts.append("لا يمكنني توليد طلب بناءً على هذه البيانات.")

        return " ".join(response_parts)


    def cleanup_demo_artifacts(self):
        """
        Cleans up any temporary files or directories created during demonstrations.
        """
        print("\n--- Performing cleanup of ArabicNLPProcessor demo artifacts ---")
        # Example: Remove any temporary analysis files or generated knowledge files
        if os.path.exists(self.knowledge_base_dir):
            try:
                shutil.rmtree(self.knowledge_base_dir)
                print(f"Removed directory: {self.knowledge_base_dir}")
            except OSError as e:
                print(f"Error removing directory {self.knowledge_base_dir}: {e}")
        print("--- ArabicNLPProcessor demo cleanup finished ---")

# Example Usage (for demonstration purposes, would be integrated by other lobes)
if __name__ == "__main__":
    nlp_processor = ArabicNLPProcessor()

    # --- Demonstration of analyze_arabic_text and generate_arabic_response ---
    print("\n--- Demonstrating Arabic Text Analysis and Response Generation ---")
    test_prompt_arabic_1 = "أريد إنشاء تطبيق اسمه 'مدير المهام' مع ميزة إضافة مهام جديدة وتحديد أولوياتها."
    analysis_1 = nlp_processor.analyze_arabic_text(test_prompt_arabic_1)
    print(f"Analysis for prompt 1: {analysis_1}")
    response_1 = nlp_processor.generate_arabic_response(analysis_1)
    print(f"Generated response 1: {response_1}")

    test_prompt_arabic_2 = "صنع برنامج اسمه 'متتبع المصاريف' يتضمن تسجيل المصروفات وعرض التقارير."
    analysis_2 = nlp_processor.analyze_arabic_text(test_prompt_arabic_2)
    print(f"Analysis for prompt 2: {analysis_2}")
    response_2 = nlp_processor.generate_arabic_response(analysis_2)
    print(f"Generated response 2: {response_2}")

    test_prompt_arabic_3 = "ما هي أحدث الأخبار؟"
    analysis_3 = nlp_processor.analyze_arabic_text(test_prompt_arabic_3)
    print(f"Analysis for prompt 3: {analysis_3}")
    response_3 = nlp_processor.generate_arabic_response(analysis_3)
    print(f"Generated response 3: {response_3}")

    # --- Demonstration of extract_apk_requirements and generate_code_skeleton ---
    print("\n--- Demonstrating APK Requirement Extraction and Code Skeleton Generation ---")
    apk_requirements_1 = nlp_processor.extract_apk_requirements(test_prompt_arabic_1)
    print(f"Extracted APK Requirements 1: {json.dumps(apk_requirements_1, indent=2, ensure_ascii=False)}")
    code_skeleton_1 = nlp_processor.generate_code_skeleton(apk_requirements_1)
    print(f"Generated Code Skeleton 1:\n{code_skeleton_1}")

    apk_requirements_2 = nlp_processor.extract_apk_requirements(test_prompt_arabic_2)
    print(f"Extracted APK Requirements 2: {json.dumps(apk_requirements_2, indent=2, ensure_ascii=False)}")
    code_skeleton_2 = nlp_processor.generate_code_skeleton(apk_requirements_2)
    print(f"Generated Code Skeleton 2:\n{code_skeleton_2}")

    # --- Demonstration of generate_arabic_text_from_intent ---
    print("\n--- Demonstrating Arabic Text Generation from Intent ---")
    intent_data_1 = {"intent": "create_app", "app_name": "مفكرة بسيطة", "features": ["إضافة ملاحظات", "حفظ الملاحظات"]}
    generated_text_1 = nlp_processor.generate_arabic_text_from_intent(intent_data_1)
    print(f"Generated Arabic text from intent 1: {generated_text_1}")

    intent_data_2 = {"intent": "display_info", "entity_type": "معلومات المستخدم", "entity_name": "أحمد"}
    generated_text_2 = nlp_processor.generate_arabic_text_from_intent(intent_data_2)
    print(f"Generated Arabic text from intent 2: {generated_text_2}")

    # --- Cleanup ---
    nlp_processor.cleanup_demo_artifacts()