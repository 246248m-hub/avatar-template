import os
import shutil
import subprocess
import sys
import json

# Assume these are defined elsewhere and accessible
# from constants import (
#     ANDROID_SDK_ROOT,
#     GRADLE_PROPERTIES_TEMPLATE,
#     BUILD_GRADLE_APP_TEMPLATE,
#     ANDROID_MANIFEST_TEMPLATE,
#     ACTIVITY_JAVA_TEMPLATE,
#     JAVA_PACKAGE_DIR,
#     APP_BUILD_GRADLE_TEMPLATE,
# )
# from utils import create_directory_structure, run_command, get_java_package_path
# from Lobe_8_apk_compiler_lobe import compile_apk

# --- Constants (for demonstration purposes, these would be imported) ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    # Fallback or raise an error if ANDROID_SDK_ROOT is not set
    # For local testing, you might hardcode a path if needed
    # ANDROID_SDK_ROOT = "/path/to/your/android/sdk"
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

GRADLE_PROPERTIES_TEMPLATE = """
org.gradle.jvmargs=-Xmx2048m
"""

BUILD_GRADLE_APP_TEMPLATE = """
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
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
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
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

ANDROID_MANIFEST_TEMPLATE = """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppName"
        tools:targetApi="31">
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

ACTIVITY_JAVA_TEMPLATE = """
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists
        // Your generated logic can go here
    }}
}}
"""

APP_BUILD_GRADLE_TEMPLATE = """
plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
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
}}

dependencies {{
    // Add your dependencies here
}}
"""

# --- Utility Functions (for demonstration purposes, these would be imported) ---
def create_directory_structure(base_path, package_name):
    """Creates the necessary directory structure for an Android project."""
    package_path = get_java_package_path(package_name)
    os.makedirs(os.path.join(base_path, "app", "src", "main", "java", *package_path.split('.')), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "main", "res", "values"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "androidTest", "java", *package_path.split('.')), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "test", "java", *package_path.split('.')), exist_ok=True)
    os.makedirs(os.path.join(base_path, "gradle", "wrapper"), exist_ok=True)
    # Create dummy files that are often expected
    with open(os.path.join(base_path, "settings.gradle"), "w") as f:
        f.write("rootProject.name = \"MyApp\"\n")
        f.write("include ':app'\n")
    with open(os.path.join(base_path, "gradlew"), "w") as f: # Placeholder gradlew
        f.write("#!/bin/bash\n")
    os.chmod(os.path.join(base_path, "gradlew"), 0o755)
    with open(os.path.join(base_path, "gradlew.bat"), "w") as f: # Placeholder gradlew.bat
        f.write("@echo off\n")
    with open(os.path.join(base_path, "gradle", "wrapper", "gradle-wrapper.jar"), "w") as f:
        pass
    with open(os.path.join(base_path, "gradle", "wrapper", "gradle-wrapper.properties"), "w") as f:
        f.write("distributionBase=GRADLE_USER_HOME\n")
        f.write("distributionPath=wrapper/dists\n")
        f.write("distributionUrl=https\\://services.gradle.org/distributions/gradle-7.6-bin.zip\n")
        f.write("zipStoreBase=GRADLE_USER_HOME\n")
        f.write("zipStorePath=wrapper/dists\n")

def get_java_package_path(package_name):
    """Converts a Java package name to a directory path."""
    return package_name.replace('.', os.sep)

