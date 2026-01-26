import os
import shutil
import logging
import re
import subprocess
from typing import List, Dict, Tuple

# Assume these are defined elsewhere and accessible
JAVA_PROJECT_DIR = "temp_android_project"
KNOWLEDGE_BASE_DIR = "knowledge_base"
GRADLEW_PATH = os.path.join(JAVA_PROJECT_DIR, "gradlew")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_package_name_from_manifest(manifest_path: str) -> str | None:
    """
    Extracts the package name from an AndroidManifest.xml file.
    """
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Use regex to find the package attribute in the manifest tag
            match = re.search(r'<manifest\s+[^>]*package="([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        logging.error(f"AndroidManifest.xml not found at {manifest_path}")
    except Exception as e:
        logging.error(f"Error reading or parsing {manifest_path}: {e}")
    return None

def create_android_project_structure(project_dir: str, package_name: str, activity_name: str = "MainActivity"):
    """
    Creates a basic Android project directory structure.
    """
    logging.info(f"Creating Android project structure in: {project_dir}")
    os.makedirs(project_dir, exist_ok=True)

    app_dir = os.path.join(project_dir, "app")
    os.makedirs(app_dir, exist_ok=True)

    src_dir = os.path.join(app_dir, "src", "main")
    os.makedirs(src_dir, exist_ok=True)

    manifest_dir = os.path.join(src_dir, "AndroidManifest.xml")
    package_path_parts = package_name.split('.')
    java_package_path = os.path.join(src_dir, "java", *package_path_parts)
    os.makedirs(java_package_path, exist_ok=True)

    # Create a dummy AndroidManifest.xml
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
        <activity android:name=".{activity_name}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(manifest_dir, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    logging.info(f"Created {manifest_dir}")

    # Create a dummy MainActivity.java
    activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()}); // Assuming a layout file

        TextView textView = findViewById(R.id.myTextView); // Assuming a TextView with this ID
        textView.setText("Hello from {activity_name}!");
    }}
}}
"""
    with open(os.path.join(java_package_path, f"{activity_name}.java"), 'w', encoding='utf-8') as f:
        f.write(activity_content)
    logging.info(f"Created {activity_name}.java")

    # Create dummy layout file
    layout_dir = os.path.join(src_dir, "res", "layout")
    os.makedirs(layout_dir, exist_ok=True)
    layout_content = f"""
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/myTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"/>

</LinearLayout>
"""
    with open(os.path.join(layout_dir, f"activity_{activity_name.lower()}.xml"), 'w', encoding='utf-8') as f:
        f.write(layout_content)
    logging.info(f"Created activity_{activity_name.lower()}.xml")

    # Create dummy string resources
    values_dir = os.path.join(src_dir, "res", "values")
    os.makedirs(values_dir, exist_ok=True)
    values_content = """
<resources>
    <string name="app_name">MyArabicApp</string>
