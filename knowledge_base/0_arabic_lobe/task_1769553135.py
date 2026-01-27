import os
import shutil
import subprocess
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path("./generated_apk_project")
APP_NAME = "MyUnifiedApp"
PACKAGE_NAME = "com.example.myunifiedapp"
ACTIVITY_NAME = "MainActivity"
MIN_SDK_VERSION = 21
TARGET_SDK_VERSION = 33
COMPILE_SDK_VERSION = 33
GRADLE_VERSION = "8.0"
GRADLE_PLUGIN_VERSION = "7.4.2"
KOTLIN_VERSION = "1.8.10"
ANDROID_GRADLE_PLUGIN_PATH = PROJECT_ROOT / "build.gradle"
APP_GRADLE_PATH = PROJECT_ROOT / "app" / "build.gradle"
MAIN_ACTIVITY_PATH = PROJECT_ROOT / "app" / "src" / "main" / "java" / PACKAGE_NAME.replace('.', '/') / f"{ACTIVITY_NAME}.kt"
MANIFEST_PATH = PROJECT_ROOT / "app" / "src" / "main" / "AndroidManifest.xml"
RES_LAYOUT_PATH = PROJECT_ROOT / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
STRINGS_XML_PATH = PROJECT_ROOT / "app" / "src" / "main" / "res" / "values" / "strings.xml"

# --- Helper Functions ---

def create_directory_structure():
    """Creates the necessary directory structure for the Android project."""
    print("--- Creating project directory structure ---")
    PROJECT_ROOT.mkdir(exist_ok=True)
    (PROJECT_ROOT / "app").mkdir(exist_ok=True)
    (PROJECT_ROOT / "app" / "src").mkdir(exist_ok=True)
    (PROJECT_ROOT / "app" / "src" / "main").mkdir(exist_ok=True)
    (PROJECT_ROOT / "app" / "src" / "main" / "java").mkdir(exist_ok=True)
    (PROJECT_ROOT / "app" / "src" / "main" / "res").mkdir(exist_ok=True)
    (PROJECT_ROOT / "app" / "src" / "main" / "res" / "layout").mkdir(exist_ok=True)
    (PROJECT_ROOT / "app" / "src" / "main" / "res" / "values").mkdir(exist_ok=True)

    java_package_dir = PROJECT_ROOT / "app" / "src" / "main" / "java" / PACKAGE_NAME.replace('.', '/')
    java_package_dir.mkdir(parents=True, exist_ok=True)

    res_values_dir = PROJECT_ROOT / "app" / "src" / "main" / "res" / "values"
    res_values_dir.mkdir(parents=True, exist_ok=True)

def create_build_gradle():
    """Creates the top-level build.gradle file."""
    print("--- Creating top-level build.gradle ---")
    build_gradle_content = f"""
buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath("com.android.tools.build:gradle:{GRADLE_PLUGIN_VERSION}")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:{KOTLIN_VERSION}")
    }}
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

task clean(type: Delete) {{
    delete rootProject.buildDir
}}
"""
    with open(ANDROID_GRADLE_PLUGIN_PATH, "w", encoding="utf-8") as f:
        f.write(build_gradle_content)

def create_app_build_gradle():
    """Creates the app-level build.gradle file."""
    print("--- Creating app-level build.gradle ---")
    app_build_gradle_content = f"""
plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{PACKAGE_NAME}"
    compileSdk = {COMPILE_SDK_VERSION}

    defaultConfig {{
        applicationId = "{PACKAGE_NAME}"
        minSdk = {MIN_SDK_VERSION}
        targetSdk = {TARGET_SDK_VERSION}
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            minifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
    }}
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }}
    kotlinOptions {{
        jvmTarget = "1.8"
    }}
    buildFeatures {{
        viewBinding = true
    }}
}}

dependencies {{
    implementation("androidx.core.ktx:core-ktx:1.9.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.10.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}}
"""
    with open(APP_GRADLE_PATH, "w", encoding="utf-8") as f:
        f.write(app_build_gradle_content)

def create_main_activity_kt():
    """Creates the main Kotlin activity file."""
    print("--- Creating MainActivity.kt ---")
    activity_kt_content = f"""
package {PACKAGE_NAME}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import {PACKAGE_NAME}.databinding.ActivityMainBinding

class {ACTIVITY_NAME} : AppCompatActivity() {{

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Example: Setting text from a string resource
        binding.textViewGreeting.text = getString(R.string.greeting_message)
    }}
}}
"""
    with open(MAIN_ACTIVITY_PATH, "w", encoding="utf-8") as f:
        f.write(activity_kt_content)

def create_android_manifest_xml(app_name, package_name, activity_name):
    """Creates the AndroidManifest.xml file."""
    print("--- Creating AndroidManifest.xml ---")
    manifest_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name}"
        tools:targetApi="31">
        <activity
            android:name=".{activity_name}"
            android:exported="true">
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

def create_activity_main_xml():
    """Creates the activity_main.xml layout file."""
    print("--- Creating activity_main.xml ---")
    activity_main_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{ACTIVITY_NAME}">

    <TextView
        android:id="@+id/textViewGreeting"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(RES_LAYOUT_PATH, "w", encoding="utf-8") as f:
        f.write(activity_main_content)

