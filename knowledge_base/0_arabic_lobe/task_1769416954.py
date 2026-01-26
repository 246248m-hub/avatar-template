import os
import shutil
import subprocess
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
JAVA_PROJECT_DIR = "temp_java_project"
GRADLE_WRAPPER_SCRIPT = "gradlew"
MAIN_ACTIVITY_TEMPLATE_PATH = "templates/MainActivity.java.template"
GRADLE_BUILD_GRADLE_TEMPLATE_PATH = "templates/build.gradle.template"
GRADLE_SETTINGS_GRADLE_TEMPLATE_PATH = "templates/settings.gradle.template"
MANIFEST_TEMPLATE_PATH = "templates/AndroidManifest.xml.template"
APP_BUILD_GRADLE_TEMPLATE_PATH = "templates/app_build.gradle.template"

# --- Helper Functions ---

def create_directory_if_not_exists(path):
    """Creates a directory if it does not already exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def copy_template_file(source_path, destination_path):
    """Copies a file from a source template to a destination."""
    try:
        shutil.copyfile(source_path, destination_path)
        logging.info(f"Copied template from {source_path} to {destination_path}")
    except FileNotFoundError:
        logging.error(f"Template file not found: {source_path}")
        raise
    except IOError as e:
        logging.error(f"Error copying file from {source_path} to {destination_path}: {e}")
        raise

def generate_android_project_structure(project_path, app_name="MyApp"):
    """Generates the basic directory structure for an Android project."""
    create_directory_if_not_exists(project_path)

    # Create app module directory
    app_dir = os.path.join(project_path, "app")
    create_directory_if_not_exists(app_dir)

    # Create src/main/java directory structure
    java_dir = os.path.join(app_dir, "src", "main", "java")
    create_directory_if_not_exists(java_dir)

    # Create package directory (e.g., com.example.myapp)
    package_name = f"com.example.{app_name.lower()}"
    package_dir = os.path.join(java_dir, *package_name.split('.'))
    create_directory_if_not_exists(package_dir)

    # Create res directory structure
    res_dir = os.path.join(app_dir, "src", "main", "res")
    create_directory_if_not_exists(os.path.join(res_dir, "layout"))
    create_directory_if_not_exists(os.path.join(res_dir, "mipmap-hdpi"))
    create_directory_if_not_exists(os.path.join(res_dir, "mipmap-mdpi"))
    create_directory_if_not_exists(os.path.join(res_dir, "mipmap-xhdpi"))
    create_directory_if_not_exists(os.path.join(res_dir, "mipmap-xxhdpi"))
    create_directory_if_not_exists(os.path.join(res_dir, "mipmap-xxxhdpi"))
    create_directory_if_not_exists(os.path.join(res_dir, "values"))

    logging.info(f"Generated Android project structure for '{app_name}' at {project_path}")
    return package_name, package_dir

def create_android_manifest(manifest_path, package_name, app_name):
    """Creates the AndroidManifest.xml file."""
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
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
    logging.info(f"Created AndroidManifest.xml at {manifest_path}")

def create_main_activity(activity_path, package_name, app_name):
    """Creates the MainActivity.java file."""
    activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assumes activity_main.xml exists

        // Example: Displaying a welcome message
        TextView welcomeText = findViewById(R.id.welcome_text_view); // Assumes a TextView with this ID
        welcomeText.setText("Welcome to {app_name}!");
    }}
}}
"""
    with open(activity_path, "w", encoding="utf-8") as f:
        f.write(activity_content)
    logging.info(f"Created MainActivity.java at {activity_path}")

def create_layout_file(layout_path, app_name):
    """Creates a simple activity_main.xml layout file."""
    layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout_content)
    logging.info(f"Created activity_main.xml at {layout_path}")

def create_values_files(values_dir):
    """Creates strings.xml and styles.xml."""
    strings_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">MyApp</string>
</resources>
"""
    with open(os.path.join(values_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_content)
    logging.info(f"Created strings.xml at {values_dir}")

    styles_content = """<resources>
    <!-- Base application theme. -->
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
    </style>
</resources>
"""
    with open(os.path.join(values_dir, "styles.xml"), "w", encoding="utf-8") as f:
        f.write(styles_content)
    logging.info(f"Created styles.xml at {values_dir}")

    colors_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#008577</color>
    <color name="colorPrimaryDark">#005F53</color>
    <color name="colorAccent">#D81B60</color>
</resources>
"""
    with open(os.path.join(values_dir, "colors.xml"), "w", encoding="utf-8") as f:
        f.write(colors_content)
    logging.info(f"Created colors.xml at {values_dir}")


