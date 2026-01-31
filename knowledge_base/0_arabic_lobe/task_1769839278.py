import os
import shutil
import subprocess
import sys

# --- Constants ---
TEMP_PROJECT_DIR = "temp_android_project"
MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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

GRADLE_PROPERTIES_TEMPLATE = """org.gradle.jvmargs=-Xmx2048m
"""

BUILD_GRADLE_APP_TEMPLATE = """plugins {{
    id 'com.android.application'
    id 'kotlin-android'
}}

android {{
    namespace "{package_name}"
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.ext.junit.runners.AndroidJUnitRunner'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""

BUILD_GRADLE_PROJECT_TEMPLATE = """plugins {{
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.0' apply false
}}
"""

SETTINGS_GRADLE_TEMPLATE = """pluginManagement {{
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

rootProject.name = "{project_name}"
include ':app'
"""

ACTIVITY_TEMPLATE = """package {package_name};

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

LAYOUT_ACTIVITY_MAIN_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

STRINGS_TEMPLATE = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""

# --- Helper Functions ---

def create_android_project_structure(project_root, package_name, app_name):
    """Creates the basic directory structure for an Android project."""
    print(f"--- Creating Android project structure in: {project_root} ---")
    os.makedirs(os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.')), exist_ok=True)
    os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "values"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "app", "src", "test", "java", *package_name.split('.')), exist_ok=True)
    os.makedirs(os.path.join(project_root, "app", "src", "androidTest", "java", *package_name.split('.')), exist_ok=True)

    # Create essential files
    with open(os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(MANIFEST_TEMPLATE.format(package_name=package_name))

    with open(os.path.join(project_root, "app", "build.gradle"), "w", encoding="utf-8") as f:
        f.write(BUILD_GRADLE_APP_TEMPLATE.format(package_name=package_name))

    with open(os.path.join(project_root, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(BUILD_GRADLE_PROJECT_TEMPLATE)

    with open(os.path.join(project_root, "settings.gradle"), "w", encoding="utf-8") as f:
        f.write(SETTINGS_GRADLE_TEMPLATE.format(project_name=app_name.replace(" ", "").lower()))

    with open(os.path.join(project_root, "gradle.properties"), "w", encoding="utf-8") as f:
        f.write(GRADLE_PROPERTIES_TEMPLATE)

    # Create placeholder files if they don't exist
    activity_path = os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.'), "MainActivity.java")
    if not os.path.exists(activity_path):
        with open(activity_path, "w", encoding="utf-8") as f:
            f.write(ACTIVITY_TEMPLATE.format(package_name=package_name))

    layout_path = os.path.join(project_root, "app", "src", "main", "res", "layout", "activity_main.xml")
    if not os.path.exists(layout_path):
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(LAYOUT_ACTIVITY_MAIN_TEMPLATE)

    strings_path = os.path.join(project_root, "app", "src", "main", "res", "values", "strings.xml")
    if not os.path.exists(strings_path):
        with open(strings_path, "w", encoding="utf-8") as f:
            f.write(STRINGS_TEMPLATE.format(app_name=app_name))

    print("Android project structure created.")

def build_apk(project_dir, output_apk_path):
    """Builds the APK from the given Android project directory."""
    print(f"--- Building APK from: {project_dir} ---")
    if not os.path.exists(os.path.join(project_dir, "gradlew")):
        print("Error: gradlew not found. Make sure it's in the project root.")
        return False

    # Ensure gradlew is executable
    os.chmod(os.path.join(project_dir, "gradlew"), 0o755)

    try:
        # Execute the Gradle build command
        # Using 'assembleDebug' for easier testing, can be changed to 'assembleRelease'
        result = subprocess.run(
            [os.path.join(project_dir, "gradlew"), "assembleDebug"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )
        print("Gradle build output:")
        print(result.stdout)
        print(result.stderr)

        # Find the generated APK
        # APKs are typically found in app/build/outputs/apk/debug/
        debug_apk_dir = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")
        apk_files = [f for f in os.listdir(debug_apk_dir) if f.endswith(".apk")]

        if not apk_files:
            print(f"Error: No APK file found in {debug_apk_dir}")
            return False

        # Assume the first found APK is the one we want, or specify a name if needed
        generated_apk_path = os.path.join(debug_apk_dir, apk_files[0])
        shutil.move(generated_apk_path, output_apk_path)
        print(f"APK successfully built and moved to: {output_apk_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("Stderr:\n", e.stderr)
        print("Stdout:\n", e.stdout)
        return False
    except FileNotFoundError:
        print("Error: Gradle wrapper (gradlew) not found. Ensure it's present in the project root.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during APK build: {e}")
        return False

# --- Main Functional Module ---

def generate_arabic_nlp_apk(natural_language_input: str, output_apk_path: str) -> str:
    """
    Processes natural language input to generate an Android APK.
    This function acts as the core orchestrator for the APK generation process,
    integrating NLP Arabic processing with APK compilation.

    Args:
        natural_language_input (str): The natural language description of the desired APK.
        output_apk_path (str): The desired path for the generated APK file.

    Returns:
        str: A message indicating success or failure, including the path to the APK if successful.
    """
    print("\n--- Initiating Lobe 8_apk_compiler_lobe Functionality ---")

    # --- Placeholder for Arabic NLP Processing ---
    # In a real scenario, this section would involve Lobe 0 (arabic_lobe) and
    # potentially other NLP lobes to parse the `natural_language_input`.
    # For this demonstration, we'll extract basic information and create a simple app.

    # Example parsing: Extracting app name and package name.
    # This is a highly simplified example. A real NLP module would be far more complex.
    # We'll assume the input contains keywords like "app name" and "package".
    app_name = "MyArabicApp"  # Default app name
    package_name = "com.example.myarabicapp" # Default package name

    if "app name" in natural_language_input.lower():
        try:
            parts = natural_language_input.lower().split("app name")
            if len(parts) > 1:
                app_name_part = parts[1].split("package")[0].strip()
                if app_name_part:
                    app_name = app_name_part.title().replace(" ", "") # Simple title casing and space removal
        except Exception as e:
            print(f"Warning: Could not parse app name from input. Using default. Error: {e}")

    if "package" in natural_language_input.lower():
        try:
            parts = natural_language_input.lower().split("package")
            if len(parts) > 1:
                pkg_part = parts[1].split("app name")[0].strip()
                if pkg_part:
                    package_name = pkg_part.replace(" ", "") # Remove spaces
        except Exception as e:
            print(f"Warning: Could not parse package name from input. Using default. Error: {e}")

    print(f"Parsed App Name: {app_name}")
    print(f"Parsed Package Name: {package_name}")

    # --- APK Generation Logic ---
    temp_project_dir = TEMP_PROJECT_DIR
    if os.path.exists(temp_project_dir):
        print(f"Removing existing temporary directory: {temp_project_dir}")
        shutil.rmtree(temp_project_dir)
    os.makedirs(temp_project_dir, exist_ok=True)

    try:
        # 1. Create the basic Android project structure
        create_android_project_structure(temp_project_dir, package_name, app_name)
        print("Basic Android project structure created.")

        # 2. Build the APK using Gradle
        # This assumes you have Android SDK and Gradle installed and configured
        # or that the gradlew wrapper can download necessary components.
        if build_apk(temp_project_dir, output_apk_path):
            print(f"APK generation successful: {output_apk_path}")
            return f"Success: APK generated at {output_apk_path}"
        else:
            print("APK build process failed.")
            return "Failure: APK build process failed."

    except Exception as e:
        print(f"An error occurred during APK generation: {e}")
        return f"Failure: An unexpected error occurred - {e}"
    finally:
        # --- Cleanup ---
        print("\n--- Cleaning up temporary project directory ---")
        if os.path.exists(temp_project_dir):
            shutil.rmtree(temp_project_dir)
            print(f"Temporary directory '{temp_project_dir}' removed.")
        else:
            print("Temporary directory already removed or not created.")

# Example Usage (for testing purposes)
if __name__ == "__main__":
    # Example 1: Basic app creation
    print("--- Running Lobe 8 Demo: Basic App ---")
    input_text_1 = "Create an Android app with the app name MyFirstApp and package name com.example.myfirstapp."
    output_apk_1 = "my_first_app.apk"
    result_1 = generate_arabic_nlp_apk(input_text_1, output_apk_1)
    print(f"Result 1: {result_1}")

    if os.path.exists(output_apk_1):
        print(f"Successfully created {output_apk_1}")
        # os.remove(output_apk_1) # Clean up the generated APK after testing

    print("\n" + "="*50 + "\n")

    # Example 2: Different app name and package
    print("--- Running Lobe 8 Demo: Another App ---")
    input_text_2 = "I want a new Android application. The app name should be HelloArabic and the package name com.arabicdev.hello."
    output_apk_2 = "hello_arabic.apk"
    result_2 = generate_arabic_nlp_apk(input_text_2, output_apk_2)
    print(f"Result 2: {result_2}")

    if os.path.exists(output_apk_2):
        print(f"Successfully created {output_apk_2}")
        # os.remove(output_apk_2) # Clean up the generated APK after testing

    print("\n--- Lobe 8_apk_compiler_lobe Demo Finished ---")