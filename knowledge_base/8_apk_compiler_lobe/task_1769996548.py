import os
import shutil
import subprocess

# --- Configuration ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
ANDROID_NDK_ROOT = os.environ.get("ANDROID_NDK_ROOT")
GRADLE_WRAPPER_PATH = "./gradlew"  # Assuming gradlew is in the current directory or PATH
APP_TEMPLATE_DIR = "./app_template"
OUTPUT_DIR = "./generated_apks"

# --- Helper Functions ---

def create_android_project_structure(project_name: str, package_name: str):
    """
    Creates a basic Android project structure using `android create`.
    This is a simplified simulation. A real implementation would involve
    more robust project creation or template copying.
    """
    print(f"Creating Android project structure for: {project_name}")
    if os.path.exists(APP_TEMPLATE_DIR):
        shutil.rmtree(APP_TEMPLATE_DIR)
    os.makedirs(APP_TEMPLATE_DIR, exist_ok=True)

    # Simulate project files. In a real scenario, this would be actual Android build files.
    os.makedirs(os.path.join(APP_TEMPLATE_DIR, "app", "src", "main", "java", *package_name.split('.')))
    os.makedirs(os.path.join(APP_TEMPLATE_DIR, "app", "src", "main", "res", "layout"))
    os.makedirs(os.path.join(APP_TEMPLATE_DIR, "app", "src", "main", "res", "drawable"))
    os.makedirs(os.path.join(APP_TEMPLATE_DIR, "app", "src", "main", "res", "values"))

    with open(os.path.join(APP_TEMPLATE_DIR, "app", "build.gradle"), "w") as f:
        f.write("""
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "{}.$package_name"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
        """.format(project_name))

    with open(os.path.join(APP_TEMPLATE_DIR, "settings.gradle"), "w") as f:
        f.write("rootProject.name = '{}'".format(project_name))

    with open(os.path.join(APP_TEMPLATE_DIR, "gradle.properties"), "w") as f:
        f.write("""org.gradle.jvmargs=-Xmx2048m
android.useAndroidX=true
android.enableJetifier=true
        """)

    print("Android project structure created.")


