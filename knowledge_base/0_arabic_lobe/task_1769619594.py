import os
import shutil
import subprocess
from pathlib import Path

# Constants for module names and paths
ARABIC_PARSER_MODULE = "arabic_parser_lobe"
APK_GENERATOR_MODULE = "apk_generator_lobe"
OUTPUT_DIR = "./output_apks"

class ArabicParserLobe:
    """
    Lobe responsible for parsing Arabic natural language descriptions into structured data
    suitable for APK generation.
    """
    def __init__(self, knowledge_base_dir: str = "./knowledge_base"):
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.knowledge_base_dir.mkdir(exist_ok=True)
        print(f"ArabicParserLobe initialized with knowledge base: {self.knowledge_base_dir}")

    def parse_description(self, description: str) -> dict:
        """
        Parses an Arabic natural language description into a structured dictionary.
        This is a simplified example. A real implementation would involve more sophisticated
        NLP techniques (e.g., NER, dependency parsing, intent recognition) for Arabic.

        Args:
            description: The Arabic natural language description of the APK.

        Returns:
            A dictionary representing the parsed APK structure.
        """
        print(f"Parsing Arabic description: '{description}'")
        parsed_data = {
            "app_name": "MyArabicApp",
            "activities": [],
            "permissions": [],
            "layout": {},
            "logic": ""
        }

        # --- Simplified parsing logic ---
        if "شاشة ترحيب" in description or "رسالة ترحيب" in description:
            parsed_data["activities"].append({
                "name": "MainActivity",
                "layout": "activity_main.xml",
                "onCreate": [
                    "setContentView(R.layout.activity_main);"
                ]
            })
            parsed_data["layout"]["activity_main.xml"] = """
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_message"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="مرحباً بك في تطبيقي!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
            """
            parsed_data["logic"] += """
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
            """

        if "زر" in description:
            if not parsed_data["activities"]:
                parsed_data["activities"].append({
                    "name": "MainActivity",
                    "layout": "activity_main.xml",
                    "onCreate": []
                })
            parsed_data["layout"].setdefault("activity_main.xml", """
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">
</androidx.constraintlayout.widget.ConstraintLayout>
            """)
            button_id = "myButton"
            button_text = "اضغط هنا"
            if "زر بعنوان" in description:
                button_text = description.split("زر بعنوان")[1].split(",")[0].strip()
            if "زر بمعرف" in description:
                button_id = description.split("زر بمعرف")[1].split(",")[0].strip()

            parsed_data["layout"]["activity_main.xml"] += f"""
    <Button
        android:id="@+id/{button_id}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{button_text}"
        app:layout_constraintTop_toBottomOf="@id/welcome_message" // Example placement
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="20dp"/>
            """
            parsed_data["activities"][0]["onCreate"].append(f"Button {button_id} = findViewById(R.id.{button_id});")
            parsed_data["activities"][0]["onCreate"].append(f"{button_id}.setOnClickListener(v -> {{ /* Handle button click */ }});")
            parsed_data["logic"] += f"""
public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button {button_id} = findViewById(R.id.{button_id});
        {button_id}.setOnClickListener(v -> {{
            // Logic for button click
            Toast.makeText(this, "تم الضغط على الزر!", Toast.LENGTH_SHORT).show();
        }});
    }}
}}
            """

        if "إنترنت" in description or "شبكة" in description:
            parsed_data["permissions"].append("android.permission.INTERNET")

        # Add a default app name if not inferred
        if "app_name" not in parsed_data or not parsed_data["app_name"]:
            parsed_data["app_name"] = "DefaultArabicApp"

        print(f"Parsed data: {parsed_data}")
        return parsed_data

