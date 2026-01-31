import os
import re
import json
from pathlib import Path

# Assume existence of these helper functions/classes from other lobes
# from lobe_4_code_generation_lobe import generate_java_code
# from lobe_0_arabic_lobe import parse_arabic_to_structure

# Placeholder for a more sophisticated Arabic parsing and structure generation
def parse_arabic_to_structure(arabic_text: str) -> dict:
    """
    Parses Arabic natural language into a structured representation.
    This is a simplified placeholder. A real implementation would involve
    advanced NLP techniques for Arabic.
    """
    # Example: "Create an app that says hello world"
    # Expected structure: {'action': 'create_app', 'components': [{'type': 'text_view', 'content': 'Hello, World!'}]}

    # Very basic pattern matching for demonstration
    app_creation_match = re.search(r"create an app that says (.+)", arabic_text, re.IGNORECASE)
    if app_creation_match:
        message = app_creation_match.group(1).strip()
        return {
            'action': 'create_app',
            'components': [
                {'type': 'text_view', 'content': message}
            ]
        }

    # Add more patterns for other app functionalities (e.g., buttons, input fields)
    return {"error": "Unsupported Arabic command"}

# Placeholder for Java code generation
def generate_java_code(app_structure: dict) -> str:
    """
    Generates Java code for an Android app based on the provided structure.
    This is a simplified placeholder. A real implementation would generate
    Activity, Layout XML, etc.
    """
    if app_structure.get('action') == 'create_app' and app_structure.get('components'):
        component = app_structure['components'][0]
        if component.get('type') == 'text_view':
            message = component.get('content', 'Hello, World!')
            java_code = f"""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("{message}");
    }}
}}
"""
            return java_code
    return "// Java code generation failed or structure not supported"

# Placeholder for XML layout generation
def generate_xml_layout(app_structure: dict) -> str:
    """
    Generates XML layout for an Android app based on the provided structure.
    This is a simplified placeholder.
    """
    if app_structure.get('action') == 'create_app' and app_structure.get('components'):
        component = app_structure['components'][0]
        if component.get('type') == 'text_view':
            message = component.get('content', 'Hello, World!')
            xml_layout = f"""<?xml version="1.0" encoding="utf-8"?>
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
        android:text="{message}"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
            return xml_layout
    return "<!-- XML layout generation failed or structure not supported -->"


class Lobe4CodeGeneration:
    def __init__(self, project_root: Path = Path("./generated_android_project")):
        self.project_root = project_root
        self.package_name = "com.example.myapp"
        self.main_activity_java_path = self.project_root / "app" / "src" / "main" / "java" / self.package_name.replace('.', os.sep) / "MainActivity.java"
        self.activity_main_xml_path = self.project_root / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        self.manifest_path = self.project_root / "app" / "src" / "main" / "AndroidManifest.xml"
        self.build_gradle_path = self.project_root / "app" / "build.gradle"

    def create_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        try:
            (self.project_root / "app" / "src" / "main" / "java" / self.package_name.replace('.', os.sep)).mkdir(parents=True, exist_ok=True)
            (self.project_root / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
            print(f"Project structure created at: {self.project_root}")
        except Exception as e:
            print(f"Error creating project structure: {e}")

    def generate_android_app(self, arabic_instruction: str) -> dict:
        """
        Orchestrates the generation of an Android APK from an Arabic instruction.
        This function acts as the entry point for Lobe 4.
        """
        print(f"\n--- Lobe 4: Generating Android App for: '{arabic_instruction}' ---")

        # 1. Parse Arabic to structure (simulated from Lobe 0)
        print("  - Parsing Arabic instruction to structure...")
        app_structure = parse_arabic_to_structure(arabic_instruction)
        if "error" in app_structure:
            print(f"  - Error parsing instruction: {app_structure['error']}")
            return {"status": "failed", "message": f"Arabic parsing error: {app_structure['error']}"}
        print(f"  - Generated structure: {json.dumps(app_structure, indent=2)}")

        # 2. Create project directory structure
        self.create_project_structure()

        # 3. Generate Java code for MainActivity
        print("  - Generating Java code for MainActivity...")
        java_code = generate_java_code(app_structure)
        if "// Java code generation failed" in java_code:
            print("  - Java code generation failed.")
            return {"status": "failed", "message": "Java code generation failed"}
        self.main_activity_java_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.main_activity_java_path, "w") as f:
            f.write(java_code)
        print(f"  - MainActivity.java written to: {self.main_activity_java_path}")

        # 4. Generate XML layout for activity_main
        print("  - Generating XML layout for activity_main...")
        xml_layout = generate_xml_layout(app_structure)
        if "<!-- XML layout generation failed" in xml_layout:
            print("  - XML layout generation failed.")
            return {"status": "failed", "message": "XML layout generation failed"}
        self.activity_main_xml_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.activity_main_xml_path, "w") as f:
            f.write(xml_layout)
        print(f"  - activity_main.xml written to: {self.activity_main_xml_path}")

        # 5. Generate basic AndroidManifest.xml
        print("  - Generating AndroidManifest.xml...")
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp">
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
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, "w") as f:
            f.write(manifest_content)
        print(f"  - AndroidManifest.xml written to: {self.manifest_path}")

        # 6. Generate a basic build.gradle file (app level)
        print("  - Generating app/build.gradle...")
        build_gradle_content = f"""plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{self.package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId "{self.package_name}"
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
        self.build_gradle_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.build_gradle_path, "w") as f:
            f.write(build_gradle_content)
        print(f"  - app/build.gradle written to: {self.build_gradle_path}")


        # --- Placeholder for next logical step ---
        # The next logical step would be to invoke Lobe 8_apk_compiler_lobe
        # to compile the generated project into an APK.
        print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe ---")
        # For demonstration, we'll just return the project path.
        # In a real scenario, we'd pass this path to Lobe 8.
        return {
            "status": "success",
            "message": "Android project generated successfully.",
            "project_path": str(self.project_root.resolve())
        }

# Example Usage (for testing this module in isolation, would be called by the orchestrator)
if __name__ == "__main__":
    # Create a temporary directory for the project
    temp_project_dir = Path("./temp_android_project_for_lobe4_test")
    if temp_project_dir.exists():
        import shutil
        shutil.rmtree(temp_project_dir)

    lobe4_generator = Lobe4CodeGeneration(project_root=temp_project_dir)

    # Test case 1: Simple "hello world" app
    arabic_instruction_1 = "Create an app that says Hello Arabic World!"
    result_1 = lobe4_generator.generate_android_app(arabic_instruction_1)
    print(f"\nResult 1: {result_1}")

    # Test case 2: Another instruction
    # arabic_instruction_2 = "Build an app showing a welcome message: As-salamu alaykum"
    # result_2 = lobe4_generator.generate_android_app(arabic_instruction_2)
    # print(f"\nResult 2: {result_2}")

    # Clean up the temporary directory
    # if temp_project_dir.exists():
    #     import shutil
    #     shutil.rmtree(temp_project_dir)
    #     print(f"\nCleaned up temporary project directory: {temp_project_dir}")

    print("\n--- Lobe 4 Code Generation Module Demo Finished ---")