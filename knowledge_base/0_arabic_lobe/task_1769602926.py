import os
import subprocess
import re
from pathlib import Path

# Assume these are defined elsewhere and accessible
# KNOWLEDGE_BASE_DIR = Path("path/to/your/knowledge_base")
# PROJECT_ROOT = Path(__file__).parent.parent # Adjust as needed

# --- Lobe 0_arabic_lobe (Modified to include APK related logic) ---

class ArabicAPKParser:
    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.manifest_template = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <uses-sdk android:minSdkVersion="{min_sdk_version}" android:targetSdkVersion="{target_sdk_version}" />

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
        self.activity_template = """package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // TODO: Add app logic based on NLP input
    }}
}}
"""
        self.build_gradle_template = """plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{package_name}'
    compileSdk {compile_sdk_version}

    defaultConfig {{
        applicationId '{package_name}'
        minSdk {min_sdk_version}
        targetSdk {target_sdk_version}
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
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""

    def parse_arabic_description_for_apk_config(self, arabic_description: str) -> dict:
        """
        Parses an Arabic description to extract APK configuration parameters.
        This is a simplified example and would require a more robust NLP approach
        for real-world scenarios.
        """
        config = {
            "package_name": "com.example.myapp",
            "min_sdk_version": "21",
            "target_sdk_version": "33",
            "compile_sdk_version": "33",
            "app_name": "My App"
        }

        # Example parsing: Look for keywords and patterns
        if "اسم التطبيق" in arabic_description:
            match = re.search(r"اسم التطبيق هو ([\w\s]+)", arabic_description)
            if match:
                config["app_name"] = match.group(1).strip()
                config["package_name"] = "com." + config["app_name"].lower().replace(" ", "")

        if "الحد الأدنى لإصدار SDK" in arabic_description:
            match = re.search(r"الحد الأدنى لإصدار SDK هو (\d+)", arabic_description)
            if match:
                config["min_sdk_version"] = match.group(1)

        if "النسخة المستهدفة من SDK" in arabic_description:
            match = re.search(r"النسخة المستهدفة من SDK هي (\d+)", arabic_description)
            if match:
                config["target_sdk_version"] = match.group(1)

        # More advanced parsing would involve dedicated NLP libraries for Arabic
        # e.g., using spaCy with an Arabic model or NLTK for tokenization and POS tagging.
        # For now, we rely on simple keyword matching.

        return config

    def generate_android_project_structure(self, config: dict, project_path: Path):
        """
        Generates the basic Android project directory and file structure.
        """
        app_module_path = project_path / "app"
        manifest_path = app_module_path / "src" / "main" / "AndroidManifest.xml"
        java_dir = app_module_path / "src" / "main" / "java"
        package_java_dir = java_dir / config["package_name"].replace(".", os.sep)
        activity_path = package_java_dir / "MainActivity.java"
        res_dir = app_module_path / "src" / "main" / "res"
        layout_dir = res_dir / "layout"
        values_dir = res_dir / "values"
        mipmap_dir = res_dir / "mipmap-hdpi" # Example mipmap, could be more

        os.makedirs(package_java_dir, exist_ok=True)
        os.makedirs(layout_dir, exist_ok=True)
        os.makedirs(values_dir, exist_ok=True)
        os.makedirs(mipmap_dir, exist_ok=True)

        # Create AndroidManifest.xml
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(self.manifest_template.format(**config))

        # Create MainActivity.java
        with open(activity_path, "w", encoding="utf-8") as f:
            f.write(self.activity_template.format(**config))

        # Create basic layout file (activity_main.xml)
        with open(layout_dir / "activity_main.xml", "w", encoding="utf-8") as f:
            f.write('<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity">\n    <!-- TODO: Add UI elements -->\n</androidx.constraintlayout.widget.ConstraintLayout>')

        # Create basic string resources
        with open(values_dir / "strings.xml", "w", encoding="utf-8") as f:
            f.write(f'<resources>\n    <string name="app_name">{config.get("app_name", "My App")}</string>\n</resources>')

        # Create basic styles.xml
        with open(values_dir / "styles.xml", "w", encoding="utf-8") as f:
            f.write('<resources>\n    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">\n        <!-- Customize your theme here. -->\n    </style>\n</resources>')

        # Create build.gradle
        with open(app_module_path / "build.gradle", "w", encoding="utf-8") as f:
            f.write(self.build_gradle_template.format(**config))

        # Create a dummy launcher icon (very basic)
        with open(mipmap_dir / "ic_launcher.png", "wb") as f:
            # This is a placeholder, a real icon would be needed
            f.write(b'')

        with open(mipmap_dir / "ic_launcher_round.png", "wb") as f:
            # This is a placeholder, a real icon would be needed
            f.write(b'')


    def create_gradle_wrapper(self, project_path: Path):
        """
        Creates the Gradle wrapper files.
        """
        try:
            subprocess.run(["./gradlew", "wrapper"], cwd=project_path, check=True, capture_output=True, text=True)
            print(f"Gradle wrapper created successfully in {project_path}")
        except FileNotFoundError:
            print("Error: gradlew command not found. Ensure you have the Android SDK and Gradle installed and configured in your PATH.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating Gradle wrapper: {e}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")

    def build_apk(self, project_path: Path) -> Path | None:
        """
        Builds the APK using Gradle.
        Returns the path to the generated APK if successful, None otherwise.
        """
        try:
            # Ensure gradlew script is executable
            gradlew_script = project_path / "gradlew"
            if os.name != 'nt': # Not on Windows
                os.chmod(gradlew_script, os.stat(gradlew_script).st_mode | 0o111)

            # Run the assembleDebug task
            result = subprocess.run([str(gradlew_script), "assembleDebug"], cwd=project_path, check=True, capture_output=True, text=True)
            print("Gradle build output:")
            print(result.stdout)

            # Locate the generated APK
            apk_path = project_path / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
            if apk_path.exists():
                print(f"APK successfully built at: {apk_path}")
                return apk_path
            else:
                print("Error: APK file not found after build. Check Gradle output for details.")
                return None

        except FileNotFoundError:
            print("Error: gradlew script not found. Ensure the project structure is correct.")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error building APK: {e}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            return None

# --- Lobe 4_code_generation_lobe (Integration with Arabic APK Parser) ---

class CodeGeneratorArabicAPK:
    def __init__(self, arabic_parser: ArabicAPKParser):
        self.arabic_parser = arabic_parser

    def generate_apk_from_arabic(self, arabic_description: str, output_dir: Path) -> Path | None:
        """
        Generates an Android APK from a natural language Arabic description.
        """
        print(f"\n--- Generating APK from Arabic Description ---")
        print(f"Input Arabic Description: '{arabic_description}'")

        # 1. Parse Arabic description for APK configuration
        apk_config = self.arabic_parser.parse_arabic_description_for_apk_config(arabic_description)
        print(f"Parsed APK Configuration: {apk_config}")

        # 2. Create a new Android project directory
        project_name = apk_config.get("app_name", "GeneratedApp").replace(" ", "_")
        project_path = output_dir / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        print(f"Created project directory: {project_path}")

        # Create basic project files (AndroidManifest.xml, build.gradle, etc.)
        # This also includes creating the app module structure.
        self.arabic_parser.generate_android_project_structure(apk_config, project_path)
        print("Generated basic Android project structure and files.")

        # 3. Create Gradle wrapper
        self.arabic_parser.create_gradle_wrapper(project_path)

        # 4. Build the APK using Gradle
        print("Attempting to build the APK...")
        apk_file_path = self.arabic_parser.build_apk(project_path)

        if apk_file_path:
            print(f"APK generation process completed successfully. APK located at: {apk_file_path}")
            return apk_file_path
        else:
            print("APK generation failed.")
            return None

# --- Example Usage (Demonstration) ---

if __name__ == "__main__":
    # Assuming KNOWLEDGE_BASE_DIR is defined
    KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

    # Instantiate the ArabicAPKParser
    arabic_apk_parser = ArabicAPKParser(KNOWLEDGE_BASE_DIR)

    # Instantiate the CodeGeneratorArabicAPK
    code_generator = CodeGeneratorArabicAPK(arabic_apk_parser)

    # Define an Arabic description for an APK
    arabic_prompt = "قم بإنشاء تطبيق باسم 'حاسبة بسيطة'. يجب أن يكون الحد الأدنى لإصدار SDK هو 24 والنسخة المستهدفة هي 34. اسم التطبيق هو حاسبة بسيطة."

    # Define the output directory for the generated APK
    output_directory = Path("./generated_apks")
    output_directory.mkdir(exist_ok=True)

    # Generate the APK
    generated_apk = code_generator.generate_apk_from_arabic(arabic_prompt, output_directory)

    if generated_apk:
        print(f"\n--- APK Generation Successful ---")
        print(f"Generated APK: {generated_apk}")
    else:
        print(f"\n--- APK Generation Failed ---")

    # --- Clean up dummy files ---
    print("\n--- Cleaning up dummy files ---")
    if KNOWLEDGE_BASE_DIR.exists():
        import shutil
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
        print(f"Removed: {KNOWLEDGE_BASE_DIR}")
    if output_directory.exists():
        # For demonstration, we might want to keep the generated APK, but for clean runs:
        # shutil.rmtree(output_directory)
        # print(f"Removed: {output_directory}")
        pass # Keep the generated APK for inspection
    print("\n--- Arabic Parser and Generator Module Demo Finished ---")