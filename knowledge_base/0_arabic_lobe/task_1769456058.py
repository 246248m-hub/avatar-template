import os
import shutil
import subprocess

JAVA_PROJECT_DIR = "generated_java_project"
TEMP_JAVA_DIR = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", "com", "example", "myapp")
MAIN_ACTIVITY_PATH = os.path.join(TEMP_JAVA_DIR, "MainActivity.java")
BUILD_GRADLE_PATH = os.path.join(JAVA_PROJECT_DIR, "app", "build.gradle")
GRADLE_WRAPPER_PROPERTIES_PATH = os.path.join(JAVA_PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.properties")
SETTINGS_GRADLE_PATH = os.path.join(JAVA_PROJECT_DIR, "settings.gradle")

def create_android_project_structure():
    """Creates the basic directory structure for an Android project."""
    os.makedirs(TEMP_JAVA_DIR, exist_ok=True)

def create_main_activity_java(activity_name="MainActivity"):
    """Creates a basic MainActivity.java file."""
    java_code = f"""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists

        TextView textView = findViewById(R.id.textView); // Assuming a TextView with id 'textView'
        textView.setText("Hello from generated APK!");
    }}
}}
"""
    with open(MAIN_ACTIVITY_PATH, "w", encoding="utf-8") as f:
        f.write(java_code)

def create_build_gradle():
    """Creates a basic app/build.gradle file."""
    gradle_content = """
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace 'com.example.myapp'
    compileSdk 33

    defaultConfig {{
        applicationId "com.example.myapp"
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
    buildFeatures {{
        viewBinding true
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
    with open(BUILD_GRADLE_PATH, "w", encoding="utf-8") as f:
        f.write(gradle_content)

def create_gradle_wrapper_properties():
    """Creates a basic gradle-wrapper.properties file."""
    properties_content = """
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-bin.zip
"""
    os.makedirs(os.path.dirname(GRADLE_WRAPPER_PROPERTIES_PATH), exist_ok=True)
    with open(GRADLE_WRAPPER_PROPERTIES_PATH, "w", encoding="utf-8") as f:
        f.write(properties_content)

def create_settings_gradle():
    """Creates a basic settings.gradle file."""
    settings_content = """
rootProject.name = "MyApp"
include ':app'
"""
    with open(SETTINGS_GRADLE_PATH, "w", encoding="utf-8") as f:
        f.write(settings_content)

def create_activity_main_xml():
    """Creates a basic activity_main.xml file."""
    xml_content = """
<?xml version="1.0" encoding="utf-8"?>
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
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    activity_res_dir = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "layout")
    os.makedirs(activity_res_dir, exist_ok=True)
    with open(os.path.join(activity_res_dir, "activity_main.xml"), "w", encoding="utf-8") as f:
        f.write(xml_content)


def build_apk(project_dir):
    """Builds the APK using Gradle."""
    try:
        # Execute Gradle wrapper to assemble the app
        # Assuming gradlew is available in the project_dir or accessible in PATH
        # If not, you might need to provide the full path to the gradlew script
        # Example: cmd = ["./gradlew", "assembleDebug"]
        # On Windows, it might be: cmd = ["gradlew.bat", "assembleDebug"]
        # For cross-platform compatibility, we can try to find gradlew
        gradlew_path = os.path.join(project_dir, "gradlew")
        if os.name == 'nt': # Windows
            gradlew_path = os.path.join(project_dir, "gradlew.bat")

        if not os.path.exists(gradlew_path):
            print(f"Error: Gradle wrapper not found at {gradlew_path}. Please ensure it's generated or available.")
            # As a fallback, try using the system gradle command if available
            cmd = ["gradle", "assembleDebug"]
        else:
            cmd = [gradlew_path, "assembleDebug"]

        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True, check=True)
        print("Gradle build output:\n", result.stdout)
        print("Gradle build errors:\n", result.stderr)

        # Find the generated APK
        apk_path = None
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = os.path.join(root, file)
                    break
            if apk_path:
                break

        if apk_path:
            print(f"Successfully built APK: {apk_path}")
            return apk_path
        else:
            print("Error: Could not find generated APK after build.")
            return None

    except FileNotFoundError:
        print("Error: 'gradlew' or 'gradle' command not found. Make sure Gradle is installed and in your PATH, or the gradlew script is present.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during APK build: {e}")
        return None

