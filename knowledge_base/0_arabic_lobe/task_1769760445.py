import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# --- Constants ---
DUMMY_PROJECT_ROOT = Path("./dummy_apk_project")
MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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

ACTIVITY_TEMPLATE = """package {package_name};

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

LAYOUT_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <!-- Your UI elements will go here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""

STRING_TEMPLATE = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""

GRADLE_PROPERTIES_TEMPLATE = """systemProp.android.project.target=android-33
"""

BUILD_GRADLE_APP_TEMPLATE = """plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId '{package_name}'
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
    buildFeatures {{
        viewBinding true
    }}
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

BUILD_GRADLE_PROJECT_TEMPLATE = """buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath 'com.android.tools.build:gradle:7.4.2'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.20'
    }}
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

tasks.register('clean', Delete) {{
    delete rootProject.buildDir
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


class APKCompilerLobe:
    """
    Responsible for compiling generated code into an APK.
    This lobe simulates the process of setting up an Android project structure
    and using the Android SDK command-line tools to build the APK.
    """

    def __init__(self, project_root: Path = DUMMY_PROJECT_ROOT):
        self.project_root = project_root
        self.app_module_path = self.project_root / "app"
        self.manifest_file = self.app_module_path / "src" / "main" / "AndroidManifest.xml"
        self.activity_file = self.app_module_path / "src" / "main" / "java" / "com" / "example" / "myapp" / "MainActivity.java"
        self.layout_file = self.app_module_path / "src" / "main" / "res" / "layout" / "activity_main.xml"
        self.strings_file = self.app_module_path / "src" / "main" / "res" / "values" / "strings.xml"
        self.gradle_properties_file = self.project_root / "gradle.properties"
        self.build_gradle_app_file = self.app_module_path / "build.gradle"
        self.build_gradle_project_file = self.project_root / "build.gradle"
        self.settings_gradle_file = self.project_root / "settings.gradle"
        self.android_sdk_cmd = self._find_android_sdk()

    def _find_android_sdk(self) -> Optional[Path]:
        """
        Attempts to find the Android SDK installation directory.
        This is a crucial step for the build process.
        """
        # Prioritize common environment variables
        sdk_path = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
        if sdk_path:
            return Path(sdk_path)

        # Fallback to common installation locations (user-specific, system-wide)
        possible_paths = [
            Path.home() / "Library" / "Android" / "sdk",  # macOS
            Path.home() / "Android" / "Sdk",  # Linux/Windows
            Path("C:") / "Users" / os.getlogin() / "AppData" / "Local" / "Android" / "Sdk",  # Windows
        ]
        for p in possible_paths:
            if p.exists() and (p / "tools").exists() and (p / "platform-tools").exists():
                return p
        return None

    def setup_project_structure(self, package_name: str, app_name: str):
        """
        Creates the directory structure for an Android project.
        """
        if not self.android_sdk_cmd:
            raise EnvironmentError("Android SDK not found. Please set ANDROID_SDK_ROOT or ANDROID_HOME.")

        print(f"Setting up project structure in: {self.project_root}")
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.app_module_path.mkdir(parents=True, exist_ok=True)

        # Create src/main/java and src/main/res directories
        java_dir = self.app_module_path / "src" / "main" / "java" / package_name.replace('.', os.sep)
        java_dir.mkdir(parents=True, exist_ok=True)
        res_dir = self.app_module_path / "src" / "main" / "res"
        values_dir = res_dir / "values"
        layout_dir = res_dir / "layout"
        values_dir.mkdir(parents=True, exist_ok=True)
        layout_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy launcher icon directories (optional but good practice)
        mipmap_dir = res_dir / "mipmap-hdpi"
        mipmap_dir.mkdir(parents=True, exist_ok=True)
        mipmap_dir = res_dir / "mipmap-mdpi"
        mipmap_dir.mkdir(parents=True, exist_ok=True)
        mipmap_dir = res_dir / "mipmap-xhdpi"
        mipmap_dir.mkdir(parents=True, exist_ok=True)
        mipmap_dir = res_dir / "mipmap-xxhdpi"
        mipmap_dir.mkdir(parents=True, exist_ok=True)
        mipmap_dir = res_dir / "mipmap-xxxhdpi"
        mipmap_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy ic_launcher.png files
        for mipmap in ["mipmap-hdpi", "mipmap-mdpi", "mipmap-xhdpi", "mipmap-xxhdpi", "mipmap-xxxhdpi"]:
            icon_path = res_dir / mipmap / "ic_launcher.png"
            if not icon_path.exists():
                with open(icon_path, "w") as f:
                    f.write("") # Dummy file

        # Create dummy proguard-rules.pro
        (self.app_module_path / "proguard-rules.pro").write_text("")

        print("Project structure created successfully.")

    def write_gradle_files(self, package_name: str, app_name: str):
        """
        Writes the necessary Gradle build files for an Android project.
        """
        print("Writing Gradle files...")
        self.gradle_properties_file.write_text(GRADLE_PROPERTIES_TEMPLATE)
        self.build_gradle_project_file.write_text(BUILD_GRADLE_PROJECT_TEMPLATE)
        self.settings_gradle_file.write_text(SETTINGS_GRADLE_TEMPLATE.format(app_name=app_name))
        self.build_gradle_app_file.write_text(BUILD_GRADLE_APP_TEMPLATE.format(package_name=package_name))
        print("Gradle files written successfully.")

    def write_android_manifest(self, package_name: str):
        """
        Writes the AndroidManifest.xml file.
        """
        print("Writing AndroidManifest.xml...")
        self.manifest_file.write_text(MANIFEST_TEMPLATE.format(package_name=package_name))
        print("AndroidManifest.xml written successfully.")

    def write_main_activity(self, package_name: str):
        """
        Writes the MainActivity.java file.
        """
        print("Writing MainActivity.java...")
        self.activity_file.write_text(ACTIVITY_TEMPLATE.format(package_name=package_name))
        print("MainActivity.java written successfully.")

    def write_layout_file(self):
        """
        Writes the activity_main.xml layout file.
        """
        print("Writing activity_main.xml...")
        self.layout_file.write_text(LAYOUT_TEMPLATE)
        print("activity_main.xml written successfully.")

    def write_strings_file(self, app_name: str):
        """
        Writes the strings.xml file.
        """
        print("Writing strings.xml...")
        self.strings_file.write_text(STRING_TEMPLATE.format(app_name=app_name))
        print("strings.xml written successfully.")

    def build_apk(self, package_name: str) -> Path:
        """
        Executes the Gradle build command to compile the project and generate an APK.
        Returns the path to the generated APK.
        """
        if not self.android_sdk_cmd:
            raise EnvironmentError("Android SDK not found. Cannot build APK.")

        print("Starting APK build process using Gradle...")
        try:
            # Ensure the project is clean before building
            print("Running Gradle clean...")
            clean_process = subprocess.run(
                ["./gradlew", "clean"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                shell=os.name == "nt" # Use shell=True on Windows
            )
            print("Gradle clean output:\n", clean_process.stdout)
            if clean_process.stderr:
                print("Gradle clean error output:\n", clean_process.stderr)

            print("Running Gradle assembleDebug...")
            assemble_process = subprocess.run(
                ["./gradlew", "assembleDebug"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                shell=os.name == "nt" # Use shell=True on Windows
            )
            print("Gradle assembleDebug output:\n", assemble_process.stdout)
            if assemble_process.stderr:
                print("Gradle assembleDebug error output:\n", assemble_process.stderr)

            # Find the generated APK
            # The APK is usually located in app/build/outputs/apk/debug/
            apk_path = (
                self.app_module_path / "build" / "outputs" / "apk" / "debug"
            )
            apks = list(apk_path.glob("*.apk"))

            if not apks:
                raise FileNotFoundError("No APK found after build. Check Gradle output for errors.")

            generated_apk_path = apks[0]
            print(f"APK generated successfully at: {generated_apk_path}")
            return generated_apk_path

        except FileNotFoundError:
            print("Error: Gradle wrapper (gradlew) not found. Ensure it's in the project root.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"Gradle build failed with error code {e.returncode}:")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            raise RuntimeError("APK build process failed.") from e
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            raise

    def cleanup_project(self):
        """
        Removes the dummy project directory.
        """
        if self.project_root.exists():
            print(f"Cleaning up project directory: {self.project_root}")
            shutil.rmtree(self.project_root)
            print("Project directory removed.")


# --- Demo Usage ---
def demo_apk_compiler_lobe():
    """
    Demonstrates the functionality of the APKCompilerLobe.
    This function simulates the process of generating an APK from basic parameters.
    """
    print("\n--- Initiating APKCompilerLobe Module Demo ---")
    package_name = "com.example.myapp"
    app_name = "MyArabicApp"
    compiler = APKCompilerLobe()

    try:
        compiler.setup_project_structure(package_name, app_name)
        compiler.write_gradle_files(package_name, app_name)
        compiler.write_android_manifest(package_name)
        compiler.write_main_activity(package_name)
        compiler.write_layout_file()
        compiler.write_strings_file(app_name)

        # This part requires a working Android SDK and Gradle environment
        # If these are not set up, the build will fail.
        # For a truly automated system, consider using Docker or a pre-configured build environment.
        if compiler.android_sdk_cmd:
            print("\nAttempting to build the APK...")
            apk_path = compiler.build_apk(package_name)
            print(f"\nDemo 1: APK successfully generated at: {apk_path}")
        else:
            print("\nSkipping APK build as Android SDK was not found.")
            print("Demo 1: Project structure and files created, but APK build skipped.")

    except EnvironmentError as e:
        print(f"\nDemo 1 failed due to environment setup: {e}")
    except FileNotFoundError as e:
        print(f"\nDemo 1 failed: Required file not found - {e}")
    except RuntimeError as e:
        print(f"\nDemo 1 failed during build: {e}")
    except Exception as e:
        print(f"\nDemo 1 failed with an unexpected error: {e}")
    finally:
        compiler.cleanup_project()

    print("\n--- APKCompilerLobe Module Demo Finished ---")

if __name__ == "__main__":
    # This ensures the demo runs only when the script is executed directly.
    # In a real integrated system, this lobe would be called by a higher-level orchestrator.

    # Check if Android SDK is available before running the demo that requires it.
    android_sdk_available = APKCompilerLobe()._find_android_sdk() is not None
    if android_sdk_available:
        demo_apk_compiler_lobe()
    else:
        print("Android SDK not found. Skipping APK build demo.")
        print("You can set the ANDROID_SDK_ROOT or ANDROID_HOME environment variable to point to your Android SDK.")