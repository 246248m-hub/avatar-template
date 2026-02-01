import os
import shutil
import re

# Assume these directories are defined elsewhere and accessible
OUTPUT_APKS_DIR = "generated_apks"
KNOWLEDGE_BASE_DIR = "knowledge_base"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"

def initialize_output_directory(dir_path):
    """Ensures the output directory exists and is clean."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print(f"Cleaned up existing contents of: {dir_path}")
    print(f"Ensured output directory exists: {dir_path}")

def generate_android_project_structure(project_name, base_dir):
    """
    Copies a base Android project template and renames it to the specified project name.
    This simulates the creation of a new Android project for compilation.
    """
    if not os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        raise FileNotFoundError(f"Android project template directory not found: {ANDROID_PROJECT_TEMPLATE_DIR}")

    project_path = os.path.join(base_dir, project_name)
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        print(f"Removed existing project directory: {project_path}")

    shutil.copytree(ANDROID_PROJECT_TEMPLATE_DIR, project_path)
    print(f"Created new Android project structure at: {project_path}")

    # Basic modification: Update package name in AndroidManifest.xml
    manifest_path = os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml")
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest_content = f.read()
        # This is a simplification; a real parser would be more robust
        new_package_name = f"com.example.{project_name.lower()}"
        manifest_content = re.sub(r'package="[^"]+"', f'package="{new_package_name}"', manifest_content, count=1)
        with open(manifest_path, 'w') as f:
            f.write(manifest_content)
        print(f"Updated package name in {manifest_path} to {new_package_name}")
    else:
        print(f"Warning: AndroidManifest.xml not found at {manifest_path}. Package name not updated.")

    return project_path

def compile_apk_from_project(project_path, output_apk_dir):
    """
    Simulates the compilation of an Android project into an APK.
    In a real scenario, this would involve calling Android build tools (e.g., Gradle).
    For this example, it will create a dummy APK file.
    """
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Project directory not found: {project_path}")

    initialize_output_directory(output_apk_dir)

    project_name = os.path.basename(project_path)
    dummy_apk_filename = f"{project_name}.apk"
    output_apk_file_path = os.path.join(output_apk_dir, dummy_apk_filename)

    # Simulate APK creation by creating a dummy file
    try:
        with open(output_apk_file_path, 'wb') as f:
            f.write(b'\x50\x4b\x03\x04')  # Simple ZIP magic bytes to mimic an APK
        print(f"Created dummy APK file: {output_apk_file_path}")
    except IOError as e:
        print(f"Error creating dummy APK file: {e}")
        raise

    return output_apk_file_path

class ApkGenerationLobe:
    """
    This lobe focuses on the final stages of APK generation,
    taking a structured project and compiling it.
    It integrates with the project structure creation and simulated compilation.
    """
    def __init__(self, output_dir=OUTPUT_APKS_DIR, template_dir=ANDROID_PROJECT_TEMPLATE_DIR):
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.project_path = None
        self.generated_apk_path = None

    def create_and_compile(self, project_name_from_nlp):
        """
        Orchestrates the creation of an Android project structure from a template
        and then simulates the compilation of that project into an APK.
        """
        print(f"\n--- Initiating APK Generation for: {project_name_from_nlp} ---")

        try:
            # Step 1: Create a project structure from a template
            print(f"Generating Android project structure for '{project_name_from_nlp}'...")
            self.project_path = generate_android_project_structure(
                project_name_from_nlp,
                base_dir=os.path.join(self.output_dir, "projects") # Keep projects separate from final APKs
            )

            # Step 2: Compile the generated project into an APK
            print(f"Compiling project '{project_name_from_nlp}' into an APK...")
            self.generated_apk_path = compile_apk_from_project(
                self.project_path,
                self.output_dir
            )

            print(f"\n--- APK Generation Complete ---")
            print(f"Project created at: {self.project_path}")
            print(f"APK generated at: {self.generated_apk_path}")
            return self.generated_apk_path

        except FileNotFoundError as e:
            print(f"Error in APK generation: {e}")
            # Handle or re-raise as appropriate
            return None
        except Exception as e:
            print(f"An unexpected error occurred during APK generation: {e}")
            # Handle or re-raise as appropriate
            return None

    def cleanup_project(self):
        """Cleans up the generated Android project directory."""
        if self.project_path and os.path.exists(self.project_path):
            try:
                shutil.rmtree(self.project_path)
                print(f"Cleaned up project directory: {self.project_path}")
                self.project_path = None
            except OSError as e:
                print(f"Error cleaning up project directory {self.project_path}: {e}")

    def cleanup_output_apk(self):
        """Cleans up the generated APK file."""
        if self.generated_apk_path and os.path.exists(self.generated_apk_path):
            try:
                os.remove(self.generated_apk_path)
                print(f"Cleaned up generated APK: {self.generated_apk_path}")
                self.generated_apk_path = None
            except OSError as e:
                print(f"Error cleaning up APK file {self.generated_apk_path}: {e}")

# Example Usage (for demonstration and testing within this module)
if __name__ == "__main__":
    # This part would typically be called by a higher-level orchestrator lobe.
    # For direct execution, we need dummy directories and files to exist.

    # Create dummy directories if they don't exist for testing
    os.makedirs(OUTPUT_APKS_DIR, exist_ok=True)
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR, exist_ok=True)

    # Create a dummy Android project template structure
    dummy_template_project_path = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, "DummyAppTemplate")
    os.makedirs(os.path.join(dummy_template_project_path, "app", "src", "main"), exist_ok=True)
    with open(os.path.join(dummy_template_project_path, "app", "src", "main", "AndroidManifest.xml"), "w") as f:
        f.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.dummy">\n</manifest>')
    with open(os.path.join(dummy_template_project_path, "build.gradle"), "w") as f:
        f.write("/* Dummy build script */")
    print(f"Created dummy Android project template at: {dummy_template_project_path}")


    print("\n--- Testing ApkGenerationLobe ---")
    apk_generator = ApkGenerationLobe()

    # Simulate receiving a project name from NLP processing
    nlp_generated_project_name = "MyAwesomeApp"

    generated_apk = apk_generator.create_and_compile(nlp_generated_project_name)

    if generated_apk:
        print(f"\nSuccessfully generated APK: {generated_apk}")
    else:
        print("\nAPK generation failed.")

    # --- Test cleanup ---
    print("\n--- Testing Cleanup ---")
    apk_generator.cleanup_project()
    apk_generator.cleanup_output_apk()

    # Final check of output directory
    print(f"\nContents of {OUTPUT_APKS_DIR} after cleanup: {os.listdir(OUTPUT_APKS_DIR)}")

    # Clean up dummy template
    if os.path.exists(dummy_template_project_path):
        shutil.rmtree(dummy_template_project_path)
        print(f"Removed dummy Android project template: {dummy_template_project_path}")
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        print(f"Removed dummy Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
    if os.path.exists(OUTPUT_APKS_DIR):
        shutil.rmtree(OUTPUT_APKS_DIR)
        print(f"Removed dummy output APK directory: {OUTPUT_APKS_DIR}")