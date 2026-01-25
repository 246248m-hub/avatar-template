# Lobe 4_code_generation_lobe

import os
import re

# Assume these are defined in other lobes or globally
# For demonstration, we'll define them here
APP_TEMPLATE_DIR = "app_templates"
TEMP_PROJ_DIR = "temp_projects"
MAIN_ACTIVITY_TEMPLATE = "MainActivity.java.template"
GRADLE_BUILD_TEMPLATE = "build.gradle.template"

def sanitize_filename(name):
    """Sanitizes a string to be a valid Python module name or filename."""
    name = re.sub(r'\W+', '_', name)
    return name.lower()

def create_java_activity(activity_name, package_name):
    """
    Generates a basic Java Activity file content.
    This is a placeholder for more sophisticated generation based on prompt.
    """
    sanitized_activity_name = sanitize_filename(activity_name)
    java_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Example import

public class {sanitized_activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{sanitized_activity_name.lower()}); // Assumes layout file

        // Example: Setting text on a TextView
        TextView welcomeText = findViewById(R.id.welcome_text); // Assumes a TextView with this ID
        if (welcomeText != null) {{
            welcomeText.setText("Welcome to {activity_name}!");
        }}
    }}
}}
"""
    return java_code

def create_layout_xml(activity_name):
    """
    Generates a basic XML layout file content for an activity.
    This is a placeholder for more sophisticated generation based on prompt.
    """
    sanitized_activity_name_lower = sanitize_filename(activity_name).lower()
    xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{sanitized_activity_name_lower.capitalize()}Activity">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    return xml_content

def generate_android_project_structure(app_name, package_name, main_activity_name):
    """
    Generates a basic Android project directory structure and initial files.
    This function takes NLP-derived app and package names and generates
    the foundational code for an Android application.
    """
    print(f"\n--- Generating Android Project Structure for '{app_name}' ---")
    sanitized_app_name = sanitize_filename(app_name)
    sanitized_package_name = sanitize_filename(package_name)
    sanitized_main_activity_name = sanitize_filename(main_activity_name)

    project_root = os.path.join(TEMP_PROJ_DIR, sanitized_app_name)
    app_source_dir = os.path.join(project_root, "app", "src", "main")
    java_package_dir = os.path.join(app_source_dir, "java", *sanitized_package_name.split('.'))
    res_layout_dir = os.path.join(app_source_dir, "res", "layout")

    os.makedirs(java_package_dir, exist_ok=True)
    os.makedirs(res_layout_dir, exist_ok=True)

    # Create main activity
    main_activity_code = create_java_activity(sanitized_main_activity_name, sanitized_package_name)
    main_activity_path = os.path.join(java_package_dir, f"{sanitized_main_activity_name}.java")
    with open(main_activity_path, "w", encoding="utf-8") as f:
        f.write(main_activity_code)
    print(f"Created MainActivity: {main_activity_path}")

    # Create layout file for main activity
    layout_xml_content = create_layout_xml(sanitized_main_activity_name)
    layout_xml_path = os.path.join(res_layout_dir, f"activity_{sanitized_main_activity_name.lower()}.xml")
    with open(layout_xml_path, "w", encoding="utf-8") as f:
        f.write(layout_xml_content)
    print(f"Created Layout file: {layout_xml_path}")

    # Create AndroidManifest.xml (simplified)
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{sanitized_package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{sanitized_app_name}">
        <activity android:name=".{sanitized_main_activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_path = os.path.join(app_source_dir, "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"Created AndroidManifest.xml: {manifest_path}")

    # Create build.gradle (simplified)
    # This would ideally be templated and modified based on prompt requirements.
    gradle_content = f"""plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin is also considered
}}

android {{
    namespace '{sanitized_package_name}'
    compileSdk 33 // Example SDK version

    defaultConfig {{
        applicationId "{sanitized_package_name}"
        minSdk 24 // Example min SDK version
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
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
    gradle_path = os.path.join(project_root, "build.gradle")
    with open(gradle_path, "w", encoding="utf-8") as f:
        f.write(gradle_content)
    print(f"Created build.gradle: {gradle_path}")

    # Create settings.gradle (simplified)
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

rootProject.name = "{sanitized_app_name}"
include ':app'
"""
    settings_gradle_path = os.path.join(project_root, "settings.gradle")
    with open(settings_gradle_path, "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)
    print(f"Created settings.gradle: {settings_gradle_path}")

    # Create .gitignore (simplified)
    gitignore_content = """
# Built application files
*.apk
*.ap_
*.aab

# Files for the Dalvik VM
*.dex

# Production files
*.o
*.so

# Debug files
*.log
debug/
proguard/

# Eclipse
.classpath
.project
.settings/
bin/
gen/

# IntelliJ
*.iml
.idea/
*.ipr
*.iml
.mvn/
.gradle/
build/

# Gradle
.gradle/
build/
"""
    gitignore_path = os.path.join(project_root, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print(f"Created .gitignore: {gitignore_path}")

    print(f"--- Android Project Structure Generation Complete for '{app_name}' ---")
    return project_root

# Example Usage (simulating input from previous lobes)
# The following would be triggered by a successful parsing of a prompt that
# describes an app with a main activity.
if __name__ == "__main__":
    # Mocking data that might come from Lobe 0_language_lobe or a similar parser
    # that extracts app name, package name, and main activity name from natural language.
    # This is a simplified example; real extraction would be more complex.
    parsed_app_description = {
        "app_name": "MyAwesomeApp",
        "package_name": "com.example.myawesomeapp",
        "main_activity_name": "WelcomeActivity"
    }

    # Ensure temporary directories exist
    os.makedirs(TEMP_PROJ_DIR, exist_ok=True)

    generated_project_path = generate_android_project_structure(
        app_name=parsed_app_description["app_name"],
        package_name=parsed_app_description["package_name"],
        main_activity_name=parsed_app_description["main_activity_name"]
    )
    print(f"\nGenerated project structure at: {generated_project_path}")

    print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe ---")