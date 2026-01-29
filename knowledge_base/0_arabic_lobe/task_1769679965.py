import os
import shutil
from pathlib import Path
import subprocess

# Assume these are defined elsewhere and accessible
# For demonstration, let's define them as placeholders
DEMO_PROJECT_BASE_DIR = Path("./arabic_demo_project")
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")

def setup_dummy_project(base_dir: Path, project_name: str = "SampleArabicApp"):
    """Sets up a dummy project structure for an Arabic Android app."""
    project_path = base_dir / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    # Create a dummy AndroidManifest.xml
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.arabicapp">

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
"""
    (project_path / "AndroidManifest.xml").write_text(manifest_content, encoding='utf-8')

    # Create dummy Java/Kotlin source directory and a simple MainActivity
    src_dir = project_path / "app" / "src" / "main" / "java" / "com" / "example" / "arabicapp"
    src_dir.mkdir(parents=True, exist_ok=True)
    main_activity_content = """package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView greetingTextView = findViewById(R.id.greetingTextView);
        greetingTextView.setText(R.string.welcome_message); // Placeholder for Arabic string
    }
}
"""
    (src_dir / "MainActivity.java").write_text(main_activity_content, encoding='utf-8')

    # Create dummy res directory with strings.xml
    res_dir = project_path / "app" / "src" / "main" / "res"
    res_dir.mkdir(parents=True, exist_ok=True)
    values_dir = res_dir / "values"
    values_dir.mkdir(parents=True, exist_ok=True)
    strings_content = """<resources>
    <string name="app_name">تطبيق عربي</string>
    <string name="welcome_message">أهلاً بك في التطبيق!</string>
