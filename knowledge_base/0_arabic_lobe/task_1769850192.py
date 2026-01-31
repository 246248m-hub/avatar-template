import os
import shutil

KNOWLEDGE_BASE_DIR = "knowledge_base"
PROJECT_TEMPLATES_DIR = "project_templates"

def _create_directory_if_not_exists(path):
    """Creates a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def _copy_project_template(template_name, target_path):
    """Copies a project template to the target path."""
    template_source = os.path.join(PROJECT_TEMPLATES_DIR, template_name)
    if not os.path.exists(template_source):
        raise FileNotFoundError(f"Project template '{template_name}' not found at '{template_source}'.")
    shutil.copytree(template_source, target_path)
    print(f"Copied project template '{template_name}' to '{target_path}'.")

def _generate_android_manifest(package_name, app_name, target_dir):
    """Generates a basic AndroidManifest.xml."""
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
        <activity android:name=".MainActivity" android:label="@string/{app_name.lower().replace(' ', '_')}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_path = os.path.join(target_dir, "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"Generated AndroidManifest.xml at '{manifest_path}'.")

def _generate_string_resources(app_name, target_dir):
    """Generates a basic strings.xml."""
    string_resources_content = f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    strings_xml_path = os.path.join(target_dir, "res", "values", "strings.xml")
    _create_directory_if_not_exists(os.path.dirname(strings_xml_path))
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(string_resources_content)
    print(f"Generated strings.xml at '{strings_xml_path}'.")

def _generate_main_activity_java(package_name, app_name, target_dir):
    """Generates a basic MainActivity.java file."""
    main_activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists

        // Example: Set app name to a TextView
        TextView appNameView = findViewById(R.id.app_name_text_view); // Assuming a TextView with this ID
        if (appNameView != null) {{
            appNameView.setText("{app_name}");
        }}
    }}
}}
"""
    main_activity_path = os.path.join(target_dir, "src", "main", "java", *package_name.split('.'))
    _create_directory_if_not_exists(main_activity_path)
    with open(os.path.join(main_activity_path, "MainActivity.java"), "w", encoding="utf-8") as f:
        f.write(main_activity_content)
    print(f"Generated MainActivity.java at '{os.path.join(main_activity_path, 'MainActivity.java')}'.")

def _generate_activity_main_xml(app_name, target_dir):
    """Generates a basic activity_main.xml file."""
    activity_main_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/app_name_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{app_name}"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    activity_main_xml_path = os.path.join(target_dir, "res", "layout", "activity_main.xml")
    _create_directory_if_not_exists(os.path.dirname(activity_main_xml_path))
    with open(activity_main_xml_path, "w", encoding="utf-8") as f:
        f.write(activity_main_content)
    print(f"Generated activity_main.xml at '{activity_main_xml_path}'.")

