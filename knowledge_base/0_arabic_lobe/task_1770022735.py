import os
import shutil
import subprocess

# Assume these paths are defined elsewhere in the unified mind's context
# For demonstration, we'll define them here.
GENERATED_APK_DIR = "generated_apks"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
LANGUAGE_PACKAGE_BASE = "com.example.generatedapp"

def create_android_project(package_name, activity_name="MainActivity"):
    """
    Creates a basic Android project structure using the command line.
    This is a simplified representation and might require specific Android SDK setup.
    """
    project_name = package_name.split('.')[-1]
    project_dir = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, project_name)

    if os.path.exists(project_dir):
        print(f"Project directory '{project_dir}' already exists. Skipping creation.")
        return project_dir

    print(f"Creating Android project: {project_name} in {project_dir}")
    os.makedirs(project_dir, exist_ok=True)

    # Create manifest
    manifest_path = os.path.join(project_dir, "AndroidManifest.xml")
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{project_name.capitalize()}">
        <activity
            android:name=".{activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Create res/values/strings.xml
    res_values_dir = os.path.join(project_dir, "res", "values")
    os.makedirs(res_values_dir, exist_ok=True)
    strings_path = os.path.join(res_values_dir, "strings.xml")
    strings_content = f"""<resources>
    <string name="app_name">{project_name.capitalize()}</string>
</resources>
"""
    with open(strings_path, "w", encoding="utf-8") as f:
        f.write(strings_content)

    # Create res/values/themes.xml
    themes_path = os.path.join(res_values_dir, "themes.xml")
    themes_content = f"""<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.{project_name.capitalize()}" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <!-- Primary brand color. -->
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryVariant</item>
        <!-- Customize your theme here. -->
    </style>
</resources>
"""
    with open(themes_path, "w", encoding="utf-8") as f:
        f.write(themes_content)

    # Create res/values/colors.xml
    colors_path = os.path.join(res_values_dir, "colors.xml")
    colors_content = """<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
    with open(colors_path, "w", encoding="utf-8") as f:
        f.write(colors_content)

    # Create src/main/java/<package_name>/<activity_name>.java
    java_dir = os.path.join(project_dir, "src", "main", "java")
    package_path = os.path.join(java_dir, *package_name.split('.'))
    os.makedirs(package_path, exist_ok=True)
    activity_path = os.path.join(package_path, f"{activity_name}.java")
    activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // setContentView(R.layout.activity_{project_name.lower()}); // Placeholder for layout
        setContentView(android.R.layout.simple_list_item_1); // Using a basic layout for demo
        System.out.println("Hello from {activity_name}!"); // Placeholder for logic
    }}
}}
"""
    with open(activity_path, "w", encoding="utf-8") as f:
        f.write(activity_content)

    # Create dummy layout file (optional, but good for completeness)
    res_layout_dir = os.path.join(project_dir, "res", "layout")
    os.makedirs(res_layout_dir, exist_ok=True)
    layout_path = os.path.join(res_layout_dir, f"activity_{project_name.lower()}.xml")
    layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <!-- Content for your activity will go here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout_content)


    print(f"Android project created at: {project_dir}")
    return project_dir

