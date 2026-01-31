import os
import shutil
import subprocess

def build_apk_from_android_project(project_dir: str, apk_output_path: str, build_tools_dir: str = None):
    """
    Builds an APK from an Android project directory using Gradle.

    Args:
        project_dir (str): The path to the root of the Android project.
        apk_output_path (str): The desired path for the generated APK file.
        build_tools_dir (str, optional): The path to the Android SDK build-tools directory.
                                          If None, it's assumed Gradle can find it.
    """
    print(f"\n--- Building APK for project: {project_dir} ---")

    gradle_command = ["./gradlew", "assembleDebug"]  # For debug builds

    if build_tools_dir:
        # This is a less common way to configure Gradle, typically Android Studio
        # handles SDK paths. If needed, one might need to configure gradle.properties
        # or use environment variables. For simplicity, we'll assume Gradle can find
        # the build tools if the SDK is correctly configured.
        print("Note: Explicitly setting build_tools_dir might require Gradle configuration.")

    try:
        # Navigate to the project directory to run Gradle commands
        original_dir = os.getcwd()
        os.chdir(project_dir)

        print(f"Executing Gradle command: {' '.join(gradle_command)}")
        # Use subprocess.run for better control and error handling
        process = subprocess.run(
            gradle_command,
            capture_output=True,
            text=True,
            check=True  # Raise CalledProcessError if the command returns a non-zero exit code
        )
        print("Gradle build output:\n", process.stdout)
        if process.stderr:
            print("Gradle build errors (if any):\n", process.stderr)

        # Find the generated APK
        # The exact location can vary, but typically it's in app/build/outputs/apk/debug/
        # Assuming a standard Android project structure
        generated_apk_dir = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")
        generated_apk_name = None
        for filename in os.listdir(generated_apk_dir):
            if filename.endswith(".apk"):
                generated_apk_name = filename
                break

        if generated_apk_name:
            source_apk_path = os.path.join(generated_apk_dir, generated_apk_name)
            print(f"Found generated APK: {source_apk_path}")

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(apk_output_path), exist_ok=True)

            # Move and rename the APK to the desired output path
            shutil.move(source_apk_path, apk_output_path)
            print(f"APK successfully built and saved to: {apk_output_path}")
        else:
            print("Error: Could not find the generated APK file in the expected location.")

    except FileNotFoundError:
        print("Error: Gradle wrapper (gradlew) not found. Make sure you are in the project root.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Gradle build: {e}")
        print("Stderr:\n", e.stderr)
        print("Stdout:\n", e.stdout)
    except Exception as e:
        print(f"An unexpected error occurred during APK building: {e}")
    finally:
        # Return to the original directory
        os.chdir(original_dir)
        print("--- APK Build Process Finished ---")

# Example Usage (requires a valid Android project structure)
if __name__ == '__main__':
    # This is a placeholder and requires a real Android project setup
    # to function correctly.
    # For a real test, you would need:
    # 1. An Android project (e.g., created with Android Studio or a template)
    # 2. A JDK and Android SDK installed and configured for Gradle
    # 3. The 'build_apk_from_android_project' function to be called with
    #    the path to your Android project and a desired output APK path.

    print("--- Demonstrating APK Builder Module ---")

    # Dummy paths for demonstration purposes. Replace with actual paths for a real run.
    dummy_android_project_path = "./dummy_android_project" # This directory needs to contain a gradlew script and Android project files
    output_apk_file_path = "./output/my_app.apk"

    # Create dummy project structure for a basic simulation (won't actually build an APK)
    if not os.path.exists(dummy_android_project_path):
        os.makedirs(os.path.join(dummy_android_project_path, "app", "build", "outputs", "apk", "debug"), exist_ok=True)
        # Create a dummy gradlew script (this is NOT a functional script)
        with open(os.path.join(dummy_android_project_path, "gradlew"), "w") as f:
            f.write("#!/bin/bash\necho 'Simulating Gradle build...'")
        os.chmod(os.path.join(dummy_android_project_path, "gradlew"), 0o755)
        print(f"Created dummy project structure at: {dummy_android_project_path}")
        print("Note: This dummy project cannot actually build an APK. For a real test,")
        print("      replace 'dummy_android_project_path' with a real Android project.")

    # Simulate building an APK (will likely fail if dummy project is used)
    # You would uncomment and adapt this for a real project.
    # try:
    #     build_apk_from_android_project(dummy_android_project_path, output_apk_file_path)
    # except Exception as e:
    #     print(f"\nSimulated build failed as expected with dummy project: {e}")


    # Clean up dummy project if created
    # if os.path.exists(dummy_android_project_path) and "./dummy_android_project" in dummy_android_project_path:
    #     shutil.rmtree(dummy_android_project_path)
    #     print(f"\nCleaned up dummy project directory: {dummy_android_project_path}")
    # if os.path.exists(os.path.dirname(output_apk_file_path)):
    #     shutil.rmtree(os.path.dirname(output_apk_file_path))
    #     print(f"Cleaned up output directory: {os.path.dirname(output_apk_file_path)}")

    print("\n--- APK Builder Module Demo Finished ---")