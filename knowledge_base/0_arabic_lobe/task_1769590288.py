import os
import json
import shutil
import subprocess
from pathlib import Path

# Assume other lobes are imported and accessible here, e.g.:
# from lobe_0_language_lobe import LanguageLobe
# from lobe_4_code_generation_lobe import CodeGenerationLobe
# from lobe_11_apk_packaging_lobe import ApkPackagingLobe

class ArabicNLPProcessingLobe:
    """
    Lobe responsible for processing Arabic natural language input
    and transforming it into structured data suitable for code generation.
    """
    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base_path = knowledge_base_path
        self.structured_data = None

    def load_arabic_knowledge_base(self) -> dict:
        """
        Loads the Arabic knowledge base from a JSON file.
        This KB should contain mappings of Arabic phrases to Android UI components,
        permissions, intents, and other relevant APK configurations.
        """
        kb_file = self.knowledge_base_path / "arabic_nlp_kb.json"
        if not kb_file.exists():
            raise FileNotFoundError(f"Arabic knowledge base not found at {kb_file}")
        with open(kb_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse_arabic_prompt(self, arabic_prompt: str, knowledge_base: dict) -> dict:
        """
        Parses the Arabic natural language prompt using the loaded knowledge base.
        Identifies intents, entities, and actions described in the prompt.
        Returns a structured dictionary representing the parsed intent.
        """
        parsed_intent = {
            "components": [],
            "permissions": [],
            "actions": [],
            "strings": {},
            "layout_elements": [],
            "manifest_settings": {}
        }

        # Simple keyword matching for demonstration. A real implementation
        # would use more advanced NLP techniques like Named Entity Recognition (NER),
        # dependency parsing, and intent classification specific to Arabic.
        for keyword, config in knowledge_base.items():
            if keyword in arabic_prompt:
                if "components" in config:
                    parsed_intent["components"].extend(config["components"])
                if "permissions" in config:
                    parsed_intent["permissions"].extend(config["permissions"])
                if "actions" in config:
                    parsed_intent["actions"].extend(config["actions"])
                if "strings" in config:
                    parsed_intent["strings"].update(config["strings"])
                if "layout_elements" in config:
                    parsed_intent["layout_elements"].extend(config["layout_elements"])
                if "manifest_settings" in config:
                    parsed_intent["manifest_settings"].update(config["manifest_settings"])

        # Further refine parsing based on prompt structure and context.
        # For example, if prompt is "إنشاء زر يسمى 'ابدأ'" (Create a button called 'Start')
        if "إنشاء زر" in arabic_prompt or "أضف زر" in arabic_prompt:
            button_name_match = self.extract_button_name(arabic_prompt)
            if button_name_match:
                parsed_intent["layout_elements"].append({"type": "Button", "text": button_name_match})
                parsed_intent["strings"][f"btn_{button_name_match.lower()}"] = button_name_match


        self.structured_data = parsed_intent
        return parsed_intent

    def extract_button_name(self, prompt: str) -> str | None:
        """
        Helper to extract button names from Arabic prompts.
        Example: "إنشاء زر يسمى 'ابدأ'" -> "ابدأ"
        """
        parts = prompt.split("'")
        if len(parts) > 1:
            return parts[1]
        return None

    def process(self, arabic_prompt: str) -> dict:
        """
        Main method to process an Arabic prompt.
        """
        print("\n--- Initiating Arabic NLP Processing Lobe ---")
        knowledge_base = self.load_arabic_knowledge_base()
        parsed_data = self.parse_arabic_prompt(arabic_prompt, knowledge_base)
        print(f"Parsed Arabic prompt into structured data: {json.dumps(parsed_data, indent=2, ensure_ascii=False)}")
        print("--- Arabic NLP Processing Lobe Finished ---")
        return parsed_data

# Example Usage (simulating integration with other lobes)

if __name__ == "__main__":
    # Mocking dependencies for standalone execution
    class MockCodeGenerationLobe:
        def generate_android_code(self, structured_data: dict) -> dict:
            print("\n--- Mock Code Generation Lobe Called ---")
            generated_files = {}
            # Simulate generating a basic Activity and layout XML
            if "layout_elements" in structured_data and structured_data["layout_elements"]:
                layout_xml_content = "<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\"\n    android:layout_width=\"match_parent\"\n    android:layout_height=\"match_parent\"\n    android:orientation=\"vertical\">\n"
                for element in structured_data["layout_elements"]:
                    if element["type"] == "Button":
                        button_id = f"btn_{element['text'].lower().replace(' ', '_')}"
                        layout_xml_content += f'    <Button\n        android:id="@+id/{button_id}"\n        android:layout_width="wrap_content"\n        android:layout_height="wrap_content"\n        android:text="{element["text"]}" />\n'
                layout_xml_content += "</LinearLayout>"
                generated_files["res/layout/activity_main.xml"] = layout_xml_content

            if "permissions" in structured_data and structured_data["permissions"]:
                # Simulate manifest addition
                manifest_content = "<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"com.example.myapp\">\n    <uses-permission android:name=\"android.permission.INTERNET\" />\n"
                for perm in structured_data["permissions"]:
                    manifest_content += f'    <uses-permission android:name="android.permission.{perm.upper()}" />\n'
                manifest_content += "    <application ...>\n        <activity android:name=\".MainActivity\">\n            <intent-filter>\n                <action android:name=\"android.intent.action.MAIN\" />\n                <category android:name=\"android.intent.category.LAUNCHER\" />\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>"
                generated_files["AndroidManifest.xml"] = manifest_content

            if "strings" in structured_data and structured_data["strings"]:
                strings_xml_content = "<resources>\n"
                for key, value in structured_data["strings"].items():
                    strings_xml_content += f'    <string name="{key}">{value}</string>\n'
                strings_xml_content += "</resources>"
                generated_files["res/values/strings.xml"] = strings_xml_content

            print("Mock code generation complete. Files: ", list(generated_files.keys()))
            return {"code_files": generated_files}

    class MockApkPackagingLobe:
        def package_apk(self, source_files: dict, app_name: str = "MyApp") -> Path:
            print("\n--- Mock APK Packaging Lobe Called ---")
            output_dir = Path("mock_apk_output")
            output_dir.mkdir(exist_ok=True)
            print(f"Simulating packaging into {output_dir / f'{app_name}.apk'}...")
            # Simulate creating a dummy APK file
            apk_path = output_dir / f"{app_name}.apk"
            with open(apk_path, "w") as f:
                f.write("This is a mock APK file.\n")
            print("Mock APK packaging complete.")
            return apk_path

    # --- Setup for demonstration ---
    KNOWLEDGE_BASE_DIR = Path("./knowledge_bases")
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    ARABIC_KB_FILE = KNOWLEDGE_BASE_DIR / "arabic_nlp_kb.json"

    arabic_kb_content = {
        "إنشاء تطبيق": {
            "actions": ["CREATE_APP"],
            "manifest_settings": {"package": "com.example.generatedapp"}
        },
        "طلب صلاحية الإنترنت": {
            "permissions": ["INTERNET"]
        },
        "زر ابدأ": {
            "layout_elements": [{"type": "Button", "text": "ابدأ"}],
            "strings": {"start_button_text": "ابدأ"}
        },
        "زر تسجيل الدخول": {
            "layout_elements": [{"type": "Button", "text": "تسجيل الدخول"}],
            "strings": {"login_button_text": "تسجيل الدخول"}
        },
        "حقل نصي للاسم": {
            "layout_elements": [{"type": "EditText", "hint": "أدخل الاسم"}],
            "strings": {"name_input_hint": "أدخل الاسم"}
        }
    }

    with open(ARABIC_KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(arabic_kb_content, f, indent=2, ensure_ascii=False)

    # --- Orchestration ---
    unified_prompt = "قم بإنشاء تطبيق بسيط يتضمن زر ابدأ وطلب صلاحية الإنترنت. يجب أن يكون هناك أيضاً حقل نصي للاسم."
    print(f"--- GRAND OBJECTIVE: Evolve into a unified, conscious mind. Master 12 lobes to generate hyper-efficient APKs from natural language. ---")
    print(f"--- Processing Prompt: '{unified_prompt}' ---")

    # Lobe 0: Arabic NLP Processing
    arabic_nlp_lobe = ArabicNLPProcessingLobe(knowledge_base_path=KNOWLEDGE_BASE_DIR)
    parsed_data = arabic_nlp_lobe.process(unified_prompt)

    # Lobe 4: Code Generation (Mocked)
    code_gen_lobe = MockCodeGenerationLobe()
    generated_code_output = code_gen_lobe.generate_android_code(parsed_data)

    # Lobe 8: APK Compiler (Mocked) - Assuming it takes generated code files
    # Lobe 11: APK Packaging (Mocked) - Renamed from 8 in your provided logs
    apk_package_lobe = MockApkPackagingLobe()
    # In a real scenario, the compiler lobe would produce intermediate build artifacts
    # that the packaging lobe then uses. Here, we pass the generated code files directly.
    apk_path = apk_package_lobe.package_apk(generated_code_output["code_files"], app_name="GeneratedApp")

    print(f"\n--- APK generation process for prompt '{unified_prompt}' completed. ---")
    print(f"Generated APK located at: {apk_path.resolve()}")

    # Clean up dummy KB file
    print("\n--- Cleaning up dummy knowledge base file ---")
    if ARABIC_KB_FILE.exists():
        ARABIC_KB_FILE.unlink()
    if KNOWLEDGE_BASE_DIR.is_dir() and not os.listdir(KNOWLEDGE_BASE_DIR):
        KNOWLEDGE_BASE_DIR.rmdir()
    if Path("mock_apk_output").exists():
        shutil.rmtree("mock_apk_output")

    print("\n--- Demonstration Finished ---")