</resources>
"""
    with open(os.path.join(values_dir, "strings.xml"), 'w', encoding='utf-8') as f:
        f.write(values_content)
    logging.info("Created strings.xml")

    # Create dummy build.gradle (app level) - very basic
    build_gradle_app_content = """
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace '""" + package_name + """'
    compileSdk 33

    defaultConfig {
        applicationId \"""" + package_name + """\"
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
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {

    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    with open(os.path.join(app_dir, "build.gradle"), 'w', encoding='utf-8') as f:
        f.write(build_gradle_app_content)
    logging.info("Created app/build.gradle")

    # Create dummy settings.gradle
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
rootProject.name = "MyArabicApp"
include ':app'
"""
    with open(os.path.join(project_dir, "settings.gradle"), 'w', encoding='utf-8') as f:
        f.write(settings_gradle_content)
    logging.info("Created settings.gradle")

    # Create dummy build.gradle (project level)
    build_gradle_project_content = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2' // Specify your desired Gradle plugin version
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.20' // Specify your desired Kotlin version
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
"""
    with open(os.path.join(project_dir, "build.gradle"), 'w', encoding='utf-8') as f:
        f.write(build_gradle_project_content)
    logging.info("Created project/build.gradle")

    # Create dummy gradlew and gradlew.bat
    with open(os.path.join(project_dir, "gradlew"), 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\nexec gradle/wrapper/gradle-wrapper.jar \"$@\"\n")
    with open(os.path.join(project_dir, "gradlew.bat"), 'w', encoding='utf-8') as f:
        f.write("@echo off\nif \\\"%~1\\\" == \\\"--stop\\\" ( goto skip )\ncall gradle/wrapper/gradle-wrapper.jar %*\n:skip\n")
    os.makedirs(os.path.join(project_dir, "gradle", "wrapper"), exist_ok=True)
    with open(os.path.join(project_dir, "gradle", "wrapper", "gradle-wrapper.properties"), 'w', encoding='utf-8') as f:
        f.write("distributionBase=GRADLE_USER_HOME\ndistributionUrl=https\\://services.gradle.org/distributions/gradle-7.6-bin.zip\ndistributionPath=wrapper/dists\ngradleVersion=7.6\n")
    logging.info("Created gradlew scripts and wrapper properties.")

def build_android_apk(project_dir: str, gradlew_path: str, task: str = "assembleDebug") -> Tuple[bool, str]:
    """
    Executes the Gradle build command to create an APK.
    Returns a tuple of (success, output_message).
    """
    logging.info(f"Starting Gradle task '{task}' for project in {project_dir}")
    try:
        # Ensure gradlew is executable
        if os.name != 'nt': # Not on Windows
            os.chmod(gradlew_path, 0o755)

        # Use subprocess to run the gradlew command
        # Capturing stdout and stderr for better error reporting
        process = subprocess.Popen(
            [gradlew_path, task],
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            logging.info(f"Gradle task '{task}' completed successfully.")
            logging.debug(f"Gradle stdout:\n{stdout}")
            return True, stdout
        else:
            logging.error(f"Gradle task '{task}' failed with return code {process.returncode}.")
            logging.error(f"Gradle stderr:\n{stderr}")
            logging.error(f"Gradle stdout:\n{stdout}")
            return False, stderr + "\n" + stdout

    except FileNotFoundError:
        logging.error(f"Gradle wrapper not found at {gradlew_path}. Ensure it's generated correctly.")
        return False, f"Gradle wrapper not found at {gradlew_path}."
    except Exception as e:
        logging.error(f"An error occurred during the Gradle build: {e}")
        return False, str(e)

def find_generated_apk(project_dir: str) -> str | None:
    """
    Finds the generated APK file in the project's build output directory.
    Assumes standard Android project structure.
    """
    apk_dir = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")
    if os.path.exists(apk_dir):
        for filename in os.listdir(apk_dir):
            if filename.endswith(".apk"):
                return os.path.join(apk_dir, filename)
    return None

def cleanup_project_artifacts(project_dir: str):
    """
    Cleans up generated build artifacts and the project directory.
    """
    logging.info(f"Cleaning up project directory: {project_dir}")
    if os.path.exists(os.path.join(project_dir, "app", "build")):
        try:
            shutil.rmtree(os.path.join(project_dir, "app", "build"))
            logging.info("Cleaned up app build directory.")
        except OSError as e:
            logging.error(f"Error removing app build directory: {e}")

    # Clean up dummy gradlew and related files if they were created
    dummy_gradlew_path = os.path.join(project_dir, "gradlew")
    if os.path.exists(dummy_gradlew_path):
        try:
            os.remove(dummy_gradlew_path)
            logging.info("Cleaned up dummy gradlew.")
        except OSError as e:
            logging.error(f"Error removing {dummy_gradlew_path}: {e}")

    dummy_gradlew_bat_path = os.path.join(project_dir, "gradlew.bat")
    if os.path.exists(dummy_gradlew_bat_path):
        try:
            os.remove(dummy_gradlew_bat_path)
            logging.info("Cleaned up dummy gradlew.bat.")
        except OSError as e:
            logging.error(f"Error removing {dummy_gradlew_bat_path}: {e}")

    # Optionally remove the entire project directory if it was purely temporary
    # This is risky if it's meant to be kept for inspection.
    # For this demo, we'll assume cleanup of build artifacts is sufficient.
    # If the objective is to create and then delete, uncomment the following:
    # try:
    #     shutil.rmtree(project_dir)
    #     logging.info(f"Removed entire project directory: {project_dir}")
    # except OSError as e:
    #     logging.error(f"Error removing directory {project_dir}: {e}")

class ArabicAndroidModuleBuilder:
    def __init__(self, project_dir: str = JAVA_PROJECT_DIR, knowledge_base_dir: str = KNOWLEDGE_BASE_DIR):
        self.project_dir = project_dir
        self.knowledge_base_dir = knowledge_base_dir
        self.package_name = None
        self.activity_name = "MainActivity" # Default activity name

    def _get_project_details_from_nl(self, natural_language_input: str) -> Dict[str, str]:
        """
        Parses natural language input to extract project details like
        package name and potentially other configurations.
        This is a placeholder for a more sophisticated NLP module.
        For now, it expects a very specific format or uses defaults.
        """
        logging.info(f"Processing NL input for project details: '{natural_language_input}'")
        details = {
            "package_name": "com.example.arabic_generated_app",
            "app_title": "My Arabic App"
        }
        # Very basic extraction - can be expanded significantly
        package_match = re.search(r"package name is ([\w.]+)", natural_language_input, re.IGNORECASE)
        if package_match:
            details["package_name"] = package_match.group(1)

        title_match = re.search(r"app title is \"(.*?)\"", natural_language_input, re.IGNORECASE)
        if title_match:
            details["app_title"] = title_match.group(1)

        logging.info(f"Extracted details: {details}")
        return details

    def _generate_android_manifest(self, package_name: str, app_title: str) -> str:
        """
        Generates the content for AndroidManifest.xml.
        """
        logging.info(f"Generating AndroidManifest.xml content for package: {package_name}, title: {app_title}")
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
        <activity android:name=".{self.activity_name}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        # Update app name in strings.xml content later
        return manifest_content

    def _generate_activity_code(self, package_name: str, activity_name: str, nl_content: str) -> str:
        """
        Generates Java/Kotlin code for the main activity, incorporating NL instructions.
        This is a simplified example. A real system would parse `nl_content` more deeply.
        """
        logging.info(f"Generating activity code for {activity_name} in package {package_name}")
        # Basic logic: find if any Arabic text should be displayed
        display_text_match = re.search(r"display the text \"(.*?)\" in the main activity", nl_content, re.IGNORECASE)
        text_to_display = '"Hello from Arabic Activity!"' # Default
        if display_text_match:
            text_to_display = f'"{display_text_match.group(1)}"'
            logging.info(f"Found specific text to display: {text_to_display}")

        # Placeholder for more complex logic, e.g., dynamically setting layout IDs
        activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Dynamically set layout based on activity name, assuming naming convention
        int layoutId = getResources().getIdentifier("activity_{activity_name.lower()}", "layout", getPackageName());
        if (layoutId != 0) {{
            setContentView(layoutId);
        }} else {{
            // Fallback or error handling if layout not found
            setContentView(R.layout.activity_default); // Assume a default layout exists
            // Or throw an error: throw new RuntimeException("Layout not found for activity: {activity_name}");
        }}

        // Dynamically find TextView by ID, expecting 'myTextView' or similar default
        int textViewId = getResources().getIdentifier("myTextView", "id", getPackageName());
        if (textViewId != 0) {{
            TextView textView = findViewById(textViewId);
            textView.setText({text_to_display});
        }} else {{
            logging.warning("TextView with ID 'myTextView' not found in layout.");
        }}
    }}
}}
"""
        return activity_content

    def _generate_layout_file(self, activity_name: str, nl_content: str) -> str:
        """
        Generates an XML layout file for the activity.
        This can be customized based on NL instructions.
        """
        logging.info(f"Generating layout for activity: {activity_name}")
        # Basic layout with a TextView
        layout_content = f"""
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/myTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading Arabic Content..."
        android:textSize="24sp"/>

