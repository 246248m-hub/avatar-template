import os
import shutil
import subprocess

# Define directories
TEMP_PROJECT_DIR = "temp_android_project"
KNOWLEDGE_BASE_DIR = "arabic_knowledge_base"
OUTPUT_DIR = "generated_apks"
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

GRADLE_PATH = os.path.join(ANDROID_SDK_ROOT, "cmdline-tools", "latest", "bin", "gradle")
AAPT2_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "aapt2") # Assuming current is the version you have


def initialize_arabic_knowledge_base():
    """Initializes the Arabic knowledge base directory if it doesn't exist."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Initialized Arabic knowledge base at: {KNOWLEDGE_BASE_DIR}")

def initialize_output_directory():
    """Initializes the output directory for generated APKs if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Initialized output directory at: {OUTPUT_DIR}")

def create_basic_android_project(project_name="MyApp", package_name="com.example.myapp", language="en"):
    """
    Creates a basic Android project structure using Gradle.
    Currently supports English, but will be extended for Arabic.
    """
    if os.path.exists(TEMP_PROJECT_DIR):
        shutil.rmtree(TEMP_PROJECT_DIR)
    os.makedirs(TEMP_PROJECT_DIR)

    # Use Gradle wrapper if available, otherwise assume Gradle is in PATH or specified by ANDROID_SDK_ROOT
    gradle_command = ["gradlew", "init", "--type", "basic", "--dsl", "kotlin", "--project-name", project_name]
    if os.name == 'nt': # Windows
        gradle_command[0] += ".bat"
    
    # Attempt to run gradlew in the temp directory
    try:
        subprocess.run(gradle_command, cwd=TEMP_PROJECT_DIR, check=True, capture_output=True, text=True)
        print(f"Created basic Android project structure in: {TEMP_PROJECT_DIR}")
    except FileNotFoundError:
        print("Gradle wrapper not found. Attempting to use system Gradle.")
        gradle_command = ["gradle", "init", "--type", "basic", "--dsl", "kotlin", "--project-name", project_name]
        try:
            subprocess.run(gradle_command, cwd=TEMP_PROJECT_DIR, check=True, capture_output=True, text=True)
            print(f"Created basic Android project structure using system Gradle in: {TEMP_PROJECT_DIR}")
        except FileNotFoundError:
            print("Gradle command not found. Please ensure Gradle is installed and in your PATH or ANDROID_SDK_ROOT is set correctly.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Gradle initialization failed: {e.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Gradle initialization failed: {e.stderr}")
        return False

    # Basic AndroidManifest.xml creation (will be enhanced for Arabic)
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
    """
    manifest_dir = os.path.join(TEMP_PROJECT_DIR, "app", "src", "main")
    os.makedirs(manifest_dir, exist_ok=True)
    with open(os.path.join(manifest_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Basic strings.xml (will be enhanced for Arabic)
    strings_content = f"""
<resources>
    <string name="app_name">{project_name}</string>
