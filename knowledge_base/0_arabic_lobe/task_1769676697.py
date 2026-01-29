import os
import shutil
import subprocess

# --- Configuration ---
# A temporary directory to hold generated project files.
DUMMY_PROJECT_ROOT = "./dummy_apk_project"
# The path to the Android SDK's build-tools directory.
# You might need to adjust this to your actual Android SDK installation path.
ANDROID_BUILD_TOOLS_PATH = os.path.expanduser("~/Android/Sdk/build-tools")

# --- Helper Functions ---

def find_latest_build_tools_version():
    """
    Finds the latest installed Android build-tools version.
    """
    if not os.path.exists(ANDROID_BUILD_TOOLS_PATH):
        raise FileNotFoundError(f"Android build-tools not found at: {ANDROID_BUILD_TOOLS_PATH}")

    versions = []
    for entry in os.listdir(ANDROID_BUILD_TOOLS_PATH):
        if os.path.isdir(os.path.join(ANDROID_BUILD_TOOLS_PATH, entry)) and entry.replace('.', '', 1).isdigit():
            versions.append(entry)

    if not versions:
        raise FileNotFoundError("No Android build-tools versions found.")

    # Sort versions numerically (e.g., '30.0.3' before '33.0.0')
    versions.sort(key=lambda v: [int(i) for i in v.split('.')])
    return versions[-1]

def ensure_project_directory(project_root):
    """
    Ensures the project root directory exists, creating it if necessary.
    Cleans up any existing dummy project before creation.
    """
    if os.path.exists(project_root):
        print(f"Cleaning up existing dummy project directory: {project_root}")
        shutil.rmtree(project_root)
    os.makedirs(project_root)
    print(f"Created dummy project directory: {project_root}")

def create_dummy_manifest(project_root, package_name="com.example.myapp"):
    """
    Creates a basic AndroidManifest.xml file.
    """
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity"
                  android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_dir = os.path.join(project_root, "app", "src", "main")
    os.makedirs(manifest_dir, exist_ok=True)
    manifest_path = os.path.join(manifest_dir, "AndroidManifest.xml")
    with open(manifest_path, "w") as f:
        f.write(manifest_content)
    print(f"Created AndroidManifest.xml at: {manifest_path}")

def create_dummy_java_activity(project_root, package_name="com.example.myapp"):
    """
    Creates a basic MainActivity.java file.
    """
    activity_dir = os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.'))
    os.makedirs(activity_dir, exist_ok=True)
    activity_path = os.path.join(activity_dir, "MainActivity.java")
    activity_content = """
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
"""
    with open(activity_path, "w") as f:
        f.write(activity_content)
    print(f"Created MainActivity.java at: {activity_path}")

def create_dummy_layout(project_root):
    """
    Creates a basic activity_main.xml layout file.
    """
    layout_dir = os.path.join(project_root, "app", "src", "main", "res", "layout")
    os.makedirs(layout_dir, exist_ok=True)
    layout_path = os.path.join(layout_dir, "activity_main.xml")
    layout_content = """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(layout_path, "w") as f:
        f.write(layout_content)
    print(f"Created activity_main.xml at: {layout_path}")

def create_dummy_gradle_files(project_root):
    """
    Creates dummy build.gradle files for an Android project.
    """
    # Project-level build.gradle
    project_build_gradle_path = os.path.join(project_root, "build.gradle")
    project_build_gradle_content = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.0.0' // Example version
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
"""
    with open(project_build_gradle_path, "w") as f:
        f.write(project_build_gradle_content)
    print(f"Created project build.gradle at: {project_build_gradle_path}")

    # App-level build.gradle
    app_build_gradle_path = os.path.join(project_root, "app", "build.gradle")
    os.makedirs(os.path.dirname(app_build_gradle_path), exist_ok=True)
    app_build_gradle_content = """
plugins {
    id 'com.android.application'
}

android {
    namespace 'com.example.myapp'
    compileSdk 33
    buildToolsVersion "33.0.0" // Placeholder, will be updated

    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
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
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1' // Example dependency
    implementation 'com.google.android.material:material:1.10.0' // Example dependency
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4' // Example dependency
}
"""
    with open(app_build_gradle_path, "w") as f:
        f.write(app_build_gradle_content)
    print(f"Created app build.gradle at: {app_build_gradle_path}")

    # settings.gradle
    settings_gradle_path = os.path.join(project_root, "settings.gradle")
    settings_gradle_content = """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "MyApp"
include ':app'
"""
    with open(settings_gradle_path, "w") as f:
        f.write(settings_gradle_content)
    print(f"Created settings.gradle at: {settings_gradle_path}")


# --- Core Functionality ---

