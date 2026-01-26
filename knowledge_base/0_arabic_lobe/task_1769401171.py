import os
import re
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assume KNOWLEDGE_BASE_DIR and JAVA_PROJECT_DIR are defined in the global scope or passed as arguments
# For demonstration purposes, let's define them here
KNOWLEDGE_BASE_DIR = os.path.join(os.getcwd(), "knowledge_base")
JAVA_PROJECT_DIR = os.path.join(os.getcwd(), "java_project_output")

class ArabicAPKGenerator:
    """
    A module to generate APKs from natural language Arabic descriptions.
    This module focuses on parsing Arabic input and constructing the necessary
    Java/Kotlin code and Gradle configurations.
    """

    def __init__(self, java_project_dir: str, knowledge_base_dir: str):
        """
        Initializes the ArabicAPKGenerator.

        Args:
            java_project_dir (str): The root directory for generated Java projects.
            knowledge_base_dir (str): The directory containing knowledge base files.
        """
        self.java_project_dir = java_project_dir
        self.knowledge_base_dir = knowledge_base_dir
        self.project_structure_manager = None # Will be initialized when needed

    def _create_project_directory(self, app_name: str):
        """
        Creates the necessary directory structure for a new Android project.

        Args:
            app_name (str): The name of the Android application.
        """
        project_path = os.path.join(self.java_project_dir, app_name)
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "java", "com", "example", app_name.lower()), exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "values"), exist_ok=True)
        logging.info(f"Created project directory structure for '{app_name}' at: {project_path}")
        return project_path

    def _generate_gradle_files(self, project_path: str, app_name: str):
        """
        Generates basic build.gradle and settings.gradle files.

        Args:
            project_path (str): The root path of the Android project.
            app_name (str): The name of the Android application.
        """
        settings_gradle_content = f"""rootProject.name = "{app_name}"
include ':app'
"""
        with open(os.path.join(project_path, "settings.gradle"), "w", encoding="utf-8") as f:
            f.write(settings_gradle_content)
        logging.info(f"Generated settings.gradle for '{app_name}'.")

        app_gradle_content = """
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin for modern Android dev
}

android {
    compileSdk 33 // Example, can be dynamic

    defaultConfig {
        applicationId "com.example.generatedapp" // Placeholder, should be dynamic
        minSdk 24 // Example, can be dynamic
        targetSdk 33 // Example, can be dynamic
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
    buildFeatures {
        viewBinding true // Enable view binding
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
        with open(os.path.join(project_path, "app", "build.gradle"), "w", encoding="utf-8") as f:
            f.write(app_gradle_content)
        logging.info(f"Generated app/build.gradle for '{app_name}'.")

    def _generate_main_activity(self, package_path: str, app_name: str):
        """
        Generates a basic MainActivity.kt file.

        Args:
            package_path (str): The path to the Java/Kotlin source directory.
            app_name (str): The name of the Android application.
        """
        activity_content = f"""
