import os
import shutil
import subprocess
from pathlib import Path

# Define constants for Arabic language processing and APK generation
ARABIC_LEXICON_PATH = Path("knowledge_base/arabic_lexicon.txt")
ARABIC_GRAMMAR_RULES_PATH = Path("knowledge_base/arabic_grammar.json")
JAVA_SOURCE_DIR = Path("generated_apk_project/app/src/main/java/com/example/myapp")
ANDROID_MANIFEST_PATH = Path("generated_apk_project/app/src/main/AndroidManifest.xml")
GRADLE_PROPERTIES_PATH = Path("generated_apk_project/gradle.properties")
BUILD_GRADLE_PATH = Path("generated_apk_project/app/build.gradle")
SETTINGS_GRADLE_PATH = Path("generated_apk_project/settings.gradle")
DUMMY_PROJECT_ROOT = Path("generated_apk_project")

class ArabicParser:
    """
    A class to parse Arabic natural language input, extract semantic meaning,
    and translate it into structured data suitable for code generation.
    """
    def __init__(self, lexicon_path: Path, grammar_rules_path: Path):
        self.lexicon = self._load_lexicon(lexicon_path)
        self.grammar_rules = self._load_grammar_rules(grammar_rules_path)

    def _load_lexicon(self, lexicon_path: Path) -> dict:
        """Loads the Arabic lexicon from a file."""
        lexicon = {}
        if lexicon_path.exists():
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word, meaning = line.strip().split(':', 1)
                    lexicon[word.strip()] = meaning.strip()
        else:
            print(f"Warning: Lexicon file not found at {lexicon_path}. Proceeding with an empty lexicon.")
        return lexicon

    def _load_grammar_rules(self, grammar_rules_path: Path) -> dict:
        """Loads Arabic grammar rules from a JSON file."""
        import json
        rules = {}
        if grammar_rules_path.exists():
            with open(grammar_rules_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
        else:
            print(f"Warning: Grammar rules file not found at {grammar_rules_path}. Proceeding with empty rules.")
        return rules

    def parse(self, arabic_text: str) -> dict:
        """
        Parses the Arabic text to extract structured semantic information.
        This is a placeholder for actual NLP parsing logic.
        In a real scenario, this would involve tokenization, POS tagging,
        dependency parsing, and semantic role labeling, potentially using
        libraries like Farasa, CAMeL Tools, or custom models.
        """
        print(f"Parsing Arabic text: '{arabic_text}'")
        # --- Placeholder for actual Arabic NLP parsing ---
        # For demonstration, we'll simulate extraction based on keywords.
        parsed_data = {
            "intent": "unknown",
            "entities": {},
            "actions": []
        }

        # Simple keyword-based intent and entity extraction
        if "إنشاء" in arabic_text or "بناء" in arabic_text:
            parsed_data["intent"] = "create_apk"
        if "عرض" in arabic_text or "نافذة" in arabic_text:
            parsed_data["intent"] = "display_ui"
        if "إرسال" in arabic_text or "رسالة" in arabic_text:
            parsed_data["intent"] = "send_message"

        # Extract entities by looking up words in the lexicon
        words = arabic_text.split()
        for word in words:
            if word in self.lexicon:
                if self.lexicon[word] == "button_text":
                    parsed_data["entities"]["button_text"] = word
                elif self.lexicon[word] == "message_content":
                    parsed_data["entities"]["message_content"] = word
                elif self.lexicon[word] == "activity_name":
                    parsed_data["entities"]["activity_name"] = word

        # Simulate extracting actions based on intent and entities
        if parsed_data["intent"] == "create_apk":
            parsed_data["actions"].append({"type": "generate_android_project", "name": parsed_data.get("entities", {}).get("activity_name", "MainActivity")})
        elif parsed_data["intent"] == "display_ui" and "button_text" in parsed_data["entities"]:
            parsed_data["actions"].append({"type": "add_button", "label": parsed_data["entities"]["button_text"]})
        elif parsed_data["intent"] == "send_message" and "message_content" in parsed_data["entities"]:
            parsed_data["actions"].append({"type": "send_notification", "content": parsed_data["entities"]["message_content"]})

        print(f"Parsed data: {parsed_data}")
        return parsed_data

class APKStructureGenerator:
    """
    A class to generate the basic structure of an Android APK project
    based on parsed semantic information.
    """
    def __init__(self, base_project_path: Path = DUMMY_PROJECT_ROOT):
        self.base_project_path = base_project_path
        self.java_source_dir = self.base_project_path / "app" / "src" / "main" / "java" / "com" / "example" / "myapp"
        self.manifest_path = self.base_project_path / "app" / "src" / "main" / "AndroidManifest.xml"
        self.gradle_properties_path = self.base_project_path / "gradle.properties"
        self.build_gradle_path = self.base_project_path / "app" / "build.gradle"
        self.settings_gradle_path = self.base_project_path / "settings.gradle"

    def create_project_structure(self, app_name: str = "MyApp"):
        """Creates the basic directory structure for an Android project."""
        print(f"Creating project structure for '{app_name}' at '{self.base_project_path}'...")

        # Clean up existing project if it exists
        if self.base_project_path.exists():
            print(f"Removing existing project directory: {self.base_project_path}")
            shutil.rmtree(self.base_project_path)

        # Create directories
        self.java_source_dir.mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "androidTest" / "java" / "com" / "example" / "myapp").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "test" / "java" / "com" / "example" / "myapp").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "gradle" / "wrapper").mkdir(parents=True, exist_ok=True)

        # Create essential files with minimal content
        self._create_empty_file(self.manifest_path)
        self._create_empty_file(self.gradle_properties_path)
        self._create_empty_file(self.build_gradle_path)
        self._create_empty_file(self.settings_gradle_path)
        self._create_empty_file(self.base_project_path / "build.gradle") # Project level build.gradle
        self._create_empty_file(self.base_project_path / "gradlew") # Gradle wrapper script
        self._create_empty_file(self.base_project_path / "gradlew.bat") # Gradle wrapper script for Windows

        # Populate with basic content
        self._populate_android_manifest(app_name)
        self._populate_settings_gradle(app_name)
        self._populate_build_gradle()
        self._populate_gradle_properties()
        self._populate_project_build_gradle()
        self._populate_gradle_wrapper()

        print("Project structure created successfully.")

    def _create_empty_file(self, file_path: Path):
        """Creates an empty file if it doesn't exist."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

    def _populate_android_manifest(self, app_name: str):
        """Populates the AndroidManifest.xml with basic content."""
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">

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
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest_content)

    def _populate_settings_gradle(self, app_name: str):
        """Populates the settings.gradle file."""
        settings_content = f"""pluginManagement {{
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
rootProject.name = "{app_name}"
include ':app'
"""
        with open(self.settings_gradle_path, 'w', encoding='utf-8') as f:
            f.write(settings_content)

    def _populate_build_gradle(self):
        """Populates the app/build.gradle file."""
        build_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.myapp'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 24
        targetSdk 34
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
        viewBinding true
    }
}

dependencies {

    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
        with open(self.build_gradle_path, 'w', encoding='utf-8') as f:
            f.write(build_gradle_content)

    def _populate_gradle_properties(self):
        """Populates the gradle.properties file."""
        gradle_properties_content = """org.gradle.jvmargs=-Xmx2048m
android.useAndroidX=true
android.enableJetifier=true
"""
        with open(self.gradle_properties_path, 'w', encoding='utf-8') as f:
            f.write(gradle_properties_content)

    def _populate_project_build_gradle(self):
        """Populates the root build.gradle file."""
        project_build_gradle_content = """// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id 'com.android.application' version '8.1.1' apply false
    id 'com.android.library' version '8.1.1' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.0' apply false
}
"""
        with open(self.base_project_path / "build.gradle", 'w', encoding='utf-8') as f:
            f.write(project_build_gradle_content)

    def _populate_gradle_wrapper(self):
        """Creates basic gradle wrapper files."""
        # Gradle wrapper properties
        wrapper_properties_content = """distributionBase=GRADLE_USER_HOME
distributionUrl=https\://services.gradle.org/distributions/gradle-8.4-bin.zip
distributionPath=wrapper/dists
zipStorePath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
"""
        with open(self.base_project_path / "gradle" / "wrapper" / "gradle-wrapper.properties", 'w', encoding='utf-8') as f:
            f.write(wrapper_properties_content)

        # Gradle wrapper script (Linux/macOS)
        gradlew_content = """#!/bin/sh

"$IDEMPOTENT_SCRIPT_DIR/../gradlew" "$@"

"""
        with open(self.base_project_path / "gradlew", 'w', encoding='utf-8') as f:
            f.write(gradlew_content)
        os.chmod(self.base_project_path / "gradlew", 0o755) # Make executable

        # Gradle wrapper script (Windows)
        gradlew_bat_content = """@rem
@echo off

if "%DEBUG_градlew%" == "" (
    rem Calculate the location of the WM_SCRIPT directory
    set WM_SCRIPT=%~dp0
    rem Remove trailing slash if present
    if "%WM_SCRIPT:~-1%" == "\\" set WM_SCRIPT=%WM_SCRIPT:~0,-1%
    rem Set the GRADLEW variable to the path of the gradlew script
    set GRADLEW=%WM_SCRIPT%\gradlew.bat
)

"%GRADLEW%" %*
"""
        with open(self.base_project_path / "gradlew.bat", 'w', encoding='utf-8') as f:
            f.write(gradlew_bat_content)

    def generate_activity_file(self, activity_name: str, layout_name: str = "activity_main"):
        """Generates a basic Java activity file."""
        java_file_path = self.java_source_dir / f"{activity_name}.java"
        java_content = f"""package com.example.myapp;

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
        with open(java_file_path, 'w', encoding='utf-8') as f:
            f.write(java_content)
        print(f"Generated activity file: {java_file_path}")

    def add_button_to_layout(self, button_text: str, activity_name: str = "MainActivity"):
        """
        Adds a button to a layout file. This is a simplified representation.
        A real implementation would involve parsing and modifying XML layout files.
        """
        layout_file_name = f"activity_{activity_name.lower()}.xml"
        layout_dir = self.base_project_path / "app" / "src" / "main" / "res" / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        layout_file_path = layout_dir / layout_file_name

        if not layout_file_path.exists():
            # Create a basic layout file if it doesn't exist
            initial_layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <!-- Add buttons here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
            with open(layout_file_path, 'w', encoding='utf-8') as f:
                f.write(initial_layout_content)
            print(f"Created initial layout file: {layout_file_path}")

        # Read existing content
        with open(layout_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the closing tag of the root layout element
        insert_index = -1
        for i, line in enumerate(lines):
            if "ConstraintLayout" in line and "app:layout_constraintTop_toTopOf" in line: # Heuristic to find the last element before closing
                insert_index = i
                break
            elif "</androidx.constraintlayout.widget.ConstraintLayout>" in line:
                insert_index = i
                break


        if insert_index != -1:
            # Add the new button
            button_id = f"button_{button_text.lower().replace(' ', '_')}"
            button_content = f"""
    <Button
        android:id="@+id/{button_id}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{button_text}"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/some_previous_element" />
""" # Note: `some_previous_element` is a placeholder for proper constraint setup.

            lines.insert(insert_index, button_content)

            # Write back to the file
            with open(layout_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Added button '{button_text}' to {layout_file_name}")
        else:
            print(f"Could not find suitable insertion point for button in {layout_file_name}.")


    def create_notification_channel_code(self, activity_name: str = "MainActivity"):
        """
        Generates code for creating a notification channel.
        This would typically be placed in an Application class or an Activity.
        For simplicity, we'll generate a snippet that can be added.
        """
        notification_service_code = """
    private static final String CHANNEL_ID = "my_channel_id";
    private void createNotificationChannel() {
        // Create the NotificationChannel, but only on API 26+ because
        // the NotificationChannel class is new and not in the support library
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = getString(R.string.channel_name); // Define in strings.xml
            String description = getString(R.string.channel_description); // Define in strings.xml
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);
            // Register the channel with the system; you can't change the importance
            // or other notification behaviors after this
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }
"""
        # This code would need to be integrated into an Activity or Application class.
        # For this generator, we'll just print a message indicating where it should go.
        print("\n--- Notification Channel Code Snippet ---")
        print("To enable notifications, you need to:")
        print("1. Add the following method to your Activity or Application class:")
        print(notification_service_code)
        print("2. Call createNotificationChannel() in onCreate() or appropriate lifecycle method.")
        print("3. Define 'channel_name' and 'channel_description' in your app/src/main/res/values/strings.xml file.")
        print("---------------------------------------")

    def generate_app(self):
        """Triggers the creation of the basic app structure."""
        self.create_project_structure()

class ArabicAPKGeneratorModule:
    """
    The main module that orchestrates the parsing of Arabic language
    and the generation of a basic APK project structure.
    """
    def __init__(self):
        self.arabic_parser = ArabicParser(ARABIC_LEXICON_PATH, ARABIC_GRAMMAR_RULES_PATH)
        self.apk_structure_generator = APKStructureGenerator()

    def process_arabic_prompt(self, prompt: str):
        """
        Processes an Arabic natural language prompt to generate an APK project structure.
        """
        print(f"\n--- Processing Arabic Prompt: '{prompt}' ---")
        parsed_data = self.arabic_parser.parse(prompt)

        if parsed_data["intent"] == "create_apk":
            app_name = parsed_data.get("entities", {}).get("activity_name", "MyApp")
            print(f"Detected intent: Create APK for '{app_name}'")
            self.apk_structure_generator.generate_app() # Create base project structure

            # Add initial activity
            self.apk_structure_generator.generate_activity_file(activity_name=app_name)

            # Process other actions
            for action in parsed_data.get("actions", []):
                if action["type"] == "generate_android_project":
                    # Already handled by intent check, but can be used for naming
                    pass
                elif action["type"] == "add_button":
                    button_text = action.get("label", "Default Button")
                    self.apk_structure_generator.add_button_to_layout(button_text=button_text)
                elif action["type"] == "send_notification":
                    # This action implies a notification setup
                    self.apk_structure_generator.create_notification_channel_code()
                    print(f"Notification content requested: '{action.get('content', '')}' (requires further implementation in code)")

        else:
            print(f"Unsupported intent detected: {parsed_data['intent']}")
            print("Please provide a prompt that indicates APK creation (e.g., 'أنشئ تطبيقاً جديداً').")

        print("--- Arabic Prompt Processing Finished ---")


if __name__ == '__main__':
    # --- Setup Dummy Knowledge Base Files for Demo ---
    # Ensure these files exist for the parser to load, even if empty.
    # In a real scenario, these would contain actual lexicons and grammar.
    os.makedirs("knowledge_base", exist_ok=True)

    if not ARABIC_LEXICON_PATH.exists():
        with open(ARABIC_LEXICON_PATH, "w", encoding="utf-8") as f:
            f.write("شاشة:activity_name\n")
            f.write("زر:button_text\n")
            f.write("نص:message_content\n")
            f.write("إنشاء:create_apk\n")
            f.write("بناء:create_apk\n")
            f.write("عرض:display_ui\n")
            f.write("نافذة:display_ui\n")
            f.write("إرسال:send_message\n")
            f.write("رسالة:send_message\n")

    if not ARABIC_GRAMMAR_RULES_PATH.exists():
        with open(ARABIC_GRAMMAR_RULES_PATH, "w", encoding="utf-8") as f:
            # This would be a JSON object defining grammar rules.
            # For now, an empty JSON object will suffice.
            f.write("{}")

    # --- Demo Usage ---
    generator_module = ArabicAPKGeneratorModule()

    # Example 1: Basic APK creation with an activity name
    prompt_1 = "أنشئ تطبيقاً جديداً باسم شاشة_الرئيسية"
    generator_module.process_arabic_prompt(prompt_1)

    # Example 2: Create APK and add a button
    prompt_2 = "بناء تطبيق ووضع زر باسم 'اضغط هنا'"
    generator_module.process_arabic_prompt(prompt_2)

    # Example 3: Create APK, add button, and request notification setup
    prompt_3 = "إنشاء تطبيق جديد يحتوي على زر 'إظهار رسالة' وإرسال إشعار 'تم الأمر بنجاح'"
    generator_module.process_arabic_prompt(prompt_3)

    # Example 4: Unsupported prompt
    prompt_4 = "ما هو الطقس اليوم؟"
    generator_module.process_arabic_prompt(prompt_4)

    # --- Clean up dummy project directory after demo ---
    print("\n--- Cleaning up dummy project directory ---")
    if DUMMY_PROJECT_ROOT.exists():
        try:
            shutil.rmtree(DUMMY_PROJECT_ROOT)
            print(f"Removed '{DUMMY_PROJECT_ROOT}'")
        except OSError as e:
            print(f"Error removing directory {DUMMY_PROJECT_ROOT}: {e.strerror}")

    print("\n--- Arabic APK Generator Module Demo Finished ---")