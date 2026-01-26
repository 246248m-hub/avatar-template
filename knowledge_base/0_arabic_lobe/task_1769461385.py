import os
import shutil
import subprocess
from pathlib import Path

# Assume these are defined elsewhere and represent the directory structure
KNOWLEDGE_BASE_DIR = "knowledge_base"
GENERATED_CODE_DIR = "generated_code"
JAVA_PROJECT_DIR = "android_project"
ANDROID_SDK_HOME = os.environ.get("ANDROID_SDK_HOME")

if not ANDROID_SDK_HOME:
    raise EnvironmentError("ANDROID_SDK_HOME environment variable not set. Cannot proceed with APK compilation.")

# --- Lobe 0: Arabic Parser and Generator ---

def setup_dummy_knowledge_base():
    """Creates a dummy knowledge base directory and files for demonstration."""
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "greeting.txt"), "w", encoding="utf-8") as f:
        f.write("مرحبا بك!")
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "question_name.txt"), "w", encoding="utf-8") as f:
        f.write("ما اسمك؟")
    print(f"Dummy knowledge base created at: {KNOWLEDGE_BASE_DIR}")

def parse_arabic_text(text: str, kb_dir: str) -> dict:
    """
    Parses Arabic natural language text, potentially using a knowledge base.
    This is a placeholder for more sophisticated NLP.
    """
    parsed_data = {"original_text": text, "intent": None, "entities": {}}
    if "مرحبا" in text:
        parsed_data["intent"] = "greeting"
        if os.path.exists(os.path.join(kb_dir, "greeting.txt")):
            with open(os.path.join(kb_dir, "greeting.txt"), "r", encoding="utf-8") as f:
                parsed_data["entities"]["greeting_response"] = f.read().strip()
    elif "اسمك" in text:
        parsed_data["intent"] = "ask_name"
        if os.path.exists(os.path.join(kb_dir, "question_name.txt")):
            with open(os.path.join(kb_dir, "question_name.txt"), "r", encoding="utf-8") as f:
                parsed_data["entities"]["question_prompt"] = f.read().strip()
    return parsed_data

def generate_arabic_response(parsed_data: dict) -> str:
    """
    Generates an Arabic response based on parsed data.
    This is a placeholder for more sophisticated NLP generation.
    """
    intent = parsed_data.get("intent")
    entities = parsed_data.get("entities", {})

    if intent == "greeting" and "greeting_response" in entities:
        return entities["greeting_response"]
    elif intent == "ask_name" and "question_prompt" in entities:
        return f"أنا مساعدك الذكي. {entities['question_prompt']}"
    else:
        return "عذرا، لم أفهم طلبك."

def arabic_nlp_module_demo():
    """
    Demonstrates the Arabic parser and generator.
    """
    setup_dummy_knowledge_base()

    test_prompt_1 = "مرحبا"
    parsed_1 = parse_arabic_text(test_prompt_1, KNOWLEDGE_BASE_DIR)
    generated_1 = generate_arabic_response(parsed_1)
    print(f"Prompt: '{test_prompt_1}' -> Parsed: {parsed_1} -> Generated: '{generated_1}'")

    test_prompt_2 = "ما اسمك؟"
    parsed_2 = parse_arabic_text(test_prompt_2, KNOWLEDGE_BASE_DIR)
    generated_2 = generate_arabic_response(parsed_2)
    print(f"Prompt: '{test_prompt_2}' -> Parsed: {parsed_2} -> Generated: '{generated_2}'")

    test_prompt_3 = "كيف حالك؟"
    parsed_3 = parse_arabic_text(test_prompt_3, KNOWLEDGE_BASE_DIR)
    generated_3 = generate_arabic_response(parsed_3)
    print(f"Prompt: '{test_prompt_3}' -> Parsed: {parsed_3} -> Generated: '{generated_3}'")

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

    # Clean up dummy knowledge base files
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
        print(f"Removed dummy knowledge base directory: {KNOWLEDGE_BASE_DIR}")

# --- Lobe 4: Code Generation ---

def create_android_project_structure(project_name: str):
    """
    Creates a basic Android project structure for a new APK.
    """
    project_path = Path(JAVA_PROJECT_DIR) / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    src_path = project_path / "app" / "src" / "main"
    src_path.mkdir(parents=True, exist_ok=True)

    java_path = src_path / "java"
    java_path.mkdir(parents=True, exist_ok=True)

    package_name = "com.example." + project_name.lower()
    package_path = java_path / package_name.replace('.', os.sep)
    package_path.mkdir(parents=True, exist_ok=True)

    manifest_path = src_path / "AndroidManifest.xml"
    with open(manifest_path, "w") as f:
        f.write(f"""<?xml version="1.0" encoding="utf-8"?>
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
""")

    # Create a placeholder strings.xml
    res_path = src_path / "res"
    res_path.mkdir(parents=True, exist_ok=True)
    values_path = res_path / "values"
    values_path.mkdir(parents=True, exist_ok=True)
    strings_xml_path = values_path / "strings.xml"
    with open(strings_xml_path, "w") as f:
        f.write(f"""<resources>
    <string name="app_name">{project_name}</string>
</resources>
""")

    print(f"Basic Android project structure created at: {project_path}")
    return project_path, package_name

