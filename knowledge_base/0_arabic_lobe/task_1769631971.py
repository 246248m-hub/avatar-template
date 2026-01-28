import os
import subprocess
import shutil
import re
from pathlib import Path

# Placeholder for a more sophisticated Arabic NLP parser
class ArabicNLPParser:
    def __init__(self, knowledge_base_dir):
        self.knowledge_base_dir = Path(knowledge_base_dir)

    def parse_intent(self, text):
        """
        Analyzes Arabic text to extract user intent.
        This is a simplified example. A real implementation would involve
        more advanced NLP techniques, dictionaries, and potentially ML models.
        """
        text = text.lower().strip()
        if "قم بتحليل البيانات" in text:
            return {"intent": "analyze_data", "parameters": {}}
        elif "إنشاء تطبيق" in text:
            match = re.search(r"إنشاء تطبيق (.+)", text)
            if match:
                return {"intent": "create_app", "parameters": {"app_name": match.group(1).strip()}}
        elif "إظهار شاشة" in text:
            match = re.search(r"إظهار شاشة (.+)", text)
            if match:
                return {"intent": "show_screen", "parameters": {"screen_name": match.group(1).strip()}}
        else:
            return {"intent": "unrecognized", "parameters": {}}

# Placeholder for an APK builder that uses the NLP parser
class ArabicAPKBuilder:
    def __init__(self, project_root="arabic_apk_project"):
        self.project_root = Path(project_root)
        self.nlp_parser = ArabicNLPParser(knowledge_base_dir="path/to/your/knowledge_base") # Replace with actual path
        self.current_project_dir = None

    def generate_apk_from_arabic(self, prompt_arabic):
        """
        Generates a functional APK structure from an Arabic prompt.
        This is a high-level orchestrator.
        """
        intent_data = self.nlp_parser.parse_intent(prompt_arabic)
        intent = intent_data.get("intent")
        parameters = intent_data.get("parameters", {})

        if intent == "unrecognized":
            return "Error: Unrecognized intent. Please provide a valid command."

        if self.current_project_dir is None or not self.current_project_dir.exists():
            self.create_new_project()

        if intent == "analyze_data":
            return self.handle_analyze_data_intent()
        elif intent == "create_app":
            app_name = parameters.get("app_name", "MyArabicApp")
            return self.handle_create_app_intent(app_name)
        elif intent == "show_screen":
            screen_name = parameters.get("screen_name", "DefaultScreen")
            return self.handle_show_screen_intent(screen_name)
        else:
            return f"Unhandled intent: {intent}"

    def create_new_project(self):
        """Creates a new, basic Android project structure."""
        if self.current_project_dir and self.current_project_dir.exists():
            print(f"Project already exists at {self.current_project_dir}. Skipping creation.")
            return

        project_name = f"ArabicApp_{os.urandom(4).hex()}"
        self.current_project_dir = self.project_root / project_name
        self.current_project_dir.mkdir(parents=True, exist_ok=True)

        # Create basic Android manifest
        manifest_dir = self.current_project_dir / "app" / "src" / "main"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.arabicapp">

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
        (manifest_dir / "AndroidManifest.xml").write_text(manifest_content)

        # Create basic MainActivity.java
        java_dir = manifest_dir / "java" / "com" / "example" / "arabicapp"
        java_dir.mkdir(parents=True, exist_ok=True)
        activity_content = """package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
"""
        (java_dir / "MainActivity.java").write_text(activity_content)

        # Create basic activity_main.xml
        layout_dir = self.current_project_dir / "app" / "src" / "main" / "res" / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        layout_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/greetingTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="مرحباً بالعالم!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        (layout_dir / "activity_main.xml").write_text(layout_content)

        # Create strings.xml
        values_dir = self.current_project_dir / "app" / "src" / "main" / "res" / "values"
        values_dir.mkdir(parents=True, exist_ok=True)
        strings_content = """<resources>
    <string name="app_name">Arabic App</string>
</resources>
"""
        (values_dir / "strings.xml").write_text(strings_content)

        # Create a dummy build.gradle (simplified for demo)
        gradle_dir = self.current_project_dir / "app"
        gradle_dir.mkdir(parents=True, exist_ok=True)
        gradle_content = """plugins {
    id 'com.android.application'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.arabicapp"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
        (gradle_dir / "build.gradle").write_text(gradle_content)


        print(f"Created new project structure at: {self.current_project_dir}")
        return f"New project initialized at {self.current_project_dir}"


    def handle_analyze_data_intent(self):
        """
        Simulates adding logic for data analysis.
        In a real scenario, this would involve generating code for data processing,
        charting libraries, etc.
        """
        if not self.current_project_dir or not self.current_project_dir.exists():
            return "Error: Project not initialized. Call create_new_project first."

        # Example: Add a data analysis related string to res/values/strings.xml
        strings_file = self.current_project_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        if strings_file.exists():
            content = strings_file.read_text()
            if "<string name=\"analysis_result\">نتائج التحليل:</string>" not in content:
                content = content.replace("</resources>", "    <string name=\"analysis_result\">نتائج التحليل:</string>\n</resources>")
                strings_file.write_text(content)
                return "Added data analysis string to strings.xml."
            else:
                return "Data analysis string already exists."
        else:
            return "Error: strings.xml not found in project."


    def handle_create_app_intent(self, app_name):
        """
        Handles the intent to create or modify an app with a specific name.
        This might involve renaming packages, updating app names in resources.
        """
        if not self.current_project_dir or not self.current_project_dir.exists():
            self.create_new_project()
            # Update project name in the new project if it wasn't initialized with the desired name
            current_app_name_in_manifest = self.current_project_dir.name.replace("ArabicApp_", "")
            if current_app_name_in_manifest != app_name:
                print(f"Renaming app from {current_app_name_in_manifest} to {app_name}")
                # Simplistic renaming - in real app this would involve complex refactoring
                strings_file = self.current_project_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml"
                if strings_file.exists():
                    content = strings_file.read_text()
                    content = content.replace(f'<string name="app_name">{current_app_name_in_manifest}</string>', f'<string name="app_name">{app_name}</string>')
                    strings_file.write_text(content)

                # Update package name in MainActivity and Manifest if needed
                # This is a highly simplified representation of package renaming.
                # Real Android Studio refactoring is complex.
                old_package_parts = "com.example.arabicapp".split('.')
                new_package_parts = f"com.example.{app_name.lower().replace(' ', '')}".split('.')

                manifest_file = self.current_project_dir / "app" / "src" / "main" / "AndroidManifest.xml"
                if manifest_file.exists():
                    manifest_content = manifest_file.read_text()
                    manifest_content = manifest_content.replace("package=\"com.example.arabicapp\"", f"package=\"{''.join(new_package_parts)}\"")
                    manifest_file.write_text(manifest_content)

                main_activity_file = self.current_project_dir / "app" / "src" / "main" / "java" / "com" / "example" / "arabicapp" / "MainActivity.java"
                if main_activity_file.exists():
                    activity_content = main_activity_file.read_text()
                    activity_content = activity_content.replace("package com.example.arabicapp;", f"package {''.join(new_package_parts)};")
                    main_activity_file.write_text(activity_content)

                # Update directory structure for new package
                old_java_path = self.current_project_dir / "app" / "src" / "main" / "java" / "com" / "example" / "arabicapp"
                new_java_path = self.current_project_dir / "app" / "src" / "main" / "java" / new_package_parts[0] / new_package_parts[1] / new_package_parts[2]
                if old_java_path.exists() and new_java_path != old_java_path:
                    shutil.move(str(old_java_path), str(new_java_path))


            return f"App initialized with name: {app_name}"
        else:
            # Update existing project name if different
            strings_file = self.current_project_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml"
            if strings_file.exists():
                content = strings_file.read_text()
                if f'<string name="app_name">{app_name}</string>' not in content:
                    content = content.replace(re.search(r'<string name="app_name">.*</string>', content).group(0), f'<string name="app_name">{app_name}</string>')
                    strings_file.write_text(content)
                    return f"App name updated to: {app_name}"
                else:
                    return f"App name is already: {app_name}"
            else:
                return "Error: strings.xml not found in existing project."


    def handle_show_screen_intent(self, screen_name):
        """
        Handles the intent to show a specific screen.
        This would involve creating new Activity/Fragment files and updating navigation.
        """
        if not self.current_project_dir or not self.current_project_dir.exists():
            return "Error: Project not initialized. Call create_new_project first."

        # Example: Create a new Activity for the screen
        package_path = Path(*"com.example.arabicapp".split('.')) # Use current package structure
        java_dir = self.current_project_dir / "app" / "src" / "main" / "java" / package_path
        java_dir.mkdir(parents=True, exist_ok=True)

        activity_name = f"{screen_name.replace(' ', '')}Activity"
        activity_file = java_dir / f"{activity_name}.java"

        if not activity_file.exists():
            package_name = ".".join(package_path.parts)
            activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // For simplicity, using a basic TextView. In a real app, this would be a layout.
        setContentView(R.layout.activity_{screen_name.lower().replace(' ', '')});
    }}
}}
"""
            (java_dir / f"activity_{screen_name.lower().replace(' ', '')}.xml").write_text(f"<TextView android:layout_width='match_parent' android:layout_height='match_parent' android:text='{screen_name}'/>")

            activity_file.write_text(activity_content)

            # Update AndroidManifest.xml to include the new activity
            manifest_file = self.current_project_dir / "app" / "src" / "main" / "AndroidManifest.xml"
            if manifest_file.exists():
                manifest_content = manifest_file.read_text()
                new_activity_declaration = f'    <activity android:name=".{activity_name}"></activity>\n'
                # Insert before the MainActivity declaration or at the end of application tag
                manifest_content = manifest_content.replace("</application>", new_activity_declaration + "    </application>")
                manifest_file.write_text(manifest_content)

            return f"Created new screen '{screen_name}' with activity '{activity_name}'."
        else:
            return f"Screen '{screen_name}' (activity '{activity_name}') already exists."


    def cleanup_project(self):
        """Removes the generated project directory."""
        if self.current_project_dir and self.current_project_dir.exists():
            try:
                shutil.rmtree(self.current_project_dir)
                print(f"Cleaned up project: {self.current_project_dir}")
                self.current_project_dir = None
            except OSError as e:
                print(f"Error removing directory {self.current_project_dir}: {e}")
        else:
            print("No project to clean up.")

