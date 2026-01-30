import os
import shutil
import re

class ArabicCodeGenerator:
    def __init__(self, project_root="arabic_apk_project"):
        self.project_root = os.path.abspath(project_root)
        self.src_dir = os.path.join(self.project_root, "src")
        self.manifest_path = os.path.join(self.project_root, "AndroidManifest.xml")
        self.main_activity_path = os.path.join(self.src_dir, "MainActivity.java")
        self.layout_dir = os.path.join(self.project_root, "res", "layout")
        self.string_resource_path = os.path.join(self.project_root, "res", "values", "strings.xml")

        self._create_project_structure()

    def _create_project_structure(self):
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.layout_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.string_resource_path), exist_ok=True)

    def _generate_manifest(self, app_name="ArabicApp"):
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.arabicapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content.strip())

    def _generate_string_resources(self, app_name="ArabicApp", welcome_message="أهلاً بك!"):
        string_resources_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
    <string name="welcome_message">{welcome_message}</string>
</resources>
"""
        with open(self.string_resource_path, "w", encoding="utf-8") as f:
            f.write(string_resources_content.strip())

    def _generate_main_activity(self, app_name="ArabicApp", welcome_message="أهلاً بك!"):
        activity_content = f"""
package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView welcomeTextView = findViewById(R.id.welcome_text);
        welcomeTextView.setText(R.string.welcome_message);
    }}
}}
"""
        with open(self.main_activity_path, "w", encoding="utf-8") as f:
            f.write(activity_content.strip())

    def _generate_layout_file(self, welcome_message="أهلاً بك!"):
        layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/welcome_message"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_path = os.path.join(self.layout_dir, "activity_main.xml")
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content.strip())

    def build_apk_structure_from_arabic(self, arabic_description: str):
        """
        Generates a basic Android APK project structure from an Arabic natural language description.

        Args:
            arabic_description (str): A string containing the Arabic description of the app.
                                      Expected to contain app name and a welcome message.
                                      Example: "تطبيق ترحيبي اسمه 'تطبيقي العربي' مع رسالة 'مرحباً بالعالم'."
        """
        app_name = "ArabicApp"
        welcome_message = "أهلاً بك!"

        # Simple parsing of Arabic description (can be enhanced with Lobe 0)
        name_match = re.search(r"اسمه ['\"](.*?)['\"]", arabic_description)
        if name_match:
            app_name = name_match.group(1)

        message_match = re.search(r"رسالة ['\"](.*?)['\"]", arabic_description)
        if message_match:
            welcome_message = message_match.group(1)

        print(f"Generating APK structure for: App Name='{app_name}', Welcome Message='{welcome_message}'")

        self._generate_manifest(app_name=app_name)
        self._generate_string_resources(app_name=app_name, welcome_message=welcome_message)
        self._generate_main_activity(app_name=app_name, welcome_message=welcome_message)
        self._generate_layout_file(welcome_message=welcome_message)

        print(f"APK project structure generated at: {self.project_root}")

    def cleanup_project(self):
        """Removes the generated project directory."""
        if os.path.exists(self.project_root):
            try:
                shutil.rmtree(self.project_root)
                print(f"Cleaned up project directory: {self.project_root}")
            except OSError as e:
                print(f"Error removing directory {self.project_root}: {e}")

if __name__ == '__main__':
    print("--- ArabicCodeGenerator Module Demo ---")

    # Initialize the generator
    code_generator = ArabicCodeGenerator("my_arabic_apk_demo")

    # Example Arabic description
    arabic_prompt = "تطبيق بسيط اسمه 'تطبيقي المميز' مع رسالة ترحيب 'أهلاً وسهلاً بكم في تطبيقي!'"

    # Generate the APK structure
    try:
        code_generator.build_apk_structure_from_arabic(arabic_prompt)
        print("\nAPK structure generation complete.")

        # You would typically then pass this structure to Lobe 8_apk_compiler_lobe
        # For demonstration, we'll just show the files created.
        print("\n--- Generated Files ---")
        for root, dirs, files in os.walk(code_generator.project_root):
            for file in files:
                print(os.path.join(root, file))

    except Exception as e:
        print(f"An error occurred during APK structure generation: {e}")

    finally:
        # Clean up the generated project
        print("\n--- Cleaning up demo project ---")
        code_generator.cleanup_project()
        print("--- ArabicCodeGenerator Module Demo Finished ---")