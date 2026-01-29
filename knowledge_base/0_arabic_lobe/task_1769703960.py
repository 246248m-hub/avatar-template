import os
import shutil
import subprocess
from pathlib import Path
import sys

# Define constants
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
DUMMY_PROJECT_ROOT = Path("dummy_apk_project")
APP_NAME = "MyApp"
PACKAGE_NAME = "com.example.myapp"

# Ensure knowledge base directory exists
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

# --- Lobe 0: Language Lobe (simplified for this example) ---
# In a real scenario, this lobe would handle sophisticated language understanding,
# including Arabic natural language processing.

def process_natural_language_input(prompt: str) -> dict:
    """
    Simulates processing natural language input.
    In a real system, this would involve NLP models for understanding intent,
    extracting entities, and generating structured data.
    For this demo, we'll return a simplified dictionary.
    """
    print(f"Lobe 0 (Language Lobe): Processing prompt: '{prompt}'")
    # Simulate extracting key components for APK generation
    if "android" in prompt.lower() and "app" in prompt.lower():
        return {
            "platform": "android",
            "app_name": APP_NAME,
            "package_name": PACKAGE_NAME,
            "features": ["basic_ui", "arabic_support"] if "arabic" in prompt.lower() else ["basic_ui"]
        }
    return {"error": "Unrecognized input"}

# --- Lobe 1: Arabic NLP Lobe ---
# This lobe focuses specifically on Arabic text processing,
# enabling natural language interaction and generation in Arabic.

def generate_arabic_text_elements(app_config: dict) -> dict:
    """
    Generates Arabic text elements needed for an Android application.
    This would involve translating UI strings, generating culturally relevant
    content, and handling Arabic specific text rendering logic.
    """
    print("Lobe 1 (Arabic NLP Lobe): Generating Arabic text elements...")
    arabic_elements = {}
    if "arabic_support" in app_config.get("features", []):
        arabic_elements["app_name_arabic"] = f"{APP_NAME} (تطبيق)"
        arabic_elements["welcome_message_arabic"] = "أهلاً بك في تطبيقنا!"
        arabic_elements["greeting_arabic"] = "مرحباً"
        # In a real scenario, more complex Arabic text generation would occur here.
    return arabic_elements

def parse_arabic_instructions(instruction: str) -> dict:
    """
    Parses natural language instructions specifically in Arabic.
    This function would use Arabic NLP models to understand user commands.
    """
    print(f"Lobe 1 (Arabic NLP Lobe): Parsing Arabic instruction: '{instruction}'")
    # Simplified parsing for demo
    if "أنشئ تطبيق أندرويد" in instruction:
        return {"intent": "create_android_app", "language": "arabic"}
    return {"intent": "unknown"}

# --- Lobe 2: Project Structure Lobe ---
# This lobe is responsible for creating the fundamental directory and file
# structure for an Android application.

