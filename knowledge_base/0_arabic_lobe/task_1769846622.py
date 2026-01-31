import os
import json
import shutil
from typing import List, Dict, Any

# Define constants for known directories
KNOWLEDGE_BASE_DIR = "knowledge_base"
GENERATED_CODE_DIR = "generated_code"
PROJECT_TEMPLATES_DIR = "project_templates"
OUTPUT_APKS_DIR = "output_apks"
JAVA_PROJECT_STRUCTURE = {
    "app": {
        "src": {
            "main": {
                "java": {
                    "com": {
                        "example": {
                            "myapp": {
                                "MainActivity.java": "",
                                "AndroidManifest.xml": ""
                            }
                        }
                    }
                },
                "res": {
                    "layout": {
                        "activity_main.xml": ""
                    },
                    "values": {
                        "strings.xml": ""
                    }
                }
            }
        },
        "build.gradle": ""
    },
    "settings.gradle": ""
}

class ArabicAPKGenerator:
    def __init__(self):
        self.unified_mind_state = {}
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensures that necessary directories exist."""
        for directory in [KNOWLEDGE_BASE_DIR, GENERATED_CODE_DIR, PROJECT_TEMPLATES_DIR, OUTPUT_APKS_DIR]:
            os.makedirs(directory, exist_ok=True)

    def _load_knowledge(self, filename: str) -> Dict[str, Any]:
        """Loads data from a JSON file in the knowledge base."""
        filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Knowledge file '{filename}' not found in '{KNOWLEDGE_BASE_DIR}'.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{filename}'.")
            return {}

    def _save_generated_code(self, code: str, filename: str, directory: str = GENERATED_CODE_DIR):
        """Saves generated code to a specified directory."""
        filepath = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return filepath

    def parse_arabic_request(self, arabic_request: str) -> Dict[str, Any]:
        """
        Parses an Arabic natural language request to extract parameters for APK generation.
        This is a placeholder for actual NLP processing.
        In a real scenario, this would involve tokenization, intent recognition, entity extraction, etc.
        """
        print(f"Parsing Arabic request: '{arabic_request}'")
        # Simulate parsing for a simple "Hello World" app
        if "تطبيق بسيط يعرض رسالة 'مرحباً بالعالم!'" in arabic_request and "وزر يسمى 'اضغط هنا'" in arabic_request:
            return {
                "app_name": "HelloWorldApp",
                "main_activity_name": "MainActivity",
                "layout_name": "activity_main",
                "hello_world_message": "مرحباً بالعالم!",
                "button_text": "اضغط هنا",
                "button_click_message": "تم الضغط!"
            }
        return {"error": "Could not parse the request."}

    def generate_android_project_structure(self, app_details: Dict[str, Any]) -> str:
        """
        Generates the basic Android project structure and placeholder files.
        Returns the path to the root of the generated project.
        """
        app_name = app_details.get("app_name", "MyApp")
        project_root = os.path.join(GENERATED_CODE_DIR, f"{app_name}_Project")
        os.makedirs(project_root, exist_ok=True)

        # Copy template structure and fill in placeholders
        template_path = os.path.join(PROJECT_TEMPLATES_DIR, "basic_android_template")
        if not os.path.exists(template_path):
            print(f"Warning: Basic Android template not found at '{template_path}'. Creating from scratch.")
            self._create_java_project_from_structure(project_root, app_details)
        else:
            shutil.copytree(template_path, project_root, dirs_exist_ok=True)
            # TODO: Implement logic to fill placeholders in template files

        print(f"Generated Android project structure at: {project_root}")
        return project_root

    def _create_java_project_from_structure(self, project_root: str, app_details: Dict[str, Any]):
        """Recursively creates directories and placeholder files based on JAVA_PROJECT_STRUCTURE."""
        for name, content in JAVA_PROJECT_STRUCTURE.items():
            path = os.path.join(project_root, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self._create_java_project_from_structure(path, app_details)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content) # Content is initially empty string, will be filled later

    def generate_java_code(self, app_details: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates Java code for MainActivity and AndroidManifest.xml based on app_details.
        Returns a dictionary mapping filenames to their generated code.
        """
        generated_files = {}
        package_name = f"com.example.{app_details.get('app_name', 'myapp').lower()}"
        main_activity_name = app_details.get("main_activity_name", "MainActivity")
        layout_name = app_details.get("layout_name", "activity_main")
        hello_world_message = app_details.get("hello_world_message", "Hello, World!")
        button_text = app_details.get("button_text", "Click Me")
        button_click_message = app_details.get("button_click_message", "Button Clicked!")

        # MainActivity.java
        main_activity_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class {main_activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.layout.{layout_name});

        TextView textView = findViewById(R.id.textViewMessage);
        textView.setText("{hello_world_message}");

        Button button = findViewById(R.id.buttonAction);
        button.setText("{button_text}");
        button.setOnClickListener(v -> {{
            Toast.makeText(this, "{button_click_message}", Toast.LENGTH_SHORT).show();
        }});
    }}
}}
"""
        generated_files[f"app/src/main/java/{package_name.replace('.', '/')}/{main_activity_name}.java"] = main_activity_code

        # AndroidManifest.xml
        manifest_code = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{main_activity_name}"
        tools:targetApi="31">
        <activity
            android:name=".{main_activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        generated_files["app/src/main/AndroidManifest.xml"] = manifest_code

        return generated_files

    def generate_xml_layouts(self, app_details: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates XML layout files for the Android application.
        Returns a dictionary mapping filenames to their generated XML content.
        """
        generated_files = {}
        layout_name = app_details.get("layout_name", "activity_main")
        hello_world_message = app_details.get("hello_world_message", "Hello, World!")
        button_text = app_details.get("button_text", "Click Me")

        # activity_main.xml
        layout_code = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_details.get('main_activity_name', 'MainActivity')}">

    <TextView
        android:id="@+id/textViewMessage"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{hello_world_message}"
        android:textSize="24sp"
        app:layout_constraintBottom_toTopOf="@+id/buttonAction"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_chainStyle="packed" />

    <Button
        android:id="@+id/buttonAction"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{button_text}"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textViewMessage" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        generated_files[f"app/src/main/res/layout/{layout_name}.xml"] = layout_code

        # strings.xml
        strings_code = f"""
<resources>
    <string name="app_name">{app_details.get('app_name', 'MyApp')}</string>
</resources>
"""
        generated_files["app/src/main/res/values/strings.xml"] = strings_code

        return generated_files

    def process_request(self, arabic_request: str) -> str:
        """
        Orchestrates the process of generating an APK from an Arabic request.
        """
        parsed_details = self.parse_arabic_request(arabic_request)
        if "error" in parsed_details:
            return f"Error processing request: {parsed_details['error']}"

        # Lobe 6: Synthesis - Prepare project structure
        project_root = self.generate_android_project_structure(parsed_details)
        self.unified_mind_state["project_root"] = project_root

        # Lobe 4: Code Generation - Generate Java and XML
        generated_java_files = self.generate_java_code(parsed_details)
        generated_xml_files = self.generate_xml_layouts(parsed_details)

        all_generated_files = {**generated_java_files, **generated_xml_files}

        # Save generated files into the project structure
        for rel_path, content in all_generated_files.items():
            abs_path = os.path.join(project_root, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # Lobe 8: APK Compiler - Placeholder for actual compilation
        # In a real implementation, this would involve using Gradle to build the APK.
        apk_filename = f"{parsed_details.get('app_name', 'MyApp')}.apk"
        output_apk_path = os.path.join(OUTPUT_APKS_DIR, apk_filename)

        print(f"\n--- Simulating APK Compilation ---")
        print(f"Project directory: {project_root}")
        print(f"Attempting to compile to: {output_apk_path}")
        # Simulate successful compilation
        try:
            os.makedirs(OUTPUT_APKS_DIR, exist_ok=True)
            # Create a dummy APK file for demonstration
            with open(output_apk_path, 'w') as f:
                f.write("This is a dummy APK file.")
            print(f"Dummy APK created successfully at: {output_apk_path}")
        except Exception as e:
            print(f"Error creating dummy APK: {e}")
            return f"Error during APK compilation: {e}"

        return output_apk_path

    def cleanup(self):
        """Cleans up generated project directories."""
        print("\n--- Cleaning up generated code ---")
        if "project_root" in self.unified_mind_state and os.path.exists(self.unified_mind_state["project_root"]):
            try:
                shutil.rmtree(self.unified_mind_state["project_root"])
                print(f"Removed project directory: {self.unified_mind_state['project_root']}")
            except OSError as e:
                print(f"Error removing directory {self.unified_mind_state['project_root']}: {e}")
        self.unified_mind_state = {}

# Example Usage (demonstrates integration of Lobe 0, Lobe 4, Lobe 6, Lobe 8)
if __name__ == "__main__":
    # Ensure the knowledge base directory exists and contains a dummy file if needed
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    # Add dummy knowledge file if it doesn't exist, for 'c_text' function simulation
    dummy_knowledge_file = os.path.join(KNOWLEDGE_BASE_DIR, "test_prompt_5_knowledge.json")
    if not os.path.exists(dummy_knowledge_file):
        with open(dummy_knowledge_file, 'w', encoding='utf-8') as f:
            json.dump({"prompt": "This is a test prompt.", "response": "This is a simulated response."}, f)

    # --- Simulate Lobe 0 (Arabic) ---
    arabic_request_example = "إنشاء تطبيق بسيط يعرض رسالة 'مرحباً بالعالم!' وزر يسمى 'اضغط هنا' وعند الضغط عليه يظهر رسالة 'تم الضغط!'"
    print(f"--- Simulating Lobe 0 (Arabic Parser) ---")
    # The ArabicAPKGenerator's parse_arabic_request is part of this simulation.
    # The 'c_text' function call is from a different lobe (assumed Lobe 0_language_lobe)
    # and is not directly part of this ArabicAPK generation logic, but shown for context.

    # Mock function for c_text to avoid dependency errors during standalone execution
    def c_text(prompt_key, knowledge_dir):
        filepath = os.path.join(knowledge_dir, f"{prompt_key}_knowledge.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("response", "Response not found.")
        except FileNotFoundError:
            return f"Error: Knowledge file for '{prompt_key}' not found."
        except json.JSONDecodeError:
            return f"Error: Could not decode JSON from '{filepath}'."

    test_prompt_5 = "test_prompt_5"
    generated_output_5 = c_text(test_prompt_5, KNOWLEDGE_BASE_DIR)
    print(f"Generated text for prompt '{test_prompt_5}': {generated_output_5}")

    # --- Simulate Unified Mind Processing ---
    print(f"\n--- Simulating Unified Mind Processing ---")
    unified_mind = ArabicAPKGenerator()
    final_apk_path = unified_mind.process_request(arabic_request_example)

    print(f"\nFinal Result: {final_apk_path}")

    # --- Clean up dummy files ---
    print("\n--- Cleaning up dummy files ---")
    # Define a dummy cleanup function if it's not globally available
    def cleanup_dummy_files():
        if os.path.exists(KNOWLEDGE_BASE_DIR):
            for filename in os.listdir(KNOWLEDGE_BASE_DIR):
                if filename.endswith("_knowledge.json"):
                    os.remove(os.path.join(KNOWLEDGE_BASE_DIR, filename))
            print("Removed dummy knowledge files.")

    cleanup_dummy_files()

    # Unified mind cleanup
    unified_mind.cleanup()

    print("\n--- Arabic APK Generation Module Demo Finished ---")