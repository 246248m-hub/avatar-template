import os
import re
import shutil
import subprocess

# Define constants for Arabic processing
ARABIC_CHARS = "[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]"

# --- Lobe 0: Arabic Language Processing ---

def is_arabic_text(text):
    """Checks if the given text contains Arabic characters."""
    return bool(re.search(ARABIC_CHARS, text))

def extract_arabic_app_name(prompt):
    """
    Extracts a potential application name from an Arabic prompt.
    Looks for phrases like "تطبيق جديد باسم '...'".
    """
    match = re.search(r"تطبيق جديد باسم ['\"]([^'\"]+)['\"]", prompt)
    if match:
        return match.group(1)
    return None

def parse_arabic_prompt(prompt):
    """
    Parses an Arabic prompt to extract app name and core functionality.
    This is a simplified parser; a more robust one would involve NLP libraries.
    """
    app_name = extract_arabic_app_name(prompt)
    if not app_name:
        # If no explicit name, try to infer from the prompt itself
        # This is a very basic inference, more advanced NLP is needed
        app_name = "MyArabicApp" # Default name if not found

    # Attempt to identify keywords for functionality
    functionality_keywords = {
        "حاسبة": "calculator",
        "ملاحظات": "notes",
        "قائمة مهام": "todo_list",
        "معرض صور": "image_gallery",
        "مترجم": "translator"
    }
    found_functionality = "basic_ui" # Default functionality

    for keyword, func_type in functionality_keywords.items():
        if keyword in prompt:
            found_functionality = func_type
            break

    return {"app_name": app_name, "functionality": found_functionality, "original_prompt": prompt}

# --- Lobe 4: Code Generation ---

def generate_android_code_from_description(description):
    """
    Generates basic Android (Java/Kotlin) code structure based on a description.
    This is a placeholder for a more sophisticated code generator.
    It will create a minimal MainActivity.java and a basic layout.
    """
    app_name = description.get("app_name", "MyGeneratedApp")
    functionality = description.get("functionality", "basic_ui")

    # Create Java code for MainActivity
    java_code = f"""
package com.example.{app_name.lower().replace(' ', '_')};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView welcomeText = findViewById(R.id.welcome_text);
        welcomeText.setText("Welcome to {app_name}!");

        // Placeholder for functionality
        switch ("{functionality}") {{
            case "calculator":
                // Add calculator specific UI and logic
                break;
            case "notes":
                // Add notes specific UI and logic
                break;
            case "todo_list":
                // Add todo list specific UI and logic
                break;
            case "image_gallery":
                // Add image gallery specific UI and logic
                break;
            case "translator":
                // Add translator specific UI and logic
                break;
            default:
                // Default UI for basic_ui
                break;
        }}
    }}
}}
"""

    # Create XML layout for activity_main.xml
    xml_layout = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

    # Create AndroidManifest.xml
    manifest_xml = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_name.lower().replace(' ', '_')}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name.replace(' ', '')}">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

    # Create strings.xml
    strings_xml = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""

    return {
        "java_main_activity": java_code,
        "xml_activity_main": xml_layout,
        "xml_manifest": manifest_xml,
        "xml_strings": strings_xml,
        "package_name": f"com.example.{app_name.lower().replace(' ', '_')}",
        "app_name_for_theme": app_name.replace(' ', '')
    }

# --- Lobe 8: APK Compiler ---

