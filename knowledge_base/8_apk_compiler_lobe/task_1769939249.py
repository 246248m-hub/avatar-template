import os
import shutil
import subprocess
from pathlib import Path

# --- Constants ---
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
OUTPUT_APKS_DIR = Path("./output_apks")
GRADLE_WRAPPER_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "gradlew"
APP_BUILD_GRADLE_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle"
MANIFEST_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml"
MAIN_ACTIVITY_JAVA_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myapp" / "MainActivity.java"

# --- Helper Functions ---
def setup_android_project_template(project_name="MyApp"):
    """
    Creates a basic Android project structure for compilation.
    In a real scenario, this would involve more sophisticated project generation
    or cloning a template with placeholders for dynamic content.
    For this simulation, we create a minimal structure.
    """
    print(f"Setting up Android project template in: {ANDROID_PROJECT_TEMPLATE_DIR}")
    if not ANDROID_PROJECT_TEMPLATE_DIR.exists():
        ANDROID_PROJECT_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

    # Create dummy Gradle wrapper (essential for building)
    if not GRADLE_WRAPPER_PATH.exists():
        print("Creating dummy gradlew script...")
        (ANDROID_PROJECT_TEMPLATE_DIR / "gradlew").write_text("#!/bin/bash\necho 'Dummy gradlew executed'\nexit 0")
        os.chmod(GRADLE_WRAPPER_PATH, 0o755) # Make it executable

    # Create dummy app directory and build.gradle
    app_dir = ANDROID_PROJECT_TEMPLATE_DIR / "app"
    app_dir.mkdir(parents=True, exist_ok=True)
    if not APP_BUILD_GRADLE_PATH.exists():
        print("Creating dummy app/build.gradle...")
        APP_BUILD_GRADLE_PATH.write_text("""
plugins {
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
    // Minimal dependencies for a basic build
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""")

    # Create dummy AndroidManifest.xml
    manifest_dir = MANIFEST_PATH.parent
    manifest_dir.mkdir(parents=True, exist_ok=True)
    if not MANIFEST_PATH.exists():
        print("Creating dummy AndroidManifest.xml...")
        MANIFEST_PATH.write_text(f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp">
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
""")

    # Create dummy MainActivity.java
    main_activity_dir = MAIN_ACTIVITY_JAVA_PATH.parent
    main_activity_dir.mkdir(parents=True, exist_ok=True)
    if not MAIN_ACTIVITY_JAVA_PATH.exists():
        print("Creating dummy MainActivity.java...")
        MAIN_ACTIVITY_JAVA_PATH.write_text(f"""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
""")

    # Create necessary resource directories and files (minimal)
    resources_dir = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res"
    resources_dir.mkdir(parents=True, exist_ok=True)

    layout_dir = resources_dir / "layout"
    layout_dir.mkdir(exist_ok=True)
    (layout_dir / "activity_main.xml").write_text("""
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
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
""")

    values_dir = resources_dir / "values"
    values_dir.mkdir(exist_ok=True)
    (values_dir / "strings.xml").write_text("""
<resources>
    <string name="app_name">MyApp</string>
</resources>
""")

    mipmap_dir = resources_dir / "mipmap-hdpi"
    mipmap_dir.mkdir(exist_ok=True)
    # Placeholder for icon, a real build would need actual icons
    (mipmap_dir / "ic_launcher.png").write_text("")

    mipmap_round_dir = resources_dir / "mipmap-xhdpi"
    mipmap_round_dir.mkdir(exist_ok=True)
    (mipmap_round_dir / "ic_launcher_round.png").write_text("")

    print("Android project template setup complete (minimal structure).")


def cleanup_android_project_template():
    """Removes the dummy Android project template and output APK directory."""
    print("\n--- Cleaning up Android project template ---")
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        try:
            shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
            print(f"Removed Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        except OSError as e:
            print(f"Error removing directory {ANDROID_PROJECT_TEMPLATE_DIR}: {e}")
    if os.path.exists(OUTPUT_APKS_DIR):
        try:
            shutil.rmtree(OUTPUT_APKS_DIR)
            print(f"Removed output APK directory: {OUTPUT_APKS_DIR}")
        except OSError as e:
            print(f"Error removing directory {OUTPUT_APKS_DIR}: {e}")

# --- Lobe 8: APK Compiler Lobe ---
class ApkCompilerLobe:
    def __init__(self):
        self.output_dir = OUTPUT_APKS_DIR
        self.project_dir = ANDROID_PROJECT_TEMPLATE_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_apk(self, app_name="final_app.apk"):
        """
        Compiles the Android project into an APK.
        This is a simulated build process as a full Android build environment
        is complex to set up and run within this context.
        We will execute a dummy gradlew command and assume success.
        """
        print("\n--- Initiating APK Compilation ---")
        if not self.project_dir.exists() or not GRADLE_WRAPPER_PATH.exists():
            print("Android project template not found or incomplete. Setting up a minimal template.")
            setup_android_project_template()

        print(f"Attempting to build APK using: {GRADLE_WRAPPER_PATH}")
        # In a real scenario, you would execute:
        # subprocess.run([str(GRADLE_WRAPPER_PATH), "assembleRelease"], cwd=str(self.project_dir), check=True)
        # For simulation purposes, we'll just print a success message.
        print("Simulating APK build process. In a real environment, this would involve Gradle.")
        print("Dummy build command executed: ./gradlew assembleRelease")

        # Simulate APK file creation
        output_apk_path = self.output_dir / app_name
        try:
            # Create a dummy APK file to represent a successful build
            with open(output_apk_path, "w") as f:
                f.write("This is a dummy APK file.")
            print(f"Dummy APK created at: {output_apk_path}")
        except IOError as e:
            print(f"Error creating dummy APK file: {e}")

        print("APK Compilation Simulation Complete.")
        return str(output_apk_path)

    def run(self, app_name="final_app.apk"):
        """Executes the APK compilation process."""
        return self.build_apk(app_name)

# --- Example Usage (for demonstration) ---
if __name__ == "__main__":
    print("--- APK Compiler Lobe Demonstration ---")

    # Initialize the APK Compiler Lobe
    apk_compiler = ApkCompilerLobe()

    # Setup a dummy Android project template
    setup_android_project_template("SimulatedApp")

    # Build the APK (simulated)
    generated_apk_path = apk_compiler.run(app_name="my_generated_app.apk")
    print(f"\nSimulated APK generation process finished. Output: {generated_apk_path}")

    # Clean up the dummy project and output
    cleanup_android_project_template()