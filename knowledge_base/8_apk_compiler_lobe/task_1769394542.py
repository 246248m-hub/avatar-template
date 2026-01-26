import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Constants ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
JAVA_PROJECT_DIR = os.path.join(PROJECT_ROOT, "android_project")
GRADLE_WRAPPER_PATH = os.path.join(JAVA_PROJECT_DIR, "gradlew")
BUILD_TASK = "assembleDebug" # or "assembleRelease" for release builds

# --- Lobe Dependencies (Conceptual) ---
# This lobe would ideally receive the generated Java/Kotlin code from Lobe 4_code_generation_lobe
# and potentially configuration details from other lobes.
# For this implementation, we'll simulate receiving the code structure.

class Lobe10ApkBuilderLobe:
    """
    Lobe 10: APK Builder Lobe
    Responsible for compiling the Android project into an APK.
    It interacts with the Android build system (Gradle).
    """

    def __init__(self, java_project_path: str = JAVA_PROJECT_DIR, gradle_wrapper: str = GRADLE_WRAPPER_PATH):
        """
        Initializes the APK Builder Lobe.

        Args:
            java_project_path (str): The root directory of the Android Java/Kotlin project.
            gradle_wrapper (str): The path to the Gradle wrapper executable.
        """
        self.java_project_path = java_project_path
        self.gradle_wrapper = gradle_wrapper
        self.output_apk_dir = os.path.join(self.java_project_path, "app", "build", "outputs", "apk", "debug")
        self.build_successful = False

        if not os.path.exists(self.gradle_wrapper):
            logging.error(f"Gradle wrapper not found at: {self.gradle_wrapper}. Please ensure the Android project is set up correctly.")
            raise FileNotFoundError(f"Gradle wrapper not found at: {self.gradle_wrapper}")

        if not os.path.exists(self.java_project_path):
            logging.error(f"Android project directory not found at: {self.java_project_path}. Please ensure the project is generated or exists.")
            raise FileNotFoundError(f"Android project directory not found at: {self.java_project_path}")

    def _run_gradle_command(self, command: str) -> bool:
        """
        Executes a Gradle command in the specified project directory.

        Args:
            command (str): The Gradle command to execute (e.g., 'assembleDebug').

        Returns:
            bool: True if the command executed successfully, False otherwise.
        """
        logging.info(f"Running Gradle command: {command}")
        try:
            # Use subprocess.run for better control and error handling
            process = subprocess.run(
                [self.gradle_wrapper, command],
                cwd=self.java_project_path,
                capture_output=True,
                text=True,
                check=True  # Raise CalledProcessError if return code is non-zero
            )
            logging.info("Gradle build output:\n" + process.stdout)
            if process.stderr:
                logging.warning("Gradle build error output:\n" + process.stderr)
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Gradle command '{command}' failed with return code {e.returncode}")
            logging.error("Error output:\n" + e.stderr)
            logging.error("Standard output:\n" + e.stdout)
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during Gradle execution: {e}")
            return False

    def compile_apk(self, build_type: str = BUILD_TASK) -> str | None:
        """
        Initiates the APK compilation process using Gradle.

        Args:
            build_type (str): The Gradle build task to execute (e.g., 'assembleDebug').

        Returns:
            str | None: The path to the generated APK file if successful, otherwise None.
        """
        logging.info("--- Initiating APK compilation process ---")
        self.build_successful = self._run_gradle_command(build_type)

        if self.build_successful:
            logging.info("APK compilation successful.")
            apk_file_path = self._find_generated_apk()
            if apk_file_path:
                logging.info(f"APK generated successfully at: {apk_file_path}")
                return apk_file_path
            else:
                logging.error("APK compilation reported success, but no APK file was found.")
                return None
        else:
            logging.error("APK compilation failed.")
            return None

    def _find_generated_apk(self) -> str | None:
        """
        Locates the most recently generated APK file in the output directory.

        Returns:
            str | None: The path to the APK file, or None if not found.
        """
        if not os.path.exists(self.output_apk_dir):
            logging.warning(f"APK output directory not found: {self.output_apk_dir}")
            return None

        apk_files = [
            os.path.join(self.output_apk_dir, f)
            for f in os.listdir(self.output_apk_dir)
            if f.endswith(".apk")
        ]

        if not apk_files:
            logging.warning(f"No APK files found in: {self.output_apk_dir}")
            return None

        # Return the most recently modified APK
        apk_files.sort(key=os.path.getmtime, reverse=True)
        return apk_files[0]

    def __str__(self) -> str:
        return "Lobe10ApkBuilderLobe"

# --- Example Usage (for demonstration purposes) ---
if __name__ == "__main__":
    # This block would be executed when running this script directly.
    # In a real scenario, Lobe 8_apk_compiler_lobe would be calling this.

    logging.info("--- Running Lobe 10_apk_builder_lobe demo ---")

    # IMPORTANT: For this demo to work, you need a valid Android project
    # at the specified JAVA_PROJECT_DIR. This includes a gradlew executable.
    # In a real integration, Lobe 4_code_generation_lobe would have
    # created this project structure.

    # --- Mocking the existence of the Android project structure ---
    # In a real scenario, this would be handled by Lobe 4_code_generation_lobe.
    # For testing purposes, we'll create dummy directories and a dummy gradlew.
    os.makedirs(JAVA_PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(JAVA_PROJECT_DIR, "app", "build", "outputs", "apk", "debug"), exist_ok=True)
    dummy_gradlew_path = GRADLE_WRAPPER_PATH
    if not os.path.exists(dummy_gradlew_path):
        logging.warning(f"Creating dummy gradlew for demo at: {dummy_gradlew_path}")
        with open(dummy_gradlew_path, "w") as f:
            f.write("#!/bin/bash\necho 'Simulating Gradle build...'\nexit 0\n") # Dummy script that exits successfully
        os.chmod(dummy_gradlew_path, 0o755) # Make it executable


    try:
        apk_builder = Lobe10ApkBuilderLobe()
        # In a real scenario, you'd pass the build_type if needed.
        # Here we use the default 'assembleDebug'.
        generated_apk_path = apk_builder.compile_apk()

        if generated_apk_path:
            print(f"\n--- Lobe 10_apk_builder_lobe successfully generated APK: {generated_apk_path} ---")
            # This path would then be passed to Lobe 11_apk_deployment_lobe
        else:
            print("\n--- Lobe 10_apk_builder_lobe failed to generate APK. ---")

    except FileNotFoundError as e:
        logging.error(f"Demo setup failed: {e}. Please ensure the Android project is correctly configured.")
        print(f"\n--- Lobe 10_apk_builder_lobe demo encountered setup error: {e} ---")
    except Exception as e:
        logging.error(f"An unexpected error occurred during the demo: {e}")
        print(f"\n--- Lobe 10_apk_builder_lobe demo encountered an unexpected error: {e} ---")

    print("\n--- Lobe 10_apk_builder_lobe Demo Finished ---")

    # Clean up dummy files if created for demo
    if os.path.exists(dummy_gradlew_path) and "Simulating Gradle build..." in open(dummy_gradlew_path).read():
        os.remove(dummy_gradlew_path)
        logging.info("Cleaned up dummy gradlew.")
    if os.path.exists(os.path.join(JAVA_PROJECT_DIR, "app", "build")):
        import shutil
        shutil.rmtree(os.path.join(JAVA_PROJECT_DIR, "app", "build"))
        logging.info("Cleaned up dummy build directory.")