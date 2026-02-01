import os
import shutil
import re

# --- Configuration ---
ARABIC_PARSING_DIR = "arabic_parsing_output"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
JAVA_CODE_DIR = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "generatedapp")
MANIFEST_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "AndroidManifest.xml")
GRADLE_PROPERTIES_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "gradle.properties")

# --- Helper Functions ---

def ensure_directory_exists(dir_path):
    """Ensures that a directory exists, creating it if necessary."""
    os.makedirs(dir_path, exist_ok=True)

def read_file(file_path):
    """Reads the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    """Writes content to a file."""
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_directory(dir_path):
    """Removes a directory and its contents if it exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

def generate_simple_activity_java(activity_name, package_name="com.example.generatedapp"):
    """Generates a basic Java Activity file content."""
    return f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()}); // Assumes layout file exists

        TextView welcomeText = findViewById(R.id.welcome_text);
        if (welcomeText != null) {{
            welcomeText.setText("Welcome to {activity_name}!");
        }}
    }}
}}
"""

def generate_simple_layout_xml(activity_name):
    """Generates a basic layout XML file content."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

def generate_manifest_entry(activity_name, package_name="com.example.generatedapp"):
    """Generates an AndroidManifest.xml entry for an activity."""
    return f"""
        <activity android:name=".{activity_name}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""

# --- Lobe 0_language_lobe / Lobe 3_arabic_processing_lobe ---
# This lobe is responsible for parsing Arabic natural language instructions
# and translating them into structured data that can be used to generate code.

class ArabicInstructionParser:
    """
    Parses Arabic natural language instructions to extract app features,
    screen names, and basic UI elements.
    """
    def __init__(self):
        pass

    def parse(self, arabic_text):
        """
        Parses Arabic text to identify app components.

        Args:
            arabic_text (str): The Arabic natural language instruction.

        Returns:
            dict: A dictionary containing parsed information, e.g.,
                  {'screens': [{'name': 'HomeScreen', 'elements': [...]}]}
        """
        parsed_data = {"screens": []}

        # Basic parsing logic: identify screen names and potential elements
        # This is a simplified example. A real-world parser would be much more complex,
        # potentially using NLP libraries like Farasa or CAMeL Tools for morphology,
        # named entity recognition, and dependency parsing.

        # Example: "إنشاء تطبيق يحتوي على شاشة رئيسية وشاشة تفاصيل"
        # -> {'screens': [{'name': 'HomeScreen'}, {'name': 'DetailsScreen'}]}

        screen_keywords = ["شاشة", "صفحة"]
        screen_match = re.search(r"إنشاء تطبيق يحتوي على (.*)", arabic_text)

        if screen_match:
            screens_str = screen_match.group(1)
            # Split by " و " (and) and potentially other conjunctions
            potential_screens = re.split(r'\s+و\s+', screens_str)
            for item in potential_screens:
                item = item.strip()
                for keyword in screen_keywords:
                    if keyword in item:
                        # Extract the name after the keyword, removing articles like "ال"
                        screen_name_part = item.replace(keyword, "").strip()
                        screen_name_part = re.sub(r'^ال', '', screen_name_part) # Remove "al-" prefix
                        if screen_name_part:
                            # Simple CamelCase conversion for activity names
                            activity_name = "".join(word.capitalize() for word in screen_name_part.split())
                            parsed_data["screens"].append({"name": activity_name, "elements": []})
                            break # Move to the next item once a screen is identified

        # Further parsing for UI elements within screens (e.g., buttons, text fields)
        # This would involve pattern matching for phrases like "زر باسم 'تسجيل الدخول'"
        # or "حقل نصي لـ 'اسم المستخدم'".

        return parsed_data

# --- Lobe 4_code_generation_lobe ---
# This lobe takes the structured data from the parser and generates
# Android project files (Java, XML, Manifest).

class AndroidCodeGenerator:
    """
    Generates Android project files (Java activities, layouts, Manifest)
    based on parsed instructions.
    """
    def __init__(self, base_project_template_dir, output_java_dir, output_manifest_path):
        self.base_project_template_dir = base_project_template_dir
        self.output_java_dir = output_java_dir
        self.output_manifest_path = output_manifest_path
        self.package_name = "com.example.generatedapp" # Default package name

    def create_project_structure(self):
        """Creates the basic directory structure for the Android project."""
        ensure_directory_exists(self.output_java_dir)
        # Create res/layout directory
        ensure_directory_exists(os.path.join(self.base_project_template_dir, "app", "src", "main", "res", "layout"))

    def generate_activity_files(self, screens_data):
        """Generates Java Activity files and corresponding layout XML files."""
        for screen in screens_data.get("screens", []):
            activity_name = screen.get("name")
            if not activity_name:
                continue

            # Generate Java Activity
            java_content = generate_simple_activity_java(activity_name, self.package_name)
            java_file_path = os.path.join(self.output_java_dir, f"{activity_name}.java")
            write_file(java_file_path, java_content)
            print(f"Generated Java Activity: {java_file_path}")

            # Generate Layout XML
            layout_content = generate_simple_layout_xml(activity_name)
            layout_file_path = os.path.join(self.base_project_template_dir, "app", "src", "main", "res", "layout", f"activity_{activity_name.lower()}.xml")
            write_file(layout_file_path, layout_content)
            print(f"Generated Layout XML: {layout_file_path}")

    def update_manifest(self, screens_data):
        """Updates the AndroidManifest.xml with new activities."""
        manifest_content = read_file(self.output_manifest_path)
        # Find the application tag to insert activity declarations
        app_tag_end_match = re.search(r"<application.*?>", manifest_content, re.DOTALL)
        if app_tag_end_match:
            insert_point = app_tag_end_match.end()
            activities_to_add = ""
            for screen in screens_data.get("screens", []):
                activity_name = screen.get("name")
                if activity_name:
                    # Avoid adding the LAUNCHER activity multiple times if it's the first screen
                    if not screens_data["screens"].index(screen) == 0:
                         # Remove LAUNCHER intent filter if not the first activity
                         activities_to_add += generate_manifest_entry(activity_name, self.package_name).replace('<intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>', '')
                    else:
                         activities_to_add += generate_manifest_entry(activity_name, self.package_name)


            # Ensure correct indentation and formatting for inserted activities
            formatted_activities = "\n".join([f"            {line.strip()}" for line in activities_to_add.strip().split('\n')])
            updated_manifest_content = manifest_content[:insert_point] + "\n" + formatted_activities + "\n" + manifest_content[insert_point:]

            # Clean up extra newlines introduced by insertion
            updated_manifest_content = re.sub(r'\n\s*\n', '\n', updated_manifest_content)

            write_file(self.output_manifest_path, updated_manifest_content)
            print(f"Updated AndroidManifest.xml")
        else:
            print("Error: Could not find <application> tag in AndroidManifest.xml")

    def run(self, screens_data):
        """Main method to generate the Android project structure and files."""
        print("\n--- Initiating Android Code Generation ---")
        self.create_project_structure()
        self.generate_activity_files(screens_data)
        self.update_manifest(screens_data)
        print("--- Android Code Generation Complete ---")

# --- Mock/Placeholder for Lobe 8_apk_compiler_lobe ---
class ApkCompiler:
    """Simulates the APK compilation process."""
    def __init__(self, project_dir):
        self.project_dir = project_dir

    def run(self, app_name="generated_app.apk"):
        """Simulates building an APK."""
        print(f"\n--- Simulating APK Compilation for '{app_name}' ---")
        # In a real scenario, this would involve calling Gradle or Android SDK tools.
        # For simulation, we just create a dummy file.
        simulated_apk_path = os.path.join(self.project_dir, app_name)
        # Create a dummy APK file
        with open(simulated_apk_path, 'w') as f:
            f.write("This is a simulated APK file.")
        print(f"Simulated APK created at: {simulated_apk_path}")
        print("--- APK Compilation Simulation Complete ---")
        return simulated_apk_path

# --- Helper Functions for Cleanup ---

def cleanup_android_project_template():
    """Cleans up the dummy Android project directory."""
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        print(f"\nCleaning up dummy project directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)

def cleanup_arabic_parsing_output():
    """Cleans up the Arabic parsing output directory."""
    if os.path.exists(ARABIC_PARSING_DIR):
        print(f"\nCleaning up Arabic parsing output directory: {ARABIC_PARSING_DIR}")
        shutil.rmtree(ARABIC_PARSING_DIR)

# --- Main Execution Logic ---

if __name__ == "__main__":
    # --- Mock Setup for Demonstration ---
    # In a real execution, these would be outputs from other lobes.

    # 1. Simulate Arabic Natural Language Input
    arabic_instruction = "إنشاء تطبيق يحتوي على شاشة رئيسية وشاشة إعدادات"
    print(f"Received Arabic instruction: '{arabic_instruction}'")

    # 2. Initialize and Run Lobe 3_arabic_processing_lobe (ArabicInstructionParser)
    arabic_parser = ArabicInstructionParser()
    parsed_app_data = arabic_parser.parse(arabic_instruction)
    print(f"\nParsed App Data: {parsed_app_data}")

    # 3. Initialize and Run Lobe 4_code_generation_lobe (AndroidCodeGenerator)
    #    We'll use the template directory and output paths directly here.
    #    Ensure the template directory and necessary sub-paths exist for the generator.
    #    In a real system, this template might be copied or managed differently.
    ensure_directory_exists(ANDROID_PROJECT_TEMPLATE_DIR)
    ensure_directory_exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "generatedapp"))
    ensure_directory_exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout"))

    # Create a dummy AndroidManifest.xml if it doesn't exist
    if not os.path.exists(MANIFEST_PATH):
        dummy_manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.generatedapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp">
        <!-- Activities will be added here -->
    </application>

</manifest>
"""
        write_file(MANIFEST_PATH, dummy_manifest_content)

    # Create a dummy gradle.properties if it doesn't exist
    if not os.path.exists(GRADLE_PROPERTIES_PATH):
        dummy_gradle_properties = "org.gradle.jvmargs=-Xmx2048m\n"
        write_file(GRADLE_PROPERTIES_PATH, dummy_gradle_properties)

    code_generator = AndroidCodeGenerator(
        base_project_template_dir=ANDROID_PROJECT_TEMPLATE_DIR,
        output_java_dir=os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "generatedapp"),
        output_manifest_path=MANIFEST_PATH
    )
    code_generator.run(parsed_app_data)

    # 4. Initialize and Run Lobe 8_apk_compiler_lobe (ApkCompiler - Simulated)
    apk_compiler = ApkCompiler(project_dir=ANDROID_PROJECT_TEMPLATE_DIR)
    generated_apk_path = apk_compiler.run(app_name="my_generated_app.apk")
    print(f"\nSimulated APK generation process finished. Output: {generated_apk_path}")

    # 5. Cleanup
    print("\n--- Cleaning up ---")
    cleanup_android_project_template()
    # No specific output dir for arabic_parser in this setup, but keep for general cleanup
    # cleanup_arabic_parsing_output()

    print("\n--- Full Module Demo Finished ---")