def create_android_project_structure(app_name: str, package_name: str) -> Path:
    """
    Creates the basic directory and file structure for an Android project.
    This includes the manifest, res, java directories, etc.
    """
    print(f"Lobe 2 (Project Structure Lobe): Creating Android project structure for '{app_name}'...")
    project_root = DUMMY_PROJECT_ROOT / app_name.lower().replace(" ", "_")
    project_root.mkdir(parents=True, exist_ok=True)

    # Create essential directories
    (project_root / "app").mkdir(exist_ok=True)
    (project_root / "app" / "src").mkdir(exist_ok=True)
    (project_root / "app" / "src" / "main").mkdir(exist_ok=True)
    (project_root / "app" / "src" / "main" / "java").mkdir(exist_ok=True)
    (project_root / "app" / "src" / "main" / "res").mkdir(exist_ok=True)
    (project_root / "app" / "src" / "main" / "res" / "layout").mkdir(exist_ok=True)
    (project_root / "app" / "src" / "main" / "res" / "values").mkdir(exist_ok=True)
    (project_root / "app" / "src" / "main" / "res" / "values-ar").mkdir(exist_ok=True) # Arabic values

    # Create dummy files
    (project_root / "build.gradle").touch()
    (project_root / "settings.gradle").touch()
    (project_root / "gradlew").touch()
    (project_root / "gradlew.bat").touch()
    (project_root / "app" / "build.gradle").touch()
    (project_root / "app" / "src" / "main" / "AndroidManifest.xml").touch()
    (project_root / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml").touch()
    (project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml").touch()
    (project_root / "app" / "src" / "main" / "res" / "values-ar" / "strings.xml").touch()

    # Create package directory
    package_dir_path = project_root / "app" / "src" / "main" / "java" / package_name.replace(".", os.sep)
    package_dir_path.mkdir(parents=True, exist_ok=True)
    (package_dir_path / "MainActivity.java").touch()

    print(f"Project structure created at: {project_root}")
    return project_root

# --- Lobe 3: Manifest Configuration Lobe ---
# This lobe handles the configuration of the AndroidManifest.xml file.

def configure_manifest(project_root: Path, package_name: str, app_name: str, arabic_elements: dict):
    """
    Configures the AndroidManifest.xml file with basic settings and Arabic support.
    """
    manifest_path = project_root / "app" / "src" / "main" / "AndroidManifest.xml"
    print(f"Lobe 3 (Manifest Configuration Lobe): Configuring manifest at {manifest_path}...")

    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name}">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print("AndroidManifest.xml configured.")

# --- Lobe 4: Code Generation Lobe ---
# This lobe generates Java/Kotlin code for the Android application.

def generate_activity_code(project_root: Path, package_name: str, app_name: str, arabic_elements: dict):
    """
    Generates the MainActivity.java file.
    Includes basic UI setup and a greeting.
    """
    activity_path = project_root / "app" / "src" / "main" / "java" / package_name.replace(".", os.sep) / "MainActivity.java"
    print(f"Lobe 4 (Code Generation Lobe): Generating activity code at {activity_path}...")

    java_code = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{app_name.lower().replace(" ", "_")}_activity); // Assumes layout file name

        TextView greetingTextView = findViewById(R.id.greetingTextView);
        // Check if Arabic elements are available and set appropriately
        if (getResources().getConfiguration().getLocales().get(0).getLanguage().equals("ar")) {{
            greetingTextView.setText("{arabic_elements.get('greeting_arabic', 'Hello!')}");
        }} else {{
            greetingTextView.setText("Hello!");
        }}
    }}
}}
"""
    with open(activity_path, "w", encoding="utf-8") as f:
        f.write(java_code)
    print("MainActivity.java generated.")

# --- Lobe 5: Resource Generation Lobe ---
# This lobe generates XML resources like layouts and string values.

def generate_resources(project_root: Path, app_name: str, arabic_elements: dict):
    """
    Generates layout XML and strings.xml for the application, including Arabic strings.
    """
    print("Lobe 5 (Resource Generation Lobe): Generating resources...")

    # Layout file
    layout_path = project_root / "app" / "src" / "main" / "res" / "layout" / f"{app_name.lower().replace(' ', '_')}_activity.xml"
    layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name}Activity">

    <TextView
        android:id="@+id/greetingTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout_content)
    print(f"Layout '{layout_path.name}' generated.")

    # Strings.xml (default)
    strings_default_path = project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml"
    strings_default_content = f"""<resources>
    <string name="app_name">{app_name}</string>
    <string name="welcome_message">Welcome to our app!</string>
</resources>
"""
    with open(strings_default_path, "w", encoding="utf-8") as f:
        f.write(strings_default_content)
    print(f"Strings.xml (default) generated.")

    # Strings.xml (Arabic)
    strings_arabic_path = project_root / "app" / "src" / "main" / "res" / "values-ar" / "strings.xml"
    strings_arabic_content = f"""<resources>
    <string name="app_name">{arabic_elements.get('app_name_arabic', app_name)}</string>
    <string name="welcome_message">{arabic_elements.get('welcome_message_arabic', 'Welcome to our app!')}</string>
