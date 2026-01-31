import os
import shutil
import subprocess
import re

# --- Constants ---
KNOWLEDGE_BASE_DIR = "knowledge_base"
TEMP_PROJECT_DIR = "temp_android_project"
APK_OUTPUT_DIR = "apks"

# --- Helper Functions ---

def ensure_directory_exists(dir_path):
    """Ensures a directory exists, creating it if necessary."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

def cleanup_directory(dir_path):
    """Removes a directory and its contents if it exists."""
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
            print(f"Cleaned up directory: {dir_path}")
        except OSError as e:
            print(f"Error cleaning up directory {dir_path}: {e}")

def generate_android_manifest(package_name, app_name, activities):
    """Generates a basic AndroidManifest.xml content."""
    activity_declarations = ""
    for activity in activities:
        activity_declarations += f'        <activity android:name=".{activity["name"]}" android:label="{activity.get("label", activity["name"])}">\n'
        if activity.get("intent_filters"):
            activity_declarations += "            <intent-filter>\n"
            for intent_filter in activity["intent_filters"]:
                if intent_filter.get("action"):
                    activity_declarations += f'                <action android:name="android.intent.action.{intent_filter["action"]}" />\n'
                if intent_filter.get("category"):
                    activity_declarations += f'                <category android:name="android.intent.category.{intent_filter["category"]}" />\n'
            activity_declarations += "            </intent-filter>\n"
        activity_declarations += "        </activity>\n"

    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:label="{app_name}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
{activity_declarations}
    </application>
</manifest>
"""
    return manifest_content

def generate_activity_java_code(activity_name, layout_name, onCreate_logic=""):
    """Generates basic Java code for an Android Activity."""
    java_content = f"""
package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{layout_name.lower()}); // Assuming layout file is activity_layout_name.xml

        // Add custom onCreate logic here
{onCreate_logic}
    }}
}}
"""
    return java_content

def generate_string_resource(app_name):
    """Generates basic strings.xml content."""
    strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    return strings_content

def generate_layout_xml(layout_name, content=""):
    """Generates basic layout XML content."""
    layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.capitalize()}">

    <!-- Add UI elements here -->
{content}
</androidx.constraintlayout.widget.ConstraintLayout>
"""
    return layout_content

def parse_arabic_description_for_app_structure(arabic_description):
    """
    Parses an Arabic description to extract app structure:
    app name, package name, activities, and their configurations.
    This is a simplified parser. A real implementation would require
    more sophisticated NLP for robust understanding.
    """
    app_name = "MyGeneratedApp"
    package_name = "com.example.generatedapp"
    activities = []

    # Basic regex to find app name and package name if explicitly mentioned
    app_name_match = re.search(r"اسم التطبيق هو (.+?)[،.\n]", arabic_description)
    if app_name_match:
        app_name = app_name_match.group(1).strip()

    package_match = re.search(r"اسم الحزمة هو (.+?)[،.\n]", arabic_description)
    if package_match:
        package_name = package_match.group(1).strip()

    # Parse activities. Expecting phrases like "نشاط اسمه ... يستخدم تخطيط ...",
    # "له واجهة رئيسية ...", "ينتقل إلى نشاط ...", etc.
    activity_sections = re.split(r"نشاط اسمه", arabic_description)[1:]

    for section in activity_sections:
        activity_name_match = re.search(r"(.+?)[،.\n]", section)
        if not activity_name_match:
            continue
        current_activity_name = activity_name_match.group(1).strip()
        current_activity_config = {"name": current_activity_name.capitalize()}
        layout_name = current_activity_name.lower().replace(" ", "_") # Default layout name

        layout_match = re.search(r"يستخدم تخطيط (.+?)[،.\n]", section)
        if layout_match:
            layout_name = layout_match.group(1).strip().lower().replace(" ", "_")
        current_activity_config["layout"] = layout_name

        intent_filters = []
        if "واجهة رئيسية" in section or "الشاشة الرئيسية" in section:
            intent_filters.append({"action": "MAIN", "category": "LAUNCHER"})
        current_activity_config["intent_filters"] = intent_filters

        # Simple parsing for UI elements in layout
        ui_elements_content = ""
        ui_match = re.search(r"يحتوي على (.+?)[،.\n]", section)
        if ui_match:
            ui_description = ui_match.group(1).strip()
            # Extremely basic parsing: if it mentions 'زر' (button), add a button.
            if "زر" in ui_description:
                ui_elements_content += """
    <Button
        android:id="@+id/myButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"/>
