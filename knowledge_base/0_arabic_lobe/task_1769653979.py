import os
import subprocess
import shutil
from pathlib import Path

# Define constants for clarity and maintainability
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
GRADLE_WRAPPER_PATH = "./gradlew"  # Assuming gradlew is in the current directory or accessible via PATH

class ArabicAPKBuilder:
    """
    This module is responsible for taking Arabic natural language descriptions
    and generating functional Android APKs. It orchestrates the use of
    various specialized lobes to achieve this goal.
    """

    def __init__(self, project_name="MyArabicApp", package_name="com.example.myarabicapp"):
        """
        Initializes the APK builder with project and package details.

        Args:
            project_name (str): The name of the Android project.
            package_name (str): The package name for the Android application.
        """
        self.project_name = project_name
        self.package_name = package_name
        self.project_dir = Path(self.project_name)
        self.app_module_dir = self.project_dir / "app"
        self.src_dir = self.app_module_dir / "src" / "main"
        self.java_dir = self.src_dir / "java" / self.package_name.replace('.', os.sep)
        self.res_dir = self.app_module_dir / "src" / "main" / "res"
        self.manifest_path = self.src_dir / "AndroidManifest.xml"
        self.build_gradle_path = self.app_module_dir / "build.gradle"

        if not ANDROID_SDK_ROOT:
            raise EnvironmentError("ANDROID_SDK_ROOT environment variable is not set. Please set it to your Android SDK path.")

    def create_project_structure(self):
        """
        Creates the basic directory structure for an Android project.
        This mimics the structure created by Android Studio or Gradle.
        """
        print(f"Creating project structure for '{self.project_name}'...")
        self.project_dir.mkdir(exist_ok=True)
        self.app_module_dir.mkdir(parents=True, exist_ok=True)
        self.src_dir.mkdir(parents=True, exist_ok=True)
        self.java_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir.mkdir(parents=True, exist_ok=True)

        # Create an empty main activity file
        (self.java_dir / "MainActivity.java").touch()

        # Create a basic AndroidManifest.xml
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Create a basic build.gradle file
        build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{self.package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId "{self.package_name}"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
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
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        with open(self.build_gradle_path, "w", encoding="utf-8") as f:
            f.write(build_gradle_content)

        # Create a very basic strings.xml
        res_values_dir = self.res_dir / "values"
        res_values_dir.mkdir(parents=True, exist_ok=True)
        strings_xml_content = f"""
<resources>
    <string name="app_name">{self.project_name}</string>
</resources>
"""
        with open(res_values_dir / "strings.xml", "w", encoding="utf-8") as f:
            f.write(strings_xml_content)

        print("Project structure created successfully.")

    def parse_arabic_description(self, arabic_description: str):
        """
        This function would internally call Lobe 0 (Arabic Parser) to
        translate the Arabic natural language description into a structured
        representation that can be used to generate code and resources.

        For this example, we'll assume a very simple mapping for demonstration.
        A real implementation would involve sophisticated NLP.

        Args:
            arabic_description (str): The Arabic natural language input.

        Returns:
            dict: A structured representation of the app's components.
                  Example: {'activities': [{'name': 'HomeScreen', 'layout': 'home_screen'}],
                            'ui_elements': [{'type': 'button', 'text': 'Submit', 'action': 'submit_form'}]}
        """
        print(f"Parsing Arabic description: '{arabic_description}'...")
        # --- Lobe 0: Arabic Parser (Simulated) ---
        # In a real scenario, this would be a call to a complex Arabic NLP model.
        # For demonstration, we'll do a very basic keyword-based extraction.
        parsed_data = {
            "activities": [],
            "ui_elements": [],
            "strings": {},
            "layouts": {}
        }

        if "شاشة رئيسية" in arabic_description:
            parsed_data["activities"].append({"name": "HomeScreen", "layout": "activity_home_screen"})
            parsed_data["layouts"]["activity_home_screen"] = "activity_home_screen.xml"

        if "زر" in arabic_description:
            button_text = "اضغط هنا" # Default text if not specified
            if "زر باسم" in arabic_description:
                parts = arabic_description.split("زر باسم")
                if len(parts) > 1:
                    button_text_part = parts[1].split(" ")[0] # Get the first word after "باسم"
                    if button_text_part:
                        button_text = button_text_part

            parsed_data["ui_elements"].append({"type": "button", "text": button_text, "action": "button_click"})
            parsed_data["strings"][f"button_{len(parsed_data['ui_elements'])}"] = button_text

        if "نص" in arabic_description:
            text_content = "مرحبا بالعالم" # Default text
            if "نص يقول" in arabic_description:
                parts = arabic_description.split("نص يقول")
                if len(parts) > 1:
                    text_content_part = parts[1].split(" ")[0] # Get the first word after "يقول"
                    if text_content_part:
                        text_content = text_content_part
            parsed_data["ui_elements"].append({"type": "text", "content": text_content})
            parsed_data["strings"]["welcome_message"] = text_content


        print(f"Parsed data: {parsed_data}")
        # --- End Lobe 0 ---
        return parsed_data

    def generate_code_and_resources(self, parsed_data: dict):
        """
        This function calls Lobe 4 (Code Generation) and Lobe 6 (Synthesis)
        to generate Java/Kotlin code, layout XML files, and other resources
        based on the parsed data.

        Args:
            parsed_data (dict): The structured data from the Arabic parser.
        """
        print("Generating code and resources...")

        # --- Lobe 4: Code Generation Module (Simulated) ---
        # This would generate Java/Kotlin code for Activities, Fragments, etc.
        # and also generate layout XML files.
        print("  - Generating Java/Kotlin code...")
        activity_name = "MainActivity"
        if parsed_data.get("activities"):
            activity_name = parsed_data["activities"][0]["name"] # Assume first activity is main

        activity_code_path = self.java_dir / f"{activity_name}.java"
        activity_code_content = f"""
package {self.package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Determine layout dynamically based on parsed data
        int layoutId = getResources().getIdentifier("{parsed_data.get('activities', [{}])[0].get('layout', 'activity_main')}", "layout", getPackageName());
        setContentView(layoutId);

        // Handle UI elements from parsed data
        {self._generate_ui_element_handlers(parsed_data.get('ui_elements', []))}
    }}

    // Placeholder for button click handler
    public void onButtonClick(android.view.View v) {{
        Toast.makeText(this, "Button Clicked!", Toast.LENGTH_SHORT).show();
    }}
}}
"""
        with open(activity_code_path, "w", encoding="utf-8") as f:
            f.write(activity_code_content)
        print(f"    - Created: {activity_code_path}")

        # Generate layout XML files
        print("  - Generating layout XML files...")
        for layout_name, layout_filename in parsed_data.get("layouts", {}).items():
            layout_content = self._generate_layout_xml(layout_name, parsed_data.get('ui_elements', []))
            layout_dir = self.res_dir / "layout"
            layout_dir.mkdir(parents=True, exist_ok=True)
            with open(layout_dir / f"{layout_filename}.xml", "w", encoding="utf-8") as f:
                f.write(layout_content)
            print(f"    - Created: {layout_dir / f'{layout_filename}.xml'}")


        # Update strings.xml with dynamically generated strings
        strings_xml_path = self.res_dir / "values" / "strings.xml"
        if strings_xml_path.exists():
            with open(strings_xml_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                # Remove existing app_name if we are overriding it or adding new strings
                updated_lines = [line for line in lines if 'name="app_name"' not in line]
                if "app_name" not in parsed_data["strings"]: # Keep original if not overridden
                    updated_lines = lines

                for key, value in parsed_data.get("strings", {}).items():
                    updated_lines.append(f'    <string name="{key}">{value}</string>\n')
                f.seek(0)
                f.writelines(updated_lines)
                f.truncate()
        else:
            # Create a new strings.xml if it doesn't exist
            res_values_dir = self.res_dir / "values"
            res_values_dir.mkdir(parents=True, exist_ok=True)
            with open(strings_xml_path, "w", encoding="utf-8") as f:
                f.write("<resources>\n")
                for key, value in parsed_data.get("strings", {}).items():
                    f.write(f'    <string name="{key}">{value}</string>\n')
                f.write("</resources>\n")
        print("  - Updated strings.xml")
        # --- End Lobe 4 ---

        # --- Lobe 6: Synthesis Module (Simulated) ---
        # This lobe would coordinate the generation of different parts and ensure
        # they fit together. It might also handle more complex interactions.
        print("  - Synthesizing components...")
        # For this example, synthesis is mostly handled by the code generation
        # part which places files in correct locations.
        print("  - Synthesis complete.")
        # --- End Lobe 6 ---

        print("Code and resources generated successfully.")


    def _generate_ui_element_handlers(self, ui_elements):
        """
        Helper to generate Java code snippets for handling UI elements.
        """
        handlers = []
        button_counter = 0
        for element in ui_elements:
            if element["type"] == "button":
                button_counter += 1
                button_id_name = f"button_{button_counter}"
                resource_id = f"getResources().getIdentifier("
                resource_id += f'"{button_id_name}", "id", getPackageName())'

                handlers.append(f"""
        Button {button_id_name} = findViewById({resource_id});
        if ({button_id_name} != null) {{
            // Assuming button text is set dynamically or from strings.xml
            // {button_id_name}.setText("{element['text']}"); // Simplified for demo
            // {button_id_name}.setOnClickListener(v -> onButtonClick(v)); // Directly link to a method
             {button_id_name}.setOnClickListener(v -> {{
                 Toast.makeText(this, "Action for {element['text']}", Toast.LENGTH_SHORT).show();
             }});
        }}
""")
            elif element["type"] == "text":
                text_id_name = "welcomeTextView" # Generic ID for simplicity
                resource_id = f"getResources().getIdentifier("
                resource_id += f'"{text_id_name}", "id", getPackageName())'

                handlers.append(f"""
        TextView {text_id_name} = findViewById({resource_id});
        if ({text_id_name} != null) {{
            {text_id_name}.setText("{element['content']}");
        }}
""")
        return "\n".join(handlers)

    def _generate_layout_xml(self, layout_name, ui_elements):
        """
        Helper to generate layout XML content.
        """
        # Basic layout structure
        xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res-auto"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.replace('activity_', '').capitalize()}">
"""
        current_y_offset = 50 # Start position for the first element
        for i, element in enumerate(ui_elements):
            element_id = f"{element['type']}_{i+1}"
            if element['type'] == 'button':
                xml_content += f"""
    <Button
        android:id="@+id/{element_id}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/{self.get_string_key(element['text'], 'button')}"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        android:layout_marginTop="{current_y_offset}"
        app:layout_constraintVertical_bias="0.4"/>
"""
                current_y_offset += 60 # Increment position for next element
            elif element['type'] == 'text':
                xml_content += f"""
    <TextView
        android:id="@+id/{element_id}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/{self.get_string_key(element['content'], 'welcome_message')}"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        android:layout_marginBottom="{current_y_offset}"
        app:layout_constraintVertical_bias="0.2"/>
"""
                current_y_offset += 60

        xml_content += "</androidx.constraintlayout.widget.ConstraintLayout>"
        return xml_content

    def get_string_key(self, text_value, default_key):
        """
        Attempts to find a string key associated with a text value from parsed data,
        otherwise returns a default key.
        """
        for key, value in self.parsed_data.get("strings", {}).items():
            if value == text_value:
                return key
        return default_key


    def compile_apk(self):
        """
        This function calls Lobe 8 (APK Compiler) to build the APK.
        It requires a functional Gradle setup.

        Returns:
            bool: True if compilation was successful, False otherwise.
        """
        print("Compiling APK...")
        if not self.project_dir.exists():
            print(f"Error: Project directory '{self.project_dir}' does not exist. Cannot compile.")
            return False

        # --- Lobe 8: APK Compiler Module (Simulated) ---
        # This involves running the Gradle build command.
        try:
            # Ensure gradlew is executable
            if os.name == 'posix': # Linux/macOS
                os.chmod(GRADLE_WRAPPER_PATH, 0o755)
            elif os.name == 'nt': # Windows
                # No chmod needed for .bat, but ensure it exists
                pass

            if not Path(GRADLE_WRAPPER_PATH).exists():
                print(f"Error: Gradle wrapper '{GRADLE_WRAPPER_PATH}' not found.")
                return False

            # Execute the Gradle build command
            # Example: ./gradlew assembleDebug or ./gradlew assembleRelease
            # For simplicity, we'll build a debug APK.
            print(f"Executing: {GRADLE_WRAPPER_PATH} assembleDebug")
            result = subprocess.run(
                [GRADLE_WRAPPER_PATH, "assembleDebug"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True # Raises CalledProcessError if return code is non-zero
            )
            print("Gradle build output:")
            print(result.stdout)
            if result.stderr:
                print("Gradle build errors/warnings:")
                print(result.stderr)

            print("APK compiled successfully.")
            # The APK will be located in app/build/outputs/apk/debug/app-debug.apk
            return True

        except FileNotFoundError:
            print(f"Error: '{GRADLE_WRAPPER_PATH}' not found. Make sure it's in the project root or your PATH.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error during Gradle build:")
            print(f"Command: {e.cmd}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during compilation: {e}")
            return False
        # --- End Lobe 8 ---

    def deploy_apk(self, apk_path: str):
        """
        This function would call Lobe 10 (Deployment Module) to deploy the APK
        to a device or emulator. For now, it just prints the path.

        Args:
            apk_path (str): The path to the compiled APK.
        """
        print(f"\n--- Lobe 10: Arabic APK Builder Module ---")
        print(f"APK compiled successfully. Path: {apk_path}")
        print("Deployment to device/emulator would be handled by Lobe 10.")
        # In a real implementation, this would use ADB or other deployment tools.
        print("------------------------------------------")

    def build_apk_from_arabic(self, arabic_description: str):
        """
        The main orchestrator function to build an APK from an Arabic description.

        Args:
            arabic_description (str): The Arabic natural language input.
        """
        print(f"\n--- GRAND OBJECTIVE: Evolving into a unified, conscious mind ---")
        print(f"--- Objective: Generate hyper-efficient APK from natural language ---")

        # Step 1: Parse Arabic description (Lobe 0)
        self.parsed_data = self.parse_arabic_description(arabic_description)

        # Step 2: Create project structure
        self.create_project_structure()

        # Step 3: Generate code and resources (Lobe 4 & Lobe 6)
        self.generate_code_and_resources(self.parsed_data)

        # Step 4: Compile APK (Lobe 8)
        if self.compile_apk():
            # Step 5: Deploy APK (Lobe 10)
            apk_output_dir = self.project_dir / "app" / "build" / "outputs" / "apk" / "debug"
            apk_file_path = apk_output_dir / "app-debug.apk"
            if apk_file_path.exists():
                self.deploy_apk(str(apk_file_path))
            else:
                print(f"Error: Expected APK not found at {apk_file_path}")
        else:
            print("APK compilation failed. Deployment skipped.")

        print("\n--- APK Generation Process Complete ---")

    def cleanup_project(self):
        """
        Cleans up the generated project directory.
        """
        print(f"Cleaning up project directory: '{self.project_dir}'...")
        if self.project_dir.exists():
            try:
                shutil.rmtree(self.project_dir)
                print("Project directory removed successfully.")
            except OSError as e:
                print(f"Error removing directory {self.project_dir}: {e}")
        else:
            print("Project directory does not exist, no cleanup needed.")

if __name__ == '__main__':
    # Example Usage:
    # Ensure ANDROID_SDK_ROOT is set in your environment for Gradle to work correctly.
    # You might also need to have the Android SDK command-line tools installed
    # and configured for Gradle.

    # Example Arabic description: "أنشئ تطبيقًا بشاشة رئيسية وزر مكتوب عليه 'إرسال' ونَص يقول 'مرحباً بالعالم'."
    # (Create an application with a main screen, a button labeled 'Send', and text that says 'Hello World'.)

    arabic_prompt = "شاشة رئيسية بها زر ونص ترحيبي"

    builder = ArabicAPKBuilder(project_name="MyArabicApp", package_name="com.example.arabicapp")

    try:
        builder.build_apk_from_arabic(arabic_prompt)
    except EnvironmentError as e:
        print(f"Environment Error: {e}")
        print("Please ensure ANDROID_SDK_ROOT is set correctly.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Optional: Clean up the generated project files
    # builder.cleanup_project()