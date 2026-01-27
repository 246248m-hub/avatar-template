import os
import shutil
from typing import Dict, Any

# Assuming these are defined elsewhere or will be defined by other lobes
# For now, we'll define them as placeholders for the sake of demonstrating structure.
# In a real scenario, these would be dynamically generated or retrieved.
KNOWLEDGE_BASE_DIR = "knowledge_base"
JAVA_PROJECT_DIR = "generated_java_project"
APK_OUTPUT_DIR = "generated_apks"

def create_project_structure(project_path: str):
    """Creates the basic directory structure for an Android project."""
    os.makedirs(os.path.join(project_path, "app", "src", "main", "java", "com", "example", "myapp"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "drawable"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "gradle"), exist_ok=True)

def generate_manifest_xml(project_path: str, app_name: str = "MyApp"):
    """Generates a basic AndroidManifest.xml file."""
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_name.lower()}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name}">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

def generate_string_xml(project_path: str, app_name: str = "MyApp"):
    """Generates a basic strings.xml file."""
    strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "values"), exist_ok=True)
    with open(os.path.join(project_path, "app", "src", "main", "res", "values", "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_content)

def generate_activity_file(project_path: str, activity_name: str = "MainActivity", layout_name: str = "activity_main"):
    """Generates a basic Activity Java file."""
    java_package_path = os.path.join(project_path, "app", "src", "main", "java", "com", "example", "myapp")
    os.makedirs(java_package_path, exist_ok=True)

    activity_content = f"""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});
    }}
}}
"""
    with open(os.path.join(java_package_path, f"{activity_name}.java"), "w", encoding="utf-8") as f:
        f.write(activity_content)

def generate_layout_xml(project_path: str, layout_name: str = "activity_main"):
    """Generates a basic layout XML file."""
    layout_path = os.path.join(project_path, "app", "src", "main", "res", "layout")
    os.makedirs(layout_path, exist_ok=True)

    layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.replace('activity_', '').capitalize()}Activity">

    <!-- Add your UI elements here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(os.path.join(layout_path, f"{layout_name}.xml"), "w", encoding="utf-8") as f:
        f.write(layout_content)

def generate_gradle_files(project_path: str, app_name: str = "MyApp"):
    """Generates essential Gradle files for an Android project."""
    # settings.gradle
    settings_content = f"""
pluginManagement {{
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
rootProject.name = "{app_name}"
include ':app'
"""
    with open(os.path.join(project_path, "settings.gradle"), "w", encoding="utf-8") as f:
        f.write(settings_content)

    # app/build.gradle
    app_build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin might be used, though not strictly required for Java
}}

android {{
    namespace 'com.example.{app_name.lower()}'
    compileSdk 33 // Or your target SDK version

    defaultConfig {{
        applicationId "com.example.{app_name.lower()}"
        minSdk 21 // Or your minimum SDK version
        targetSdk 33 // Or your target SDK version
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
    // If using Kotlin, uncomment the following
    // kotlinOptions {{
    //     jvmTarget = '1.8'
    // }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
    os.makedirs(os.path.join(project_path, "app"), exist_ok=True)
    with open(os.path.join(project_path, "app", "build.gradle"), "w", encoding="utf-8") as f:
        f.write(app_build_gradle_content)

    # build.gradle (project level)
    build_gradle_content = f"""
// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {{
    id 'com.android.application' version '8.1.0' apply false
    id 'com.android.library' version '8.1.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.10' apply false // Adjust Kotlin version if needed
}}
"""
    with open(os.path.join(project_path, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(build_gradle_content)

def _android_module_builder(
    natural_language_input: str,
    app_name: str = "MyApp",
    activity_name: str = "MainActivity",
    layout_name: str = "activity_main"
) -> str:
    """
    This function acts as the core of the Arabic-to-APK module.
    It takes natural language input (expected to be Arabic),
    parses it (though parsing logic is not detailed here),
    and generates the foundational structure of an Android project.

    Args:
        natural_language_input (str): The Arabic prompt describing the desired app.
        app_name (str): The desired name for the Android application.
        activity_name (str): The name of the main Activity.
        layout_name (str): The name of the main layout file.

    Returns:
        str: The path to the root of the generated Android project.
    """
    print(f"\n--- Starting Android Module Builder ---")
    print(f"Processing input: '{natural_language_input}'")

    # Initialize project directory
    project_root = os.path.join(JAVA_PROJECT_DIR, app_name.lower().replace(" ", "_"))
    if os.path.exists(project_root):
        shutil.rmtree(project_root) # Clean up previous runs
    os.makedirs(project_root, exist_ok=True)
    print(f"Created project root: {project_root}")

    # 1. Create basic project structure
    create_project_structure(project_root)
    print("Created project structure.")

    # 2. Generate essential XML files
    generate_manifest_xml(project_root, app_name)
    print("Generated AndroidManifest.xml.")
    generate_string_xml(project_root, app_name)
    print("Generated strings.xml.")
    generate_layout_xml(project_root, layout_name)
    print(f"Generated layout: {layout_name}.xml.")

    # 3. Generate Java Activity file
    generate_activity_file(project_root, activity_name, layout_name)
    print(f"Generated Activity: {activity_name}.java.")

    # 4. Generate Gradle build files
    generate_gradle_files(project_root, app_name)
    print("Generated Gradle build files.")

    print(f"--- Android Module Builder Finished. Project generated at: {project_root} ---")
    return project_root

# Example usage (this would typically be called by Lobe 6_synthesis_lobe)
if __name__ == "__main__":
    # Simulate Arabic input - in a real scenario, this would be processed by Lobe 0
    arabic_prompt = "إنشاء تطبيق بسيط يعرض رسالة ترحيب." # "Create a simple app that displays a welcome message."

    # Simulate extracted parameters from Arabic input (by other lobes)
    # For demonstration, we'll hardcode these.
    app_name_from_arabic = "WelcomeApp"
    main_activity_name = "WelcomeActivity"
    main_layout_file = "activity_welcome"

    generated_project_path = _android_module_builder(
        natural_language_input=arabic_prompt,
        app_name=app_name_from_arabic,
        activity_name=main_activity_name,
        layout_name=main_layout_file
    )

    print(f"\nSuccessfully generated Android project at: {generated_project_path}")

    # Clean up generated project for demonstration purposes
    print("\n--- Cleaning up generated project ---")
    if os.path.exists(JAVA_PROJECT_DIR):
        shutil.rmtree(JAVA_PROJECT_DIR)
        print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")

    print("\n--- Android Module Builder Demo Finished ---")