def _generate_build_gradle(package_name, target_dir):
    """Generates a basic build.gradle file."""
    build_gradle_content = f"""plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin support might be useful later
}}

android {{
    compileSdk 33 // Example target SDK

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21 // Example min SDK
        targetSdk 33 // Example target SDK
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
    build_gradle_path = os.path.join(target_dir, "build.gradle")
    with open(build_gradle_path, "w", encoding="utf-8") as f:
        f.write(build_gradle_content)
    print(f"Generated build.gradle at '{build_gradle_path}'.")

def _generate_settings_gradle(project_root_dir, target_dir):
    """Generates a basic settings.gradle file."""
    settings_gradle_content = f"""pluginManagement {{
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

rootProject.name = "GeneratedApp"
include ':app'
"""
    settings_gradle_path = os.path.join(project_root_dir, "settings.gradle") # settings.gradle is at the root
    with open(settings_gradle_path, "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)
    print(f"Generated settings.gradle at '{settings_gradle_path}'.")


class AndroidProjectGenerator:
    """
    Module responsible for generating the basic structure of an Android APK project.
    It creates necessary directories, manifest files, resource files, and source code.
    """
    def __init__(self, project_root_dir="generated_apk_project", package_name="com.example.generatedapp", app_name="GeneratedApp"):
        self.project_root_dir = project_root_dir
        self.package_name = package_name
        self.app_name = app_name
        self.app_module_dir = os.path.join(self.project_root_dir, "app")

    def create_project_structure(self):
        """
        Creates the directory structure for the Android project.
        """
        print(f"\n--- Creating Android Project Structure in '{self.project_root_dir}' ---")
        _create_directory_if_not_exists(self.project_root_dir)
        _create_directory_if_not_exists(self.app_module_dir)
        _create_directory_if_not_exists(os.path.join(self.app_module_dir, "src", "main", "java", *self.package_name.split('.')))
        _create_directory_if_not_exists(os.path.join(self.app_module_dir, "src", "main", "res", "layout"))
        _create_directory_if_not_exists(os.path.join(self.app_module_dir, "src", "main", "res", "values"))
        print("Android project directory structure created.")

    def generate_android_files(self):
        """
        Generates core Android project files like Manifest, strings.xml, MainActivity, and build.gradle.
        """
        print("\n--- Generating Core Android Project Files ---")
        _generate_android_manifest(self.package_name, self.app_name, self.app_module_dir)
        _generate_string_resources(self.app_name, self.app_module_dir)
        _generate_main_activity_java(self.package_name, self.app_name, self.app_module_dir)
        _generate_activity_main_xml(self.app_name, self.app_module_dir)
        _generate_build_gradle(self.package_name, self.app_module_dir)
        _generate_settings_gradle(self.project_root_dir, self.app_module_dir)
        print("Core Android project files generated.")

    def build_apk_structure(self, arabic_prompt: str):
        """
        Orchestrates the generation of the basic Android project structure
        based on an Arabic prompt.
        """
        print(f"\n--- Initiating APK Structure Generation for Arabic Prompt: '{arabic_prompt[:50]}...' ---")
        # Basic structure generation, can be extended with more complex logic
        # based on the prompt in future iterations.
        self.create_project_structure()
        self.generate_android_files()
        print(f"\n--- APK Structure Generation Complete. Project created at: '{self.project_root_dir}' ---")
        return self.project_root_dir


# Example of how this module might be called (for testing or integration)
if __name__ == "__main__":
    # Ensure necessary directories exist for templates if they were to be used
    _create_directory_if_not_exists(PROJECT_TEMPLATES_DIR)
    _create_directory_if_not_exists(KNOWLEDGE_BASE_DIR)

    # Clean up previous runs if they exist
    if os.path.exists("generated_apk_project"):
        shutil.rmtree("generated_apk_project")
    if os.path.exists("generated_apk_project_arabic"):
        shutil.rmtree("generated_apk_project_arabic")

    # --- Demo for Lobe 0_arabic_lobe ---
    # This part simulates the call from Lobe 0_arabic_lobe,
    # assuming it produces a package name and app name.
    # In a real scenario, Lobe 0_arabic_lobe would parse the prompt
    # to extract these details and potentially more for customization.

    print("\n--- Demoing AndroidProjectGenerator for Arabic Input ---")
    arabic_demo_project_generator = AndroidProjectGenerator(
        project_root_dir="generated_apk_project_arabic",
        package_name="com.example.arabicgenerated",
        app_name="تطبيق عربي" # Arabic for "Arabic App"
    )
    simulated_arabic_prompt = "أنشئ تطبيق أندرويد بسيط باسم 'تطبيق عربي' بحزمة 'com.example.arabicgenerated'."
    generated_project_path = arabic_demo_project_generator.build_apk_structure(simulated_arabic_prompt)

    if os.path.exists(generated_project_path):
        print(f"\nDemo successful: APK project structure was generated at '{generated_project_path}'.")
    else:
        print("\nDemo failed: APK project structure generation did not complete successfully.")

    print("\n--- Arabic APK Structure Generator Module Demo Finished ---")

    # --- Clean up dummy files ---
    print("\n--- Cleaning up dummy files ---")
    if os.path.exists("generated_apk_project_arabic"):
        shutil.rmtree("generated_apk_project_arabic")
    print("Dummy files cleaned up.")