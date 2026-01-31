import os
import shutil
import subprocess

# Assuming these paths are defined elsewhere or can be determined dynamically
KNOWLEDGE_BASE_DIR = "knowledge_base"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def setup_project_directory(project_name="my_arabic_app"):
    """Creates the necessary project directory structure."""
    project_path = os.path.join(PROJECT_ROOT, project_name)
    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "java", "com", "example", project_name.replace(" ", "_").lower()), exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "values"), exist_ok=True)
    return project_path

def generate_android_manifest(project_path, package_name):
    """Generates a basic AndroidManifest.xml file."""
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{package_name.split('.')[-1].capitalize()}">

        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_dir = os.path.join(project_path, "app", "src", "main")
    os.makedirs(manifest_dir, exist_ok=True)
    with open(os.path.join(manifest_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

def generate_activity_file(project_path, package_name, activity_name="MainActivity"):
    """Generates a basic Activity Java file."""
    activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{activity_name.lower()}); // Assuming a layout file with the same name
    }}
}}
"""
    activity_dir = os.path.join(project_path, "app", "src", "main", "java", *package_name.split('.'))
    os.makedirs(activity_dir, exist_ok=True)
    with open(os.path.join(activity_dir, f"{activity_name}.java"), "w", encoding="utf-8") as f:
        f.write(activity_content)

def generate_layout_file(project_path, layout_name="main_activity"):
    """Generates a basic layout XML file."""
    layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.capitalize()}">

    <!-- Add your UI elements here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    layout_dir = os.path.join(project_path, "app", "src", "main", "res", "layout")
    os.makedirs(layout_dir, exist_ok=True)
    with open(os.path.join(layout_dir, f"{layout_name}.xml"), "w", encoding="utf-8") as f:
        f.write(layout_content)

def generate_strings_xml(project_path, app_name="MyArabicApp"):
    """Generates a basic strings.xml file."""
    strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    strings_dir = os.path.join(project_path, "app", "src", "main", "res", "values")
    os.makedirs(strings_dir, exist_ok=True)
    with open(os.path.join(strings_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_content)

def generate_gradle_files(project_path, package_name):
    """Generates basic build.gradle files."""
    # app/build.gradle
    app_build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin might be used later or for compatibility
}}

android {{
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
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

    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
    os.makedirs(os.path.join(project_path, "app"), exist_ok=True)
    with open(os.path.join(project_path, "app", "build.gradle"), "w", encoding="utf-8") as f:
        f.write(app_build_gradle_content)

    # project/build.gradle
    project_build_gradle_content = f"""
// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {{
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.0' apply false // Match with app/build.gradle
}}