</LinearLayout>
"""
        # Example: If NL asked for a Button
        if re.search(r"add a button", nl_content, re.IGNORECASE):
            layout_content = re.sub(r"</LinearLayout>",
                                    """
    <Button
        android:id="@+id/myButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me" />

</LinearLayout>""", layout_content)
            logging.info("Added a button to the layout.")

        return layout_content

    def _generate_strings_xml(self, app_title: str) -> str:
        """
        Generates strings.xml content.
        """
        logging.info(f"Generating strings.xml with app title: {app_title}")
        return f"""
<resources>
    <string name="app_name">{app_title}</string>
</resources>
"""

    def _create_project_files(self, nl_instructions: str):
        """
        Creates the necessary Android project files based on NL instructions.
        """
        project_details = self._get_project_details_from_nl(nl_instructions)
        self.package_name = project_details["package_name"]
        app_title = project_details["app_title"]

        logging.info(f"Creating project structure for package: {self.package_name}")
        os.makedirs(self.project_dir, exist_ok=True)

        app_dir = os.path.join(self.project_dir, "app")
        src_dir = os.path.join(app_dir, "src", "main")
        os.makedirs(src_dir, exist_ok=True)

        # Manifest file
        manifest_path = os.path.join(src_dir, "AndroidManifest.xml")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_android_manifest(self.package_name, app_title))
        logging.info(f"Created {manifest_path}")

        # Java/Kotlin source files
        package_path_parts = self.package_name.split('.')
        java_package_path = os.path.join(src_dir, "java", *package_path_parts)
        os.makedirs(java_package_path, exist_ok=True)

        activity_java_path = os.path.join(java_package_path, f"{self.activity_name}.java")
        with open(activity_java_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_activity_code(self.package_name, self.activity_name, nl_instructions))
        logging.info(f"Created {activity_java_path}")

        # Resource files
        layout_dir = os.path.join(src_dir, "res", "layout")
        os.makedirs(layout_dir, exist_ok=True)
        layout_xml_path = os.path.join(layout_dir, f"activity_{self.activity_name.lower()}.xml")
        with open(layout_xml_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_layout_file(self.activity_name, nl_instructions))
        logging.info(f"Created {layout_xml_path}")

        values_dir = os.path.join(src_dir, "res", "values")
        os.makedirs(values_dir, exist_ok=True)
        strings_xml_path = os.path.join(values_dir, "strings.xml")
        with open(strings_xml_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_strings_xml(app_title))
        logging.info(f"Created {strings_xml_path}")

        # Create dummy build.gradle (app level) - very basic, assuming Android plugin is available
        build_gradle_app_content = """
