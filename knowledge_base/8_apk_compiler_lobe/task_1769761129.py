import os
import subprocess
from typing import List, Dict, Any

class ApkCompiler:
    """
    A module responsible for compiling Android APKs from project structures.
    """

    def __init__(self, project_root: str):
        """
        Initializes the ApkCompiler.

        Args:
            project_root: The root directory of the Android project.
        """
        self.project_root = os.path.abspath(project_root)
        self.gradle_wrapper_path = os.path.join(self.project_root, "gradlew")

        if not os.path.exists(self.gradle_wrapper_path):
            raise FileNotFoundError(
                f"Gradle wrapper not found at {self.gradle_wrapper_path}. "
                "Ensure the project is a valid Android project with a gradlew script."
            )
        if not os.access(self.gradle_wrapper_path, os.X_OK):
            os.chmod(self.gradle_wrapper_path, 0o755)

    def _run_gradle_command(self, commands: List[str]) -> subprocess.CompletedProcess:
        """
        Runs a Gradle command within the project context.

        Args:
            commands: A list of Gradle commands and their arguments.

        Returns:
            The completed process object.

        Raises:
            subprocess.CalledProcessError: If the Gradle command fails.
        """
        command = [self.gradle_wrapper_path] + commands
        print(f"Running command: {' '.join(command)}")
        try:
            process = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Gradle stdout:\n{process.stdout}")
            if process.stderr:
                print(f"Gradle stderr:\n{process.stderr}")
            return process
        except subprocess.CalledProcessError as e:
            print(f"Gradle command failed with exit code {e.returncode}")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            raise

    def build_apk(self, build_variant: str = "release") -> str:
        """
        Builds the Android APK for a given build variant.

        Args:
            build_variant: The build variant to build (e.g., 'release', 'debug').

        Returns:
            The path to the generated APK file.

        Raises:
            FileNotFoundError: If the APK file is not found after a successful build.
            subprocess.CalledProcessError: If the Gradle build command fails.
        """
        print(f"\n--- Building APK for variant: {build_variant} ---")
        try:
            self._run_gradle_command(["assemble" if build_variant == "release" else "assembleDebug"])
        except subprocess.CalledProcessError:
            print(f"APK build failed for variant '{build_variant}'.")
            raise

        # Determine the expected APK path
        # This is a common path, but might vary based on project structure or flavor
        apk_dir = os.path.join(self.project_root, "app", "build", "outputs", "apk", build_variant)
        apk_filename = f"app-{build_variant}.apk"
        expected_apk_path = os.path.join(apk_dir, apk_filename)

        if not os.path.exists(expected_apk_path):
            # Attempt to find any APK if the default one isn't found
            found_apk = None
            for root, _, files in os.walk(apk_dir):
                for file in files:
                    if file.endswith(".apk"):
                        found_apk = os.path.join(root, file)
                        break
                if found_apk:
                    break

            if found_apk:
                print(f"Found APK at an alternative path: {found_apk}")
                return found_apk
            else:
                raise FileNotFoundError(f"APK file not found in expected directory: {apk_dir} after build.")

        print(f"APK successfully built at: {expected_apk_path}")
        return expected_apk_path

    def clean_project(self):
        """Cleans the build artifacts of the project."""
        print(f"\n--- Cleaning project: {self.project_root} ---")
        try:
            self._run_gradle_command(["clean"])
            print("Project cleaned.")
        except subprocess.CalledProcessError:
            print("Project cleaning failed.")
            raise

    def check_apk_exists(self, apk_path: str) -> bool:
        """
        Checks if a given APK path exists.

        Args:
            apk_path: The full path to the APK file.

        Returns:
            True if the APK exists, False otherwise.
        """
        print(f"Checking if APK exists at: {apk_path}")
        exists = os.path.exists(apk_path)
        print(f"APK exists: {exists}")
        return exists


# Example Usage (for demonstration purposes, not part of the final module output)
if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario,
    # you would point this to an actual Android project.
    # For testing purposes, we might create a dummy project structure.

    # Create a dummy project structure for demonstration
    dummy_project_root = "dummy_android_project"
    os.makedirs(os.path.join(dummy_project_root, "app", "build", "outputs", "apk", "release"), exist_ok=True)
    os.makedirs(os.path.join(dummy_project_root, "app", "build", "outputs", "apk", "debug"), exist_ok=True)
    # Create a dummy gradlew script (this won't actually run Gradle commands)
    with open(os.path.join(dummy_project_root, "gradlew"), "w") as f:
        f.write("#!/bin/bash\necho 'Simulating Gradle command...'")
    os.chmod(os.path.join(dummy_project_root, "gradlew"), 0o755)

    # Create a dummy APK file
    dummy_apk_path_release = os.path.join(dummy_project_root, "app", "build", "outputs", "apk", "release", "app-release.apk")
    with open(dummy_apk_path_release, "w") as f:
        f.write("This is a dummy APK file.")

    try:
        # Initialize the compiler with the dummy project path
        compiler = ApkCompiler(dummy_project_root)

        # Check if the dummy APK exists
        print(f"\n--- Testing check_apk_exists ---")
        apk_exists = compiler.check_apk_exists(dummy_apk_path_release)
        print(f"Check result: {apk_exists}")

        # Simulate building an APK (this won't actually build, but will run the simulated command)
        print(f"\n--- Testing build_apk ---")
        # Note: This will use the dummy gradlew which just prints.
        # For a real build, remove this dummy project and use a real Android project path.
        try:
            built_apk_path = compiler.build_apk("release")
            print(f"Simulated build APK path: {built_apk_path}")
            # Verify the path returned by build_apk
            if os.path.abspath(built_apk_path) != os.path.abspath(dummy_apk_path_release):
                print(f"Warning: Returned APK path '{built_apk_path}' does not match expected dummy path '{dummy_apk_path_release}'.")
        except FileNotFoundError as e:
            print(f"Caught expected FileNotFoundError during simulated build: {e}")
        except Exception as e:
            print(f"Caught unexpected exception during simulated build: {e}")


        # Simulate cleaning the project
        print(f"\n--- Testing clean_project ---")
        compiler.clean_project()
        print("Simulated project cleaning complete.")

    except FileNotFoundError as e:
        print(f"Error initializing ApkCompiler: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during demonstration: {e}")
    finally:
        # Clean up dummy files
        import shutil
        if os.path.exists(dummy_project_root):
            print("\n--- Cleaning up dummy project directory ---")
            shutil.rmtree(dummy_project_root)
            print("Dummy project directory removed.")

    print("\n--- ApkCompiler Module Demo Finished ---")