package com.example.{app_name.lower()}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.generatedapp.R // Adjust R import if needed

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main) // Link to activity_main.xml
    }}
}}
"""
        with open(os.path.join(package_path, "MainActivity.kt"), "w", encoding="utf-8") as f:
            f.write(activity_content)
        logging.info(f"Generated MainActivity.kt for '{app_name}'.")

    def _generate_activity_main_layout(self, layout_path: str, app_name: str):
        """
        Generates a basic activity_main.xml layout file.

        Args:
            layout_path (str): The path to the layout directory.
            app_name (str): The name of the Android application.
        """
        layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name}Activity">

    <!-- Content will be added based on Arabic description -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="مرحباً بك في تطبيق {app_name}"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(os.path.join(layout_path, "activity_main.xml"), "w", encoding="utf-8") as f:
            f.write(layout_content)
        logging.info(f"Generated activity_main.xml for '{app_name}'.")

    def _parse_arabic_description(self, arabic_description: str) -> dict:
        """
        Parses the Arabic natural language description to extract app details
        and UI elements. This is a simplified parser.

        Args:
            arabic_description (str): The Arabic text describing the app.

        Returns:
            dict: A dictionary containing parsed information, e.g., app name, UI elements.
        """
        parsed_data = {
            "app_name": "GeneratedApp",  # Default
            "ui_elements": []
        }

        # Basic app name extraction
        name_match = re.search(r"تطبيق اسمه ([\w\s]+)", arabic_description)
        if name_match:
            parsed_data["app_name"] = name_match.group(1).strip()
        else:
            # Attempt to get a shorter name from the beginning if no explicit name found
            first_few_words = arabic_description.split()[:3]
            if first_few_words:
                parsed_data["app_name"] = "".join(first_few_words)

        # Simplified UI element parsing (e.g., looking for buttons, text fields)
        # This would be significantly more complex in a real-world scenario,
        # potentially involving NLP libraries for Arabic intent recognition.
        if "زر" in arabic_description:
            parsed_data["ui_elements"].append({"type": "Button", "text": "زر", "id": "button_generic"})
        if "حقل نص" in arabic_description:
            parsed_data["ui_elements"].append({"type": "EditText", "hint": "أدخل نص", "id": "edittext_generic"})
        if "عنوان" in arabic_description:
            title_match = re.search(r"عنوان هو ([\w\s]+)", arabic_description)
            if title_match:
                parsed_data["ui_elements"].append({"type": "TextView", "text": title_match.group(1).strip(), "id": "textview_title"})

        logging.info(f"Parsed Arabic description: {parsed_data}")
        return parsed_data

    def generate_apk_from_arabic(self, arabic_description: str) -> str:
        """
        Generates a functional APK structure from an Arabic description.

        Args:
            arabic_description (str): The natural language Arabic description of the app.

        Returns:
            str: The path to the generated APK or a success message.
        """
        logging.info(f"Starting APK generation for: '{arabic_description}'")

        parsed_data = self._parse_arabic_description(arabic_description)
        app_name = parsed_data["app_name"].replace(" ", "") # Remove spaces for directory names
        if not app_name:
            app_name = "DefaultAppName"

        project_path = self._create_project_directory(app_name)
        self._generate_gradle_files(project_path, app_name)
        package_path = os.path.join(project_path, "app", "src", "main", "java", "com", "example", app_name.lower())
        self._generate_main_activity(package_path, app_name)
        layout_path = os.path.join(project_path, "app", "src", "main", "res", "layout")
        self._generate_activity_main_layout(layout_path, app_name)

        # Add more logic here to dynamically generate other activities, fragments,
        # or modify layouts based on parsed_data["ui_elements"].

        logging.info(f"Basic project structure for '{app_name}' generated at: {project_path}")

        # Placeholder for actual APK compilation. This requires Android SDK and build tools.
        # In a real scenario, you would call 'gradlew assembleDebug' or 'gradlew assembleRelease'
        # using subprocess.
        # For now, we return the project path.
        # Example of calling gradlew (requires Android SDK and Gradle installed):
        # try:
        #     subprocess.run(["./gradlew", "assembleDebug"], cwd=project_path, check=True, capture_output=True, text=True)
        #     logging.info("Successfully built APK (debug).")
        #     # Find the APK file in app/build/outputs/apk/debug/
        #     apk_path = os.path.join(project_path, "app", "build", "outputs", "apk", "debug", f"{app_name.lower()}-debug.apk")
        #     return apk_path
        # except FileNotFoundError:
        #     logging.error("Gradle wrapper not found or not executable. Ensure Android SDK and Gradle are set up.")
        #     return f"Project structure generated at {project_path}, but APK build failed. Ensure Gradle is configured."
        # except subprocess.CalledProcessError as e:
        #     logging.error(f"Gradle build failed: {e.stderr}")
        #     return f"Project structure generated at {project_path}, but APK build failed. Error: {e.stderr}"

        return f"Project structure for '{app_name}' generated successfully at: {project_path}. APK compilation requires Android SDK and Gradle setup."

# --- DEMO USAGE ---
# This part would be called from another lobe.
# For demonstration, we'll include it here but it should be separate.

def demo_arabic_apk_generation():
    """
    Demonstrates the ArabicAPKGenerator module.
    """
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
    if not os.path.exists(JAVA_PROJECT_DIR):
        os.makedirs(JAVA_PROJECT_DIR)

    generator = ArabicAPKGenerator(JAVA_PROJECT_DIR, KNOWLEDGE_BASE_DIR)

    # Example Arabic descriptions
    arabic_prompt_1 = "أريد تطبيقاً اسمه آلة حاسبة بسيط، به زر للجمع وزر للطرح."
    arabic_prompt_2 = "أنشئ لي تطبيقاً لعرض رسالة ترحيب، عنوانه هو 'أهلاً بك'."
    arabic_prompt_3 = "تطبيق اسمه مدقق الإملاء، به حقل نص لإدخال الكلمات."

    print("\n--- Initiating Arabic APK Generation Module Demo ---")

    # Test Case 1: Simple Calculator App
    print(f"\nProcessing prompt: '{arabic_prompt_1}'")
    result_1 = generator.generate_apk_from_arabic(arabic_prompt_1)
    print(f"Result for prompt 1: {result_1}")

    # Test Case 2: Welcome Message App
    print(f"\nProcessing prompt: '{arabic_prompt_2}'")
    result_2 = generator.generate_apk_from_arabic(arabic_prompt_2)
    print(f"Result for prompt 2: {result_2}")

    # Test Case 3: Spelling Checker App
    print(f"\nProcessing prompt: '{arabic_prompt_3}'")
    result_3 = generator.generate_apk_from_arabic(arabic_prompt_3)
    print(f"Result for prompt 3: {result_3}")

    print("\n--- Arabic APK Generation Module Demo Finished ---")

    # Cleanup is handled by other lobes or a dedicated cleanup function.
    # For this module's demo, we just show generation.