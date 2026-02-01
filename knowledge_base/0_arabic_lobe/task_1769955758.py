import os
import shutil
import re

# --- Constants ---
KNOWLEDGE_BASE_DIR = "knowledge_base"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
SIMULATED_APK_OUTPUT_DIR = "simulated_apk_output"
ARABIC_LEXICON_PATH = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_lexicon.txt")
ARABIC_GRAMMAR_RULES_PATH = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_grammar_rules.json")
ANDROID_MANIFEST_TEMPLATE = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "AndroidManifest.xml")
ANDROID_ACTIVITY_TEMPLATE = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "MainActivity.java")

# --- Helper Functions ---

def ensure_directory_exists(dir_path):
    """Ensures a directory exists, creating it if necessary."""
    os.makedirs(dir_path, exist_ok=True)

def create_dummy_knowledge_base():
    """Creates dummy knowledge base files for demonstration."""
    ensure_directory_exists(KNOWLEDGE_BASE_DIR)
    with open(ARABIC_LEXICON_PATH, "w", encoding="utf-8") as f:
        f.write("مرحبا\n")
        f.write("العالم\n")
        f.write("تطبيق\n")
        f.write("شاشة\n")
        f.write("زر\n")
        f.write("نص\n")
        f.write("عرض\n")
        f.write("إلى\n")
        f.write("حساب\n")
        f.write("النتيجة\n")

    with open(ARABIC_GRAMMAR_RULES_PATH, "w", encoding="utf-8") as f:
        f.write("""
{
    "sentence_structure": {
        "intent_display_text": ["عرض نص", "عرض شاشة"],
        "entity_text": ["نص", "شاشة"]
    },
    "commands": {
        "show_text": {"verb": "عرض", "object": "نص"},
        "show_screen": {"verb": "عرض", "object": "شاشة"}
    }
}
""")

