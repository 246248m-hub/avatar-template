import os
import shutil
import xml.etree.ElementTree as ET

# Assume these are defined elsewhere or will be created in other lobes
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
OUTPUT_DIR = "output"
MANIFEST_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "AndroidManifest.xml")
JAVA_DIR = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "mygeneratedapp")
RES_DIR = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res")
LAYOUT_DIR = os.path.join(RES_DIR, "layout")
DRAWABLE_DIR = os.path.join(RES_DIR, "drawable")
VALUES_DIR = os.path.join(RES_DIR, "values")


def initialize_android_project_structure():
    """
    Initializes the basic Android project directory structure.
    This is a simplified version. A real-world scenario would involve
    copying a more complete template or using a build tool.
    """
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "mygeneratedapp"), exist_ok=True)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "drawable"), exist_ok=True)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "values"), exist_ok=True)
    print(f"Initialized basic Android project structure in '{ANDROID_PROJECT_TEMPLATE_DIR}'.")


def create_android_manifest(app_name="MyGeneratedApp"):
    """
    Creates a basic AndroidManifest.xml file.
    """
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.mygeneratedapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app_name}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyGeneratedApp">

        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"Created '{MANIFEST_PATH}'.")


def create_layout_file(layout_name: str, content: str):
    """
    Creates an XML layout file.
    """
    layout_path = os.path.join(LAYOUT_DIR, f"{layout_name}.xml")
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created layout file: '{layout_path}'.")


def create_java_file(class_name: str, content: str):
    """
    Creates a Java file for an Android activity or other component.
    """
    java_path = os.path.join(JAVA_DIR, f"{class_name}.java")
    with open(java_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created Java file: '{java_path}'.")


def create_string_resource(key: str, value: str):
    """
    Adds a string resource to strings.xml.
    """
    strings_xml_path = os.path.join(VALUES_DIR, "strings.xml")

    if not os.path.exists(strings_xml_path):
        strings_xml_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">MyGeneratedApp</string>
</resources>
"""
        with open(strings_xml_path, "w", encoding="utf-8") as f:
            f.write(strings_xml_content)

    tree = ET.parse(strings_xml_path)
    root = tree.getroot()

    # Check if the string resource already exists
    found = False
    for string_elem in root.findall('string'):
        if string_elem.get('name') == key:
            string_elem.text = value
            found = True
            break

    if not found:
        new_string = ET.Element("string")
        new_string.set("name", key)
        new_string.text = value
        root.append(new_string)

    tree.write(strings_xml_path, encoding="utf-8", xml_declaration=True)
    print(f"Added/Updated string resource '{key}' in '{strings_xml_path}'.")


def generate_arabic_nlp_android_module(app_name: str, primary_language: str = "ar"):
    """
    This module focuses on integrating Arabic NLP capabilities and
    setting up the foundational Android project structure.
    It simulates the creation of an app that might leverage Arabic text processing.
    """
    print("\n--- Initiating Lobe 1_arabic_nlp_android_integration_lobe ---")

    # 1. Initialize Android Project Structure
    initialize_android_project_structure()
    create_android_manifest(app_name=app_name)

    # 2. Simulate Arabic NLP Integration - Add a basic string resource for demonstration
    arabic_greeting = "مرحباً بالعالم"
    create_string_resource("greeting_message", arabic_greeting)

    # 3. Create a simple MainActivity that might display this greeting
    # This is a placeholder for actual NLP logic that might be integrated later.
    main_activity_content = f"""
package com.example.mygeneratedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists

        TextView greetingTextView = findViewById(R.id.greetingTextView);
        // In a real app, this text would come from NLP processing or be dynamically set.
        // For now, we'll set it directly from resources.
        greetingTextView.setText(getString(R.string.greeting_message));
    }}
}}
"""
    create_java_file("MainActivity", main_activity_content)

    # 4. Create a corresponding layout file
    activity_main_layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
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
        android:text="{arabic_greeting}"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    create_layout_file("activity_main", activity_main_layout_content)

    print(f"Successfully generated basic Android structure with Arabic resource for app '{app_name}'.")
    print("--- Lobe 1_arabic_nlp_android_integration_lobe Finished ---")

    # Return path to the generated project for subsequent lobes
    return ANDROID_PROJECT_TEMPLATE_DIR


# Example usage (for demonstration purposes within a script)
if __name__ == "__main__":
    # Simulate a prompt that would trigger this lobe
    prompt_for_arabic_app = {
        "app_name": "ArabicGreetingApp",
        "primary_language": "ar",
        "features": ["display_greeting"]
    }

    generated_project_path = generate_arabic_nlp_android_module(
        app_name=prompt_for_arabic_app["app_name"],
        primary_language=prompt_for_arabic_app["primary_language"]
    )

    print(f"\nGenerated Android project at: {generated_project_path}")
    print("\n--- Next step would be Lobe 4_code_generation_lobe or Lobe 8_apk_compiler_lobe depending on context ---")

    # Clean up dummy project if it exists
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        print(f"\nCleaning up dummy project directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)