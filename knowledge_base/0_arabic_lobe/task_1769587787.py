import os
import shutil
from pathlib import Path
from typing import List

# Define the directory for knowledge base (assuming it's in the same directory as the script)
KNOWLEDGE_BASE_DIR = Path(__file__).parent / "knowledge_base"
if not KNOWLEDGE_BASE_DIR.exists():
    KNOWLEDGE_BASE_DIR.mkdir()

def generate_arabic_code_structure(project_name: str, package_name: str, activities: List[str]) -> Path:
    """
    Generates the basic directory and file structure for an Android project
    written in Arabic.

    Args:
        project_name: The name of the Android project.
        package_name: The package name for the Android application.
        activities: A list of activity names to be created.

    Returns:
        The path to the root of the generated project structure.
    """
    project_root = Path(project_name)
    if project_root.exists():
        shutil.rmtree(project_root)
    project_root.mkdir()

    # Create app directory
    app_dir = project_root / "app"
    app_dir.mkdir()

    # Create source directory
    src_dir = app_dir / "src"
    src_dir.mkdir()

    # Create main directory
    main_dir = src_dir / "main"
    main_dir.mkdir()

    # Create AndroidManifest.xml
    manifest_path = main_dir / "AndroidManifest.xml"
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{project_name}">
        
        <!-- Activities will be added here -->
    </application>
</manifest>
"""
    manifest_path.write_text(manifest_content, encoding='utf-8')

    # Create java directory structure
    java_dir = main_dir / "java"
    package_path = java_dir
    for part in package_name.split('.'):
        package_path = package_path / part
    package_path.mkdir(parents=True)

    # Create strings.xml
    res_dir = main_dir / "res"
    values_dir = res_dir / "values"
    values_dir.mkdir(parents=True)
    strings_path = values_dir / "strings.xml"
    strings_content = f"""<resources>
    <string name="app_name">{project_name}</string>
</resources>
"""
    strings_path.write_text(strings_content, encoding='utf-8')

    # Create styles.xml
    styles_path = values_dir / "styles.xml"
    styles_content = f"""<resources>
    <!-- Base application theme. -->
    <style name="Theme.{project_name}" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <!-- Primary brand color. -->
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
        <!-- Customize your theme here. -->
    </style>
</resources>
"""
    styles_path.write_text(styles_content, encoding='utf-8')

    # Create colors.xml
    colors_path = values_dir / "colors.xml"
    colors_content = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
    colors_path.write_text(colors_content, encoding='utf-8')


    # Create dummy launcher icon and background
    mipmap_dir = res_dir / "mipmap-hdpi"
    mipmap_dir.mkdir(parents=True)
    (mipmap_dir / "ic_launcher.webp").touch()
    (mipmap_dir / "ic_launcher_round.webp").touch()

    # Generate Activity files
    for activity_name in activities:
        activity_class_name = f"{activity_name.capitalize()}Activity"
        activity_file_path = package_path / f"{activity_class_name}.java"
        activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_class_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Set layout for this activity (e.g., setContentView(R.layout.{activity_name.lower()}));
        // For now, we'll just print a message.
        System.out.println("تم إنشاء النشاط: {activity_class_name}");
    }}
}}
"""
        activity_file_path.write_text(activity_content, encoding='utf-8')

        # Add activity to AndroidManifest.xml
        manifest_content = manifest_path.read_text(encoding='utf-8')
        application_tag_end = manifest_content.rfind("</application>")
        activity_declaration = f'\n        <activity android:name=".{activity_class_name}" />'
        manifest_content = manifest_content[:application_tag_end] + activity_declaration + manifest_content[application_tag_end:]
        manifest_path.write_text(manifest_content, encoding='utf-8')

    print(f"تم إنشاء هيكل مشروع Android في: {project_root.resolve()}")
    return project_root

def generate_arabic_language_module(project_name: str, language_code: str = "ar"):
    """
    This module would be responsible for handling language-specific resources
    and potentially localized UI elements. For this example, it will create
    a basic Arabic resources directory.

    Args:
        project_name: The name of the Android project.
        language_code: The ISO language code (e.g., "ar" for Arabic).
    """
    project_root = Path(project_name)
    if not project_root.exists():
        print(f"Project root '{project_name}' does not exist. Please create the project first.")
        return

    res_dir = project_root / "app" / "src" / "main" / "res"
    if not res_dir.exists():
        res_dir.mkdir(parents=True)

    # Create language-specific values directory
    language_values_dir = res_dir / f"values-{language_code}"
    language_values_dir.mkdir(parents=True)

    # Create strings.xml for Arabic
    arabic_strings_path = language_values_dir / "strings.xml"
    arabic_strings_content = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{project_name} (عربي)</string>
    <string name="welcome_message">أهلاً بك في تطبيقنا!</string>
</resources>
"""
    arabic_strings_path.write_text(arabic_strings_content, encoding='utf-8')

    print(f"تم إنشاء موارد اللغة العربية في: {language_values_dir.resolve()}")

if __name__ == '__main__':
    # Example Usage:
    project_name = "MyArabicApp"
    package_name = "com.example.myarabicapp"
    activities = ["main", "settings"]

    print("--- Generating Arabic Android Project Structure ---")
    generated_project_path = generate_arabic_code_structure(project_name, package_name, activities)

    print("\n--- Generating Arabic Language Module ---")
    generate_arabic_language_module(project_name, "ar")

    print("\n--- Demonstrating basic NLP integration (simulated) ---")
    # In a real scenario, Lobe 0_language_lobe would process natural language input.
    # Here, we simulate the output of such processing.
    natural_language_input = "إنشاء واجهة بها زر وزر تبديل" # "Create an interface with a button and a toggle button"
    print(f"Input natural language: '{natural_language_input}'")

    # Simulate what Lobe 0_language_lobe might interpret and pass to Lobe 6_synthesis_lobe
    # For instance, it might identify UI components and their desired properties.
    interpreted_ui_elements = {
        "button": ["OK", "Cancel"],
        "toggle_button": ["Enable Feature"]
    }
    print(f"Simulated interpretation: {interpreted_ui_elements}")

    # This simulated interpreted_ui_elements would then be passed to Lobe 6_synthesis_lobe
    # to generate layout XML, code for event handling, etc.
    # For now, we'll just acknowledge the output.
    print("This interpreted data would be fed to Lobe 6_synthesis_lobe for further processing.")

    print("\n--- Arabic Language Module Demo Finished ---")

    # Cleanup for potential re-runs
    print("\n--- Cleaning up demo project ---")
    if Path(project_name).exists():
        shutil.rmtree(project_name)
        print(f"Removed project directory: {project_name}")