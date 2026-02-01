import os
import shutil
import subprocess
from typing import Dict, Any

# --- Constants and Configuration ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

BUILD_TOOLS_DIR = os.path.join(ANDROID_SDK_ROOT, "build-tools")
# Find the latest build tools version
build_tools_versions = sorted([d for d in os.listdir(BUILD_TOOLS_DIR) if os.path.isdir(os.path.join(BUILD_TOOLS_DIR, d))])
if not build_tools_versions:
    raise EnvironmentError("No Android build tools found. Please install them.")
LATEST_BUILD_TOOLS_VERSION = build_tools_versions[-1]
AAPT2_PATH = os.path.join(BUILD_TOOLS_DIR, LATEST_BUILD_TOOLS_VERSION, "aapt2")
APKSIGNER_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", LATEST_BUILD_TOOLS_VERSION, "apksigner") # Placeholder for actual apksigner path if different

# Dummy Keystore for signing (in a real scenario, this would be managed securely)
DUMMY_KEYSTORE_PATH = "debug.keystore"
DUMMY_KEY_ALIAS = "androiddebugkey"
DUMMY_KEY_PASS = "android"
DUMMY_STORE_PASS = "android"

# --- Helper Functions ---

def create_dummy_android_project(project_dir: str, app_name: str) -> None:
    """Creates a minimal dummy Android project structure."""
    os.makedirs(os.path.join(project_dir, "app", "src", "main", "java", app_name.lower().replace(" ", "_")), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "app", "src", "main", "res", "values"), exist_ok=True)

    # Create AndroidManifest.xml
    manifest_content = f"""
    <manifest xmlns:android="http://schemas.android.com/apk/res/android"
        package="{app_name.lower().replace(' ', '_')}">

        <application
            android:allowBackup="true"
            android:icon="@mipmap/ic_launcher"
            android:label="@string/app_name"
            android:roundIcon="@mipmap/ic_launcher_round"
            android:supportsRtl="true"
            android:theme="@style/AppTheme">
            <activity android:name=".MainActivity">
                <intent-filter>
                    <action android:name="android.intent.action.MAIN" />
                    <category android:name="android.intent.category.LAUNCHER" />
                </intent-filter>
            </activity>
        </application>
    </manifest>
    """
    with open(os.path.join(project_dir, "app", "src", "main", "AndroidManifest.xml"), "w") as f:
        f.write(manifest_content)

    # Create MainActivity.java
    activity_content = f"""
    package {app_name.lower().replace(' ', '_')};

    import androidx.appcompat.app.AppCompatActivity;
    import android.os.Bundle;

    public class MainActivity extends AppCompatActivity {{

        @Override
        protected void onCreate(Bundle savedInstanceState) {{
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
        }}
    }}
    """
    with open(os.path.join(project_dir, "app", "src", "main", "java", app_name.lower().replace(" ", "_"), "MainActivity.java"), "w") as f:
        f.write(activity_content)

    # Create activity_main.xml
    layout_content = """
    <?xml version="1.0" encoding="utf-8"?>
    <androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://schemas.android.com/apk/res-auto"
        xmlns:tools="http://schemas.android.com/tools"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        tools:context=".MainActivity">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Hello World!"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintLeft_toLeftOf="parent"
            app:layout_constraintRight_toRightOf="parent"
            app:layout_constraintTop_toTopOf="parent" />

    </androidx.constraintlayout.widget.ConstraintLayout>
    """
    with open(os.path.join(project_dir, "app", "src", "main", "res", "layout", "activity_main.xml"), "w") as f:
        f.write(layout_content)

    # Create strings.xml
    values_content = f"""
    <resources>
        <string name="app_name">{app_name}</string>
    </resources>
    """
    with open(os.path.join(project_dir, "app", "src", "main", "res", "values", "strings.xml"), "w") as f:
        f.write(values_content)

    # Create build.gradle (app level) - minimal for demonstration
    gradle_app_content = """
    plugins {
        id 'com.android.application'
    }

    android {
        namespace '""" + app_name.lower().replace(' ', '_') + """'
        compileSdk 34

        defaultConfig {
            applicationId '""" + app_name.lower().replace(' ', '_') + """'
            minSdk 24
            targetSdk 34
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
    }

    dependencies {
        implementation 'androidx.appcompat:appcompat:1.6.1'
        implementation 'com.google.android.material:material:1.11.0'
        implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    }
    """
    with open(os.path.join(project_dir, "app", "build.gradle"), "w") as f:
        f.write(gradle_app_content)

    # Create build.gradle (project level)
    gradle_project_content = """
    plugins {
        id 'com.android.application' version '8.2.0' apply false
    }
    """
    with open(os.path.join(project_dir, "build.gradle"), "w") as f:
        f.write(gradle_project_content)

    # Create settings.gradle
    settings_content = """
    rootProject.name = '""" + app_name + """'
    include ':app'
    """
    with open(os.path.join(project_dir, "settings.gradle"), "w") as f:
        f.write(settings_content)

