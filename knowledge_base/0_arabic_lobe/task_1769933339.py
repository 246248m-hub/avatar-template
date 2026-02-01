import os
import json
import re
import sys
import subprocess
import time
import shutil

# Assume necessary imports for other lobes are present, e.g.,
# from lobe_0_language_lobe import extract_keywords, generate_text
# from lobe_1_parsing_lobe import parse_apk_structure
# from lobe_2_entity_extraction_lobe import extract_entities
# from lobe_3_intent_recognition_lobe import recognize_intent
# from lobe_4_code_generation_lobe import generate_android_code
# from lobe_5_resource_generation_lobe import generate_resources
# from lobe_7_testing_lobe import run_tests
# from lobe_8_apk_compiler_lobe import compile_apk
# from lobe_11_deployment_lobe import deploy_apk

# --- Lobe 0_arabic_lobe ---
# This lobe focuses on understanding and generating Arabic text,
# specifically for describing APKs and their functionalities.

ARABIC_KNOWLEDGE_BASE_DIR = "arabic_kb"
ARABIC_TEMPLATES_DIR = os.path.join(ARABIC_KNOWLEDGE_BASE_DIR, "templates")
ARABIC_EXAMPLES_DIR = os.path.join(ARABIC_KNOWLEDGE_BASE_DIR, "examples")

def ensure_arabic_kb_exists():
    """Ensures the Arabic knowledge base directory structure exists."""
    os.makedirs(ARABIC_TEMPLATES_DIR, exist_ok=True)
    os.makedirs(ARABIC_EXAMPLES_DIR, exist_ok=True)
    # Add dummy template and example files if they don't exist
    if not os.path.exists(os.path.join(ARABIC_TEMPLATES_DIR, "app_template.txt")):
        with open(os.path.join(ARABIC_TEMPLATES_DIR, "app_template.txt"), "w", encoding="utf-8") as f:
            f.write("اسم التطبيق: [اسم التطبيق]\n")
            f.write("وصف التطبيق: [وصف التطبيق]\n")
            f.write("الميزات الرئيسية: [الميزات الرئيسية]\n")
            f.write("الغرض: [الغرض]\n")
    if not os.path.exists(os.path.join(ARABIC_EXAMPLES_DIR, "weather_app_example.txt")):
        with open(os.path.join(ARABIC_EXAMPLES_DIR, "weather_app_example.txt"), "w", encoding="utf-8") as f:
            f.write("اسم التطبيق: تطبيق الطقس\n")
            f.write("وصف التطبيق: يعرض معلومات الطقس الحالية والمتوقعة.\n")
            f.write("الميزات الرئيسية: عرض درجة الحرارة، حالة الطقس، توقعات.\n")
            f.write("الغرض: مساعدة المستخدمين في متابعة أحوال الطقس.\n")

