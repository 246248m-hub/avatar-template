import os
import shutil
import subprocess

# Global constants (can be adjusted based on actual project structure)
ANDROID_PROJECT_TEMPLATE_DIR = "./android_project_template"
OUTPUT_APKS_DIR = "./generated_apks"
JAVA_COMPILER_PATH = "javac"  # Path to your Java compiler
DX_TOOL_PATH = "dx"  # Path to your dx tool (part of Android SDK build-tools)
AAPT_TOOL_PATH = "aapt"  # Path to your aapt tool (part of Android SDK build-tools)
APKSIGNER_TOOL_PATH = "apksigner" # Path to your apksigner tool (part of Android SDK build-tools)
KEYSTORE_PATH = "./debug.keystore" # Path to your debug keystore
KEYSTORE_ALIAS = "androiddebugkey"
KEYSTORE_PASSWORD = "android"


def create_android_project_structure(project_name="MyApp"):
    """
    Creates a basic Android project directory structure.
    This is a simplified template. A real implementation would involve
    more complex templating for manifest, build.gradle, etc.
    """
    if not os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR)

    src_dir = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main")
    os.makedirs(src_dir, exist_ok=True)

    # Create a minimal AndroidManifest.xml
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{project_name.lower()}">
    <application android:allowBackup="true"
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
    with open(os.path.join(src_dir, "AndroidManifest.xml"), "w") as f:
        f.write(manifest_content)

    # Create minimal res/values directories and string resources
    res_dir = os.path.join(src_dir, "res")
    os.makedirs(res_dir, exist_ok=True)
    values_dir = os.path.join(res_dir, "values")
    os.makedirs(values_dir, exist_ok=True)
    strings_content = f"""
<resources>
    <string name="app_name">{project_name}</string>
</resources>
"""
    with open(os.path.join(values_dir, "strings.xml"), "w") as f:
        f.write(strings_content)

    # Create a dummy MainActivity.java
    java_package_dir = os.path.join(src_dir, "java", "com", "example", project_name.lower())
    os.makedirs(java_package_dir, exist_ok=True)
    main_activity_content = """
package com.example.%s;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists
    }
}
""" % project_name.lower()
    with open(os.path.join(java_package_dir, "MainActivity.java"), "w") as f:
        f.write(main_activity_content)

    print(f"Created basic Android project structure in: {ANDROID_PROJECT_TEMPLATE_DIR}")
    return True

def compile_java_to_dex(java_source_dir, output_classes_dex):
    """
    Compiles Java source files into a classes.dex file using dx tool.
    This is a simplified approach. A real build would use Gradle.
    """
    java_files = []
    for root, _, files in os.walk(java_source_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))

    if not java_files:
        print("No Java files found to compile.")
        return False

    # Compile Java files to class files first
    class_files_dir = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "classes")
    os.makedirs(class_files_dir, exist_ok=True)
    compile_command = [JAVA_COMPILER_PATH, "-d", class_files_dir] + java_files
    try:
        subprocess.run(compile_command, check=True, capture_output=True, text=True)
        print("Java files compiled to class files successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Java files: {e.stderr}")
        return False

    # Convert class files to DEX format
    dex_command = [DX_TOOL_PATH, "--dex", "--output=" + output_classes_dex, class_files_dir]
    try:
        subprocess.run(dex_command, check=True, capture_output=True, text=True)
        print(f"Compiled classes to DEX format: {output_classes_dex}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting to DEX: {e.stderr}")
        return False
    finally:
        # Clean up intermediate class files
        if os.path.exists(class_files_dir):
            shutil.rmtree(class_files_dir)


