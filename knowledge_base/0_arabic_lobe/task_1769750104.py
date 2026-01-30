import os
import shutil
from pathlib import Path

# Define a dummy directory for temporary storage, similar to Lobe 0_arabic_lobe
DUMMY_STORAGE_DIR = Path("./arabic_processing_temp")

class ArabicProjectBuilder:
    """
    This module is responsible for orchestrating the creation of an Android project
    structure based on Arabic natural language descriptions. It leverages other lobes
    for specific tasks.
    """

    def __init__(self, project_root: Path):
        """
        Initializes the ArabicProjectBuilder.

        Args:
            project_root: The root directory where the Android project will be built.
        """
        self.project_root = project_root
        self.project_root.mkdir(parents=True, exist_ok=True)
        print(f"Initialized ArabicProjectBuilder with project root: {self.project_root}")

    def create_project_structure(self, arabic_description: str):
        """
        Builds the basic Android project structure based on an Arabic description.
        This function acts as a high-level orchestrator.

        Args:
            arabic_description: The natural language Arabic description of the project.
        """
        print(f"Starting project structure creation for description: '{arabic_description}'")

        # Placeholder for Lobe 0_arabic_lobe: Parse the Arabic description
        # In a real scenario, this would call a function from Lobe 0 to extract
        # key components like app name, package name, main activity name, etc.
        # For this example, we'll simulate parsed components.
        parsed_components = self._parse_arabic_description(arabic_description)
        app_name = parsed_components.get("app_name", "MyArabicApp")
        package_name = parsed_components.get("package_name", "com.example.myarabicapp")
        main_activity_name = parsed_components.get("main_activity", "MainActivity")

        print(f"Parsed components: App Name='{app_name}', Package='{package_name}', Main Activity='{main_activity_name}'")

        # Create necessary directories
        src_dir = self.project_root / "app" / "src" / "main"
        java_dir = src_dir / "java"
        package_dir = java_dir / package_name.replace('.', '/')
        res_dir = src_dir / "res"
        layout_dir = res_dir / "layout"
        values_dir = res_dir / "values"

        java_dir.mkdir(parents=True, exist_ok=True)
        package_dir.mkdir(parents=True, exist_ok=True)
        layout_dir.mkdir(parents=True, exist_ok=True)
        values_dir.mkdir(parents=True, exist_ok=True)

        print("Created basic Android project directory structure.")

        # Placeholder for Lobe 4_code_generation_lobe: Generate MainActivity.java
        # This would call a function from Lobe 4 to generate Java code.
        self.generate_main_activity(package_dir, main_activity_name, package_name)

        # Placeholder for Lobe 4_code_generation_lobe: Generate activity_main.xml
        # This would call a function from Lobe 4 to generate XML layout.
        self.generate_main_layout(layout_dir, main_activity_name.lower())

        # Placeholder for Lobe 4_code_generation_lobe: Generate strings.xml
        # This would call a function from Lobe 4 to generate strings.
        self.generate_strings_xml(values_dir, app_name)

        # Placeholder for Lobe 4_code_generation_lobe: Generate AndroidManifest.xml
        # This would call a function from Lobe 4 to generate the manifest.
        self.generate_manifest(src_dir, package_name, main_activity_name)

        # Placeholder for Lobe 4_code_generation_lobe: Generate build.gradle (app level)
        # This would call a function from Lobe 4 to generate the build.gradle.
        self.generate_build_gradle(self.project_root / "app", package_name)

        # Placeholder for Lobe 4_code_generation_lobe: Generate build.gradle (project level)
        # This would call a function from Lobe 4 to generate the build.gradle.
        self.generate_project_build_gradle(self.project_root)

        print("Generated core project files.")
        print(f"Android project structure created at: {self.project_root}")

    def _parse_arabic_description(self, arabic_description: str) -> dict:
        """
        Simulates parsing an Arabic description to extract project details.
        In a real implementation, this would involve complex NLP from Lobe 0.
        """
        print(f"Simulating Arabic parsing for: '{arabic_description}'")
        # This is a mock. A real Lobe 0 would analyze the text.
        parsed_data = {
            "app_name": "تطبيق عربي",  # Arabic App
            "package_name": "com.example.arabicapp",
            "main_activity": "MainActivity"
        }
        # Simple keyword matching as a placeholder
        if "اسم التطبيق هو" in arabic_description:
            parts = arabic_description.split("اسم التطبيق هو")
            if len(parts) > 1:
                app_name_arabic = parts[1].split("و")[0].strip()
                parsed_data["app_name"] = app_name_arabic

        if "اسم الحزمة" in arabic_description:
            parts = arabic_description.split("اسم الحزمة")
            if len(parts) > 1:
                package_name_arabic = parts[1].split("و")[0].strip()
                parsed_data["package_name"] = package_name_arabic

        if "النشاط الرئيسي" in arabic_description:
            parts = arabic_description.split("النشاط الرئيسي")
            if len(parts) > 1:
                activity_name_arabic = parts[1].split("و")[0].strip()
                parsed_data["main_activity"] = activity_name_arabic.replace(" ", "") # Remove spaces

        return parsed_data

    def generate_main_activity(self, package_dir: Path, activity_name: str, package_name: str):
        """
        Simulates code generation for MainActivity.java.
        This would be handled by Lobe 4_code_generation_lobe.
        """
        java_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{activity_name.lower()}); // Assumes layout file matches activity name lowercase

        TextView welcomeText = findViewById(R.id.welcome_text);
        welcomeText.setText("مرحباً بك في تطبيقك!"); // Welcome to your app!
    }}
}}
"""
        file_path = package_dir / f"{activity_name}.java"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(java_code)
        print(f"Generated {file_path}")

    def generate_main_layout(self, layout_dir: Path, layout_name: str):
        """
        Simulates code generation for activity_main.xml.
        This would be handled by Lobe 4_code_generation_lobe.
        """
        xml_code = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.capitalize()}">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        android:gravity="center"/>

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        file_path = layout_dir / f"{layout_name}.xml"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xml_code)
        print(f"Generated {file_path}")

    def generate_strings_xml(self, values_dir: Path, app_name: str):
        """
        Simulates code generation for strings.xml.
        This would be handled by Lobe 4_code_generation_lobe.
        """
        xml_code = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
        file_path = values_dir / "strings.xml"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xml_code)
        print(f"Generated {file_path}")

    def generate_manifest(self, src_dir: Path, package_name: str, main_activity_name: str):
        """
        Simulates code generation for AndroidManifest.xml.
        This would be handled by Lobe 4_code_generation_lobe.
        """
        xml_code = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{main_activity_name}">
        <activity android:name=".{main_activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        file_path = src_dir / "AndroidManifest.xml"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xml_code)
        print(f"Generated {file_path}")

    def generate_build_gradle(self, app_module_dir: Path, package_name: str):
        """
        Simulates code generation for app/build.gradle.
        This would be handled by Lobe 4_code_generation_lobe.
        """
        gradle_code = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming potential Kotlin usage
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId "{package_name}"
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
        file_path = app_module_dir / "build.gradle"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(gradle_code)
        print(f"Generated {file_path}")

    def generate_project_build_gradle(self, project_root: Path):
        """
        Simulates code generation for project-level build.gradle.
        This would be handled by Lobe 4_code_generation_lobe.
        """
        gradle_code = f"""
// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {{
    id 'com.android.application' version '8.1.1' apply false
    id 'com.android.library' version '8.1.1' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.0' apply false
}}
"""
        file_path = project_root / "build.gradle"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(gradle_code)
        print(f"Generated {file_path}")

    def cleanup(self):
        """
        Cleans up the generated project directory.
        This mirrors the cleanup logic from Lobe 0_arabic_lobe.
        """
        if self.project_root.exists():
            print(f"Cleaning up project directory: {self.project_root}")
            shutil.rmtree(self.project_root)

# Example of how this module would be called by other lobes
if __name__ == "__main__":
    # Example usage:
    print("--- Demonstrating ArabicProjectBuilder Module ---")

    # Define a temporary root for the project
    temp_project_root = Path("./temp_android_project")

    # Initialize the builder
    builder = ArabicProjectBuilder(project_root=temp_project_root)

    # Provide an Arabic description of the project
    arabic_project_description = "أنشئ لي تطبيق أندرويد جديد. اسم التطبيق هو تطبيق مراقبة المهام، واسم الحزمة هو com.example.taskmonitor، والنشاط الرئيسي هو MainScreenActivity."

    try:
        # Orchestrate the project creation
        builder.create_project_structure(arabic_project_description)
        print("\n--- Project structure generation complete. ---")
        print(f"Project files can be found in: {temp_project_root}")

        # Simulate Lobe 8_apk_compiler_lobe's call to build/compile (this module doesn't compile, just builds structure)
        print("\n--- Simulating next step: Lobe 8_apk_compiler_lobe ---")
        print("Lobe 8 would now take the generated project structure and attempt to compile it.")

    except Exception as e:
        print(f"An error occurred during project building: {e}")
    finally:
        # Clean up the generated project directory
        builder.cleanup()
        print("\n--- ArabicProjectBuilder Module Demo Finished ---")