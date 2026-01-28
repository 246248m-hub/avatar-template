import os
import re
import shutil
from pathlib import Path

# --- Configuration ---
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
APK_STRUCTURE_TEMPLATES_DIR = Path("./apk_structure_templates")
DEFAULT_PACKAGE_NAME = "com.example.myapp"
DEFAULT_APP_NAME = "MyApp"

# --- Helper Functions ---

def create_directory_if_not_exists(dir_path: Path):
    """Creates a directory if it doesn't exist."""
    dir_path.mkdir(parents=True, exist_ok=True)

def load_text_from_file(file_path: Path) -> str:
    """Loads text content from a given file path."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_text_to_file(file_path: Path, content: str):
    """Saves text content to a given file path."""
    create_directory_if_not_exists(file_path.parent)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def cleanup_dummy_files():
    """Cleans up dummy files and directories created for demos."""
    if KNOWLEDGE_BASE_DIR.exists():
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
    if APK_STRUCTURE_TEMPLATES_DIR.exists():
        shutil.rmtree(APK_STRUCTURE_TEMPLATES_DIR)
    # Add any other temporary files/dirs created by previous lobes here

# --- Lobe 0: Language Lobe (Arabic Focus) ---

class ArabicParser:
    """
    A parser specifically designed to understand Arabic natural language
    instructions for APK generation.
    """
    def __init__(self):
        self.arabic_keywords = {
            "اسم_التطبيق": "app_name",
            "اسم_الحزمة": "package_name",
            "شاشة_رئيسية": "main_activity",
            "مكون_واجهة": "ui_component",
            "زر": "button",
            "نص": "text_view",
            "حقل_إدخال": "edit_text",
            "قائمة": "list_view",
            "إجراء": "action",
            "فتح": "open",
            "عرض": "display",
            "تخزين": "storage",
            "قاعدة_بيانات": "database",
            "اتصال_شبكة": "network_request",
            "صورة": "image_view",
            "تنسيق": "layout",
            "عمودي": "vertical",
            "أفقي": "horizontal",
            "تخطيط": "layout"
        }

    def parse_instruction(self, instruction: str) -> dict:
        """
        Parses an Arabic natural language instruction into a structured dictionary.
        This is a simplified example and would require more sophisticated NLP
        techniques for real-world use (e.g., using libraries like Farasa, CAMeL Tools).
        """
        parsed_data = {}
        words = instruction.split()

        # Simple keyword matching for demonstration
        for i, word in enumerate(words):
            if word in self.arabic_keywords:
                keyword_meaning = self.arabic_keywords[word]
                if keyword_meaning == "app_name":
                    # Assume app name follows the keyword
                    if i + 1 < len(words):
                        parsed_data["app_name"] = words[i+1]
                elif keyword_meaning == "package_name":
                    # Assume package name follows the keyword
                    if i + 1 < len(words):
                        parsed_data["package_name"] = words[i+1]
                elif keyword_meaning == "main_activity":
                    if i + 1 < len(words):
                        parsed_data["main_activity"] = words[i+1]
                elif keyword_meaning == "ui_component":
                    # This is a broad category, would need more context
                    pass
                elif keyword_meaning == "layout":
                    if i + 1 < len(words):
                        parsed_data["layout_type"] = words[i+1] # e.g., "vertical", "horizontal"

        # Extract specific UI component definitions (simplified)
        ui_elements = []
        for word in words:
            if word in ["زر", "نص", "حقل_إدخال", "قائمة", "صورة"]:
                ui_elements.append({"type": word, "label": f"Component_{len(ui_elements) + 1}"}) # Simplified label
        if ui_elements:
            parsed_data["ui_elements"] = ui_elements

        return parsed_data

# --- Lobe 1: APK Structure Lobe (Templates) ---

class ApkStructureGenerator:
    """
    Generates the basic directory and file structure for an Android APK
    based on parsed instructions.
    """
    def __init__(self, apk_structure_templates_path: Path = APK_STRUCTURE_TEMPLATES_DIR):
        self.templates_path = apk_structure_templates_path
        self.structure_templates = {}
        self._load_templates()

    def _load_templates(self):
        """Loads predefined directory and file templates for APK structure."""
        # In a real scenario, these would be external template files (e.g., XML, JSON)
        # For this example, we'll define them programmatically.
        self.structure_templates = {
            "base": {
                "directories": [
                    "app",
                    "app/src",
                    "app/src/main",
                    "app/src/main/java",
                    "app/src/main/res",
                    "app/src/main/res/layout",
                    "app/src/main/res/values",
                    "app/src/main/AndroidManifest.xml",
                    "gradle",
                    "gradle/wrapper",
                    "gradlew",
                    "gradlew.bat",
                    "build.gradle",
                    "settings.gradle"
                ],
                "files": {
                    "app/src/main/res/values/strings.xml": "<resources>\n    <string name=\"app_name\">{app_name}</string>\n</resources>",
                    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name_camel}">

        <activity android:name=".{main_activity}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>""",
                    "build.gradle": """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {
        applicationId "{package_name}"
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
    androidTestImplementation 'androidx.test.core:core:1.5.0'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""",
                    "settings.gradle": """pluginManagement {
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
rootProject.name = "{app_name_gradle}"
include ':app'
"""
                }
            }
        }

    def generate_android_project_structure(self, project_dir: Path, apk_config: dict):
        """
        Creates the directory and file structure for a new Android project.

        Args:
            project_dir: The root directory for the new Android project.
            apk_config: A dictionary containing configuration like app_name, package_name.
        """
        create_directory_if_not_exists(project_dir)
        app_name = apk_config.get("app_name", DEFAULT_APP_NAME)
        package_name = apk_config.get("package_name", DEFAULT_PACKAGE_NAME)
        main_activity = apk_config.get("main_activity", "MainActivity")

        app_name_camel = "".join(word.capitalize() for word in app_name.split())
        app_name_gradle = app_name.lower().replace(" ", "")

        # Create base structure
        for dir_name in self.structure_templates["base"]["directories"]:
            target_path = project_dir / dir_name
            create_directory_if_not_exists(target_path)

        # Populate files with content
        for file_path_str, content_template in self.structure_templates["base"]["files"].items():
            target_file_path = project_dir / file_path_str
            content = content_template.format(
                app_name=app_name,
                package_name=package_name,
                main_activity=main_activity,
                app_name_camel=app_name_camel,
                app_name_gradle=app_name_gradle
            )
            save_text_to_file(target_file_path, content)

        print(f"Generated Android project structure in: {project_dir}")

