import os
import json
import re

OUTPUT_DIR = "generated_apks"
KNOWLEDGE_BASE_DIR = "knowledge_base"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

def save_structured_output(data, directory, filename_prefix):
    """Saves structured data to a JSON file."""
    filepath = os.path.join(directory, f"{filename_prefix}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filepath

def load_structured_input(filepath):
    """Loads structured data from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def cleanup_dummy_files():
    """Removes dummy files created during testing."""
    for filename in os.listdir("."):
        if filename.startswith("dummy_"):
            os.remove(filename)
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.startswith("dummy_"):
            os.remove(os.path.join(KNOWLEDGE_BASE_DIR, filename))

def cleanup_android_project_template():
    """Removes the dummy Android project template."""
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        import shutil
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)

class ArabicNLPProcessor:
    def __init__(self, knowledge_base_dir):
        self.knowledge_base_dir = knowledge_base_dir
        self.arabic_stopwords = self._load_stopwords()
        self.arabic_morphological_rules = self._load_morphological_rules()

    def _load_stopwords(self):
        """Loads Arabic stopwords from a file."""
        stopwords_path = os.path.join(self.knowledge_base_dir, "arabic_stopwords.txt")
        if not os.path.exists(stopwords_path):
            # Create a dummy file if it doesn't exist
            with open(stopwords_path, 'w', encoding='utf-8') as f:
                f.write("و\n") # 'and'
                f.write("في\n") # 'in'
                f.write("من\n") # 'from'
                f.write("على\n") # 'on'
                f.write("إلى\n") # 'to'
            print(f"Created dummy stopwords file: {stopwords_path}")
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())

    def _load_morphological_rules(self):
        """Loads simplified Arabic morphological rules."""
        # This is a highly simplified representation. A real system would use a lexicon and complex algorithms.
        # Example: Rules to identify common prefixes and suffixes
        rules = {
            "prefixes": {
                "ال": "definite article", # Al-
                "و": "and", # Wa-
                "ف": "then", # Fa-
                "ب": "with/in", # Bi-
                "ك": "like/as", # Ka-
                "ل": "for", # Li-
                "س": "future prefix", # Sa-
                "سأ": "future prefix", # Sa'a-
                "ي": "present tense prefix (he/she)", # Ya-
                "ت": "present tense prefix (she/you)", # Ta-
                "أ": "present tense prefix (I)", # 'A-
                "ن": "present tense prefix (we)", # Na-
            },
            "suffixes": {
                "ون": "plural masculine suffix", # -oon
                "ين": "plural masculine suffix", # -een
                "ات": "plural feminine suffix", # -aat
                "هم": "their (masc. plural)", # -hum
                "هن": "their (fem. plural)", # -hunna
                "ه": "his/it", # -hu
                "ها": "her/it", # -ha
                "ي": "my", # -i
                "نا": "our", # -na
            }
        }
        return rules

    def tokenize(self, text):
        """Basic tokenization for Arabic text, splitting by whitespace and punctuation."""
        text = re.sub(r'[^\w\s]', ' ', text) # Remove punctuation except for common Arabic characters
        tokens = text.split()
        return [token for token in tokens if token]

    def remove_stopwords(self, tokens):
        """Removes Arabic stopwords from a list of tokens."""
        return [token for token in tokens if token not in self.arabic_stopwords]

    def lemmatize_simple(self, token):
        """A very basic lemmatization attempt by stripping known prefixes and suffixes."""
        original_token = token
        token = token.lower()

        # Strip prefixes
        for prefix, _ in sorted(self.arabic_morphological_rules["prefixes"].items(), key=lambda item: len(item[0]), reverse=True):
            if token.startswith(prefix):
                token = token[len(prefix):]
                break # Assume only one primary prefix

        # Strip suffixes
        for suffix, _ in sorted(self.arabic_morphological_rules["suffixes"].items(), key=lambda item: len(item[0]), reverse=True):
            if token.endswith(suffix):
                token = token[:-len(suffix)]
                break # Assume only one primary suffix

        # Handle cases where stripping might result in an empty string or single character
        if not token:
            return original_token # Return original if stripping resulted in empty
        if len(token) <= 1 and token not in "ا و ي": # Keep single letters that are not common connectors
            return original_token

        return token

    def process_text(self, text):
        """Processes Arabic text: tokenizes, removes stopwords, and performs simple lemmatization."""
        tokens = self.tokenize(text)
        tokens_no_stopwords = self.remove_stopwords(tokens)
        lemmas = [self.lemmatize_simple(token) for token in tokens_no_stopwords]
        return " ".join(lemmas)

class ArabicAPKStructureGenerator:
    def __init__(self, nlp_processor):
        self.nlp_processor = nlp_processor

    def extract_keywords_and_entities(self, natural_language_prompt):
        """
        Extracts keywords and potential entities from an Arabic prompt using NLP.
        This is a simplified example. A real implementation would involve Named Entity Recognition (NER).
        """
        processed_text = self.nlp_processor.process_text(natural_language_prompt)
        keywords = processed_text.split()

        # Very basic entity extraction: look for capitalized words or patterns
        # This is extremely rudimentary and language-dependent.
        # For Arabic, we might look for common patterns like app names or feature names if they are clear.
        potential_entities = []
        # Example: If the prompt mentions "آلة حاسبة بسيطة", we might want to identify "آلة حاسبة"
        # For simplicity, let's assume keywords are the primary entities for now.

        # A more sophisticated approach would involve a pre-trained NER model for Arabic.
        # For this example, we'll consider key nouns as potential entities.
        # This requires a part-of-speech tagger which is not included here.
        # For now, we'll just return the processed keywords as a basis for entity identification.
        return keywords, keywords # Returning keywords as both keywords and potential entities for now

    def map_to_apk_components(self, keywords, entities):
        """
        Maps extracted keywords and entities to potential APK components.
        This function is highly abstract and would require extensive domain knowledge
        and potentially machine learning models for robust mapping.
        """
        component_mapping = {
            "app_name": "MyApp",
            "ui_elements": [],
            "functionality": [],
            "permissions": []
        }

        # Example mapping logic (highly simplified)
        app_name_keywords = ["تطبيق", "برنامج", "لعبة"]
        calculator_keywords = ["حاسبة", "حساب", "عمليات حسابية"]
        text_editor_keywords = ["محرر", "نص", "كتابة"]
        camera_keywords = ["كاميرا", "صورة", "التقاط"]
        location_keywords = ["موقع", "خريطة", "مكان"]
        internet_keywords = ["إنترنت", "شبكة", "اتصال"]

        all_keywords_str = " ".join(keywords)

        # Determine App Name
        if any(kw in all_keywords_str for kw in ["تطبيق", "برنامج"]):
            potential_name_parts = [word for word in keywords if word not in app_name_keywords and len(word) > 2]
            if potential_name_parts:
                component_mapping["app_name"] = "".join(potential_name_parts).capitalize() + "App"
            else:
                component_mapping["app_name"] = "MyGenericApp"
        else:
            component_mapping["app_name"] = "MyGenericApp"


        # Map Functionality
        if any(kw in all_keywords_str for kw in calculator_keywords):
            component_mapping["functionality"].append("calculator")
        if any(kw in all_keywords_str for kw in text_editor_keywords):
            component_mapping["functionality"].append("text_editor")
        if any(kw in all_keywords_str for kw in camera_keywords):
            component_mapping["functionality"].append("camera")
            component_mapping["permissions"].append("android.permission.CAMERA")
        if any(kw in all_keywords_str for kw in location_keywords):
            component_mapping["functionality"].append("location")
            component_mapping["permissions"].append("android.permission.ACCESS_FINE_LOCATION")
            component_mapping["permissions"].append("android.permission.ACCESS_COARSE_LOCATION")
        if any(kw in all_keywords_str for kw in internet_keywords):
            component_mapping["functionality"].append("internet")
            component_mapping["permissions"].append("android.permission.INTERNET")

        # Map UI Elements (very basic based on functionality)
        if "calculator" in component_mapping["functionality"]:
            component_mapping["ui_elements"].extend(["numeric_buttons", "operator_buttons", "display_field", "clear_button"])
        if "text_editor" in component_mapping["functionality"]:
            component_mapping["ui_elements"].extend(["editable_text_area", "save_button"])
        if "camera" in component_mapping["functionality"]:
            component_mapping["ui_elements"].extend(["preview_surface", "capture_button"])
        if "location" in component_mapping["functionality"]:
            component_mapping["ui_elements"].extend(["map_view", "current_location_marker"])

        # Ensure unique permissions and UI elements
        component_mapping["permissions"] = list(set(component_mapping["permissions"]))
        component_mapping["ui_elements"] = list(set(component_mapping["ui_elements"]))

        return component_mapping

    def generate_apk_structure(self, natural_language_prompt):
        """
        Generates a structured representation of an APK from a natural language prompt in Arabic.
        """
        keywords, entities = self.extract_keywords_and_entities(natural_language_prompt)
        apk_structure = self.map_to_apk_components(keywords, entities)

        # Add basic manifest structure if permissions are present
        if apk_structure.get("permissions"):
            apk_structure["manifest"] = {
                "uses-permission": apk_structure["permissions"]
            }
        else:
             apk_structure["manifest"] = {}

        # Add basic activity structure
        apk_structure["activities"] = [
            {
                "name": f"{apk_structure['app_name'].replace('App', '')}Activity",
                "layout": f"activity_{apk_structure['app_name'].lower().replace('app', '')}.xml",
                "ui_elements": apk_structure.get("ui_elements", [])
            }
        ]

        return apk_structure

class LanguageIntegrationLobe:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def save_structured_output(self, structured_data, filename_prefix):
        """Saves structured APK data to a JSON file in the output directory."""
        filepath = os.path.join(self.output_dir, f"{filename_prefix}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=4, ensure_ascii=False)
        return filepath

class ApkCompilerLobe:
    def __init__(self, output_dir, android_project_template_dir):
        self.output_dir = output_dir
        self.android_project_template_dir = android_project_template_dir

    def run(self, app_name):
        """
        Simulates the APK compilation process.
        In a real scenario, this would involve creating a project from a template,
        populating it with generated code based on the APK structure, and then
        compiling it using Android SDK tools.
        """
        print(f"Simulating APK compilation for: {app_name}")

        # 1. Create a dummy project directory if it doesn't exist
        project_path = os.path.join(self.output_dir, app_name.replace(".apk", "_project"))
        os.makedirs(project_path, exist_ok=True)
        print(f"Created dummy project directory: {project_path}")

        # 2. Simulate populating the project with generated code (e.g., Java/Kotlin files, XML layouts)
        # This would be based on the 'apk_structure' generated by the synthesis lobe.
        print("Simulating generation of source code and resources...")
        # Example: Create dummy main activity and layout file
        main_activity_path = os.path.join(project_path, "MainActivity.java")
        with open(main_activity_path, "w", encoding="utf-8") as f:
            f.write("""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Example import

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Example layout

        // Example: Dynamically add a TextView based on synthesized structure
        TextView welcomeText = findViewById(R.id.welcome_text_view); // Assumes this ID exists in layout
        if (welcomeText != null) {
            welcomeText.setText("Welcome to your generated app!");
        }
    }
}
            """)
        print(f"Created dummy MainActivity: {main_activity_path}")

        layout_path = os.path.join(project_path, "activity_main.xml")
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write("""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
            """)
        print(f"Created dummy layout file: {layout_path}")


        # 3. Simulate the build process (e.g., running Gradle commands)
        print("Simulating build commands (e.g., gradle assembleDebug)...")
        # In a real system, you would execute external commands here.

        # 4. Simulate the final APK file creation
        generated_apk_path = os.path.join(self.output_dir, app_name)
        # Create a dummy file to represent the APK
        with open(generated_apk_path, "w") as f:
            f.write("This is a simulated APK file.")
        print(f"Simulated APK created at: {generated_apk_path}")

        return generated_apk_path

# Example Usage (for demonstration purposes within this module)
if __name__ == "__main__":
    print("--- Initializing Arabic NLP Processor ---")
    arabic_nlp = ArabicNLPProcessor(KNOWLEDGE_BASE_DIR)

    print("\n--- Initializing APK Structure Generator ---")
    apk_generator = ArabicAPKStructureGenerator(arabic_nlp)

    print("\n--- Initializing Language Integration Lobe ---")
    lang_integration = LanguageIntegrationLobe(OUTPUT_DIR)

    print("\n--- Initializing APK Compiler Lobe ---")
    apk_compiler = ApkCompilerLobe(OUTPUT_DIR, ANDROID_PROJECT_TEMPLATE_DIR)


    # --- Demonstrating the flow ---
    arabic_prompt_1 = "أريد تطبيق آلة حاسبة بسيط مع أزرار للأرقام والعمليات الأساسية."
    print(f"\nProcessing Arabic prompt 1: '{arabic_prompt_1}'")

    # Step 1: Generate APK Structure
    structured_apk_data_1 = apk_generator.generate_apk_structure(arabic_prompt_1)
    print("Generated APK Structure:")
    print(json.dumps(structured_apk_data_1, indent=2, ensure_ascii=False))

    # Step 2: Save the structured APK data
    saved_apk_structure_path_1 = lang_integration.save_structured_output(structured_apk_data_1, "calculator_app_structure")
    print(f"Saved APK structure to: {saved_apk_structure_path_1}")

    # Step 3: Compile the APK (simulated)
    # Use the app name from the generated structure for the APK file name
    app_name_from_structure = structured_apk_data_1.get("app_name", "SimulatedApp")
    generated_apk_path_1 = apk_compiler.run(f"{app_name_from_structure.replace('App', '').lower()}_app.apk")
    print(f"Simulated APK generation process finished. Output: {generated_apk_path_1}")

    print("\n--- Arabic NLP and APK Generation Module Demo Finished ---")

    # Clean up dummy files
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()
    cleanup_android_project_template()