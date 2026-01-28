import os
import re
from pathlib import Path

# Define directory paths
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
GENERATED_APKS_DIR = Path("generated_apks")

# --- Lobe 0: Arabic Language Processing ---
# This lobe is responsible for understanding and parsing Arabic natural language.
# For this iteration, we'll simulate parsing by extracting keywords.

def parse_arabic_request(arabic_text: str) -> dict:
    """
    Simulates parsing an Arabic natural language request to identify key components
    for APK generation.

    Args:
        arabic_text: The Arabic natural language request.

    Returns:
        A dictionary containing extracted components like app name, features, etc.
    """
    parsed_data = {
        "app_name": "UnnamedApp",
        "features": [],
        "permissions": [],
        "ui_elements": []
    }

    # Simple keyword extraction (this would be much more sophisticated in a real system)
    arabic_keywords = {
        "اسم التطبيق": "app_name",
        "تسجيل الدخول": "login_feature",
        "عرض القائمة": "list_view_feature",
        "استخدام الكاميرا": "camera_permission",
        "الوصول إلى الموقع": "location_permission",
        "زر": "button_ui",
        "حقل نصي": "text_field_ui"
    }

    # Basic tokenization and matching
    tokens = re.findall(r'\b\w+\b', arabic_text, re.UNICODE)
    for token in tokens:
        for keyword, key in arabic_keywords.items():
            if token in keyword.split(): # Simple check if token is part of a keyword
                if key == "app_name":
                    # Assuming app name follows a pattern like "اسم التطبيق: [App Name]"
                    match = re.search(r"اسم التطبيق:\s*([\w\s]+)", arabic_text, re.UNICODE)
                    if match:
                        parsed_data["app_name"] = match.group(1).strip()
                elif "feature" in key:
                    parsed_data["features"].append(keyword)
                elif "permission" in key:
                    parsed_data["permissions"].append(keyword)
                elif "ui" in key:
                    parsed_data["ui_elements"].append(keyword)
                break # Move to next token once a match is found

    return parsed_data

# --- Lobe 1: APK Structure Generation ---
# This lobe takes parsed information and generates the basic structure for an APK.
# It will define directories and placeholder files.

