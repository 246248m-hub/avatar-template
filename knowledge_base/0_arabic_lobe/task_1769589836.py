import subprocess
import os
from pathlib import Path
import json
import time

class ArabicApkModule:
    def __init__(self, base_project_path: Path):
        self.base_project_path = base_project_path
        self.project_name = "ArabicRtlProject"
        self.project_path = self.base_project_path / self.project_name
        self.app_module_path = self.project_path / "app"
        self.build_gradle_path = self.app_module_path / "build.gradle"
        self.main_activity_path = self.app_module_path / "src/main/java/com/rtl/arabic/javademo/MainActivity.java"
        self.manifest_path = self.app_module_path / "src/main/AndroidManifest.xml"

        self.debug_keystore_dir = Path.home() / ".android/debug/keystore"
        self.debug_keystore_path = self.debug_keystore_dir / "debug.keystore"

    def _create_directory_structure(self):
        """Creates the necessary directory structure for an Android project."""
        print(f"Creating project structure at: {self.project_path}")
        self.project_path.mkdir(parents=True, exist_ok=True)
        self.app_module_path.mkdir(parents=True, exist_ok=True)
        (self.app_module_path / "src/main/java/com/rtl/arabic/javademo").mkdir(parents=True, exist_ok=True)
        (self.app_module_path / "src/main/res/values").mkdir(parents=True, exist_ok=True)
        (self.app_module_path / "src/main/res/layout").mkdir(parents=True, exist_ok=True)

    def _create_build_gradle(self, package_name: str, use_kotlin: bool):
        """Creates a basic build.gradle file."""
        print(f"Creating build.gradle at: {self.build_gradle_path}")
        gradle_content = f"""
plugins {{
    id 'com.android.application'
    {'id "org.jetbrains.kotlin.android"' if use_kotlin else ''}
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
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
    {'kotlinOptions {{ jvmTarget = "1.8" }}' if use_kotlin else ''}
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
        with open(self.build_gradle_path, "w") as f:
            f.write(gradle_content)

    def _create_main_activity(self, app_name: str, package_name: str, use_kotlin: bool):
        """Creates a basic MainActivity file."""
        print(f"Creating MainActivity at: {self.main_activity_path}")
        activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Import TextView

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Set layout for the activity. For RTL support, we'll use a layout that handles it.
        // For simplicity, let's set content view directly and assume a basic layout.
        setContentView(R.layout.activity_main); // Assumes activity_main.xml exists

        // Example of setting text, which can be RTL-aware depending on the TextView's configuration
        TextView welcomeText = findViewById(R.id.welcome_message); // Assumes a TextView with id 'welcome_message' exists
        if (welcomeText != null) {{
            // The framework handles RTL rendering for text if the locale is Arabic and TextView properties are set.
            welcomeText.setText("{app_name}");
        }}
    }}
}}
"""
        if use_kotlin:
            activity_content = f"""
package {package_name}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView // Import TextView

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main) // Assumes activity_main.xml exists

        // Example of setting text, which can be RTL-aware depending on the TextView's configuration
        val welcomeText = findViewById<TextView>(R.id.welcome_message) // Assumes a TextView with id 'welcome_message' exists
        welcomeText?.let {{
            // The framework handles RTL rendering for text if the locale is Arabic and TextView properties are set.
            it.text = "{app_name}"
        }}
    }}
}}
"""
        main_activity_file = Path(str(self.main_activity_path).replace(".java", ".kt" if use_kotlin else ".java"))
        with open(main_activity_file, "w") as f:
            f.write(activity_content)

    def _create_manifest(self, app_name: str, package_name: str):
        """Creates a basic AndroidManifest.xml file."""
        print(f"Creating AndroidManifest.xml at: {self.manifest_path}")
        manifest_content = f"""
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
        android:theme="@style/Theme.{self.project_name}"
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
        with open(self.manifest_path, "w") as f:
            f.write(manifest_content)

    def _create_resources(self, app_name: str):
        """Creates basic string and layout resources."""
        print("Creating resource files...")
        # strings.xml
        strings_xml_path = self.app_module_path / "src/main/res/values/strings.xml"
        strings_xml_content = f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
        with open(strings_xml_path, "w") as f:
            f.write(strings_xml_content)

        # activity_main.xml
        activity_main_xml_path = self.app_module_path / "src/main/res/layout/activity_main.xml"
        activity_main_xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_message"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        android:gravity="center"
        />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(activity_main_xml_path, "w") as f:
            f.write(activity_main_xml_content)

    def _ensure_debug_keystore(self):
        """Ensures a debug.keystore exists. Mocks it if not found."""
        print("Ensuring debug.keystore exists...")
        if not self.debug_keystore_path.exists():
            print(f"Debug keystore not found at {self.debug_keystore_path}. Mocking...")
            self.debug_keystore_dir.mkdir(parents=True, exist_ok=True)
            # Create a dummy file to simulate its presence
            with open(self.debug_keystore_path, "w") as f:
                f.write("This is a mock debug.keystore file.\n")
            print("Mock debug.keystore created.")
        else:
            print("Debug keystore found.")

    def _mock_gradlew_script(self):
        """Mocks the gradlew script if it doesn't exist."""
        gradlew_path = self.project_path / "gradlew"
        if not gradlew_path.exists():
            print(f"Mocking gradlew script at: {gradlew_path}")
            # Simple mock script that prints a message.
            # In a real scenario, you'd want to copy a real gradlew from an Android SDK.
            mock_script_content = """#!/bin/bash
echo "Mock gradlew script executed."
echo "This script is a placeholder for the actual Gradle wrapper."
exit 0
"""
            with open(gradlew_path, "w") as f:
                f.write(mock_script_content)
            # Make the script executable
            os.chmod(gradlew_path, 0o755)

    def _run_gradle_build(self, package_name: str):
        """Attempts to run a Gradle build command. This is a simplified mock."""
        print("Attempting to run Gradle build (simulated)...")
        # In a real scenario, you'd call the gradlew command:
        # try:
        #     subprocess.run([str(self.project_path / "gradlew"), "build"], cwd=str(self.project_path), check=True)
        #     print("Gradle build command executed (simulated).")
        # except subprocess.CalledProcessError as e:
        #     print(f"Gradle build command failed (simulated): {e}")
        # except FileNotFoundError:
        #     print("Gradle wrapper (gradlew) not found. Please ensure it's available or mocked correctly.")

        # For this example, we'll just print a success message.
        print(f"Simulating successful Gradle build for APK generation for package: {package_name}")
        time.sleep(1) # Simulate build time
        print("APK generation process (simulated) completed.")

    def build_module(self, app_name: str, package_name: str, use_kotlin: bool = False):
        """Builds the entire Android APK module structure."""
        self._create_directory_structure()
        self._create_build_gradle(package_name, use_kotlin)
        self._create_main_activity(app_name, package_name, use_kotlin)
        self._create_manifest(app_name, package_name)
        self._create_resources(app_name)
        self._ensure_debug_keystore()
        self._mock_gradlew_script()
        self._run_gradle_build(package_name)

    def clean_project_directory(self):
        """Cleans up the generated project directory."""
        print(f"Cleaning up project directory: {self.project_path}")
        if self.project_path.exists():
            import shutil
            try:
                shutil.rmtree(self.project_path)
                print(f"Successfully removed: {self.project_path}")
            except OSError as e:
                print(f"Error removing directory {self.project_path}: {e}")
        else:
            print(f"Project directory {self.project_path} does not exist. Nothing to clean.")

        # Clean up mocked debug.keystore if it was mocked by this module
        if self.debug_keystore_path.exists() and "mock debug.keystore file" in self.debug_keystore_path.read_text():
            print(f"Removing mocked debug.keystore: {self.debug_keystore_path}")
            try:
                self.debug_keystore_path.unlink()
                if not any(self.debug_keystore_dir.iterdir()): # Check if directory is empty
                    self.debug_keystore_dir.rmdir()
                print("Mock debug.keystore removed.")
            except OSError as e:
                print(f"Error removing mock debug.keystore: {e}")


