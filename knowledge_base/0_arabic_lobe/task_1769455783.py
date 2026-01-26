import os
import shutil
import subprocess
import time

# Global constants (assuming these are defined elsewhere or will be defined)
# For demonstration purposes, let's define some placeholders:
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT", "/path/to/android/sdk")
JAVA_HOME = os.environ.get("JAVA_HOME", "/path/to/java")
BUILD_TOOLS_DIR = os.path.join(ANDROID_SDK_ROOT, "build-tools")
APKs_DIR = "generated_apks"
JAVA_PROJECT_DIR = "android_project"
SMALI_TMP_DIR = "smali_tmp"
DEX_TMP_DIR = "dex_tmp"
AAPT2_PATH = os.path.join(BUILD_TOOLS_DIR, "latest_build_tools_version", "aapt2") # Needs to be dynamic
DX_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "latest_build_tools_version", "dx") # Needs to be dynamic
APKSIGNER_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "latest_build_tools_version", "apksigner") # Needs to be dynamic
ZIPALIGN_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "latest_build_tools_version", "zipalign") # Needs to be dynamic
DEBUG_KEYSTORE = "debug.keystore" # Assuming a dummy keystore for signing


def find_latest_build_tools_path():
    """Finds the path to the latest Android build tools."""
    if not os.path.exists(BUILD_TOOLS_DIR):
        raise FileNotFoundError("Android build tools directory not found. Please set ANDROID_SDK_ROOT.")

    build_tools_versions = sorted(
        [d for d in os.listdir(BUILD_TOOLS_DIR) if os.path.isdir(os.path.join(BUILD_TOOLS_DIR, d))],
        key=lambda x: list(map(int, x.split('.')))
    )
    if not build_tools_versions:
        raise FileNotFoundError("No Android build tools found in the specified directory.")
    latest_version = build_tools_versions[-1]
    return os.path.join(BUILD_TOOLS_DIR, latest_version)

# Dynamically set paths based on the latest build tools
LATEST_BUILD_TOOLS = find_latest_build_tools_path()
AAPT2_PATH = os.path.join(LATEST_BUILD_TOOLS, "aapt2")
DX_PATH = os.path.join(LATEST_BUILD_TOOLS, "dx")
APKSIGNER_PATH = os.path.join(LATEST_BUILD_TOOLS, "apksigner")
ZIPALIGN_PATH = os.path.join(LATEST_BUILD_TOOLS, "zipalign")

def generate_manifest_xml(package_name, activity_name):
    """Generates a basic AndroidManifest.xml file."""
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".{activity_name}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

def generate_strings_xml():
    """Generates a basic strings.xml file."""
    strings_content = """
<resources>
    <string name="app_name">GeneratedApp</string>
</resources>
"""
    strings_dir = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "values")
    os.makedirs(strings_dir, exist_ok=True)
    with open(os.path.join(strings_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_content)

def generate_activity_java(package_name, activity_name):
    """Generates a basic Java activity file."""
    java_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()}); // Assuming a layout file exists
    }}
}}
"""
    java_dir = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", *package_name.split('.'))
    os.makedirs(java_dir, exist_ok=True)
    with open(os.path.join(java_dir, f"{activity_name}.java"), "w", encoding="utf-8") as f:
        f.write(java_content)

def generate_layout_xml(activity_name):
    """Generates a basic layout XML file."""
    layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <!-- Content will be added by other modules -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    layout_dir = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "layout")
    os.makedirs(layout_dir, exist_ok=True)
    with open(os.path.join(layout_dir, f"activity_{activity_name.lower()}.xml"), "w", encoding="utf-8") as f:
        f.write(layout_content)

def setup_android_project(package_name, activity_name):
    """Sets up a minimal Android project structure."""
    print(f"Setting up Android project for package: {package_name}")
    os.makedirs(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main"), exist_ok=True)
    os.makedirs(os.path.join(JAVA_PROJECT_DIR, "app", "libs"), exist_ok=True)
    os.makedirs(os.path.join(JAVA_PROJECT_DIR, "app", "build"), exist_ok=True)

    # Create a dummy build.gradle file
    build_gradle_content = f"""
plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 33
    namespace '{package_name}'

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    // Add other necessary dependencies here
}}
"""
    with open(os.path.join(JAVA_PROJECT_DIR, "app", "build.gradle"), "w", encoding="utf-8") as f:
        f.write(build_gradle_content)

    # Create a dummy settings.gradle file
    settings_gradle_content = f"""