def generate_apk_structure(app_name: str, parsed_data: dict) -> Path:
    """
    Generates the directory and file structure for a new APK project.

    Args:
        app_name: The name of the application.
        parsed_data: The data parsed from the Arabic request.

    Returns:
        The path to the root directory of the generated APK project.
    """
    app_dir_name = app_name.replace(" ", "_").lower()
    apk_project_path = GENERATED_APKS_DIR / app_dir_name

    # Create project directories
    (apk_project_path / "app" / "src" / "main" / "java" / "com" / "example" / app_dir_name.lower()).mkdir(parents=True, exist_ok=True)
    (apk_project_path / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
    (apk_project_path / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)
    (apk_project_path / "app" / "src" / "main" / "assets").mkdir(parents=True, exist_ok=True)
    (apk_project_path / "app" / "src" / "main" / "jniLibs").mkdir(parents=True, exist_ok=True)

    # Create placeholder files
    # Manifest file (AndroidManifest.xml)
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_dir_name.lower()}">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33"/>

    {"".join([f'<uses-permission android:name="android.permission.{perm.split('_')[-1].upper()}" />\\n' for perm in parsed_data.get("permissions", [])])}

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(apk_project_path / "app" / "src" / "main" / "AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest_content.strip())

    # Strings resource file (strings.xml)
    strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    with open(apk_project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml", "w", encoding="utf-8") as f:
        f.write(strings_content.strip())

    # Main Activity Java file (MainActivity.java)
    main_activity_content = f"""
package com.example.{app_dir_name.lower()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Your app logic will go here based on features and UI elements
    }}
}}
"""
    with open(apk_project_path / "app" / "src" / "main" / "java" / "com" / "example" / app_dir_name.lower() / "MainActivity.java", "w", encoding="utf-8") as f:
        f.write(main_activity_content.strip())

    # Layout file for MainActivity (activity_main.xml)
    layout_content = """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <!-- Content will be added here based on UI elements -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(apk_project_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml", "w", encoding="utf-8") as f:
        f.write(layout_content.strip())

    # Gradle wrapper properties
    (apk_project_path / "gradle" / "wrapper").mkdir(parents=True, exist_ok=True)
    with open(apk_project_path / "gradle" / "wrapper" / "gradle-wrapper.properties", "w") as f:
        f.write("distributionBase=GRADLE_USER_HOME\n")
        f.write("distributionPath=wrapper/dists\n")
        f.write("distributionUrl=https\://services.gradle.org/distributions/gradle-7.5.1-bin.zip\n")
        f.write("zipStoreBase=GRADLE_USER_HOME\n")
        f.write("zipStorePath=wrapper/dists\n")

    # build.gradle (app level)
    with open(apk_project_path / "app" / "build.gradle", "w") as f:
        f.write("""
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.{app_dir_name.lower()}"
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
""".format(app_dir_name=app_dir_name).strip())

    # build.gradle (project level)
    with open(apk_project_path / "build.gradle", "w") as f:
        f.write("""
plugins {
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.7.20' apply false
}
""".strip())

    # settings.gradle
    with open(apk_project_path / "settings.gradle", "w") as f:
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
rootProject.name = "{app_name}"
include ':app'
""".format(app_name=app_name).strip())


    return apk_project_path

# --- Demo Execution ---

def demo_arabic_processing_and_apk_struct_generation():
    """
    Demonstrates the Arabic parsing and APK structure generation process.
    """
    print("--- Initiating Arabic Parser and Generator Module Demo ---")

    arabic_request = "أريد تطبيق باسم 'متجري السهل' مع ميزة تسجيل الدخول واستخدام الكاميرا. يجب أن يتضمن زر للبحث."
    print(f"Arabic Request: {arabic_request}")

    # Lobe 0: Arabic Processing
    parsed_data = parse_arabic_request(arabic_request)
    print(f"Parsed Data: {parsed_data}")

    # Lobe 1: APK Structure Generation
    app_name = parsed_data.get("app_name", "DefaultAppName")
    generated_project_path = generate_apk_structure(app_name, parsed_data)
    print(f"Generated APK project structure at: {generated_project_path}")

    # Verify some generated files
    print("\nVerifying generated files:")
    manifest_path = generated_project_path / "app" / "src" / "main" / "AndroidManifest.xml"
    strings_path = generated_project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml"
    main_activity_path = generated_project_path / "app" / "src" / "main" / "java" / "com" / "example" / app_name.replace(" ", "_").lower() / "MainActivity.java"

    print(f"Manifest exists: {manifest_path.exists()}")
    print(f"Strings.xml exists: {strings_path.exists()}")
    print(f"MainActivity.java exists: {main_activity_path.exists()}")

    # --- Simulate next step ---
    print("\n--- Initiating next step: Lobe 6_synthesis_lobe ---")
    # In a real scenario, Lobe 6 would take the generated structure and further synthesize code.
    # For this demo, we just acknowledge its initiation.


def cleanup_dummy_files():
    """
    Cleans up the generated dummy files and directories.
    """
    if GENERATED_APKS_DIR.exists():
        import shutil
        print(f"Removing directory: {GENERATED_APKS_DIR}")
        shutil.rmtree(GENERATED_APKS_DIR)

    if KNOWLEDGE_BASE_DIR.exists():
        import shutil
        print(f"Removing directory: {KNOWLEDGE_BASE_DIR}")
        shutil.rmtree(KNOWLEDGE_BASE_DIR)

# --- Execute the demo ---
if __name__ == "__main__":
    # Ensure necessary directories exist for the demo
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    GENERATED_APKS_DIR.mkdir(exist_ok=True)

    demo_arabic_processing_and_apk_struct_generation()

    # Clean up dummy files
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")