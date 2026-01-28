import os
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AndroidProjectBuilder:
    def __init__(self, project_root="android_project"):
        self.project_root = Path(project_root)
        self.app_name = "MyApp" # Default app name
        self.package_name = "com.example.myapp" # Default package name

    def create_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        logging.info(f"Creating project structure at: {self.project_root}")
        self.project_root.mkdir(parents=True, exist_ok=True)

        # Manifest
        manifest_dir = self.project_root / "app" / "src" / "main"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        self.create_manifest_file(manifest_dir)

        # Java/Kotlin source
        src_dir = manifest_dir / "java" / self.package_name.replace('.', '/')
        src_dir.mkdir(parents=True, exist_ok=True)
        self.create_main_activity_file(src_dir)

        # Resources
        res_dir = self.project_root / "app" / "src" / "main" / "res"
        res_dir.mkdir(parents=True, exist_ok=True)
        self.create_layout_files(res_dir / "layout")
        self.create_values_files(res_dir / "values")

        # Gradle files
        self.create_build_gradle_app()
        self.create_build_gradle_project()
        self.create_settings_gradle()
        self.create_gradle_wrapper()

        logging.info("Project structure created successfully.")

    def create_manifest_file(self, manifest_dir: Path):
        """Creates a basic AndroidManifest.xml file."""
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{self.app_name}">

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
        manifest_path = manifest_dir / "AndroidManifest.xml"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        logging.info(f"Created {manifest_path}")

    def create_main_activity_file(self, src_dir: Path):
        """Creates a basic MainActivity.java file."""
        activity_content = f"""package {self.package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
"""
        activity_path = src_dir / "MainActivity.java"
        with open(activity_path, "w", encoding="utf-8") as f:
            f.write(activity_content)
        logging.info(f"Created {activity_path}")

    def create_layout_files(self, layout_dir: Path):
        """Creates a basic activity_main.xml file."""
        layout_dir.mkdir(parents=True, exist_ok=True)
        layout_content = """<?xml version="1.0" encoding="utf-8"?>
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
"""
        layout_path = layout_dir / "activity_main.xml"
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content)
        logging.info(f"Created {layout_path}")

    def create_values_files(self, values_dir: Path):
        """Creates basic strings.xml and themes.xml files."""
        values_dir.mkdir(parents=True, exist_ok=True)

        strings_content = """<resources>
    <string name="app_name">%s</string>
</resources>
""" % self.app_name
        strings_path = values_dir / "strings.xml"
        with open(strings_path, "w", encoding="utf-8") as f:
            f.write(strings_content)
        logging.info(f"Created {strings_path}")

        theme_content = """<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.%s" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <!-- Primary brand color. -->
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryVariant</item>
        <!-- Customize your theme here. -->
    </style>

    <!-- Define colors here -->
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
""" % self.app_name
        theme_path = values_dir / "themes.xml"
        with open(theme_path, "w", encoding="utf-8") as f:
            f.write(theme_content)
        logging.info(f"Created {theme_path}")

    def create_build_gradle_app(self):
        """Creates the app-level build.gradle file."""
        app_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming potential future Kotlin use
}

