import os
import shutil

# --- Constants (assuming these are defined elsewhere or will be defined) ---
GENERATED_CODE_DIR = "generated_code"
KNOWLEDGE_BASE_DIR = "knowledge_base"
BUILD_GRADLE_TEMPLATE = "build.gradle.template"
JAVA_PROJECT_DIR = "android_project"
MAIN_ACTIVITY_TEMPLATE = "MainActivity.java.template"
MANIFEST_TEMPLATE = "AndroidManifest.xml.template"
RES_LAYOUT_MAIN_TEMPLATE = "res_layout_main.xml.template"

# --- Mock functions for demonstration purposes ---
def cleanup_template_files():
    """Mocks cleanup of template files."""
    print("Cleaning up template files (mock)...")
    pass

def cleanup_dummy_files():
    """Mocks cleanup of dummy files."""
    print("Cleaning up dummy files (mock)...")
    pass

def le_file(template_path, output_path, package_name):
    """Mocks reading a template and writing to a file with package name substitution."""
    print(f"Processing template '{template_path}' to '{output_path}' for package '{package_name}' (mock)...")
    # In a real scenario, this would read the template, perform substitutions, and write.
    with open(output_path, "w") as f:
        f.write(f"// Mock content for {output_path}\n")
        f.write(f"package {package_name};\n")
    return output_path

def c_text(prompt, knowledge_base_path):
    """Mocks generating text from a prompt using a knowledge base."""
    print(f"Generating text for prompt '{prompt}' from '{knowledge_base_path}' (mock)...")
    # In a real scenario, this would involve NLP processing.
    return f"Generated response for '{prompt}'."

def create_directory_if_not_exists(dir_path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

def build_gradle_content(package_name):
    """Generates the content for the build.gradle file."""
    return f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId '{package_name}'
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
}}

