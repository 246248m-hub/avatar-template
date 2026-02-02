import os
import subprocess
import shutil
import re

# --- Constants ---
KNOWLEDGE_BASE_DIR = "./knowledge_base"
ANDROID_PROJECT_TEMPLATE_DIR = "./android_project_template"
APP_PACKAGE_NAME_PREFIX = "com.example.generatedapp"
GRADLE_PROPERTIES_FILE = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "gradle.properties")
APP_BUILD_GRADLE_FILE = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "build.gradle")
MAIN_ACTIVITY_JAVA_FILE = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "generatedapp", "MainActivity.java")
MANIFEST_FILE = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "app", "src", "main", "AndroidManifest.xml")

# --- Helper Functions ---

def create_directory_if_not_exists(dir_path):
    """Creates a directory if it doesn't already exist."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

def cleanup_directory(dir_path):
    """Removes a directory and all its contents if it exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"Cleaned up directory: {dir_path}")

def copy_template_project():
    """Copies the Android project template to a working directory."""
    print(f"Copying template project from '{ANDROID_PROJECT_TEMPLATE_DIR}' to './current_android_project'")
    if os.path.exists("./current_android_project"):
        shutil.rmtree("./current_android_project")
    shutil.copytree(ANDROID_PROJECT_TEMPLATE_DIR, "./current_android_project")
    print("Template project copied.")

def update_gradle_properties(app_name="GeneratedApp"):
    """Updates the app name and package name in gradle.properties."""
    app_package_name = f"{APP_PACKAGE_NAME_PREFIX}.{app_name.lower().replace(' ', '')}"
    with open(os.path.join("./current_android_project", "gradle.properties"), "r") as f:
        lines = f.readlines()
    with open(os.path.join("./current_android_project", "gradle.properties"), "w") as f:
        for line in lines:
            if line.startswith("appName="):
                f.write(f"appName={app_name}\n")
            elif line.startswith("packageName="):
                f.write(f"packageName={app_package_name}\n")
            else:
                f.write(line)
    return app_package_name

def update_manifest_package_name(package_name):
    """Updates the package name in the AndroidManifest.xml."""
    manifest_path = os.path.join("./current_android_project", "app", "src", "main", "AndroidManifest.xml")
    with open(manifest_path, "r") as f:
        content = f.read()
    # Use regex to replace the package attribute of the manifest tag
    content = re.sub(r'<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="[^"]+"',
                     f'<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package_name}"',
                     content)
    with open(manifest_path, "w") as f:
        f.write(content)
    print(f"Updated AndroidManifest.xml with package name: {package_name}")

def update_main_activity_package_name(package_name):
    """Updates the package name in MainActivity.java."""
    # Adjust the path based on the actual package name
    java_dir = os.path.join("./current_android_project", "app", "src", "main", "java")
    package_parts = package_name.split('.')
    java_package_path = os.path.join(java_dir, *package_parts)
    main_activity_path = os.path.join(java_package_path, "MainActivity.java")

    if not os.path.exists(main_activity_path):
        # Create nested directories if they don't exist
        os.makedirs(java_package_path, exist_ok=True)
        # Copy a default MainActivity or create a basic one if it doesn't exist
        # For simplicity, we'll assume a template exists and might need adjustment.
        # In a real scenario, you'd likely have a template for each package structure.
        print(f"Warning: MainActivity not found at expected path: {main_activity_path}. Creating a basic one.")
        with open(main_activity_path, "w") as f:
            f.write(f"package {package_name};\n\n")
            f.write("import androidx.appcompat.app.AppCompatActivity;\n")
            f.write("import android.os.Bundle;\n\n")
            f.write("public class MainActivity extends AppCompatActivity {\n\n")
            f.write("    @Override\n")
            f.write("    protected void onCreate(Bundle savedInstanceState) {\n")
            f.write("        super.onCreate(savedInstanceState);\n")
            f.write("        setContentView(R.layout.activity_main);\n")
            f.write("    }\n")
            f.write("}\n")
    else:
        with open(main_activity_path, "r") as f:
            lines = f.readlines()
        with open(main_activity_path, "w") as f:
            for line in lines:
                if line.startswith("package "):
                    f.write(f"package {package_name};\n")
                else:
                    f.write(line)
    print(f"Updated MainActivity.java with package name: {package_name}")