def create_dummy_keystore():
    """Creates a dummy debug keystore if it doesn't exist."""
    if not os.path.exists(DUMMY_KEYSTORE_PATH):
        print(f"Creating dummy keystore at {DUMMY_KEYSTORE_PATH}...")
        try:
            # Using keytool to generate a self-signed certificate
            subprocess.run([
                "keytool", "-genkey", "-v", "-keystore", DUMMY_KEYSTORE_PATH,
                "-alias", DUMMY_KEY_ALIAS, "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-dname", "CN=Android Debug,O=Android,C=US",
                "-storepass", DUMMY_STORE_PASS, "-keypass", DUMMY_KEY_PASS
            ], check=True, capture_output=True, text=True)
            print("Dummy keystore created successfully.")
        except FileNotFoundError:
            print("Error: 'keytool' command not found. Please ensure Java Development Kit (JDK) is installed and in your PATH.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"Error creating keystore: {e}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            raise

def run_gradle_build(project_dir: str, output_apk_path: str) -> None:
    """Runs the Gradle build process to generate an APK."""
    print(f"Running Gradle build in {project_dir}...")
    try:
        # We'll use Gradle wrapper if available, otherwise assume Gradle is in PATH
        gradle_command = ["./gradlew", "assembleDebug", "-p", project_dir]
        if not os.path.exists(os.path.join(project_dir, "gradlew")):
            gradle_command = ["gradle", "assembleDebug", "-p", project_dir]

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_apk_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Execute the Gradle command
        process = subprocess.run(gradle_command, cwd=project_dir, check=True, capture_output=True, text=True)
        print("Gradle build output:")
        print(process.stdout)

        # Find the generated APK
        generated_apk_dir = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")
        generated_apk_name = next((f for f in os.listdir(generated_apk_dir) if f.endswith(".apk")), None)

        if not generated_apk_name:
            raise FileNotFoundError("Generated APK not found after build.")

        shutil.move(os.path.join(generated_apk_dir, generated_apk_name), output_apk_path)
        print(f"APK successfully built and moved to: {output_apk_path}")

    except FileNotFoundError:
        print("Error: Gradle command not found. Ensure Gradle is installed or a gradlew wrapper exists in the project.")
        raise
    except subprocess.CalledProcessError as e:
        print(f"Gradle build failed: {e}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during Gradle build: {e}")
        raise

def sign_apk(apk_path: str, output_signed_apk_path: str) -> None:
    """Signs the APK using apksigner."""
    print(f"Signing APK: {apk_path}...")
    create_dummy_keystore() # Ensure keystore exists

    try:
        command = [
            APKSIGNER_PATH, "sign",
            "--ks", DUMMY_KEYSTORE_PATH,
            "--ks-key-alias", DUMMY_KEY_ALIAS,
            "--ks-pass", f"pass:{DUMMY_KEY_PASS}",
            "--key-pass", f"pass:{DUMMY_STORE_PASS}",
            "--out", output_signed_apk_path,
            apk_path
        ]
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        print("ApkSigner output:")
        print(process.stdout)
        print(f"APK successfully signed and saved to: {output_signed_apk_path}")

    except FileNotFoundError:
        print(f"Error: '{APKSIGNER_PATH}' command not found. Ensure Android SDK build tools are correctly installed and in PATH.")
        raise
    except subprocess.CalledProcessError as e:
        print(f"APK signing failed: {e}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during APK signing: {e}")
        raise

def cleanup_android_project_template(project_path: str) -> None:
    """Removes the dummy Android project directory."""
    if os.path.exists(project_path):
        print(f"Cleaning up dummy project directory: {project_path}")
        shutil.rmtree(project_path)

# --- Lobe 8: APK Compiler Lobe ---

class ApkCompilerLobe:
    """
    Lobe responsible for compiling natural language descriptions into APKs.
    This lobe simulates the process by creating a basic Android project,
    building it with Gradle, and signing the resulting APK.
    """
    def __init__(self, temp_dir: str = "temp_android_project"):
        self.temp_dir = temp_dir
        self.project_path = os.path.join(os.getcwd(), self.temp_dir)
        self.generated_apk_path = None

    def run(self, app_name: str = "SimulatedApp", output_dir: str = "generated_apks") -> str:
        """
        Simulates the APK generation process.

        Args:
            app_name: The desired name for the application.
            output_dir: The directory where the final APK will be saved.

        Returns:
            The absolute path to the generated and signed APK file.
        """
        print(f"\n--- Lobe 8: APK Compiler Lobe ---")
        print(f"Initiating APK generation for: {app_name}")

        # 1. Create a dummy Android project structure
        print(f"Creating dummy Android project in: {self.project_path}")
        create_dummy_android_project(self.project_path, app_name)
        print("Dummy project structure created.")

        # 2. Build the APK using Gradle
        unsigned_apk_filename = f"{app_name.lower().replace(' ', '_')}-unsigned.apk"
        unsigned_apk_path_temp = os.path.join(self.project_path, unsigned_apk_filename) # Temporary path during build

        # Ensure the output directory for the final APK exists
        os.makedirs(output_dir, exist_ok=True)
        signed_apk_filename = f"{app_name.lower().replace(' ', '_')}.apk"
        self.generated_apk_path = os.path.abspath(os.path.join(output_dir, signed_apk_filename))

        try:
            run_gradle_build(self.project_path, unsigned_apk_path_temp)

            # 3. Sign the APK
            sign_apk(unsigned_apk_path_temp, self.generated_apk_path)

            print(f"\nSimulated APK generation process finished. Output: {self.generated_apk_path}")
            return self.generated_apk_path

        finally:
            # 4. Clean up the dummy project
            cleanup_android_project_template(self.project_path)
            # Clean up the unsigned APK if it exists
            if os.path.exists(unsigned_apk_path_temp):
                os.remove(unsigned_apk_path_temp)

# --- Example Usage (for demonstration purposes) ---
if __name__ == "__main__":
    # This block is for demonstrating the ApkCompilerLobe's functionality
    # In a real scenario, this would be called by another lobe.

    print("--- Demonstrating ApkCompilerLobe ---")
    apk_compiler = ApkCompilerLobe()

    try:
        # Simulate generating an APK for an app named "MyAwesomeApp"
        generated_apk_location = apk_compiler.run(app_name="MyAwesomeApp", output_dir="my_apks")
        print(f"\nSuccessfully generated and signed APK at: {generated_apk_location}")

        # Clean up the dummy keystore if created for this demo (optional)
        # if os.path.exists(DUMMY_KEYSTORE_PATH):
        #     os.remove(DUMMY_KEYSTORE_PATH)
        #     print(f"Removed dummy keystore: {DUMMY_KEYSTORE_PATH}")

    except Exception as e:
        print(f"\nDemonstration failed: {e}")

    print("\n--- ApkCompilerLobe Demonstration Finished ---")