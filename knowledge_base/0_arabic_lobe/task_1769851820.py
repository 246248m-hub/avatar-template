import os
import shutil
import subprocess
import sys

# Assume these are defined in other lobes or configurations
KNOWLEDGE_BASE_DIR = "knowledge_base"
GENERATED_PROJECT_DIR = "generated_android_project"
OUTPUT_APK_DIR = "output_apks"

# --- Lobe 0_arabic_lobe ---
class ArabicNLPProcessor:
    def __init__(self, knowledge_base_path):
        self.knowledge_base_path = knowledge_base_path
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        print(f"ArabicNLPProcessor initialized with knowledge base: {self.knowledge_base_path}")

    def process_arabic_text(self, text):
        """
        Simulates processing Arabic natural language to extract intent and entities.
        In a real scenario, this would involve advanced NLP techniques.
        """
        print(f"Processing Arabic text: '{text}'")
        # Dummy extraction: identify keywords as entities and a simple intent
        keywords = text.lower().split()
        entities = {"words": keywords}
        intent = "general_query"
        if "app" in keywords or "application" in keywords:
            intent = "app_creation"
        if "create" in keywords or "build" in keywords:
            intent = "app_creation"

        print(f"Extracted intent: {intent}, entities: {entities}")
        return {"intent": intent, "entities": entities}

    def generate_android_project_structure(self, project_name, intent_data):
        """
        Simulates generating a basic Android project structure based on NLP output.
        This would involve creating directories, manifest, and basic Java/Kotlin files.
        """
        print(f"Generating Android project structure for '{project_name}'")
        project_path = os.path.join(GENERATED_PROJECT_DIR, project_name)
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "java", "com", "example", project_name.replace(" ", "").lower()), exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "layout"), exist_ok=True)

        # Create a dummy AndroidManifest.xml
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{project_name.replace(" ", "").lower()}">

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
        with open(os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Create a dummy strings.xml
        strings_content = f"""
<resources>
    <string name="app_name">{project_name}</string>
</resources>
"""
        with open(os.path.join(project_path, "app", "src", "main", "res", "values", "strings.xml"), "w", encoding="utf-8") as f:
            f.write(strings_content)

        # Create a dummy MainActivity.java
        main_activity_content = f"""
package com.example.{project_name.replace(" ", "").lower()};

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
        with open(os.path.join(project_path, "app", "src", "main", "java", "com", "example", project_name.replace(" ", "").lower(), "MainActivity.java"), "w", encoding="utf-8") as f:
            f.write(main_activity_content)

        # Create a dummy activity_main.xml
        activity_main_content = """
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
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(os.path.join(project_path, "app", "src", "main", "res", "layout", "activity_main.xml"), "w", encoding="utf-8") as f:
            f.write(activity_main_content)

        print(f"Generated project structure at: {project_path}")
        return project_path

    def cleanup_generated_project(self, project_path):
        """
        Removes the dummy generated project directory.
        """
        if os.path.exists(project_path):
            print(f"Cleaning up generated project: {project_path}")
            shutil.rmtree(project_path)

# --- Lobe 4_code_generation_lobe ---
class CodeGenerator:
    def __init__(self, target_language="java"):
        self.target_language = target_language
        print(f"CodeGenerator initialized for target language: {self.target_language}")

    def generate_code_from_intent(self, intent_data, project_path):
        """
        Generates code snippets or modifies existing code based on intent and entities.
        This is a placeholder for more sophisticated code generation logic.
        """
        print(f"Generating code for intent: {intent_data['intent']} with entities: {intent_data['entities']}")
        # In a real scenario, this would involve parsing intent_data and generating
        # specific Java/Kotlin code for UI elements, logic, etc.

        if intent_data["intent"] == "app_creation":
            # Example: Add a button and a TextView to the layout and handle its click
            activity_xml_path = os.path.join(project_path, "app", "src", "main", "res", "layout", "activity_main.xml")
            main_java_path = os.path.join(project_path, "app", "src", "main", "java", "com", "example", os.path.basename(project_path).replace(" ", "").lower(), "MainActivity.java")

            # Modify XML
            with open(activity_xml_path, "r", encoding="utf-8") as f:
                xml_content = f.read()

            # Simple modification: add a button below the TextView
            if "<TextView" in xml_content:
                modified_xml_content = xml_content.replace(
                    '<TextView',
                    '<TextView android:id="@+id/myTextView"\n'
                )
                modified_xml_content = modified_xml_content.replace(
                    'app:layout_constraintTop_toTopOf="parent"',
                    'app:layout_constraintTop_toBottomOf="@+id/myButton"\n        app:layout_constraintEnd_toEndOf="parent"\n        app:layout_constraintStart_toStartOf="parent"'
                )
                modified_xml_content = modified_xml_content.replace(
                    'tools:context=".MainActivity">',
                    'tools:context=".MainActivity">\n\n    <Button\n        android:id="@+id/myButton"\n        android:layout_width="wrap_content"\n        android:layout_height="wrap_content"\n        android:text="Click Me"\n        app:layout_constraintBottom_toBottomOf="parent"\n        app:layout_constraintLeft_toLeftOf="parent"\n        app:layout_constraintRight_toRightOf="parent"\n        app:layout_constraintTop_toTopOf="parent"\n        app:layout_constraintVertical_bias="0.6"/>'
                )
                with open(activity_xml_path, "w", encoding="utf-8") as f:
                    f.write(modified_xml_content)
                print(f"Modified {activity_xml_path} to add a button.")

            # Modify Java
            with open(main_java_path, "r", encoding="utf-8") as f:
                java_content = f.read()

            # Add imports and button click listener
            if "import androidx.appcompat.app.AppCompatActivity;" in java_content:
                java_content = java_content.replace(
                    "import androidx.appcompat.app.AppCompatActivity;",
                    "import androidx.appcompat.app.AppCompatActivity;\nimport android.widget.Button;\nimport android.widget.Toast;\nimport android.view.View;"
                )
                java_content = java_content.replace(
                    "setContentView(R.layout.activity_main);",
                    "setContentView(R.layout.activity_main);\n\n        Button myButton = findViewById(R.id.myButton);\n        myButton.setOnClickListener(new View.OnClickListener() {\n            @Override\n            public void onClick(View v) {\n                Toast.makeText(MainActivity.this, \"Button clicked!\", Toast.LENGTH_SHORT).show();\n            }\n        });"
                )
                with open(main_java_path, "w", encoding="utf-8") as f:
                    f.write(java_content)
                print(f"Modified {main_java_path} to add button click listener.")

        return project_path

# --- Lobe 8_apk_compiler_lobe ---
class APKCompiler:
    def __init__(self, android_sdk_path, output_dir):
        self.android_sdk_path = android_sdk_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"APKCompiler initialized. Android SDK: {self.android_sdk_path}, Output dir: {self.output_dir}")

    def compile_apk(self, project_path, project_name):
        """
        Compiles the Android project into an APK using Gradle.
        Requires Gradle and Android SDK to be installed and configured.
        """
        print(f"Starting APK compilation for project: {project_name} at {project_path}")
        output_apk_path = os.path.join(self.output_dir, f"{project_name.replace(' ', '').lower()}.apk")

        # Ensure Gradle wrapper is present or use system Gradle
        gradle_w = os.path.join(project_path, "gradlew")
        if not os.path.exists(gradle_w):
            print("Gradle wrapper not found. Attempting to use system Gradle.")
            gradle_command = "gradle"
        else:
            # Make gradlew executable
            st = os.stat(gradle_w)
            os.chmod(st.st_mode | 0o111, st.st_mode)
            gradle_command = gradle_w

        # Assume assembleDebug task for simplicity
        build_command = [gradle_command, "assembleDebug"]

        try:
            # Set JAVA_HOME if not already set or to ensure correct JDK is used
            java_home = os.environ.get("JAVA_HOME")
            if not java_home:
                # Attempt to find a common JDK path (this might need adjustment)
                possible_java_homes = [
                    "/usr/lib/jvm/java-11-openjdk-amd64",
                    "/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home",
                    "C:\\Program Files\\Java\\jdk-11.0.12"
                ]
                for jh in possible_java_homes:
                    if os.path.exists(os.path.join(jh, "bin", "java")):
                        java_home = jh
                        break
                if java_home:
                    print(f"JAVA_HOME not set, using detected: {java_home}")
                    env_vars = os.environ.copy()
                    env_vars["JAVA_HOME"] = java_home
                else:
                    print("Warning: JAVA_HOME not set and auto-detection failed. Compilation might fail.")
                    env_vars = os.environ.copy()
            else:
                env_vars = os.environ.copy()

            print(f"Executing command: {' '.join(build_command)} in directory: {project_path}")
            # Use subprocess.run with capture_output for better error handling
            process = subprocess.run(
                build_command,
                cwd=project_path,
                check=True,
                capture_output=True,
                text=True,
                env=env_vars
            )
            print("Gradle build output:\n", process.stdout)
            print("Gradle build errors:\n", process.stderr)
            print("APK compilation successful.")

            # Find the generated APK
            # The exact path can vary, common locations are app/build/outputs/apk/debug/
            debug_apk_path = os.path.join(project_path, "app", "build", "outputs", "apk", "debug", f"{project_name.replace(' ', '').lower()}-debug.apk")

            if os.path.exists(debug_apk_path):
                shutil.move(debug_apk_path, output_apk_path)
                print(f"APK moved to: {output_apk_path}")
            else:
                print(f"Error: Generated APK not found at expected location: {debug_apk_path}")
                return None

            return output_apk_path

        except FileNotFoundError:
            print(f"Error: '{gradle_command}' command not found. Is Gradle installed and in your PATH, or is the wrapper available?")
            print("Ensure Android SDK and Gradle are properly set up.")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error during Gradle build:")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            print("APK compilation failed.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during APK compilation: {e}")
            return None