task clean(type: Delete) {{
    delete rootProject.buildDir
}}
"""
    with open(os.path.join(project_path, "build.gradle"), "w", encoding="utf-8") as f:
        f.write(project_build_gradle_content)

    # settings.gradle
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
rootProject.name = "{package_name.split('.')[-1]}"
include ':app'
"""
    with open(os.path.join(project_path, "settings.gradle"), "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)

class ArabicAndroidProjectBuilder:
    """
    This module is responsible for generating the foundational structure
    of an Android APK project, specifically tailored for Arabic language
    support and content. It leverages the Arabic text and code generation
    capabilities of other lobes to populate the project.
    """
    def __init__(self, project_name="arabic_generated_app", app_name_arabic="تطبيق عربي"):
        self.project_name = project_name
        self.app_name_arabic = app_name_arabic
        self.project_path = None
        self.package_name = f"com.example.{self.project_name.replace(' ', '_').lower()}"

    def build_base_project(self):
        """
        Constructs the initial directory structure and essential Android configuration files.
        This is the starting point for generating a functional APK.
        """
        print(f"\n--- Building base Android project structure for: {self.project_name} ---")
        self.project_path = setup_project_directory(self.project_name)

        generate_android_manifest(self.project_path, self.package_name)
        generate_activity_file(self.project_path, self.package_name)
        generate_layout_file(self.project_path)
        generate_strings_xml(self.project_path, self.app_name_arabic)
        generate_gradle_files(self.project_path, self.package_name)

        print(f"Base project structure created at: {self.project_path}")
        return self.project_path

    def integrate_arabic_content(self, arabic_text_data):
        """
        Integrates Arabic text content into the Android project.
        This method acts as a bridge, receiving processed Arabic text
        (e.g., for UI elements, resources) and placing it into the
        appropriate project files.

        Args:
            arabic_text_data (dict): A dictionary containing Arabic text,
                                     structured by where it should be placed
                                     (e.g., {'strings': {'app_name': 'اسم التطبيق'}}).
        """
        print("\n--- Integrating Arabic content into the project ---")
        if not self.project_path:
            print("Project path not set. Call build_base_project() first.")
            return

        # Update strings.xml with provided Arabic app name
        if 'strings' in arabic_text_data and 'app_name' in arabic_text_data['strings']:
            strings_xml_path = os.path.join(self.project_path, "app", "src", "main", "res", "values", "strings.xml")
            with open(strings_xml_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            updated_lines = []
            for line in lines:
                if '<string name="app_name">' in line:
                    updated_lines.append(f'    <string name="app_name">{arabic_text_data["strings"]["app_name"]}</string>\n')
                else:
                    updated_lines.append(line)

            with open(strings_xml_path, "w", encoding="utf-8") as f:
                f.writelines(updated_lines)
            print(f"Updated app_name in strings.xml to: {arabic_text_data['strings']['app_name']}")

        # TODO: Extend this to handle other Arabic text placements,
        #       like dynamic UI generation based on Arabic descriptions.
        #       This would likely involve interacting with Lobe 4 (code_generation_lobe)
        #       to generate Java/Kotlin code or XML layouts.

        print("Arabic content integration complete (basic app_name updated).")

    def finalize_project_structure(self):
        """
        Performs any final structural adjustments or cleanup before
        the project is ready for compilation.
        """
        print("\n--- Finalizing project structure ---")
        # Ensure all necessary directories are present (though build_base_project should cover this)
        os.makedirs(os.path.join(self.project_path, "app", "src", "main", "res", "drawable"), exist_ok=True)
        os.makedirs(os.path.join(self.project_path, "app", "src", "main", "res", "mipmap"), exist_ok=True)
        print("Project structure finalized.")

    def compile_to_apk(self, output_apk_dir="output_apks"):
        """
        Initiates the process of compiling the Android project into an APK.
        This is a placeholder and would typically involve calling the Android SDK's
        gradle wrapper or a similar build tool.

        Args:
            output_apk_dir (str): The directory where the generated APK will be saved.

        Returns:
            str: The path to the generated APK file, or None if compilation fails.
        """
        print("\n--- Initiating APK compilation ---")
        if not self.project_path:
            print("Project path not set. Call build_base_project() first.")
            return None

        # Clean up previous build artifacts if they exist
        build_dir = os.path.join(self.project_path, "app", "build")
        if os.path.exists(build_dir):
            print(f"Cleaning previous build directory: {build_dir}")
            shutil.rmtree(build_dir)

        # Ensure the output directory exists
        os.makedirs(output_apk_dir, exist_ok=True)

        # --- Compilation logic ---
        # This is a simplified representation. In a real scenario, you'd execute
        # the Android build process, likely via ./gradlew assembleDebug or assembleRelease
        # from the project's root directory.
        # This requires the Android SDK and Gradle to be installed and configured.

        # Example using subprocess (requires gradlew to be executable and Android SDK configured)
        try:
            print(f"Navigating to project directory: {self.project_path}")
            original_dir = os.getcwd()
            os.chdir(self.project_path)

            # Attempt to run the gradlew command
            # You might need to specify the path to gradlew explicitly if it's not in PATH
            # and ensure it's executable (`chmod +x gradlew`)
            print("Running Gradle assembleDebug...")
            # Use 'gradlew' if available or 'gradle' if it's in system PATH
            gradle_command = ["./gradlew", "assembleDebug"]
            if os.name == 'nt': # Windows
                gradle_command = ["gradlew", "assembleDebug"]

            # Execute the command
            process = subprocess.run(gradle_command, capture_output=True, text=True, check=True)
            print("Gradle build output:\n", process.stdout)
            print("Gradle build errors:\n", process.stderr) # Print stderr even on success to check for warnings

            # Locate the generated APK
            # The exact path can vary slightly based on Gradle version and build type
            apk_path_relative = os.path.join("app", "build", "outputs", "apk", "debug", f"{self.project_name.replace(' ', '_').lower()}-debug.apk")
            generated_apk_path = os.path.join(self.project_path, apk_path_relative)

            if os.path.exists(generated_apk_path):
                final_apk_name = f"{self.project_name.replace(' ', '_').lower()}_v1.0.apk"
                final_apk_path = os.path.join(original_dir, output_apk_dir, final_apk_name)
                shutil.copy(generated_apk_path, final_apk_path)
                print(f"APK successfully compiled and copied to: {final_apk_path}")
                return final_apk_path
            else:
                print(f"Error: Generated APK not found at expected path: {generated_apk_path}")
                return None

        except FileNotFoundError:
            print("Error: gradlew command not found. Ensure it's in your PATH or the project directory.")
            print("Please make sure you have the Android SDK and Gradle installed and configured.")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error during Gradle build: {e}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            return None
        finally:
            # Return to the original directory
            os.chdir(original_dir)

        print("APK compilation process initiated (actual compilation requires Android SDK/Gradle).")
        return None

    def cleanup_project(self):
        """
        Cleans up the generated project directory.
        """
        print("\n--- Cleaning up generated project directory ---")
        if self.project_path and os.path.exists(self.project_path):
            try:
                shutil.rmtree(self.project_path)
                print(f"Cleaned up project directory: {self.project_path}")
            except OSError as e:
                print(f"Error cleaning up directory {self.project_path}: {e}")
        else:
            print("No project directory to clean up.")

# Example Usage (for demonstration purposes, this code would be called by higher-level logic)
if __name__ == "__main__":
    # This block demonstrates how the class might be used.
    # In a real scenario, the inputs would come from other lobes.

    # Simulate input from Lobe 0_language_lobe (Arabic text)
    arabic_content_input = {
        'strings': {
            'app_name': 'تطبيق العربية الذكي'
        },
        # Potentially other data for layouts, activities, etc.
        # 'layouts': {
        #     'main_activity': {'title': 'شاشة رئيسية'}
        # }
    }

    # Initialize the builder
    project_builder = ArabicAndroidProjectBuilder(
        project_name="SmartArabicApp",
        app_name_arabic=arabic_content_input['strings']['app_name']
    )

    # Step 1: Build the base project structure
    built_project_path = project_builder.build_base_project()

    if built_project_path:
        # Step 2: Integrate Arabic content
        project_builder.integrate_arabic_content(arabic_content_input)

        # Step 3: Finalize structure (optional, for any post-integration tweaks)
        project_builder.finalize_project_structure()

        # Step 4: Attempt to compile to APK
        # NOTE: This requires Android SDK and Gradle to be installed and configured
        #       on the system where this code is run.
        print("\n--- Attempting APK compilation (requires Android SDK/Gradle) ---")
        generated_apk = project_builder.compile_to_apk(output_apk_dir="generated_apks")

        if generated_apk:
            print(f"\nAPK successfully generated at: {generated_apk}")
        else:
            print("\nAPK compilation failed or was not attempted due to missing dependencies.")

        # Step 5: Cleanup the project directory
        # project_builder.cleanup_project()
    else:
        print("Base project building failed. Cannot proceed.")

    print("\n--- ArabicAndroidProjectBuilder Demo Finished ---")