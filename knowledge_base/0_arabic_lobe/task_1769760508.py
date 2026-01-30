import os
import re
import shutil
import subprocess
from pathlib import Path

# Assuming Lobe 0_arabic_lobe and Lobe 4_code_generation_lobe are already defined and accessible

# --- Constants ---
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
DEMO_PROJECT_DIR = KNOWLEDGE_BASE_DIR / "demo_apk_project"
MAIN_ACTIVITY_TEMPLATE = """
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
        textView.setText("Hello, World from a generated APK!");
    }
}
"""

ACTIVITY_MAIN_XML_TEMPLATE = """
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
        android:text="Loading..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

GRADLE_PROPERTIES_TEMPLATE = """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
"""

GRADLE_WRAPPER_PROPERTIES_TEMPLATE = """
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-7.4-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

SETTINGS_GRADLE_TEMPLATE = """
rootProject.name = "MyApp"
include ':app'
"""

BUILD_GRADLE_APP_TEMPLATE = """
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
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.7.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""

MANIFEST_TEMPLATE = """
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
        android:theme="@style/Theme.MyApp"
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

STRINGS_XML_TEMPLATE = """
<resources>
    <string name="app_name">MyApp</string>
</resources>
"""

# --- Helper Functions ---

def setup_project_structure(project_root: Path):
    """Sets up the basic directory structure for an Android project."""
    (project_root / "app").mkdir(parents=True, exist_ok=True)
    (project_root / "app" / "src" / "main" / "java" / "com" / "example" / "myapp").mkdir(parents=True, exist_ok=True)
    (project_root / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
    (project_root / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)
    (project_root / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)

def create_file(path: Path, content: str):
    """Creates a file with the given content."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def parse_arabic_nl_to_apk_params(arabic_text: str) -> dict:
    """
    Parses Arabic natural language input to extract parameters for APK generation.
    This is a placeholder; a real implementation would involve Lobe 0_arabic_lobe.
    """
    params = {
        "app_name": "MyApp",
        "package_name": "com.example.myapp",
        "main_activity_title": "Hello, World from a generated APK!",
        "dependencies": [
            "androidx.core:core-ktx:1.7.0",
            "androidx.appcompat:appcompat:1.6.1",
            "com.google.android.material:material:1.10.0",
            "androidx.constraintlayout:constraintlayout:2.1.4"
        ]
    }

    # Simple example of parsing:
    name_match = re.search(r"اسم التطبيق هو ([\w\s]+)", arabic_text)
    if name_match:
        params["app_name"] = name_match.group(1).strip()
        params["package_name"] = "com.example." + params["app_name"].lower().replace(" ", "")
        
    title_match = re.search(r"النص الرئيسي هو ([\w\s]+)", arabic_text)
    if title_match:
        params["main_activity_title"] = title_match.group(1).strip()

    return params

class ApkCompilerLobe:
    def __init__(self, android_sdk_path: str = None):
        self.android_sdk_path = android_sdk_path or os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
        if not self.android_sdk_path:
            raise EnvironmentError("Android SDK path not found. Set ANDROID_SDK_ROOT or ANDROID_HOME.")
        self.build_tools_path = self._find_build_tools()
        if not self.build_tools_path:
            raise EnvironmentError("Android build-tools not found. Ensure they are installed.")
        self.sdk_manager_path = Path(self.android_sdk_path) / "cmdline-tools" / "latest" / "bin" / "sdkmanager" # Adjust path as needed

    def _find_build_tools(self) -> Path | None:
        """Finds the latest installed Android build-tools directory."""
        build_tools_dir = Path(self.android_sdk_path) / "build-tools"
        if not build_tools_dir.exists():
            return None
        build_versions = sorted([d for d in build_tools_dir.iterdir() if d.is_dir()], key=lambda x: x.name, reverse=True)
        if build_versions:
            return build_versions[0]
        return None

    def _run_command(self, command: list, cwd: Path = None):
        """Runs a shell command and returns its output."""
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed with error:\n{result.stderr}")
        print(f"Command output:\n{result.stdout}")
        return result.stdout

    def _generate_gradle_wrapper(self, project_root: Path):
        """Generates the Gradle wrapper files."""
        create_file(project_root / "gradle.properties", GRADLE_PROPERTIES_TEMPLATE)
        create_file(project_root / "gradlew", "#!/bin/bash\nexec gradle/wrapper/gradle-wrapper.jar \"$@\"\n")
        os.chmod(project_root / "gradlew", 0o755)
        create_file(project_root / "gradlew.bat", "@if not \"%GRADLE_HOME%\" == \"\" goto gotContrition\nset GRADLE_HOME=%~dp0..\n:gotContrition\ncall gradle\\wrapper\\gradle-wrapper.bat %*\n")
        create_file(project_root / "gradle" / "wrapper" / "gradle-wrapper.properties", GRADLE_WRAPPER_PROPERTIES_TEMPLATE)
        (project_root / "gradle" / "wrapper").mkdir(parents=True, exist_ok=True)

    def _create_android_project_files(self, project_root: Path, params: dict):
        """Creates all necessary Android project files."""
        setup_project_structure(project_root)
        create_file(project_root / "settings.gradle", SETTINGS_GRADLE_TEMPLATE.replace("MyApp", params["app_name"]))
        create_file(project_root / "build.gradle", BUILD_GRADLE_APP_TEMPLATE.replace("com.example.myapp", params["package_name"]))

        app_dir = project_root / "app"
        create_file(app_dir / "src" / "main" / "AndroidManifest.xml", MANIFEST_TEMPLATE.replace("com.example.myapp", params["package_name"]))
        create_file(app_dir / "src" / "main" / "res" / "values" / "strings.xml", STRINGS_XML_TEMPLATE.replace("MyApp", params["app_name"]))
        create_file(app_dir / "src" / "main" / "res" / "layout" / "activity_main.xml", ACTIVITY_MAIN_XML_TEMPLATE)

        java_dir = app_dir / "src" / "main" / "java" / "com" / "example" / "myapp"
        main_activity_content = MAIN_ACTIVITY_TEMPLATE.replace("package com.example.myapp;", f"package {params['package_name']};").replace("Hello, World from a generated APK!", params["main_activity_title"])
        create_file(java_dir / "MainActivity.java", main_activity_content)

        # Create proguard-rules.pro if it doesn't exist
        proguard_file = project_root / "app" / "proguard-rules.pro"
        if not proguard_file.exists():
            with open(proguard_file, "w") as f:
                f.write("-keep class com.example.myapp.** { *; }\n") # Basic rule


    def build_apk(self, natural_language_prompt: str) -> Path:
        """
        Builds an Android APK from a natural language prompt.
        This function orchestrates the entire APK building process.
        """
        print(f"\n--- Initiating APK build for prompt: '{natural_language_prompt}' ---")

        # Step 1: Parse natural language into project parameters
        print("Parsing natural language prompt...")
        apk_params = parse_arabic_nl_to_apk_params(natural_language_prompt)
        print(f"Parsed parameters: {apk_params}")

        # Step 2: Set up the project directory and files
        print(f"Setting up project structure at: {DEMO_PROJECT_DIR}")
        if DEMO_PROJECT_DIR.exists():
            shutil.rmtree(DEMO_PROJECT_DIR)
        DEMO_PROJECT_DIR.mkdir(parents=True, exist_ok=True)

        self._create_android_project_files(DEMO_PROJECT_DIR, apk_params)
        self._generate_gradle_wrapper(DEMO_PROJECT_DIR)
        print("Project structure created.")

        # Step 3: Build the APK using Gradle
        print("Building APK using Gradle...")
        # Ensure gradlew is executable
        gradlew_path = DEMO_PROJECT_DIR / "gradlew"
        if not gradlew_path.exists():
            raise FileNotFoundError("gradlew not found. Project setup might have failed.")
        os.chmod(gradlew_path, 0o755)

        # The command to build the release APK
        build_command = ["./gradlew", "assembleRelease"]
        try:
            self._run_command(build_command, cwd=DEMO_PROJECT_DIR)
            print("APK build successful.")

            # Step 4: Locate the generated APK
            apk_path = DEMO_PROJECT_DIR / "app" / "build" / "outputs" / "apk" / "release" / f"{apk_params['app_name'].lower().replace(' ', '')}-release.apk"
            if not apk_path.exists():
                raise FileNotFoundError(f"Generated APK not found at expected location: {apk_path}")

            print(f"APK generated at: {apk_path}")
            return apk_path

        except Exception as e:
            print(f"\nAPK build process failed: {e}")
            raise

    def cleanup_project(self):
        """Cleans up the dummy project directory."""
        if DEMO_PROJECT_DIR.exists():
            print(f"Removing dummy project directory: {DEMO_PROJECT_DIR}")
            shutil.rmtree(DEMO_PROJECT_DIR)

# --- Lobe Function ---

def _arabic_nl_to_apk_compiler_lobe(arabic_prompt: str, android_sdk_path: str = None) -> Path | None:
    """
    Lobe responsible for compiling an Android APK from Arabic natural language.

    Args:
        arabic_prompt (str): The Arabic natural language prompt describing the desired APK.
        android_sdk_path (str, optional): Path to the Android SDK. If None, it will be
                                           searched in environment variables.

    Returns:
        Path | None: The path to the generated APK if successful, otherwise None.
    """
    try:
        apk_compiler = ApkCompilerLobe(android_sdk_path=android_sdk_path)
        generated_apk_path = apk_compiler.build_apk(arabic_prompt)
        return generated_apk_path
    except EnvironmentError as e:
        print(f"Environment error during APK compilation: {e}")
        print("Please ensure the Android SDK is installed and accessible.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during APK compilation: {e}")
        return None
    finally:
        # Clean up the dummy project after the process, regardless of success or failure
        # This is handled within ApkCompilerLobe.build_apk for now, but could be
        # moved here for centralized cleanup.
        pass

# --- Example Usage (for demonstration within this module, not part of the final output) ---

if __name__ == '__main__':
    # This block is for testing the lobe locally.
    # In the integrated system, this lobe would be called by another.

    # Mock Lobe 0_arabic_lobe and Lobe 4_code_generation_lobe for standalone testing
    class MockArabicLobe:
        def parse_arabic_prompt(self, prompt):
            # In a real scenario, this would call into Lobe 0_arabic_lobe
            print(f"Mock parsing prompt: {prompt}")
            # Using the internal parse_arabic_nl_to_apk_params for this mock
            return parse_arabic_nl_to_apk_params(prompt)

    class MockCodeGenerationLobe:
        def generate_java_code(self, params):
            print(f"Mock generating Java code for: {params}")
            return MAIN_ACTIVITY_TEMPLATE.replace("package com.example.myapp;", f"package {params['package_name']};").replace("Hello, World from a generated APK!", params["main_activity_title"])

    # Assume Android SDK is available for this test
    # If not, the ApkCompilerLobe constructor will raise an error.
    # You might need to set ANDROID_SDK_ROOT or ANDROID_HOME environment variables.
    try:
        # Example Arabic prompt
        arabic_prompt_example = "قم بإنشاء تطبيق أندرويد بسيط. اسم التطبيق هو 'تطبيقي العربي' والنص الرئيسي هو 'مرحباً بالعالم العربي'."

        print("\n--- Testing _arabic_nl_to_apk_compiler_lobe ---")
        generated_apk_path = _arabic_nl_to_apk_compiler_lobe(arabic_prompt_example)

        if generated_apk_path:
            print(f"\nSuccessfully generated APK at: {generated_apk_path}")
        else:
            print("\nAPK generation failed.")

    except EnvironmentError as e:
        print(f"\nSkipping test due to missing Android SDK: {e}")
    except Exception as e:
        print(f"\nAn error occurred during the test: {e}")

    finally:
        # Clean up the demo project if it exists after the test
        if DEMO_PROJECT_DIR.exists():
            print(f"\n--- Cleaning up demo project directory from test ---")
            shutil.rmtree(DEMO_PROJECT_DIR)