# --- Example Usage ---
if __name__ == "__main__":
    # This part is for demonstration and would not be in the final module if integrated.
    # Assuming a dummy knowledge base directory exists for the parser.
    if not os.path.exists("path/to/your/knowledge_base"):
        os.makedirs("path/to/your/knowledge_base")

    builder = ArabicAPKBuilder()

    print("--- ArabicAPKBuilder Module Demo ---")

    # Example 1: Create a new app
    prompt_arabic_1 = "إنشاء تطبيق اسم التطبيق الخاص بي"
    result_1 = builder.generate_apk_from_arabic(prompt_arabic_1)
    print(f"Result 1: {result_1}")

    # Example 2: Add a new screen
    prompt_arabic_2 = "إظهار شاشة إعدادات"
    result_2 = builder.generate_apk_from_arabic(prompt_arabic_2)
    print(f"Result 2: {result_2}")

    # Example 3: Analyze data (uses existing project)
    prompt_arabic_3 = "قم بتحليل البيانات."
    result_3 = builder.generate_apk_from_arabic(prompt_arabic_3)
    print(f"Result 3: {result_3}")

    # Example 4: Unrecognized intent
    prompt_arabic_4 = "هذا أمر غير معروف"
    result_4 = builder.generate_apk_from_arabic(prompt_arabic_4)
    print(f"Result 4: {result_4}")

    # Example 5: Create another app to show project creation logic
    builder.cleanup_project() # Clean up previous to start fresh
    prompt_arabic_5 = "إنشاء تطبيق حاسبة"
    result_5 = builder.generate_apk_from_arabic(prompt_arabic_5)
    print(f"Result 5: {result_5}")

    # Clean up the generated project
    builder.cleanup_project()
    print("\n--- ArabicAPKBuilder Module Demo Finished ---")