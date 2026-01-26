import os
import logging
import subprocess

# Assume JAVA_PROJECT_DIR and KNOWLEDGE_BASE_DIR are defined globally or passed as arguments
# For demonstration, let's define them here
JAVA_PROJECT_DIR = "dummy_java_project"
KNOWLEDGE_BASE_DIR = "knowledge_base"

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ArabicCodeGenerator:
    """
    A module responsible for generating Arabic code snippets and integrating them
    into a Java project structure.
    """
    def __init__(self, java_project_dir: str, knowledge_base_dir: str):
        self.java_project_dir = java_project_dir
        self.knowledge_base_dir = knowledge_base_dir
        logging.info(f"ArabicCodeGenerator initialized with project dir: {self.java_project_dir}")
        logging.info(f"Knowledge base dir: {self.knowledge_base_dir}")

    def _ensure_project_structure(self):
        """
        Ensures the basic Java project structure exists.
        Creates dummy files for demonstration if they don't exist.
        """
        os.makedirs(os.path.join(self.java_project_dir, "app", "src", "main", "java", "com", "example", "arabicapp"), exist_ok=True)
        os.makedirs(os.path.join(self.java_project_dir, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(self.java_project_dir, "app", "src", "main", "assets"), exist_ok=True)

        # Create dummy AndroidManifest.xml if it doesn't exist
        manifest_path = os.path.join(self.java_project_dir, "app", "src", "main", "AndroidManifest.xml")
        if not os.path.exists(manifest_path):
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.arabicapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.ArabicApp">
        <activity android:name=".MainActivity"></activity>
    </application>
</manifest>
""")
            logging.info(f"Created dummy AndroidManifest.xml at {manifest_path}")

        # Create dummy build.gradle if it doesn't exist
        build_gradle_path = os.path.join(self.java_project_dir, "app", "build.gradle")
        if not os.path.exists(build_gradle_path):
            with open(build_gradle_path, "w", encoding="utf-8") as f:
                f.write("""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.arabicapp'
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
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""")
            logging.info(f"Created dummy app/build.gradle at {build_gradle_path}")

        # Create dummy gradlew script if it doesn't exist
        gradlew_path = os.path.join(self.java_project_dir, "gradlew")
        if not os.path.exists(gradlew_path):
            with open(gradlew_path, "w", encoding="utf-8") as f:
                f.write("#!/bin/bash\n")
                f.write("echo 'Simulating gradlew execution'\n")
                f.write("exit 0\n")
            os.chmod(gradlew_path, 0o755)  # Make it executable
            logging.info(f"Created dummy gradlew script at {gradlew_path}")


    def generate_arabic_component(self, component_type: str, component_name: str, code_logic: str) -> str:
        """
        Generates a specific Arabic-focused component (e.g., a Java Activity,
        a Kotlin Fragment, or a layout XML file) based on the provided logic.

        Args:
            component_type (str): The type of component to generate ('Activity', 'Fragment', 'Layout').
            component_name (str): The name of the component.
            code_logic (str): Natural language description of the component's logic.

        Returns:
            str: The path to the generated component file.
        """
        logging.info(f"Generating {component_type} '{component_name}' with logic: '{code_logic}'")

        if component_type == 'Activity':
            java_file_path = os.path.join(self.java_project_dir, "app", "src", "main", "java", "com", "example", "arabicapp", f"{component_name}.java")
            with open(java_file_path, "w", encoding="utf-8") as f:
                f.write(self._generate_java_activity_code(component_name, code_logic))
            logging.info(f"Generated Java Activity: {java_file_path}")
            return java_file_path

        elif component_type == 'Fragment':
            kotlin_file_path = os.path.join(self.java_project_dir, "app", "src", "main", "java", "com", "example", "arabicapp", f"{component_name}.kt")
            with open(kotlin_file_path, "w", encoding="utf-8") as f:
                f.write(self._generate_kotlin_fragment_code(component_name, code_logic))
            logging.info(f"Generated Kotlin Fragment: {kotlin_file_path}")
            return kotlin_file_path

        elif component_type == 'Layout':
            layout_file_path = os.path.join(self.java_project_dir, "app", "src", "main", "res", "layout", f"activity_{component_name.lower()}.xml")
            with open(layout_file_path, "w", encoding="utf-8") as f:
                f.write(self._generate_layout_xml(component_name, code_logic))
            logging.info(f"Generated Layout XML: {layout_file_path}")
            return layout_file_path

        else:
            logging.error(f"Unsupported component type: {component_type}")
            raise ValueError(f"Unsupported component type: {component_type}")

    def _generate_java_activity_code(self, activity_name: str, logic: str) -> str:
        """
        Generates boilerplate Java code for an Android Activity, incorporating
        basic logic derived from natural language.
        """
        # This is a simplified generation. A real implementation would involve
        # more sophisticated NLP to parse 'logic' and generate meaningful code.
        setup_code = ""
        if "initialize a text view" in logic.lower() and "display" in logic.lower():
            view_name = "myTextView"
            text_to_display = logic.split("display")[-1].strip().strip('"')
            setup_code += f"""
        TextView {view_name} = findViewById(R.id.text_view_id); // Assuming a TextView with id 'text_view_id' exists in layout
        {view_name}.setText("{text_to_display}");
        Log.i("ArabicActivity", "Text view updated.");
"""
        elif "handle a button click" in logic.lower():
            button_id = "myButton"
            action_description = logic.split("handle a button click")[-1].strip()
            setup_code += f"""
        Button {button_id} = findViewById(R.id.button_id); // Assuming a Button with id 'button_id'
        {button_id}.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                // Logic for button click: {action_description}
                Log.i("ArabicActivity", "Button clicked!");
                // Add actual logic here based on parsed 'action_description'
            }}
        }});
        Log.i("ArabicActivity", "Button click listener set.");
