import os
import subprocess
from pathlib import Path

# Global constants (replace with actual configuration)
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
TEMP_DIR = Path("./temp")
JAVA_SDK_PATH = os.environ.get("JAVA_HOME") # Assume JAVA_HOME is set
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT") # Assume ANDROID_SDK_ROOT is set
BUILD_TOOLS_VERSION = "34.0.0" # Example, should be dynamically determined if possible

if not KNOWLEDGE_BASE_DIR.exists():
    KNOWLEDGE_BASE_DIR.mkdir(parents=True)
if not TEMP_DIR.exists():
    TEMP_DIR.mkdir(parents=True)

class ArabicAPKGenerator:
    def __init__(self, knowledge_base_dir: Path, temp_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.temp_dir = temp_dir
        self.apk_template_path = self.knowledge_base_dir / "apk_template"
        self.android_manifest_template_path = self.apk_template_path / "AndroidManifest.xml"
        self.gradle_build_template_path = self.apk_template_path / "build.gradle"
        self.settings_gradle_template_path = self.apk_template_path / "settings.gradle"
        self.app_gradle_template_path = self.apk_template_path / "app/build.gradle"
        self.main_activity_template_path = self.apk_template_path / "app/src/main/java/com/example/generated/MainActivity.java"
        self.strings_xml_template_path = self.apk_template_path / "app/src/main/res/values/strings.xml"
        self.colors_xml_template_path = self.apk_template_path / "app/src/main/res/values/colors.xml"
        self.themes_xml_template_path = self.apk_template_path / "app/src/main/res/values/themes.xml"

        # Ensure templates exist or handle their creation/loading
        self._ensure_templates()

    def _ensure_templates(self):
        # In a real scenario, these templates would be pre-existing files.
        # For this demonstration, we'll create placeholder content if they don't exist.
        if not self.apk_template_path.exists():
            self.apk_template_path.mkdir(parents=True)
        if not (self.apk_template_path / "app").exists():
            (self.apk_template_path / "app").mkdir(parents=True)
        if not (self.apk_template_path / "app/src").exists():
            (self.apk_template_path / "app/src").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main").exists():
            (self.apk_template_path / "app/src/main").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main/java").exists():
            (self.apk_template_path / "app/src/main/java").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main/java/com").exists():
            (self.apk_template_path / "app/src/main/java/com").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main/java/com/example").exists():
            (self.apk_template_path / "app/src/main/java/com/example").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main/java/com/example/generated").exists():
            (self.apk_template_path / "app/src/main/java/com/example/generated").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main/res").exists():
            (self.apk_template_path / "app/src/main/res").mkdir(parents=True)
        if not (self.apk_template_path / "app/src/main/res/values").exists():
            (self.apk_template_path / "app/src/main/res/values").mkdir(parents=True)

        if not self.android_manifest_template_path.exists():
            with open(self.android_manifest_template_path, "w", encoding="utf-8") as f:
                f.write("""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.generated">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
                """)

        if not self.gradle_build_template_path.exists():
            with open(self.gradle_build_template_path, "w", encoding="utf-8") as f:
                f.write("""
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.0.0' // Version might need adjustment
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.buildDir = '../build'
subprojects {
    project.buildDir = rootProject.buildDir.toString() + '/' + name
}

tasks.register('clean', Delete) {
    delete rootProject.buildDir
}
                """)

        if not self.settings_gradle_template_path.exists():
            with open(self.settings_gradle_template_path, "w", encoding="utf-8") as f:
                f.write("""
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "GeneratedApp"
include ':app'
                """)

        if not self.app_gradle_template_path.exists():
            with open(self.app_gradle_template_path, "w", encoding="utf-8") as f:
                f.write(f"""
plugins {{
    id 'com.android.application'
    id 'kotlin-android' // Optional, if supporting Kotlin
}}

android {{
    namespace 'com.example.generated'
    compileSdk 34 // Target SDK version

    defaultConfig {{
        applicationId "com.example.generated"
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
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
    // If using Java 11+ for Gradle, uncomment the following:
    // useLibrary 'org.apache.http.legacy'
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1' // Example version
    implementation 'com.google.android.material:material:1.11.0' // Example version
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4' // Example version
    testImplementation 'junit:junit:4.13.2' // Example version
    androidTestImplementation 'androidx.test.ext:junit:1.1.5' // Example version
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1' // Example version
}}
                """)

        if not self.main_activity_template_path.exists():
            with open(self.main_activity_template_path, "w", encoding="utf-8") as f:
                f.write("""
package com.example.generated;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists

        TextView welcomeText = findViewById(R.id.welcome_text);
        if (welcomeText != null) {
            welcomeText.setText(R.string.welcome_message); // Dynamic message
        }
    }
}
                """)

        if not self.strings_xml_template_path.exists():
            with open(self.strings_xml_template_path, "w", encoding="utf-8") as f:
                f.write("""
<resources>
    <string name="app_name">Generated Arabic App</string>
    <string name="welcome_message">مرحباً بك في تطبيقك!</string>
</resources>
                """)

        if not self.colors_xml_template_path.exists():
            with open(self.colors_xml_template_path, "w", encoding="utf-8") as f:
                f.write("""
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
                """)

        if not self.themes_xml_template_path.exists():
            with open(self.themes_xml_template_path, "w", encoding="utf-8") as f:
                f.write("""
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.GeneratedApp" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <!-- Primary brand color. -->
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/black</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
        <!-- Customize your theme here. -->
    </style>
</resources>
                """)

    def _create_project_structure(self, project_name: str, app_name_arabic: str, package_name: str = "com.example.generated"):
        project_root = self.temp_dir / project_name
        app_module_path = project_root / "app"
        src_main_path = app_module_path / "src" / "main"
        java_path = src_main_path / "java"
        res_path = src_main_path / "res"
        values_path = res_path / "values"

        project_root.mkdir(parents=True, exist_ok=True)
        app_module_path.mkdir(parents=True, exist_ok=True)
        src_main_path.mkdir(parents=True, exist_ok=True)
        java_path.mkdir(parents=True, exist_ok=True)
        res_path.mkdir(parents=True, exist_ok=True)
        values_path.mkdir(parents=True, exist_ok=True)

        # Create package directories
        package_dirs = java_path / package_name.replace('.', os.sep)
        package_dirs.mkdir(parents=True, exist_ok=True)

        # Copy template files and modify as needed
        shutil.copy(self.android_manifest_template_path, src_main_path)
        shutil.copy(self.gradle_build_template_path, project_root)
        shutil.copy(self.settings_gradle_template_path, project_root)
        shutil.copy(self.app_gradle_template_path, app_module_path)
        shutil.copy(self.main_activity_template_path, package_dirs)
        shutil.copy(self.strings_xml_template_path, values_path)
        shutil.copy(self.colors_xml_template_path, values_path)
        shutil.copy(self.themes_xml_template_path, values_path)

        # Modify AndroidManifest.xml to use Arabic app name
        manifest_path = src_main_path / "AndroidManifest.xml"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_content = f.read()
        manifest_content = manifest_content.replace("@string/app_name", f'"{app_name_arabic}"') # Direct string for simplicity
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Modify strings.xml to set the Arabic app name
        strings_xml_path = values_path / "strings.xml"
        with open(strings_xml_path, "r", encoding="utf-8") as f:
            strings_content = f.read()
        strings_content = strings_content.replace("<string name=\"app_name\">Generated Arabic App</string>", f'<string name="app_name">{app_name_arabic}</string>')
        with open(strings_xml_path, "w", encoding="utf-8") as f:
            f.write(strings_content)

        # Potentially create activity_main.xml if it's not part of the base template
        activity_main_xml_path = values_path.parent / "layout" / "activity_main.xml"
        if not activity_main_xml_path.exists():
            activity_main_xml_path.parent.mkdir(exist_ok=True)
            with open(activity_main_xml_path, "w", encoding="utf-8") as f:
                f.write(f"""
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".generated.MainActivity">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/welcome_message"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
                """)


        return project_root

    def generate_apk(self, natural_language_prompt: str, output_apk_path: Path):
        """
        Generates an Android APK from a natural language prompt,
        focusing on Arabic text and basic app structure.
        """
        print(f"--- Generating APK for prompt: '{natural_language_prompt}' ---")

        # 1. Parse the prompt for Arabic-specific elements and app intent
        # This is a simplified parsing. A real system would use Lobe 0 for deep NLP.
        app_name_arabic = "تطبيق عربي"
        if "اسم التطبيق" in natural_language_prompt:
            parts = natural_language_prompt.split("اسم التطبيق")
            if len(parts) > 1:
                potential_name = parts[1].split(".")[0].strip()
                if potential_name:
                    app_name_arabic = potential_name

        package_name = "com.example.generated" # Default, can be extracted from prompt

        # Generate a unique project name
        project_name = f"arabic_app_{hash(natural_language_prompt) % 10000}"
        project_root = self._create_project_structure(project_name, app_name_arabic, package_name)

        # 2. Prepare build environment and execute Gradle
        print(f"--- Building APK using Gradle in {project_root} ---")

        # Ensure necessary tools are available
        if not JAVA_SDK_PATH:
            raise EnvironmentError("JAVA_HOME environment variable is not set. Please set it to your Java SDK path.")
        if not ANDROID_SDK_ROOT:
            raise EnvironmentError("ANDROID_SDK_ROOT environment variable is not set. Please set it to your Android SDK path.")

        # Construct path to Gradle wrapper
        gradle_wrapper_path = project_root / "gradlew"
        if os.name == 'nt': # Windows
            gradle_wrapper_path = project_root / "gradlew.bat"

        # Ensure gradlew exists and is executable
        if not gradle_wrapper_path.exists():
            print("Gradle wrapper not found. Attempting to create it (requires Gradle installation).")
            try:
                # This is a simplification; a robust solution would involve downloading Gradle or using a pre-existing installation.
                # For demonstration, assume 'gradle' command is available in PATH.
                subprocess.run(["gradle", "wrapper", "--gradle-version", "8.5"], cwd=project_root, check=True)
                print("Gradle wrapper created successfully.")
            except FileNotFoundError:
                raise FileNotFoundError("Gradle command not found. Please ensure Gradle is installed and in your PATH, or provide a path to the Gradle distribution.")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to create Gradle wrapper: {e}")

        # Execute Gradle build
        try:
            print("Running Gradle build...")
            # Use the Gradle wrapper to build the project
            # We will build a debug APK.
            build_command = [str(gradle_wrapper_path), "assembleDebug"]

            # Set JAVA_HOME for the subprocess if it's not already inherited
            env = os.environ.copy()
            env["JAVA_HOME"] = JAVA_SDK_PATH
            env["ANDROID_SDK_ROOT"] = ANDROID_SDK_ROOT # Ensure Android SDK is known

            process = subprocess.Popen(build_command, cwd=project_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print("Gradle build failed. Errors:")
                print(stderr)
                raise RuntimeError(f"Gradle build failed with return code {process.returncode}")

            print("Gradle build successful.")
            # print("Gradle stdout:")
            # print(stdout)
            # print("Gradle stderr:")
            # print(stderr)

            # Locate the generated APK
            # Debug APKs are typically located in app/build/outputs/apk/debug/
            debug_apk_path = project_root / "app" / "build" / "outputs" / "apk" / "debug" / f"{project_name}-debug.apk"

            if not debug_apk_path.exists():
                # Fallback path if the structure differs slightly
                fallback_debug_apk_path = project_root / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
                if fallback_debug_apk_path.exists():
                    debug_apk_path = fallback_debug_apk_path
                else:
                    raise FileNotFoundError(f"Could not find the generated debug APK. Expected at {debug_apk_path} or {fallback_debug_apk_path}")

            # Move the generated APK to the desired output path
            shutil.move(str(debug_apk_path), str(output_apk_path))
            print(f"Successfully generated APK: {output_apk_path}")

        except FileNotFoundError:
            print("Error: Gradle wrapper or Java/Android SDK tools not found. Ensure they are correctly configured.")
            raise
        except Exception as e:
            print(f"An error occurred during APK generation: {e}")
            raise
        finally:
            # Optional: Clean up temporary project directory
            # print(f"Cleaning up temporary project directory: {project_root}")
            # shutil.rmtree(project_root)
            pass # Keep for debugging if needed

# Example Usage (for testing purposes, not part of the final output)
if __name__ == "__main__":
    import shutil

    # Create necessary directories if they don't exist
    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # Mock environment variables if not set
    if not os.environ.get("JAVA_HOME"):
        print("Warning: JAVA_HOME not set. Mocking with a placeholder.")
        os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64" # Example path
    if not os.environ.get("ANDROID_SDK_ROOT"):
        print("Warning: ANDROID_SDK_ROOT not set. Mocking with a placeholder.")
        os.environ["ANDROID_SDK_ROOT"] = "/home/user/Android/Sdk" # Example path

    try:
        arabic_generator = ArabicAPKGenerator(KNOWLEDGE_BASE_DIR, TEMP_DIR)

        # Ensure templates are in place (if running this script directly for the first time)
        arabic_generator._ensure_templates()

        prompt = "إنشاء تطبيق بسيط باللغة العربية باسم 'تطبيق الترجمة'."
        output_apk = TEMP_DIR / "translation_app.apk"

        # Clean up previous runs
        if output_apk.exists():
            output_apk.unlink()
        if (TEMP_DIR / "arabic_app_1234").exists(): # Adjust project name based on hash if needed
            shutil.rmtree(TEMP_DIR / "arabic_app_1234")

        arabic_generator.generate_apk(prompt, output_apk)

        print(f"\nAPK generation process completed. Check '{output_apk}'")

    except (EnvironmentError, FileNotFoundError, RuntimeError) as e:
        print(f"\nError during example execution: {e}")
        print("Please ensure JAVA_HOME and ANDROID_SDK_ROOT are correctly set and that you have the Android SDK and build tools installed.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    # --- Mocking debug.keystore cleanup ---
    # This part simulates the cleanup logic from Lobe 8, ensuring it doesn't interfere.
    debug_keystore_path = Path("~/.android/debug.keystore").expanduser()
    if debug_keystore_path.exists():
        print("\n--- Mocking debug.keystore cleanup ---")
        print(f"Mocking cleanup for: {debug_keystore_path}")
        # In a real scenario, this would involve deleting the file.
        # For this mock, we just acknowledge it.
        print("Mock cleanup successful (file was not actually deleted).")