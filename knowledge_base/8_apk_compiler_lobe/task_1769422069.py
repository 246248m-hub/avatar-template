import os
import shutil
import logging
import subprocess

# --- Configuration ---
JAVA_PROJECT_DIR = "generated_apk_project"
GRADLE_WRAPPER_SCRIPT = "gradlew"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions ---
def create_directory_if_not_exists(path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def cleanup_generated_project():
    """Cleans up the generated APK project directory."""
    if os.path.exists(JAVA_PROJECT_DIR):
        logging.info(f"Cleaning up existing project directory: {JAVA_PROJECT_DIR}")
        shutil.rmtree(JAVA_PROJECT_DIR)
        logging.info("Project directory cleaned up.")

def copy_project_template(source_dir, dest_dir):
    """Copies a project template to the destination directory."""
    if not os.path.exists(source_dir):
        logging.error(f"Project template source directory not found: {source_dir}")
        return False
    try:
        shutil.copytree(source_dir, dest_dir)
        logging.info(f"Copied project template from {source_dir} to {dest_dir}")
        return True
    except Exception as e:
        logging.error(f"Error copying project template: {e}")
        return False

def run_gradle_command(command):
    """Runs a Gradle command in the project directory."""
    gradlew_path = os.path.join(JAVA_PROJECT_DIR, GRADLE_WRAPPER_SCRIPT)
    if not os.path.exists(gradlew_path):
        logging.error(f"Gradle wrapper script not found at {gradlew_path}")
        return False

    try:
        # Ensure gradlew is executable
        os.chmod(gradlew_path, 0o755)
        logging.info(f"Executing Gradle command: {command} in {JAVA_PROJECT_DIR}")
        result = subprocess.run([f"./{GRADLE_WRAPPER_SCRIPT}", command], cwd=JAVA_PROJECT_DIR, capture_output=True, text=True, check=True)
        logging.info(f"Gradle command output:\n{result.stdout}")
        if result.stderr:
            logging.warning(f"Gradle command stderr:\n{result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Gradle command failed: {command}")
        logging.error(f"Error output:\n{e.stderr}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while running Gradle: {e}")
        return False

# --- Lobe 8: APK Compiler Lobe ---
class ApkCompilerLobe:
    """
    Lobe responsible for compiling generated code into a hyper-efficient APK.
    This lobe assumes that Lobe 4 (Code Generation) has produced valid Android project structure
    and Lobe 6 (Synthesis) has orchestrated the process.
    """
    def __init__(self, project_template_path="android_project_template"):
        """
        Initializes the ApkCompilerLobe.

        Args:
            project_template_path (str): Path to a directory containing a basic Android project structure
                                         (e.g., with build.gradle, settings.gradle, app module).
                                         This serves as a template to be populated by Lobe 4.
        """
        self.project_template_path = project_template_path
        logging.info(f"APK Compiler Lobe initialized with template: {self.project_template_path}")

    def compile_apk(self, generated_code_dir):
        """
        Compiles the generated Android project into an APK.

        This method performs the following steps:
        1. Cleans up any previous APK compilation artifacts.
        2. Copies a basic Android project template.
        3. Integrates the generated code into the project structure (this part
           is highly dependent on Lobe 4's output and would involve modifying
           build files, source code, and resource files). For this example,
           we'll assume Lobe 4 has already placed files in the correct structure
           within `generated_code_dir` which will be copied over.
        4. Executes the Gradle wrapper to build the APK.

        Args:
            generated_code_dir (str): The directory containing the generated Android project files
                                      (e.g., Java/Kotlin sources, AndroidManifest.xml, res files).

        Returns:
            bool: True if the APK compilation was successful, False otherwise.
        """
        logging.info("--- Initiating APK Compilation ---")
        cleanup_generated_project()
        create_directory_if_not_exists(JAVA_PROJECT_DIR)

        # 1. Copy Project Template
        if not copy_project_template(self.project_template_path, JAVA_PROJECT_DIR):
            logging.error("Failed to copy project template. Aborting compilation.")
            return False

        # 2. Integrate Generated Code (Simplified)
        # In a real scenario, Lobe 4 would have already placed files in a structure
        # that is compatible with the template, or this step would involve more
        # sophisticated file merging and build script modification.
        # For this example, we assume `generated_code_dir` *is* the final project structure
        # and we've already copied it over. If `generated_code_dir` contained specific modules
        # to be merged, more complex logic would go here.
        logging.info(f"Assuming generated code from '{generated_code_dir}' is already placed correctly within '{JAVA_PROJECT_DIR}'.")
        # A more robust integration might look like:
        # shutil.copytree(os.path.join(generated_code_dir, "app"), os.path.join(JAVA_PROJECT_DIR, "app"), dirs_exist_ok=True)
        # shutil.copy2(os.path.join(generated_code_dir, "build.gradle"), JAVA_PROJECT_DIR)
        # etc.

        # 3. Run Gradle to build the APK
        # We will build a release APK. For debug, use 'assembleDebug'.
        if run_gradle_command("assembleRelease"):
            logging.info("APK compilation successful.")
            # The APK will be located in JAVA_PROJECT_DIR/app/build/outputs/apk/release/
            apk_path = os.path.join(JAVA_PROJECT_DIR, "app", "build", "outputs", "apk", "release")
            apk_files = [f for f in os.listdir(apk_path) if f.endswith(".apk")]
            if apk_files:
                logging.info(f"Generated APKs found: {[os.path.join(apk_path, f) for f in apk_files]}")
                # Move the first found APK to the root of the project for easier access
                final_apk_name = f"generated_app_{os.path.basename(generated_code_dir)}.apk"
                try:
                    shutil.move(os.path.join(apk_path, apk_files[0]), os.path.join(JAVA_PROJECT_DIR, final_apk_name))
                    logging.info(f"Primary APK moved to: {os.path.join(JAVA_PROJECT_DIR, final_apk_name)}")
                except Exception as e:
                    logging.warning(f"Could not move primary APK: {e}")
            return True
        else:
            logging.error("APK compilation failed.")
            return False

    def __str__(self):
        return "Lobe 8: APK Compiler Lobe"

# --- Example Usage (for demonstration purposes, would be called by Lobe 6) ---
if __name__ == "__main__":
    # This block simulates how Lobe 6 might use Lobe 8.
    # In a real execution, `generated_android_project` would be the output
    # of Lobe 4, structured correctly.
    logging.info("--- Simulating Lobe 8 Execution ---")

    # Create a dummy Android project template for testing
    DUMMY_TEMPLATE_DIR = "dummy_android_template"
    if not os.path.exists(DUMMY_TEMPLATE_DIR):
        os.makedirs(DUMMY_TEMPLATE_DIR)
    with open(os.path.join(DUMMY_TEMPLATE_DIR, "build.gradle"), "w") as f:
        f.write("// Dummy build.gradle\n")
    with open(os.path.join(DUMMY_TEMPLATE_DIR, "settings.gradle"), "w") as f:
        f.write("// Dummy settings.gradle\n")
    app_dir = os.path.join(DUMMY_TEMPLATE_DIR, "app")
    os.makedirs(os.path.join(app_dir, "src", "main", "java", "com", "example", "myapp"))
    with open(os.path.join(app_dir, "src", "main", "java", "com", "example", "myapp", "MainActivity.java"), "w") as f:
        f.write("""
package com.example.myapp;
import android.app.Activity;
import android.os.Bundle;
public class MainActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming R.layout.activity_main exists
    }
}
        """)
    os.makedirs(os.path.join(app_dir, "src", "main", "res", "layout"))
    with open(os.path.join(app_dir, "src", "main", "res", "layout", "activity_main.xml"), "w") as f:
        f.write("""
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello, World!" />
</LinearLayout>
        """)
    os.makedirs(os.path.join(app_dir, "src", "main"))
    with open(os.path.join(app_dir, "src", "main", "AndroidManifest.xml"), "w") as f:
        f.write("""
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.myapp">
    <application android:label="@string/app_name">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
        """)
    # Create a dummy gradlew script (Linux/macOS)
    with open(os.path.join(DUMMY_TEMPLATE_DIR, "gradlew"), "w") as f:
        f.write("""#!/bin/bash
# Dummy gradlew script for demonstration
# In a real project, this would be the actual Gradle wrapper script.
# For this demo, we'll just try to execute a gradle command.
# Note: This requires a Java Development Kit (JDK) and Gradle to be installed on the system.
if [ -z "$JAVA_HOME" ]; then
  echo "JAVA_HOME is not set. Please set it to your JDK installation path."
  exit 1
fi
GRADLE_EXEC="$JAVA_HOME/bin/java -Dorg.gradle.appname=gradlew -cp \"$(dirname $0)/gradle/wrapper/gradle-wrapper.jar\" org.gradle.wrapper.GradleWrapperMain \"$@\""
eval $GRADLE_EXEC
""")
    os.chmod(os.path.join(DUMMY_TEMPLATE_DIR, "gradlew"), 0o755)


    # Create a dummy generated code directory that matches the template structure for simplicity
    dummy_generated_code_dir = "dummy_generated_code"
    shutil.copytree(DUMMY_TEMPLATE_DIR, dummy_generated_code_dir)
    # NOTE: In a real scenario, Lobe 4 would produce code that goes *into* the template,
    # or Lobe 8 would have logic to merge/modify the template based on Lobe 4's output.
    # For this simulation, we copy the template itself as "generated code".

    apk_compiler = ApkCompilerLobe(project_template_path=DUMMY_TEMPLATE_DIR)
    compile_success = apk_compiler.compile_apk(generated_code_dir=dummy_generated_code_dir)

    if compile_success:
        logging.info("APK compilation simulation completed successfully.")
    else:
        logging.error("APK compilation simulation failed.")

    # --- Clean up dummy files ---
    print("\n--- Cleaning up dummy APK compiler test files ---")
    if os.path.exists(DUMMY_TEMPLATE_DIR):
        shutil.rmtree(DUMMY_TEMPLATE_DIR)
        print(f"Removed dummy template directory: {DUMMY_TEMPLATE_DIR}")
    if os.path.exists(dummy_generated_code_dir):
        shutil.rmtree(dummy_generated_code_dir)
        print(f"Removed dummy generated code directory: {dummy_generated_code_dir}")
    if os.path.exists(JAVA_PROJECT_DIR):
        shutil.rmtree(JAVA_PROJECT_DIR)
        print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")

    print("\n--- APK Compiler Lobe Demo Finished ---")