plugins {
    id 'com.android.application'
}

android {
    namespace '""" + self.package_name + """'
    compileSdk 33

    defaultConfig {
        applicationId \"""" + self.package_name + """\"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
        // Add Arabic support if needed, though not strictly required for basic APK build
        // resConfigs "xxhdpi", "en", "ar"
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
    // Add necessary dependencies, e.g., AppCompat
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    // Add other dependencies as required by your NL instructions or default setup
}
"""
        with open(os.path.join(app_dir, "build.gradle"), 'w', encoding='utf-8') as f:
            f.write(build_gradle_app_content)
        logging.info("Created app/build.gradle")

        # Create basic project-level build.gradle and settings.gradle if they don't exist
        if not os.path.exists(os.path.join(self.project_dir, "build.gradle")):
            build_gradle_project_content = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2' // Example version
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
"""
            with open(os.path.join(self.project_dir, "build.gradle"), 'w', encoding='utf-8') as f:
                f.write(build_gradle_project_content)
            logging.info("Created project/build.gradle")

        if not os.path.exists(os.path.join(self.project_dir, "settings.gradle")):
            settings_gradle_content = f"""
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{app_title.replace('"', '').replace("'", '')}"
include ':app'
"""
            with open(os.path.join(self.project_dir, "settings.gradle"), 'w', encoding='utf-8') as f:
                f.write(settings_gradle_content)
            logging.info("Created settings.gradle")

        # Create dummy gradlew and wrapper files if they don't exist
        gradlew_script_path = os.path.join(self.project_dir, "gradlew")
        gradlew_bat_path = os.path.join(self.project_dir, "gradlew.bat")
        gradle_wrapper_properties_path = os.path.join(self.project_dir, "gradle", "wrapper", "gradle-wrapper.properties")

        if not os.path.exists(gradlew_script_path):
            os.makedirs(os.path.dirname(gradlew_script_path), exist_ok=True)
            with open(gradlew_script_path, 'w', encoding='utf-8') as f:
                f.write("#!/bin/bash\nexec gradle/wrapper/gradle-wrapper.jar \"$@\"\n")
            logging.info("Created gradlew script.")

        if not os.path.exists(gradlew_bat_path):
            os.makedirs(os.path.dirname(gradlew_bat_path), exist_ok=True)
            with open(gradlew_bat_path, 'w', encoding='utf-8') as f:
                f.write("@echo off\nif \\\"%~1\\\" == \\\"--stop\\\" ( goto skip )\ncall gradle/wrapper/gradle-wrapper.jar %*\n:skip\n")
            logging.info("Created gradlew.bat.")

        if not os.path.exists(gradle_wrapper_properties_path):
            os.makedirs(os.path.dirname(gradle_wrapper_properties_path), exist_ok=True)
            with open(gradle_wrapper_properties_path, 'w', encoding='utf-8') as f:
                f.write("distributionBase=GRADLE_USER_HOME\ndistributionUrl=https\\://services.gradle.org/distributions/gradle-7.6-bin.zip\ndistributionPath=wrapper/dists\ngradleVersion=7.6\n")
            logging.info("Created gradle-wrapper.properties.")

    def _build_apk(self) -> Tuple[bool, str]:
        """
        Builds the Android APK using the created project structure and gradlew.
        """
        gradlew_path = os.path.join(self.project_dir, "gradlew")
        if os.name == 'nt': # Windows
            gradlew_path = os.path.join(self.project_dir, "gradlew.bat")

        if not os.path.exists(gradlew_path):
            logging.error(f"Gradle wrapper script not found at {gradlew_path}.")
            return False, f"Gradle wrapper not found at {gradlew_path}."

        # Ensure gradlew is executable on non-Windows systems
        if os.name != 'nt':
            try:
                os.chmod(gradlew_path, 0o755)
            except OSError as e:
                logging.error(f"Failed to make gradlew executable: {e}")
                # Continue, as it might work on some systems without explicit chmod

        success, message = build_android_apk(self.project_dir, gradlew_path, task="assembleDebug")
        return success, message

    def build_module(self, natural_language_instructions: str) -> str | None:
        """
        Orchestrates the creation of Android project files and building the APK.
        Returns the path to the generated APK if successful, otherwise None.
        """
        logging.info("--- Initiating Arabic Android Module Build ---")

        # Clean previous build artifacts if directory exists
        if os.path.exists(self.project_dir):
            logging.warning(f"Project directory '{self.project_dir}' already exists. Cleaning previous artifacts.")
            cleanup_project_artifacts(self.project_dir)
            # Recreate directory structure if it was fully removed by cleanup
            os.makedirs(self.project_dir, exist_ok=True)

        try:
            self._create_project_files(natural_language_instructions)
        except Exception as e:
            logging.error(f"Failed to create Android project files: {e}")
            return None

        logging.info("--- Project structure created. Attempting to build APK ---")
        success, build_output = self._build_apk()

        if success:
            apk_path = find_generated_apk(self.project_dir)
            if apk_path:
                logging.info(f"Successfully built APK: {apk_path}")
                # Optional: Clean up project directory after successful build if desired
                # cleanup_project_artifacts(self.project_dir)
                return apk_path
            else:
                logging.error("APK build succeeded, but APK file not found in expected location.")
                return None
        else:
            logging.error(f"APK build failed. Build output:\n{build_output}")
            # Optional: Clean up project directory even on failure
            # cleanup_project_artifacts(self.project_dir)
            return None

# --- DEMO USAGE ---
if __name__ == "__main__":
    # Example 1: Basic Arabic app
    nl_input_1 = "Create an Android app with package name com.example.arabicdemo. Basic setup."
    builder1 = ArabicAndroidModuleBuilder()
    apk_path1 = builder1.build_module(nl_input_1)
    if apk_path1:
        print(f"\n[DEMO 1] APK generated at: {apk_path1}")
    else:
        print("\n[DEMO 1] APK generation failed.")
    print("\n" + "="*50 + "\n")

    # Example 2: App with specific text and title, potentially adding a button
    nl_input_2 = "Generate an Android app with package name com.arabic.story. The app title should be 'My Arabic Stories'. Display the text 'مرحباً بالعالم' in the main activity. Add a button to the layout."
    builder2 = ArabicAndroidModuleBuilder(project_dir="temp_android_project_stories")
    apk_path2 = builder2.build_module(nl_input_2)
    if apk_path2:
        print(f"\n[DEMO 2] APK generated at: {apk_path2}")
    else:
        print("\n[DEMO 2] APK generation failed.")
    print("\n" + "="*50 + "\n")

    # Example 3: Another custom package name and app title
    nl_input_3 = "Build an Android application. Use package name com.uae.dubai.metro. The application should be titled 'Dubai Metro Guide'."
    builder3 = ArabicAndroidModuleBuilder(project_dir="temp_android_project_dubai")
    apk_path3 = builder3.build_module(nl_input_3)
    if apk_path3:
        print(f"\n[DEMO 3] APK generated at: {apk_path3}")
    else:
        print("\n[DEMO 3] APK generation failed.")
    print("\n" + "="*50 + "\n")

    # Clean up any lingering project directories from the demo if needed
    # print("\n--- Cleaning up demo project directories ---")
    # for dir_name in ["temp_android_project", "temp_android_project_stories", "temp_android_project_dubai"]:
    #     if os.path.exists(dir_name):
    #         try:
    #             shutil.rmtree(dir_name)
    #             print(f"Removed: {dir_name}")
    #         except OSError as e:
    #             print(f"Error removing {dir_name}: {e}")