def create_gradle_files(project_path, app_name):
    """Creates the main build.gradle and settings.gradle files."""
    settings_gradle_content = f"""rootProject.name = "{app_name}"
include ':app'
"""
    with open(os.path.join(project_path, "settings.gradle"), "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)
    logging.info(f"Created settings.gradle at {project_path}")

    build_gradle_content = """allprojects {
    repositories {
        google()
        mavenCentral()
        jcenter() // Deprecated but often still needed for older dependencies
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
"""
    with open(os.path.join(project_path, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(build_gradle_content)
    logging.info(f"Created root build.gradle at {project_path}")

def create_app_build_gradle(app_dir, package_name, app_name):
    """Creates the app's build.gradle file."""
    app_build_gradle_content = f"""plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // If you plan to use Kotlin later
}}

android {{
    namespace '{package_name}'
    compileSdk 34 // Use a recent SDK version

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
    // If using Kotlin, uncomment the following:
    // kotlinOptions {{
    //     jvmTarget = '1.8'
    // }}
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
    with open(os.path.join(app_dir, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(app_build_gradle_content)
    logging.info(f"Created app/build.gradle at {app_dir}")

def create_gradlew_files(project_path):
    """Creates gradlew and gradlew.bat files."""
    gradlew_content = """#!/usr/bin/env bash

APP_NAME="$(basename "$0")"
APP_HOME="$(cd "$(dirname "$0")" && pwd)"

DEFAULT_JVMARGS=""

# Look for a JAVA_HOME environment variable and use it if set.
if [ -z "$JAVA_HOME" ] ; then
    JAVA_HOME="$PWD/../.gradle/wrapper/dists/gradle-8.5-bin/..." # Placeholder, needs actual path from downloaded gradle
else
    # If JAVA_HOME is set, use it.
    JAVA="$JAVA_HOME/bin/java"
    if [ ! -x "$JAVA" ] ; then
        echo "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME"
        exit 1
    fi
fi

# Prefer a bundled JVM if available.
if [ -z "$JAVA_HOME" ] && [ -f "$APP_HOME/../.gradle/wrapper/dists/gradle-8.5-bin/.../bin/java" ]; then # Placeholder
    JAVA="$APP_HOME/../.gradle/wrapper/dists/gradle-8.5-bin/.../bin/java" # Placeholder
elif [ -z "$JAVA_HOME" ] && [ -f "$APP_HOME/gradle/wrapper/your_gradle_version/bin/java" ]; then # Placeholder
    JAVA="$APP_HOME/gradle/wrapper/your_gradle_version/bin/java" # Placeholder
fi


# Use the java executable found.
# Note: If JAVA_HOME is not set, then the JAVA_HOME path below will be empty,
# and the script will fail if it cannot find a java executable in the PATH.
if [ -z "$JAVA" ] ; then
  JAVA="java"
fi

# Uncomment this line if you want to move to a different working directory
# cd
# Uncomment this line if you want to change the JVM arguments
# JVM_ARGS="-Xmx64m -Xms64m $DEFAULT_JVMARGS"

"$JAVA" $JVM_ARGS -cp "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"
"""
    # Note: The gradlew script generation is complex due to needing the actual Gradle wrapper JAR.
    # For a functional example, you would typically download the wrapper distribution and
    # use its `gradlew` script directly or adapt this to download it.
    # This is a simplified representation. A robust solution would involve the Gradle wrapper task.

    # Placeholder for the actual gradlew script. A real implementation would download the wrapper.
    logging.warning("Placeholder gradlew script created. A real implementation would download the Gradle wrapper.")
    with open(os.path.join(project_path, GRADLE_WRAPPER_SCRIPT), "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\n# Placeholder for gradlew script. Real implementation required.\nexit 1\n") # Make it non-executable by default until proper generation
    logging.info(f"Created placeholder {GRADLE_WRAPPER_SCRIPT} at {project_path}")

    gradlew_bat_content = """@echo off
if "%DEBUG%_JAVA_CMD%" == "" (
    set JAVA_CMD=java
) else (
    set JAVA_CMD=%DEBUG%_JAVA_CMD%
)

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=Gradle
set REMAINING_ARGS=%*

"%JAVA_HOME%\bin\java.exe" %JAVA_OPTS% -cp "%DIRNAME%\gradle\wrapper\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %REMAINING_ARGS%
"""
    with open(os.path.join(project_path, f"{GRADLE_WRAPPER_SCRIPT}.bat"), "w", encoding="utf-8") as f:
        f.write(gradlew_bat_content)
    logging.info(f"Created {GRADLE_WRAPPER_SCRIPT}.bat at {project_path}")


def build_apk_module(natural_language_input, output_directory="generated_apks"):
    """
    Builds a functional Python module for generating basic Android APK structures
    from natural language descriptions.

    This module will:
    1. Parse simplified natural language input to extract app name and basic components.
    2. Generate the necessary directory structure for an Android project.
    3. Create essential Android files (AndroidManifest.xml, MainActivity.java, build.gradle, etc.).
    4. Prepare for APK compilation (though actual compilation requires an Android SDK).
    """
    logging.info(f"--- Initiating APK Generation Module ---")
    logging.info(f"Processing natural language input: '{natural_language_input}'")

    # --- Simplified NLP Parsing ---
    # In a real scenario, this would involve advanced NLP to understand user intent,
    # desired features, UI elements, etc. Here, we'll use a very basic approach.

    app_name = "GeneratedApp"
    if "app named" in natural_language_input.lower():
        parts = natural_language_input.lower().split("app named")
        if len(parts) > 1:
            app_name_candidate = parts[1].strip().split(' ')[0] # Take first word after "app named"
            if app_name_candidate:
                app_name = app_name_candidate.capitalize()

    logging.info(f"Deduced App Name: {app_name}")

    # --- Project Setup ---
    project_path = os.path.join(output_directory, f"{app_name.lower()}_project")
    create_directory_if_not_exists(output_directory)
    create_directory_if_not_exists(project_path)

    # Generate the basic Android project structure
    package_name, package_dir = generate_android_project_structure(project_path, app_name)

    # Define file paths
    manifest_path = os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml")
    activity_path = os.path.join(package_dir, "MainActivity.java")
    layout_dir = os.path.join(project_path, "app", "src", "main", "res", "layout")
    layout_path = os.path.join(layout_dir, "activity_main.xml")
    values_dir = os.path.join(project_path, "app", "src", "main", "res", "values")
    app_dir = os.path.join(project_path, "app")

    # Create essential Android files
    create_android_manifest(manifest_path, package_name, app_name)
    create_main_activity(activity_path, package_name, app_name)
    create_layout_file(layout_path, app_name)
    create_values_files(values_dir)

    # Create Gradle build files
    create_gradle_files(project_path, app_name)
    create_app_build_gradle(app_dir, package_name, app_name)
    create_gradlew_files(project_path) # This will create placeholder files

    logging.info(f"Basic Android project structure and files generated for '{app_name}' at: {project_path}")

    # --- APK Compilation Preparation ---
    # To actually compile an APK, you would need:
    # 1. A properly set up Android SDK.
    # 2. The Java Development Kit (JDK).
    # 3. The Gradle wrapper to be functional (downloaded and configured).
    # 4. Execute the Gradle build command (e.g., ./gradlew assembleDebug).

    logging.info("--- APK Generation Module Finished ---")
    logging.info("Next steps would involve setting up the Android SDK and running Gradle build commands.")
    logging.info(f"Project generated at: {project_path}")
    return project_path

# Example Usage (demonstrates the module's functionality)
if __name__ == '__main__':
    # Simulate a natural language input for an Arabic app
    arabic_app_description = "Create an Android application named 'AlifApp' for demonstrating Arabic text rendering."

    # Call the module
    generated_project_path = build_apk_module(arabic_app_description)

    print(f"\n--- APK Module Demo Complete ---")
    print(f"Generated project structure at: {generated_project_path}")
    print("To build the APK, you would need to:")
    print("1. Install the Android SDK.")
    print("2. Ensure the Gradle wrapper is functional (downloaded correctly).")
    print("3. Navigate to the project directory and run: ./gradlew assembleDebug")
    print("\nThis module focuses on generating the project structure and essential files.")

    # Clean up dummy files and directories created by this module
    print("\n--- Cleaning up generated APK project ---")
    try:
        if os.path.exists(generated_project_path):
            shutil.rmtree(generated_project_path)
            logging.info(f"Removed generated project directory: {generated_project_path}")
        if os.path.exists("generated_apks"):
            # Remove the parent directory if it's empty after removing the app project
            if not os.listdir("generated_apks"):
                os.rmdir("generated_apks")
                logging.info("Removed empty 'generated_apks' directory.")
    except OSError as e:
        logging.error(f"Error during cleanup: {e}")