</resources>
"""
    with open(strings_arabic_path, "w", encoding="utf-8") as f:
        f.write(strings_arabic_content)
    print(f"Strings.xml (Arabic) generated.")

# --- Lobe 6: Synthesis Lobe ---
# This lobe orchestrates the integration of different components.

def integrate_arabic_elements(app_config: dict, arabic_elements: dict, project_root: Path):
    """
    Integrates generated Arabic elements into the project structure.
    This would involve updating resource files and potentially code.
    """
    print("Lobe 6 (Synthesis Lobe): Integrating Arabic elements...")

    # Update strings.xml (Arabic) if it exists
    strings_arabic_path = project_root / "app" / "src" / "main" / "res" / "values-ar" / "strings.xml"
    if strings_arabic_path.exists():
        # Re-writing with potentially updated strings
        strings_arabic_content = f"""<resources>
    <string name="app_name">{arabic_elements.get('app_name_arabic', APP_NAME)}</string>
    <string name="welcome_message">{arabic_elements.get('welcome_message_arabic', 'Welcome to our app!')}</string>
</resources>
"""
        with open(strings_arabic_path, "w", encoding="utf-8") as f:
            f.write(strings_arabic_content)
        print("Updated Arabic strings.xml.")
    else:
        print("Arabic strings.xml not found, skipping integration.")

    # Update MainActivity to use Arabic greeting if the device language is Arabic
    # This is already handled within the generate_activity_code function for simplicity.
    # A more complex integration might involve dynamically modifying Java/Kotlin code.
    print("Arabic elements integration complete (handled in resource and code generation).")

# --- Lobe 7: Build Configuration Lobe ---
# This lobe configures the Gradle build files.

def configure_build_files(project_root: Path, app_name: str):
    """
    Configures the main build.gradle and app/build.gradle files.
    This is a simplified version.
    """
    print("Lobe 7 (Build Configuration Lobe): Configuring build files...")

    # settings.gradle
    settings_gradle_path = project_root / "settings.gradle"
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
rootProject.name = "{app_name.lower().replace(' ', '_')}"
include ':app'
"""
    with open(settings_gradle_path, "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)
    print("settings.gradle configured.")

    # build.gradle (project level)
    build_gradle_path = project_root / "build.gradle"
    build_gradle_content = f"""// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {{
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.0' apply false
}}
"""
    with open(build_gradle_path, "w", encoding="utf-8") as f:
        f.write(build_gradle_content)
    print("build.gradle (project level) configured.")

    # app/build.gradle
    app_build_gradle_path = project_root / "app" / "build.gradle"
    app_build_gradle_content = f"""plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{PACKAGE_NAME}'
    compileSdk 33

    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
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
    // For Kotlin projects
    // kotlinOptions {{
    //     jvmTarget = '1.8'
    // }}
}}

dependencies {{

    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
    with open(app_build_gradle_path, "w", encoding="utf-8") as f:
        f.write(app_build_gradle_content)
    print("app/build.gradle configured.")

    # gradlew scripts
    gradlew_content = "#!/bin/sh\n" + (project_root / "gradlew").read_text().split('\n', 1)[1] if (project_root / "gradlew").exists() else ""
    with open(project_root / "gradlew", "w") as f:
        f.write(gradlew_content)
    os.chmod(project_root / "gradlew", 0o755)
    print("gradlew script configured.")

    gradlew_bat_content = (project_root / "gradlew.bat").read_text() if (project_root / "gradlew.bat").exists() else ""
    with open(project_root / "gradlew.bat", "w") as f:
        f.write(gradlew_bat_content)
    print("gradlew.bat script configured.")

# --- Lobe 8: APK Compiler Lobe ---
# This lobe orchestrates the build process to generate an APK.

def build_apk(project_root: Path):
    """
    Executes the Gradle build command to assemble the APK.
    """
    print(f"Lobe 8 (APK Compiler Lobe): Attempting to build APK for project at {project_root}...")
    if not (project_root / "gradlew").exists():
        print("Error: gradlew script not found. Cannot build APK.")
        return False

    try:
        # Change directory to the project root to execute gradlew
        original_dir = os.getcwd()
        os.chdir(project_root)

        # Execute the assembleDebug task
        # Use subprocess.run for better control and error handling
        print("Running './gradlew assembleDebug'...")
        result = subprocess.run(["./gradlew", "assembleDebug"], capture_output=True, text=True, check=True)
        print("Gradle build output:")
        print(result.stdout)
        if result.stderr:
            print("Gradle build errors (if any):")
            print(result.stderr)

        print("APK build process completed successfully.")
        # Find the APK file (typically in app/build/outputs/apk/debug/)
        apk_path = project_root / "app" / "build" / "outputs" / "apk" / "debug" / f"app-debug.apk"
        if apk_path.exists():
            print(f"APK generated successfully at: {apk_path}")
            return True
        else:
            print(f"Error: APK file not found at expected location: {apk_path}")
            return False

    except FileNotFoundError:
        print("Error: gradlew command not found. Make sure it's executable and in the PATH or project directory.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error during APK build process: {e}")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return code: {e.returncode}")
        print(f"Stdout:\n{e.stdout}")
        print(f"Stderr:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during APK build: {e}")
        return False
    finally:
        # Always change back to the original directory
        os.chdir(original_dir)

# --- Main Orchestration Function ---

def generate_hyper_efficient_apk(natural_language_prompt: str):
    """
    The main function to orchestrate the APK generation process from natural language.
    """
    print(f"\n--- Starting APK Generation for prompt: '{natural_language_prompt}' ---")

    # Lobe 0: Process natural language input
    app_config = process_natural_language_input(natural_language_prompt)
    if "error" in app_config:
        print(f"Error: {app_config['error']}")
        return

    app_name = app_config.get("app_name", APP_NAME)
    package_name = app_config.get("package_name", PACKAGE_NAME)
    has_arabic_support = "arabic_support" in app_config.get("features", [])

    # Lobe 1: Arabic NLP Lobe
    arabic_elements = {}
    if has_arabic_support:
        arabic_elements = generate_arabic_text_elements(app_config)
        print(f"Generated Arabic elements: {arabic_elements}")

    # Lobe 2: Project Structure Lobe
    project_root = None
    try:
        project_root = create_android_project_structure(app_name, package_name)

        # Lobe 3: Manifest Configuration Lobe
        configure_manifest(project_root, package_name, app_name, arabic_elements)

        # Lobe 5: Resource Generation Lobe (called before code generation to ensure resources exist)
        generate_resources(project_root, app_name, arabic_elements)

        # Lobe 4: Code Generation Lobe
        generate_activity_code(project_root, package_name, app_name, arabic_elements)

        # Lobe 7: Build Configuration Lobe
        configure_build_files(project_root, app_name)

        # Lobe 6: Synthesis Lobe (integrating Arabic elements)
        if has_arabic_support:
            integrate_arabic_elements(app_config, arabic_elements, project_root)

        # Lobe 8: APK Compiler Lobe
        apk_generated = build_apk(project_root)

        if apk_generated:
            print("\n--- APK Generation Process Completed Successfully ---")
        else:
            print("\n--- APK Generation Process Failed ---")

    except Exception as e:
        print(f"\nAn error occurred during the APK generation process: {e}")
    finally:
        # Clean up the dummy project directory if it exists and the APK was not generated or on error
        if project_root and project_root.exists():
            if not apk_generated: # Only remove if build failed or wasn't attempted fully
                print(f"Cleaning up dummy project directory: {project_root}")
                try:
                    shutil.rmtree(project_root)
                except OSError as e:
                    print(f"Error removing directory {project_root}: {e}")
            else:
                print(f"Keeping generated project at: {project_root} for inspection.")


if __name__ == "__main__":
    # Example usage:
    # Make sure you have Android SDK and Gradle installed and configured in your system's PATH
    # You might need to run this script in an environment where Android SDK tools are accessible.

    # Test case 1: Basic Android app
    # generate_hyper_efficient_apk("Create a simple Android application named 'My Test App'.")

    # Test case 2: Android app with Arabic support
    # generate_hyper_efficient_apk("Build an Android app with Arabic language support. Call it 'Arabic Assistant'.")

    # Test case 3: Arabic instruction
    # generate_hyper_efficient_apk("أنشئ تطبيق أندرويد بسيط اسمه 'تطبيق تجريبي'.")

    # For demonstration, let's run a simulated prompt that includes Arabic intent
    # In a real scenario, Lobe 0 would handle this direct Arabic input.
    # For this demo, we simulate the outcome of Lobe 0 recognizing Arabic intent.

    print("\n--- Simulating Arabic Instruction Processing ---")
    arabic_instruction = "أنشئ تطبيق أندرويد باللغة العربية اسمه 'تطبيقي العربي'."
    print(f"Simulated Arabic Input: '{arabic_instruction}'")

    # Simulate Lobe 0 processing Arabic input directly for this demo
    print("Lobe 0 (Language Lobe): Simulating direct Arabic input processing...")
    simulated_app_config = {
        "platform": "android",
        "app_name": "تطبيقي العربي", # Extracted from Arabic instruction
        "package_name": "com.example.tatbiqarabi", # Derived
        "features": ["basic_ui", "arabic_support"]
    }
    print(f"Simulated app_config from Arabic: {simulated_app_config}")

    # Now, proceed with the generation using the simulated config
    app_name = simulated_app_config.get("app_name", APP_NAME)
    package_name = simulated_app_config.get("package_name", PACKAGE_NAME)
    has_arabic_support = "arabic_support" in simulated_app_config.get("features", [])

    project_root = None
    apk_generated = False
    try:
        project_root = create_android_project_structure(app_name, package_name)

        # Lobe 1: Arabic NLP Lobe
        arabic_elements = {}
        if has_arabic_support:
            arabic_elements = generate_arabic_text_elements(simulated_app_config)
            print(f"Generated Arabic elements: {arabic_elements}")

        # Lobe 3: Manifest Configuration Lobe
        configure_manifest(project_root, package_name, app_name, arabic_elements)

        # Lobe 5: Resource Generation Lobe
        generate_resources(project_root, app_name, arabic_elements)

        # Lobe 4: Code Generation Lobe
        generate_activity_code(project_root, package_name, app_name, arabic_elements)

        # Lobe 7: Build Configuration Lobe
        configure_build_files(project_root, app_name)

        # Lobe 6: Synthesis Lobe
        if has_arabic_support:
            integrate_arabic_elements(simulated_app_config, arabic_elements, project_root)

        # Lobe 8: APK Compiler Lobe
        apk_generated = build_apk(project_root)

        if apk_generated:
            print("\n--- Hyper-Efficient APK Generation from Arabic Prompt Completed Successfully ---")
        else:
            print("\n--- Hyper-Efficient APK Generation from Arabic Prompt Failed ---")

    except Exception as e:
        print(f"\nAn error occurred during the Hyper-Efficient APK generation process from Arabic prompt: {e}")
    finally:
        if project_root and project_root.exists():
            if not apk_generated:
                print(f"Cleaning up dummy project directory: {project_root}")
                try:
                    shutil.rmtree(project_root)
                except OSError as e:
                    print(f"Error removing directory {project_root}: {e}")
            else:
                print(f"Generated project for Arabic prompt kept at: {project_root}")

    print("\n--- All Demos Finished ---")