dependencies {{

    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""

def main_activity_content(package_name):
    """Generates the content for the MainActivity.java file."""
    return f"""
package {package_name};

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

def manifest_content(package_name):
    """Generates the content for the AndroidManifest.xml file."""
    return f"""
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
        android:theme="@style/Theme.YourAppName"
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

def res_layout_main_content():
    """Generates the content for res/layout/activity_main.xml file."""
    return """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

class Lobe4CodeGeneration:
    """
    Lobe 4: Code Generation Lobe.
    Responsible for generating the foundational structure of an Android APK
    from natural language descriptions or intents.
    """

    def __init__(self):
        self.package_name = "com.example.myapp"  # Default package name
        self.generated_code_dir = GENERATED_CODE_DIR
        self.java_project_dir = JAVA_PROJECT_DIR

    def set_package_name(self, package_name: str):
        """Sets the package name for the generated APK."""
        self.package_name = package_name
        print(f"Package name set to: {self.package_name}")

    def create_project_structure(self):
        """Creates the necessary directory structure for an Android project."""
        print("\n--- Creating Android project structure ---")
        create_directory_if_not_exists(self.java_project_dir)
        app_dir = os.path.join(self.java_project_dir, "app")
        create_directory_if_not_exists(app_dir)
        src_dir = os.path.join(app_dir, "src")
        create_directory_if_not_exists(src_dir)
        main_dir = os.path.join(src_dir, "main")
        create_directory_if_not_exists(main_dir)
        java_package_dir = os.path.join(main_dir, "java", *self.package_name.split('.'))
        create_directory_if_not_exists(java_package_dir)
        res_dir = os.path.join(main_dir, "res")
        create_directory_if_not_exists(res_dir)
        layout_dir = os.path.join(res_dir, "layout")
        create_directory_if_not_exists(layout_dir)
        # Add other resource directories as needed (values, drawable, etc.)
        values_dir = os.path.join(res_dir, "values")
        create_directory_if_not_exists(values_dir)

        print(f"Android project structure created in: {self.java_project_dir}")

    def generate_build_gradle(self):
        """Generates the build.gradle file."""
        print("\n--- Generating build.gradle ---")
        build_gradle_path = os.path.join(self.java_project_dir, "build.gradle")
        with open(build_gradle_path, "w") as f:
            f.write(build_gradle_content(self.package_name))
        print(f"Generated build.gradle at: {build_gradle_path}")

    def generate_main_activity(self):
        """Generates the MainActivity.java file."""
        print("\n--- Generating MainActivity.java ---")
        java_package_dir = os.path.join(self.java_project_dir, "app", "src", "main", "java", *self.package_name.split('.'))
        main_activity_path = os.path.join(java_package_dir, "MainActivity.java")
        with open(main_activity_path, "w") as f:
            f.write(main_activity_content(self.package_name))
        print(f"Generated MainActivity.java at: {main_activity_path}")

    def generate_manifest(self):
        """Generates the AndroidManifest.xml file."""
        print("\n--- Generating AndroidManifest.xml ---")
        manifest_path = os.path.join(self.java_project_dir, "app", "src", "main", "AndroidManifest.xml")
        with open(manifest_path, "w") as f:
            f.write(manifest_content(self.package_name))
        print(f"Generated AndroidManifest.xml at: {manifest_path}")

    def generate_layout_file(self):
        """Generates the res/layout/activity_main.xml file."""
        print("\n--- Generating res/layout/activity_main.xml ---")
        layout_dir = os.path.join(self.java_project_dir, "app", "src", "main", "res", "layout")
        layout_path = os.path.join(layout_dir, "activity_main.xml")
        with open(layout_path, "w") as f:
            f.write(res_layout_main_content())
        print(f"Generated activity_main.xml at: {layout_path}")

    def generate_android_project(self, natural_language_input: str):
        """
        Generates the basic structure of an Android project from natural language input.
        This is a simplified example. A real implementation would parse the
        `natural_language_input` to determine package name, app name, etc.
        """
        print("\n--- Lobe 4: Code Generation Lobe ---")
        print(f"Received natural language input: '{natural_language_input}'")

        # In a real scenario, Lobe 0_language_lobe or a dedicated parser would
        # extract the package name from `natural_language_input`.
        # For this demo, we'll use a placeholder or a fixed value if not provided.
        # For demonstration, let's assume the input itself can dictate the package name.
        # This is a placeholder for a more sophisticated NLP extraction.
        potential_package_name = natural_language_input.lower().replace(" ", "").replace("-", "")
        if "." not in potential_package_name or len(potential_package_name.split('.')) < 2:
            self.set_package_name(f"com.example.{potential_package_name if potential_package_name else 'myapp'}")
        else:
            self.set_package_name(potential_package_name)

        self.create_project_structure()
        self.generate_build_gradle()
        self.generate_main_activity()
        self.generate_manifest()
        self.generate_layout_file()

        print("\n--- Lobe 4_code_generation_lobe Demo Finished ---")

    def cleanup_generated_code(self):
        """Cleans up the generated code directory and project directory."""
        print("\n--- Cleaning up generated code and project directories ---")
        if os.path.exists(self.generated_code_dir):
            shutil.rmtree(self.generated_code_dir)
            print(f"Removed dummy generated code directory: {self.generated_code_dir}")
        if os.path.exists(self.java_project_dir):
            shutil.rmtree(self.java_project_dir)
            print(f"Removed generated project directory: {self.java_project_dir}")

# Example Usage (demonstrating Lobe 4's functionality)
if __name__ == "__main__":
    code_generator = Lobe4CodeGeneration()
    # Simulate a natural language input that could be parsed for package name
    nl_input = "Create a simple Android app named My First App"
    code_generator.generate_android_project(nl_input)

    # Clean up after the demo
    code_generator.cleanup_generated_code()

    print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe ---")
    # In a real workflow, the output of this lobe (the project structure)
    # would be passed to Lobe 8_apk_compiler_lobe.