"""

        return f"""package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Typically, you would set a layout here
        // setContentView(R.layout.activity_{activity_name.lower()}); // Assuming a layout file

        // Basic logic derived from natural language prompt: "{logic}"
{setup_code}
        Log.i("ArabicActivity", "{activity_name} created.");
    }}
}}
"""

    def _generate_kotlin_fragment_code(self, fragment_name: str, logic: str) -> str:
        """
        Generates boilerplate Kotlin code for an Android Fragment.
        """
        setup_code = ""
        if "initialize a text view" in logic.lower() and "display" in logic.lower():
            view_name = "myTextView"
            text_to_display = logic.split("display")[-1].strip().strip('"')
            setup_code += f"""
        view?.findViewById<TextView>(R.id.text_view_id)?.apply {{ // Assuming a TextView with id 'text_view_id'
            text = "{text_to_display}"
            Log.i("ArabicFragment", "Text view updated.")
        }}
"""
        elif "handle a button click" in logic.lower():
            button_id = "myButton"
            action_description = logic.split("handle a button click")[-1].strip()
            setup_code += f"""
        view?.findViewById<Button>(R.id.button_id)?.setOnClickListener {{ // Assuming a Button with id 'button_id'
            // Logic for button click: {action_description}
            Log.i("ArabicFragment", "Button clicked!")
            // Add actual logic here based on parsed 'action_description'
        }}
        Log.i("ArabicFragment", "Button click listener set.")
"""

        return f"""package com.example.arabicapp

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Button
import androidx.fragment.app.Fragment