def create_strings_xml(app_name, greeting_message):
    """Creates the strings.xml file."""
    print("--- Creating strings.xml ---")
    strings_xml_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
    <string name="greeting_message">{greeting_message}</string>
</resources>
"""
    with open(STRINGS_XML_PATH, "w", encoding="utf-8") as f:
        f.write(strings_xml_content)

def initialize_android_project(app_name, greeting_message):
    """Initializes a basic Android project structure."""
    print(f"\n--- Initializing Android Project: {app_name} ---")
    if PROJECT_ROOT.exists():
        print(f"Cleaning up existing project directory: {PROJECT_ROOT}")
        shutil.rmtree(PROJECT_ROOT)

    create_directory_structure()
    create_build_gradle()
    create_app_build_gradle()
    create_main_activity_kt()
    create_android_manifest_xml(app_name, PACKAGE_NAME, ACTIVITY_NAME)
    create_activity_main_xml()
    create_strings_xml(app_name, greeting_message)
    print("--- Android Project Initialization Complete ---")

def build_apk(project_path, app_name):
    """
    Builds the APK using Gradle.
    This function assumes Gradle is installed and accessible in the PATH.
    """
    print(f"\n--- Building APK for: {app_name} ---")
    gradle_w = "./gradlew" if os.name == "nt" else "./gradlew"
    try:
        # Navigate to the project directory
        original_cwd = os.getcwd()
        os.chdir(project_path)

        # Execute the assembleRelease task
        print(f"Running: {gradle_w} assembleRelease")
        subprocess.run([gradle_w, "assembleRelease"], check=True, capture_output=True, text=True)
        print("APK build successful!")

        # Find the generated APK
        apk_path = None
        for root, dirs, files in os.walk("app/build/outputs/apk/release"):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = Path(root) / file
                    break
            if apk_path:
                break

        if apk_path:
            print(f"APK generated at: {apk_path}")
            return apk_path
        else:
            print("Could not find the generated APK file.")
            return None

    except FileNotFoundError:
        print("Error: gradlew command not found. Please ensure Gradle is installed and in your PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Gradle build failed:")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        return None
    finally:
        # Return to the original directory
        os.chdir(original_cwd)

def generate_apk_from_natural_language(natural_language_description: str):
    """
    Parses natural language to generate an Android APK.
    This is a high-level function that orchestrates the process.
    It's designed to be a placeholder for Lobe 7_nlp_to_code integration.
    """
    print(f"\n--- Generating APK from: '{natural_language_description}' ---")

    # Placeholder for NLP parsing to extract app name, greeting, etc.
    # In a real scenario, Lobe 7_nlp_to_code would handle this.
    # For demonstration, we'll use hardcoded values or simple parsing.
    app_name = APP_NAME
    greeting_message = "Welcome to the Unified Mind!"

    if "app name" in natural_language_description.lower():
        try:
            # Very basic extraction for demo purposes
            parts = natural_language_description.split("app name")
            if len(parts) > 1:
                app_name_candidate = parts[1].split("and")[0].strip()
                if app_name_candidate:
                    app_name = app_name_candidate
        except Exception as e:
            print(f"Could not parse app name: {e}")

    if "greeting" in natural_language_description.lower():
        try:
            parts = natural_language_description.split("greeting")
            if len(parts) > 1:
                greeting_candidate = parts[1].split("and")[0].strip()
                if greeting_candidate:
                    greeting_message = greeting_candidate
        except Exception as e:
            print(f"Could not parse greeting: {e}")


    print(f"Extracted App Name: {app_name}")
    print(f"Extracted Greeting Message: {greeting_message}")

    # 1. Initialize the Android project structure
    initialize_android_project(app_name, greeting_message)

    # 2. Build the APK using Gradle
    apk_output_path = build_apk(PROJECT_ROOT, app_name)

    if apk_output_path:
        print(f"Successfully generated APK for '{app_name}' at: {apk_output_path}")
        return {"status": "success", "apk_path": str(apk_output_path)}
    else:
        print(f"Failed to generate APK for '{app_name}'.")
        return {"status": "failure", "message": "APK build process failed."}

# --- Example Usage (for demonstration purposes) ---
if __name__ == "__main__":
    # Simulate input from Arabic Lobe or other NLP processing
    # This would typically be the output of Lobe 7_nlp_to_code
    natural_language_input = "Create an Android app. The app name should be 'ArabicAI' and the greeting message should be 'أهلاً بك يا عقل موحد' (Welcome, unified mind)."

    print("\n--- Starting APK Generation Module ---")
    generation_result = generate_apk_from_natural_language(natural_language_input)
    print("\n--- APK Generation Module Finished ---")
    print(f"Generation Result: {generation_result}")

    # Example of cleaning up the generated project
    if PROJECT_ROOT.exists():
        print(f"\n--- Cleaning up generated project: {PROJECT_ROOT} ---")
        shutil.rmtree(PROJECT_ROOT)