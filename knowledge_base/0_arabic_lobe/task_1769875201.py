import os
import json
import shutil
from pathlib import Path

# --- Constants ---
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
DEMO_APK_BUILD_DIR = Path("demo_apk_build")
DEMO_ANDROID_PROJECT_DIR = DEMO_APK_BUILD_DIR / "my_android_project"

# --- Helper Functions ---
def ensure_directory_exists(dir_path: Path):
    """Ensures that a directory exists, creating it if it doesn't."""
    dir_path.mkdir(parents=True, exist_ok=True)

def cleanup_demo_directories():
    """Cleans up dummy directories used for demonstrations."""
    if DEMO_APK_BUILD_DIR.exists():
        shutil.rmtree(DEMO_APK_BUILD_DIR)
        print(f"Cleaned up demo directory: {DEMO_APK_BUILD_DIR}")

def load_apk_manifest_template(template_path: Path) -> dict:
    """Loads a JSON manifest template."""
    if not template_path.exists():
        raise FileNotFoundError(f"Manifest template not found at: {template_path}")
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_apk_manifest(manifest_data: dict, output_path: Path):
    """Saves the generated APK manifest."""
    ensure_directory_exists(output_path.parent)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=4)

def generate_gradle_wrapper_script(project_dir: Path):
    """Generates a dummy gradlew script."""
    gradlew_path = project_dir / "gradlew"
    with open(gradlew_path, "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\n")
        f.write("echo 'Simulating gradlew execution...'\n")
        f.write("exit 0\n")
    os.chmod(gradlew_path, 0o755) # Make it executable

def generate_build_gradle_file(project_dir: Path, app_name: str):
    """Generates a dummy build.gradle file."""
    build_gradle_path = project_dir / "build.gradle"
    with open(build_gradle_path, "w", encoding="utf-8") as f:
        f.write(f"android {{\n")
        f.write(f"    compileSdkVersion 33\n")
        f.write(f"    defaultConfig {{\n")
        f.write(f"        applicationId 'com.example.{app_name.lower()}'\n")
        f.write(f"        minSdkVersion 21\n")
        f.write(f"        targetSdkVersion 33\n")
        f.write(f"        versionCode 1\n")
        f.write(f"        versionName '1.0'\n")
        f.write(f"    }}\n")
        f.write(f"}}\n")
        f.write(f"dependencies {{\n")
        f.write(f"    implementation 'androidx.appcompat:appcompat:1.6.1'\n")
        f.write(f"}}\n")

# --- Lobe Function ---
def build_apk_structure(app_name: str, manifest_data: dict, output_dir: Path) -> Path:
    """
    Builds the foundational structure for an Android project to facilitate APK compilation.

    This function creates a dummy Android project directory with essential files like
    AndroidManifest.xml, build.gradle, and gradlew, which are required for a basic
    APK build process.

    Args:
        app_name (str): The name of the application, used for package naming and directory structures.
        manifest_data (dict): The parsed AndroidManifest.xml content.
        output_dir (Path): The root directory where the dummy Android project will be created.

    Returns:
        Path: The path to the created Android project directory.
    """
    print(f"\n--- Initiating APK Structure Builder for app: '{app_name}' ---")

    # Define project paths
    project_root = output_dir / app_name.lower().replace(" ", "_")
    app_module_dir = project_root / "app"
    manifest_file_path = app_module_dir / "src" / "main" / "AndroidManifest.xml"

    # Clean up any previous runs
    if project_root.exists():
        shutil.rmtree(project_root)
        print(f"Cleaned up existing project directory: {project_root}")

    # Ensure directories are created
    ensure_directory_exists(app_module_dir / "src" / "main")
    ensure_directory_exists(project_root)

    # Save the AndroidManifest.xml
    save_apk_manifest(manifest_data, manifest_file_path)
    print(f"Saved AndroidManifest.xml to: {manifest_file_path}")

    # Generate dummy build.gradle and gradlew script
    generate_build_gradle_file(project_root, app_name)
    print(f"Generated build.gradle to: {project_root / 'build.gradle'}")
    generate_gradle_wrapper_script(project_root)
    print(f"Generated gradlew script to: {project_root / 'gradlew'}")

    print(f"\n--- APK Structure Builder Finished. Project created at: {project_root} ---")
    return project_root

# --- Lobe 8: APK Compiler Lobe Logic ---
# This lobe's responsibility is to prepare the project structure that the actual
# APK compiler (Lobe 9) will use. It doesn't perform the compilation itself.

# Example Usage (for demonstration purposes within this lobe's scope)
if __name__ == "__main__":
    print("\n--- Lobe 8_apk_compiler_lobe Demonstration ---")
    cleanup_demo_directories() # Ensure a clean start

    # --- Mocking Lobe 0 and Lobe 4 outputs ---
    # Simulate a manifest generated from Arabic text
    mock_manifest_data = {
        "manifest": {
            "package": "com.example.arabicapp",
            "versionCode": 1,
            "versionName": "1.0",
            "application": {
                "label": "@string/app_name",
                "icon": "@mipmap/ic_launcher",
                "usesPermissions": [
                    {"name": "android.permission.INTERNET"}
                ]
            },
            "activity": [
                {
                    "name": ".MainActivity",
                    "intentFilter": {
                        "action": [{"name": "android.intent.action.MAIN"}],
                        "category": [{"name": "android.intent.category.LAUNCHER"}]
                    }
                }
            ]
        }
    }

    # Simulate the creation of an Android project structure
    generated_project_path = build_apk_structure(
        app_name="My Arabic App",
        manifest_data=mock_manifest_data,
        output_dir=DEMO_APK_BUILD_DIR
    )

    # Simulating the output of this lobe which is the path to the project root
    # This path would be passed to the next lobe (APK Compiler)
    print(f"\nSuccessfully prepared Android project structure. Project path: {generated_project_path}")

    print("\n--- APK Structure Builder Module Demonstration Finished ---")

    # --- Clean up dummy files ---
    print("\n--- Cleaning up dummy files ---")
    cleanup_demo_directories()