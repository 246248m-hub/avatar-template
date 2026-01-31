import os
import json
import xml.etree.ElementTree as ET
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Assume Lobe 0_language_lobe provides a function to process Arabic text
# Assume Lobe 6_synthesis_lobe provides a function to synthesize components

# --- Constants and Configuration ---
ARABIC_RESOURCE_DIR = "arabic_resources"
MANIFEST_TEMPLATE_PATH = os.path.join(ARABIC_RESOURCE_DIR, "AndroidManifest.xml.template")
STRINGS_TEMPLATE_PATH = os.path.join(ARABIC_RESOURCE_DIR, "values/strings.xml.template")
LAYOUT_TEMPLATE_PATH = os.path.join(ARABIC_RESOURCE_DIR, "layout/activity_main.xml.template")

# --- Helper Functions ---

def load_template(template_path):
    """Loads content from a template file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(content, filepath):
    """Saves content to a file, creating directories if necessary."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {filepath}")

def preprocess_arabic_text(text):
    """Reshapes and bidi-corrects Arabic text."""
    reshaped_text = reshape(text)
    return get_display(reshaped_text)

def extract_apk_elements(natural_language_description):
    """
    Parses a natural language description to extract key APK components.
    This is a simplified example; a real implementation would involve more
    sophisticated NLP techniques.
    """
    elements = {
        "app_name": "My Arabic App",
        "main_activity_label": "Home",
        "welcome_message": "Welcome!",
        "package_name": "com.example.arabicapp"
    }

    # Simple keyword-based extraction
    if "app name is" in natural_language_description.lower():
        parts = natural_language_description.lower().split("app name is")
        if len(parts) > 1:
            elements["app_name"] = parts[1].split(".")[0].strip().capitalize()

    if "main screen title" in natural_language_description.lower():
        parts = natural_language_description.lower().split("main screen title")
        if len(parts) > 1:
            elements["main_activity_label"] = parts[1].split(".")[0].strip().capitalize()

    if "welcome message" in natural_language_description.lower():
        parts = natural_language_description.lower().split("welcome message")
        if len(parts) > 1:
            elements["welcome_message"] = parts[1].split(".")[0].strip()

    if "package name" in natural_language_description.lower():
        parts = natural_language_description.lower().split("package name")
        if len(parts) > 1:
            elements["package_name"] = parts[1].split(".")[0].strip()

    # Preprocess Arabic text
    elements["app_name"] = preprocess_arabic_text(elements["app_name"])
    elements["main_activity_label"] = preprocess_arabic_text(elements["main_activity_label"])
    elements["welcome_message"] = preprocess_arabic_text(elements["welcome_message"])

    return elements

def generate_android_manifest(package_name, main_activity_label):
    """Generates the AndroidManifest.xml content."""
    manifest_template = load_template(MANIFEST_TEMPLATE_PATH)
    # Replace placeholders. Note: This is a very basic replacement.
    # A more robust solution would parse the XML and modify attributes/elements.
    manifest_content = manifest_template.replace("{{package_name}}", package_name)
    manifest_content = manifest_content.replace("{{main_activity_label}}", main_activity_label)
    return manifest_content

def generate_strings_xml(app_name, welcome_message):
    """Generates the strings.xml content."""
    strings_template = load_template(STRINGS_TEMPLATE_PATH)
    strings_content = strings_template.replace("{{app_name}}", app_name)
    strings_content = strings_content.replace("{{welcome_message}}", welcome_message)
    return strings_content

def generate_activity_layout(welcome_message):
    """Generates the activity_main.xml content."""
    layout_template = load_template(LAYOUT_TEMPLATE_PATH)
    # Assuming the welcome message is to be displayed in a TextView
    layout_content = layout_template.replace("{{welcome_message}}", welcome_message)
    return layout_content