def build_apk_from_project(project_dir, output_dir):
    """
    Builds an APK from a given Android project directory.
    This function assumes the 'gradlew' executable is available in the project's root.
    For a real scenario, this would involve calling the Android build tools.
    """
    if not os.path.exists(project_dir):
        print(f"Error: Project directory '{project_dir}' not found.")
        return None

    print(f"\n--- Building APK for project in '{project_dir}' ---")
    os.makedirs(output_dir, exist_ok=True)

    # Ensure gradlew is executable
    gradlew_path = os.path.join(project_dir, "gradlew")
    if os.path.exists(gradlew_path):
        st = os.stat(gradlew_path)
        os.chmod(gradlew_path, st.st_mode | 0o111) # Add execute permissions
    else:
        print(f"Error: 'gradlew' not found in '{project_dir}'. Cannot build APK.")
        print("Please ensure you have a proper Android project structure with Gradle.")
        return None

    # Execute Gradle build command
    # 'assembleDebug' will build a debug APK
    # For production, 'assembleRelease' would be used, requiring signing configurations.
    build_command = ["./gradlew", "assembleDebug"]
    print(f"Running command: {' '.join(build_command)} in directory: {project_dir}")

    try:
        # Running the build process
        # Capturing stdout and stderr for debugging
        process = subprocess.Popen(build_command, cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        print("Gradle Build Output:\n", stdout)
        if stderr:
            print("Gradle Build Error Output:\n", stderr)

        if process.returncode == 0:
            print("APK build successful.")
            # The APK is typically found in app/build/outputs/apk/debug/
            apk_path_relative = os.path.join("app", "build", "outputs", "apk", "debug", f"{os.path.basename(project_dir)}-debug.apk")
            generated_apk_path = os.path.join(project_dir, apk_path_relative)

            if os.path.exists(generated_apk_path):
                final_apk_name = f"{os.path.basename(project_dir)}_{os.path.basename(generated_apk_path)}"
                final_apk_path = os.path.join(output_dir, final_apk_name)
                shutil.copy(generated_apk_path, final_apk_path)
                print(f"APK copied to: {final_apk_path}")
                return final_apk_path
            else:
                print(f"Error: Expected APK not found at '{generated_apk_path}'. Build might have succeeded but APK location is different.")
                return None
        else:
            print(f"APK build failed with return code {process.returncode}.")
            return None

    except FileNotFoundError:
        print("Error: 'gradlew' command not found. Ensure Gradle is installed and accessible in your PATH, or the gradlew script exists and is executable.")
        return None
    except Exception as e:
        print(f"An error occurred during APK build: {e}")
        return None

def cleanup_android_project_template():
    """
    Cleans up the dummy Android project template directory.
    """
    print(f"\n--- Cleaning up demo project template directory: {ANDROID_PROJECT_TEMPLATE_DIR} ---")
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        try:
            shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
            print(f"Removed: {ANDROID_PROJECT_TEMPLATE_DIR}")
        except OSError as e:
            print(f"Error removing directory {ANDROID_PROJECT_TEMPLATE_DIR}: {e}")
    else:
        print("Directory not found, nothing to clean up.")

def create_arabic_driven_app(nlp_output, output_apk_dir=GENERATED_APK_DIR):
    """
    This function acts as a bridge between Lobe 0 (language processing)
    and Lobe 8 (APK compilation). It takes structured NLP output
    (presumably from Arabic processing) and initiates the Android project
    creation and APK building process.

    Args:
        nlp_output (dict): A dictionary containing structured information derived
                           from natural language input. Expected keys might include:
                           'app_name' (str): The desired name for the application.
                           'package_name' (str): The desired package name for the app.
                           'main_activity_name' (str): Name for the main activity.
                           'ui_elements' (list): A list of UI elements and their
                                                 configurations to be placed in the activity.
                                                 (More complex UI generation would be here).
        output_apk_dir (str): The directory where the generated APK will be saved.

    Returns:
        str or None: The path to the generated APK if successful, otherwise None.
    """
    print("\n--- Lobe 4_code_generation_lobe: Initiating Arabic-driven App Generation ---")

    if not nlp_output:
        print("Error: No NLP output provided for app generation.")
        return None

    # Extract information for Android project creation
    app_name = nlp_output.get('app_name', 'MyArabicApp')
    package_name = nlp_output.get('package_name', f"{LANGUAGE_PACKAGE_BASE}.{app_name.lower().replace(' ', '')}")
    main_activity_name = nlp_output.get('main_activity_name', 'MainActivity')

    print(f"App Name: {app_name}")
    print(f"Package Name: {package_name}")
    print(f"Main Activity: {main_activity_name}")

    # --- Step 1: Create Android Project Structure ---
    # This is a placeholder for Lobe 4's code generation logic.
    # In a more advanced scenario, nlp_output['ui_elements'] would be used
    # to generate layouts (res/layout/*.xml) and populate the Activity Java code.
    created_project_dir = create_android_project(package_name, main_activity_name)

    if not created_project_dir:
        print("Failed to create Android project structure.")
        return None

    # --- Step 2: Populate Activity Logic and Layout (Placeholder) ---
    # Here, you would use nlp_output['ui_elements'] and potentially
    # other structured data from Lobe 0 to modify the generated Java code
    # and XML layout files.

    # Example of how you might add a simple TextView to the layout based on NLP
    # For this simplified example, we'll just assume the basic template is sufficient.
    if 'app_description' in nlp_output:
        description = nlp_output['app_description']
        print(f"App description from NLP: '{description}' (This would be used to populate UI)")
        # In a real implementation, you'd parse this and add relevant UI elements.

    # --- Step 3: Build the APK ---
    print("\n--- Initiating APK Compilation (Lobe 8 integration) ---")
    generated_apk_path = build_apk_from_project(created_project_dir, output_apk_dir)

    if generated_apk_path:
        print(f"\nSuccessfully generated APK at: {generated_apk_path}")
        return generated_apk_path
    else:
        print("\nAPK generation process failed.")
        return None

# --- Demo Usage ---
if __name__ == "__main__":
    # Simulate NLP output that Lobe 0 would provide
    # This dictionary structure would be generated by Lobe 0 after processing Arabic text.
    simulated_nlp_output = {
        "app_name": "MyArabicApp",
        "package_name": "com.example.myarabicapp",
        "main_activity_name": "MyAwesomeActivity",
        "app_description": "This app displays information related to Arabic culture.",
        "ui_elements": [
            {"type": "TextView", "text": "مرحبا بالعالم", "id": "welcome_text"},
            {"type": "Button", "text": "اضغط هنا", "id": "action_button"}
        ]
    }

    print("--- Starting Lobe 4 Demo: Arabic-driven App Generation ---")

    # Ensure the base output directory exists
    os.makedirs(GENERATED_APK_DIR, exist_ok=True)

    # Call the function to create the app and build the APK
    final_apk_path = create_arabic_driven_app(simulated_nlp_output, GENERATED_APK_DIR)

    if final_apk_path:
        print(f"\n--- Lobe 4 Demo Finished: APK created successfully at {final_apk_path} ---")
    else:
        print("\n--- Lobe 4 Demo Finished: APK generation failed ---")

    # Clean up the dummy project created for this demo run
    # In a real scenario, this cleanup might be managed by a higher-level orchestrator.
    print("\n--- Cleaning up demo project template ---")
    cleanup_android_project_template()
    print("\n--- Lobe 4 Demo Finished ---")