def generate_arabic_apk_description(apk_name: str, features: list[str], purpose: str) -> str:
    """
    Generates a descriptive text for an APK in Arabic based on provided information.
    This function simulates interaction with the language lobe for Arabic text generation.
    """
    ensure_arabic_kb_exists()
    template_path = os.path.join(ARABIC_TEMPLATES_DIR, "app_template.txt")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Arabic template not found at {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    description = template.replace("[اسم التطبيق]", apk_name)
    description = description.replace("[وصف التطبيق]", f"تطبيق يهدف إلى {purpose}.")
    description = description.replace("[الميزات الرئيسية]", ", ".join(features))
    description = description.replace("[الغرض]", purpose)

    # In a real scenario, this would involve more sophisticated NLP
    # and potentially Arabic language models. For this example, we
    # are using a template-based approach.
    return description

def parse_arabic_apk_description(arabic_text: str) -> dict:
    """
    Parses an Arabic APK description string to extract relevant information.
    This function simulates interaction with the language lobe for Arabic text parsing.
    """
    parsed_data = {
        "apk_name": None,
        "description": None,
        "features": [],
        "purpose": None
    }

    lines = arabic_text.split('\n')
    for line in lines:
        if line.startswith("اسم التطبيق:"):
            parsed_data["apk_name"] = line.split(":", 1)[1].strip()
        elif line.startswith("وصف التطبيق:"):
            parsed_data["description"] = line.split(":", 1)[1].strip()
        elif line.startswith("الميزات الرئيسية:"):
            features_str = line.split(":", 1)[1].strip()
            parsed_data["features"] = [f.strip() for f in features_str.split(',')]
        elif line.startswith("الغرض:"):
            parsed_data["purpose"] = line.split(":", 1)[1].strip()

    # Further NLP processing could be done here to refine extracted entities
    # and relationships.

    return parsed_data

# --- Lobe 4_code_generation_lobe ---
# This lobe is responsible for generating Android code (Java/Kotlin)
# based on parsed requirements.

ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
OUTPUT_APKS_DIR = "generated_apks"

def ensure_android_project_template_exists():
    """Ensures the Android project template directory structure exists."""
    os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR, exist_ok=True)
    # Create dummy files for a minimal Android project structure
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "myapp"), exist_ok=True)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "values"), exist_ok=True)

    if not os.path.exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "myapp", "MainActivity.java")):
        with open(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "myapp", "MainActivity.java"), "w") as f:
            f.write("""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView greetingTextView = findViewById(R.id.greetingTextView);
        // This text will be dynamically set by the generator
        greetingTextView.setText("Hello, User!");
    }
}
""")
    if not os.path.exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout", "activity_main.xml")):
        with open(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout", "activity_main.xml"), "w") as f:
            f.write("""
<?xml version="1.0" encoding="utf-8"?>
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
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
    if not os.path.exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "values", "strings.xml")):
        with open(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "values", "strings.xml"), "w") as f:
            f.write("""
<resources>
    <string name="app_name">MyGeneratedApp</string>
</resources>
""")
    if not os.path.exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "build.gradle")):
        with open(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "build.gradle"), "w") as f:
            f.write("""
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.0.0' // Example version
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
task clean(type: Delete) {
    delete rootProject.buildDir
}
""")
    if not os.path.exists(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "settings.gradle")):
        with open(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "settings.gradle"), "w") as f:
            f.write("""
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "MyGeneratedApp"
include ':app'
""")


def generate_android_project(apk_name: str, features: list[str], purpose: str, output_dir: str):
    """
    Generates a basic Android project structure based on the APK details.
    This function simulates code generation.
    """
    ensure_android_project_template_exists()
    project_name = apk_name.replace(" ", "_").lower()
    target_project_path = os.path.join(output_dir, project_name)
    shutil.copytree(ANDROID_PROJECT_TEMPLATE_DIR, target_project_path)

    # Modify key files to reflect the new project name and features
    # 1. settings.gradle
    settings_gradle_path = os.path.join(target_project_path, "settings.gradle")
    with open(settings_gradle_path, "r", encoding="utf-8") as f:
        settings_content = f.read()
    settings_content = settings_content.replace("rootProject.name = \"MyGeneratedApp\"", f"rootProject.name = \"{project_name}\"")
    with open(settings_gradle_path, "w", encoding="utf-8") as f:
        f.write(settings_content)

    # 2. app/build.gradle (applicationId)
    app_build_gradle_path = os.path.join(target_project_path, "app", "build.gradle")
    with open(app_build_gradle_path, "r", encoding="utf-8") as f:
        app_build_content = f.read()
    # This is a simplified change; in reality, it might be more complex
    app_build_content = app_build_content.replace("com.example.myapp", f"com.example.{project_name}")
    with open(app_build_gradle_path, "w", encoding="utf-8") as f:
        f.write(app_build_content)

    # 3. app/src/main/res/values/strings.xml (app_name)
    strings_xml_path = os.path.join(target_project_path, "app", "src", "main", "res", "values", "strings.xml")
    with open(strings_xml_path, "r", encoding="utf-8") as f:
        strings_content = f.read()
    strings_content = strings_content.replace("<string name=\"app_name\">MyGeneratedApp</string>", f"<string name=\"app_name\">{apk_name}</string>")
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(strings_content)

    # 4. app/src/main/java/com/example/myapp/MainActivity.java
    main_activity_java_path = os.path.join(target_project_path, "app", "src", "main", "java", "com", "example", project_name, "MainActivity.java")
    # Need to create the package directory if it doesn't exist
    os.makedirs(os.path.dirname(main_activity_java_path), exist_ok=True)
    with open(main_activity_java_path, "w", encoding="utf-8") as f:
        f.write(f"""
package com.example.{project_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView greetingTextView = findViewById(R.id.greetingTextView);
        // Dynamically setting text based on purpose/features
        String appPurpose = "{purpose}";
        String appFeatures = String.join(", ", {json.dumps(features)});
        greetingTextView.setText("Welcome to " + getString(R.string.app_name) + "!");
        // In a real app, this would be more complex, e.g., displaying features or linking to them.
        // For this demo, we just show a basic greeting.
    }}
}}
""")

    print(f"Generated Android project structure at: {target_project_path}")
    return target_project_path

# --- Lobe 8_apk_compiler_lobe ---
# This lobe is responsible for compiling the Android project into an APK.

def compile_android_project_to_apk(project_path: str, output_apk_dir: str) -> str:
    """
    Compiles an Android project into an APK using Gradle.
    Requires Android SDK and Gradle to be installed and configured.
    """
    print(f"Starting APK compilation for project at: {project_path}")

    # Ensure the output directory exists
    os.makedirs(output_apk_dir, exist_ok=True)

    # The actual compilation command depends on your setup.
    # This assumes you can run gradle from the project directory.
    # You might need to specify the path to gradlew if it's not directly runnable.

    # Common gradle commands:
    # For Linux/macOS: ./gradlew assembleDebug
    # For Windows: gradlew assembleDebug

    gradlew_command = ["./gradlew", "assembleDebug"]
    if sys.platform == "win32":
        gradlew_command = ["gradlew.bat", "assembleDebug"]

    try:
        # Execute the gradle build command
        # We're running this from the project directory
        process = subprocess.Popen(
            gradlew_command,
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        print("Gradle stdout:")
        print(stdout)
        print("Gradle stderr:")
        print(stderr)

        if process.returncode != 0:
            raise RuntimeError(f"Gradle build failed with return code {process.returncode}")

        # Find the generated APK file
        # The location can vary slightly based on Gradle version and configuration.
        # Common locations: app/build/outputs/apk/debug/app-debug.apk
        debug_apk_path = os.path.join(project_path, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
        if not os.path.exists(debug_apk_path):
            # Try a slightly different path if the first one fails
            debug_apk_path = os.path.join(project_path, "app", "build", "outputs", "apk", "release", "app-release.apk") # Less common for debug build
            if not os.path.exists(debug_apk_path):
                 raise FileNotFoundError(f"Could not find the generated APK in expected locations within {project_path}")


        # Copy the APK to the final output directory
        final_apk_filename = os.path.basename(debug_apk_path)
        destination_apk_path = os.path.join(output_apk_dir, final_apk_filename)

        # Clean up previous APK if it exists in the output directory
        if os.path.exists(destination_apk_path):
            os.remove(destination_apk_path)
            print(f"Removed existing APK at {destination_apk_path}")

        shutil.copy(debug_apk_path, destination_apk_path)
        print(f"APK successfully compiled and saved to: {destination_apk_path}")
        return destination_apk_path

    except FileNotFoundError:
        print("Error: gradlew command not found. Make sure you are in the project directory or have it in your PATH.")
        print("Ensure you have the Android SDK and Gradle installed and configured.")
        return None
    except Exception as e:
        print(f"An error occurred during APK compilation: {e}")
        return None

def create_dummy_android_project(output_dir: str, project_name: str = "MyDummyApp") -> str:
    """Creates a dummy Android project for testing purposes."""
    ensure_android_project_template_exists()
    dummy_project_path = os.path.join(output_dir, project_name)
    if os.path.exists(dummy_project_path):
        shutil.rmtree(dummy_project_path)
    shutil.copytree(ANDROID_PROJECT_TEMPLATE_DIR, dummy_project_path)

    # Basic modifications for the dummy project
    settings_gradle_path = os.path.join(dummy_project_path, "settings.gradle")
    with open(settings_gradle_path, "r", encoding="utf-8") as f:
        settings_content = f.read()
    settings_content = settings_content.replace("rootProject.name = \"MyGeneratedApp\"", f"rootProject.name = \"{project_name}\"")
    with open(settings_gradle_path, "w", encoding="utf-8") as f:
        f.write(settings_content)

    app_build_gradle_path = os.path.join(dummy_project_path, "app", "build.gradle")
    with open(app_build_gradle_path, "r", encoding="utf-8") as f:
        app_build_content = f.read()
    app_build_content = app_build_content.replace("com.example.myapp", f"com.example.{project_name.lower()}")
    with open(app_build_gradle_path, "w", encoding="utf-8") as f:
        f.write(app_build_content)

    strings_xml_path = os.path.join(dummy_project_path, "app", "src", "main", "res", "values", "strings.xml")
    with open(strings_xml_path, "r", encoding="utf-8") as f:
        strings_content = f.read()
    strings_content = strings_content.replace("<string name=\"app_name\">MyGeneratedApp</string>", f"<string name=\"app_name\">{project_name}</string>")
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(strings_content)

    print(f"Created dummy Android project at: {dummy_project_path}")
    return dummy_project_path

def demo_arabic_parser_generator_module():
    """Demonstrates the Arabic parser and generator functionality."""
    print("\n--- Starting Arabic Parser and Generator Module Demo ---")

    # --- Generation Demo ---
    apk_name_arabic = "تطبيق الآلة الحاسبة"
    features_arabic = ["جمع", "طرح", "ضرب", "قسمة"]
    purpose_arabic = "إجراء العمليات الحسابية الأساسية"

    generated_description = generate_arabic_apk_description(
        apk_name=apk_name_arabic,
        features=features_arabic,
        purpose=purpose_arabic
    )
    print(f"\nGenerated Arabic Description:\n{generated_description}")

    # --- Parsing Demo ---
    sample_arabic_description = """
