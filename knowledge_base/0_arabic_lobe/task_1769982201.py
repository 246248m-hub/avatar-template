import os
import re
import json
from typing import List, Dict, Any

# --- Configuration ---
ANDROID_PROJECT_TEMPLATE_DIR = "./android_project_template"
APP_MANIFEST_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "AndroidManifest.xml")
GRADLE_PROPERTIES_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "gradle.properties")
BUILD_GRADLE_APP_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "build.gradle")
RES_LAYOUT_ACTIVITY_MAIN_XML_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout", "activity_main.xml")
JAVA_MAIN_ACTIVITY_PATH = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "mygeneratedapp", "MainActivity.java")

# --- Utility Functions ---

def ensure_directory_exists(filepath: str):
    """Ensures the directory for a given file path exists."""
    dir_name = os.path.dirname(filepath)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

def read_file_content(filepath: str) -> str:
    """Reads the content of a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file_content(filepath: str, content: str):
    """Writes content to a file, creating directories if necessary."""
    ensure_directory_exists(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_in_file(filepath: str, old_string: str, new_string: str):
    """Replaces all occurrences of a string in a file."""
    content = read_file_content(filepath)
    new_content = content.replace(old_string, new_string)
    write_file_content(filepath, new_content)

def create_android_project_template():
    """Creates a dummy Android project structure (simplified for demonstration)."""
    print("Creating dummy Android project template...")
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "mygeneratedapp"), exist_ok=True)

    # Dummy AndroidManifest.xml
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.mygeneratedapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
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
    write_file_content(APP_MANIFEST_PATH, manifest_content)

    # Dummy gradle.properties
    gradle_properties_content = """# Gradlew settings
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
# AndroidX packages
android.useAndroidX=true
"""
    write_file_content(GRADLE_PROPERTIES_PATH, gradle_properties_content)

    # Dummy build.gradle (app level)
    build_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.mygeneratedapp"
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
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {

    implementation 'androidx.core:core-ktx:1.8.0'
    implementation 'androidx.appcompat:appcompat:1.4.1'
    implementation 'com.google.android.material:material:1.5.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.3'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.3'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'
}
"""
    write_file_content(BUILD_GRADLE_APP_PATH, build_gradle_content)

    # Dummy activity_main.xml
    activity_main_content = """<?xml version="1.0" encoding="utf-8"?>
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
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    write_file_content(RES_LAYOUT_ACTIVITY_MAIN_XML_PATH, activity_main_content)

    # Dummy MainActivity.java
    main_activity_content = """package com.example.mygeneratedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView greetingTextView = findViewById(R.id.greetingTextView);
        // Default greeting, can be updated by the generator
        greetingTextView.setText("Welcome to your generated app!");
    }
}
"""
    write_file_content(JAVA_MAIN_ACTIVITY_PATH, main_activity_content)

    print("Dummy Android project template created.")

def cleanup_android_project_template():
    """Removes the dummy Android project structure."""
    import shutil
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        print(f"Cleaning up dummy Android project template: {ANDROID_PROJECT_TEMPLATE_DIR}")
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        print("Cleanup complete.")

class ArabicAppGenerator:
    """
    A module responsible for generating Android APKs from Arabic natural language descriptions.
    This module focuses on parsing Arabic to understand app requirements and then
    modifying the Android project template accordingly.
    """

    def __init__(self):
        self.app_name = "MyGeneratedApp"
        self.package_name = "com.example.mygeneratedapp"
        self.main_activity_layout_id = "greetingTextView"
        self.main_activity_text = "Welcome to your generated app!"

    def parse_arabic_request(self, nl_request: str) -> Dict[str, Any]:
        """
        Parses an Arabic natural language request to extract app components and configurations.
        This is a simplified parser. A real-world implementation would involve more sophisticated NLP techniques.

        Args:
            nl_request: The Arabic natural language description of the app.

        Returns:
            A dictionary containing parsed app configuration.
        """
        print(f"Parsing Arabic request: '{nl_request}'")
        parsed_config = {
            "app_name": self.app_name,
            "package_name": self.package_name,
            "main_activity_text": self.main_activity_text,
            "layout_elements": []
        }

        # Simple keyword-based parsing for demonstration
        if "تطبيق ترحيبي" in nl_request or "تطبيق تحية" in nl_request:
            parsed_config["app_name"] = "تطبيق ترحيبي"
            parsed_config["main_activity_text"] = "أهلاً بك في تطبيقك!"

        if "اسم التطبيق هو" in nl_request:
            match = re.search(r"اسم التطبيق هو\s+([\w\s]+)", nl_request)
            if match:
                parsed_config["app_name"] = match.group(1).strip()

        if "يحتوي على نص" in nl_request and "في الشاشة الرئيسية" in nl_request:
            match = re.search(r"يحتوي على نص\s+['\"](.+)['\"]\s+في الشاشة الرئيسية", nl_request)
            if match:
                parsed_config["main_activity_text"] = match.group(1).strip()

        # Future enhancements: Parse for buttons, input fields, specific actions, etc.
        # Example: "أضف زر باسم 'التالي' عند الضغط عليه يظهر رسالة 'تم الضغط'"
        # This would require identifying UI elements, properties, and event handlers.

        print(f"Parsed configuration: {parsed_config}")
        return parsed_config

    def update_android_project(self, config: Dict[str, Any]):
        """
        Updates the Android project template files based on the parsed configuration.

        Args:
            config: The dictionary containing parsed app configuration.
        """
        print("Updating Android project files based on configuration...")

        # Update app name in AndroidManifest.xml (label attribute)
        app_name_res_id = "@string/app_name" # This is a simplification, actual string resources would be managed
        replace_in_file(APP_MANIFEST_PATH, 'android:label="@string/app_name"', f'android:label="{config["app_name"]}"')
        # Note: In a real scenario, you'd update strings.xml as well.

        # Update package name if it were to change (complex, usually not changed post-creation easily)
        # For simplicity, we assume package name remains "com.example.mygeneratedapp" for this demo.
        # If the package name needed to change, it would involve renaming directories and updating build.gradle.

        # Update MainActivity.java
        main_activity_content = read_file_content(JAVA_MAIN_ACTIVITY_PATH)
        # Replace the default text in the TextView
        new_java_content = re.sub(
            rf"findViewById\(R.id.{self.main_activity_layout_id}\).setText\([^)]*\);",
            f"greetingTextView.setText(\"{config['main_activity_text']}\");",
            main_activity_content
        )
        # Update the TextView ID if it were specified in the request (advanced)
        # For now, we keep the default ID `greetingTextView`

        write_file_content(JAVA_MAIN_ACTIVITY_PATH, new_java_content)
        print("MainActivity.java updated.")

        # Update activity_main.xml (e.g., change text for the TextView)
        activity_main_content = read_file_content(RES_LAYOUT_ACTIVITY_MAIN_XML_PATH)
        # This is a very basic example. More complex layouts would require more sophisticated XML parsing and manipulation.
        # Here, we are assuming we know the ID of the TextView to update.
        # A more robust solution would parse the XML to find the TextView and update its text attribute.
        # For demonstration, we'll just set the text content for the known ID.
        new_xml_content = re.sub(
            rf'<TextView[^>]*android:id="@+id/{self.main_activity_layout_id}"[^>]*>.*?</TextView>',
            f'<TextView android:id="@+id/{self.main_activity_layout_id}" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="{config["main_activity_text"]}" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent" />',
            activity_main_content,
            flags=re.DOTALL
        )
        write_file_content(RES_LAYOUT_ACTIVITY_MAIN_XML_PATH, new_xml_content)
        print("activity_main.xml updated.")

        print("Android project files updated successfully.")

    def generate_apk_from_nl(self, nl_request: str) -> str:
        """
        Orchestrates the process of generating an APK from an Arabic natural language request.

        Args:
            nl_request: The Arabic natural language description of the app.

        Returns:
            The path to the generated APK file (simulated).
        """
        print(f"\n--- Starting APK Generation for: '{nl_request}' ---")

        # 1. Parse the Arabic natural language request
        app_config = self.parse_arabic_request(nl_request)

        # 2. Prepare the Android project template
        create_android_project_template()

        # 3. Update the project template with the parsed configuration
        self.update_android_project(app_config)

        # 4. Simulate APK compilation (replace with actual build process)
        print("\n--- Simulating APK Compilation ---")
        apk_name = f"{app_config['app_name'].replace(' ', '_')}.apk"
        generated_apk_path = os.path.join("./output", apk_name)
        ensure_directory_exists(generated_apk_path)
        with open(generated_apk_path, "w") as f:
            f.write(f"Simulated APK content for {apk_name}")
        print(f"Simulated APK created at: {generated_apk_path}")

        # 5. Clean up the project template
        cleanup_android_project_template()

        print(f"--- APK Generation Complete ---")
        return generated_apk_path

# --- Example Usage ---
if __name__ == "__main__":
    generator = ArabicAppGenerator()

    # Example 1: A simple welcome app
    arabic_request_1 = "أنشئ لي تطبيقاً باسم 'تطبيق ترحيبي' يعرض رسالة 'أهلاً بك في تطبيقك!' على الشاشة الرئيسية."
    generated_apk_1 = generator.generate_apk_from_nl(arabic_request_1)
    print(f"\nGenerated APK 1: {generated_apk_1}")

    # Example 2: Another app with a different name and text
    arabic_request_2 = "أريد تطبيقاً جديداً. اسم التطبيق هو 'رسالة خاصة' ويحتوي على نص 'هذه رسالة مهمة لك' في الشاشة الرئيسية."
    generated_apk_2 = generator.generate_apk_from_nl(arabic_request_2)
    print(f"\nGenerated APK 2: {generated_apk_2}")

    # Example 3: A request that might not directly map to UI elements easily with this simple parser
    # This demonstrates the need for more advanced parsing.
    arabic_request_3 = "أريد تطبيقاً يعرض قائمة بأسماء المستخدمين."
    print("\n--- Testing a request with more complex UI expectations ---")
    generated_apk_3 = generator.generate_apk_from_nl(arabic_request_3)
    print(f"\nGenerated APK 3 (may not fully reflect request due to parser limitations): {generated_apk_3}")

    # Clean up any residual output directory if needed
    import shutil
    if os.path.exists("./output"):
        print("\nCleaning up output directory...")
        # shutil.rmtree("./output") # Uncomment to clean the output directory
        print("Output directory cleanup complete (manual cleanup may be required).")

    print("\n--- Arabic App Generation Module Demo Finished ---")