class ApkGeneratorLobe:
    """
    Lobe responsible for generating a basic APK structure from parsed data.
    This is a highly simplified representation of an APK generation process.
    A real APK generator would involve:
    - Android SDK integration
    - Manifest generation
    - Resource compilation (layouts, drawables, strings)
    - Java/Kotlin code compilation
    - DEX file generation
    - APK signing
    """
    def __init__(self, base_project_template_dir: str = "./android_project_template"):
        self.base_project_template_dir = Path(base_project_template_dir)
        self.base_project_template_dir.mkdir(exist_ok=True)
        print(f"ApkGeneratorLobe initialized with template directory: {self.base_project_template_dir}")

        # Create a dummy template if it doesn't exist
        if not (self.base_project_template_dir / "app").exists():
            print("Creating dummy Android project template...")
            (self.base_project_template_dir / "app").mkdir(parents=True, exist_ok=True)
            (self.base_project_template_dir / "app" / "src").mkdir(parents=True, exist_ok=True)
            (self.base_project_template_dir / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
            (self.base_project_template_dir / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
            (self.base_project_template_dir / "app" / "src" / "main" / "res").mkdir(parents=True, exist_ok=True)
            (self.base_project_template_dir / "app" / "src" / "main" / "res" / "layout").mkdir(exist_ok=True)
            (self.base_project_template_dir / "app" / "src" / "main" / "res" / "values").mkdir(exist_ok=True)
            with open(self.base_project_template_dir / "app" / "src" / "main" / "AndroidManifest.xml", "w", encoding="utf-8") as f:
                f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myarabicapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyArabicApp">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")
            with open(self.base_project_template_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml", "w", encoding="utf-8") as f:
                f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">MyArabicApp</string>
</resources>
""")
            with open(self.base_project_template_dir / "build.gradle", "w", encoding="utf-8") as f:
                f.write("""
plugins {
    id 'com.android.application'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.myarabicapp"
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
""")
            print("Dummy template created.")


    def generate_apk_from_arabic(self, description: str, output_dir: str) -> str:
        """
        Generates a simplified APK structure from an Arabic description.
        This function simulates the process of creating an Android project,
        adding specified components, and attempting a build.

        Args:
            description: The Arabic natural language description.
            output_dir: The directory to save the generated APK.

        Returns:
            A status message indicating success or failure.
        """
        print(f"Initiating APK generation for: '{description}'")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 1. Parse the Arabic description
        parser = ArabicParserLobe()
        parsed_data = parser.parse_description(description)

        # 2. Create a temporary project directory based on the template
        temp_project_dir = output_path / f"temp_project_{os.getpid()}"
        if temp_project_dir.exists():
            shutil.rmtree(temp_project_dir)
        shutil.copytree(self.base_project_template_dir, temp_project_dir)

        # Update package name based on app_name if available
        package_name = parsed_data.get("app_name", "com.example.defaultapp").lower().replace(" ", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace(",", "").replace(".", "")
        if not package_name:
            package_name = "com.example.defaultapp"

        # Update AndroidManifest.xml
        manifest_path = temp_project_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_content = f.read()
        manifest_content = manifest_content.replace("package=\"com.example.myarabicapp\"", f"package=\"com.example.{package_name}\"")
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Update strings.xml for app name
        strings_xml_path = temp_project_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        app_name_res = parsed_data.get("app_name", "My App")
        with open(strings_xml_path, "r", encoding="utf-8") as f:
            strings_content = f.read()
        strings_content = strings_content.replace("<string name=\"app_name\">MyArabicApp</string>", f"<string name=\"app_name\">{app_name_res}</string>")
        with open(strings_xml_path, "w", encoding="utf-8") as f:
            f.write(strings_content)

        # Add permissions to AndroidManifest.xml
        if parsed_data.get("permissions"):
            permissions_xml = "\n".join([f'    <uses-permission android:name="{perm}" />' for perm in parsed_data["permissions"]])
            manifest_content = manifest_content.replace("</manifest>", f"{permissions_xml}\n</manifest>")
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest_content)
            print(f"Added permissions: {parsed_data['permissions']}")


        # Create Activity and Layout files based on parsed data
        java_dir = temp_project_dir / "app" / "src" / "main" / "java" / "com" / "example" / package_name
        java_dir.mkdir(parents=True, exist_ok=True)
        res_layout_dir = temp_project_dir / "app" / "src" / "main" / "res" / "layout"

        # Default MainActivity content
        main_activity_code = """
package com.example.%s;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
"""
        main_activity_end = """
    }
}
"""
        layout_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        activity_created = False
        if parsed_data.get("activities"):
            for activity in parsed_data["activities"]:
                activity_name = activity["name"]
                layout_name = activity["layout"]
                java_file_path = java_dir / f"{activity_name}.java"
                layout_file_path = res_layout_dir / layout_name

                # Generate Java code
                current_activity_code = f"""
package com.example.{package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;
import android.widget.Button; // Import for Button

public class {activity_name} extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name.replace(".xml", "")});
"""
                if "onCreate" in activity:
                    current_activity_code += "\n".join(activity["onCreate"]) + "\n"

                current_activity_code += """
    }
}
"""
                with open(java_file_path, "w", encoding="utf-8") as f:
                    f.write(current_activity_code)
                print(f"Generated Java file: {java_file_path}")

                # Generate Layout XML
                current_layout_content = layout_content # Start with base
                if "layout" in activity and layout_name in activity["layout"]:
                     # This is a simplification, actual logic would merge or replace
                    # For this demo, we assume the parsed_data['layout'][layout_name]
                    # contains the *entire* layout content if provided.
                    pass # Handled below if a specific layout is defined in parsed_data
                elif layout_name in parsed_data.get("layout", {}):
                    current_layout_content = parsed_data["layout"][layout_name]

                with open(layout_file_path, "w", encoding="utf-8") as f:
                    f.write(current_layout_content)
                print(f"Generated Layout file: {layout_file_path}")

                if activity_name == "MainActivity":
                    activity_created = True


        # Ensure MainActivity exists if no activities were explicitly defined but description implies it
        if not activity_created and not parsed_data.get("activities"):
            main_activity_file = java_dir / "MainActivity.java"
            layout_file = res_layout_dir / "activity_main.xml"

            activity_code = main_activity_code % package_name
            activity_code += "\n".join(parsed_data.get("logic", "").splitlines()) # Add any generic logic
            activity_code += main_activity_end

            with open(main_activity_file, "w", encoding="utf-8") as f:
                f.write(activity_code)
            print(f"Generated default MainActivity: {main_activity_file}")

            # Use the layout defined in parsed_data if available, otherwise default
            default_layout_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/default_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Default App"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
"""
            if "activity_main.xml" in parsed_data.get("layout", {}):
                layout_content_to_write = parsed_data["layout"]["activity_main.xml"]
            else:
                layout_content_to_write = default_layout_content

            with open(layout_file, "w", encoding="utf-8") as f:
                f.write(layout_content_to_write)
            print(f"Generated default activity_main.xml: {layout_file}")

        # 3. Simulate APK build process (this part is highly complex and requires Android SDK)
        # In a real scenario, you'd call Gradle or Android build tools.
        # For this demo, we'll just create a dummy APK file.

        # Mocking the build process:
        print("Simulating APK build process...")
        # In a real scenario, you would navigate to temp_project_dir and run:
        # subprocess.run(["./gradlew", "assembleDebug"], cwd=temp_project_dir, check=True)
        # Then find the APK in app/build/outputs/apk/debug/app-debug.apk

        # For this demonstration, we'll just create a placeholder file.
        dummy_apk_path = output_path / f"{package_name.split('.')[-1]}-debug.apk"
        try:
            with open(dummy_apk_path, "w") as f:
                f.write("This is a placeholder for a generated APK.\n")
            print(f"Successfully simulated APK creation: {dummy_apk_path}")
            status = f"APK generation simulated successfully for '{description}'. See: {dummy_apk_path}"
        except Exception as e:
            print(f"Error during simulated APK creation: {e}")
            status = f"APK generation failed for '{description}'. Error: {e}"

        # 4. Clean up temporary project directory
        try:
            shutil.rmtree(temp_project_dir)
            print(f"Cleaned up temporary project directory: {temp_project_dir}")
        except OSError as e:
            print(f"Error removing temporary directory {temp_project_dir}: {e}")

        return status