def cleanup_apk_compiler_artifacts(project_root, java_project_dir):
    """Cleans up generated project files and temporary directories."""
    if os.path.exists(java_project_dir):
        shutil.rmtree(java_project_dir)
        print(f"Removed generated project directory: {java_project_dir}")
    # Clean up any other temporary files or directories created during the process
    # For example, if a separate dummy APK was created and not removed
    # if os.path.exists(os.path.join(project_root, "dummy_apk.apk")):
    #     os.remove(os.path.join(project_root, "dummy_apk.apk"))
    #     print("Removed dummy_apk.apk")

class APKCompilerLobe:
    def __init__(self):
        self.generated_apk_path = None

    def generate_apk_from_code(self, java_code_content, layout_xml_content):
        """
        Generates an Android APK from provided Java code and XML layout content.
        This is a simplified implementation. A real scenario would involve more
        complex project setup and potentially template-based generation.
        """
        print("\n--- Initiating APK Compilation Lobe ---")
        try:
            # 1. Create Project Structure
            create_android_project_structure()
            create_activity_main_xml() # Ensure layout is created

            # 2. Write Java Code
            # Assuming the provided java_code_content is for MainActivity.java
            # In a more complex scenario, this would be dynamically written or selected
            main_activity_file_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", "com", "example", "myapp", "MainActivity.java")
            os.makedirs(os.path.dirname(main_activity_file_path), exist_ok=True)
            with open(main_activity_file_path, "w", encoding="utf-8") as f:
                f.write(java_code_content)
            print(f"Created MainActivity.java at: {main_activity_file_path}")

            # 3. Write Layout XML
            layout_dir = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "layout")
            os.makedirs(layout_dir, exist_ok=True)
            with open(os.path.join(layout_dir, "activity_main.xml"), "w", encoding="utf-8") as f:
                f.write(layout_xml_content)
            print("Created activity_main.xml")

            # 4. Create Gradle files
            create_build_gradle()
            create_gradle_wrapper_properties()
            create_settings_gradle()
            print("Created necessary Gradle configuration files.")

            # 5. Build the APK
            print("Attempting to build APK...")
            self.generated_apk_path = build_apk(JAVA_PROJECT_DIR)

            if self.generated_apk_path:
                print(f"APK generated successfully at: {self.generated_apk_path}")
            else:
                print("APK generation failed.")

        except Exception as e:
            print(f"An error occurred during APK generation: {e}")
            self.generated_apk_path = None
        finally:
            print("--- APK Compilation Lobe Finished ---")
        return self.generated_apk_path

    def cleanup(self):
        """Cleans up the generated project artifacts."""
        print("\n--- Cleaning up APK Compiler Lobe artifacts ---")
        cleanup_apk_compiler_artifacts(".", JAVA_PROJECT_DIR)
        self.generated_apk_path = None

# Example Usage (demonstrating the module's functionality)
if __name__ == "__main__":
    apk_compiler = APKCompilerLobe()

    # --- Dummy Java Code and XML for demonstration ---
    sample_java_code = """
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("Hello from Generated Arabic App!");
    }
}
"""

    sample_xml_layout = """
<?xml version="1.0" encoding="utf-8"?>
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
        android:text="Welcome!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

    # Generate APK
    generated_apk = apk_compiler.generate_apk_from_code(sample_java_code, sample_xml_layout)

    if generated_apk:
        print(f"\nDemo: APK successfully generated at {generated_apk}")
        # In a real scenario, you might want to copy this APK to a specific location
        # or proceed with further analysis/deployment.
    else:
        print("\nDemo: APK generation failed.")

    # Clean up artifacts
    apk_compiler.cleanup()