def create_apk(project_name, classes_dex_path):
    """
    Builds a basic APK from the DEX file and AndroidManifest.xml.
    This is a highly simplified process and bypasses many build steps.
    """
    if not os.path.exists(OUTPUT_APKS_DIR):
        os.makedirs(OUTPUT_APKS_DIR)

    apk_path = os.path.join(OUTPUT_APKS_DIR, f"{project_name}.apk")
    temp_apk_dir = os.path.join(OUTPUT_APKS_DIR, f"{project_name}_temp")
    os.makedirs(temp_apk_dir, exist_ok=True)

    try:
        # 1. Use AAPT to create an unsigned APK (aapt package -f -M ... -I ... -F ...)
        manifest_path = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "AndroidManifest.xml")
        android_jar_path = os.path.join(os.environ.get("ANDROID_HOME", ""), "platforms", "android-30", "android.jar") # Adjust platform version as needed

        aapt_command = [
            AAPT_TOOL_PATH, "package",
            "-M", manifest_path,
            "-I", android_jar_path,
            "-F", os.path.join(temp_apk_dir, f"{project_name}.unsigned.apk"),
            "-A", os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "assets"), # Assuming assets directory exists
            "--rename-manifest-package", f"com.example.{project_name.lower()}" # Ensure package name is consistent
        ]
        subprocess.run(aapt_command, check=True, capture_output=True, text=True)
        print("Unsigned APK created with AAPT.")

        # 2. Add the classes.dex file to the unsigned APK
        # This step is usually handled by build tools like Gradle or dx directly packaging.
        # For simplicity here, we'll use a tool like `zip` to add the dex file.
        # A more robust approach would involve ApkBuilder.
        unsigned_apk_path = os.path.join(temp_apk_dir, f"{project_name}.unsigned.apk")
        with open(unsigned_apk_path, "rb") as f_in:
            unsigned_apk_content = f_in.read()

        with open(unsigned_apk_path, "wb") as f_out:
            f_out.write(unsigned_apk_content)
            # Add classes.dex file
            with open(classes_dex_path, "rb") as f_dex:
                f_out.write(f_dex.read())
        print("Added classes.dex to unsigned APK.")

        # 3. Sign the APK using apksigner
        # Ensure you have a debug.keystore. If not, it will be created by Android SDK build tools
        # when you run `keytool -genkey ...` or it's automatically generated by some IDEs.
        # For this example, we assume it exists at KEYSTORE_PATH.
        if not os.path.exists(KEYSTORE_PATH):
            print(f"Error: Keystore not found at {KEYSTORE_PATH}. Please generate a debug keystore.")
            return False

        sign_command = [
            APKSIGNER_TOOL_PATH, "sign",
            "--ks", KEYSTORE_PATH,
            "--ks-alias", KEYSTORE_ALIAS,
            "--ks-key-alias", KEYSTORE_ALIAS,
            "--ks-pass", f"pass:{KEYSTORE_PASSWORD}",
            "--in", unsigned_apk_path,
            "--out", apk_path
        ]
        subprocess.run(sign_command, check=True, capture_output=True, text=True)
        print(f"APK signed successfully: {apk_path}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error during APK creation: {e.stderr}")
        return False
    finally:
        if os.path.exists(temp_apk_dir):
            shutil.rmtree(temp_apk_dir)

def generate_arabic_apk_from_nlp(natural_language_input: str) -> str:
    """
    This module is a placeholder for the Arabic NLP integration and APK generation.
    It would parse the natural language, extract requirements,
    generate Android project code, compile it, and package it into an APK.

    For this example, we simulate the process by:
    1. Creating a basic Android project structure.
    2. Compiling a dummy Java file to DEX.
    3. Packaging and signing a dummy APK.
    """
    project_name = "ArabicApp" # Example project name, could be derived from input

    # Simulate NLP processing to determine project name and potentially content
    print(f"NLP Processing for: '{natural_language_input}'")
    # In a real scenario, Lobe 0_language_lobe and Lobe 6_synthesis_lobe
    # would have already processed this and prepared the necessary code/assets.

    # Assume we have a project name derived from the NLP input
    # project_name = derive_project_name_from_nlp(natural_language_input)

    print(f"\n--- Building APK for project: {project_name} ---")

    # 1. Create a basic Android project structure
    if not create_android_project_structure(project_name):
        print("Failed to create Android project structure.")
        return "APK generation failed."

    # 2. Compile dummy Java code to DEX
    # In a real scenario, this would involve generating actual Java code based on NLP.
    # Here we use the dummy MainActivity.java created in the template.
    dummy_java_source_dir = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java")
    dex_output_path = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "classes.dex")
    if not compile_java_to_dex(dummy_java_source_dir, dex_output_path):
        print("Failed to compile Java to DEX.")
        return "APK generation failed."

    # 3. Create and sign the APK
    if not create_apk(project_name, dex_output_path):
        print("Failed to create and sign APK.")
        return "APK generation failed."

    print(f"\n--- APK generation process for '{project_name}' completed. ---")
    return os.path.join(OUTPUT_APKS_DIR, f"{project_name}.apk")

# Example usage (for demonstration purposes outside of the main loop)
if __name__ == "__main__":
    # This part is for testing the module in isolation.
    # In the grand objective, this function would be called by a higher-level orchestrator.

    # Ensure necessary tools are in PATH or specify their full paths
    # You might need to set ANDROID_HOME environment variable.
    # Example: os.environ['ANDROID_HOME'] = '/path/to/android/sdk'

    # Clean up previous runs
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
    if os.path.exists(OUTPUT_APKS_DIR):
        shutil.rmtree(OUTPUT_APKS_DIR)

    print("--- Starting Arabic APK Generation Module Demo ---")

    arabic_nlp_input = "Create a simple Android app that displays 'Hello, World!' in Arabic."
    generated_apk_path = generate_arabic_apk_from_nlp(arabic_nlp_input)

    if generated_apk_path != "APK generation failed.":
        print(f"\nSuccessfully generated APK: {generated_apk_path}")
    else:
        print("\nAPK generation process failed.")

    print("\n--- Arabic APK Generation Module Demo Finished ---")

    # Clean up dummy files after demo
    print("\n--- Cleaning up dummy files ---")
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        print(f"Removed dummy Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
    if os.path.exists(OUTPUT_APKS_DIR):
        shutil.rmtree(OUTPUT_APKS_DIR)
        print(f"Removed dummy output APK directory: {OUTPUT_APKS_DIR}")