def run_command(command, cwd=None, env=None):
    """Runs a shell command and returns its output."""
    print(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        print("Command stdout:\n", result.stdout)
        if result.stderr:
            print("Command stderr:\n", result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        print("Stdout:\n", e.stdout)
        print("Stderr:\n", e.stderr)
        raise

def compile_apk(project_root):
    """Compiles the Android project into an APK using Gradle."""
    gradle_wrapper_path = os.path.join(project_root, "gradlew")
    if sys.platform == "win32":
        gradle_wrapper_path = os.path.join(project_root, "gradlew.bat")

    # Check if gradlew exists and is executable
    if not os.path.exists(gradle_wrapper_path):
        raise FileNotFoundError(f"Gradle wrapper not found at {gradle_wrapper_path}")
    if sys.platform != "win32":
        os.chmod(gradle_wrapper_path, 0o755)

    # Set ANDROID_SDK_ROOT in the environment for the Gradle command
    gradle_env = os.environ.copy()
    gradle_env["ANDROID_SDK_ROOT"] = ANDROID_SDK_ROOT

    # Run the assembleDebug task
    command = [gradle_wrapper_path, "assembleDebug"]
    run_command(command, cwd=project_root, env=gradle_env)

    # The APK will be located in app/build/outputs/apk/debug/
    apk_path = os.path.join(project_root, "app", "build", "outputs", "debug", "app-debug.apk")
    if not os.path.exists(apk_path):
        # Try the alternative location if the first one doesn't exist
        apk_path_alt = os.path.join(project_root, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
        if os.path.exists(apk_path_alt):
            apk_path = apk_path_alt
        else:
            raise FileNotFoundError(f"APK not found after build. Searched in: {os.path.join(project_root, 'app', 'build', 'outputs')}")
    return apk_path

# --- Lobe 7_android_project_builder_lobe ---
class AndroidProjectBuilder:
    """
    Responsible for constructing a basic Android project structure and files
    necessary for APK generation.
    """

    def __init__(self, project_root_dir="temp_android_project"):
        self.project_root = os.path.abspath(project_root_dir)
        self.package_name = "com.example.generatedapp" # Default, can be overridden

    def set_package_name(self, package_name):
        """Sets the package name for the Android application."""
        if not package_name or not isinstance(package_name, str):
            raise ValueError("Invalid package name provided.")
        # Basic validation for package name format
        if not all(c.isalnum() or c == '.' for c in package_name):
            raise ValueError(f"Package name '{package_name}' contains invalid characters.")
        self.package_name = package_name
        print(f"Package name set to: {self.package_name}")

    def create_project_structure(self):
        """Creates the essential directory and file structure for the Android project."""
        print(f"Creating Android project structure at: {self.project_root}")
        if os.path.exists(self.project_root):
            print(f"Project root '{self.project_root}' already exists. Removing and recreating.")
            shutil.rmtree(self.project_root)
        os.makedirs(self.project_root, exist_ok=True)
        create_directory_structure(self.project_root, self.package_name)
        print("Android project structure created.")

    def create_gradle_files(self):
        """Creates the necessary Gradle build files."""
        print("Creating Gradle build files...")
        # Create settings.gradle (basic)
        with open(os.path.join(self.project_root, "settings.gradle"), "w") as f:
            f.write(f"rootProject.name = \"GeneratedApp\"\n")
            f.write("include ':app'\n")

        # Create app/build.gradle
        app_build_gradle_path = os.path.join(self.project_root, "app", "build.gradle")
        with open(app_build_gradle_path, "w") as f:
            f.write(APP_BUILD_GRADLE_TEMPLATE.format(package_name=self.package_name))
        print("Created app/build.gradle")

        # Create gradle.properties
        gradle_properties_path = os.path.join(self.project_root, "gradle.properties")
        with open(gradle_properties_path, "w") as f:
            f.write(GRADLE_PROPERTIES_TEMPLATE)
        print("Created gradle.properties")

        # Create gradlew and gradlew.bat (placeholders)
        with open(os.path.join(self.project_root, "gradlew"), "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"exec \"{os.path.join(self.project_root, 'gradlew.bat')}\" $@\n") # For Windows compatibility
        os.chmod(os.path.join(self.project_root, "gradlew"), 0o755)

        with open(os.path.join(self.project_root, "gradlew.bat"), "w") as f:
            f.write("@echo off\n")
            f.write(f"if not exist \"%GRADLE_USER_HOME%\\wrapper\\dists\\gradle-7.6-bin\\gradle-7.6\\bin\\gradle.bat\" ( call :downloadTask ) \n")
            f.write(f"call \"%GRADLE_USER_HOME%\\wrapper\\dists\\gradle-7.6-bin\\gradle-7.6\\bin\\gradle.bat\" %*\n")
            f.write("goto :eof\n")
            f.write(":downloadTask\n")
            f.write("echo Downloading Gradle...\n")
            f.write(f"call \"{os.path.join(self.project_root, 'gradlew')}\" wrapper --gradle-version 7.6\n")
            f.write("goto :eof\n")


        # Create gradle/wrapper/gradle-wrapper.properties
        os.makedirs(os.path.join(self.project_root, "gradle", "wrapper"), exist_ok=True)
        with open(os.path.join(self.project_root, "gradle", "wrapper", "gradle-wrapper.properties"), "w") as f:
            f.write("distributionBase=GRADLE_USER_HOME\n")
            f.write("distributionPath=wrapper/dists\n")
            f.write("distributionUrl=https\\://services.gradle.org/distributions/gradle-7.6-bin.zip\n")
            f.write("zipStoreBase=GRADLE_USER_HOME\n")
            f.write("zipStorePath=wrapper/dists\n")
        print("Created Gradle wrapper files.")

    def create_manifest_file(self):
        """Creates the AndroidManifest.xml file."""
        print("Creating AndroidManifest.xml...")
        manifest_path = os.path.join(self.project_root, "app", "src", "main", "AndroidManifest.xml")
        with open(manifest_path, "w") as f:
            f.write(ANDROID_MANIFEST_TEMPLATE)
        print("AndroidManifest.xml created.")

        # Create dummy xml resource files as placeholders
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "res", "xml"), exist_ok=True)
        with open(os.path.join(self.project_root, "app", "src", "main", "res", "xml", "backup_rules.xml"), "w") as f:
            f.write("<full-backup-content/>\n")
        with open(os.path.join(self.project_root, "app", "src", "main", "res", "xml", "data_extraction_rules.xml"), "w") as f:
            f.write("<data-extraction-rules>\n    <cloud-backup />\n</data-extraction-rules>\n")

    def create_activity_file(self, activity_content=""):
        """Creates the main Activity Java file."""
        print("Creating MainActivity.java...")
        package_path = get_java_package_path(self.package_name)
        activity_dir = os.path.join(self.project_root, "app", "src", "main", "java", *package_path.split('.'))
        activity_path = os.path.join(activity_dir, "MainActivity.java")

        final_activity_content = ACTIVITY_JAVA_TEMPLATE.format(package_name=self.package_name)
        if activity_content:
            # Inject custom content into the onCreate method
            # This is a simplified approach; more sophisticated injection might be needed
            onCreate_start_index = final_activity_content.find("super.onCreate(savedInstanceState);")
            if onCreate_start_index != -1:
                insert_point = onCreate_start_index + len("super.onCreate(savedInstanceState);")
                final_activity_content = final_activity_content[:insert_point] + f"\n        // --- Generated Logic Start ---\n        {activity_content}\n        // --- Generated Logic End ---\n" + final_activity_content[insert_point:]
            else:
                # Fallback if super.onCreate is not found in template
                final_activity_content = final_activity_content.replace("setContentView(R.layout.activity_main);",
                                                                        f"setContentView(R.layout.activity_main);\n        {activity_content}")

        with open(activity_path, "w") as f:
            f.write(final_activity_content)
        print("MainActivity.java created.")

        # Create dummy activity_main.xml
        with open(os.path.join(self.project_root, "app", "src", "main", "res", "layout", "activity_main.xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity">\n    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Hello World!" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintLeft_toLeftOf="parent" app:layout_constraintRight_toRightOf="parent" app:layout_constraintTop_toTopOf="parent" />\n</androidx.constraintlayout.widget.ConstraintLayout>\n')

    def create_app_build_gradle(self):
        """Creates the app-level build.gradle file with minimal configuration."""
        print("Creating app/build.gradle...")
        app_build_gradle_path = os.path.join(self.project_root, "app", "build.gradle")
        with open(app_build_gradle_path, "w") as f:
            f.write(BUILD_GRADLE_APP_TEMPLATE.format(package_name=self.package_name))
        print("app/build.gradle created.")

    def build_project(self, generated_code_snippet=""):
        """Orchestrates the creation of the entire Android project."""
        print("\n--- Initiating Android Project Build ---")
        self.create_project_structure()
        self.create_gradle_files()
        self.create_manifest_file()
        self.create_activity_file(activity_content=generated_code_snippet)
        self.create_app_build_gradle()
        print("--- Android Project Build Complete ---")

    def compile(self):
        """Compiles the constructed Android project into an APK."""
        print("\n--- Initiating APK Compilation ---")
        try:
            apk_path = compile_apk(self.project_root)
            print(f"APK successfully compiled: {apk_path}")
            return apk_path
        except Exception as e:
            print(f"Error during APK compilation: {e}")
            raise
        finally:
            print("--- APK Compilation Process Finished ---")

    def cleanup(self):
        """Removes the generated project directory."""
        print(f"\n--- Cleaning up project directory: {self.project_root} ---")
        if os.path.exists(self.project_root):
            try:
                shutil.rmtree(self.project_root)
                print("Project directory removed successfully.")
            except OSError as e:
                print(f"Error removing directory {self.project_root}: {e.strerror}")
        else:
            print("Project directory does not exist, no cleanup needed.")

# --- Example Usage and Integration Point ---
if __name__ == '__main__':
    # This section demonstrates how Lobe 7 would be used.
    # In the grand objective, this would be triggered by Lobe 6 (Synthesis).

    print("--- Lobe 7: AndroidProjectBuilder DEMO START ---")

    # Define the package name and potentially some generated Java code.
    # This generated_java_code would typically come from Lobe 4 (Code Generation)
    # or Lobe 3 (LLM Interface) after processing Arabic NLP.
    demo_package_name = "com.arabic.app.generator"
    demo_java_snippet = """
        android.util.Log.d("GeneratedApp", "Hello from generated Java code!");
        TextView textView = findViewById(R.id.textView); // Assuming a TextView with id 'textView' exists in activity_main.xml
        if (textView != null) {
            textView.setText("Generated by Arabic NLP!");
        }
    """

    project_builder = AndroidProjectBuilder(project_root_dir="temp_generated_apk_project")

    try:
        project_builder.set_package_name(demo_package_name)
        project_builder.build_project(generated_code_snippet=demo_java_snippet)
        compiled_apk_path = project_builder.compile()
        print(f"\nDemo successful! APK generated at: {compiled_apk_path}")

        # Example of how to interact with the compiled APK (e.g., using ADB)
        # This part would typically be handled by Lobe 8 (APK Compiler) or a subsequent lobe.
        # For demonstration, we just confirm the path exists.
        if os.path.exists(compiled_apk_path):
            print(f"Verified APK file exists: {compiled_apk_path}")
        else:
            print(f"Error: APK file not found at expected path: {compiled_apk_path}")

    except Exception as e:
        print(f"\n--- DEMO FAILED ---")
        print(f"An error occurred: {e}")
    finally:
        # Clean up the dummy project
        project_builder.cleanup()
        print("\n--- Lobe 7: AndroidProjectBuilder DEMO FINISHED ---")



import os
import shutil
import subprocess
import sys
import json

# --- Assume these are defined elsewhere and accessible ---
# from constants import ANDROID_SDK_ROOT
# from utils import run_command
# from Lobe_8_apk_compiler_lobe import compile_apk

# --- Constants (for demonstration purposes, these would be imported) ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    # Fallback or raise an error if ANDROID_SDK_ROOT is not set
    # For local testing, you might hardcode a path if needed
    # ANDROID_SDK_ROOT = "/path/to/your/android/sdk"
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

GRADLE_PROPERTIES_TEMPLATE = """
org.gradle.jvmargs=-Xmx2048m
"""

APP_BUILD_GRADLE_TEMPLATE = """
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace "{package_name}"
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
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
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
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

ANDROID_MANIFEST_TEMPLATE = """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp"
        tools:targetApi="31">
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

ACTIVITY_JAVA_TEMPLATE = """
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Added for potential text manipulation

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists
        // --- Generated Logic Start ---
        // Placeholder for logic generated from Arabic NLP
        // --- Generated Logic End ---
    }}
}}
"""

# --- Utility Functions (for demonstration purposes, these would be imported) ---
def create_directory_structure(base_path, package_name):
    """Creates the necessary directory structure for an Android project."""
    package_path = package_name.replace('.', os.sep)
    os.makedirs(os.path.join(base_path, "app", "src", "main", "java", *package_path.split('.')), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "main", "res", "values"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "androidTest", "java", *package_path.split('.')), exist_ok=True)
    os.makedirs(os.path.join(base_path, "app", "src", "test", "java", *package_path.split('.')), exist_ok=True)
    os.makedirs(os.path.join(base_path, "gradle", "wrapper"), exist_ok=True)
    # Create dummy files that are often expected
    with open(os.path.join(base_path, "settings.gradle"), "w") as f:
        f.write("rootProject.name = \"GeneratedApp\"\n")
        f.write("include ':app'\n")
    with open(os.path.join(base_path, "gradlew"), "w") as f: # Placeholder gradlew
        f.write("#!/bin/bash\n")
    os.chmod(os.path.join(base_path, "gradlew"), 0o755)
    with open(os.path.join(base_path, "gradlew.bat"), "w") as f: # Placeholder gradlew.bat
        f.write("@echo off\n")
    with open(os.path.join(base_path, "gradle", "wrapper", "gradle-wrapper.jar"), "w") as f:
        pass
    with open(os.path.join(base_path, "gradle", "wrapper", "gradle-wrapper.properties"), "w") as f:
        f.write("distributionBase=GRADLE_USER_HOME\n")
        f.write("distributionPath=wrapper/dists\n")
        f.write("distributionUrl=https\\://services.gradle.org/distributions/gradle-7.6-bin.zip\n")
        f.write("zipStoreBase=GRADLE_USER_HOME\n")
        f.write("zipStorePath=wrapper/dists\n")

def run_command(command, cwd=None, env=None, error_message="Command failed"):
    """Runs a shell command and returns its output, raising an error on failure."""
    print(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        # print("Command stdout:\n", result.stdout) # Suppress verbose output by default
        if result.stderr:
            print("Command stderr:\n", result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: Exit code {e.returncode}")
        print("Stdout:\n", e.stdout)
        print("Stderr:\n", e.stderr)
        raise

def compile_apk(project_root):
    """Compiles the Android project into an APK using Gradle."""
    gradle_wrapper_path = os.path.join(project_root, "gradlew")
    if sys.platform == "win32":
        gradle_wrapper_path = os.path.join(project_root, "gradlew.bat")

    if not os.path.exists(gradle_wrapper_path):
        raise FileNotFoundError(f"Gradle wrapper not found at {gradle_wrapper_path}")
    if sys.platform != "win32":
        os.chmod(gradle_wrapper_path, 0o755)

    gradle_env = os.environ.copy()
    gradle_env["ANDROID_SDK_ROOT"] = ANDROID_SDK_ROOT

    # Use assembleDebug to build the APK
    command = [gradle_wrapper_path, "assembleDebug"]
    run_command(command, cwd=project_root, env=gradle_env, error_message="Gradle assembleDebug failed")

    # Determine the APK path
    apk_path_debug = os.path.join(project_root, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
    if not os.path.exists(apk_path_debug):
        raise FileNotFoundError(f"APK not found after build. Expected: {apk_path_debug}")
    return apk_path_debug

# --- Lobe 7: AndroidProjectBuilder ---
class AndroidProjectBuilder:
    """
    Constructs a functional Android project structure from natural language inputs,
    generating necessary files and configurations for APK compilation.
    This lobe acts as the bridge between synthesized code/logic and the Android build system.
    """

    def __init__(self, project_root_dir="temp_android_project"):
        """
        Initializes the builder with a root directory for the project.
        Args:
            project_root_dir (str): The path where the Android project will be created.
        """
        self.project_root = os.path.abspath(project_root_dir)
        self.package_name = "com.generated.app"  # Default package name
        self.app_name = "GeneratedApp"          # Default app name

    def set_app_details(self, app_name, package_name):
        """
        Sets the application name and package name.
        Args:
            app_name (str): The desired name for the Android application.
            package_name (str): The Java package name for the application (e.g., "com.example.myapp").
        """
        if not app_name or not isinstance(app_name, str):
            raise ValueError("Invalid application name provided.")
        if not package_name or not isinstance(package_name, str):
            raise ValueError("Invalid package name provided.")
        if not all(c.isalnum() or c == '.' for c in package_name):
            raise ValueError(f"Package name '{package_name}' contains invalid characters.")

        self.app_name = app_name
        self.package_name = package_name
        print(f"App details set: Name='{self.app_name}', Package='{self.package_name}'")

    def _create_gradle_wrapper_files(self):
        """Creates essential Gradle wrapper files."""
        print("Configuring Gradle wrapper...")
        # Ensure gradle/wrapper directory exists
        wrapper_dir = os.path.join(self.project_root, "gradle", "wrapper")
        os.makedirs(wrapper_dir, exist_ok=True)

        # gradle-wrapper.properties
        properties_path = os.path.join(wrapper_dir, "gradle-wrapper.properties")
        with open(properties_path, "w") as f:
            f.write("distributionBase=GRADLE_USER_HOME\n")
            f.write("distributionPath=wrapper/dists\n")
            # Use a recent stable version of Gradle
            f.write("distributionUrl=https\\://services.gradle.org/distributions/gradle-8.4-bin.zip\n")
            f.write("zipStoreBase=GRADLE_USER_HOME\n")
            f.write("zipStorePath=wrapper/dists\n")
        print(f"Created: {properties_path}")

        # gradlew (Unix/Linux/macOS)
        gradlew_path = os.path.join(self.project_root, "gradlew")
        with open(gradlew_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("set -e\n")
            f.write(f"exec \"{os.path.join(self.project_root, 'gradlew.bat')}\" \"$@\"\n")
        os.chmod(gradlew_path, 0o755)
        print(f"Created: {gradlew_path} (executable)")

        # gradlew.bat (Windows)
        gradlew_bat_path = os.path.join(self.project_root, "gradlew.bat")
        with open(gradlew_bat_path, "w") as f:
            f.write("@echo off\n")
            f.write("setlocal\n")
            f.write("set \"GRADLE_executable=%~dp0\\gradle\\wrapper\\gradle-wrapper.jar\"\n")
            f.write("if not exist \"%GRADLE_executable%\" (\n")
            f.write("    echo Downloading Gradle wrapper JAR...\n")
            # This part is tricky, as it relies on the wrapper task itself.
            # A more robust approach might pre-download or ensure it's present.
            # For now, we rely on Gradle itself to download if missing.
            f.write("    call \"%~dp0\\gradlew\" wrapper --gradle-version 8.4 --distribution-type bin\n")
            f.write(")\n")
            f.write("java -Dorg.gradle.appname=\"gradle\" -classpath \"%GRADLE_executable%\" org.gradle.wrapper.GradleWrapperMain %*\n")
            f.write("endlocal\n")
        print(f"Created: {gradlew_bat_path}")

    def _create_build_files(self):
        """Creates the main build.gradle and app/build.gradle files."""
        print("Creating build.gradle files...")
        # settings.gradle
        settings_gradle_path = os.path.join(self.project_root, "settings.gradle")
        with open(settings_gradle_path, "w") as f:
            f.write(f"rootProject.name = \"{self.app_name}\"\n")
            f.write("include ':app'\n")
        print(f"Created: {settings_gradle_path}")

        # app/build.gradle
        app_build_gradle_path = os.path.join(self.project_root, "app", "build.gradle")
        os.makedirs(os.path.dirname(app_build_gradle_path), exist_ok=True)
        with open(app_build_gradle_path, "w") as f:
            f.write(APP_BUILD_GRADLE_TEMPLATE.format(package_name=self.package_name))
        print(f"Created: {app_build_gradle_path}")

        # gradle.properties
        gradle_properties_path = os.path.join(self.project_root, "gradle.properties")
        with open(gradle_properties_path, "w") as f:
            f.write(GRADLE_PROPERTIES_TEMPLATE)
        print(f"Created: {gradle_properties_path}")

    def _create_android_manifest(self):
        """Creates the AndroidManifest.xml file."""
        print("Creating AndroidManifest.xml...")
        manifest_dir = os.path.join(self.project_root, "app", "src", "main")
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, "AndroidManifest.xml")
        with open(manifest_path, "w") as f:
            f.write(ANDROID_MANIFEST_TEMPLATE.replace("Theme.YourAppName", f"Theme.{self.app_name}")) # Customize theme name
        print(f"Created: {manifest_path}")

        # Create dummy xml resource files as placeholders required by manifest
        res_xml_dir = os.path.join(manifest_dir, "res", "xml")
        os.makedirs(res_xml_dir, exist_ok=True)
        with open(os.path.join(res_xml_dir, "backup_rules.xml"), "w") as f:
            f.write("<full-backup-content/>\n")
        with open(os.path.join(res_xml_dir, "data_extraction_rules.xml"), "w") as f:
            f.write("<data-extraction-rules>\n    <cloud-backup />\n</data-extraction-rules>\n")

    def _create_main_activity(self, generated_java_code_snippet=""):
        """
        Creates the main Activity Java file.
        Args:
            generated_java_code_snippet (str): A string containing Java code to be injected
                                                into the onCreate method of MainActivity.
        """
        print("Creating MainActivity.java...")
        package_path_parts = self.package_name.split('.')
        activity_dir = os.path.join(self.project_root, "app", "src", "main", "java", *package_path_parts)
        os.makedirs(activity_dir, exist_ok=True)
        activity_path = os.path.join(activity_dir, "MainActivity.java")

        final_activity_content = ACTIVITY_JAVA_TEMPLATE.format(package_name=self.package_name)

        # Inject the generated code snippet into the onCreate method
        injection_point_marker = "// --- Generated Logic Start ---"
        injection_end_marker = "// --- Generated Logic End ---"
        if injection_point_marker in final_activity_content:
            # Split the template and insert the snippet
            parts = final_activity_content.split(injection_point_marker)
            if len(parts) == 2:
                header = parts[0]
                footer = parts[1].replace(injection_end_marker, "", 1) # Remove only the first occurrence
                final_activity_content = f"{header}{injection_point_marker}\n{generated_java_code_snippet}\n{injection_end_marker}{footer}"
            else:
                 print("Warning: Could not properly inject generated code into MainActivity template. Using fallback.")
                 final_activity_content = final_activity_content.replace("setContentView(R.layout.activity_main);",
                                                                        f"setContentView(R.layout.activity_main);\n        {generated_java_code_snippet}")
        else:
            print("Warning: Injection marker not found in template. Appending generated code.")
            final_activity_content = final_activity_content.replace(
                "setContentView(R.layout.activity_main);",
                f"setContentView(R.layout.activity_main);\n        {generated_java_code_snippet}"
            )

        with open(activity_path, "w") as f:
            f.write(final_activity_content)
        print(f"Created: {activity_path}")

        # Create a basic layout file for activity_main.xml
        layout_dir = os.path.join(self.project_root, "app", "src", "main", "res", "layout")
        os.makedirs(layout_dir, exist_ok=True)
        layout_path = os.path.join(layout_dir, "activity_main.xml")
        with open(layout_path, "w") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"\n')
            f.write('    xmlns:app="http://schemas.android.com/apk/res-auto"\n')
            f.write('    xmlns:tools="http://schemas.android.com/tools"\n')
            f.write('    android:layout_width="match_parent"\n')
            f.write('    android:layout_height="match_parent"\n')
            f.write('    tools:context=".MainActivity">\n\n')
            f.write('    <TextView\n')
            f.write('        android:id="@+id/greeting_text"\n')
            f.write('        android:layout_width="wrap_content"\n')
            f.write('        android:layout_height="wrap_content"\n')
            f.write('        android:text="Hello from Generated App!"\n')
            f.write('        android:textSize="24sp"\n')
            f.write('        app:layout_constraintBottom_toBottomOf="parent"\n')
            f.write('        app:layout_constraintEnd_toEndOf="parent"\n')
            f.write('        app:layout_constraintStart_toStartOf="parent"\n')
            f.write('        app:layout_constraintTop_toTopOf="parent" />\n')
            f.write('</androidx.constraintlayout.widget.ConstraintLayout>\n')
        print(f"Created: {layout_path}")

        # Create basic values/strings.xml
        values_dir = os.path.join(self.project_root, "app", "src", "main", "res", "values")
        os.makedirs(values_dir, exist_ok=True)
        strings_path = os.path.join(values_dir, "strings.xml")
        with open(strings_path, "w") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<resources>\n')
            f.write(f'    <string name="app_name">{self.app_name}</string>\n')
            f.write('</resources>\n')
        print(f"Created: {strings_path}")


    def build(self, app_name, package_name, generated_java_code_snippet=""):
        """
        Orchestrates the creation of the entire Android project structure.
        Args:
            app_name (str): The desired name for the Android application.
            package_name (str): The Java package name for the application.
            generated_java_code_snippet (str): Java code to inject into MainActivity.
        Returns:
            str: The path to the root directory of the created Android project.
        """
        print(f"\n--- Initiating Android Project Build (Root: {self.project_root}) ---")
        if os.path.exists(self.project_root):
            print(f"Project root '{self.project_root}' exists. Removing and recreating.")
            shutil.rmtree(self.project_root)
        os.makedirs(self.project_root)

        self.set_app_details(app_name, package_name)
        
        # 1. Create directory structure
        print("Creating base directory structure...")
        package_path_parts = self.package_name.split('.')
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "java", *package_path_parts), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "res", "values"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "androidTest", "java", *package_path_parts), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "test", "java", *package_path_parts), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "gradle", "wrapper"), exist_ok=True)

        # 2. Create Gradle wrapper files
        self._create_gradle_wrapper_files()

        # 3. Create build files (settings.gradle, app/build.gradle, gradle.properties)
        self._create_build_files()

        # 4. Create AndroidManifest.xml
        self._create_android_manifest()

        # 5. Create MainActivity.java and associated layout/strings resources
        self._create_main_activity(generated_java_code_snippet)

        print("--- Android Project Build Complete ---")
        return self.project_root

    def compile(self):
        """
        Compiles the constructed Android project into an APK using the Gradle wrapper.
        Returns:
            str: The absolute path to the generated APK file.
        Raises:
            FileNotFoundError: If the Gradle wrapper or expected APK is not found.
            RuntimeError: If the Gradle build process fails.
        """
        print("\n--- Initiating APK Compilation ---")
        if not os.path.exists(self.project_root):
            raise FileNotFoundError(f"Project root directory does not exist: {self.project_root}")

        try:
            apk_path = compile_apk(self.project_root)
            print(f"APK successfully compiled: {apk_path}")
            return apk_path
        except Exception as e:
            print(f"Error during APK compilation: {e}")
            raise RuntimeError("APK compilation failed.") from e
        finally:
            print("--- APK Compilation Process Finished ---")

    def cleanup(self):
        """Removes the generated project directory."""
        print(f"\n--- Cleaning up project directory: {self.project_root} ---")
        if os.path.exists(self.project_root):
            try:
                shutil.rmtree(self.project_root)
                print("Project directory removed successfully.")
            except OSError as e:
                print(f"Error removing directory {self.project_root}: {e.strerror}")
        else:
            print("Project directory does not exist, no cleanup needed.")

