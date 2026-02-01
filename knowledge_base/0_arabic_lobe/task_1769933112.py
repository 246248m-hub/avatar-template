import os
import sys
import shutil
import subprocess
import re
import json
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent
SMALI_DIR = PROJECT_ROOT / "smali_code"
TEMP_DIR = PROJECT_ROOT / "temp_build"
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

STRINGS_TEMPLATE = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""

MAIN_ACTIVITY_TEMPLATE = """package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("{greeting_message}");
    }}
}}
"""

ACTIVITY_MAIN_LAYOUT_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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

# --- Helper Functions ---

def create_android_project_structure(project_path: Path, package_name: str, app_name: str, greeting_message: str):
    """Creates the basic Android project directory structure."""
    src_main_path = project_path / "app" / "src" / "main"
    res_layout_path = src_main_path / "res" / "layout"
    res_values_path = src_main_path / "res" / "values"
    java_package_path = src_main_path / "java" / package_name.replace('.', os.sep)

    os.makedirs(res_layout_path, exist_ok=True)
    os.makedirs(res_values_path, exist_ok=True)
    os.makedirs(java_package_path, exist_ok=True)

    # Write AndroidManifest.xml
    manifest_content = MANIFEST_TEMPLATE.format(package_name=package_name)
    with open(src_main_path / "AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Write strings.xml
    strings_content = STRINGS_TEMPLATE.format(app_name=app_name)
    with open(res_values_path / "strings.xml", "w", encoding="utf-8") as f:
        f.write(strings_content)

    # Write activity_main.xml
    with open(res_layout_path / "activity_main.xml", "w", encoding="utf-8") as f:
        f.write(ACTIVITY_MAIN_LAYOUT_TEMPLATE)

    # Write MainActivity.java
    main_activity_content = MAIN_ACTIVITY_TEMPLATE.format(package_name=package_name, greeting_message=greeting_message)
    with open(java_package_path / "MainActivity.java", "w", encoding="utf-8") as f:
        f.write(main_activity_content)

def create_build_gradle_file(project_path: Path, package_name: str):
    """Creates a minimal build.gradle file."""
    build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 24
        targetSdk 34
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
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
    with open(project_path / "build.gradle", "w", encoding="utf-8") as f:
        f.write(build_gradle_content)

def create_settings_gradle_file(project_path: Path):
    """Creates a minimal settings.gradle file."""
    settings_gradle_content = f"""pluginManagement {{
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

rootProject.name = "MyApplication"
include ':app'
"""
    with open(project_path / "settings.gradle", "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)

def create_gradle_wrapper(project_path: Path):
    """Creates the Gradle wrapper files."""
    gradle_wrapper_path = project_path / "gradle" / "wrapper"
    os.makedirs(gradle_wrapper_path, exist_ok=True)

    with open(project_path / "gradlew", "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\nexec gradle/wrapper/gradle-wrapper.jar \"$@\"\n")
    os.chmod(project_path / "gradlew", 0o755)

    with open(project_path / "gradlew.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\nif ''%_OPTIONS%'':'' == ':'' set _OPTIONS=\njava %_OPTIONS% -Dorg.gradle.logging.level=warn -jar "%~dp0gradle/wrapper/gradle-wrapper.jar" %*\n")

    with open(gradle_wrapper_path / "gradle-wrapper.properties", "w", encoding="utf-8") as f:
        f.write("distributionBase=GRADLE_USER_HOME\ndistributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip\ndistributionVersion=8.5\n")

    with open(gradle_wrapper_path / "gradle-wrapper.jar", "wb") as f:
        # This is a placeholder for the actual gradle-wrapper.jar.
        # In a real scenario, you would download this or use a known path.
        # For this example, we'll assume it's provided or will be downloaded by Gradle itself.
        pass

def cleanup_dummy_files():
    """Removes temporary directories and files."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print(f"Removed temporary directory: {TEMP_DIR}")
    if SMALI_DIR.exists():
        shutil.rmtree(SMALI_DIR)
        print(f"Removed smali directory: {SMALI_DIR}")

# --- Lobe Function ---

def parse_arabic_nlp_output(nlp_output: dict) -> dict:
    """
    Parses the structured NLP output from Arabic Lobe to extract project details.

    Args:
        nlp_output (dict): A dictionary containing parsed Arabic NLP results.
                           Expected keys: 'app_name', 'package_name', 'greeting_message'.

    Returns:
        dict: A dictionary with extracted and validated project details.
              Returns an empty dictionary if required keys are missing or invalid.
    """
    project_details = {}

    # Extract and validate app_name
    app_name = nlp_output.get("app_name")
    if app_name and isinstance(app_name, str) and 3 <= len(app_name) <= 30:
        # Sanitize for XML resource names (basic sanitization)
        project_details["app_name"] = re.sub(r'[^\w\s-]', '', app_name).strip()
    else:
        print("Warning: Invalid or missing 'app_name'.")
        return {}

    # Extract and validate package_name
    package_name = nlp_output.get("package_name")
    if package_name and isinstance(package_name, str) and re.match(r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$', package_name):
        project_details["package_name"] = package_name
    else:
        print("Warning: Invalid or missing 'package_name'. Must follow Java package naming conventions.")
        return {}

    # Extract and validate greeting_message
    greeting_message = nlp_output.get("greeting_message")
    if greeting_message and isinstance(greeting_message, str):
        project_details["greeting_message"] = greeting_message
    else:
        # Provide a default if not critical
        project_details["greeting_message"] = "أهلاً بك!" # Default Arabic greeting
        print("Warning: Invalid or missing 'greeting_message'. Using default.")

    print(f"Parsed Project Details: {project_details}")
    return project_details

def build_android_project(project_details: dict, output_dir: Path):
    """
    Builds a basic Android project structure using provided details.

    Args:
        project_details (dict): Dictionary containing 'package_name', 'app_name',
                                'greeting_message'.
        output_dir (Path): The root directory where the Android project will be created.
    """
    package_name = project_details.get("package_name")
    app_name = project_details.get("app_name")
    greeting_message = project_details.get("greeting_message")

    if not all([package_name, app_name, greeting_message]):
        print("Error: Missing critical project details for building.")
        return

    # Create the main project directory and 'app' module
    project_root = output_dir / "android_app"
    app_module_path = project_root / "app"
    os.makedirs(app_module_path, exist_ok=True)

    print(f"\n--- Creating Android Project Structure at: {project_root} ---")
    create_android_project_structure(project_root, package_name, app_name, greeting_message)
    create_build_gradle_file(project_root, package_name)
    create_settings_gradle_file(project_root)
    create_gradle_wrapper(project_root)

    print("\n--- Android Project Structure Created ---")
    return project_root

def build_apk(project_root: Path) -> Path | None:
    """
    Builds the APK from the created Android project using Gradle.

    Args:
        project_root (Path): The root directory of the Android project.

    Returns:
        Path | None: The path to the generated APK file if successful, otherwise None.
    """
    print("\n--- Building APK using Gradle ---")
    apk_output_path = None
    try:
        # Ensure gradlew is executable
        gradlew_path = project_root / "gradlew"
        if not gradlew_path.exists():
            print("Error: gradlew script not found.")
            return None
        os.chmod(gradlew_path, 0o755)

        # Execute the Gradle build command
        # Using 'assembleRelease' for a release build, or 'assembleDebug' for debug
        process = subprocess.run(
            [str(gradlew_path), "assembleRelease", "-p", str(project_root)],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        print("Gradle build stdout:")
        print(process.stdout)
        print("Gradle build stderr:")
        print(process.stderr)

        # Find the generated APK
        # APKs are typically found in app/build/outputs/apk/release/
        potential_apk_dir = project_root / "app" / "build" / "outputs" / "apk" / "release"
        if potential_apk_dir.exists():
            apk_files = list(potential_apk_dir.glob("*.apk"))
            if apk_files:
                apk_output_path = apk_files[0]
                print(f"Successfully built APK: {apk_output_path}")
            else:
                print("Error: No APK file found in the expected output directory.")
        else:
            print("Error: APK output directory not found.")

    except FileNotFoundError:
        print("Error: 'gradlew' command not found. Is Java installed and Gradle available?")
    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("Gradle stdout:")
        print(e.stdout)
        print("Gradle stderr:")
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during APK build: {e}")

    print("\n--- APK Build Process Finished ---")
    return apk_output_path

# --- Main Lobe Function (Arabic APK Generation) ---

class ArabicAPKGeneratorLobe:
    """
    This Lobe focuses on parsing Arabic NLP output and initiating the Android APK build process.
    It bridges the gap between language understanding and code generation/compilation.
    """
    def __init__(self):
        self.last_thought = None
        self.generated_apk_path = None

    def process_nlp_output(self, nlp_result: dict) -> bool:
        """
        Processes the structured NLP output from the Arabic Lobe.

        Args:
            nlp_result (dict): The output from Lobe 0 (Arabic Lobe), expected to contain
                               'app_name', 'package_name', and 'greeting_message'.

        Returns:
            bool: True if processing and project creation were successful, False otherwise.
        """
        print("\n--- Initiating Arabic APK Generation Lobe ---")
        self.last_thought = f"Processing NLP output: {nlp_result}"

        project_details = parse_arabic_nlp_output(nlp_result)

        if not project_details:
            print("Failed to parse valid project details from NLP output.")
            self.last_thought = "Failed to parse project details."
            return False

        # Create a temporary directory for the Android project
        temp_project_dir = TEMP_DIR / project_details["package_name"].replace('.', '_')
        if temp_project_dir.exists():
            shutil.rmtree(temp_project_dir)
        temp_project_dir.mkdir(parents=True, exist_ok=True)

        generated_project_root = build_android_project(project_details, temp_project_dir)

        if generated_project_root:
            self.last_thought = f"Android project structure created at: {generated_project_root}"
            # Attempt to build the APK
            self.generated_apk_path = build_apk(generated_project_root)
            if self.generated_apk_path:
                print(f"APK generation successful: {self.generated_apk_path}")
                self.last_thought = f"APK generated successfully: {self.generated_apk_path}"
                return True
            else:
                print("APK generation failed.")
                self.last_thought = "APK generation failed after project build."
                return False
        else:
            print("Android project structure creation failed.")
            self.last_thought = "Android project structure creation failed."
            return False

    def get_last_thought(self):
        return self.last_thought

    def get_generated_apk_path(self):
        return self.generated_apk_path

# --- Example Usage ---
# This part would be triggered by a higher-level orchestrator or another Lobe.

def arabic_apk_generation_lobe_demo():
    """Demonstrates the functionality of the ArabicAPKGeneratorLobe."""
    print("\n--- Arabic APK Generation Lobe Demo ---")

    # Simulate output from Lobe 0 (Arabic NLP)
    # This would be the result of `c_text` or a similar function
    simulated_nlp_output = {
        "app_name": "تطبيقي العربي",
        "package_name": "com.example.myarabicapp",
        "greeting_message": "مرحباً بالعالم من العربية!"
    }

    arabic_apk_generator = ArabicAPKGeneratorLobe()
    success = arabic_apk_generator.process_nlp_output(simulated_nlp_output)

    if success:
        print(f"\nDemo successful. APK generated at: {arabic_apk_generator.get_generated_apk_path()}")
    else:
        print("\nDemo failed.")

    print(f"Last thought of Arabic APK Generator Lobe: {arabic_apk_generator.get_last_thought()}")

    # Clean up dummy files if they were created by the demo
    cleanup_dummy_files()

    print("\n--- Arabic APK Generation Lobe Demo Finished ---")

if __name__ == "__main__":
    # Ensure necessary tools are available (e.g., Java JDK for Gradle)
    # This check is simplified; a real system would have more robust checks.
    try:
        subprocess.run(["java", "-version"], check=True, capture_output=True)
        print("Java is installed and accessible.")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: Java Development Kit (JDK) is required for Gradle builds.")
        print("Please install a JDK and ensure 'java' is in your system's PATH.")
        sys.exit(1)

    # Ensure the Gradle wrapper can be downloaded (internet connection required)
    # This is implicitly tested when `build_apk` is called.

    arabic_apk_generation_lobe_demo()