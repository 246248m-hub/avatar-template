import os
import json
import re
from typing import List, Dict, Any

# Constants for Lobe 4
KNOWLEDGE_BASE_DIR = "knowledge_base"
ARABIC_NLP_MODULE_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_nlp_module.json")
CODE_TEMPLATE_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "code_templates")
ANDROID_MANIFEST_TEMPLATE = "AndroidManifest.xml"
ACTIVITY_TEMPLATE = "MainActivity.java"
BUILD_GRADLE_APP_TEMPLATE = "build.gradle.app"
BUILD_GRADLE_PROJECT_TEMPLATE = "build.gradle.project"

# Ensure code template directory exists
if not os.path.exists(CODE_TEMPLATE_DIR):
    os.makedirs(CODE_TEMPLATE_DIR)

# --- Dummy Data and Helper Functions (simulating existing Lobe 0 functionality) ---

def create_dummy_arabic_nlp_module_config():
    """Creates a dummy configuration for the Arabic NLP module."""
    config = {
        "arabic_tokenizer_model": "path/to/arabic_tokenizer.model",
        "arabic_parser_model": "path/to/arabic_parser.model",
        "arabic_intent_recognition_model": "path/to/arabic_intent_model",
        "entity_mapping": {
            "اسم التطبيق": "appName",
            "الإجراء": "action",
            "البيانات": "data"
        }
    }
    with open(ARABIC_NLP_MODULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print(f"Created dummy Arabic NLP module config: {ARABIC_NLP_MODULE_FILE}")

def create_dummy_code_templates():
    """Creates dummy code template files."""
    if not os.path.exists(CODE_TEMPLATE_DIR):
        os.makedirs(CODE_TEMPLATE_DIR)

    with open(os.path.join(CODE_TEMPLATE_DIR, ANDROID_MANIFEST_TEMPLATE), 'w', encoding='utf-8') as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="__PACKAGE_NAME__">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="__APP_NAME__"
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
""")
    print(f"Created dummy template: {os.path.join(CODE_TEMPLATE_DIR, ANDROID_MANIFEST_TEMPLATE)}")

    with open(os.path.join(CODE_TEMPLATE_DIR, ACTIVITY_TEMPLATE), 'w', encoding='utf-8') as f:
        f.write("""package __PACKAGE_NAME__;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("__INITIAL_MESSAGE__");
    }
}
""")
    print(f"Created dummy template: {os.path.join(CODE_TEMPLATE_DIR, ACTIVITY_TEMPLATE)}")

    with open(os.path.join(CODE_TEMPLATE_DIR, BUILD_GRADLE_APP_TEMPLATE), 'w', encoding='utf-8') as f:
        f.write("""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace '__PACKAGE_NAME__'
    compileSdk 33

    defaultConfig {
        applicationId "__PACKAGE_NAME__"
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

    implementation 'androidx.core:core-ktx:1.10.1'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""")
    print(f"Created dummy template: {os.path.join(CODE_TEMPLATE_DIR, BUILD_GRADLE_APP_TEMPLATE)}")

    with open(os.path.join(CODE_TEMPLATE_DIR, BUILD_GRADLE_PROJECT_TEMPLATE), 'w', encoding='utf-8') as f:
        f.write("""
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:7.4.2" // Example version
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.10" // Example version
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
""")
    print(f"Created dummy template: {os.path.join(CODE_TEMPLATE_DIR, BUILD_GRADLE_PROJECT_TEMPLATE)}")

def cleanup_dummy_files():
    """Cleans up dummy files and directories."""
    if os.path.exists(ARABIC_NLP_MODULE_FILE):
        os.remove(ARABIC_NLP_MODULE_FILE)
        print(f"Removed dummy file: {ARABIC_NLP_MODULE_FILE}")
    if os.path.exists(CODE_TEMPLATE_DIR):
        import shutil
        shutil.rmtree(CODE_TEMPLATE_DIR)
        print(f"Removed dummy directory: {CODE_TEMPLATE_DIR}")
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        # Only remove if empty after other removals
        if not os.listdir(KNOWLEDGE_BASE_DIR):
            os.rmdir(KNOWLEDGE_BASE_DIR)
            print(f"Removed empty knowledge base directory: {KNOWLEDGE_BASE_DIR}")

# --- Lobe 4: Code Generation Lobe ---

class CodeGenerator:
    """
    Generates Android project files from structured natural language input.
    This lobe focuses on the initial scaffolding of an Android project based on
    parsed Arabic input.
    """
    def __init__(self, templates_dir: str, knowledge_base_dir: str):
        self.templates_dir = templates_dir
        self.knowledge_base_dir = knowledge_base_dir
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Loads code templates from the specified directory."""
        loaded_templates = {}
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".xml") or filename.endswith(".gradle") or filename.endswith(".java"):
                filepath = os.path.join(self.templates_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    loaded_templates[filename] = f.read()
        return loaded_templates

    def generate_android_project_structure(self, app_name: str, package_name: str, initial_message: str = "Hello, World!") -> Dict[str, str]:
        """
        Generates the core files for a basic Android project.

        Args:
            app_name (str): The name of the application.
            package_name (str): The package name for the Android application.
            initial_message (str): The initial text to display in the MainActivity.

        Returns:
            Dict[str, str]: A dictionary where keys are filenames and values are
                            the generated file content.
        """
        if not all([app_name, package_name]):
            raise ValueError("App name and package name are required for project generation.")

        generated_files = {}

        # AndroidManifest.xml
        manifest_content = self.templates.get(ANDROID_MANIFEST_TEMPLATE, "")
        manifest_content = manifest_content.replace("__PACKAGE_NAME__", package_name)
        manifest_content = manifest_content.replace("__APP_NAME__", app_name)
        generated_files[f"{package_name.replace('.', '/')}/AndroidManifest.xml"] = manifest_content

        # MainActivity.java
        activity_content = self.templates.get(ACTIVITY_TEMPLATE, "")
        activity_content = activity_content.replace("__PACKAGE_NAME__", package_name)
        activity_content = activity_content.replace("__INITIAL_MESSAGE__", initial_message)
        generated_files[f"{package_name.replace('.', '/')}/app/src/main/java/{package_name.replace('.', '/')}/MainActivity.java"] = activity_content

        # build.gradle (app level)
        build_gradle_app_content = self.templates.get(BUILD_GRADLE_APP_TEMPLATE, "")
        build_gradle_app_content = build_gradle_app_content.replace("__PACKAGE_NAME__", package_name)
        generated_files[f"{package_name.replace('.', '/')}/build.gradle"] = build_gradle_app_content

        # build.gradle (project level)
        build_gradle_project_content = self.templates.get(BUILD_GRADLE_PROJECT_TEMPLATE, "")
        generated_files["build.gradle"] = build_gradle_project_content

        # Dummy layout file (activity_main.xml) - required by MainActivity
        generated_files[f"{package_name.replace('.', '/')}/app/src/main/res/layout/activity_main.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        print("Generated dummy activity_main.xml")

        # Dummy ic_launcher files (required by AndroidManifest)
        # For simplicity, we'll create placeholder files. A real system would generate proper icons.
        launcher_icon_dir = os.path.join(self.knowledge_base_dir, f"{package_name.replace('.', '/')}/app/src/main/res/mipmap-hdpi")
        if not os.path.exists(launcher_icon_dir):
            os.makedirs(launcher_icon_dir)
        with open(os.path.join(launcher_icon_dir, "ic_launcher.png"), "wb") as f:
            f.write(b"dummy_icon_data")
        print(f"Created dummy icon: {os.path.join(launcher_icon_dir, 'ic_launcher.png')}")
        launcher_icon_round_dir = os.path.join(self.knowledge_base_dir, f"{package_name.replace('.', '/')}/app/src/main/res/mipmap-hdpi")
        if not os.path.exists(launcher_icon_round_dir):
            os.makedirs(launcher_icon_round_dir)
        with open(os.path.join(launcher_icon_round_dir, "ic_launcher_round.png"), "wb") as f:
            f.write(b"dummy_icon_data")
        print(f"Created dummy icon: {os.path.join(launcher_icon_round_dir, 'ic_launcher_round.png')}")


        # The structure is usually:
        # project_root/
        #   app/
        #     build.gradle
        #     src/
        #       main/
        #         AndroidManifest.xml
        #         java/
        #           com/example/myapp/MainActivity.java
        #         res/
        #           layout/
        #             activity_main.xml
        #           mipmap-hdpi/
        #             ic_launcher.png
        #             ic_launcher_round.png
        #   build.gradle (project level)

        # Let's adjust the keys to reflect a more typical structure, assuming we're generating
        # the content that would be *inside* a target directory.
        final_generated_files = {}
        for key, value in generated_files.items():
            # Reconstruct path assuming a base project dir
            if key.endswith("AndroidManifest.xml"):
                 final_generated_files[os.path.join("app", "src", "main", key)] = value
            elif key.endswith(".java"):
                 java_path_parts = key.split('/')
                 # Find the start of the package path and reconstruct
                 try:
                     java_pkg_index = java_path_parts.index(package_name.split('.')[-1])
                     final_generated_files[os.path.join("app", "src", "main", "java", *java_path_parts[java_pkg_index:])] = value
                 except ValueError:
                      # Fallback if package name isn't found as expected
                      final_generated_files[os.path.join("app", "src", "main", "java", key)] = value

            elif key.endswith(".gradle") and "build.gradle.app" in key:
                 final_generated_files[os.path.join("app", "build.gradle")] = value
            elif key.endswith(".gradle") and "build.gradle.project" in key:
                 final_generated_files["build.gradle"] = value
            elif key.endswith("activity_main.xml"):
                 final_generated_files[os.path.join("app", "src", "main", "res", "layout", "activity_main.xml")] = value
            elif "ic_launcher.png" in key:
                 final_generated_files[os.path.join("app", "src", "main", "res", "mipmap-hdpi", "ic_launcher.png")] = value
            elif "ic_launcher_round.png" in key:
                 final_generated_files[os.path.join("app", "src", "main", "res", "mipmap-hdpi", "ic_launcher_round.png")] = value
            else:
                 # For any other keys, try to infer a sensible path
                 final_generated_files[key] = value


        return final_generated_files


def demonstrate_code_generation_module():
    """Demonstrates the functionality of the CodeGenerator Lobe."""
    print("\n--- Initiating Lobe 4: Code Generation Module Demo ---")

    # Ensure necessary dummy files and directories exist for demonstration
    create_dummy_arabic_nlp_module_config()
    create_dummy_code_templates()

    try:
        # Simulate a parsed Arabic input that translates to desired app parameters
        # This would typically come from Lobe 0 (Language) or Lobe 1 (Arabic) after processing.
        parsed_nl_input = {
            "appName": "تطبيقي الأول",
            "package": "com.example.myfirstapp",
            "initialMessage": "أهلاً بك في تطبيقي!"
        }

        print(f"\nSimulating parsed NLP input: {parsed_nl_input}")

        # Instantiate the CodeGenerator
        code_generator = CodeGenerator(templates_dir=CODE_TEMPLATE_DIR, knowledge_base_dir=KNOWLEDGE_BASE_DIR)

        # Generate the project structure
        generated_apk_components = code_generator.generate_android_project_structure(
            app_name=parsed_nl_input["appName"],
            package_name=parsed_nl_input["package"],
            initial_message=parsed_nl_input["initialMessage"]
        )

        print(f"\n--- Generated Android Project Components ---")
        for filename, content in generated_apk_components.items():
            print(f"Generated '{filename}' (length: {len(content)} bytes)")
            # In a real scenario, these would be written to disk in a project directory.
            # For demonstration, we'll just show they were created.

        # Example of generating a different app
        parsed_nl_input_2 = {
            "appName": "مفكرة بسيطة",
            "package": "com.example.simplememo",
            "initialMessage": "ابدأ بكتابة ملاحظاتك."
        }
        print(f"\nSimulating parsed NLP input: {parsed_nl_input_2}")
        generated_apk_components_2 = code_generator.generate_android_project_structure(
            app_name=parsed_nl_input_2["appName"],
            package_name=parsed_nl_input_2["package"],
            initial_message=parsed_nl_input_2["initialMessage"]
        )
        print(f"\n--- Generated Android Project Components (App 2) ---")
        for filename, content in generated_apk_components_2.items():
            print(f"Generated '{filename}' (length: {len(content)} bytes)")

    except Exception as e:
        print(f"An error occurred during code generation demo: {e}")

    print("\n--- Lobe 4: Code Generation Module Demo Finished ---")

# --- Main Execution Block (for demonstration purposes) ---

if __name__ == "__main__":
    # Ensure knowledge base directory exists for NLP module config
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Created knowledge base directory: {KNOWLEDGE_BASE_DIR}")

    # This function call would typically be orchestrated by a higher-level lobe
    # or a main loop. For this standalone demo, we call it directly.
    demonstrate_code_generation_module()

    # Clean up dummy files created for this lobe's demo
    print("\n--- Cleaning up dummy files for Lobe 4 ---")
    cleanup_dummy_files()

    print("\n--- Lobe 4: Code Generation Module Demo Finished Entirely ---")