# --- Integration Point ---
# This section would be called by Lobe 6 (Synthesis) after Lobe 4 (Code Generation)
# produces a Java snippet.

# Example of how Lobe 7 would be used by the system:
def build_and_compile_apk_from_nlp(nlp_output_data, output_dir="generated_apks"):
    """
    Processes NLP output to build and compile an Android APK.
    Args:
        nlp_output_data (dict): A dictionary containing structured information
                                extracted from NLP, e.g.:
                                {
                                    "app_name": "MyArabicApp",
                                    "package_name": "com.arabic.app.generated",
                                    "java_code_snippet": "TextView tv = findViewById(R.id.greeting_text);\ntv.setText(\"تم إنشاؤه بواسطة الذكاء الاصطناعي!\");"
                                }
        output_dir (str): Directory to store the generated APK.
    Returns:
        str: Path to the compiled APK, or None if compilation failed.
    """
    if not nlp_output_data:
        print("Error: No NLP output data provided.")
        return None

    app_name = nlp_output_data.get("app_name", "GeneratedApp")
    package_name = nlp_output_data.get("package_name", "com.generated.app")
    java_snippet = nlp_output_data.get("java_code_snippet", "")

    # Create a unique project directory to avoid conflicts
    timestamp = os.urandom(4).hex()
    project_root = os.path.join(output_dir, f"{app_name.replace(' ', '_').lower()}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    builder = AndroidProjectBuilder(project_root_dir=project_root)
    apk_path = None

    try:
        builder.build(app_name, package_name, java_snippet)
        apk_path = builder.compile()
        print(f"Successfully built and compiled APK: {apk_path}")
        # Move APK to a final destination if needed
        final_apk_name = f"{package_name.split('.')[-1]}-{app_name.lower().replace(' ', '_')}.apk"
        final_apk_path = os.path.join(output_dir, final_apk_name)
        if apk_path and os.path.exists(apk_path):
            shutil.move(apk_path, final_apk_path)
            print(f"APK moved to: {final_apk_path}")
            return final_apk_path
        else:
            print("Warning: Compiled APK path is invalid or does not exist.")
            return None

    except Exception as e:
        print(f"Failed to build or compile APK for {app_name}: {e}")
        return None
    finally:
        # Cleanup the temporary project directory
        builder.cleanup()


if __name__ == '__main__':
    # --- DEMO USAGE ---
    print("--- Lobe 7: AndroidProjectBuilder DEMO START ---")

    # Simulate NLP output data
    sample_nlp_output = {
        "app_name": "تطبيقي الأول", # My First App
        "package_name": "com.arabic.firstapp.generated",
        "java_code_snippet": """
            TextView greetingTextView = findViewById(R.id.greeting_text);
            if (greetingTextView != null) {
                greetingTextView.setText("أهلاً بك في تطبيقي!"); // Welcome to my app!
                android.util.Log.d("AppBuilderDemo", "Greeting text updated.");
            } else {
                android.util.Log.e("AppBuilderDemo", "TextView with ID 'greeting_text' not found.");
            }
            // Example: Add a simple button click listener if we had a button
            // Button myButton = findViewById(R.id.my_button);
            // if (myButton != null) {
            //     myButton.setOnClickListener(v -> {
            //         android.widget.Toast.makeText(this, "Button Clicked!", android.widget.Toast.LENGTH_SHORT).show();
            //     });
            // }
        """
    }

    # Define an output directory for the final APK
    output_directory = "generated_apks_output"

    # Call the integration function
    compiled_apk_location = build_and_compile_apk_from_nlp(sample_nlp_output, output_directory)

    if compiled_apk_location:
        print(f"\n--- DEMO SUCCESS ---")
        print(f"Final APK generated and saved at: {compiled_apk_location}")
    else:
        print("\n--- DEMO FAILED ---")
        print("APK generation process encountered errors.")

    print("\n--- Lobe 7: AndroidProjectBuilder DEMO FINISHED ---")