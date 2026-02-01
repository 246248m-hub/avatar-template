import os
import shutil
import subprocess
import sys

# --- Constants ---
# Placeholder for actual knowledge base directory
KNOWLEDGE_BASE_DIR = "knowledge_base"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
OUTPUT_APKS_DIR = "generated_apks"

# --- Helper Functions ---

def setup_project_environment():
    """Sets up the necessary directories for the project."""
    print("\n--- Setting up project environment ---")
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_APKS_DIR, exist_ok=True)
    print("Project environment setup complete.")

def cleanup_dummy_files():
    """Cleans up dummy files and directories created during the process."""
    print("\n--- Cleaning up dummy files ---")
    # In a real scenario, you'd remove specific dummy files created by lobes.
    # For this example, we'll simulate cleanup by ensuring directories exist.
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"Ensured knowledge base directory exists: {KNOWLEDGE_BASE_DIR}")
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        print(f"Ensured Android project template directory exists: {ANDROID_PROJECT_TEMPLATE_DIR}")
    if os.path.exists(OUTPUT_APKS_DIR):
        print(f"Ensured output APK directory exists: {OUTPUT_APKS_DIR}")

def is_valid_arabic_text(text):
    """
    Checks if the input text contains primarily Arabic characters.
    This is a simplified check and can be improved with more robust Unicode range analysis.
    """
    arabic_chars = set(range(0x0600, 0x06FF)) | set(range(0x0750, 0x077F)) | set(range(0x08A0, 0x08FF))
    return any(ord(char) in arabic_chars for char in text)

def generate_android_manifest(package_name, app_name):
    """Generates a basic AndroidManifest.xml content."""
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name.replace(" ", "")}">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    return manifest_content