def create_android_project_structure(project_dir, code_files, package_name, app_name_for_theme):
    """
    Creates a minimal Android project directory structure and places generated files.
    """
    app_src_dir = os.path.join(project_dir, "app", "src", "main")
    java_package_dir = os.path.join(app_src_dir, "java", *package_name.split('.'))
    res_layout_dir = os.path.join(app_src_dir, "res", "layout")
    res_values_dir = os.path.join(app_src_dir, "res", "values")
    res_mipmap_dir = os.path.join(app_src_dir, "res", "mipmap-hdpi") # Minimal requirement

    os.makedirs(java_package_dir, exist_ok=True)
    os.makedirs(res_layout_dir, exist_ok=True)
    os.makedirs(res_values_dir, exist_ok=True)
    os.makedirs(res_mipmap_dir, exist_ok=True) # Create mipmap directory

    # Write Java MainActivity
    with open(os.path.join(java_package_dir, "MainActivity.java"), "w", encoding="utf-8") as f:
        f.write(code_files["java_main_activity"])

    # Write XML layout
    with open(os.path.join(res_layout_dir, "activity_main.xml"), "w", encoding="utf-8") as f:
        f.write(code_files["xml_activity_main"])

    # Write Manifest
    with open(os.path.join(app_src_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(code_files["xml_manifest"])

    # Write Strings
    with open(os.path.join(res_values_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write(code_files["xml_strings"])

    # Create dummy ic_launcher.png (required for build)
    dummy_icon_path = os.path.join(res_mipmap_dir, "ic_launcher.png")
    if not os.path.exists(dummy_icon_path):
        # Create a minimal placeholder if it doesn't exist
        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color = (255, 0, 0))
            img.save(dummy_icon_path)
        except ImportError:
            print("Pillow not installed. Cannot create dummy icon. Please install Pillow: pip install Pillow")
            # As a fallback, create an empty file if Pillow is not available
            with open(dummy_icon_path, "w") as f:
                pass # Create an empty file

    # Create a dummy build.gradle file (minimal for structure)
    build_gradle_content = f"""
plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
}}
"""
    with open(os.path.join(project_dir, "app", "build.gradle"), "w", encoding="utf-8") as f:
        f.write(build_gradle_content)

    # Create a dummy settings.gradle
    settings_gradle_content = f"""
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{app_name_for_theme}"
include ':app'
"""
    with open(os.path.join(project_dir, "settings.gradle"), "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)

    # Create a dummy root build.gradle
    root_build_gradle_content = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2' // Example version
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
"""
    with open(os.path.join(project_dir, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(root_build_gradle_content)


def build_apk(project_dir, output_dir):
    """
    Builds an APK using Gradle.
    Requires Android SDK and Gradle to be installed and configured.
    """
    print(f"Attempting to build APK for project at: {project_dir}")
    os.makedirs(output_dir, exist_ok=True)

    # Locate Gradle wrapper
    gradle_wrapper_path = os.path.join(project_dir, "gradlew")
    if not os.path.exists(gradle_wrapper_path):
        # If gradlew is not found, assume it's an environment where Gradle is in PATH
        gradle_command = "gradlew"
        print("Using 'gradlew' command. Ensure it's in your PATH or located in the project.")
    else:
        gradle_command = gradle_wrapper_path
        # Make sure gradlew is executable
        os.chmod(gradle_wrapper_path, 0o755)

    # Command to build the APK
    # Using ':app:assembleDebug' for a debug APK. For release, use ':app:assembleRelease'
    # and ensure signing configurations are set up.
    command = [gradle_command, "clean", "assembleDebug"]

    try:
        # Execute the command in the project directory
        process = subprocess.Popen(command, cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error building APK:\n{stderr.decode('utf-8')}")
            return None
        else:
            print("APK build successful.")
            # Find the generated APK file
            # The exact path can vary slightly based on Gradle version and build type
            # Common path: app/build/outputs/apk/debug/app-debug.apk
            debug_apk_path = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
            if os.path.exists(debug_apk_path):
                apk_filename = os.path.basename(debug_apk_path)
                final_apk_path = os.path.join(output_dir, apk_filename)
                shutil.copy(debug_apk_path, final_apk_path)
                print(f"APK saved to: {final_apk_path}")
                return final_apk_path
            else:
                print("Could not find the generated APK file at expected location.")
                return None

    except FileNotFoundError:
        print("Error: 'gradlew' command not found. Make sure Gradle is installed and in your PATH, or the gradlew script exists.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during APK build: {e}")
        return None

# --- Main Arabic APK Generator Function ---

def arabic_apk_generator(prompt):
    """
    Parses an Arabic prompt, generates code, builds a minimal Android project,
    and compiles it into an APK.
    """
    print(f"\n--- Processing Arabic Prompt: '{prompt}' ---")

    # Lobe 0: Parse the Arabic prompt
    if not is_arabic_text(prompt):
        print("Prompt does not appear to be in Arabic. Skipping.")
        return None

    description = parse_arabic_prompt(prompt)
    print(f"Parsed description: {description}")

    # Lobe 4: Generate Android code
    code_files = generate_android_code_from_description(description)
    print("Generated Android code structure.")

    # Lobe 8: Create project structure and compile APK
    # Use a temporary directory for the Android project
    TEMP_PROJECT_DIR = "./temp_android_project"
    OUTPUT_APKS_DIR = "./generated_apks"

    # Clean up previous temporary project if it exists
    if os.path.exists(TEMP_PROJECT_DIR):
        shutil.rmtree(TEMP_PROJECT_DIR)
        print(f"Cleaned up previous temporary project directory: {TEMP_PROJECT_DIR}")

    os.makedirs(TEMP_PROJECT_DIR, exist_ok=True)
    print(f"Created temporary project directory: {TEMP_PROJECT_DIR}")

    create_android_project_structure(
        TEMP_PROJECT_DIR,
        code_files,
        code_files["package_name"],
        code_files["app_name_for_theme"]
    )
    print("Created Android project structure with generated files.")

    # Build the APK
    apk_path = build_apk(TEMP_PROJECT_DIR, OUTPUT_APKS_DIR)

    # Clean up the temporary project directory after build
    if os.path.exists(TEMP_PROJECT_DIR):
        shutil.rmtree(TEMP_PROJECT_DIR)
        print(f"Cleaned up temporary project directory: {TEMP_PROJECT_DIR}")

    if apk_path:
        print(f"Successfully generated APK: {apk_path}")
    else:
        print("Failed to generate APK.")

    return apk_path

# Example Usage (for demonstration purposes, not part of the final output)
if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs("./generated_apks", exist_ok=True)

    # --- Test Case 1: Basic Arabic prompt with implied name ---
    test_prompt_arabic_1 = "إنشاء تطبيق جديد يعرض رسالة ترحيب."
    print(f"\n--- Testing with prompt: '{test_prompt_arabic_1}' ---")
    result_apk_path_1 = arabic_apk_generator(test_prompt_arabic_1)
    print(f"Result for prompt 1: {result_apk_path_1}")

    # --- Test Case 2: Arabic prompt with explicit name and functionality ---
    test_prompt_arabic_2 = "أنشئ لي تطبيق مترجم عربي جديد باسم 'مترجمي'."
    print(f"\n--- Testing with prompt: '{test_prompt_arabic_2}' ---")
    result_apk_path_2 = arabic_apk_generator(test_prompt_arabic_2)
    print(f"Result for prompt 2: {result_apk_path_2}")

    # --- Test Case 3: Arabic prompt with explicit name and functionality ---
    test_prompt_arabic_3 = "إنشاء تطبيق جديد باسم 'حاسبتي' ليكون حاسبة."
    print(f"\n--- Testing with prompt: '{test_prompt_arabic_3}' ---")
    result_apk_path_3 = arabic_apk_generator(test_prompt_arabic_3)
    print(f"Result for prompt 3: {result_apk_path_3}")

    # --- Test Case 4: Non-Arabic prompt ---
    test_prompt_english = "Create a new app called 'My App'."
    print(f"\n--- Testing with prompt: '{test_prompt_english}' ---")
    result_apk_path_4 = arabic_apk_generator(test_prompt_english)
    print(f"Result for prompt 4: {result_apk_path_4}")

    print("\n--- Arabic APK Generator Module Demo Finished ---")

    # Clean up generated APKs directory if desired
    # if os.path.exists("./generated_apks"):
    #     shutil.rmtree("./generated_apks")
    #     print("Cleaned up generated APKs directory.")