def generate_main_activity_java(package_name: str, project_path: Path) -> Path:
    """
    Generates a basic MainActivity.java file.
    """
    main_activity_path = project_path / "app" / "src" / "main" / "java" / package_name.replace('.', os.sep) / "MainActivity.java"

    java_code = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // This layout needs to be created
        TextView textView = findViewById(R.id.mainTextView);
        textView.setText("Hello from Android!");
    }}
}}
"""
    with open(main_activity_path, "w") as f:
        f.write(java_code)

    print(f"Generated MainActivity.java at: {main_activity_path}")
    return main_activity_path

def generate_activity_main_layout_xml(project_path: Path):
    """
    Generates a basic activity_main.xml layout file.
    """
    layout_path = project_path / "app" / "src" / "main" / "res" / "layout"
    layout_path.mkdir(parents=True, exist_ok=True)
    activity_main_xml_path = layout_path / "activity_main.xml"

    xml_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/mainTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(activity_main_xml_path, "w") as f:
        f.write(xml_content)
    print(f"Generated activity_main.xml at: {activity_main_xml_path}")

def generate_apk_code_module_demo():
    """
    Demonstrates the code generation for an APK.
    """
    project_name = "MyFirstApp"
    print(f"\n--- Generating code for APK: {project_name} ---")
    project_path, package_name = create_android_project_structure(project_name)
    generate_main_activity_java(package_name, project_path)
    generate_activity_main_layout_xml(project_path)

    print("\n--- APK Code Generation Module Demo Finished ---")

# --- Lobe 8: APK Compiler ---

def build_apk(project_path: Path) -> Path:
    """
    Compiles the Android project into an APK using Gradle.
    Assumes Gradle wrapper is present or Gradle is in PATH.
    """
    print(f"Attempting to build APK for project at: {project_path}")

    if not (project_path / "build.gradle").exists() and not (project_path / "app" / "build.gradle").exists():
        raise FileNotFoundError(f"Could not find build.gradle file in {project_path} or its subdirectories. Ensure it's a valid Android project.")

    # Navigate to the project directory
    original_dir = os.getcwd()
    os.chdir(project_path)

    try:
        # Execute Gradle build command
        # Assumes gradlew is available or 'gradle' command works
        gradle_command = ["./gradlew", "assembleDebug"] # Build a debug APK
        if os.name == 'nt': # Windows
            gradle_command = ["gradlew.bat", "assembleDebug"]

        print(f"Running command: {' '.join(gradle_command)}")
        result = subprocess.run(gradle_command, capture_output=True, text=True, check=True)
        print("Gradle build output:\n", result.stdout)

        # Find the generated APK
        apk_path = None
        # Standard location for debug APKs in Android Studio projects
        debug_apk_dir = project_path / "app" / "build" / "outputs" / "apk" / "debug"
        for apk_file in debug_apk_dir.glob("*.apk"):
            apk_path = apk_file
            break

        if not apk_path:
            raise FileNotFoundError("Could not find the generated APK file. Check Gradle build output for errors.")

        print(f"Successfully built APK: {apk_path}")
        return apk_path

    except FileNotFoundError:
        print("Error: gradlew or gradlew.bat not found. Make sure you are in the project root and the Gradle wrapper is set up.")
        raise
    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build:\n{e.stderr}")
        raise
    finally:
        # Return to the original directory
        os.chdir(original_dir)

def apk_compiler_module_demo():
    """
    Demonstrates the APK compilation process.
    """
    project_name = "MyCompiledApp"
    print(f"\n--- Initiating APK compilation for: {project_name} ---")

    # 1. Generate project structure and code (as if from Lobe 4)
    project_path, package_name = create_android_project_structure(project_name)
    generate_main_activity_java(package_name, project_path)
    generate_activity_main_layout_xml(project_path)

    # 2. Compile the APK
    try:
        built_apk_path = build_apk(project_path)
        print(f"APK compiled successfully: {built_apk_path}")
    except Exception as e:
        print(f"Failed to compile APK: {e}")

    print("\n--- APK Compiler Lobe Demo Finished ---")

    # Clean up dummy generated code directory
    if os.path.exists(JAVA_PROJECT_DIR):
        shutil.rmtree(JAVA_PROJECT_DIR)
        print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")

# --- Main Execution Flow ---

def main_workflow():
    """
    Orchestrates the demonstration of the integrated lobes.
    """
    print("--- Starting Unified Mind Evolution ---")

    # Demonstrate Arabic NLP
    print("\n--- Demonstrating Lobe 0: Arabic Parser and Generator ---")
    arabic_nlp_module_demo()

    # Demonstrate Code Generation for APK
    print("\n--- Demonstrating Lobe 4: Code Generation ---")
    generate_apk_code_module_demo()

    # Demonstrate APK Compilation
    print("\n--- Demonstrating Lobe 8: APK Compiler ---")
    apk_compiler_module_demo()

    print("\n--- Unified Mind Evolution Process Simulated ---")

if __name__ == "__main__":
    main_workflow()