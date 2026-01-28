import os
import shutil
from pathlib import Path

# Assuming AndroidProjectBuilder is defined elsewhere and accessible.
# For demonstration purposes, let's create a mock class.
class AndroidProjectBuilder:
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = Path(project_name)
        self.src_dir = self.project_dir / "app" / "src" / "main" / "java" / "com" / "example" / project_name.lower().replace(" ", "_")
        self.res_dir = self.project_dir / "app" / "src" / "main" / "res"
        self.manifest_path = self.project_dir / "app" / "src" / "main" / "AndroidManifest.xml"

    def _create_directory_structure(self):
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.src_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir.mkdir(parents=True, exist_ok=True)

    def _create_manifest(self):
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{self.project_name.lower().replace(' ', '_')}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{self.project_name.replace(' ', '')}">

        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(self.manifest_path, "w") as f:
            f.write(manifest_content)

    def _create_strings_xml(self):
        strings_xml_path = self.res_dir / "values" / "strings.xml"
        strings_xml_path.parent.mkdir(parents=True, exist_ok=True)
        strings_content = f"""
<resources>
    <string name="app_name">{self.project_name}</string>
</resources>
"""
        with open(strings_xml_path, "w") as f:
            f.write(strings_content)

    def _create_main_activity(self, activity_name="MainActivity"):
        activity_file_path = self.src_dir / f"{activity_name}.java"
        activity_content = f"""
package com.example.{self.project_name.lower().replace(' ', '_')};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming a default layout
    }}
}}
"""
        with open(activity_file_path, "w") as f:
            f.write(activity_content)

    def _create_activity_main_layout(self):
        layout_dir = self.res_dir / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        layout_file_path = layout_dir / "activity_main.xml"
        layout_content = """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <!-- Placeholder content -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(layout_file_path, "w") as f:
            f.write(layout_content)


    def build_project(self, natural_language_input: str):
        """
        Parses natural language input to configure and build a basic Android project structure.
        This is a simplified mock; a real implementation would involve much more complex parsing
        and generation of Android-specific code and configurations.
        """
        print(f"Simulating Android project build for: {self.project_name}")
        print(f"Processing input: '{natural_language_input}'")

        self._create_directory_structure()
        self._create_manifest()
        self._create_strings_xml()
        self._create_main_activity()
        self._create_activity_main_layout() # Essential for a runnable app

        print(f"Basic project structure for '{self.project_name}' created at '{self.project_dir}'.")
        print("Note: This is a simplified mock. A real implementation would generate specific code based on input.")

# Mocking a function to get the current working directory
class MockOS:
    def __init__(self):
        self._current_dir = Path.cwd()

    def chdir(self, path):
        if path == "..":
            self._current_dir = self._current_dir.parent
        else:
            self._current_dir /= path
        print(f"Changed directory to: {self._current_dir}")

    def getcwd(self):
        return self._current_dir

# Instantiate mock OS
os = MockOS()

# Global variables for demonstration
KNOWLEDGE_BASE_DIR = "."
test_prompt_5 = "Create a simple calculator app with addition and subtraction."
generated_output_5 = "This is a simulated output for the calculator app prompt."

def cleanup_dummy_files():
    """
    Cleans up any dummy files or directories created during the demo.
    In a real scenario, this would be more robust.
    """
    projects_to_clean = ["MyApp_Counter", "MyApp_Calculator"] # Example project names
    for proj_name in projects_to_clean:
        proj_path = Path(proj_name)
        if proj_path.exists():
            print(f"Removing directory: {proj_path}")
            shutil.rmtree(proj_path)

def build_android_project_from_arabic(arabic_input: str, project_name: str):
    """
    Handles the process of building an Android project from Arabic natural language input.
    This function acts as an orchestrator for the AndroidProjectBuilder.
    """
    print(f"\n--- Building Android Project: {project_name} ---")
    print(f"Receiving Arabic input: '{arabic_input}'")

    # In a real scenario, arabic_input would be parsed by an Arabic NLP module
    # to extract project name, features, UI elements, etc.
    # For this mock, we'll use the provided project_name directly and a generic input string.

    builder = AndroidProjectBuilder(project_name=project_name)
    builder.build_project(arabic_input)

    print(f"--- Android Project Build for {project_name} Completed ---")

def arabic_parser_and_generator_module_demo():
    """
    Demonstrates the Arabic parser and generator module's functionality
    by building a basic counter app and a conceptual calculator app.
    """
    print("\n" + "="*50 + "\n")
    print("--- Arabic Parser and Generator Module Demo ---")

    # Mocking the initial directory state
    original_dir = os.getcwd()
    print(f"Initial directory: {original_dir}")

    # --- Demo Part 1: Basic Counter App ---
    print("\n--- Building Basic Counter App ---")
    arabic_input_1 = "أنشئ تطبيق عداد بسيط" # "Create a simple counter app"
    project_name_counter = "MyApp_Counter"
    build_android_project_from_arabic(arabic_input_1, project_name_counter)

    # --- Demo Part 2: Conceptual Calculator App ---
    print("\n--- Building Conceptual Calculator App ---")
    arabic_input_2 = "أنشئ تطبيق آلة حاسبة يدعم الجمع والطرح" # "Create a calculator app that supports addition and subtraction"
    project_name_calculator = "MyApp_Calculator"
    build_android_project_from_arabic(arabic_input_2, project_name_calculator)

    # --- End of Demo ---
    print("\n" + "="*50 + "\n")
    print("--- Arabic Parser and Generator Module Demo Finished ---")

    # Clean up dummy files
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()

    # Reset to original directory if needed (though the mock doesn't strictly enforce it without more context)
    os.chdir(original_dir)
    print(f"Returned to directory: {os.getcwd()}")

# Example execution of the demo
if __name__ == "__main__":
    arabic_parser_and_generator_module_demo()