# Example Usage (for demonstration purposes, not part of the final output code block)
if __name__ == "__main__":
    print("--- Starting Arabic Parser and Generator Module Demo ---")

    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Initialize the APK Generator Lobe
    apk_generator = ApkGeneratorLobe()

    # --- Test Case 1: Basic welcome message ---
    arabic_desc_1 = "تطبيق يعرض رسالة ترحيب \"مرحباً بك في تطبيقي!\""
    print(f"\n--- Generating APK for: '{arabic_desc_1}' ---")
    result_1 = apk_generator.generate_apk_from_arabic(arabic_desc_1, OUTPUT_DIR)
    print(f"Result 1: {result_1}")

    # --- Test Case 2: App with a button ---
    arabic_desc_2 = "تطبيق يحتوي على زر بعنوان \"انقر هنا\""
    print(f"\n--- Generating APK for: '{arabic_desc_2}' ---")
    result_2 = apk_generator.generate_apk_from_arabic(arabic_desc_2, OUTPUT_DIR)
    print(f"Result 2: {result_2}")

    # --- Test Case 3: App with internet permission ---
    arabic_desc_3 = "تطبيق بسيط يحتاج إلى إذن الإنترنت"
    print(f"\n--- Generating APK for: '{arabic_desc_3}' ---")
    result_3 = apk_generator.generate_apk_from_arabic(arabic_desc_3, OUTPUT_DIR)
    print(f"Result 3: {result_3}")

    # --- Test Case 4: Combined description ---
    arabic_desc_4 = "تطبيق بشاشة ترحيب تقول \"أهلاً وسهلاً\" وزر \"متابعة\""
    print(f"\n--- Generating APK for: '{arabic_desc_4}' ---")
    result_4 = apk_generator.generate_apk_from_arabic(arabic_desc_4, OUTPUT_DIR)
    print(f"Result 4: {result_4}")

    # --- Test Case 5: App with specific button ID and text ---
    arabic_desc_5 = "تطبيق به زر بمعرف \"start_button\" وزر بعنوان \"ابدأ الآن\""
    print(f"\n--- Generating APK for: '{arabic_desc_5}' ---")
    result_5 = apk_generator.generate_apk_from_arabic(arabic_desc_5, OUTPUT_DIR)
    print(f"Result 5: {result_5}")

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

    # Clean up dummy template if it was created and is no longer needed
    # This part might need refinement based on how the template is managed
    # For now, we'll leave it as is.