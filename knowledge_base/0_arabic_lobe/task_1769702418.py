import os
import re
import shutil
import subprocess
from typing import Dict, List, Optional, Tuple

# --- Constants ---
SIMULATED_PROJECT_ROOT = "simulated_apk_project"
ANDROID_MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
MAIN_ACTIVITY_JAVA_TEMPLATE = """package {package_name};

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
ACTIVITY_MAIN_XML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/greetingTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
GRADLE_PROPERTIES_TEMPLATE = """systemProp.android.isInstrumentationTestRunnerInvoked=true
systemProp.user.language=en
systemProp.user.region=US
"""
BUILD_GRADLE_TEMPLATE = """plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 24
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

    implementation 'androidx.core:core-ktx:1.10.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
SETTINGS_GRADLE_TEMPLATE = """pluginManagement {{
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

rootProject.name = "MyApplication"
include ':app'
"""

class CodeGenerationLobe:
    """
    This lobe is responsible for generating the foundational structure of an Android APK
    based on natural language descriptions, specifically focusing on Arabic text integration.
    It creates the necessary directory structure, manifest, activity files, and build scripts.
    """

    def __init__(self, project_root: str = SIMULATED_PROJECT_ROOT):
        self.project_root = project_root
        self.app_module_path = os.path.join(self.project_root, "app")
        self.manifest_path = os.path.join(self.app_module_path, "src", "main", "AndroidManifest.xml")
        self.java_path = os.path.join(self.app_module_path, "src", "main", "java")
        self.res_path = os.path.join(self.app_module_path, "src", "main", "res")
        self.layout_path = os.path.join(self.res_path, "layout")
        self.values_path = os.path.join(self.res_path, "values")
        self.gradle_build_path = os.path.join(self.app_module_path, "build.gradle")
        self.gradle_properties_path = os.path.join(self.project_root, "gradle.properties")
        self.settings_gradle_path = os.path.join(self.project_root, "settings.gradle")

    def _create_directory_structure(self, package_name: str):
        """Creates the standard Android project directory structure."""
        os.makedirs(self.app_module_path, exist_ok=True)
        java_package_path = os.path.join(self.java_path, *package_name.split('.'))
        os.makedirs(java_package_path, exist_ok=True)
        os.makedirs(self.layout_path, exist_ok=True)
        os.makedirs(self.values_path, exist_ok=True)
        print(f"Created project structure in: {self.project_root}")

    def _write_file(self, filepath: str, content: str):
        """Writes content to a given file path."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_android_manifest(self, package_name: str):
        """Generates the AndroidManifest.xml file."""
        content = ANDROID_MANIFEST_TEMPLATE.format(package_name=package_name)
        self._write_file(self.manifest_path, content)
        print(f"Generated: {self.manifest_path}")

    def _generate_main_activity_java(self, package_name: str):
        """Generates the MainActivity.java file."""
        content = MAIN_ACTIVITY_JAVA_TEMPLATE.format(package_name=package_name)
        java_package_path = os.path.join(self.java_path, *package_name.split('.'))
        self._write_file(os.path.join(java_package_path, "MainActivity.java"), content)
        print(f"Generated: {os.path.join(java_package_path, 'MainActivity.java')}")

    def _generate_activity_main_xml(self):
        """Generates the activity_main.xml file."""
        content = ACTIVITY_MAIN_XML_TEMPLATE
        self._write_file(os.path.join(self.layout_path, "activity_main.xml"), content)
        print(f"Generated: {os.path.join(self.layout_path, 'activity_main.xml')}")

    def _generate_build_gradle(self, package_name: str):
        """Generates the app/build.gradle file."""
        content = BUILD_GRADLE_TEMPLATE.format(package_name=package_name)
        self._write_file(self.gradle_build_path, content)
        print(f"Generated: {self.gradle_build_path}")

    def _generate_gradle_properties(self):
        """Generates the gradle.properties file."""
        content = GRADLE_PROPERTIES_TEMPLATE
        self._write_file(self.gradle_properties_path, content)
        print(f"Generated: {self.gradle_properties_path}")

    def _generate_settings_gradle(self):
        """Generates the settings.gradle file."""
        content = SETTINGS_GRADLE_TEMPLATE
        self._write_file(self.settings_gradle_path, content)
        print(f"Generated: {self.settings_gradle_path}")

    def _clean_project_directory(self):
        """Removes the simulated project directory if it exists."""
        if os.path.exists(self.project_root):
            shutil.rmtree(self.project_root)
            print(f"Cleaned up existing project directory: {self.project_root}")

    def generate_apk_structure(self, package_name: str = "com.example.arabicapp") -> bool:
        """
        Generates the foundational Android project structure for an APK.

        Args:
            package_name: The package name for the Android application.

        Returns:
            True if the structure was generated successfully, False otherwise.
        """
        self._clean_project_directory()
        try:
            self._create_directory_structure(package_name)
            self._generate_android_manifest(package_name)
            self._generate_main_activity_java(package_name)
            self._generate_activity_main_xml()
            self._generate_build_gradle(package_name)
            self._generate_gradle_properties()
            self._generate_settings_gradle()
            print("Android APK structure generated successfully.")
            return True
        except Exception as e:
            print(f"Error generating APK structure: {e}")
            return False

    def integrate_arabic_text_elements(self, arabic_text_elements: Dict[str, str]) -> bool:
        """
        Integrates specific Arabic text elements into the APK structure,
        primarily by modifying layout files and string resources.

        Args:
            arabic_text_elements: A dictionary where keys are resource names (e.g., "greetingTextView")
                                  and values are the Arabic strings to be displayed.

        Returns:
            True if integration was successful, False otherwise.
        """
        # For simplicity, this example modifies activity_main.xml.
        # A more robust implementation would involve generating string resources.
        activity_main_path = os.path.join(self.layout_path, "activity_main.xml")
        if not os.path.exists(activity_main_path):
            print(f"Error: Layout file not found at {activity_main_path}")
            return False

        try:
            with open(activity_main_path, "r", encoding="utf-8") as f:
                content = f.read()

            for view_id, arabic_string in arabic_text_elements.items():
                # Simple regex to find the TextView with the corresponding ID and update its text attribute
                # This is a basic example and might need more sophisticated parsing for complex layouts.
                pattern = re.compile(
                    rf'(<TextView\s+android:id="@+id/{re.escape(view_id)}"[^>]*?)'
                    rf'android:text="[^"]*"(.*?>)',
                    re.DOTALL
                )
                repl = rf'\1android:text="{re.escape(arabic_string)}"\2'
                content = pattern.sub(repl, content)

            # Create strings.xml for actual string resource management (better practice)
            strings_xml_content = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            for key, value in arabic_text_elements.items():
                # Sanitize key for XML attribute name
                string_name = re.sub(r'[^a-zA-Z0-9_]', '_', key).lower()
                strings_xml_content += f'    <string name="{string_name}">{value}</string>\n'
            strings_xml_content += '</resources>'
            self._write_file(os.path.join(self.values_path, "strings.xml"), strings_xml_content)
            print(f"Generated: {os.path.join(self.values_path, 'strings.xml')}")

            # Update activity_main.xml to reference the string resources
            content_with_string_refs = '<?xml version="1.0" encoding="utf-8"?>\n'
            content_with_string_refs += '<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"\n'
            content_with_string_refs += '    xmlns:app="http://schemas.android.com/apk/res-auto"\n'
            content_with_string_refs += '    xmlns:tools="http://schemas.android.com/tools"\n'
            content_with_string_refs += '    android:layout_width="match_parent"\n'
            content_with_string_refs += '    android:layout_height="match_parent"\n'
            content_with_string_refs += '    tools:context=".MainActivity">\n\n'

            for view_id, arabic_string in arabic_text_elements.items():
                string_name = re.sub(r'[^a-zA-Z0-9_]', '_', view_id).lower()
                content_with_string_refs += f'    <TextView\n'
                content_with_string_refs += f'        android:id="@+id/{view_id}"\n'
                content_with_string_refs += f'        android:layout_width="wrap_content"\n'
                content_with_string_refs += f'        android:layout_height="wrap_content"\n'
                content_with_string_refs += f'        android:text="@string/{string_name}"\n' # Reference string resource
                content_with_string_refs += f'        app:layout_constraintBottom_toBottomOf="parent"\n'
                content_with_string_refs += f'        app:layout_constraintEnd_toEndOf="parent"\n'
                content_with_string_refs += f'        app:layout_constraintStart_toStartOf="parent"\n'
                content_with_string_refs += f'        app:layout_constraintTop_toTopOf="parent" />\n\n'
            content_with_string_refs += '</androidx.constraintlayout.widget.ConstraintLayout>'

            self._write_file(activity_main_path, content_with_string_refs)
            print(f"Integrated Arabic text into: {activity_main_path}")
            return True
        except Exception as e:
            print(f"Error integrating Arabic text: {e}")
            return False

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Starting Code Generation Lobe Demo ---")

    # Clean up any previous runs
    if os.path.exists(SIMULATED_PROJECT_ROOT):
        shutil.rmtree(SIMULATED_PROJECT_ROOT)
        print(f"Cleaned up previous project directory: {SIMULATED_PROJECT_ROOT}")

    # Initialize the Code Generation Lobe
    code_gen_lobe = CodeGenerationLobe()

    # Define Arabic text and corresponding view IDs
    arabic_content_mapping = {
        "welcomeMessage": "مرحباً بالعالم",
        "instructionText": "أدخل اسمك أدناه"
    }

    # Step 1: Generate the basic APK structure
    print("\n--- Generating basic APK structure ---")
    package_name = "com.arabic.translator"
    structure_generated = code_gen_lobe.generate_apk_structure(package_name)

    if structure_generated:
        print("Basic APK structure generated successfully.")

        # Step 2: Integrate Arabic text elements
        print("\n--- Integrating Arabic text elements ---")
        integration_successful = code_gen_lobe.integrate_arabic_text_elements(arabic_content_mapping)

        if integration_successful:
            print("Arabic text elements integrated successfully.")
            print(f"\nSimulated APK project created at: {os.path.abspath(SIMULATED_PROJECT_ROOT)}")
            print("You can now find the generated project files in the 'simulated_apk_project' directory.")
            print("To build the APK, you would typically use Android Studio or the Gradle command-line tool.")
            print("\nExample command to build (requires Android SDK and Gradle installed):")
            print(f"cd {SIMULATED_PROJECT_ROOT}")
            print("chmod +x gradlew")
            print("./gradlew assembleDebug")
        else:
            print("Failed to integrate Arabic text elements.")
    else:
        print("Failed to generate basic APK structure.")

    print("\n--- Code Generation Lobe Demo Finished ---")