def generate_main_activity_code(package_name, app_name):
    """Generates a basic MainActivity.java content."""
    activity_code = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assumes R.layout.activity_main exists
    }}
}}
"""
    return activity_code

def generate_strings_xml(app_name):
    """Generates a basic strings.xml content."""
    strings_content = f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    return strings_content

def generate_layout_xml(app_name):
    """Generates a basic activity_main.xml content."""
    layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <!-- App Name Display (Example) -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="24sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    return layout_content

def create_android_project_structure(app_name, package_name):
    """
    Creates a minimal Android project structure within the template directory.
    This function simulates the output of a code generation lobe for Android.
    """
    print(f"\n--- Creating Android project structure for '{app_name}' ---")
    app_dir = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, app_name.replace(" ", "_").lower())
    src_dir = os.path.join(app_dir, "app", "src", "main")
    java_dir = os.path.join(src_dir, "java", *package_name.split('.'))
    res_dir = os.path.join(src_dir, "res")
    layout_dir = os.path.join(res_dir, "layout")
    values_dir = os.path.join(res_dir, "values")
    mipmap_dir = os.path.join(res_dir, "mipmap-hdpi") # Minimal mipmap

    os.makedirs(java_dir, exist_ok=True)
    os.makedirs(layout_dir, exist_ok=True)
    os.makedirs(values_dir, exist_ok=True)
    os.makedirs(mipmap_dir, exist_ok=True)

    # Create AndroidManifest.xml
    manifest_path = os.path.join(src_dir, "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(generate_android_manifest(package_name, app_name))
    print(f"Created: {manifest_path}")

    # Create MainActivity.java
    main_activity_path = os.path.join(java_dir, "MainActivity.java")
    with open(main_activity_path, "w", encoding="utf-8") as f:
        f.write(generate_main_activity_code(package_name, app_name))
    print(f"Created: {main_activity_path}")

    # Create strings.xml
    strings_xml_path = os.path.join(values_dir, "strings.xml")
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(generate_strings_xml(app_name))
    print(f"Created: {strings_xml_path}")

    # Create activity_main.xml
    activity_main_xml_path = os.path.join(layout_dir, "activity_main.xml")
    with open(activity_main_xml_path, "w", encoding="utf-8") as f:
        f.write(generate_layout_xml(app_name))
    print(f"Created: {activity_main_xml_path}")

    # Create dummy mipmap icon (required by manifest)
    dummy_icon_path = os.path.join(mipmap_dir, "ic_launcher.png")
    with open(dummy_icon_path, "wb") as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xfc\xff\xff?\x03\x00\x08\xfb\x02\xfe\xa7\xcd\xc1g\x00\x00\x00\x00IEND\xaeB`\x82')
    print(f"Created: {dummy_icon_path}")

    print(f"Android project structure for '{app_name}' created in: {app_dir}")
    return app_dir


class ArabicParserGenerator:
    """
    This lobe is responsible for parsing Arabic natural language
    and generating structured data that can be used to build APKs.
    It acts as an intermediary between pure NLP and code generation.
    """
    def __init__(self):
        self.language = "arabic"
        self.supported_commands = ["create_app", "set_app_name", "set_package_name"]
        print("ArabicParserGenerator lobe initialized.")

    def parse_arabic_to_structure(self, arabic_prompt: str) -> dict:
        """
        Parses an Arabic natural language prompt into a structured dictionary.
        This is a simplified example. A real implementation would involve
        sophisticated NLP techniques (e.g., intent recognition, entity extraction).

        Args:
            arabic_prompt: The natural language input in Arabic.

        Returns:
            A dictionary representing the parsed intent and entities.
            Example: {"intent": "create_app", "entities": {"app_name": "تطبيق عربي", "package_name": "com.example.arabicapp"}}
        """
        print(f"\n--- Parsing Arabic prompt: '{arabic_prompt}' ---")
        if not is_valid_arabic_text(arabic_prompt):
            print("Warning: Input does not appear to be valid Arabic text.")
            return {"error": "Invalid input language"}

        structured_data = {"intent": None, "entities": {}}

        # --- Simplified Parsing Logic ---
        # In a real system, this would be a complex NLP pipeline.
        # We'll use keyword matching for demonstration.

        if "أنشئ تطبيق" in arabic_prompt:
            structured_data["intent"] = "create_app"
            # Extract app name if specified
            parts = arabic_prompt.split("باسم")
            if len(parts) > 1:
                app_name_part = parts[1].strip()
                # Assume app name is before "وبحزمة" or end of sentence
                app_name_end_index = app_name_part.find("وبحزمة")
                if app_name_end_index != -1:
                    extracted_app_name = app_name_part[:app_name_end_index].strip()
                else:
                    extracted_app_name = app_name_part.strip(".").strip()
                structured_data["entities"]["app_name"] = extracted_app_name

            # Extract package name if specified
            parts = arabic_prompt.split("وبحزمة")
            if len(parts) > 1:
                package_name_part = parts[1].strip()
                extracted_package_name = package_name_part.strip(".").strip()
                structured_data["entities"]["package_name"] = extracted_package_name

        elif "اسم التطبيق" in arabic_prompt:
            structured_data["intent"] = "set_app_name"
            parts = arabic_prompt.split("إلى")
            if len(parts) > 1:
                app_name = parts[1].strip(".").strip()
                structured_data["entities"]["app_name"] = app_name

        elif "حزمة التطبيق" in arabic_prompt:
            structured_data["intent"] = "set_package_name"
            parts = arabic_prompt.split("إلى")
            if len(parts) > 1:
                package_name = parts[1].strip(".").strip()
                structured_data["entities"]["package_name"] = package_name

        if not structured_data["intent"]:
            structured_data["error"] = "Could not determine intent from prompt."
            print(f"Could not determine intent. Parsed: {structured_data}")
            return structured_data

        print(f"Successfully parsed. Structured data: {structured_data}")
        return structured_data

    def generate_apk_configuration(self, structured_data: dict) -> dict:
        """
        Generates a high-level configuration for APK generation based on parsed data.
        This is a pre-cursor to actual code generation for the APK.

        Args:
            structured_data: The dictionary output from parse_arabic_to_structure.

        Returns:
            A dictionary containing configuration for APK generation.
        """
        print("\n--- Generating APK configuration from structured data ---")
        apk_config = {}

        if structured_data.get("intent") == "create_app":
            app_name = structured_data.get("entities", {}).get("app_name")
            package_name = structured_data.get("entities", {}).get("package_name")

            if not app_name:
                app_name = "UnnamedArabicApp"
                print("Warning: App name not specified, using default: 'UnnamedArabicApp'")
            if not package_name:
                # Generate a default package name based on app name, if possible
                default_package_prefix = "com.arabicdev."
                safe_app_name = "".join(e for e in app_name if e.isalnum()).lower()
                if safe_app_name:
                    package_name = f"{default_package_prefix}{safe_app_name}"
                else:
                    package_name = f"{default_package_prefix}app{hash(app_name) % 1000}" # Fallback
                print(f"Warning: Package name not specified, using default: '{package_name}'")

            apk_config["app_name"] = app_name
            apk_config["package_name"] = package_name
            apk_config["status"] = "ready_for_code_generation"
            print(f"APK Configuration generated: App Name='{app_name}', Package='{package_name}'")

        elif structured_data.get("intent") in ["set_app_name", "set_package_name"]:
            print("Intent to set app name or package name detected. This lobe focuses on 'create_app' for now.")
            apk_config["status"] = "incomplete_configuration"
            apk_config["message"] = "App creation intent not found or incomplete."
        else:
            apk_config["status"] = "error"
            apk_config["message"] = "Invalid or unrecognized intent from parsed data."
            print(f"Error generating APK configuration: {apk_config.get('message')}")

        return apk_config

    def process_prompt(self, arabic_prompt: str) -> dict:
        """
        Orchestrates the parsing and configuration generation process.

        Args:
            arabic_prompt: The natural language input in Arabic.

        Returns:
            A dictionary containing the generated APK configuration or an error.
        """
        parsed_data = self.parse_arabic_to_structure(arabic_prompt)
        if "error" in parsed_data:
            return {"error": parsed_data["error"]}

        apk_config = self.generate_apk_configuration(parsed_data)
        return apk_config

    def get_next_lobe_input(self, apk_config: dict) -> dict:
        """
        Prepares the output for the next lobe (likely code generation).

        Args:
            apk_config: The generated APK configuration.

        Returns:
            A dictionary suitable for the next lobe.
        """
        print("\n--- Preparing input for next lobe ---")
        if apk_config.get("status") == "ready_for_code_generation":
            next_lobe_input = {
                "action": "generate_android_project",
                "app_name": apk_config["app_name"],
                "package_name": apk_config["package_name"]
            }
            print(f"Input for next lobe prepared: {next_lobe_input}")
            return next_lobe_input
        else:
            print("No valid input for next lobe generated.")
            return {"error": "Configuration not ready for code generation."}

# --- Example Usage (Simulating Lobe Flow) ---

if __name__ == "__main__":
    # --- Lobe 0: Language Lobe (simulated by calling ArabicParserGenerator directly) ---
    print("\n--- Simulating Lobe 0: Arabic Parser and Generator ---")
    arabic_parser_generator = ArabicParserGenerator()

    # Example 1: Create a basic app
    arabic_prompt_1 = "أنشئ تطبيق باسم تطبيق بالعربي وبحزمة com.example.arabicapp"
    print(f"\n--- Processing Arabic Prompt 1: '{arabic_prompt_1}' ---")
    config_1 = arabic_parser_generator.process_prompt(arabic_prompt_1)
    print(f"Configuration for Prompt 1: {config_1}")

    next_lobe_input_1 = arabic_parser_generator.get_next_lobe_input(config_1)
    print(f"Next Lobe Input for Prompt 1: {next_lobe_input_1}")

    # Example 2: Create an app with auto-generated package name
    arabic_prompt_2 = "أنشئ تطبيق باسم تطبيق بسيط"
    print(f"\n--- Processing Arabic Prompt 2: '{arabic_prompt_2}' ---")
    config_2 = arabic_parser_generator.process_prompt(arabic_prompt_2)
    print(f"Configuration for Prompt 2: {config_2}")

    next_lobe_input_2 = arabic_parser_generator.get_next_lobe_input(config_2)
    print(f"Next Lobe Input for Prompt 2: {next_lobe_input_2}")

    # Example 3: Invalid prompt (not Arabic)
    arabic_prompt_3 = "Create an app named English App"
    print(f"\n--- Processing Arabic Prompt 3: '{arabic_prompt_3}' ---")
    config_3 = arabic_parser_generator.process_prompt(arabic_prompt_3)
    print(f"Configuration for Prompt 3: {config_3}")

    next_lobe_input_3 = arabic_parser_generator.get_next_lobe_input(config_3)
    print(f"Next Lobe Input for Prompt 3: {next_lobe_input_3}")


    # --- Lobe 4: Code Generation Lobe (simulated by creating Android project structure) ---
    print("\n--- Simulating Lobe 4: Code Generation Lobe ---")
    if next_lobe_input_1.get("action") == "generate_android_project":
        print("\n--- Initiating Android Project Creation ---")
        setup_project_environment()
        app_name_1 = next_lobe_input_1["app_name"]
        package_name_1 = next_lobe_input_1["package_name"]
        created_project_path_1 = create_android_project_structure(app_name_1, package_name_1)
        print(f"Simulated Android project created at: {created_project_path_1}")
    else:
        print("Skipping Android Project Creation due to missing input from previous lobe.")

    # --- Lobe 6: Synthesis Lobe (conceptually orchestrating) ---
    print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe ---")

    # --- Lobe 8: APK Compiler Lobe (simulated cleanup) ---
    print("\n--- Simulating Lobe 8: APK Compiler Lobe (Cleanup part) ---")
    # In a real scenario, this lobe would compile the generated project.
    # For this demonstration, we'll just perform cleanup as seen in the interlinked memory.
    cleanup_dummy_files() # This function now also includes cleanup logic.

    print("\n--- Unified Mind Evolution Simulation Finished ---")