# Example Usage (for demonstration purposes, not part of the raw code output)
if __name__ == "__main__":
    print("--- Arabic Parser and Generator Module Demo ---")

    # Setup dummy directory
    DUMMY_PROJECT_BASE = Path("./dummy_android_projects")
    DUMMY_PROJECT_BASE.mkdir(exist_ok=True)

    def cleanup_dummy_files():
        if DUMMY_PROJECT_BASE.exists():
            import shutil
            shutil.rmtree(DUMMY_PROJECT_BASE)
            print(f"Removed dummy directory: {DUMMY_PROJECT_BASE}")

    # --- Test Case 1: Java Android Module ---
    print("\n--- Test Case 1: Building Java Android Module ---")
    arabic_module_java = ArabicApkModule(base_project_path=DUMMY_PROJECT_BASE)
    arabic_module_java.build_module(app_name="My RTL App Java", package_name="com.rtl.arabic.javademo", use_kotlin=False)
    print("\nJava module build process simulated.")
    arabic_module_java.clean_project_directory()

    # --- Test Case 2: Kotlin Android Module ---
    print("\n--- Test Case 2: Building Kotlin Android Module ---")
    arabic_module_kotlin = ArabicApkModule(base_project_path=DUMMY_PROJECT_BASE)
    arabic_module_kotlin.build_module(app_name="My RTL App Kotlin", package_name="com.rtl.arabic.kotlindemo", use_kotlin=True)
    print("\nKotlin module build process simulated.")
    arabic_module_kotlin.clean_project_directory()

    # --- Test Case 3: Verify Cleanup ---
    print("\n--- Test Case 3: Verifying Cleanup ---")
    cleanup_dummy_files()

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")