rootProject.name = "{JAVA_PROJECT_DIR}"
include ':app'
"""
    with open(os.path.join(JAVA_PROJECT_DIR, "settings.gradle"), "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)

    # Create a dummy proguard-rules.pro file
    with open(os.path.join(JAVA_PROJECT_DIR, "app", "proguard-rules.pro"), "w", encoding="utf-8") as f:
        f.write("")

    # Generate core Android files
    generate_manifest_xml(package_name, activity_name)
    generate_strings_xml()
    generate_activity_java(package_name, activity_name)
    generate_layout_xml(activity_name)
    print("Android project structure and core files created.")

def compile_android_project(package_name, activity_name):
    """Compiles the Android project into an unsigned APK."""
    print("Starting Android project compilation...")

    # 1. Create a dummy Android project structure
    setup_android_project(package_name, activity_name)

    # 2. Use Gradle wrapper to build the APK
    # This assumes a Gradle wrapper (gradlew) exists or can be created.
    # For simplicity, we'll try to use the system's Gradle if available,
    # or expect gradlew to be present in the project root.

    gradlew_path = os.path.join(JAVA_PROJECT_DIR, "gradlew")
    if not os.path.exists(gradlew_path):
        print("Gradle wrapper (gradlew) not found. Attempting to use system Gradle.")
        gradle_command = ["gradle", "assembleDebug"]
    else:
        print("Using Gradle wrapper (gradlew).")
        gradle_command = [gradlew_path, "assembleDebug"]

    try:
        # Ensure JAVA_HOME is set for Gradle to find Java
        env = os.environ.copy()
        if JAVA_HOME:
            env["JAVA_HOME"] = JAVA_HOME
        else:
            print("Warning: JAVA_HOME not set. Gradle compilation may fail.")

        # Run the Gradle build command
        build_process = subprocess.Popen(
            gradle_command,
            cwd=JAVA_PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        stdout, stderr = build_process.communicate()

        if build_process.returncode != 0:
            print(f"Gradle build failed with return code {build_process.returncode}")
            print("--- Gradle STDOUT ---")
            print(stdout.decode('utf-8', errors='ignore'))
            print("--- Gradle STDERR ---")
            print(stderr.decode('utf-8', errors='ignore'))
            raise RuntimeError("Android project compilation failed.")
        else:
            print("Gradle build successful.")
            print(stdout.decode('utf-8', errors='ignore')) # Print stdout for success

    except FileNotFoundError:
        print("Error: 'gradle' command not found or gradlew script is missing/not executable.")
        print("Please ensure Java is installed and JAVA_HOME is set, and that Gradle is in your PATH or gradlew is present.")
        raise
    except Exception as e:
        print(f"An error occurred during Gradle compilation: {e}")
        raise

    # The unsigned APK will be in app/build/outputs/apk/debug/app-debug.apk
    unsigned_apk_path = os.path.join(JAVA_PROJECT_DIR, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
    if not os.path.exists(unsigned_apk_path):
        raise FileNotFoundError(f"Unsigned APK not found at expected location: {unsigned_apk_path}")

    print(f"Unsigned APK generated at: {unsigned_apk_path}")
    return unsigned_apk_path

def sign_apk(unsigned_apk_path, output_apk_path):
    """Signs the APK using debug keystore and zipaligns it."""
    print("Signing and zipaligning APK...")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_apk_path), exist_ok=True)

    # 1. Create a dummy debug keystore if it doesn't exist
    if not os.path.exists(DEBUG_KEYSTORE):
        print(f"Creating dummy debug keystore: {DEBUG_KEYSTORE}")
        # Using keytool to generate a self-signed certificate for debugging
        keytool_command = [
            "keytool",
            "-genkey",
            "-v",
            "-keystore", DEBUG_KEYSTORE,
            "-alias", "androiddebugkey",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-dname", "CN=Android Debug,OU=Android,O=Android,C=US"
        ]
        try:
            # Provide dummy password input for keytool non-interactively
            # This is a simplified approach; in a real scenario, you'd manage passwords securely.
            # For this demo, we'll assume default passwords or no password prompt issues.
            # A more robust solution might involve piping input.
            # For this demo, we'll assume the prompt is handled or non-existent for simplicity.
            # If it prompts for passwords, this part will fail interactively.
            # A common workaround for CI/CD is to use command-line args for passwords.
            # Example: -storepass android -keypass android
            subprocess.run(keytool_command, check=True, capture_output=True)
            print("Dummy debug keystore created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating debug keystore: {e}")
            print(f"Stderr: {e.stderr.decode('utf-8', errors='ignore')}")
            raise
        except FileNotFoundError:
            print("Error: 'keytool' command not found. Ensure Java Development Kit (JDK) is installed and 'keytool' is in your PATH.")
            raise


    # 2. Sign the APK with apksigner
    print("Using apksigner for signing...")
    signed_apk_path = output_apk_path.replace(".apk", "-signed-unsigned.apk") # Temporary signed file
    sign_command = [
        APKSIGNER_PATH,
        "sign",
        "--ks", DEBUG_KEYSTORE,
        "--ks-key-alias", "androiddebugkey",
        "--out", signed_apk_path,
        unsigned_apk_path
    ]
    # Add password flags if needed, e.g., "--ks-pass pass:android", "--key-pass pass:android"
    # For simplicity, we assume default or interactive password handling for this demo.
    # If keytool was run with passwords, these should match.
    # If keytool was run without passwords, these might not be needed or could be 'pass:'

    try:
        # Attempt to run without explicit password arguments first, assuming defaults or no prompt
        sign_process = subprocess.run(sign_command, check=True, capture_output=True)
        print("APK signed successfully (temporary file).")
        print(sign_process.stdout.decode('utf-8', errors='ignore'))
    except subprocess.CalledProcessError as e:
        print(f"Error signing APK with apksigner: {e}")
        print(f"Stderr: {e.stderr.decode('utf-8', errors='ignore')}")
        # If it failed, try again with common default passwords
        print("Retrying signing with default passwords 'android'...")
        sign_command.extend(["--ks-pass", "pass:android", "--key-pass", "pass:android"])
        try:
            sign_process = subprocess.run(sign_command, check=True, capture_output=True)
            print("APK signed successfully (temporary file with default passwords).")
            print(sign_process.stdout.decode('utf-8', errors='ignore'))
        except subprocess.CalledProcessError as e_retry:
            print(f"Retry signing failed: {e_retry}")
            print(f"Stderr: {e_retry.stderr.decode('utf-8', errors='ignore')}")
            raise RuntimeError("APK signing failed.")
    except FileNotFoundError:
        print(f"Error: '{APKSIGNER_PATH}' not found. Ensure Android SDK build tools are correctly configured.")
        raise

    # 3. Zipalign the signed APK
    print("Using zipalign for optimization...")
    zipalign_command = [
        ZIPALIGN_PATH,
        "-v",  # Verbose output
        "4",   # Alignment in bytes
        signed_apk_path,
        output_apk_path
    ]
    try:
        zipalign_process = subprocess.run(zipalign_command, check=True, capture_output=True)
        print("APK zipaligned successfully.")
        print(zipalign_process.stdout.decode('utf-8', errors='ignore'))
    except subprocess.CalledProcessError as e:
        print(f"Error zipaligning APK: {e}")
        print(f"Stderr: {e.stderr.decode('utf-8', errors='ignore')}")
        raise RuntimeError("APK zipaligning failed.")
    except FileNotFoundError:
        print(f"Error: '{ZIPALIGN_PATH}' not found. Ensure Android SDK build tools are correctly configured.")
        raise

    # Clean up the temporary signed-unsigned APK
    if os.path.exists(signed_apk_path):
        os.remove(signed_apk_path)
        print(f"Removed temporary signed file: {signed_apk_path}")

    print(f"Final signed and zipaligned APK saved to: {output_apk_path}")

def cleanup_apk_compiler_artifacts(project_root, generated_code_dir):
    """Cleans up generated artifacts from the APK compilation process."""
    print("\n--- Cleaning up APK compiler artifacts ---")

    # Remove the generated Java project directory
    if os.path.exists(JAVA_PROJECT_DIR):
        try:
            shutil.rmtree(JAVA_PROJECT_DIR)
            print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")
        except OSError as e:
            print(f"Error removing directory {JAVA_PROJECT_DIR}: {e}")

    # Remove temporary directories if they exist
    for tmp_dir in [SMALI_TMP_DIR, DEX_TMP_DIR]:
        if os.path.exists(tmp_dir):
            try:
                shutil.rmtree(tmp_dir)
                print(f"Removed temporary directory: {tmp_dir}")
            except OSError as e:
                print(f"Error removing directory {tmp_dir}: {e}")

    # Remove generated APKs directory if empty or specific APKs need removal
    if os.path.exists(APKs_DIR):
        # Optionally remove all generated APKs
        # for item in os.listdir(APKs_DIR):
        #     item_path = os.path.join(APKS_DIR, item)
        #     if os.path.isfile(item_path):
        #         os.remove(item_path)
        #         print(f"Removed generated APK: {item_path}")
        # If APKs_DIR is empty after removing APKs, you might remove the directory itself:
        # if not os.listdir(APKS_DIR):
        #     shutil.rmtree(APKS_DIR)
        #     print(f"Removed empty APKs directory: {APKs_DIR}")
        pass # Keep APKs_DIR for inspection or further use for now.

    # Remove debug keystore if created by this module and no longer needed
    if os.path.exists(DEBUG_KEYSTORE):
        # Decide whether to remove it based on its creation.
        # For this demo, we might leave it for potential reuse.
        # If you want to remove it:
        # try:
        #     os.remove(DEBUG_KEYSTORE)
        #     print(f"Removed debug keystore: {DEBUG_KEYSTORE}")
        # except OSError as e:
        #     print(f"Error removing debug keystore {DEBUG_KEYSTORE}: {e}")
        pass


def generate_apk_from_natural_language(natural_language_prompt: str) -> str:
    """
    This function orchestrates the generation of an APK from a natural language prompt.
    It acts as a high-level controller for the APK compilation process.

    Args:
        natural_language_prompt: The input string describing the desired APK.

    Returns:
        The path to the generated APK file.
    """
    print("\n--- Initiating APK Generation from Natural Language ---")

    # --- Step 1: Parse Natural Language Prompt (Simulated) ---
    # In a real scenario, Lobe 0_arabic_lobe would process this prompt.
    # For demonstration, we'll extract placeholder package and activity names.
    # A more sophisticated parser would identify UI elements, permissions, etc.
    print(f"Processing prompt: '{natural_language_prompt}'")
    # Example: Extracting package name and activity name.
    # This logic would be far more complex in a real system.
    try:
        # Simple parsing for demo purposes: assume prompt contains "package name" and "activity name"
        # A real Arabic NLP model would do this much more robustly.
        parts = natural_language_prompt.split("activity name")
        if len(parts) < 2:
            raise ValueError("Prompt format not recognized for package and activity extraction.")
        
        package_name_part = parts[0].strip()
        package_name = package_name_part.split("package name")[-1].strip()
        activity_name = parts[1].strip()
        
        if not package_name or not activity_name:
            raise ValueError("Could not extract package name or activity name from prompt.")
            
        # Ensure valid Java/Android identifiers
        package_name = package_name.replace(" ", "_").lower()
        activity_name = "".join(word.capitalize() for word in activity_name.split())

        print(f"Extracted Package Name: {package_name}")
        print(f"Extracted Activity Name: {activity_name}")

    except Exception as e:
        print(f"Error parsing prompt: {e}")
        print("Please provide a prompt in the format: 'Create an app with package name <package_name> and activity name <activity_name>'.")
        return None

    # --- Step 2: Compile Android Project ---
    # This part uses Gradle to build the initial APK.
    # It's a simplified representation of Lobe 8_apk_compiler_lobe.
    try:
        unsigned_apk_path = compile_android_project(package_name, activity_name)
    except Exception as e:
        print(f"Failed to compile Android project: {e}")
        return None

    # --- Step 3: Sign and Align APK ---
    # This is another part of Lobe 8_apk_compiler_lobe's responsibility.
    timestamp = int(time.time())
    apk_filename = f"{package_name}-{activity_name}-{timestamp}.apk"
    output_apk_path = os.path.join(APKs_DIR, apk_filename)
    
    try:
        sign_apk(unsigned_apk_path, output_apk_path)
    except Exception as e:
        print(f"Failed to sign and align APK: {e}")
        return None

    print(f"\n--- APK Generation Complete ---")
    print(f"Generated APK: {output_apk_path}")
    return output_apk_path


# --- Example Usage ---
if __name__ == "__main__":
    # Ensure necessary environment variables are set for Android SDK and Java
    if not ANDROID_SDK_ROOT or not JAVA_HOME:
        print("Please set ANDROID_SDK_ROOT and JAVA_HOME environment variables.")
        print(f"ANDROID_SDK_ROOT: {ANDROID_SDK_ROOT}")
        print(f"JAVA_HOME: {JAVA_HOME}")
    else:
        # Clean up any previous runs
        cleanup_apk_compiler_artifacts(".", JAVA_PROJECT_DIR)
        # cleanup_dummy_files() # Redundant if cleanup_apk_compiler_artifacts is called

        # Simulate an Arabic natural language prompt
        # In a real scenario, Lobe 0_arabic_lobe would process and potentially
        # translate or enrich this prompt before it reaches this module.
        # Example prompt that this demo parser can handle:
        demo_prompt_arabic_style = "Create an app with package name com.example.myapp and activity name MyMainActivity"
        
        generated_apk_path = generate_apk_from_natural_language(demo_prompt_arabic_style)

        if generated_apk_path and os.path.exists(generated_apk_path):
            print(f"\nSuccessfully generated APK: {generated_apk_path}")
        else:
            print("\nAPK generation failed.")
            
        # Demonstrate cleanup after generation
        print("\n--- Performing final cleanup ---")
        cleanup_apk_compiler_artifacts(".", JAVA_PROJECT_DIR)
        print("\n--- APK Compiler Module Demo Finished ---")