اسم التطبيق: تطبيق إدارة المهام
وصف التطبيق: يساعد المستخدمين على تتبع وتنظيم مهامهم اليومية.
الميزات الرئيسية: إنشاء مهمة، تحديد موعد نهائي، وضع علامة مكتملة.
الغرض: تحسين الإنتاجية وإدارة الوقت.
"""
    print(f"\nParsing Sample Arabic Description:\n{sample_arabic_description}")
    parsed_info = parse_arabic_apk_description(sample_arabic_description)
    print(f"Parsed Information:\n{json.dumps(parsed_info, indent=2, ensure_ascii=False)}")

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

def demo_apk_compiler_module():
    """Demonstrates the APK compiler functionality."""
    print("\n--- Starting APK Compiler Module Demo ---")

    # Create a dummy project for compilation
    DUMMY_PROJECT_OUTPUT_DIR = "dummy_android_projects"
    os.makedirs(DUMMY_PROJECT_OUTPUT_DIR, exist_ok=True)
    dummy_project_path = create_dummy_android_project(DUMMY_PROJECT_OUTPUT_DIR)

    # Define where the final APKs will be stored
    os.makedirs(OUTPUT_APKS_DIR, exist_ok=True)

    # Attempt to compile the dummy project
    print("\nAttempting to compile dummy project to APK...")
    compiled_apk_path = compile_android_project_to_apk(dummy_project_path, OUTPUT_APKS_DIR)

    if compiled_apk_path:
        print(f"\nSuccessfully compiled APK: {compiled_apk_path}")
    else:
        print("\nAPK compilation failed. Please check the error messages above.")
        print("Ensure you have the Android SDK and Gradle installed and configured, and that the 'gradlew' command is accessible.")

    print("\n--- APK Compiler Module Demo Finished ---")

# --- Main Execution Block for Demonstration ---
if __name__ == "__main__":
    # This block is for running the demo independently.
    # In a real application, this would be called by an orchestrator.

    # Setup for demo
    if not os.path.exists(ARABIC_KNOWLEDGE_BASE_DIR):
        os.makedirs(ARABIC_KNOWLEDGE_BASE_DIR)
    if not os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR)

    print("--- Running Demonstrations ---")

    print("\n--- Demonstrating Lobe 0_arabic_lobe ---")
    demo_arabic_parser_generator_module()

    print("\n--- Demonstrating Lobe 4_code_generation_lobe ---")
    demo_code_gen_output_dir = "generated_android_projects"
    os.makedirs(demo_code_gen_output_dir, exist_ok=True)
    generated_project_path = generate_android_project(
        apk_name="مفكرة بسيطة",
        features=["إضافة ملاحظة", "عرض الملاحظات", "حذف ملاحظة"],
        purpose="تدوين الأفكار والملاحظات السريعة",
        output_dir=demo_code_gen_output_dir
    )
    print(f"Android project generated at: {generated_project_path}")

    print("\n--- Demonstrating Lobe 8_apk_compiler_lobe ---")
    demo_apk_compiler_module()

    # Clean up dummy files and directories created during demos
    print("\n--- Cleaning up demo artifacts ---")
    if os.path.exists(ARABIC_KNOWLEDGE_BASE_DIR):
        shutil.rmtree(ARABIC_KNOWLEDGE_BASE_DIR)
        print(f"Removed: {ARABIC_KNOWLEDGE_BASE_DIR}")
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        print(f"Removed: {ANDROID_PROJECT_TEMPLATE_DIR}")
    if os.path.exists(demo_code_gen_output_dir):
        shutil.rmtree(demo_code_gen_output_dir)
        print(f"Removed: {demo_code_gen_output_dir}")
    if os.path.exists(DUMMY_PROJECT_OUTPUT_DIR):
        shutil.rmtree(DUMMY_PROJECT_OUTPUT_DIR)
        print(f"Removed: {DUMMY_PROJECT_OUTPUT_DIR}")
    if os.path.exists(OUTPUT_APKS_DIR):
        # Clean up individual APKs, but keep the directory for potential future use if needed
        for item in os.listdir(OUTPUT_APKS_DIR):
            item_path = os.path.join(OUTPUT_APKS_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        print(f"Cleaned up contents of: {OUTPUT_APKS_DIR}")

    print("\n--- All Demos Finished ---")