import os
import logging
import shutil
from pathlib import Path

# Assume these are defined elsewhere and represent core functionalities
# For this example, we'll create placeholder functions
def parse_arabic_intent(natural_language_input: str) -> dict:
    """
    Parses Arabic natural language input to extract intent and parameters
    for APK generation.
    """
    logging.info(f"Parsing Arabic intent for: '{natural_language_input}'")
    # In a real scenario, this would involve NLP models, dictionaries, etc.
    # For demonstration, we'll return a simplified structure.
    if "create an app named" in natural_language_input:
        app_name_parts = natural_language_input.split("create an app named")
        if len(app_name_parts) > 1:
            app_name = app_name_parts[1].strip().replace("'", "").replace('"', '')
            return {"intent": "create_app", "app_name": app_name}
    elif "add a button with text" in natural_language_input:
        parts = natural_language_input.split("add a button with text")
        if len(parts) > 1:
            text_parts = parts[1].split("to the main screen")
            if len(text_parts) > 0:
                button_text = text_parts[0].strip().replace("'", "").replace('"', '')
                return {"intent": "add_button", "button_text": button_text}
    return {"intent": "unknown", "raw_input": natural_language_input}

def generate_android_project_structure(project_name: str, base_dir: str):
    """
    Generates the basic Android project directory structure.
    """
    logging.info(f"Generating Android project structure for: {project_name} at {base_dir}")
    project_path = Path(base_dir) / project_name
    if project_path.exists():
        logging.warning(f"Project directory already exists: {project_path}")
        return project_path

    project_path.mkdir(parents=True, exist_ok=True)

    # App module structure
    app_dir = project_path / "app"
    app_dir.mkdir(exist_ok=True)
    (app_dir / "src").mkdir(exist_ok=True)
    (app_dir / "src" / "main").mkdir(exist_ok=True)
    (app_dir / "src" / "main" / "java").mkdir(exist_ok=True)
    (app_dir / "src" / "main" / "res").mkdir(exist_ok=True)
    (app_dir / "src" / "main" / "res" / "layout").mkdir(exist_ok=True)
    (app_dir / "src" / "main" / "res" / "values").mkdir(exist_ok=True)

    # Build files (placeholders for now)
    (project_path / "build.gradle").touch()
    (app_dir / "build.gradle").touch()
    (project_path / "settings.gradle").touch()

    logging.info(f"Created project structure at: {project_path}")
    return project_path

def create_android_manifest(package_name: str, project_root: Path):
    """
    Creates a basic AndroidManifest.xml file.
    """
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
        <activity android:name=".MainActivity"></activity>
    </application>
</manifest>
"""
    manifest_path = project_root / "app" / "src" / "main" / "AndroidManifest.xml"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    logging.info(f"Created AndroidManifest.xml at: {manifest_path}")

def create_main_activity_java(package_name: str, project_root: Path):
    """
    Creates a basic MainActivity.java file.
    """
    activity_package_path = Path(package_name.replace('.', os.sep))
    activity_dir = project_root / "app" / "src" / "main" / "java" / activity_package_path
    activity_dir.mkdir(parents=True, exist_ok=True)

    activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
"""
    activity_path = activity_dir / "MainActivity.java"
    with open(activity_path, "w", encoding="utf-8") as f:
        f.write(activity_content)
    logging.info(f"Created MainActivity.java at: {activity_path}")

def create_layout_xml(layout_name: str, project_root: Path, content: str = ""):
    """
    Creates a basic layout XML file.
    """
    layout_dir = project_root / "app" / "src" / "main" / "res" / "layout"
    layout_path = layout_dir / f"{layout_name}.xml"

    default_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.capitalize()}">

    {content}

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(default_content if not content else content)
    logging.info(f"Created layout XML at: {layout_path}")

def create_values_xml(values_name: str, project_root: Path, content: str = ""):
    """
    Creates a basic values XML file (e.g., strings.xml, styles.xml).
    """
    values_dir = project_root / "app" / "src" / "main" / "res" / "values"
    values_path = values_dir / f"{values_name}.xml"

    default_content = f"""
<resources>
    {content}
</resources>
"""
    with open(values_path, "w", encoding="utf-8") as f:
        f.write(default_content if not content else content)
    logging.info(f"Created values XML at: {values_path}")