# --- Main execution flow (simulated integration) ---
def main_demo_workflow():
    print("\n--- Starting Grand Objective Simulation ---")

    # --- Lobe 0: Arabic NLP Processing ---
    arabic_kb_path = KNOWLEDGE_BASE_DIR
    arabic_processor = ArabicNLPProcessor(arabic_kb_path)

    arabic_prompt = "ابني لي تطبيق بسيط يحتوي على زر" # "Build me a simple app with a button"
    processed_data = arabic_processor.process_arabic_text(arabic_prompt)

    project_name = "SimpleButtonApp"
    generated_project_path = arabic_processor.generate_android_project_structure(project_name, processed_data)

    # --- Lobe 4: Code Generation ---
    code_generator = CodeGenerator(target_language="java")
    modified_project_path = code_generator.generate_code_from_intent(processed_data, generated_project_path)

    # --- Lobe 8: APK Compilation ---
    # IMPORTANT: Set your actual Android SDK path here
    # Example paths:
    # Linux: "/usr/lib/android-sdk" or "/home/user/Android/Sdk"
    # macOS: "/Users/user/Library/Android/sdk"
    # Windows: "C:\\Users\\user\\AppData\\Local\\Android\\Sdk"
    android_sdk_path = os.environ.get("ANDROID_HOME") # Try to get from environment variable
    if not android_sdk_path:
        # Provide a fallback or prompt the user if not set
        print("\nWARNING: ANDROID_HOME environment variable not set.")
        print("Please set ANDROID_HOME to your Android SDK location for APK compilation.")
        print("Attempting to use common default paths (may fail)...")
        possible_paths = [
            "/usr/lib/android-sdk",
            "/home/user/Android/Sdk",
            "/Users/user/Library/Android/sdk",
            "C:\\Users\\user\\AppData\\Local\\Android\\Sdk"
        ]
        for path in possible_paths:
            if os.path.exists(os.path.join(path, "tools", "sdkmanager")) or os.path.exists(os.path.join(path, "cmdline-tools")):
                android_sdk_path = path
                print(f"Found potential SDK at: {android_sdk_path}")
                break
    if not android_sdk_path:
        print("Could not automatically determine Android SDK path. Please set ANDROID_HOME.")
        print("Skipping APK compilation step.")
        apk_output_path = None
    else:
        apk_compiler = APKCompiler(android_sdk_path, OUTPUT_APK_DIR)
        apk_output_path = apk_compiler.compile_apk(modified_project_path, project_name)

    print("\n--- Grand Objective Simulation Finished ---")
    if apk_output_path:
        print(f"Successfully generated APK: {apk_output_path}")
    else:
        print("APK generation process encountered issues.")

    # --- Cleanup ---
    print("\n--- Initiating Cleanup ---")
    arabic_processor.cleanup_generated_project(generated_project_path)
    if os.path.exists(arabic_kb_path):
        print(f"Cleaning up knowledge base: {arabic_kb_path}")
        shutil.rmtree(arabic_kb_path)
    if os.path.exists(OUTPUT_APK_DIR):
        print(f"Cleanup of output directory: {OUTPUT_APK_DIR}")
        # Optionally clean up the output APKs if needed, or leave them
        # for inspection. For this example, we'll leave them.
        pass
    print("Cleanup complete.")

if __name__ == "__main__":
    # Ensure necessary paths exist before running
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(GENERATED_PROJECT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_APK_DIR, exist_ok=True)

    # Call the main workflow function
    main_demo_workflow()