android {
    compileSdk 33 // Using a recent SDK version

    defaultConfig {
        applicationId "%s"
        minSdk 21 // Minimum SDK version
        targetSdk 33 // Target SDK version
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
    // For Kotlin projects
    // kotlinOptions {
    //     jvmTarget = '1.8'
    // }
}

dependencies {

    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""" % self.package_name
        app_gradle_path = self.project_root / "app" / "build.gradle"
        app_gradle_path.parent.mkdir(parents=True, exist_ok=True)
        with open(app_gradle_path, "w", encoding="utf-8") as f:
            f.write(app_gradle_content)
        logging.info(f"Created {app_gradle_path}")

    def create_build_gradle_project(self):
        """Creates the project-level build.gradle file."""
        project_gradle_content = """// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.0' apply false // Matching Kotlin version
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
"""
        project_gradle_path = self.project_root / "build.gradle"
        with open(project_gradle_path, "w", encoding="utf-8") as f:
            f.write(project_gradle_content)
        logging.info(f"Created {project_gradle_path}")

    def create_settings_gradle(self):
        """Creates the settings.gradle file."""
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

rootProject.name = "{self.app_name.lower()}"
include ':app'
"""
        settings_gradle_path = self.project_root / "settings.gradle"
        with open(settings_gradle_path, "w", encoding="utf-8") as f:
            f.write(settings_gradle_content)
        logging.info(f"Created {settings_gradle_path}")

    def create_gradle_wrapper(self):
        """Creates the Gradle wrapper files."""
        wrapper_dir = self.project_root / "gradle" / "wrapper"
        wrapper_dir.mkdir(parents=True, exist_ok=True)

        gradle_wrapper_properties_content = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5.1-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
        gradle_wrapper_properties_path = wrapper_dir / "gradle-wrapper.properties"
        with open(gradle_wrapper_properties_path, "w", encoding="utf-8") as f:
            f.write(gradle_wrapper_properties_content)
        logging.info(f"Created {gradle_wrapper_properties_path}")

        # Create gradlew scripts
        gradlew_content = """#!/bin/sh

"$

            echo "ERROR: JAVA_HOME is not set.  Please set the JAVA_HOME environment variable
            to point to the Java Development Kit installation."

            exit 1
        fi
    fi
fi

baseDir=$(dirname "$0")

# Add execution permissions for gradlew script
chmod +x "$baseDir/gradlew"

# Execute Gradle wrapper
exec "$baseDir/gradlew" "$@"
"""
        # Create gradlew (Unix)
        gradlew_path = self.project_root / "gradlew"
        with open(gradlew_path, "w", encoding="utf-8") as f:
            f.write(gradlew_content.replace('"$JAVA_HOME"', '$JAVA_HOME')) # Fix for escaped var
        os.chmod(gradlew_path, 0o755) # Make it executable
        logging.info(f"Created {gradlew_path}")

        # Create gradlew.bat (Windows)
        gradlew_bat_content = """@if "%~1" == "" goto init
@rem Check for JAVA_HOME or fallback to default java
@if "%JAVA_HOME%" == "" goto fallback
@rem Execute Gradle wrapper
call "%~dp0gradlew.bat" %*
goto end

:fallback
@rem Try to find java
set JAVA_EXE=java.exe
call :findJavaExecutable
if "%JAVA_EXE%" == "" (
    echo ERROR: JAVA_HOME is not set and java.exe could not be found.
    echo Please set the JAVA_HOME environment variable to point to your JDK installation.
    exit /b 1
)
@rem Execute Gradle wrapper with found java
call "%~dp0gradlew.bat" %*
goto end

:init
@rem Initialize JAVA_HOME for first execution
set JAVA_HOME=
call :fallback

:findJavaExecutable
@rem Search for java.exe in common JDK locations
set JAVA_PATH=%JAVA_HOME%\bin
if exist "%JAVA_PATH%\%JAVA_EXE%" goto :eof
set JAVA_PATH=C:\Program Files\Java
for /d %%i in ("%JAVA_PATH%\jdk*") do (
    if exist "%%i\bin\%JAVA_EXE%" (
        set JAVA_HOME=%%i
        set JAVA_EXE=%%i\bin\%JAVA_EXE%
        goto :eof
    )
)
set JAVA_PATH=C:\Program Files (x86)\Java
for /d %%i in ("%JAVA_PATH%\jdk*") do (
    if exist "%%i\bin\%JAVA_EXE%" (
        set JAVA_HOME=%%i
        set JAVA_EXE=%%i\bin\%JAVA_EXE%
        goto :eof
    )
)
set JAVA_EXE=

:end
"""
        gradlew_bat_path = self.project_root / "gradlew.bat"
        with open(gradlew_bat_path, "w", encoding="utf-8") as f:
            f.write(gradlew_bat_content)
        logging.info(f"Created {gradlew_bat_path}")


    def build_apk(self):
        """Builds the APK using Gradle wrapper. Assumes project structure is ready."""
        logging.info("Starting APK build process...")
        if not self.project_root.exists():
            logging.error("Project root does not exist. Please create project structure first.")
            return None

        gradlew_command = "./gradlew" if os.name != 'nt' else "gradlew.bat"
        build_command = [os.path.join(self.project_root, gradlew_command), "assembleDebug"]

        try:
            logging.info(f"Executing build command: {' '.join(build_command)}")
            # Use a dictionary to pass environment variables, especially JAVA_HOME if needed
            env = os.environ.copy()
            # Ensure JAVA_HOME is set if not already
            if 'JAVA_HOME' not in env or not env['JAVA_HOME']:
                logging.warning("JAVA_HOME environment variable not set. Trying to find a default.")
                # This is a basic attempt; a more robust solution might be needed
                try:
                    java_home_path = subprocess.check_output(['where', 'java'], text=True).strip().split(os.sep)[:-1]
                    env['JAVA_HOME'] = os.sep.join(java_home_path)
                    logging.info(f"JAVA_HOME set to: {env['JAVA_HOME']}")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    logging.error("Could not automatically detect JAVA_HOME. Please set it manually.")
                    return None

            process = subprocess.Popen(build_command, cwd=self.project_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                logging.info("APK build successful.")
                apk_path = self.find_generated_apk()
                if apk_path:
                    logging.info(f"Generated APK found at: {apk_path}")
                    return apk_path
                else:
                    logging.error("APK build completed, but could not locate the generated APK file.")
                    return None
            else:
                logging.error(f"APK build failed. Return code: {process.returncode}")
                logging.error("--- STDERR ---")
                logging.error(stderr.decode('utf-8', errors='ignore'))
                logging.error("--- STDOUT ---")
                logging.error(stdout.decode('utf-8', errors='ignore'))
                return None
        except FileNotFoundError:
            logging.error(f"'{gradlew_command}' not found. Make sure it's in the project root and executable.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred during APK build: {e}")
            return None

    def find_generated_apk(self):
        """Finds the generated debug APK file."""
        # The path to the APK file can vary slightly based on Gradle version and build type
        # We'll look in the standard location for debug builds
        debug_apk_dir = self.project_root / "app" / "build" / "outputs" / "apk" / "debug"
        if debug_apk_dir.exists():
            for apk_file in debug_apk_dir.glob("*.apk"):
                if "app-debug" in str(apk_file): # Heuristic to find the main debug APK
                    return apk_file
        return None

    def cleanup_project(self):
        """Cleans up the generated project files."""
        logging.info(f"Cleaning up project directory: {self.project_root}")
        if self.project_root.exists():
            import shutil
            try:
                shutil.rmtree(self.project_root)
                logging.info("Project directory cleaned up successfully.")
            except OSError as e:
                logging.error(f"Error cleaning up project directory: {e}")
        else:
            logging.warning("Project directory does not exist, nothing to clean.")

# Example Usage (for demonstration purposes, this code will not be executed directly by the system)
if __name__ == "__main__":
    # This section is for manual testing and would not be part of the Lobe's output.
    # The Lobe's output is the class definition itself.

    builder = AndroidProjectBuilder(project_root="temp_android_project_arabic")
    builder.app_name = "MyArabicApp"
    builder.package_name = "com.example.myarabicapp"

    print("--- Building Arabic APK Example ---")
    try:
        builder.create_project_structure()
        apk_path = builder.build_apk()

        if apk_path:
            print(f"\nSUCCESS: APK generated at: {apk_path}")
        else:
            print("\nFAILURE: APK generation failed.")

    finally:
        builder.cleanup_project()
    print("\n--- Arabic APK Example Finished ---")