import os
import subprocess
import shutil
import zipfile
import stat
from pathlib import Path

# Constants for Android build
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT is not set. Please set it to your Android SDK path.")

GRADLE_WRAPPER_EXEC = "./gradlew"

class ApkBuilder:
    """
    Manages the process of building an APK from an Android project.
    This lobe focuses on the compilation and packaging aspects.
    """
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.build_output_dir = self.project_dir / "app" / "build" / "outputs" / "apk" / "debug"
        self.keystore_dir = Path.home() / ".android"
        self.debug_keystore_path = self.keystore_dir / "debug.keystore"

    def _ensure_debug_keystore(self):
        """
        Ensures the debug.keystore file exists, creating a mock one if necessary.
        This is a temporary measure to allow building without a real keystore.
        In a production scenario, a proper keystore should be used.
        """
        if not self.debug_keystore_path.exists():
            print(f"Debug keystore not found at {self.debug_keystore_path}. Mocking...")
            self.keystore_dir.mkdir(parents=True, exist_ok=True)
            try:
                # Create a dummy keystore with minimal required structure
                # Note: This is not a functional keystore for release, just for build simulation
                with open(self.debug_keystore_path, "wb") as f:
                    f.write(b"This is a mock debug keystore file.\n")
                # Set appropriate permissions (similar to a real keystore)
                st = os.stat(self.debug_keystore_path)
                os.chmod(self.debug_keystore_path, st.st_mode | stat.S_IRUSR | stat.S_IWUSR)
                print("Mock debug.keystore created.")
            except Exception as e:
                print(f"Error creating mock debug.keystore: {e}")
                raise

    def _configure_gradle_properties(self):
        """
        Configures the gradle.properties file to point to the correct keystore.
        """
        gradle_properties_path = self.project_dir / "gradle.properties"
        properties_content = [
            "MYAPP_RELEASE_STORE_FILE=debug.keystore",
            "MYAPP_RELEASE_KEY_ALIAS=androiddebugkey",
            "MYAPP_RELEASE_STORE_PASSWORD=android",
            "MYAPP_RELEASE_KEY_PASSWORD=android",
        ]
        try:
            with open(gradle_properties_path, "a") as f:
                for line in properties_content:
                    f.write(line + "\n")
            print("gradle.properties configured.")
        except Exception as e:
            print(f"Error configuring gradle.properties: {e}")
            raise

    def build_apk(self) -> Path:
        """
        Executes the Gradle build command to generate an APK.

        Returns:
            Path: The path to the generated APK file.
        """
        print(f"Starting APK build for project at: {self.project_dir}")
        if not (self.project_dir / "gradlew").exists():
            raise FileNotFoundError("Gradle wrapper (gradlew) not found in the project directory.")

        self._ensure_debug_keystore()
        self._configure_gradle_properties()

        # Ensure gradlew is executable
        gradlew_path = self.project_dir / "gradlew"
        if not gradlew_path.exists():
            raise FileNotFoundError("Gradle wrapper not found at {}".format(gradlew_path))
        try:
            st = os.stat(gradlew_path)
            os.chmod(gradlew_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except Exception as e:
            print(f"Error making gradlew executable: {e}")
            raise

        try:
            # Execute the Gradle build command
            # We're targeting the 'assembleDebug' task
            result = subprocess.run(
                [str(gradlew_path), "assembleDebug"],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                check=True  # Raise an exception if the command fails
            )
            print("Gradle build output:")
            print(result.stdout)
            if result.stderr:
                print("Gradle build error output:")
                print(result.stderr)

            # Locate the generated APK
            debug_apk_path = self.build_output_dir / "app-debug.apk"
            if not debug_apk_path.exists():
                raise FileNotFoundError(f"APK not found at expected location: {debug_apk_path}")

            print(f"APK successfully built at: {debug_apk_path}")
            return debug_apk_path

        except subprocess.CalledProcessError as e:
            print(f"Gradle build failed with error code {e.returncode}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            raise
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            raise

    def cleanup_build_artifacts(self):
        """
        Cleans up build directories.
        """
        print("Cleaning up build artifacts...")
        build_dir = self.project_dir / "app" / "build"
        if build_dir.exists():
            try:
                shutil.rmtree(build_dir)
                print(f"Removed build directory: {build_dir}")
            except OSError as e:
                print(f"Error removing build directory {build_dir}: {e}")

    def cleanup_mock_keystore(self):
        """
        Cleans up the mocked debug.keystore if it was created by this module.
        """
        print("Attempting to clean up mocked debug.keystore...")
        if self.debug_keystore_path.exists():
            try:
                # Check if it's the mock we created
                with open(self.debug_keystore_path, "r") as f:
                    content = f.read()
                    if "This is a mock debug keystore file." in content:
                        print("Cleaning up mocked debug.keystore...")
                        self.debug_keystore_path.unlink()
                        # Attempt to remove parent directory if empty
                        try:
                            self.debug_keystore_path.parent.rmdir()
                            print(f"Removed empty directory: {self.debug_keystore_path.parent}")
                        except OSError:
                            pass # Directory not empty, ignore
            except Exception as e:
                print(f"Error during mock keystore cleanup: {e}")
        else:
            print("Mock debug.keystore not found, no cleanup needed.")

# Example Usage (for demonstration purposes, not to be included in final output)
if __name__ == "__main__":
    # This section demonstrates how Lobe 8 might be used.
    # In a real scenario, project_dir would be dynamically generated
    # or passed from a previous lobe.

    # Create a dummy project structure for testing
    DUMMY_PROJECT_ROOT = Path("./dummy_android_project")
    if DUMMY_PROJECT_ROOT.exists():
        shutil.rmtree(DUMMY_PROJECT_ROOT)
    DUMMY_PROJECT_ROOT.mkdir()

    # Create essential Android project files (minimal for build)
    (DUMMY_PROJECT_ROOT / "settings.gradle").write_text("rootProject.name = 'MyTestApp'")
    (DUMMY_PROJECT_ROOT / "build.gradle").write_text("""
    buildscript {
        repositories {
            google()
            mavenCentral()
        }
        dependencies {
            classpath 'com.android.tools.build:gradle:7.0.0' // Use a compatible version
        }
    }
    allprojects {
        repositories {
            google()
            mavenCentral()
        }
    }
    """)
    (DUMMY_PROJECT_ROOT / "gradlew").write_text("#!/bin/bash\n./gradlew \"$@\"\n")
    (DUMMY_PROJECT_ROOT / "gradlew.bat").write_text("@echo off\ncall gradlew.bat %*\n")
    (DUMMY_PROJECT_ROOT / "gradle" / "wrapper" / "gradle-wrapper.jar").parent.mkdir(parents=True)
    (DUMMY_PROJECT_ROOT / "gradle" / "wrapper" / "gradle-wrapper.properties").write_text("distributionBase=GRADLE_USER_HOME\ndistributionUrl=https\://services.gradle.org/distributions/gradle-7.4.2-bin.zip\ndistributionVersion=7.4.2\n")

    APP_DIR = DUMMY_PROJECT_ROOT / "app"
    APP_DIR.mkdir()
    (APP_DIR / "build.gradle").write_text("""
    plugins {
        id 'com.android.application'
    }

    android {
        namespace 'com.example.mytestapp'
        compileSdk 33

        defaultConfig {
            applicationId "com.example.mytestapp"
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
    }

    dependencies {
        implementation 'androidx.core:core-ktx:1.6.0'
        implementation 'androidx.appcompat:appcompat:1.3.1'
        implementation 'com.google.android.material:material:1.4.0'
        implementation 'androidx.constraintlayout:constraintlayout:2.1.1'
        testImplementation 'junit:junit:4.13.2'
        androidTestImplementation 'androidx.test.ext:junit:1.1.3'
        androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'
    }
    """)
    (APP_DIR / "proguard-rules.pro").write_text("-keep public class *memberNameLink {\n    public *;\n}\n")
    (APP_DIR / "src" / "main" / "AndroidManifest.xml").write_text("""
    <?xml version="1.0" encoding="utf-8"?>
    <manifest xmlns:android="http://schemas.android.com/apk/res/android"
        package="com.example.mytestapp">

        <application
            android:allowBackup="true"
            android:icon="@mipmap/ic_launcher"
            android:label="@string/app_name"
            android:roundIcon="@mipmap/ic_launcher_round"
            android:supportsRtl="true"
            android:theme="@style/Theme.MyTestApp">
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
    (APP_DIR / "src" / "main" / "res" / "layout" / "activity_main.xml").write_text("""
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
    """)
    (APP_DIR / "src" / "main" / "java" / "com" / "example" / "mytestapp" / "MainActivity.kt").write_text("""
    package com.example.mytestapp

    import androidx.appcompat.app.AppCompatActivity
    import android.os.Bundle

    class MainActivity : AppCompatActivity() {
        override fun onCreate(savedInstanceState: Bundle?) {
            super.onCreate(savedInstanceState)
            setContentView(R.layout.activity_main)
        }
    }
    """)
    (APP_DIR / "src" / "main" / "res" / "values" / "strings.xml").write_text("""
    <resources>
        <string name="app_name">MyTestApp</string>
    </resources>
    """)
    (APP_DIR / "src" / "main" / "res" / "values" / "themes.xml").write_text("""
    <resources xmlns:tools="http://schemas.android.com/tools">
        <!-- Base application theme. -->
        <style name="Theme.MyTestApp" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
            <!-- Primary brand color. -->
            <item name="colorPrimary">#6200EE</item>
            <item name="colorPrimaryVariant">#3700B3</item>
            <item name="colorOnPrimary">#FFFFFF</item>
            <!-- Secondary brand color. -->
            <item name="colorSecondary">#03DAC6</item>
            <item name="colorSecondaryVariant">#03DAC6</item>
            <item name="colorOnSecondary">#000000</item>
            <!-- Status bar color. -->
            <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryVariant</item>
            <!-- Customize your theme here. -->
        </style>
    </resources>
    """)

    # Ensure ANDROID_SDK_ROOT is set for the example to run
    if not ANDROID_SDK_ROOT:
        print("Skipping APK build example: ANDROID_SDK_ROOT is not set.")
    else:
        try:
            apk_builder = ApkBuilder(DUMMY_PROJECT_ROOT)
            generated_apk_path = apk_builder.build_apk()
            print(f"\nDemo: APK generated at {generated_apk_path}")

            # Optional: Add a placeholder for further processing of the APK
            # For instance, Lobe 9_apk_analysis_lobe might take this path.

            apk_builder.cleanup_build_artifacts()
            apk_builder.cleanup_mock_keystore() # Clean up the mocked keystore
            print("Demo cleanup finished.")

        except Exception as e:
            print(f"\nDemo failed: {e}")
        finally:
            # Clean up the dummy project
            if DUMMY_PROJECT_ROOT.exists():
                print(f"Removing dummy project directory: {DUMMY_PROJECT_ROOT}")
                shutil.rmtree(DUMMY_PROJECT_ROOT)