def generate_apk(project_dir="./current_android_project"):
    """Builds the APK for the Android project using Gradle."""
    print(f"\n--- Building APK for project in: {project_dir} ---")
    # Ensure the build.gradle and gradle wrapper are executable
    gradlew_path = os.path.join(project_dir, "gradlew")
    if not os.path.exists(gradlew_path):
        raise FileNotFoundError(f"Gradle wrapper not found at {gradlew_path}")
    os.chmod(gradlew_path, 0o755)

    try:
        # Execute the assembleDebug task
        result = subprocess.run([gradlew_path, "assembleDebug"], cwd=project_dir, capture_output=True, text=True, check=True)
        print("Gradle build output:")
        print(result.stdout)
        print(result.stderr)

        # Find the generated APK
        apk_path = None
        for root, _, files in os.walk(os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = os.path.join(root, file)
                    break
            if apk_path:
                break

        if apk_path:
            print(f"\nSuccessfully generated APK at: {apk_path}")
            return apk_path
        else:
            print("\nAPK file not found after build.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"\nError during APK generation: {e}")
        print("Gradle build error output:")
        print(e.stdout)
        print(e.stderr)
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred during APK generation: {e}")
        return None

def cleanup_android_project_template():
    """Removes the temporary Android project directory."""
    cleanup_directory("./current_android_project")

# --- Lobe 6: Synthesis Lobe (Integration Point) ---

def synthesize_apk_from_nlp(arabic_nlp_output: str, app_name: str = "MyGeneratedApp") -> str:
    """
    Synthesizes an Android application (APK) from natural language Arabic input.

    Args:
        arabic_nlp_output (str): The natural language Arabic description of the app's functionality.
        app_name (str): The desired name for the generated application.

    Returns:
        str: The path to the generated APK file, or an empty string if generation failed.
    """
    print("\n--- Initiating Lobe 6: APK Synthesis from NLP ---")
    print(f"App Name: {app_name}")
    print(f"Arabic NLP Description: {arabic_nlp_output[:100]}...") # Print a snippet

    # 1. Preprocessing and Understanding NLP Output (Simplified)
    # In a real scenario, this would involve parsing the arabic_nlp_output
    # to extract features, UI elements, functionalities, etc.
    # For this demo, we'll use the app_name to derive a package name
    # and assume basic functionality which is handled by the template.
    print("Step 1: Preprocessing and understanding NLP output (simplified).")
    # Basic extraction: look for keywords or patterns if more sophisticated parsing is needed.
    # For now, we rely on app_name to customize.

    # 2. Project Setup and Configuration
    print("Step 2: Setting up and configuring the Android project.")
    copy_template_project()
    generated_package_name = update_gradle_properties(app_name=app_name)
    update_manifest_package_name(generated_package_name)
    update_main_activity_package_name(generated_package_name)
    # Further customization based on arabic_nlp_output would happen here,
    # e.g., modifying layout files, adding dependencies, etc.

    # 3. APK Generation
    print("Step 3: Generating the APK.")
    generated_apk_path = generate_apk()

    # 4. Cleanup
    print("Step 4: Cleaning up the temporary project.")
    cleanup_android_project_template()

    if generated_apk_path:
        print(f"\nAPK successfully synthesized and located at: {generated_apk_path}")
        return generated_apk_path
    else:
        print("\nAPK synthesis failed.")
        return ""

# --- Example Usage ---
if __name__ == "__main__":
    # This section demonstrates how Lobe 6 would be called.
    # The actual Arabic NLP processing would be handled by other lobes (e.g., Lobe 0).

    # Dummy Arabic NLP output (replace with actual output from Lobe 0)
    dummy_arabic_description = "تطبيق لتدوين الملاحظات يدعم اللغة العربية، يسمح بإنشاء وحفظ وتعديل الملاحظات النصية."

    # Simulate calling Lobe 6
    print("\n--- DEMO: Lobe 6 Synthesis Lobe ---")
    apk_path = synthesize_apk_from_nlp(dummy_arabic_description, app_name="Notes App")

    if apk_path:
        print(f"\nDemo finished. APK available at: {apk_path}")
    else:
        print("\nDemo finished with APK generation failure.")

    # Clean up any remaining directories if the demo was interrupted
    cleanup_android_project_template()
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"Knowledge base directory '{KNOWLEDGE_BASE_DIR}' is assumed to be managed by other lobes.")

    print("\n--- Lobe 6 Demo Finished ---")