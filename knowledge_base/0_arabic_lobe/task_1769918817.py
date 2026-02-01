import os
import re
import json
import subprocess
from pathlib import Path

# --- Configuration ---
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
PROJECT_TEMPLATE_DIR = Path("./project_templates/android_basic")
OUTPUT_DIR = Path("./generated_apks")

# Ensure directories exist
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
PROJECT_TEMPLATE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Helper Functions ---

def load_arabic_keywords(file_path: Path) -> dict:
    """Loads Arabic keywords and their corresponding code snippets from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Keyword file not found at {file_path}. Returning empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {file_path}. Returning empty dictionary.")
        return {}

def extract_arabic_intent(text: str, keywords: dict) -> tuple[str, list]:
    """Extracts the main intent and relevant entities from Arabic text based on keywords."""
    detected_intent = "unknown"
    entities = []
    for intent, data in keywords.items():
        for keyword in data.get("keywords", []):
            if keyword in text:
                detected_intent = intent
                # Simple entity extraction: take words following the keyword as entities
                # This can be significantly improved with more sophisticated NLP techniques
                keyword_index = text.find(keyword)
                potential_entities_str = text[keyword_index + len(keyword):].strip()
                # Split by common delimiters and filter out empty strings
                potential_entities = re.split(r'[\s،,؛]', potential_entities_str)
                entities.extend([e.strip() for e in potential_entities if e.strip()])
                break # Assuming one intent per text for simplicity
        if detected_intent != "unknown":
            break
    return detected_intent, entities

def map_intent_to_code_structure(intent: str, entities: list, keywords: dict) -> dict:
    """Maps a detected Arabic intent to a basic code structure and parameters."""
    if intent in keywords:
        template_info = keywords[intent]
        code_structure = template_info.get("code_structure", {})
        # Basic mapping of entities to parameters - can be expanded
        parameters = {}
        param_mapping = template_info.get("entity_to_param_mapping", {})
        for i, entity in enumerate(entities):
            param_name = param_mapping.get(str(i), f"param{i+1}") # Default param name
            parameters[param_name] = entity
        return {
            "package_name": template_info.get("default_package_name", "com.example.generatedapp"),
            "activity_name": template_info.get("default_activity_name", "MainActivity"),
            "layout_name": template_info.get("default_layout_name", "activity_main"),
            "code_structure": code_structure,
            "parameters": parameters
        }
    return None

def generate_android_project_structure(output_project_path: Path, config: dict):
    """Generates a basic Android project structure from a template and configuration."""
    try:
        # Copy the project template
        import shutil
        shutil.copytree(PROJECT_TEMPLATE_DIR, output_project_path)
        print(f"Copied project template to: {output_project_path}")

        # Update package name and activity name in Manifest (simplified)
        manifest_path = output_project_path / "app" / "src" / "main" / "AndroidManifest.xml"
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_content = f.read()
            manifest_content = manifest_content.replace("package=\"com.example.generatedapp\"", f"package=\"{config['package_name']}\"")
            manifest_content = manifest_content.replace("android:label=\"@string/app_name\"", f"android:label=\"{config.get('app_label', 'Generated App')}\"") # Added app_label to config
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(manifest_content)
            print(f"Updated AndroidManifest.xml for package: {config['package_name']}")

        # Create or update layout file (simplified)
        layout_dir = output_project_path / "app" / "src" / "main" / "res" / "layout"
        layout_dir.mkdir(exist_ok=True)
        layout_file_path = layout_dir / f"{config['layout_name']}.xml"
        if not layout_file_path.exists():
            with open(layout_file_path, 'w', encoding='utf-8') as f:
                f.write("<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\"\n"
                        "    xmlns:app=\"http://schemas.android.com/apk/res-auto\"\n"
                        "    xmlns:tools=\"http://schemas.android.com/tools\"\n"
                        "    android:layout_width=\"match_parent\"\n"
                        "    android:layout_height=\"match_parent\"\n"
                        "    android:orientation=\"vertical\"\n"
                        "    tools:context=\".MainActivity\">\n\n" # Default context
                        "    <TextView\n"
                        "        android:id=\"@+id/greeting_text\"\n"
                        "        android:layout_width=\"wrap_content\"\n"
                        "        android:layout_height=\"wrap_content\"\n"
                        "        android:text=\"Hello from Generated App!\"\n"
                        "        android:textSize=\"24sp\"\n"
                        "        android:layout_gravity=\"center_horizontal\"\n"
                        "        android:layout_marginTop=\"16dp\"/>\n\n"
                        "    <!-- Content from Arabic intent will be placed here -->\n"
                        "</LinearLayout>")
            print(f"Created layout file: {layout_file_path}")

        # Generate Java/Kotlin code for MainActivity (simplified)
        src_dir = output_project_path / "app" / "src" / "main" / "java" / config['package_name'].replace('.', os.sep)
        src_dir.mkdir(parents=True, exist_ok=True)
        main_activity_path = src_dir / f"{config['activity_name']}.java" # Default to Java
        if not main_activity_path.exists():
            with open(main_activity_path, 'w', encoding='utf-8') as f:
                f.write(f"package {config['package_name']};\n\n"
                        "import androidx.appcompat.app.AppCompatActivity;\n"
                        "import android.os.Bundle;\n"
                        "import android.widget.TextView;\n\n"
                        f"public class {config['activity_name']} extends AppCompatActivity {{\n\n"
                        "    @Override\n"
                        "    protected void onCreate(Bundle savedInstanceState) {\n"
                        "        super.onCreate(savedInstanceState);\n"
                        f"        setContentView(R.layout.{config['layout_name']});\n\n"
                        "        TextView greetingTextView = findViewById(R.id.greeting_text);\n"
                        f"        // Logic based on Arabic intent parameters will go here.\n"
                        f"        // Example: greetingTextView.setText(\"Hello, {config.get('parameters', {}).get('name', 'World')}!\");\n"
                        "    }\n"
                        "}\n")
            print(f"Created MainActivity: {main_activity_path}")

        return True

    except Exception as e:
        print(f"Error generating Android project structure: {e}")
        return False

class Lobe_Arabic_NLP_APK_Builder:
    """
    This Lobe focuses on processing Arabic natural language input to define
    an Android application's core structure and then initiates the APK build process.
    """

    def __init__(self, keywords_file: Path = KNOWLEDGE_BASE_DIR / "arabic_keywords.json"):
        self.keywords = load_arabic_keywords(keywords_file)
        self.current_project_config = None
        self.generated_project_path = None

    def process_arabic_input(self, arabic_text: str) -> bool:
        """
        Processes Arabic text to extract intent and generate a configuration
        for an Android application.
        """
        if not self.keywords:
            print("Error: Arabic keywords not loaded. Cannot process input.")
            return False

        intent, entities = extract_arabic_intent(arabic_text, self.keywords)
        print(f"Detected Intent: {intent}, Entities: {entities}")

        if intent == "unknown":
            print("Could not determine a known intent from the Arabic text.")
            return False

        self.current_project_config = map_intent_to_code_structure(intent, entities, self.keywords)

        if self.current_project_config:
            print(f"Generated project configuration: {json.dumps(self.current_project_config, indent=2, ensure_ascii=False)}")
            return True
        else:
            print("Failed to map intent to a project configuration.")
            return False

    def build_apk_structure(self, output_apk_dir: Path = OUTPUT_DIR) -> bool:
        """
        Generates the basic Android project structure based on the processed configuration.
        """
        if not self.current_project_config:
            print("No project configuration available. Call process_arabic_input first.")
            return False

        package_name = self.current_project_config.get("package_name", "com.example.generatedapp").replace('.', os.sep)
        activity_name = self.current_project_config.get("activity_name", "MainActivity")
        project_name = f"{activity_name}_{package_name.split(os.sep)[-1]}" # Simple project naming
        self.generated_project_path = output_apk_dir / project_name

        print(f"\n--- Generating Android Project Structure for: {project_name} ---")
        success = generate_android_project_structure(self.generated_project_path, self.current_project_config)

        if success:
            print(f"Android project structure generated at: {self.generated_project_path}")
            return True
        else:
            print("Failed to generate Android project structure.")
            return False

    def compile_apk(self) -> bool:
        """
        Initiates the compilation of the generated Android project into an APK.
        This is a placeholder for actual build commands (e.g., Gradle).
        """
        if not self.generated_project_path or not self.generated_project_path.exists():
            print("Android project not found. Cannot compile APK.")
            return False

        print("\n--- Initiating APK Compilation (Simulated) ---")
        print(f"Attempting to compile project at: {self.generated_project_path}")

        # --- Actual Compilation Steps (requires Android SDK and Gradle) ---
        # This is a placeholder. In a real scenario, you would execute Gradle commands.
        # Example:
        # try:
        #     # Assumes Gradle wrapper exists in the project
        #     gradle_wrapper_path = self.generated_project_path / "gradlew"
        #     if not gradle_wrapper_path.exists():
        #         print("Gradle wrapper not found. Cannot compile.")
        #         return False
        #
        #     # Run the assembleDebug or assembleRelease task
        #     # Use subprocess.run for more robust execution
        #     result = subprocess.run([str(gradle_wrapper_path), "assembleDebug"],
        #                             cwd=str(self.generated_project_path),
        #                             capture_output=True,
        #                             text=True,
        #                             check=True) # check=True raises CalledProcessError on non-zero exit code
        #
        #     print("Gradle build output:\n", result.stdout)
        #     if result.stderr:
        #         print("Gradle build errors:\n", result.stderr)
        #
        #     # Find the generated APK (location can vary based on Gradle configuration)
        #     # Example: app/build/outputs/apk/debug/app-debug.apk
        #     apk_path = self.generated_project_path / "app" / "build" / "outputs" / "apk" / "debug" / f"{self.current_project_config.get('activity_name', 'app').lower()}-debug.apk"
        #     if apk_path.exists():
        #         print(f"APK successfully built at: {apk_path}")
        #         return True
        #     else:
        #         print("APK file not found after build. Check Gradle output.")
        #         return False
        #
        # except FileNotFoundError:
        #     print("Error: gradlew command not found. Ensure Android SDK and Gradle are set up correctly.")
        #     return False
        # except subprocess.CalledProcessError as e:
        #     print(f"Gradle build failed with exit code {e.returncode}")
        #     print("Stdout:\n", e.stdout)
        #     print("Stderr:\n", e.stderr)
        #     return False
        # except Exception as e:
        #     print(f"An unexpected error occurred during compilation: {e}")
        #     return False
        # --- End of Actual Compilation Steps ---

        # Simulated success for demonstration
        print("Simulating successful APK compilation.")
        print(f"APK would be generated in: {self.generated_project_path / 'app' / 'build' / 'outputs' / 'apk' / 'debug'}")
        return True


# --- Example Usage (for testing the Lobe) ---
if __name__ == "__main__":
    # Create a dummy keywords file for demonstration
    if not (KNOWLEDGE_BASE_DIR / "arabic_keywords.json").exists():
        dummy_keywords_data = {
            "hello_world_app": {
                "keywords": ["تطبيق ترحيب", "إنشاء تطبيق ترحيب"],
                "default_package_name": "com.example.hellogreeter",
                "default_activity_name": "GreetingActivity",
                "default_layout_name": "activity_greeting",
                "app_label": "Hello Greeter",
                "entity_to_param_mapping": {
                    "0": "name" # Expecting a name after "تطبيق ترحيب بـ " for example
                },
                "code_structure": {
                    "activity": "AppCompatActivity",
                    "layout": "activity_greeting",
                    "views": [
                        {"type": "TextView", "id": "greeting_text", "text": "أهلاً بك، {name}!"}
                    ]
                }
            },
            "calculator_app": {
                "keywords": ["آلة حاسبة", "برنامج حساب"],
                "default_package_name": "com.example.calculator",
                "default_activity_name": "CalculatorActivity",
                "default_layout_name": "activity_calculator",
                 "app_label": "Simple Calculator",
                "code_structure": {
                    "activity": "AppCompatActivity",
                    "layout": "activity_calculator",
                    "views": [
                        {"type": "EditText", "id": "num1"},
                        {"type": "EditText", "id": "num2"},
                        {"type": "Button", "id": "add_button", "text": "+"},
                        {"type": "TextView", "id": "result_text"}
                    ]
                }
            }
        }
        with open(KNOWLEDGE_BASE_DIR / "arabic_keywords.json", 'w', encoding='utf-8') as f:
            json.dump(dummy_keywords_data, f, indent=2, ensure_ascii=False)
        print(f"Created dummy keyword file: {KNOWLEDGE_BASE_DIR / 'arabic_keywords.json'}")

    # Create a dummy project template directory and files if they don't exist
    if not (PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml").exists():
        print(f"Creating dummy project template at: {PROJECT_TEMPLATE_DIR}")
        (PROJECT_TEMPLATE_DIR / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
        (PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml").write_text(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.generatedapp">\n'
            '    <application\n'
            '        android:allowBackup="true"\n'
            '        android:icon="@mipmap/ic_launcher"\n'
            '        android:label="@string/app_name"\n'
            '        android:roundIcon="@mipmap/ic_launcher_round"\n'
            '        android:supportsRtl="true"\n'
            '        android:theme="@style/Theme.GeneratedApp">\n'
            '        <activity android:name=".MainActivity" android:exported="true">\n'
            '            <intent-filter>\n'
            '                <action android:name="android.intent.action.MAIN" />\n'
            '                <category android:name="android.intent.category.LAUNCHER" />\n'
            '            </intent-filter>\n'
            '        </activity>\n'
            '    </application>\n'
            '</manifest>\n'
        )
        (PROJECT_TEMPLATE_DIR / "build.gradle").write_text('// Dummy build.gradle\n')
        (PROJECT_TEMPLATE_DIR / "gradlew").write_text('#!/bin/bash\n# Dummy gradlew script\n')
        os.chmod(str(PROJECT_TEMPLATE_DIR / "gradlew"), 0o755) # Make executable


    # Instantiate the Lobe
    arabic_apk_builder = Lobe_Arabic_NLP_APK_Builder()

    # Test Case 1: Hello World App
    print("\n--- Testing Hello World App Generation ---")
    arabic_input_hello = "أنشئ تطبيق ترحيب باسم أحمد"
    if arabic_apk_builder.process_arabic_input(arabic_input_hello):
        if arabic_apk_builder.build_apk_structure():
            if arabic_apk_builder.compile_apk():
                print("\n--- Hello World App Test Completed Successfully ---")
            else:
                print("\n--- Hello World App Test: APK Compilation Failed ---")
        else:
            print("\n--- Hello World App Test: Structure Generation Failed ---")
    else:
        print("\n--- Hello World App Test: Input Processing Failed ---")

    # Clean up generated project for the next test
    if arabic_apk_builder.generated_project_path and arabic_apk_builder.generated_project_path.exists():
        print(f"Cleaning up previous project: {arabic_apk_builder.generated_project_path}")
        import shutil
        shutil.rmtree(arabic_apk_builder.generated_project_path)

    # Test Case 2: Calculator App
    print("\n--- Testing Calculator App Generation ---")
    arabic_input_calc = "أريد إنشاء آلة حاسبة بسيطة"
    # Re-instantiate or reset internal state if necessary for clean test
    arabic_apk_builder = Lobe_Arabic_NLP_APK_Builder() # Re-instantiate for a clean state
    if arabic_apk_builder.process_arabic_input(arabic_input_calc):
        if arabic_apk_builder.build_apk_structure():
            if arabic_apk_builder.compile_apk():
                print("\n--- Calculator App Test Completed Successfully ---")
            else:
                print("\n--- Calculator App Test: APK Compilation Failed ---")
        else:
            print("\n--- Calculator App Test: Structure Generation Failed ---")
    else:
        print("\n--- Calculator App Test: Input Processing Failed ---")

    # Final cleanup of generated APKs directory
    print(f"\n--- Final Cleanup ---")
    if OUTPUT_DIR.exists():
        print(f"Contents of {OUTPUT_DIR} will be kept for inspection.")
        # Example cleanup:
        # import shutil
        # shutil.rmtree(OUTPUT_DIR)
        # print(f"Removed directory: {OUTPUT_DIR}")

    print("\n--- Lobe_Arabic_NLP_APK_Builder Demo Finished ---")