def create_android_project_template():
    """Creates a dummy Android project template for demonstration."""
    ensure_directory_exists(ANDROID_PROJECT_TEMPLATE_DIR)
    with open(ANDROID_MANIFEST_TEMPLATE, "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.generatedapp">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")
    with open(ANDROID_ACTIVITY_TEMPLATE, "w") as f:
        f.write("""package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists
        // Default content, will be replaced by generated code
        TextView textView = findViewById(R.id.main_text_view); // Assuming a TextView with id 'main_text_view' exists
        if (textView != null) {
            textView.setText("Welcome to the generated app!");
        }
    }
}
""")

def cleanup_android_project_template():
    """Cleans up the dummy Android project template."""
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
    if os.path.exists(SIMULATED_APK_OUTPUT_DIR):
        shutil.rmtree(SIMULATED_APK_OUTPUT_DIR)

def cleanup_dummy_files():
    """Cleans up dummy knowledge base files."""
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        shutil.rmtree(KNOWLEDGE_BASE_DIR)

# --- Lobe 1_language_processing_lobe ---

class ArabicNLPProcessor:
    def __init__(self, lexicon_path, grammar_rules_path):
        self.lexicon = self._load_lexicon(lexicon_path)
        self.grammar_rules = self._load_grammar_rules(grammar_rules_path)
        self.commands = self.grammar_rules.get("commands", {})

    def _load_lexicon(self, lexicon_path):
        """Loads Arabic words from a file."""
        with open(lexicon_path, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())

    def _load_grammar_rules(self, grammar_rules_path):
        """Loads grammar rules from a JSON file."""
        import json
        with open(grammar_rules_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def tokenize(self, text):
        """Simple tokenization for Arabic text."""
        # Remove punctuation and split by whitespace, preserving Arabic words
        cleaned_text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
        tokens = cleaned_text.split()
        return [token for token in tokens if token in self.lexicon]

    def parse_intent(self, tokens):
        """Parses the intent from a list of tokens based on grammar rules."""
        sentence_structure = self.grammar_rules.get("sentence_structure", {})
        intent_triggers = sentence_structure.get("intent_display_text", [])

        for trigger in intent_triggers:
            trigger_tokens = self.tokenize(trigger)
            if all(token in tokens for token in trigger_tokens):
                # Basic intent matching: find the command that matches the verb and object
                for command_name, command_details in self.commands.items():
                    if command_details.get("verb") in trigger_tokens and command_details.get("object") in trigger_tokens:
                        return command_name, trigger_tokens
        return None, []

    def extract_entities(self, tokens, command_name):
        """Extracts entities based on the identified command."""
        command_details = self.commands.get(command_name)
        if not command_details:
            return {}

        entities = {}
        verb = command_details.get("verb")
        obj = command_details.get("object")

        if verb and verb in tokens:
            entities["verb"] = verb
        if obj and obj in tokens:
            entities["object"] = obj

        # Attempt to extract more specific data if available (e.g., text content)
        if obj == "نص" and "عرض" in tokens:
            try:
                # Find the index of "عرض" and "نص" and extract the text in between
                verb_index = tokens.index(verb)
                object_index = tokens.index(obj)
                if object_index > verb_index:
                    entities["text_content"] = " ".join(tokens[verb_index + 1:object_index])
                else:
                    entities["text_content"] = " ".join(tokens[object_index + 1:])
            except ValueError:
                pass # Handle cases where indices might not be found as expected

        return entities

    def process_arabic_prompt(self, prompt):
        """Processes an Arabic natural language prompt."""
        tokens = self.tokenize(prompt)
        intent_name, intent_tokens = self.parse_intent(tokens)

        if intent_name:
            entities = self.extract_entities(tokens, intent_name)
            return {
                "intent": intent_name,
                "entities": entities,
                "original_tokens": tokens
            }
        else:
            return {"intent": "unknown", "entities": {}, "original_tokens": tokens}

# --- Lobe 4_code_generation_lobe ---

class CodeGenerator:
    def __init__(self, android_manifest_template_path, android_activity_template_path):
        self.android_manifest_template_path = android_manifest_template_path
        self.android_activity_template_path = android_activity_template_path

    def generate_android_activity_code(self, app_name, ui_elements):
        """Generates Java code for an Android Activity based on UI elements."""
        with open(self.android_activity_template_path, "r") as f:
            activity_code = f.read()

        # Modify package name (simplistic for demo)
        activity_code = activity_code.replace("package com.example.generatedapp;", f"package com.example.{app_name.lower()};")

        # Inject UI elements logic (simplified for demonstration)
        ui_injection_code = ""
        layout_creation_code = "setContentView(R.layout.activity_main);\n" # Assuming activity_main.xml

        if "show_text" in ui_elements and ui_elements["show_text"].get("text_content"):
            text_to_display = ui_elements["show_text"]["text_content"]
            # Add TextView declaration and text setting
            ui_injection_code += f"""
        TextView textView = findViewById(R.id.main_text_view); // Assuming a TextView with id 'main_text_view' exists
        if (textView != null) {{
            textView.setText("{text_to_display}");
        }}
"""
            layout_creation_code += "// Added TextView for displaying text.\n"

        if "show_screen" in ui_elements:
            # This could involve inflating different layouts or navigating to other activities
            ui_injection_code += "// Logic for showing a new screen would go here.\n"
            layout_creation_code += "// Potentially loading a different layout for the screen.\n"

        # Find the onCreate method and insert the generated code
        onCreate_start_marker = "protected void onCreate(Bundle savedInstanceState) {"
        onCreate_end_marker = "}" # Simplified end marker

        start_index = activity_code.find(onCreate_start_marker)
        if start_index != -1:
            start_index = activity_code.find("super.onCreate(savedInstanceState);", start_index) + len("super.onCreate(savedInstanceState);")
            # Find the end of the onCreate method body
            brace_count = 0
            end_index = -1
            for i in range(start_index, len(activity_code)):
                if activity_code[i] == '{':
                    brace_count += 1
                elif activity_code[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_index = i
                        break

            if end_index != -1:
                # Insert the layout creation and UI injection code
                activity_code = (activity_code[:end_index] +
                                 "\n        " + layout_creation_code.strip() +
                                 ui_injection_code +
                                 "\n" + activity_code[end_index:])

        return activity_code

    def generate_android_manifest(self, app_name, main_activity_name="MainActivity"):
        """Generates an AndroidManifest.xml file."""
        with open(self.android_manifest_template_path, "r") as f:
            manifest_code = f.read()

        # Update package name
        manifest_code = manifest_code.replace("package=\"com.example.generatedapp\"", f"package=\"com.example.{app_name.lower()}\"")
        # Update activity name if it's different
        manifest_code = manifest_code.replace('android:name=".MainActivity"', f'android:name=".{main_activity_name}"')

        return manifest_code

    def create_project_structure(self, app_name, manifest_content, activity_content):
        """Creates a dummy project structure with manifest and activity files."""
        project_root = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, app_name.replace(" ", "_").lower())
        ensure_directory_exists(project_root)

        # Create src/main/java/com/example/<app_name> directory
        java_dir = os.path.join(project_root, "app", "src", "main", "java", "com", "example", app_name.lower())
        ensure_directory_exists(java_dir)

        # Write AndroidManifest.xml
        manifest_path = os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml")
        with open(manifest_path, "w") as f:
            f.write(manifest_content)

        # Write MainActivity.java
        activity_path = os.path.join(java_dir, "MainActivity.java")
        with open(activity_path, "w") as f:
            f.write(activity_content)

        return project_root


# --- Lobe 8_apk_compiler_lobe ---

class ApkCompiler:
    def __init__(self, output_dir=SIMULATED_APK_OUTPUT_DIR):
        self.output_dir = output_dir
        ensure_directory_exists(self.output_dir)

    def run(self, app_name="generated_app.apk"):
        """Simulates the APK compilation process."""
        print(f"--- Simulating APK compilation for: {app_name} ---")
        # In a real scenario, this would involve using Android SDK tools (aapt, dx, apksigner, etc.)
        # For this demo, we'll just create a dummy file.
        simulated_apk_path = os.path.join(self.output_dir, app_name)
        with open(simulated_apk_path, "w") as f:
            f.write(f"This is a simulated APK file for {app_name}.\n")
            f.write("Generated by the unified mind.\n")
        print(f"Simulated APK created at: {simulated_apk_path}")
        return simulated_apk_path

# --- Main Execution Flow (Conceptual) ---

def main_workflow(natural_language_prompt):
    """Orchestrates the process from NLP to APK generation."""

    # --- Setup ---
    create_dummy_knowledge_base()
    create_android_project_template()

    # --- Lobe 1: Language Processing ---
    print("\n--- Initiating Lobe 1: Arabic NLP Processing ---")
    nlp_processor = ArabicNLPProcessor(ARABIC_LEXICON_PATH, ARABIC_GRAMMAR_RULES_PATH)
    parsed_output = nlp_processor.process_arabic_prompt(natural_language_prompt)
    print(f"Parsed Arabic Prompt: {parsed_output}")

    if parsed_output["intent"] == "unknown":
        print("Could not understand the prompt. Please try a different phrasing.")
        return

    # --- Lobe 4: Code Generation ---
    print("\n--- Initiating Lobe 4: Code Generation ---")
    code_generator = CodeGenerator(ANDROID_MANIFEST_TEMPLATE, ANDROID_ACTIVITY_TEMPLATE)

    # Determine app name from prompt (simplistic)
    app_name_parts = []
    if "تطبيق" in parsed_output["original_tokens"]:
        app_name_parts.extend([token for token in parsed_output["original_tokens"] if token not in ["عرض", "إلى"]])
    app_name = "_".join(app_name_parts) if app_name_parts else "MyGeneratedApp"
    app_name = app_name.capitalize() # Ensure proper casing

    # Generate Manifest and Activity Code
    generated_manifest = code_generator.generate_android_manifest(app_name)
    generated_activity = code_generator.generate_android_activity_code(app_name, {parsed_output["intent"]: parsed_output["entities"]})

    print("--- Generated AndroidManifest.xml (snippet) ---")
    print(generated_manifest[:500] + "...") # Print a snippet

    print("\n--- Generated MainActivity.java (snippet) ---")
    print(generated_activity[:500] + "...") # Print a snippet

    # Create dummy project structure
    project_dir = code_generator.create_project_structure(app_name, generated_manifest, generated_activity)
    print(f"Dummy Android project structure created at: {project_dir}")


    # --- Lobe 8: APK Compilation ---
    print("\n--- Initiating Lobe 8: APK Compilation ---")
    apk_compiler = ApkCompiler()
    simulated_apk_path = apk_compiler.run(app_name=f"{app_name.lower().replace(' ', '_')}.apk")
    print(f"Simulated APK path: {simulated_apk_path}")

    # --- Cleanup ---
    print("\n--- Initiating Cleanup ---")
    cleanup_dummy_files()
    cleanup_android_project_template()
    print("Cleanup complete.")

    return simulated_apk_path

if __name__ == "__main__":
    # Example Usage:
    arabic_prompt_1 = "عرض نص مرحبا بالعالم"
    print(f"Processing prompt: '{arabic_prompt_1}'")
    generated_apk_1 = main_workflow(arabic_prompt_1)
    print(f"\n--- Workflow for prompt 1 finished. APK: {generated_apk_1} ---")

    arabic_prompt_2 = "عرض شاشة رئيسية"
    print(f"\n\nProcessing prompt: '{arabic_prompt_2}'")
    generated_apk_2 = main_workflow(arabic_prompt_2)
    print(f"\n--- Workflow for prompt 2 finished. APK: {generated_apk_2} ---")

    arabic_prompt_3 = "عرض تطبيق جديد" # This prompt might be less well-defined by current rules
    print(f"\n\nProcessing prompt: '{arabic_prompt_3}'")
    generated_apk_3 = main_workflow(arabic_prompt_3)
    print(f"\n--- Workflow for prompt 3 finished. APK: {generated_apk_3} ---")

    arabic_prompt_4 = "لا أفهم هذا" # Unknown intent
    print(f"\n\nProcessing prompt: '{arabic_prompt_4}'")
    generated_apk_4 = main_workflow(arabic_prompt_4)
    print(f"\n--- Workflow for prompt 4 finished. APK: {generated_apk_4} ---")