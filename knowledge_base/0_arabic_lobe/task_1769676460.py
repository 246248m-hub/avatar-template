import os
import re
import json
import subprocess
import zipfile
import shutil

# Assume these directories and file paths are defined elsewhere
# For demonstration purposes, we'll define them here
KNOWLEDGE_BASE_DIR = "knowledge_base"
PROJECT_TEMPLATE_DIR = "project_templates/android_template"
OUTPUT_DIR = "generated_apks"
DUMMY_PROJECT_ROOT = "dummy_android_project"

def extract_manifest_package(manifest_path):
    """
    Extracts the package name from an AndroidManifest.xml file.
    """
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'package="([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        print(f"Error: Manifest file not found at {manifest_path}")
    except Exception as e:
        print(f"Error parsing manifest file {manifest_path}: {e}")
    return None

def create_android_project(project_name, package_name, output_dir):
    """
    Creates a basic Android project structure using a template.
    In a real scenario, this would use Android's build tools or a project generator.
    For this example, we'll simulate by copying a template.
    """
    if not os.path.exists(PROJECT_TEMPLATE_DIR):
        print(f"Error: Project template directory not found: {PROJECT_TEMPLATE_DIR}")
        return None

    project_root = os.path.join(output_dir, project_name)
    if os.path.exists(project_root):
        shutil.rmtree(project_root)
    shutil.copytree(PROJECT_TEMPLATE_DIR, project_root)

    # Update package name in AndroidManifest.xml
    manifest_path = os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('package="com.example.myapp"', f'package="{package_name}"')
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error updating package name in manifest: {e}")

    # Update application ID in build.gradle (app level)
    build_gradle_path = os.path.join(project_root, "app", "build.gradle")
    if os.path.exists(build_gradle_path):
        try:
            with open(build_gradle_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = re.sub(r"applicationId\s+['\"]com\.example\.myapp['\"]", f"applicationId \"{package_name}\"", content)
            with open(build_gradle_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error updating application ID in build.gradle: {e}")

    print(f"Created Android project at: {project_root}")
    return project_root

def compile_apk(project_dir, output_apk_path):
    """
    Compiles an Android project into an APK using Gradle.
    Requires Android SDK and Gradle to be installed and configured in the environment.
    """
    print(f"Attempting to compile APK for project: {project_dir}")
    if not os.path.exists(project_dir):
        print(f"Error: Project directory not found: {project_dir}")
        return False

    # Navigate to the project directory
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        # Execute Gradle wrapper to build the APK
        # Assuming gradlew is available in the project root (standard for new Android projects)
        if os.path.exists("./gradlew"):
            build_command = ["./gradlew", "assembleDebug"] # Use assembleDebug for simplicity
        else:
            print("Error: gradlew not found. Ensure it's part of the project template.")
            return False

        print(f"Running Gradle build command: {' '.join(build_command)}")
        process = subprocess.run(build_command, capture_output=True, text=True, check=True)
        print("Gradle build output:\n", process.stdout)

        # Locate the generated APK
        apk_dir = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")
        apk_filename = None
        for file in os.listdir(apk_dir):
            if file.endswith(".apk"):
                apk_filename = file
                break

        if apk_filename:
            source_apk_path = os.path.join(apk_dir, apk_filename)
            os.makedirs(os.path.dirname(output_apk_path), exist_ok=True)
            shutil.move(source_apk_path, output_apk_path)
            print(f"APK successfully compiled and saved to: {output_apk_path}")
            return True
        else:
            print("Error: Could not find generated APK in build output.")
            return False

    except FileNotFoundError:
        print("Error: 'gradlew' command not found. Ensure Gradle is installed and accessible.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("Stderr:\n", e.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred during compilation: {e}")
        return False
    finally:
        # Return to the original directory
        os.chdir(original_dir)

def build_apk_from_nlp(natural_language_description, project_name="generated_app"):
    """
    Parses natural language to generate an Android project structure and compile it into an APK.
    This is a high-level function that orchestrates the process.
    """
    print("\n--- Initiating APK generation from NLP ---")

    # 1. Parse NLP to extract information for Android project
    # This step would involve Lobe 0_language_lobe and potentially other lobes
    # For now, we simulate by extracting a package name and a dummy project name.
    # In a real scenario, this would parse the description for UI elements, functionalities, etc.
    print("Parsing natural language description...")
    extracted_package_name = "com.example.arabic_generated_" + re.sub(r'\W+', '', natural_language_description.lower())[:15]
    print(f"Simulated extracted package name: {extracted_package_name}")

    # Ensure output directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DUMMY_PROJECT_ROOT, exist_ok=True)

    # 2. Create the Android project structure
    print("Creating Android project structure...")
    generated_project_dir = create_android_project(project_name, extracted_package_name, DUMMY_PROJECT_ROOT)

    if not generated_project_dir:
        print("Failed to create Android project.")
        return None

    # 3. Compile the Android project into an APK
    print("Compiling APK...")
    output_apk_filename = f"{project_name}.apk"
    output_apk_path = os.path.join(OUTPUT_DIR, output_apk_filename)

    success = compile_apk(generated_project_dir, output_apk_path)

    if success:
        print(f"APK successfully generated: {output_apk_path}")
        return output_apk_path
    else:
        print("APK compilation failed.")
        return None

# --- DEMO USAGE ---
if __name__ == "__main__":
    print("--- Android APK Compiler Lobe Demo ---")

    # Example natural language description (can be in Arabic or other languages)
    # This would be the output from Lobe 0_language_lobe or a similar module
    arabic_description_example = "إنشاء تطبيق بسيط يعرض نصًا ترحيبيًا باللغة العربية."

    # Ensure necessary directories exist before running demo
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(PROJECT_TEMPLATE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Create a dummy Android project template for the demo ---
    # In a real scenario, this template would be pre-existing.
    # We create a minimal structure here.
    dummy_template_app_dir = os.path.join(PROJECT_TEMPLATE_DIR, "app")
    dummy_template_manifest_dir = os.path.join(dummy_template_app_dir, "src", "main")
    os.makedirs(dummy_template_manifest_dir, exist_ok=True)
    dummy_manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">
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
    with open(os.path.join(dummy_template_manifest_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(dummy_manifest_content)

    dummy_build_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.myapp'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 24
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

    implementation 'androidx.core:core-ktx:1.10.1'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    with open(os.path.join(dummy_template_project_dir, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(dummy_build_gradle_content)

    # Create a placeholder gradlew and gradlew.bat for demonstration
    with open(os.path.join(PROJECT_TEMPLATE_DIR, "gradlew"), "w") as f:
        f.write("#!/bin/bash\necho 'Mock gradlew executed.'\nexit 0\n")
    with open(os.path.join(PROJECT_TEMPLATE_DIR, "gradlew.bat"), "w") as f:
        f.write("@echo off\necho Mock gradlew executed.\nexit /b 0\n")


    # --- Run the APK generation process ---
    generated_apk_path = build_apk_from_nlp(arabic_description_example, project_name="arabic_greeting_app")

    if generated_apk_path:
        print(f"\nAPK generation process completed successfully. APK saved at: {generated_apk_path}")
    else:
        print("\nAPK generation process encountered errors.")

    # --- Cleanup dummy directories ---
    print("\n--- Cleaning up dummy directories ---")
    if os.path.exists(DUMMY_PROJECT_ROOT):
        print(f"Removing dummy project directory: {DUMMY_PROJECT_ROOT}")
        shutil.rmtree(DUMMY_PROJECT_ROOT)
    if os.path.exists(PROJECT_TEMPLATE_DIR):
        # In a real scenario, you might not want to delete the template
        # For this demo, we clean it up to ensure a clean state next run
        print(f"Removing dummy project template directory: {PROJECT_TEMPLATE_DIR}")
        shutil.rmtree(PROJECT_TEMPLATE_DIR)
    # Keep generated APKs for inspection, so no cleanup here.

    print("\n--- Android APK Compiler Lobe Demo Finished ---")