class Lobe_2_arabic_nlp_and_project_builder:
    def __init__(self, project_base_dir: str = "generated_projects"):
        self.project_base_dir = Path(project_base_dir)
        if not self.project_base_dir.exists():
            self.project_base_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.current_project_root = None
        self.package_name = None
        self.app_name = None

    def process_arabic_request(self, natural_language_request: str) -> Path | None:
        """
        Processes an Arabic natural language request to generate an Android project
        structure and basic files.
        """
        logging.info(f"--- Starting Lobe 2_arabic_nlp_and_project_builder ---")
        logging.info(f"Received Arabic request: '{natural_language_request}'")

        intent_data = parse_arabic_intent(natural_language_request)
        intent = intent_data.get("intent")

        if intent == "create_app":
            self.app_name = intent_data.get("app_name", "MyArabicApp")
            # For simplicity, derive package name from app name, though a more robust
            # mapping or user input would be better.
            self.package_name = f"com.example.{self.app_name.lower().replace(' ', '')}"
            logging.info(f"Detected intent: Create App. App Name: {self.app_name}, Package Name: {self.package_name}")

            self.current_project_root = generate_android_project_structure(self.app_name, self.project_base_dir)

            # Create essential Android project files
            create_android_manifest(self.package_name, self.current_project_root)

            # Basic strings.xml
            strings_content = f"""
    <string name="app_name">{self.app_name}</string>
    <string name="hello_world">مرحباً بالعالم!</string>
"""
            create_values_xml("strings", self.current_project_root, strings_content)

            # Basic styles.xml (optional, but good practice)
            styles_content = f"""
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
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
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
"""
            create_values_xml("styles", self.current_project_root, styles_content)

            # Basic activity_main.xml
            main_layout_content = """
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
"""
            create_layout_xml("activity_main", self.current_project_root, main_layout_content)

            # Create MainActivity.java
            create_main_activity_java(self.package_name, self.current_project_root)

            # If the intent was also to add a button, handle that
            if intent_data.get("button_text"):
                button_text = intent_data["button_text"]
                logging.info(f"Adding button with text: '{button_text}'")
                # Modify activity_main.xml to include the button
                # This would be more complex in reality, involving parsing and
                # re-writing XML, or using a dedicated XML builder.
                # For simplicity, we'll just regenerate the layout with a button.

                # A more sophisticated approach would parse the existing XML and insert.
                # For this example, we'll assume the first request is 'create app' and
                # subsequent requests add elements.
                # A better design would be to maintain state of UI elements.

                button_layout_content = f"""
    <Button
        android:id="@+id/myButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{button_text}"
        app:layout_constraintTop_toBottomOf="@+id/textView"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
"""
                create_layout_xml("activity_main", self.current_project_root, button_layout_content)
                # Note: MainActivity.java would also need to be updated to reference this button.
                # This is a simplification for the demonstration.

            logging.info(f"--- Lobe 2_arabic_nlp_and_project_builder Finished. Project created at: {self.current_project_root} ---")
            return self.current_project_root

        elif intent == "add_button":
            if self.current_project_root and self.app_name and self.package_name:
                button_text = intent_data.get("button_text", "Click Me")
                logging.info(f"Detected intent: Add Button. Button Text: '{button_text}'")

                # Assume we are modifying the existing project.
                # In a real system, this would likely involve reading the existing
                # layout, parsing it, inserting the new element, and writing back.
                # For simplicity, we'll recreate activity_main.xml with the button.
                # This is a significant simplification.

                logging.warning("Modifying existing project. Recreating activity_main.xml with new button (simplification).")
                main_layout_content_modified = f"""
    <Button
        android:id="@+id/newButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{button_text}"
        app:layout_constraintTop_toBottomOf="@+id/textView"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
"""
                create_layout_xml("activity_main", self.current_project_root, main_layout_content_modified)
                logging.info(f"Updated activity_main.xml to include button: '{button_text}'")
                # Note: MainActivity.java would also need to be updated to reference this button.

                logging.info(f"--- Lobe 2_arabic_nlp_and_project_builder Finished. Project updated at: {self.current_project_root} ---")
                return self.current_project_root
            else:
                logging.error("Cannot add button: No existing project found or project details are missing.")
                logging.info("--- Lobe 2_arabic_nlp_and_project_builder Finished (with error) ---")
                return None

        else:
            logging.warning(f"Unknown intent detected: '{intent}'. No action taken.")
            logging.info("--- Lobe 2_arabic_nlp_and_project_builder Finished (no action) ---")
            return None

    def cleanup_project(self, project_path: Path):
        """
        Removes a generated project directory.
        """
        if project_path and project_path.exists():
            logging.info(f"Cleaning up project: {project_path}")
            try:
                shutil.rmtree(project_path)
                logging.info(f"Successfully removed project directory: {project_path}")
            except OSError as e:
                logging.error(f"Error removing project directory {project_path}: {e}")
        else:
            logging.warning(f"Project path does not exist or is invalid: {project_path}")

# Example Usage (for testing purposes, will be removed in final integration)
if __name__ == '__main__':
    # Setup logging for this script if it's run directly
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = Lobe_2_arabic_nlp_and_project_builder()

    # Test Case 1: Create a new app
    request1 = "قم بإنشاء تطبيق اسمه 'الهاتف الذكي'"
    print(f"\n--- Testing Request 1: '{request1}' ---")
    project_path1 = builder.process_arabic_request(request1)
    if project_path1:
        print(f"Project generated successfully at: {project_path1}")
    else:
        print("Project generation failed.")

    # Test Case 2: Add a button to the existing app (assuming project1 is still in context)
    request2 = "أضف زرًا بنص 'اضغط هنا' إلى الشاشة الرئيسية"
    print(f"\n--- Testing Request 2: '{request2}' ---")
    project_path2 = builder.process_arabic_request(request2)
    if project_path2:
        print(f"Project updated successfully at: {project_path2}")
    else:
        print("Project update failed.")

    # Test Case 3: Create another app
    request3 = "أنشئ تطبيقاً جديداً اسمه 'المترجم الفوري'"
    print(f"\n--- Testing Request 3: '{request3}' ---")
    project_path3 = builder.process_arabic_request(request3)
    if project_path3:
        print(f"Project generated successfully at: {project_path3}")
    else:
        print("Project generation failed.")

    # Test Case 4: Unknown request
    request4 = "ما هو الطقس اليوم؟"
    print(f"\n--- Testing Request 4: '{request4}' ---")
    project_path4 = builder.process_arabic_request(request4)
    if project_path4:
        print(f"Project generated/updated (unexpectedly) at: {project_path4}")
    else:
        print("No action taken as expected for unknown request.")

    # Clean up generated projects
    print("\n--- Cleaning up all generated projects ---")
    builder.cleanup_project(project_path1)
    builder.cleanup_project(project_path3)