</resources>
    """
    values_dir = os.path.join(manifest_dir, "res", "values")
    os.makedirs(values_dir, exist_ok=True)
    with open(os.path.join(values_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_content)

    return True

def generate_arabic_strings(prompt_text, language_code="ar"):
    """
    Generates Arabic string resources from natural language prompts.
    This function is a placeholder and requires actual NLP/NLG implementation.
    """
    print(f"Generating Arabic strings for prompt: '{prompt_text}' (Language: {language_code})")
    # In a real scenario, this would involve:
    # 1. Parsing the prompt to identify key phrases and their desired string names.
    # 2. Translating or generating Arabic text for these phrases.
    # 3. Formatting them into Android string resource format (e.g., <string name="greeting">مرحبا</string>).

    # Dummy implementation:
    if "greeting" in prompt_text.lower():
        return {"greeting": "مرحبا بالعالم"}
    elif "welcome" in prompt_text.lower():
        return {"welcome_message": "أهلاً بك في تطبيقنا"}
    else:
        return {"default_message": "رسالة افتراضية"}

def inject_arabic_strings_into_project(generated_strings, project_path=TEMP_PROJECT_DIR):
    """
    Injects generated Arabic strings into the Android project's resources.
    This currently creates a separate values-ar directory.
    """
    arabic_values_dir = os.path.join(project_path, "app", "src", "main", "res", "values-ar")
    os.makedirs(arabic_values_dir, exist_ok=True)

    strings_xml_path = os.path.join(arabic_values_dir, "strings.xml")
    
    strings_content_parts = ['<resources>']
    for name, value in generated_strings.items():
        strings_content_parts.append(f'    <string name="{name}">{value}</string>')
    strings_content_parts.append('</resources>')
    
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(strings_content_parts))
    
    print(f"Injected Arabic strings into: {strings_xml_path}")

def build_apk(project_path=TEMP_PROJECT_DIR, output_dir=OUTPUT_DIR, project_name="MyApp"):
    """
    Builds the Android APK using Gradle.
    """
    print(f"\n--- Building APK for project: {project_name} ---")

    # Ensure Gradle command uses the correct path (either gradlew or system gradle)
    gradlew_path = os.path.join(project_path, "gradlew")
    if os.name == 'nt': # Windows
        gradlew_path += ".bat"

    if os.path.exists(gradlew_path):
        gradle_command = [gradlew_path, "assembleDebug"]
    else:
        print("Gradle wrapper not found. Attempting to use system Gradle.")
        gradle_command = ["gradle", "assembleDebug"]

    try:
        # Execute the Gradle build command
        process = subprocess.run(
            gradle_command,
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8' # Explicitly set encoding for broad compatibility
        )
        print("Gradle build output:")
        print(process.stdout)

        # Locate the generated APK
        # The default location for debug APKs is app/build/outputs/apk/debug/app-debug.apk
        apk_source_path = os.path.join(project_path, "app", "build", "outputs", "apk", "debug", f"{project_name.lower()}-debug.apk")
        
        if not os.path.exists(apk_source_path):
            # Try alternative naming if the project name wasn't used in the APK name
            apk_source_path = os.path.join(project_path, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
            
        if os.path.exists(apk_source_path):
            # Copy the APK to the output directory
            final_apk_name = f"{project_name}_arabic_debug.apk"
            final_apk_path = os.path.join(output_dir, final_apk_name)
            shutil.copy(apk_source_path, final_apk_path)
            print(f"\nSuccessfully generated APK at: {final_apk_path}")
            return final_apk_path
        else:
            print(f"\nError: APK file not found at expected location: {apk_source_path} (or fallback)")
            return None

    except FileNotFoundError:
        print("Gradle command not found. Please ensure Gradle is installed and in your PATH or ANDROID_SDK_ROOT is set correctly.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"\nAPK generation process failed. Error details:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"Stdout:\n{e.stdout}")
        print(f"Stderr:\n{e.stderr}")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred during APK build: {e}")
        return None

def cleanup_android_project_template(project_path=TEMP_PROJECT_DIR):
    """Cleans up the temporary Android project directory."""
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        print(f"Cleaned up temporary project directory: {project_path}")

def demo_arabic_nlp_and_apk_generation():
    """
    Demonstrates the integration of Arabic NLP logic and APK generation.
    """
    print("\n--- Starting Lobe 10_arabic_apk_integration_lobe Demo ---")

    # 1. Initialize directories
    initialize_arabic_knowledge_base()
    initialize_output_directory()

    # 2. Create a basic Android project
    project_name = "MyArabicApp"
    package_name = "com.example.myarabicapp"
    if not create_basic_android_project(project_name=project_name, package_name=package_name):
        print("Failed to create basic Android project. Aborting demo.")
        return

    # 3. Simulate Arabic NLP processing
    arabic_prompt_1 = "Provide a greeting message for the app."
    arabic_strings_1 = generate_arabic_strings(arabic_prompt_1)
    inject_arabic_strings_into_project(arabic_strings_1, TEMP_PROJECT_DIR)

    arabic_prompt_2 = "Display a welcome message to the user."
    arabic_strings_2 = generate_arabic_strings(arabic_prompt_2)
    inject_arabic_strings_into_project(arabic_strings_2, TEMP_PROJECT_DIR)
    
    # 4. Build the APK
    generated_apk_path = build_apk(project_path=TEMP_PROJECT_DIR, output_dir=OUTPUT_DIR, project_name=project_name)

    if generated_apk_path:
        print(f"\nAPK successfully generated and saved to: {generated_apk_path}")
    else:
        print("\nAPK generation process failed.")

    # 5. Clean up the dummy project
    print("\n--- Cleaning up demo project ---")
    cleanup_android_project_template()
    print("\n--- Lobe 10 Demo Finished ---")

# Example of how to run the demo:
if __name__ == "__main__":
    # Ensure ANDROID_SDK_ROOT is set for the script to run
    if not ANDROID_SDK_ROOT:
        print("Error: ANDROID_SDK_ROOT environment variable not set.")
        print("Please set it to your Android SDK installation path before running this script.")
    else:
        demo_arabic_nlp_and_apk_generation()