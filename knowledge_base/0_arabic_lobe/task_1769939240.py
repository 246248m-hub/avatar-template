import os
import shutil
import subprocess
from pathlib import Path

# --- Configuration ---
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
OUTPUT_APKS_DIR = Path("./output_apks")
GRADLE_WRAPPER_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "gradlew"
MAIN_ACTIVITY_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myapp" / "MainActivity.java"
MAIN_ACTIVITY_TEMPLATE = """
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists
        TextView textView = findViewById(R.id.textView); // Assuming a TextView with id 'textView' exists
        textView.setText("{generated_text}");
    }
}
"""

# --- Helper Functions ---

def create_directory_if_not_exists(dir_path: Path):
    """Creates a directory if it doesn't exist."""
    dir_path.mkdir(parents=True, exist_ok=True)

def copy_android_project_template(source_template_dir: Path, destination_dir: Path):
    """Copies the Android project template to a new location."""
    if not source_template_dir.exists():
        raise FileNotFoundError(f"Android project template not found at: {source_template_dir}")
    shutil.copytree(source_template_dir, destination_dir)
    print(f"Copied Android project template to: {destination_dir}")

def modify_main_activity(activity_path: Path, generated_text: str):
    """Modifies the MainActivity.java file to display generated text."""
    if not activity_path.exists():
        raise FileNotFoundError(f"MainActivity.java not found at: {activity_path}")

    with open(activity_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace placeholder with actual generated text
    # Note: This is a simplified approach. A more robust solution would involve parsing Java code.
    # For this demo, we'll assume a direct string replacement.
    modified_content = content.replace("{generated_text}", generated_text.replace('"', '\\"'))

    with open(activity_path, "w", encoding="utf-8") as f:
        f.write(modified_content)
    print(f"Modified MainActivity.java to display: '{generated_text[:50]}...'")

def run_gradle_build(gradle_wrapper: Path, output_dir: Path) -> bool:
    """Runs the Gradle build command to compile the APK."""
    if not gradle_wrapper.exists():
        raise FileNotFoundError(f"Gradle wrapper not found at: {gradle_wrapper}")

    # Ensure output directory exists for the build process
    output_dir.mkdir(parents=True, exist_ok=True)

    # Command to build the release APK
    # This assumes your build.gradle is configured to produce an APK in build/outputs/apk/
    command = [
        str(gradle_wrapper),
        "assembleRelease",
        f"-Pandroid.injected.signing.store.file={Path('./release.keystore')}", # Placeholder for keystore
        f"-Pandroid.injected.signing.store.password={os.environ.get('KEYSTORE_PASSWORD', 'password')}",
        f"-Pandroid.injected.signing.key.alias={os.environ.get('KEY_ALIAS', 'keyalias')}",
        f"-Pandroid.injected.signing.key.password={os.environ.get('KEY_PASSWORD', 'password')}",
        f"-Pandroid.build.output.dir={output_dir}"
    ]
    print(f"Running Gradle command: {' '.join(command)}")

    try:
        # Capture stdout and stderr to prevent blocking issues with large outputs
        process = subprocess.Popen(command, cwd=str(output_dir.parent), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        print("Gradle build stdout:")
        print(stdout)
        print("Gradle build stderr:")
        print(stderr)

        if process.returncode == 0:
            print("Gradle build successful.")
            return True
        else:
            print(f"Gradle build failed with return code: {process.returncode}")
            return False
    except Exception as e:
        print(f"An error occurred during Gradle build: {e}")
        return False

def find_generated_apk(output_dir: Path) -> Path | None:
    """Finds the generated APK file in the output directory."""
    # Assuming the APK name follows a pattern like app-release.apk
    for apk_file in output_dir.glob("*.apk"):
        if "release" in apk_file.name:
            return apk_file
    return None

def build_apk_from_text(arabic_text: str, output_apk_path: Path):
    """
    Orchestrates the process of building an APK from provided Arabic text.
    This function acts as the core logic for the APK compiler.
    """
    print("\n--- Initiating APK Compilation Process ---")

    # 1. Prepare the Android project environment
    create_directory_if_not_exists(ANDROID_PROJECT_TEMPLATE_DIR)
    create_directory_if_not_exists(OUTPUT_APKS_DIR)

    # In a real scenario, you'd have a robust template project.
    # For this demo, we'll simulate a basic template.
    # Assume 'android_project_template' contains a minimal Android project structure.
    # For demonstration purposes, let's create a dummy structure if it doesn't exist.
    if not (ANDROID_PROJECT_TEMPLATE_DIR / "build.gradle").exists():
        print("Creating a dummy Android project template for demonstration...")
        create_directory_if_not_exists(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myapp")
        create_directory_if_not_exists(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout")
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "build.gradle", "w") as f:
            f.write("plugins { id 'com.android.application' }\nandroid { compileSdk 33 }\n")
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle", "w") as f:
            f.write("plugins { id 'com.android.application' }\nandroid { compileSdk 33 }\n")
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml", "w") as f:
            f.write("<manifest package='com.example.myapp'><application><activity android:name='.MainActivity' android:exported='true'><intent-filter><action android:name='android.intent.action.MAIN'/><category android:name='android.intent.category.LAUNCHER'/></intent-filter></activity></application></manifest>")
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml", "w") as f:
            f.write("<androidx.constraintlayout.widget.ConstraintLayout xmlns:android='http://schemas.android.com/apk/res/android'><TextView android:id='@+id/textView' android:layout_width='wrap_content' android:layout_height='wrap_content' /></androidx.constraintlayout.widget.ConstraintLayout>")
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "gradlew", "w") as f: # Dummy gradlew, actual one needed for build
            f.write("#!/bin/bash\nexec ./gradle/wrapper/gradlew \"$@\"\n")
        os.chmod(ANDROID_PROJECT_TEMPLATE_DIR / "gradlew", 0o755)


    # Copy the template to a working directory
    working_project_dir = ANDROID_PROJECT_TEMPLATE_DIR # Use template dir directly for simplicity in this demo
    # In a real scenario, you'd copy to a unique temp dir:
    # working_project_dir = Path(f"./temp_project_{os.getpid()}")
    # copy_android_project_template(ANDROID_PROJECT_TEMPLATE_DIR, working_project_dir)

    # 2. Inject the generated Arabic text into the MainActivity
    # This requires a way to dynamically generate Java code.
    # For this demo, we'll assume `MAIN_ACTIVITY_PATH` is the target and can be modified.
    # In a more advanced system, this would involve AST manipulation or code generation.

    # Let's simulate getting the text for the app. This text would typically
    # come from Lobe 0 (Language Lobe) after processing a prompt.
    # For now, we use the input `arabic_text`.

    # We need a placeholder to inject the text into.
    # Let's assume the template has a structure that allows this.
    # If the template doesn't exist, we create a basic one.
    if not MAIN_ACTIVITY_PATH.exists():
        print(f"Creating dummy MainActivity at {MAIN_ACTIVITY_PATH}")
        create_directory_if_not_exists(MAIN_ACTIVITY_PATH.parent)
        with open(MAIN_ACTIVITY_PATH, "w", encoding="utf-8") as f:
            f.write(MAIN_ACTIVITY_TEMPLATE.format(generated_text="Welcome!"))

    # Modify the MainActivity to include the Arabic text.
    # This requires careful escaping and handling of Arabic characters in Java strings.
    try:
        modify_main_activity(MAIN_ACTIVITY_PATH, arabic_text)
    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure the Android project template is correctly set up.")
        return

    # 3. Compile the APK using Gradle
    gradle_wrapper_path = working_project_dir / "gradlew"
    if not gradle_wrapper_path.exists():
        print("Error: gradlew not found. Please ensure your Android project template includes it.")
        return

    # Ensure Gradle wrapper is executable
    os.chmod(gradle_wrapper_path, 0o755)

    if not run_gradle_build(gradle_wrapper_path, OUTPUT_APKS_DIR):
        print("APK compilation failed.")
        return

    # 4. Locate and rename the generated APK
    generated_apk = find_generated_apk(OUTPUT_APKS_DIR / "app" / "build" / "outputs" / "apk" / "release")
    if generated_apk:
        shutil.move(generated_apk, output_apk_path)
        print(f"Successfully built and moved APK to: {output_apk_path}")
    else:
        print("Could not find the generated APK in the expected output directory.")
        print(f"Looked in: {OUTPUT_APKS_DIR / 'app' / 'build' / 'outputs' / 'apk' / 'release'}")


    # --- Cleanup (optional, but good practice) ---
    # In a real application, you might want to clean up the working project directory.
    # For this example, we'll leave it for inspection if needed.
    # if working_project_dir != ANDROID_PROJECT_TEMPLATE_DIR and working_project_dir.exists():
    #     shutil.rmtree(working_project_dir)
    #     print(f"Cleaned up temporary project directory: {working_project_dir}")

    print("\n--- APK Compilation Process Finished ---")

if __name__ == '__main__':
    # --- Demo Usage ---
    # This section is for demonstrating the function.
    # In the grand objective, this function would be called by other lobes.

    # Ensure necessary directories exist
    create_directory_if_not_exists(KNOWLEDGE_BASE_DIR)
    create_directory_if_not_exists(OUTPUT_APKS_DIR)

    # Dummy Arabic text to be embedded in the APK
    dummy_arabic_text = "مرحباً بالعالم! هذا تطبيق Android تم إنشاؤه بواسطة الذكاء الاصطناعي."
    output_apk_filename = OUTPUT_APKS_DIR / "unified_mind_app.apk"

    # Execute the APK build function
    build_apk_from_text(dummy_arabic_text, output_apk_filename)

    # --- Cleanup dummy files created during demo ---
    print("\n--- Cleaning up dummy files and directories ---")
    if ANDROID_PROJECT_TEMPLATE_DIR.exists():
        # Careful with this in a real setup if it's a shared template
        # For this demo, we created a dummy structure inside it.
        # shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        # print(f"Removed dummy Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        pass # Keep template for potential re-runs in demo

    if OUTPUT_APKS_DIR.exists():
        # Keep the generated APK for inspection
        # shutil.rmtree(OUTPUT_APKS_DIR)
        # print(f"Removed dummy output APK directory: {OUTPUT_APKS_DIR}")
        pass

    print("\n--- APK Compiler Module Demo Finished ---")