"""
            if "نص" in ui_description:
                ui_elements_content += """
    <TextView
        android:id="@+id/myTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintTop_toBottomOf="@id/myButton"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>
"""

        current_activity_config["layout_content"] = ui_elements_content

        # Parse transitions to other activities (simplified)
        transition_match = re.search(r"ينتقل إلى نشاط (.+?)[،.\n]", section)
        if transition_match:
            target_activity_name = transition_match.group(1).strip().capitalize()
            # We assume the target activity is also defined or will be.
            # In a real scenario, this would require linking defined activities.
            # For now, we just add a placeholder intent filter for navigation.
            current_activity_config["intent_filters"].append({
                "action": "NAVIGATE_TO",
                "category": target_activity_name
            })

        activities.append(current_activity_config)

    # Ensure a main activity exists if none were explicitly defined as launcher
    if not any(act.get("intent_filters") and "MAIN" in [i.get("action") for i in act.get("intent_filters", [])] for act in activities):
        main_activity_found = False
        for act in activities:
            if act["name"] == "MainActivity":
                act["intent_filters"].append({"action": "MAIN", "category": "LAUNCHER"})
                main_activity_found = True
                break
        if not main_activity_found:
            activities.insert(0, {"name": "MainActivity", "layout": "main", "label": app_name, "intent_filters": [{"action": "MAIN", "category": "LAUNCHER"}], "layout_content": ""})


    return {
        "app_name": app_name,
        "package_name": package_name,
        "activities": activities
    }


class Lobe3ArabicParser:
    """
    Lobe 3: Arabic Parser Module
    Responsible for understanding Arabic natural language descriptions
    and extracting information relevant to Android application structure.
    """

    def __init__(self):
        self.knowledge_base_dir = KNOWLEDGE_BASE_DIR
        self.temp_project_dir = TEMP_PROJECT_DIR
        ensure_directory_exists(self.knowledge_base_dir)
        ensure_directory_exists(self.temp_project_dir)

    def parse_description(self, arabic_description_text):
        """
        Processes the Arabic natural language description to generate
        an intermediate representation of the app structure.

        Args:
            arabic_description_text (str): The Arabic text describing the app.

        Returns:
            dict: A dictionary containing the parsed app structure
                  (app_name, package_name, activities, etc.).
        """
        print(f"\n--- Initiating Lobe 3: Arabic Parser ---")
        print(f"Parsing Arabic description for app structure...")

        # In a real scenario, this would involve sophisticated NLP models.
        # For this example, we use a simplified parser.
        parsed_structure = parse_arabic_description_for_app_structure(arabic_description_text)

        print(f"Successfully parsed app structure:")
        print(f"  App Name: {parsed_structure.get('app_name')}")
        print(f"  Package Name: {parsed_structure.get('package_name')}")
        print(f"  Number of Activities: {len(parsed_structure.get('activities', []))}")
        for i, activity in enumerate(parsed_structure.get('activities', [])):
            print(f"    Activity {i+1}: Name='{activity['name']}', Layout='{activity['layout']}'")

        # Store the parsed structure in the knowledge base (mocked)
        # In a real system, this would be saved to a file or database.
        print(f"Storing parsed structure in knowledge base (mocked)...")

        print(f"--- Lobe 3: Arabic Parser Finished ---")
        return parsed_structure

    def cleanup(self):
        """Cleans up temporary directories created by this lobe."""
        print(f"\n--- Cleaning up Lobe 3 temporary directories ---")
        cleanup_directory(self.temp_project_dir)
        print(f"--- Lobe 3 Cleanup Finished ---")

# --- Example Usage (for testing Lobe 3) ---
if __name__ == "__main__":
    arabic_prompt = """
    أنشئ تطبيق أندرويد. اسم التطبيق هو "حاسبة بسيطة".
    اسم الحزمة هو "com.example.simplecalculator".
    يجب أن يحتوي التطبيق على نشاط اسمه "Main" يستخدم تخطيط "main_layout".
    هذا النشاط يجب أن يكون الواجهة الرئيسية للتطبيق.
    النشاط "Main" يجب أن يحتوي على زر ونص.
    أضف نشاطاً آخر اسمه "Result" يستخدم تخطيط "result_layout".
    النشاط "Result" يجب أن يعرض نتيجة العملية الحسابية.
    عند الضغط على زر في النشاط "Main"، يجب أن ينتقل إلى نشاط "Result".
    """

    parser = Lobe3ArabicParser()
    app_structure = parser.parse_description(arabic_prompt)

    # Simulate interaction with Lobe 4 (Code Generation)
    print("\n--- Simulating interaction with Lobe 4 (Code Generation) ---")
    # This part would be handled by Lobe 4. We are just demonstrating
    # what Lobe 3 produces that Lobe 4 would consume.

    # Lobe 3's output (app_structure) would be fed into Lobe 4.
    # For demonstration, let's print the structure again.
    print("\nParsed structure ready for Lobe 4:")
    print(app_structure)

    # --- Simulate Lobe 4 and Lobe 8 based on Lobe 3's output ---
    print("\n--- Simulating Lobe 4 (Code Generation) and Lobe 8 (APK Compiler) ---")

    # Basic setup for simulated Lobe 4 and Lobe 8
    ensure_directory_exists(TEMP_PROJECT_DIR)
    ensure_directory_exists(APK_OUTPUT_DIR)

    package_name = app_structure["package_name"]
    app_name = app_structure["app_name"]
    activities_data = app_structure["activities"]

    # Create AndroidManifest.xml
    manifest_content = generate_android_manifest(package_name, app_name, activities_data)
    manifest_path = os.path.join(TEMP_PROJECT_DIR, "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"Generated {manifest_path}")

    # Create Java source files
    java_dir = os.path.join(TEMP_PROJECT_DIR, "src", "main", "java", *package_name.split('.'))
    ensure_directory_exists(java_dir)
    for activity in activities_data:
        activity_name = activity["name"]
        layout_name = activity["layout"]
        onCreate_logic = ""
        if activity_name == "Main":
             # Add mock onCreate logic for button click to navigate
             onCreate_logic = """
        Button myButton = findViewById(R.id.myButton);
        TextView myTextView = findViewById(R.id.myTextView);
        myTextView.setText("Hello from Arabic Parser!");

        myButton.setOnClickListener(v -> {
            // Navigate to Result activity (simplified)
            Intent intent = new Intent(this, Result.class);
            startActivity(intent);
        });