class ArabicAPKGenerator:
    def __init__(self, natural_language_prompt):
        self.natural_language_prompt = natural_language_prompt
        self.project_dir = "arabic_app_project"
        self.app_src_dir = os.path.join(self.project_dir, "app", "src", "main")
        self.res_dir = os.path.join(self.app_src_dir, "res")
        self.layout_dir = os.path.join(self.res_dir, "layout")
        self.values_dir = os.path.join(self.res_dir, "values")
        self.manifest_path = os.path.join(self.app_src_dir, "AndroidManifest.xml")
        self.strings_path = os.path.join(self.values_dir, "strings.xml")
        self.layout_path = os.path.join(self.layout_dir, "activity_main.xml")
        self.apk_output_path = "output_arabic_app.apk"

    def setup_project_structure(self):
        """Creates the necessary directories for the Android project."""
        os.makedirs(self.layout_dir, exist_ok=True)
        os.makedirs(self.values_dir, exist_ok=True)
        print(f"Project structure created at: {self.project_dir}")

    def generate_apk_components(self):
        """Extracts information and generates Android resource files."""
        print("\n--- Extracting APK Components from Prompt ---")
        apk_elements = extract_apk_elements(self.natural_language_prompt)

        print("\n--- Generating Android Manifest ---")
        manifest_content = generate_android_manifest(
            apk_elements["package_name"],
            apk_elements["main_activity_label"]
        )
        save_file(manifest_content, self.manifest_path)

        print("\n--- Generating strings.xml ---")
        strings_content = generate_strings_xml(
            apk_elements["app_name"],
            apk_elements["welcome_message"]
        )
        save_file(strings_content, self.strings_path)

        print("\n--- Generating activity_main.xml ---")
        layout_content = generate_activity_layout(
            apk_elements["welcome_message"]
        )
        save_file(layout_content, self.layout_path)

        return apk_elements

    def synthesize_and_compile(self, apk_elements):
        """
        Synthesizes components and triggers compilation (simulated).
        In a real scenario, this would call Lobe 8_apk_compiler_lobe.
        """
        print("\n--- Synthesizing and Simulating Compilation ---")
        # This is a placeholder for Lobe 6_synthesis_lobe and Lobe 8_apk_compiler_lobe
        # It would involve taking the generated resources and code (if any)
        # and using a build tool (like Gradle) to create the APK.
        print("Simulating synthesis and compilation process...")
        print(f"App Name: {apk_elements['app_name']}")
        print(f"Package Name: {apk_elements['package_name']}")
        print(f"Main Activity Label: {apk_elements['main_activity_label']}")
        print(f"Welcome Message: {apk_elements['welcome_message']}")
        print(f"Generated resources are in: {self.project_dir}")
        print("Compilation would occur here, leading to a final APK.")
        print(f"Placeholder for generated APK: {self.apk_output_path}")

    def cleanup_project(self):
        """Cleans up the generated project directory."""
        print("\n--- Cleaning up project directory ---")
        if os.path.exists(self.project_dir):
            import shutil
            try:
                shutil.rmtree(self.project_dir)
                print(f"Removed project directory: {self.project_dir}")
            except Exception as e:
                print(f"Error removing project directory {self.project_dir}: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    # Ensure necessary resource templates exist
    if not os.path.exists(ARABIC_RESOURCE_DIR):
        os.makedirs(ARABIC_RESOURCE_DIR)
    if not os.path.exists(os.path.join(ARABIC_RESOURCE_DIR, "values")):
        os.makedirs(os.path.join(ARABIC_RESOURCE_DIR, "values"))
    if not os.path.exists(os.path.join(ARABIC_RESOURCE_DIR, "layout")):
        os.makedirs(os.path.join(ARABIC_RESOURCE_DIR, "layout"))

    # Create dummy template files if they don't exist
    if not os.path.exists(MANIFEST_TEMPLATE_PATH):
        with open(MANIFEST_TEMPLATE_PATH, "w", encoding="utf-8") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{{package_name}}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{{app_name}}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity"
            android:label="{{main_activity_label}}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")
        print(f"Created dummy template: {MANIFEST_TEMPLATE_PATH}")

    if not os.path.exists(STRINGS_TEMPLATE_PATH):
        with open(STRINGS_TEMPLATE_PATH, "w", encoding="utf-8") as f:
            f.write("""<resources>
    <string name="app_name">{{app_name}}</string>
    <string name="welcome_message">{{welcome_message}}</string>
</resources>
""")
        print(f"Created dummy template: {STRINGS_TEMPLATE_PATH}")

    if not os.path.exists(LAYOUT_TEMPLATE_PATH):
        with open(LAYOUT_TEMPLATE_PATH, "w", encoding="utf-8") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/welcome_message"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
        print(f"Created dummy template: {LAYOUT_TEMPLATE_PATH}")

    # Example usage of the ArabicAPKGenerator
    arabic_description = (
        "Create an Android app. The app name is 'تطبيقي العربي'. "
        "The main screen title should be 'الصفحة الرئيسية'. "
        "Display a welcome message: 'أهلاً بك في تطبيقي!'. "
        "The package name is 'com.example.myarabicapp'."
    )

    generator = ArabicAPKGenerator(arabic_description)
    generator.setup_project_structure()
    apk_elements = generator.generate_apk_components()
    generator.synthesize_and_compile(apk_elements)
    # generator.cleanup_project() # Uncomment to clean up after execution

    print("\n--- Arabic APK Generation Module Demo Finished ---")