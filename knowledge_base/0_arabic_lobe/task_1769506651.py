import os
import subprocess
import shutil
from pathlib import Path

# Define constants for clarity and maintainability
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
TARGET_PACKAGE_NAME = "com.example.generatedapp"
TARGET_ACTIVITY_NAME = "MainActivity"
APP_NAME = "GeneratedApp"
BUILD_GRADLE_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle"
MANIFEST_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml"
MAIN_ACTIVITY_JAVA_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / TARGET_PACKAGE_NAME.replace('.', os.sep) / f"{TARGET_ACTIVITY_NAME}.java"
STRINGS_XML_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "values" / "strings.xml"

class ApkGenerator:
    """
    A module responsible for generating hyper-efficient APKs from natural language prompts,
    focusing on Arabic language understanding and integration with Android development tools.
    """

    def __init__(self, output_dir="generated_apks"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_root = None

    def _setup_android_project(self, project_name: str, package_name: str, activity_name: str, app_name: str):
        """
        Sets up a new Android project directory structure based on a template.
        Replaces placeholders in build.gradle, AndroidManifest.xml, and the main activity file.
        """
        if not ANDROID_PROJECT_TEMPLATE_DIR.exists():
            raise FileNotFoundError("Android project template directory not found. Please create it.")

        self.project_root = self.output_dir / project_name
        if self.project_root.exists():
            shutil.rmtree(self.project_root)
        shutil.copytree(ANDROID_PROJECT_TEMPLATE_DIR, self.project_root)

        # --- Modify build.gradle ---
        with open(self.project_root / "app" / "build.gradle", "r") as f:
            build_gradle_content = f.read()
        build_gradle_content = build_gradle_content.replace("com.example.generatedapp", package_name)
        build_gradle_content = build_gradle_content.replace("GeneratedApp", app_name)
        with open(self.project_root / "app" / "build.gradle", "w") as f:
            f.write(build_gradle_content)

        # --- Modify AndroidManifest.xml ---
        with open(self.project_root / "app" / "src" / "main" / "AndroidManifest.xml", "r") as f:
            manifest_content = f.read()
        manifest_content = manifest_content.replace("package=\"com.example.generatedapp\"", f"package=\"{package_name}\"")
        manifest_content = manifest_content.replace("<activity android:name=\".MainActivity\">", f"<activity android:name=\".{activity_name}\">")
        with open(self.project_root / "app" / "src" / "main" / "AndroidManifest.xml", "w") as f:
            f.write(manifest_content)

        # --- Modify MainActivity.java ---
        java_dir = self.project_root / "app" / "src" / "main" / "java"
        package_dir = java_dir / package_name.replace('.', os.sep)
        package_dir.mkdir(parents=True, exist_ok=True)

        main_activity_template_path = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com.example.generatedapp".replace('.', os.sep) / "MainActivity.java"
        if not main_activity_template_path.exists():
             raise FileNotFoundError("MainActivity template not found.")

        with open(main_activity_template_path, "r") as f:
            activity_content = f.read()
        activity_content = activity_content.replace("package com.example.generatedapp;", f"package {package_name};")
        activity_content = activity_content.replace("public class MainActivity", f"public class {activity_name}")
        # Placeholder for dynamic content injection based on prompt
        activity_content = activity_content.replace("// TODO: Inject dynamic UI/logic here", "// Dynamic content injection will go here")
        with open(package_dir / f"{activity_name}.java", "w") as f:
            f.write(activity_content)

        # --- Modify strings.xml ---
        with open(self.project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml", "r") as f:
            strings_content = f.read()
        strings_content = strings_content.replace("GeneratedApp", app_name)
        with open(self.project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml", "w") as f:
            f.write(strings_content)

        print(f"Android project structure set up at: {self.project_root}")

    def _integrate_arabic_features(self, arabic_text: str):
        """
        Integrates Arabic language features into the Android project.
        This could involve:
        - Adding Arabic text to strings.xml.
        - Potentially adding RTL support to the manifest.
        - Modifying UI layouts (if prompt suggests it) to support Arabic.
        """
        if not self.project_root:
            raise RuntimeError("Android project has not been set up yet.")

        strings_xml_path = self.project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        if not strings_xml_path.exists():
            raise FileNotFoundError("strings.xml not found in project.")

        # Basic integration: Add a new string resource for Arabic text
        # More advanced integration would involve parsing the arabic_text
        # to determine layout needs (e.g., text direction, string concatenation).
        arabic_string_name = "translated_greeting"
        new_string_element = f'\n    <string name="{arabic_string_name}">{arabic_text}</string>'

        with open(strings_xml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the closing tag for <resources> and insert before it
        insert_index = -1
        for i, line in enumerate(lines):
            if '</resources>' in line:
                insert_index = i
                break

        if insert_index != -1:
            lines.insert(insert_index, new_string_element)
            with open(strings_xml_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Added Arabic string '{arabic_string_name}' to strings.xml.")
        else:
            print("Warning: Could not find <resources> tag in strings.xml to insert Arabic text.")

        # TODO: More sophisticated Arabic feature integration based on prompt analysis.
        # This might involve:
        # - Generating Arabic-specific layout files (e.g., in res/layout-ldrtl).
        # - Modifying the Activity to handle text direction or input.
        # - Using Arabic fonts.


    def _build_apk(self) -> Path:
        """
        Builds the Android project into an APK using Gradle.
        Requires JAVA_HOME and ANDROID_SDK_ROOT to be set.
        """
        if not self.project_root or not self.project_root.exists():
            raise RuntimeError("Android project has not been set up or does not exist.")

        print(f"Building APK for project at: {self.project_root}")

        # Ensure Gradle wrapper is executable
        gradle_wrapper_path = self.project_root / "gradlew"
        if os.name != 'nt': # Not Windows
            gradle_wrapper_path.chmod(gradle_wrapper_path.stat().st_mode | 0o111)

        try:
            # Run Gradle assembleRelease to create a signed release APK (for production)
            # or assembleDebug for an unsigned debug APK. For simplicity, using debug.
            # For a truly "hyper-efficient APK", release build is usually preferred.
            # You might need to configure signing in a real scenario.
            build_command = [str(gradle_wrapper_path), "assembleDebug"]
            print(f"Executing build command: {' '.join(build_command)}")

            process = subprocess.Popen(build_command, cwd=self.project_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            print("Gradle Build Output:\n", stdout)
            if process.returncode != 0:
                print("Gradle Build Error:\n", stderr)
                raise RuntimeError(f"Gradle build failed with return code {process.returncode}")

            print("APK build successful.")

            # Locate the generated APK
            # The path can vary slightly depending on Gradle version and build type
            apk_path = None
            debug_apk_dir = self.project_root / "app" / "build" / "outputs" / "apk" / "debug"
            for apk_file in debug_apk_dir.glob("*.apk"):
                if "app-debug.apk" in str(apk_file):
                    apk_path = apk_file
                    break

            if not apk_path:
                raise FileNotFoundError("Generated APK not found after build.")

            print(f"APK generated at: {apk_path}")
            return apk_path

        except FileNotFoundError as e:
            print(f"Error: Gradle wrapper or Java might not be found. Ensure JAVA_HOME is set and gradlew is executable.")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            raise e

    def generate_apk_from_prompt(self, natural_language_prompt: str, arabic_content: str) -> Path:
        """
        The main function to orchestrate the APK generation process.
        Parses the natural language prompt to guide project setup and integration,
        then builds the APK.
        """
        # --- Lobe 4: Code Generation & Lobe 0: Language Integration ---
        # This step would involve advanced NLP to parse the natural_language_prompt.
        # For this example, we'll derive basic project parameters.
        # In a real scenario, a more sophisticated Arabic NLP parser would be used here.

        # Example of simple prompt parsing (replace with actual NLP logic)
        if "create an app called" in natural_language_prompt.lower():
            parts = natural_language_prompt.split("create an app called")
            app_name_part = parts[1].strip().split(".")[0]
            app_name = app_name_part.replace(" ", "_") # Sanitize for file names
            project_name = f"{app_name.lower()}_project"
            package_name = f"com.generated.{app_name.lower()}"
            activity_name = f"{app_name}Activity"
        else:
            project_name = "my_generated_app_project"
            app_name = "MyGeneratedApp"
            package_name = TARGET_PACKAGE_NAME
            activity_name = TARGET_ACTIVITY_NAME

        print(f"Parsed prompt: App Name='{app_name}', Project Name='{project_name}', Package='{package_name}', Activity='{activity_name}'")

        # --- Setup Project Structure ---
        self._setup_android_project(project_name, package_name, activity_name, app_name)

        # --- Integrate Arabic Features ---
        self._integrate_arabic_features(arabic_content)

        # --- Lobe 8: APK Compilation ---
        generated_apk_path = self._build_apk()

        return generated_apk_path

# Example Usage (for demonstration within this module)
if __name__ == "__main__":
    print("\n--- Initiating Lobe 8_apk_compiler_lobe ---")
    print("--- Building APK from Arabic Prompt ---")

    # Requires a pre-existing android_project_template directory with basic structure.
    # Create a dummy template if it doesn't exist for testing purposes.
    if not ANDROID_PROJECT_TEMPLATE_DIR.exists():
        print(f"Creating dummy template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        ANDROID_PROJECT_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)

        # Minimal build.gradle
        with open(BUILD_GRADLE_PATH, "w") as f:
            f.write("""
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.generatedapp'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.generatedapp"
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
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.core:core-ktx:1.5.0'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
            """)

        # Minimal AndroidManifest.xml
        with open(MANIFEST_PATH, "w") as f:
            f.write("""
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
            """)

        # Minimal MainActivity.java
        with open(MAIN_ACTIVITY_JAVA_PATH, "w") as f:
            f.write("""
package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists

        // TODO: Inject dynamic UI/logic here
        TextView welcomeText = findViewById(R.id.welcome_text); // Assuming a TextView with this ID
        if (welcomeText != null) {
            welcomeText.setText("Welcome!"); // Default text
        }
    }
}
            """)

        # Minimal strings.xml
        with open(STRINGS_XML_PATH, "w") as f:
            f.write("""
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">GeneratedApp</string>
</resources>
            """)
        print("Dummy template created.")

    # --- Test Case ---
    prompt = "Create an app called 'Hello Arabic World'."
    arabic_text_input = "مرحبا بالعالم العربي" # "Hello Arabic World"

    try:
        apk_generator = ApkGenerator()
        generated_apk = apk_generator.generate_apk_from_prompt(prompt, arabic_text_input)
        print(f"\n--- APK Generation Complete ---")
        print(f"Generated APK: {generated_apk}")

        # --- Cleanup Dummy Project Directory (if it was created for the demo) ---
        # This part is crucial to avoid leaving large temp directories.
        if generated_apk and generated_apk.parent.parent.name.startswith("my_generated_app_project"): # Check if it's the generated one
            print("\n--- Cleaning up generated project directory ---")
            try:
                shutil.rmtree(generated_apk.parent.parent) # Remove the project root
                print(f"Cleaned up generated project directory: {generated_apk.parent.parent}")
            except OSError as e:
                print(f"Error removing directory {generated_apk.parent.parent}: {e}")

    except Exception as e:
        print(f"\nAn error occurred during APK generation: {e}")

    print("\n--- Lobe 8_apk_compiler_lobe Finished ---")