def compile_apk(project_dir: str, apk_output_dir: str, app_name: str) -> str:
    """
    Compiles an Android project into an APK using Gradle.
    """
    print(f"\n--- Compiling APK for: {app_name} ---")
    if not os.path.exists(GRADLE_WRAPPER_PATH):
        raise FileNotFoundError("Gradle wrapper not found. Ensure gradlew is in the PATH or current directory.")

    if not ANDROID_SDK_ROOT or not ANDROID_NDK_ROOT:
        print("Warning: ANDROID_SDK_ROOT or ANDROID_NDK_ROOT not set. APK compilation might fail or be incomplete.")
        # Attempt to proceed, but warn the user.

    os.makedirs(apk_output_dir, exist_ok=True)

    # Change directory to the project root for Gradle command
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        # Execute Gradle assembleRelease or assembleDebug
        # For simplicity, we'll use assembleDebug here. For release, signing would be needed.
        print("Running Gradle build (assembleDebug)...")
        build_command = [GRADLE_WRAPPER_PATH, "assembleDebug"]
        # On Windows, gradlew.bat is used
        if os.name == 'nt':
            build_command = ["gradlew.bat", "assembleDebug"]

        process = subprocess.Popen(build_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Gradle build failed with return code {process.returncode}")
            print("--- Gradle STDOUT ---")
            print(stdout.decode('utf-8'))
            print("--- Gradle STDERR ---")
            print(stderr.decode('utf-8'))
            raise RuntimeError("APK compilation failed.")
        else:
            print("Gradle build successful.")
            # Find the generated APK
            # The path to the APK can vary slightly depending on Gradle version and configuration
            # Common path: app/build/outputs/apk/debug/app-debug.apk
            apk_path_relative = os.path.join("app", "build", "outputs", "apk", "debug", f"{os.path.splitext(app_name)[0]}-debug.apk")
            generated_apk_full_path = os.path.join(original_dir, apk_output_dir, os.path.basename(apk_path_relative))

            # Copy the generated APK to the final output directory
            shutil.copy(apk_path_relative, generated_apk_full_path)
            print(f"APK successfully generated and copied to: {generated_apk_full_path}")
            return generated_apk_full_path

    except Exception as e:
        print(f"An error occurred during APK compilation: {e}")
        raise
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


def cleanup_android_project_template():
    """
    Cleans up the temporary Android project directory.
    """
    print("\n--- Cleaning up Android project template ---")
    if os.path.exists(APP_TEMPLATE_DIR):
        try:
            shutil.rmtree(APP_TEMPLATE_DIR)
            print(f"Removed directory: {APP_TEMPLATE_DIR}")
        except OSError as e:
            print(f"Error removing directory {APP_TEMPLATE_DIR}: {e}")
    else:
        print("No Android project template directory found to clean up.")

# --- Lobe 8: APK Compiler Lobe ---

class ApkCompilerLobe:
    """
    This lobe is responsible for compiling the generated Android project
    into a functional APK. It interfaces with the Android build tools (Gradle).
    """
    def __init__(self):
        self.project_dir = APP_TEMPLATE_DIR
        self.output_dir = OUTPUT_DIR
        self.generated_apk_path = None

    def run(self, app_name: str = "my_generated_app.apk") -> str:
        """
        Simulates the process of generating and compiling an Android APK.
        In a real scenario, this would involve:
        1. Receiving a complete Android project structure.
        2. Executing the Gradle build command.
        3. Locating and returning the path to the generated APK.
        """
        print("\n--- Lobe 8: APK Compiler Lobe Activated ---")

        # In a real scenario, this lobe would receive the fully formed project.
        # Here, we simulate its creation if it doesn't exist, or assume it's ready.
        # For demonstration, we'll call create_android_project_structure if it's not there.
        if not os.path.exists(self.project_dir):
            print("Android project template not found. Creating a placeholder template.")
            # This assumes a default package name and project name for placeholder creation.
            # In a full flow, this would be dynamic based on Lobe 6 output.
            create_android_project_structure("PlaceholderApp", "com.example.placeholder")
        else:
            print("Using existing Android project structure.")

        try:
            self.generated_apk_path = compile_apk(self.project_dir, self.output_dir, app_name)
            print(f"APK compilation complete. Path: {self.generated_apk_path}")
            return self.generated_apk_path
        except Exception as e:
            print(f"APK compilation failed: {e}")
            return None
        finally:
            # Cleanup is typically handled by a higher-level orchestrator,
            # but for self-containment, we can include it here or call a cleanup function.
            # cleanup_android_project_template() # Decided to let orchestrator handle cleanup.
            pass

    def get_generated_apk_path(self) -> str | None:
        return self.generated_apk_path

# --- Example Usage (for demonstration purposes within this lobe's context) ---
if __name__ == "__main__":
    print("--- Running Lobe 8 Demo ---")

    # Ensure environment variables are set for the demo to potentially work
    if not ANDROID_SDK_ROOT:
        print("ANDROID_SDK_ROOT environment variable not set. APK compilation might fail.")
    if not ANDROID_NDK_ROOT:
        print("ANDROID_NDK_ROOT environment variable not set. APK compilation might fail.")

    # Simulate a scenario where a project structure needs to be created
    # In a real flow, Lobe 6 (Synthesis) would provide this.
    print("\nCreating a dummy Android project structure for demonstration...")
    create_android_project_structure("DemoApp", "com.example.demo")

    apk_compiler = ApkCompilerLobe()
    generated_apk_path = apk_compiler.run(app_name="demo_app.apk")

    if generated_apk_path:
        print(f"\nSuccessfully generated APK at: {generated_apk_path}")
    else:
        print("\nAPK generation process failed.")

    # Clean up the dummy project created for this demo run
    print("\n--- Cleaning up demo project ---")
    cleanup_android_project_template()
    print("\n--- Lobe 8 Demo Finished ---")