</resources>
"""
    (values_dir / "strings.xml").write_text(strings_content, encoding='utf-8')

    # Create dummy layout file
    layout_dir = res_dir / "layout"
    layout_dir.mkdir(parents=True, exist_ok=True)
    activity_main_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/greetingTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    (layout_dir / "activity_main.xml").write_text(activity_main_content, encoding='utf-8')

    return project_path

def clean_up_dummy_project(project_path: Path):
    """Removes the dummy project directory."""
    if project_path.exists():
        print(f"Removing dummy project directory: {project_path}")
        shutil.rmtree(project_path)

class ArabicNLPIntegration:
    """
    Lobe 7: Integrates Arabic NLP processing into the APK generation pipeline.
    This lobe focuses on understanding and generating Arabic text for UI elements,
    resource files, and potentially code comments or string literals.
    """

    def __init__(self):
        pass

    def analyze_arabic_prompt(self, natural_language_prompt: str) -> dict:
        """
        Analyzes an Arabic natural language prompt to extract intents, entities,
        and desired outcomes for APK generation.

        Args:
            natural_language_prompt: The Arabic prompt from the user.

        Returns:
            A dictionary containing parsed information:
            - 'intent': The user's goal (e.g., "create_screen", "add_button").
            - 'entities': Key information extracted (e.g., screen name, button text).
            - 'ui_elements': Specific UI components requested.
            - 'text_content': Arabic text for UI elements or resources.
        """
        print(f"Analyzing Arabic prompt: '{natural_language_prompt}'")
        # This is a placeholder for actual Arabic NLP analysis.
        # In a real implementation, this would involve a sophisticated Arabic NLP model.
        # For demonstration, we'll use simple keyword matching.
        parsed_data = {
            "intent": "unknown",
            "entities": {},
            "ui_elements": [],
            "text_content": {}
        }

        if "إنشاء شاشة" in natural_language_prompt or "create screen" in natural_language_prompt:
            parsed_data["intent"] = "create_screen"
            parts = natural_language_prompt.split("اسمها")
            if len(parts) > 1:
                screen_name = parts[1].strip().replace("'", "").replace('"', '')
                parsed_data["entities"]["screen_name"] = screen_name
                parsed_data["text_content"][f"screen_title_{screen_name}"] = f"عنوان {screen_name}"
        elif "إضافة زر" in natural_language_prompt or "add button" in natural_language_prompt:
            parsed_data["intent"] = "add_button"
            parts = natural_language_prompt.split("نص الزر")
            if len(parts) > 1:
                button_text = parts[1].strip().replace("'", "").replace('"', '')
                parsed_data["entities"]["button_text"] = button_text
                parsed_data["ui_elements"].append({"type": "button", "text": button_text})
                parsed_data["text_content"]["button_action"] = button_text # Example: button action text

        # Extract general Arabic text for strings.xml
        if "اكتب" in natural_language_prompt:
            parts = natural_language_prompt.split("اكتب")
            if len(parts) > 1:
                text_to_add = parts[1].strip().replace("'", "").replace('"', '')
                parsed_data["text_content"]["general_message"] = text_to_add

        # Default to a welcome message if no specific text is found
        if not parsed_data["text_content"]:
            parsed_data["text_content"]["default_welcome"] = "أهلاً بك!"

        print(f"Parsed data: {parsed_data}")
        return parsed_data

    def generate_arabic_resources(self, parsed_data: dict, project_dir: Path) -> Path:
        """
        Generates or updates Android resource files (e.g., strings.xml)
        with Arabic content based on the parsed data.

        Args:
            parsed_data: The dictionary returned by analyze_arabic_prompt.
            project_dir: The root directory of the Android project.

        Returns:
            The path to the updated strings.xml file.
        """
        strings_xml_path = project_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        strings_xml_path.parent.mkdir(parents=True, exist_ok=True)

        existing_content = ""
        if strings_xml_path.exists():
            existing_content = strings_xml_path.read_text(encoding='utf-8')

        # A simple way to merge new strings. In a real scenario, proper XML parsing and merging would be needed.
        new_strings = []
        for key, value in parsed_data.get("text_content", {}).items():
            new_strings.append(f'    <string name="{key}">{value}</string>')

        if not new_strings:
            print("No new strings to add to strings.xml.")
            return strings_xml_path

        # Basic XML structure - assumes it's either empty or has a basic <resources> tag
        if "<resources>" not in existing_content:
            final_content = "<resources>\n"
        else:
            # Remove existing <resources> tag to re-insert with new content
            existing_content = existing_content.replace("<resources>", "").replace("</resources>", "").strip()
            final_content = "<resources>\n"

        # Add existing strings if any, avoiding duplicates if possible (simple check)
        all_lines = existing_content.splitlines() + new_strings
        unique_lines = []
        seen_names = set()
        for line in all_lines:
            if line.strip().startswith("<string name="):
                name_start = line.find('name="') + 6
                name_end = line.find('"', name_start)
                if name_start != -1 and name_end != -1:
                    name = line[name_start:name_end]
                    if name not in seen_names:
                        unique_lines.append(line.strip())
                        seen_names.add(name)
                else:
                    unique_lines.append(line.strip()) # Handle lines that are not string definitions
            else:
                unique_lines.append(line.strip())

        # Add new strings if they are not already present (based on the simple seen_names logic)
        for new_string in new_strings:
            name_start = new_string.find('name="') + 6
            name_end = new_string.find('"', name_start)
            if name_start != -1 and name_end != -1:
                name = new_string[name_start:name_end]
                if name not in seen_names:
                    unique_lines.append(new_string.strip())
                    seen_names.add(name)


        final_content += "\n".join(unique_lines)
        final_content += "\n</resources>"

        strings_xml_path.write_text(final_content, encoding='utf-8')
        print(f"Updated {strings_xml_path}")
        return strings_xml_path

    def adapt_ui_for_arabic(self, parsed_data: dict, project_dir: Path):
        """
        Adjusts UI layouts and code based on Arabic language requirements
        (e.g., RTL support, text direction).

        Args:
            parsed_data: The dictionary returned by analyze_arabic_prompt.
            project_dir: The root directory of the Android project.
        """
        print("Adapting UI for Arabic...")
        # This is a placeholder. Real implementation would involve:
        # 1. Modifying layout XMLs to support RTL (e.g., using start/end instead of left/right).
        # 2. Potentially adjusting text views for Arabic script properties.
        # 3. Generating new UI components if requested.

        # Example: If a new screen was requested, create a basic layout and activity.
        screen_name = parsed_data.get("entities", {}).get("screen_name")
        if screen_name:
            activity_name = screen_name.capitalize()
            package_path = project_dir / "app" / "src" / "main" / "java" / "com" / "example" / "arabicapp"
            package_path.mkdir(parents=True, exist_ok=True)

            # Create Java Activity
            activity_content = f"""package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{screen_name.lower()}); // Assumes layout file name is lowercase screen_name

        // Example: Set a title or welcome message for the new screen
        TextView screenTitleTextView = findViewById(R.id.screenTitleTextView); // Assuming a TextView with this ID exists
        screenTitleTextView.setText(R.string.title_{screen_name.lower()}); // Assumes a string resource is defined
    }}
}}
"""
            (package_path / f"{activity_name}.java").write_text(activity_content, encoding='utf-8')
            print(f"Created Java activity: {activity_name}.java")

            # Create Layout XML
            layout_path = project_dir / "app" / "src" / "main" / "res" / "layout" / f"{screen_name.lower()}.xml"
            layout_path.parent.mkdir(parents=True, exist_ok=True)
            layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/screenTitleTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/title_{screen_name.lower()}"
        android:textSize="20sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>

    <!-- Other UI elements for the screen can be added here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
            layout_path.write_text(layout_content, encoding='utf-8')
            print(f"Created layout file: {screen_name.lower()}.xml")

            # Update strings.xml for the new screen title
            strings_update_data = {"text_content": {f"title_{screen_name.lower()}": f"صفحة {screen_name}"}}
            self.generate_arabic_resources(strings_update_data, project_dir)


        # Example: Add a button if requested
        ui_elements = parsed_data.get("ui_elements", [])
        for element in ui_elements:
            if element.get("type") == "button":
                button_text = element.get("text", "زر")
                # This would require modifying the current activity's layout or a specified one.
                # For simplicity, we'll assume modification of activity_main.xml
                activity_main_layout_path = project_dir / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
                if activity_main_layout_path.exists():
                    layout_content = activity_main_layout_path.read_text(encoding='utf-8')
                    # Simple insertion before the closing ConstraintLayout tag
                    insert_point = layout_content.rfind("</androidx.constraintlayout.widget.ConstraintLayout>")
                    if insert_point != -1:
                        button_id = f"button_{button_text.replace(' ', '_').lower()}"
                        # Using a placeholder string name that will be handled by generate_arabic_resources
                        new_button_xml = f"""
    <Button
        android:id="@+id/{button_id}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/{button_id}"
        app:layout_constraintTop_toBottomOf="@id/greetingTextView"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>"""
                        layout_content = layout_content[:insert_point] + new_button_xml + layout_content[insert_point:]
                        activity_main_layout_path.write_text(layout_content, encoding='utf-8')
                        print(f"Added button to activity_main.xml with text: '{button_text}'")
                        # Add string resource for the button text
                        strings_update_data = {"text_content": {button_id: button_text}}
                        self.generate_arabic_resources(strings_update_data, project_dir)
                else:
                    print(f"Could not find {activity_main_layout_path} to add button.")


        print("UI Adaptation for Arabic complete (simulated).")


    def process_prompt(self, natural_language_prompt: str, project_dir: Path) -> dict:
        """
        Orchestrates the Arabic NLP integration process.

        Args:
            natural_language_prompt: The Arabic natural language input.
            project_dir: The directory where the Android project is or will be created.

        Returns:
            A dictionary containing the results of the integration,
            including generated resources and potential code modifications.
        """
        print("\n--- Lobe 7: Arabic NLP Integration Module ---")
        parsed_data = self.analyze_arabic_prompt(natural_language_prompt)
        generated_resources_path = self.generate_arabic_resources(parsed_data, project_dir)
        self.adapt_ui_for_arabic(parsed_data, project_dir)

        print("--- Arabic NLP Integration Module Finished ---")
        return {
            "parsed_data": parsed_data,
            "generated_resources_path": str(generated_resources_path)
        }

# --- Demo Usage ---
if __name__ == "__main__":
    print("--- Starting Lobe 7: Arabic NLP Integration Module Demo ---")

    # Setup a dummy project structure
    if DEMO_PROJECT_BASE_DIR.exists():
        shutil.rmtree(DEMO_PROJECT_BASE_DIR)
    DEMO_PROJECT_BASE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Created dummy project base directory: {DEMO_PROJECT_BASE_DIR}")

    # Create an initial dummy project
    initial_project_path = setup_dummy_project(DEMO_PROJECT_BASE_DIR, "InitialArabicApp")
    print(f"Initial dummy project created at: {initial_project_path}")

    arabic_nlp_integrator = ArabicNLPIntegration()

    # Example 1: Creating a new screen and adding text
    prompt_1 = "يا مساعد، قم بإنشاء شاشة جديدة اسمها 'معلومات' واكتب فيها 'هذه صفحة المعلومات الخاصة بالتطبيق'."
    print(f"\nProcessing prompt 1: {prompt_1}")
    result_1 = arabic_nlp_integrator.process_prompt(prompt_1, initial_project_path)
    print(f"Lobe 7 Result 1: {result_1}")

    # Example 2: Adding a button with specific text
    prompt_2 = "الرجاء إضافة زر إلى الشاشة الرئيسية بنص 'اضغط هنا'."
    print(f"\nProcessing prompt 2: {prompt_2}")
    result_2 = arabic_nlp_integrator.process_prompt(prompt_2, initial_project_path)
    print(f"Lobe 7 Result 2: {result_2}")

    # Example 3: Just adding some general text to resources
    prompt_3 = "أضف النص التالي إلى موارد التطبيق: 'تحذير: استخدام غير صحيح قد يؤدي إلى مشاكل.'"
    print(f"\nProcessing prompt 3: {prompt_3}")
    result_3 = arabic_nlp_integrator.process_prompt(prompt_3, initial_project_path)
    print(f"Lobe 7 Result 3: {result_3}")


    # Clean up dummy project
    print("\n--- Cleaning up dummy project ---")
    clean_up_dummy_project(DEMO_PROJECT_BASE_DIR)

    print("\n--- Lobe 7: Arabic NLP Integration Module Demo Finished ---")