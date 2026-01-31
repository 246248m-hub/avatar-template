import os
import shutil
import subprocess
from pathlib import Path

# Assuming these directories are defined elsewhere
ANDROID_PROJECTS_DIR = Path("dummy_android_projects")
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
OUTPUT_DIR = Path("output")

def create_dummy_android_project(app_name: str, package_name: str) -> Path:
    """
    Creates a dummy Android project structure.
    In a real scenario, this would involve using Android SDK tools or templates.
    For this demo, we'll create a minimal directory structure.
    """
    project_path = ANDROID_PROJECTS_DIR / f"{app_name.replace(' ', '_').lower()}"
    project_path.mkdir(parents=True, exist_ok=True)

    # Create typical Android project subdirectories and minimal files
    (project_path / "app").mkdir(exist_ok=True)
    (project_path / "app" / "src").mkdir(exist_ok=True)
    (project_path / "app" / "src" / "main").mkdir(exist_ok=True)
    (project_path / "app" / "src" / "main" / "java").mkdir(exist_ok=True)
    (project_path / "app" / "src" / "main" / "java" / package_name.replace('.', os.sep)).mkdir(parents=True, exist_ok=True)

    # Create a dummy manifest
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">
    <application android:label="{app_name}" />
</manifest>
"""
    (project_path / "app" / "src" / "main" / "AndroidManifest.xml").write_text(manifest_content)

    # Create a dummy MainActivity
    activity_dir = project_path / "app" / "src" / "main" / "java" / package_name.replace('.', os.sep)
    activity_content = f"""package {package_name};

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // setContentView(R.layout.activity_main); // In a real app
    }}
}}
"""
    (activity_dir / "MainActivity.java").write_text(activity_content)

    # Create dummy build.gradle files
    build_gradle_app_content = """
