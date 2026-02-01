import os
import re
import shutil
import subprocess
from datetime import datetime

# --- Constants ---
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
OUTPUT_APKS_DIR = "generated_apks"
JAVA_SOURCE_DIR = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "generatedapp")
MANIFEST_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "AndroidManifest.xml")
GRADLE_BUILD_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "build.gradle")

# --- Helper Functions ---

def cleanup_dummy_files():
    """Removes temporary files and directories created during the process."""
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        print(f"Removed dummy Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
    if os.path.exists(OUTPUT_APKS_DIR):
        shutil.rmtree(OUTPUT_APKS_DIR)
        print(f"Removed dummy output APK directory: {OUTPUT_APKS_DIR}")

def create_android_project_structure():
    """Creates a basic Android project structure as a template."""
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)

    os.makedirs(JAVA_SOURCE_DIR, exist_ok=True)

    # Create a dummy AndroidManifest.xml
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.generatedapp">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Create a dummy build.gradle (app level)
    gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.generatedapp'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.generatedapp"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
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
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    with open(GRADLE_BUILD_PATH, "w", encoding="utf-8") as f:
        f.write(gradle_content)

    print("Created basic Android project structure.")

def generate_main_activity_code(app_name, description):
    """Generates the Java code for MainActivity based on app_name and description."""
    activity_name = "MainActivity.java"
    java_file_path = os.path.join(JAVA_SOURCE_DIR, activity_name)

    # A very simple parsing of description for potential UI elements (highly simplified)
    # In a real scenario, this would be much more sophisticated NLP.
    layout_elements = []
    if "button" in description.lower():
        layout_elements.append("Button submitButton = findViewById(R.id.submitButton);")
        layout_elements.append("submitButton.setText(\"Submit\");")
    if "text" in description.lower():
        layout_elements.append("TextView messageText = findViewById(R.id.messageText);")
        layout_elements.append("messageText.setText(\"Welcome to " + app_name + "!\");")

    activity_content = f"""
package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Dynamically generated UI elements based on description
        {''.join([f'{elem}\n        ' for elem in layout_elements])}

        // You can add more logic here based on parsed natural language
    }}
}}
"""
    with open(java_file_path, "w", encoding="utf-8") as f:
        f.write(activity_content)
    print(f"Generated {activity_name}")
    return java_file_path

def generate_layout_file(app_name, description):
    """Generates a basic activity_main.xml layout file."""
    layout_dir = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout")
    os.makedirs(layout_dir, exist_ok=True)
    layout_file_path = os.path.join(layout_dir, "activity_main.xml")

    # Simple parsing for layout elements
    layout_xml_elements = []
    if "button" in description.lower():
        layout_xml_elements.append('<Button android:id="@+id/submitButton" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Default Button" app:layout_constraintTop_toBottomOf="@id/messageText" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent" />')
    if "text" in description.lower():
        layout_xml_elements.append('<TextView android:id="@+id/messageText" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Loading..." android:textSize="24sp" app:layout_constraintTop_toTopOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintBottom_toTopOf="@id/submitButton" />')

    layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    {''.join([f'{elem}\n    ' for elem in layout_xml_elements])}

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(layout_file_path, "w", encoding="utf-8") as f:
        f.write(layout_content)
    print(f"Generated layout file: {layout_file_path}")
    return layout_file_path