class ArabicAPKCompiler:
    def __init__(self, android_sdk_path=None):
        """
        Initializes the ArabicAPKCompiler.

        Args:
            android_sdk_path (str, optional): Path to the Android SDK. If None, it tries to find it.
        """
        self.android_sdk_path = android_sdk_path or os.path.expanduser("~/Android/Sdk")
        if not os.path.exists(self.android_sdk_path):
            raise FileNotFoundError(f"Android SDK not found at {self.android_sdk_path}. Please set android_sdk_path.")
        self.build_tools_version = find_latest_build_tools_version()
        self.apk_compiler_lobe_directory = DUMMY_PROJECT_ROOT
        self.package_name = "com.example.arabicapp" # Default package name

    def _update_app_build_gradle(self):
        """
        Updates the buildToolsVersion in the app's build.gradle file.
        """
        app_build_gradle_path = os.path.join(self.apk_compiler_lobe_directory, "app", "build.gradle")
        if not os.path.exists(app_build_gradle_path):
            print(f"Warning: {app_build_gradle_path} not found. Skipping buildToolsVersion update.")
            return

        with open(app_build_gradle_path, 'r') as f:
            lines = f.readlines()

        updated_lines = []
        for line in lines:
            if "buildToolsVersion" in line:
                updated_lines.append(f'    buildToolsVersion "{self.build_tools_version}"\n')
                print(f"Updated buildToolsVersion to: {self.build_tools_version}")
            else:
                updated_lines.append(line)

        with open(app_build_gradle_path, 'w') as f:
            f.writelines(updated_lines)

    def generate_apk_structure(self, arabic_code_snippet: str):
        """
        Generates the basic Android project structure for an APK compilation.
        This function is a placeholder for actual Arabic code generation and
        integration into an Android project.

        Args:
            arabic_code_snippet (str): A string representing Arabic code or instructions.
                                       In a real scenario, this would be parsed and
                                       translated into Android Java/Kotlin code and resources.
        """
        print("\n--- Generating APK Structure from Arabic Snippet ---")
        ensure_project_directory(self.apk_compiler_lobe_directory)
        create_dummy_manifest(self.apk_compiler_lobe_directory, self.package_name)
        create_dummy_java_activity(self.apk_compiler_lobe_directory, self.package_name)
        create_dummy_layout(self.apk_compiler_lobe_directory)
        create_dummy_gradle_files(self.apk_compiler_lobe_directory)
        self._update_app_build_gradle()

        # Placeholder for actual Arabic code integration:
        # In a more advanced version, 'arabic_code_snippet' would be parsed.
        # Relevant parts would be translated into Java/Kotlin code, XML layouts,
        # and potentially resource files. This generated code would then replace
        # or augment the dummy files created above.
        print(f"Placeholder: Parsed Arabic snippet: '{arabic_code_snippet}'")
        print("Basic Android project structure created. Ready for compilation.")

    def compile_apk(self):
        """
        Compiles the generated Android project into an APK using Gradle.
        """
        print("\n--- Compiling APK ---")
        if not os.path.exists(os.path.join(self.apk_compiler_lobe_directory, "gradlew")):
            # If gradlew doesn't exist, try to create it or assume it's handled elsewhere
            # For simplicity, we'll assume it's present or the user will handle it.
            print("Warning: gradlew script not found. Assuming it's available or will be created.")

        # Navigate to the project directory
        original_dir = os.getcwd()
        os.chdir(self.apk_compiler_lobe_directory)

        try:
            # Execute the Gradle wrapper to build the APK
            # Use 'assembleDebug' for a debug APK or 'assembleRelease' for a release APK
            gradlew_command = ["./gradlew", "assembleDebug"]
            print(f"Executing Gradle command: {' '.join(gradlew_command)}")
            result = subprocess.run(gradlew_command, capture_output=True, text=True, check=True)

            print("Gradle build output:")
            print(result.stdout)

            # Find the generated APK
            apk_path = None
            for root, _, files in os.walk("app/build/outputs/apk/debug"):
                for file in files:
                    if file.endswith(".apk"):
                        apk_path = os.path.join(root, file)
                        break
                if apk_path:
                    break

            if apk_path:
                print(f"\nSuccessfully generated APK: {os.path.abspath(apk_path)}")
                return os.path.abspath(apk_path)
            else:
                print("\nError: APK file not found in build output.")
                return None

        except subprocess.CalledProcessError as e:
            print(f"\nGradle build failed with error code {e.returncode}:")
            print("--- STDOUT ---")
            print(e.stdout)
            print("--- STDERR ---")
            print(e.stderr)
            return None
        except FileNotFoundError:
            print("\nError: 'gradlew' command not found. Please ensure you have the Android SDK and Gradle installed and in your PATH, or that 'gradlew' is present in the project directory.")
            return None
        finally:
            # Return to the original directory
            os.chdir(original_dir)

    def cleanup(self):
        """
        Cleans up the dummy project directory.
        """
        print("\n--- Cleaning up APK compiler lobe ---")
        if os.path.exists(self.apk_compiler_lobe_directory):
            print(f"Removing dummy project directory: {self.apk_compiler_lobe_directory}")
            shutil.rmtree(self.apk_compiler_lobe_directory)
        print("Cleanup complete.")


# --- Demo Usage ---
if __name__ == "__main__":
    try:
        # Initialize the compiler (adjust SDK path if necessary)
        compiler = ArabicAPKCompiler()

        # Example Arabic code snippet (placeholder for actual NLP parsing)
        arabic_instructions = "أنشئ تطبيقًا بسيطًا يعرض رسالة ترحيب باللغة العربية."

        # 1. Generate the project structure
        compiler.generate_apk_structure(arabic_instructions)

        # 2. Compile the APK
        # This step requires a properly set up Android SDK and build tools.
        # It might take a significant amount of time.
        # For demonstration, we'll comment it out if not explicitly desired.
        # generated_apk_path = compiler.compile_apk()
        # if generated_apk_path:
        #     print(f"APK generated at: {generated_apk_path}")

        print("\n--- Arabic APK Compiler Lobe Demo Finished (APK compilation step commented out for faster execution) ---")
        compiler.cleanup()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the Android SDK is installed and the ANDROID_SDK_PATH is correctly configured.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Ensure cleanup happens even if compilation fails
        if 'compiler' in locals() and compiler:
            compiler.cleanup()