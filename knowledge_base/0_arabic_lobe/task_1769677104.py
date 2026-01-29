import os
import shutil
from pathlib import Path

# --- Constants ---
DUMMY_PROJECT_ROOT = Path("./dummy_android_project_for_arabic")
ARABIC_LANGUAGE_CODE = "ar"
DEFAULT_PACKAGE_NAME = "com.example.arabicapp"

# --- Helper Functions ---
def create_dummy_android_project(project_path: Path, package_name: str):
    """Creates a basic dummy Android project structure."""
    print(f"Creating dummy Android project at: {project_path}")
    project_path.mkdir(parents=True, exist_ok=True)

    # Create manifest
    manifest_dir = project_path / "app" / "src" / "main"
    manifest_dir.mkdir(parents=True, exist_ok=True)
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
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(manifest_dir / "AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Create strings.xml for app name and potential Arabic text
    res_dir = project_path / "app" / "src" / "main" / "res"
    res_dir.mkdir(parents=True, exist_ok=True)
    values_dir = res_dir / "values"
    values_dir.mkdir(parents=True, exist_ok=True)
    with open(values_dir / "strings.xml", "w", encoding="utf-8") as f:
        f.write("""
<resources>
    <string name="app_name">Arabic App</string>
</resources>
""")

    # Create Arabic values directory and strings.xml
    values_ar_dir = res_dir / f"values-{ARABIC_LANGUAGE_CODE}"
    values_ar_dir.mkdir(parents=True, exist_ok=True)
    with open(values_ar_dir / "strings.xml", "w", encoding="utf-8") as f:
        f.write("""
<resources>
    <string name="app_name">تطبيق عربي</string>
</resources>
""")

    # Create MainActivity (basic placeholder)
    java_dir = project_path / "app" / "src" / "main" / "java"
    package_path = Path(java_dir)
    for part in package_name.split('.'):
        package_path /= part
    package_path.mkdir(parents=True, exist_ok=True)
    main_activity_content = f"""
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
    with open(package_path / "MainActivity.java", "w", encoding="utf-8") as f:
        f.write(main_activity_content)

    # Create a placeholder layout file
    layout_dir = res_dir / "layout"
    layout_dir.mkdir(parents=True, exist_ok=True)
    with open(layout_dir / "activity_main.xml", "w", encoding="utf-8") as f:
        f.write("""
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")

    print("Dummy Android project structure created.")


def generate_arabic_apk_structure(instruction: str, project_root: Path = DUMMY_PROJECT_ROOT, package_name: str = DEFAULT_PACKAGE_NAME) -> Path:
    """
    Generates a basic Android APK structure tailored for Arabic language support.
    This function will create a minimal Android project directory.

    Args:
        instruction (str): A natural language instruction for the Arabic APK.
                           Currently, this function creates a default structure.
                           Future iterations will parse this instruction.
        project_root (Path): The root directory for the generated project.
        package_name (str): The package name for the Android application.

    Returns:
        Path: The path to the root of the generated Android project.
    """
    print(f"\n--- Lobe 0: Arabic APK Structure Generator ---")
    print(f"Instruction received: '{instruction}'")

    if project_root.exists():
        print(f"Removing existing dummy project at: {project_root}")
        shutil.rmtree(project_root)

    create_dummy_android_project(project_root, package_name)

    print(f"Basic Arabic APK structure generated at: {project_root}")
    return project_root

def update_strings_for_arabic_instruction(project_path: Path, user_instruction: str):
    """
    Parses the user instruction and updates the Arabic strings.xml
    with relevant translations or dynamically generated text.
    This is a placeholder for advanced NLP parsing.
    """
    print(f"Updating Arabic strings for instruction: '{user_instruction}'")
    strings_ar_path = project_path / "app" / "src" / "main" / "res" / f"values-{ARABIC_LANGUAGE_CODE}" / "strings.xml"

    if not strings_ar_path.exists():
        print(f"Error: Arabic strings file not found at {strings_ar_path}")
        return

    # --- Placeholder for actual NLP parsing and dynamic string generation ---
    # In a real scenario, we'd use Lobe 0's NLP capabilities to:
    # 1. Understand the 'user_instruction'.
    # 2. Extract key phrases or concepts.
    # 3. Translate them or generate Arabic text dynamically.
    # For this demo, we'll just append a generic string.

    dynamic_arabic_text = "مرحباً بالعالم" # "Hello World" in Arabic
    if "greet" in user_instruction.lower():
        dynamic_arabic_text = "مرحباً بالعالم"
    elif "welcome" in user_instruction.lower():
        dynamic_arabic_text = "أهلاً وسهلاً"

    try:
        with open(strings_ar_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Simple insertion before the closing </resources> tag
        if dynamic_arabic_text not in content:
            new_content = content.replace("</resources>", f'    <string name="dynamic_greeting">{dynamic_arabic_text}</string>\n</resources>')
            with open(strings_ar_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully added '{dynamic_arabic_text}' to Arabic strings.")
        else:
            print(f"'{dynamic_arabic_text}' already present in Arabic strings.")

    except Exception as e:
        print(f"Error updating Arabic strings: {e}")
    # --- End Placeholder ---


# --- Main Function (for demonstration) ---
if __name__ == "__main__":
    # Simulate instruction from Lobe 0 (Arabic)
    arabic_instruction_example = "Create an Android app with a greeting message in Arabic."

    print("--- Simulating Lobe 0: Arabic APK Structure Generator ---")
    generated_project_path = generate_arabic_apk_structure(arabic_instruction_example)

    # Simulate Lobe 0 updating strings based on the instruction
    print("\n--- Simulating Lobe 0: Updating Arabic Strings ---")
    update_strings_for_arabic_instruction(generated_project_path, arabic_instruction_example)

    print("\n--- Lobe 0: Arabic APK Structure Generator Demo Finished ---")

    # Clean up the dummy project
    if generated_project_path.exists():
        print(f"\nRemoving dummy project directory: {generated_project_path}")
        shutil.rmtree(generated_project_path)

    print("\n--- Lobe 0: Arabic APK Structure Generator Module Demo Finished ---")