def compile_apk(app_name):
    """Compiles the Android project into an APK."""
    os.makedirs(OUTPUT_APKS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    apk_filename = f"{app_name.replace(' ', '_').lower()}_{timestamp}.apk"
    apk_output_path = os.path.join(OUTPUT_APKS_DIR, apk_filename)

    # This assumes you have the Android SDK and Gradle installed and configured
    # in your PATH.
    # A more robust solution would involve specifying the SDK path and using
    # Gradle wrapper.
    try:
        print(f"Attempting to build APK for '{app_name}'...")
        # Navigate to the project directory
        original_cwd = os.getcwd()
        os.chdir(ANDROID_PROJECT_TEMPLATE_DIR)

        # Run the Gradle build command
        # Using './gradlew' assumes gradlew exists. If not, you might need 'gradlew' directly or 'gradle'
        build_command = ["./gradlew", "assembleDebug", "-q"] # -q for quiet
        process = subprocess.run(build_command, capture_output=True, text=True, check=True)

        # Find the generated APK (usually in app/build/outputs/apk/debug/)
        debug_apk_path = os.path.join("app", "build", "outputs", "apk", "debug", "app-debug.apk")
        if os.path.exists(debug_apk_path):
            shutil.move(debug_apk_path, os.path.join("..", "..", "..", "..", apk_output_path)) # Move to OUTPUT_APKS_DIR
            print(f"APK successfully generated at: {apk_output_path}")
            return apk_output_path
        else:
            print("Error: Could not find the generated APK.")
            print("Gradle build output:")
            print(process.stdout)
            print(process.stderr)
            return None

    except FileNotFoundError:
        print("Error: './gradlew' command not found. Please ensure you have the Android SDK and Gradle installed and in your PATH, or use the Gradle wrapper.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during APK compilation: {e}")
        return None
    finally:
        # Return to the original directory
        os.chdir(original_cwd)

# --- Main Lobe Function ---

def arabic_apk_generator(natural_language_prompt: str) -> str:
    """
    Parses an Arabic natural language prompt to generate an Android APK.

    Args:
        natural_language_prompt: The Arabic text describing the desired app.

    Returns:
        The path to the generated APK file, or an error message.
    """
    print(f"\n--- Starting Arabic APK Generation for prompt: '{natural_language_prompt}' ---")

    # --- Step 1: Parse Arabic Prompt ---
    # This is a highly simplified placeholder for advanced NLP.
    # In a real scenario, this would involve:
    # - Tokenization
    # - Part-of-Speech Tagging
    # - Named Entity Recognition (for app name, features, etc.)
    # - Intent Recognition (what kind of app is it?)
    # - Semantic Role Labeling (what are the components and their actions?)

    app_name = "MyArabicApp" # Default app name
    app_description = ""

    # Simple keyword extraction for app name and basic features
    # This is extremely rudimentary and would need a robust Arabic NLP library.
    # Example: If prompt contains "تطبيق اسمه" (app named), extract the following word(s).
    # Example: If prompt contains "يحتوي على زر" (contains a button), set a flag.
    # Example: If prompt contains "يعرض نص" (displays text), set a flag.

    # A very basic attempt to extract an app name if specified
    name_match = re.search(r"تطبيق اسمه\s+([\w\s]+)", natural_language_prompt, re.IGNORECASE)
    if name_match:
        app_name = name_match.group(1).strip()
        app_description = natural_language_prompt # Use the full prompt for description for now

    # Basic feature detection
    has_button = "زر" in natural_language_prompt or "أزرار" in natural_language_prompt
    has_text_display = "نص" in natural_language_prompt or "يعرض" in natural_language_prompt or "رسالة" in natural_language_prompt

    # Construct a more descriptive string for code generation (simplified)
    description_parts = []
    if has_button:
        description_parts.append("a button")
    if has_text_display:
        description_parts.append("a text display")

    if not description_parts:
        app_description = f"A simple app named {app_name}"
    else:
        app_description = f"A simple app named {app_name} that has {' and '.join(description_parts)}."

    print(f"Parsed App Name: {app_name}")
    print(f"Parsed Description: {app_description}")

    # --- Step 2: Build Android Project Structure ---
    print("\n--- Building Android Project Structure ---")
    create_android_project_structure()

    # --- Step 3: Generate Code based on parsed prompt ---
    print("\n--- Generating Java Code ---")
    generated_activity_path = generate_main_activity_code(app_name, app_description)

    print("\n--- Generating Layout File ---")
    generated_layout_path = generate_layout_file(app_name, app_description)

    # Update AndroidManifest.xml if needed (e.g., app name)
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest_content = f.read()
        manifest_content = manifest_content.replace('package="com.example.generatedapp"', f'package="com.example.{app_name.lower().replace(" ", "")}"')
        manifest_content = re.sub(r'<application[^>]*\n.*label="@string/app_name"', f'<application\n        android:label="{app_name}"', manifest_content, flags=re.DOTALL)
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"Updated AndroidManifest.xml with app name: {app_name}")
    except Exception as e:
        print(f"Error updating AndroidManifest.xml: {e}")


    # --- Step 4: Compile APK ---
    print("\n--- Compiling APK ---")
    generated_apk_path = compile_apk(app_name)

    # --- Step 5: Output and Cleanup ---
    if generated_apk_path:
        print(f"\n--- APK Generation Complete ---")
        print(f"Generated APK at: {generated_apk_path}")
    else:
        print(f"\n--- APK Generation Failed ---")
        print(f"Error: Failed to generate APK for prompt: '{natural_language_prompt}'")

    # Final cleanup (optional, can be controlled by a flag)
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()

    print("\n--- Arabic APK Generator Module Finished ---")
    return generated_apk_path if generated_apk_path else "Error: APK generation failed."

if __name__ == '__main__':
    # Example Usage
    test_prompt_arabic_1 = "أريد تطبيق اسمه تطبيق الترحيب يعرض رسالة ترحيبية ونص ترحيبي."
    print(f"Testing with prompt: {test_prompt_arabic_1}")
    result_apk_path_1 = arabic_apk_generator(test_prompt_arabic_1)
    print(f"Result for prompt 1: {result_apk_path_1}")

    print("\n" + "="*50 + "\n")

    test_prompt_arabic_2 = "بناء تطبيق بسيط يحتوي على زر."
    print(f"Testing with prompt: {test_prompt_arabic_2}")
    result_apk_path_2 = arabic_apk_generator(test_prompt_arabic_2)
    print(f"Result for prompt 2: {result_apk_path_2}")

    print("\n" + "="*50 + "\n")

    test_prompt_arabic_3 = "إنشاء تطبيق جديد باسم 'حاسبتي' مع نص." # Test explicit name extraction
    print(f"Testing with prompt: {test_prompt_arabic_3}")
    result_apk_path_3 = arabic_apk_generator(test_prompt_arabic_3)
    print(f"Result for prompt 3: {result_apk_path_3}")