class {fragment_name} : Fragment() {{

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {{
        // Inflate the layout for this fragment
        // return inflater.inflate(R.layout.fragment_{fragment_name.lower()}, container, false) // Assuming a layout file

        // Basic logic derived from natural language prompt: "{logic}"
{setup_code}
        Log.i("ArabicFragment", "{fragment_name} view created.")
        return super.onCreateView(inflater, container, savedInstanceState)
    }}
}}
"""

    def _generate_layout_xml(self, layout_name: str, logic: str) -> str:
        """
        Generates a basic Android layout XML file.
        """
        content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_or_fragment_name}">
""".format(activity_or_fragment_name=layout_name) # Placeholder for context

        if "initialize a text view" in logic.lower():
            text_content = logic.split("display")[-1].strip().strip('"')
            content += f"""
    <TextView
        android:id="@+id/text_view_id"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{text_content}"
        android:textSize="24sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />
"""
        if "handle a button click" in logic.lower():
            button_text = logic.split("handle a button click")[-1].strip().split("and")[0].strip().strip('"') or "Click Me"
            content += f"""
    <Button
        android:id="@+id/button_id"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{button_text}"
        app:layout_constraintTop_toBottomOf="@id/text_view_id"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>
"""
        content += "\n</androidx.constraintlayout.widget.ConstraintLayout>"
        return content

    def integrate_arabic_component(self, component_path: str, target_activity_or_fragment: str):
        """
        Integrates a generated Arabic component into a target activity or fragment.
        This is a conceptual placeholder for deeper integration logic.
        """
        logging.info(f"Integrating component '{component_path}' into '{target_activity_or_fragment}'.")
        # This method would parse the target activity/fragment code and add calls
        # to instantiate or reference the new component.
        # For example, if a new Activity is generated, this method would modify
        # AndroidManifest.xml to declare it, or modify an existing Activity to
        # start this new Activity.
        pass # Placeholder for actual integration logic

    def build_apk(self, output_dir: str = "./builds") -> str:
        """
        Attempts to build the APK using Gradle.
        This method assumes a functional Gradle environment and project setup.
        """
        logging.info(f"Attempting to build APK in: {self.java_project_dir}")
        os.makedirs(output_dir, exist_ok=True)
        gradlew_path = os.path.join(self.java_project_dir, "gradlew")

        if not os.path.exists(gradlew_path):
            logging.error("gradlew script not found. Cannot build APK.")
            raise FileNotFoundError("gradlew script not found. Cannot build APK.")

        try:
            # Execute the Gradle wrapper to build the AAB (which can be converted to APK)
            # or directly build APK if configured. For simplicity, we'll use 'assemble'.
            # The actual command might vary depending on the Gradle setup.
            command = [gradlew_path, "assembleDebug"]
            logging.info(f"Executing command: {' '.join(command)}")
            process = subprocess.Popen(command, cwd=self.java_project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            logging.info("Gradle stdout:\n" + stdout)
            logging.error("Gradle stderr:\n" + stderr)

            if process.returncode == 0:
                logging.info("APK build process completed successfully (or at least Gradle exited with 0).")
                # Find the generated APK file (path might vary based on Gradle version and config)
                # Common path: app/build/outputs/apk/debug/app-debug.apk
                apk_path_relative = os.path.join("app", "build", "outputs", "apk", "debug", "app-debug.apk")
                generated_apk_path = os.path.join(self.java_project_dir, apk_path_relative)

                if os.path.exists(generated_apk_path):
                    final_apk_name = f"arabicapp_{os.path.basename(self.java_project_dir)}_{os.urandom(4).hex()}.apk"
                    final_apk_path = os.path.join(output_dir, final_apk_name)
                    os.rename(generated_apk_path, final_apk_path)
                    logging.info(f"APK built and saved to: {final_apk_path}")
                    return final_apk_path
                else:
                    logging.warning(f"APK file not found at expected location: {generated_apk_path}. Build might have succeeded but output path is different.")
                    return ""
            else:
                logging.error(f"APK build failed with return code {process.returncode}.")
                return ""

        except Exception as e:
            logging.error(f"An error occurred during APK build: {e}")
            return ""

    def cleanup_project_files(self):
        """
        Cleans up dummy project files created for demonstration.
        """
        logging.info(f"Cleaning up dummy project directory: {self.java_project_dir}")
        if os.path.exists(self.java_project_dir):
            try:
                import shutil
                shutil.rmtree(self.java_project_dir)
                logging.info(f"Successfully removed directory: {self.java_project_dir}")
            except OSError as e:
                logging.error(f"Error removing directory {self.java_project_dir}: {e}")
                print(f"Error removing directory {self.java_project_dir}: {e}")
        else:
            print("Dummy project directory not found for cleanup.")

# Example Usage (demonstrating the module's functionality)
if __name__ == "__main__":
    # Ensure dummy directories exist
    os.makedirs(JAVA_PROJECT_DIR, exist_ok=True)
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

    generator = ArabicCodeGenerator(JAVA_PROJECT_DIR, KNOWLEDGE_BASE_DIR)
    generator._ensure_project_structure()

    print("\n--- Generating Arabic Components ---")

    # Generate an Activity
    activity_logic = "This activity should initialize a text view and display 'مرحباً بالعالم!'"
    main_activity_path = generator.generate_arabic_component("Activity", "MainActivity", activity_logic)
    print(f"Generated: {main_activity_path}")

    # Generate a Fragment
    fragment_logic = "This fragment should initialize a text view and display 'جزء العربية'"
    arabic_fragment_path = generator.generate_arabic_component("Fragment", "ArabicFragment", fragment_logic)
    print(f"Generated: {arabic_fragment_path}")

    # Generate a Layout XML
    layout_logic = "This layout should contain a text view displaying 'تصميم الواجهة' and a button to 'ابدأ العملية'"
    main_layout_path = generator.generate_arabic_component("Layout", "MainActivity", layout_logic)
    print(f"Generated: {main_layout_path}")

    # Demonstrate integrating a component (conceptual)
    generator.integrate_arabic_component(main_activity_path, "SomeEntryActivity")

    print("\n--- Attempting APK Build (will likely fail without proper SDK/NDK setup) ---")
    # The build_apk method is a placeholder and requires a full Android SDK and NDK setup
    # to actually succeed. It will likely fail with the dummy gradlew script.
    # For real execution, replace dummy gradlew with actual and have Android build tools installed.
    # generated_apk = generator.build_apk(output_dir="./apk_builds")
    # if generated_apk:
    #     print(f"APK successfully built and saved to: {generated_apk}")
    # else:
    #     print("APK build failed. Ensure Android SDK and NDK are configured.")

    print("\n--- Cleaning up dummy files ---")
    generator.cleanup_project_files()

    print("\n--- Arabic Code Generator Module Demo Finished ---")