# --- Main Demonstration Function ---

def demo_arabic_processing_and_apk_struct_generation():
    """
    Demonstrates the integration of Arabic parsing and APK structure generation.
    """
    print("\n--- Starting Arabic Parser and APK Structure Generation Demo ---")

    # Initialize components
    arabic_parser = ArabicParser()
    apk_struct_generator = ApkStructureGenerator()

    # Example Arabic instruction
    arabic_instruction = "بناء تطبيق جديد اسمه 'مساعدي' وحزمة 'com.example.myhelper' والشاشة الرئيسية 'HomeActivity'."

    print(f"\nParsing Arabic instruction: '{arabic_instruction}'")
    parsed_config = arabic_parser.parse_instruction(arabic_instruction)
    print(f"Parsed configuration: {parsed_config}")

    # Determine project directory (e.g., based on app name)
    app_name_for_dir = parsed_config.get("app_name", DEFAULT_APP_NAME)
    project_root_dir = Path(f"./generated_projects/{app_name_for_dir.replace(' ', '_').lower()}")

    print(f"\nGenerating APK structure for project: {project_root_dir}")
    apk_struct_generator.generate_android_project_structure(project_root_dir, parsed_config)

    print("\n--- Arabic Parser and APK Structure Generation Demo Finished ---")

if __name__ == "__main__":
    # Ensure dummy directories are clean before starting
    cleanup_dummy_files()
    create_directory_if_not_exists(KNOWLEDGE_BASE_DIR)
    create_directory_if_not_exists(APK_STRUCTURE_TEMPLATES_DIR)

    demo_arabic_processing_and_apk_struct_generation()

    # Optional: Clean up generated project directories after demo
    print("\n--- Cleaning up generated project directories ---")
    generated_projects_dir = Path("./generated_projects")
    if generated_projects_dir.exists():
        shutil.rmtree(generated_projects_dir)
        print(f"Removed: {generated_projects_dir}")

    cleanup_dummy_files()
    print("\n--- Demo Complete ---")