"""
        java_code = generate_activity_java_code(activity_name, layout_name, onCreate_logic)
        java_file_path = os.path.join(java_dir, f"{activity_name}.java")
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(java_code)
        print(f"Generated {java_file_path}")

    # Create resource files (strings.xml, layouts)
    res_dir = os.path.join(TEMP_PROJECT_DIR, "src", "main", "res")
    layout_dir = os.path.join(res_dir, "layout")
    values_dir = os.path.join(res_dir, "values")
    ensure_directory_exists(layout_dir)
    ensure_directory_exists(values_dir)

    # strings.xml
    strings_content = generate_string_resource(app_name)
    strings_file_path = os.path.join(values_dir, "strings.xml")
    with open(strings_file_path, "w", encoding="utf-8") as f:
        f.write(strings_content)
    print(f"Generated {strings_file_path}")

    # Layout XML files
    for activity in activities_data:
        layout_name = activity["layout"]
        layout_content = activity.get("layout_content", "")
        layout_xml_content = generate_layout_xml(layout_name, layout_content)
        layout_file_path = os.path.join(layout_dir, f"activity_{layout_name}.xml")
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_xml_content)
        print(f"Generated {layout_file_path}")

    # Mocking APK compilation (in a real scenario, this would invoke Gradle)
    print("\n--- Mocking APK Compilation ---")
    # In a real scenario, you would call Gradle build commands here:
    # subprocess.run(['gradle', 'assembleDebug'], cwd=TEMP_PROJECT_DIR)
    # For this mock, we'll just create a dummy APK file.

    # Assume a successful build creates an APK in a build/outputs/apk/debug directory
    mock_apk_path = os.path.join(TEMP_PROJECT_DIR, "app", "build", "outputs", "apk", "debug", f"{app_name.lower().replace(' ', '')}-debug.apk")
    ensure_directory_exists(os.path.dirname(mock_apk_path))
    with open(mock_apk_path, "w") as f:
        f.write("This is a mock APK file.")
    print(f"Mock APK created at: {mock_apk_path}")

    # Simulate moving the APK to the final output directory
    final_apk_name = f"{app_name.lower().replace(' ', '')}-release.apk"
    final_apk_path = os.path.join(APK_OUTPUT_DIR, final_apk_name)
    shutil.copy(mock_apk_path, final_apk_path)
    print(f"APK moved to final output: {final_apk_path}")

    print("\n--- Lobe 3, 4, and 8 Simulation Finished ---")

    # Clean up
    parser.cleanup()
    cleanup_directory(TEMP_PROJECT_DIR)
    cleanup_directory(APK_OUTPUT_DIR)