plugins {
    id 'com.android.application'
}
android {
    compileSdk 33
    defaultConfig {
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}
dependencies {{
    // Add dependencies if needed
}}
"""
    (project_path / "app" / "build.gradle").write_text(build_gradle_app_content.format(package_name=package_name))

    build_gradle_project_content = """
plugins {{
    id 'com.android.application' version '7.3.0' apply false
    id 'com.android.library' version '7.3.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.7.10' apply false
}}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
task clean(type: Delete) {
    delete rootProject.buildDir
}
"""
    (project_path / "build.gradle").write_text(build_gradle_project_content)

    # Create settings.gradle
    settings_gradle_content = f"""pluginManagement {{
    repositories {{
        gradlePluginPortal()
        google()
        mavenCentral()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{app_name.replace(' ', '_').lower()}"
include ':app'
"""
    (project_path / "settings.gradle").write_text(settings_gradle_content)


    print(f"Dummy Android project created at: {project_path}")
    return project_path

def cleanup_dummy_files_and_dirs():
    """Cleans up dummy files and directories."""
    if ANDROID_PROJECTS_DIR.exists():
        shutil.rmtree(ANDROID_PROJECTS_DIR)
        print(f"Removed directory: {ANDROID_PROJECTS_DIR}")
    if KNOWLEDGE_BASE_DIR.exists():
        # Specific cleanup for Arabic Parser and Generator Module Demo
        for item in KNOWLEDGE_BASE_DIR.iterdir():
            if item.is_file() and item.name.endswith(".txt"):
                try:
                    item.unlink()
                    print(f"Removed file: {item}")
                except OSError as e:
                    print(f"Error removing file {item}: {e}")
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
        print(f"Removed directory: {OUTPUT_DIR}")


def build_android_apk(project_path: Path, output_apk_path: Path):
    """
    Builds an Android APK from the project path.
    This function assumes the Android SDK (specifically the `gradlew` wrapper) is available.
    """
    print(f"\n--- Attempting to build APK for project at: {project_path} ---")
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return

    # Navigate to the project directory
    original_dir = os.getcwd()
    os.chdir(project_path)

    # Ensure the output directory exists
    output_apk_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Execute the Gradle build command
        # This command assumes a standard Android project structure with a gradlew wrapper
        # On Windows, it might be 'gradlew.bat'
        gradlew_command = ["./gradlew", "assembleDebug"] # Using debug build for simplicity
        if os.name == 'nt': # For Windows
            gradlew_command = ["gradlew.bat", "assembleDebug"]

        print(f"Running command: {' '.join(gradlew_command)}")
        result = subprocess.run(gradlew_command, capture_output=True, text=True, check=True)
        print("Gradle build output:\n", result.stdout)

        # Find the generated APK. The exact path depends on the Gradle build configuration.
        # Common locations are app/build/outputs/apk/debug/app-debug.apk
        debug_apk_path = project_path / "app" / "build" / "outputs" / "apk" / "debug" / f"{project_path.name}-debug.apk"

        if debug_apk_path.exists():
            # Move the generated APK to the desired output location
            shutil.move(str(debug_apk_path), str(output_apk_path))
            print(f"Successfully built and moved APK to: {output_apk_path}")
        else:
            print(f"Error: APK file not found at expected location: {debug_apk_path}")
            print("Please check Gradle build output for clues.")

    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("Stderr:\n", e.stderr)
        print("Stdout:\n", e.stdout)
    except FileNotFoundError:
        print("Error: gradlew command not found. Ensure the Android SDK and Gradle are installed and accessible.")
    except Exception as e:
        print(f"An unexpected error occurred during APK building: {e}")
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

    print("\n--- APK Builder Module Finished ---")

# --- Arabic Parser and Generator Module ---
def parse_arabic_text(text: str, knowledge_base_dir: Path) -> dict:
    """
    Parses Arabic text to extract structured information.
    This is a placeholder. In a real system, this would involve NLP libraries
    for Arabic language processing (e.g., CAMeL Tools, Farasa, NLTK with Arabic support).
    It should identify intents, entities, and generate a structured representation.
    """
    print(f"\n--- Parsing Arabic text: '{text[:50]}...' ---")
    # Simulate parsing by returning a dictionary based on keywords
    parsed_data = {
        "intent": "unknown",
        "entities": {},
        "original_text": text
    }
    text_lower = text.lower()

    if "إنشاء تطبيق" in text_lower or "create app" in text_lower:
        parsed_data["intent"] = "create_app"
        # Example: Extracting app name and package name
        if "اسم التطبيق" in text_lower:
            app_name_match = text_lower.split("اسم التطبيق")[1].strip()
            if ":" in app_name_match:
                parsed_data["entities"]["app_name"] = app_name_match.split(":")[1].strip().split(',')[0]
            else:
                parsed_data["entities"]["app_name"] = app_name_match.split()[0] # Simple split

        if "حزمة التطبيق" in text_lower or "package" in text_lower:
            package_name_match = text_lower.split("حزمة التطبيق")[1].strip() if "حزمة التطبيق" in text_lower else text_lower.split("package")[1].strip()
            if ":" in package_name_match:
                 parsed_data["entities"]["package_name"] = package_name_match.split(":")[1].strip().split(',')[0]
            else:
                 parsed_data["entities"]["package_name"] = package_name_match.split()[0]

    elif "عرض" in text_lower or "show" in text_lower:
        parsed_data["intent"] = "display_info"
        # Example: Extracting what to display
        if "قائمة المهام" in text_lower:
            parsed_data["entities"]["display_item"] = "task_list"
        elif "الإعدادات" in text_lower:
            parsed_data["entities"]["display_item"] = "settings"

    # Simulate loading some generic Arabic knowledge
    # In a real scenario, this would query a sophisticated knowledge base
    example_knowledge = {
        "arabic_greetings": ["مرحبا", "أهلا", "السلام عليكم"],
        "arabic_farewells": ["وداعا", "مع السلامة", "إلى اللقاء"],
        "task_keywords": ["مهمة", "واجب", "عمل"]
    }
    # Save/load logic would be here for a real KB, for demo just use in-memory
    # knowledge_base_dir is provided for conceptual integration

    print(f"Parsed data: {parsed_data}")
    return parsed_data

def generate_arabic_response(parsed_data: dict) -> str:
    """
    Generates an Arabic natural language response based on parsed data.
    This is a placeholder for natural language generation (NLG).
    """
    print(f"\n--- Generating Arabic response for intent: {parsed_data.get('intent')} ---")
    intent = parsed_data.get("intent", "unknown")
    entities = parsed_data.get("entities", {})
    response = ""

    if intent == "create_app":
        app_name = entities.get("app_name", "تطبيق جديد")
        package_name = entities.get("package_name", "com.example.newapp")
        response = f"بالتأكيد، سأقوم بإنشاء تطبيق باسم \"{app_name}\" وحزمة التطبيق \"{package_name}\"."
        if "app_name" not in entities or "package_name" not in entities:
            response += " يرجى توفير اسم التطبيق وحزمة التطبيق لإنشاء التطبيق."
    elif intent == "display_info":
        display_item = entities.get("display_item", "المعلومات المطلوبة")
        response = f"حسناً، سأعرض لك {display_item}."
    elif intent == "unknown":
        response = "عذراً، لم أفهم طلبك. هل يمكنك إعادة الصياغة؟"
    else:
        response = f"لقد فهمت أنك تريد القيام بـ {intent}."

    print(f"Generated response: {response}")
    return response

# --- Demo Usage ---

if __name__ == "__main__":
    # --- Arabic Parser and Generator Module Demo ---
    print("\n--- Arabic Parser and Generator Module Demo ---")

    arabic_prompt_1 = "إنشاء تطبيق جديد باسم 'مدير المهام' وحزمة التطبيق 'com.example.taskmanager'"
    parsed_output_1 = parse_arabic_text(arabic_prompt_1, KNOWLEDGE_BASE_DIR)
    generated_response_1 = generate_arabic_response(parsed_output_1)

    arabic_prompt_2 = "أريد عرض قائمة المهام الخاصة بي."
    parsed_output_2 = parse_arabic_text(arabic_prompt_2, KNOWLEDGE_BASE_DIR)
    generated_response_2 = generate_arabic_response(parsed_output_2)

    arabic_prompt_3 = "ما هي الإعدادات المتاحة؟"
    parsed_output_3 = parse_arabic_text(arabic_prompt_3, KNOWLEDGE_BASE_DIR)
    generated_response_3 = generate_arabic_response(parsed_output_3)

    arabic_prompt_4 = "حدث خطأ غير متوقع."
    parsed_output_4 = parse_arabic_text(arabic_prompt_4, KNOWLEDGE_BASE_DIR)
    generated_response_4 = generate_arabic_response(parsed_output_4)

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

    # --- APK Builder Module Demo ---
    print("\n--- APK Builder Module Demo ---")

    # Create dummy projects
    app_name_1 = "My Task Manager"
    package_name_1 = "com.example.taskmanager"
    dummy_project_path_1 = create_dummy_android_project(app_name_1, package_name_1)

    app_name_2 = "Simple Calculator"
    package_name_2 = "com.example.calculator"
    dummy_project_path_2 = create_dummy_android_project(app_name_2, package_name_2)

    # Define output paths for APKs
    output_apk_1 = OUTPUT_DIR / f"{package_name_1.replace('.', '_')}.apk"
    output_apk_2 = OUTPUT_DIR / f"{package_name_2.replace('.', '_')}.apk"

    # Build APKs (this part requires Android SDK setup and might take time)
    # NOTE: This will only work if you have the Android SDK and Gradle configured.
    # The dummy project creation is a placeholder for the structure.
    # For demonstration purposes, we'll skip the actual build if gradlew is not found.
    try:
        subprocess.run(["gradlew", "--version"], check=True, capture_output=True) # Check if gradlew is available
        build_android_apk(dummy_project_path_1, output_apk_1)
        build_android_apk(dummy_project_path_2, output_apk_2)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\n--- Skipping actual APK build: gradlew command not found or not configured. ---")
        print("This demo requires the Android SDK and Gradle to be set up.")
        print("The dummy project structure is created, but the APK compilation step is skipped.")

    # --- Cleanup ---
    cleanup_dummy_files_and_dirs()
    print("\n--- APK Builder Module Demo Finished ---")