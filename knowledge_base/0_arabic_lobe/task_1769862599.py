import os
import subprocess
import shutil
import re

# Assume these directories are pre-defined and accessible
# TEMP_PROJECT_DIR = "/path/to/temporary/project"
# APK_OUTPUT_DIR = "/path/to/apk/output"
# KNOWLEDGE_BASE_DIR = "/path/to/knowledge/base"

# Placeholder for actual build commands based on your setup
# These might involve Android SDK tools, build tools, etc.
# Example using Gradle (common for Android development)
GRADLE_BUILD_COMMAND = ["./gradlew", "assembleDebug"]

def is_valid_package_name(name):
    """Checks if a string is a valid Java/Android package name."""
    return re.match(r'^[a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)*$', name) is not None

class ArabicNLPProcessor:
    """
    A placeholder class for Arabic Natural Language Processing tasks.
    In a real scenario, this would integrate with libraries like NLTK, SpaCy with Arabic models,
    or custom Arabic NLP tools.
    """
    def __init__(self, knowledge_base_dir):
        self.knowledge_base_dir = knowledge_base_dir
        print(f"ArabicNLPProcessor initialized with knowledge base: {self.knowledge_base_dir}")

    def extract_package_name_from_text(self, text):
        """
        Extracts a potential Android package name from Arabic text.
        This is a simplified example. Real extraction would be more complex.
        It looks for common patterns like 'اسم الحزمة' followed by a potential package.
        """
        match = re.search(r'(?:اسم الحزمة|حزمة التطبيق)\s*[:\s]\s*([a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)*)', text, re.IGNORECASE)
        if match:
            package_name = match.group(1).lower()
            if is_valid_package_name(package_name):
                print(f"Extracted potential package name: {package_name}")
                return package_name
        print("Could not extract a valid package name from the text.")
        return None

    def generate_app_name_from_text(self, text):
        """
        Generates a human-readable app name from Arabic text.
        Simplified example: looks for phrases indicating the app's purpose.
        """
        # This is highly dependent on the NLP model and data.
        # For demonstration, we'll extract a phrase after a specific keyword.
        match = re.search(r'(?:اسم التطبيق|هذا التطبيق هو)\s*[:\s]\s*(.*)', text, re.IGNORECASE)
        if match:
            app_name = match.group(1).strip()
            # Basic cleaning: remove trailing punctuation and trim
            app_name = re.sub(r'[.،؛!?]$', '', app_name).strip()
            if app_name:
                print(f"Generated app name: {app_name}")
                return app_name
        print("Could not generate a meaningful app name from the text.")
        return None

    def clean_arabic_text(self, text):
        """
        Cleans Arabic text by removing noise, diacritics, etc.
        A more robust implementation would handle specific NLP cleaning steps.
        """
        # Remove diacritics
        text = re.sub(r'[\u064B-\u0652]', '', text)
        # Remove common Arabic punctuation that might not be relevant for code generation
        text = re.sub(r'[،؛؟]', '', text)
        # Normalize different forms of alif, ya, ta marbuta
        text = re.sub(r'[أإآ]', 'ا', text)
        text = re.sub(r'[ى]', 'ي', text)
        text = re.sub(r'[ة]', 'ه', text)
        return text.strip()


class CodeGenerator:
    """
    Handles the generation of Android project structure and code.
    This class would be responsible for creating necessary files like
    AndroidManifest.xml, build.gradle, and basic Java/Kotlin source files.
    """
    def __init__(self, temp_project_dir):
        self.temp_project_dir = temp_project_dir
        print(f"CodeGenerator initialized for temporary directory: {self.temp_project_dir}")

    def create_android_project_structure(self, package_name, app_name):
        """
        Creates a basic Android project directory structure.
        This is a simplified simulation. A real implementation would use Android Studio's
        project creation tools or meticulously build the structure.
        """
        if not is_valid_package_name(package_name):
            raise ValueError(f"Invalid package name provided: {package_name}")

        project_path = os.path.join(self.temp_project_dir, app_name.replace(" ", "_").lower())
        src_path = os.path.join(project_path, "app", "src", "main")
        manifest_path = os.path.join(src_path, "AndroidManifest.xml")
        build_gradle_path = os.path.join(project_path, "app", "build.gradle")
        main_activity_path = os.path.join(src_path, "java", *package_name.split('.'), "MainActivity.java")

        os.makedirs(os.path.dirname(main_activity_path), exist_ok=True)
        os.makedirs(os.path.dirname(build_gradle_path), exist_ok=True)

        print(f"Creating project structure at: {project_path}")

        # Create a dummy AndroidManifest.xml
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app_name}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppName">
        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"Created {manifest_path}")

        # Create a dummy build.gradle file (simplified)
        build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // If using Kotlin, otherwise adjust
}}

android {{
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
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
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        with open(build_gradle_path, "w", encoding="utf-8") as f:
            f.write(build_gradle_content)
        print(f"Created {build_gradle_path}")


        # Create a dummy MainActivity.java
        main_activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Basic UI for demonstration
        TextView textView = new TextView(this);
        textView.setText("Welcome to {app_name}!");
        textView.setTextSize(24);
        textView.setGravity(android.view.Gravity.CENTER);
        setContentView(textView);
    }}
}}
"""
        with open(main_activity_path, "w", encoding="utf-8") as f:
            f.write(main_activity_content)
        print(f"Created {main_activity_path}")

        return project_path

    def build_apk(self, project_root_dir, output_apk_dir):
        """
        Builds the Android project into an APK.
        This function assumes a Gradle-based project and the Android SDK is configured.
        """
        print(f"\n--- Initiating APK build for project at: {project_root_dir} ---")
        # Ensure the output directory exists
        os.makedirs(output_apk_dir, exist_ok=True)

        # Determine the correct Gradle wrapper command.
        # On Windows, it might be .\gradlew.bat, on Linux/macOS ./gradlew
        gradle_wrapper_command = "./gradlew"
        if os.name == 'nt': # For Windows
            gradle_wrapper_command = ".\\gradlew.bat"
            if not os.path.exists(os.path.join(project_root_dir, gradle_wrapper_command)):
                # Fallback if no wrapper is found, assuming gradlew is in PATH
                gradle_wrapper_command = "gradle"


        # Define the command to build the APK (assembleDebug for debuggable APK)
        # The command needs to be executed from the project's root directory
        build_command = [gradle_wrapper_command, "assembleDebug"]

        try:
            # Change directory to the project root to run Gradle commands
            original_dir = os.getcwd()
            os.chdir(project_root_dir)

            print(f"Executing build command: {' '.join(build_command)}")
            # Execute the build command
            # We use capture_output=True and text=True to get stdout/stderr
            result = subprocess.run(
                build_command,
                capture_output=True,
                text=True,
                check=True,  # Raises CalledProcessError if the command returns a non-zero exit code
                encoding='utf-8',
                errors='replace'
            )
            print("Gradle Build Output (stdout):")
            print(result.stdout)
            print("Gradle Build Output (stderr):")
            print(result.stderr)

            # Find the generated APK. The location depends on the Gradle setup.
            # Typically it's app/build/outputs/apk/debug/app-debug.apk
            debug_apk_path = os.path.join(project_root_dir, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
            if not os.path.exists(debug_apk_path):
                raise FileNotFoundError(f"APK not found at expected location: {debug_apk_path}")

            # Construct the final APK name
            final_apk_name = "generated_app.apk" # This could be derived from app_name if needed
            final_apk_path = os.path.join(output_apk_dir, final_apk_name)

            # Move the APK to the final output directory
            shutil.copy(debug_apk_path, final_apk_path)
            print(f"Successfully built APK. Copied to: {final_apk_path}")

            return final_apk_path

        except FileNotFoundError as e:
            print(f"Error: Build command or APK file not found. Ensure Android SDK and Gradle are set up correctly. Details: {e}")
            raise
        except subprocess.CalledProcessError as e:
            print(f"Error during Gradle build process:")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return Code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            raise
        finally:
            # Return to the original directory
            os.chdir(original_dir)

# Example Usage (for demonstration purposes, not part of the final output)
if __name__ == "__main__":
    # Define some constants for the demo
    DEMO_KNOWLEDGE_BASE_DIR = "./mock_kb"
    DEMO_TEMP_PROJECT_DIR = "./temp_project_build"
    DEMO_APK_OUTPUT_DIR = "./apk_output"

    # Clean up previous runs
    if os.path.exists(DEMO_TEMP_PROJECT_DIR):
        shutil.rmtree(DEMO_TEMP_PROJECT_DIR)
    if os.path.exists(DEMO_APK_OUTPUT_DIR):
        shutil.rmtree(DEMO_APK_OUTPUT_DIR)

    os.makedirs(DEMO_KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(DEMO_TEMP_PROJECT_DIR, exist_ok=True)
    os.makedirs(DEMO_APK_OUTPUT_DIR, exist_ok=True)

    # --- Mocking Language Lobe Output ---
    mock_arabic_prompt = "أنشئ تطبيقًا جديدًا باسم 'حاسبة بسيطة'. اسم الحزمة يجب أن يكون com.example.simplecalculator. هذا التطبيق يقوم بعمليات الجمع والطرح."
    print(f"--- Simulating Lobe 0_language_lobe processing prompt: '{mock_arabic_prompt}' ---")

    nlp_processor = ArabicNLPProcessor(DEMO_KNOWLEDGE_BASE_DIR)
    extracted_package = nlp_processor.extract_package_name_from_text(mock_arabic_prompt)
    generated_app_name = nlp_processor.generate_app_name_from_text(mock_arabic_prompt)
    cleaned_text = nlp_processor.clean_arabic_text(mock_arabic_prompt)
    print(f"Cleaned Arabic text: {cleaned_text}")

    # --- Simulating Code Generation ---
    print("\n--- Initiating Lobe 4_code_generation_lobe ---")
    if extracted_package and generated_app_name:
        code_generator = CodeGenerator(DEMO_TEMP_PROJECT_DIR)
        project_path = code_generator.create_android_project_structure(extracted_package, generated_app_name)

        # --- Simulating APK Compilation ---
        print("\n--- Initiating Lobe 8_apk_compiler_lobe ---")
        try:
            final_apk_path = code_generator.build_apk(project_path, DEMO_APK_OUTPUT_DIR)
            print(f"\n--- Lobe 8_apk_compiler_lobe Finished. APK generated at: {final_apk_path} ---")
        except Exception as e:
            print(f"\n--- Lobe 8_apk_compiler_lobe encountered an error: {e} ---")
            print("APK build failed. Ensure you have Android SDK and Gradle configured correctly.")
            print("You might need to manually create a 'gradlew' script and 'settings.gradle' file in the project root.")
            print("Also, ensure that 'app/build.gradle' has the correct configuration.")
    else:
        print("\nSkipping APK build due to missing package name or app name.")

    print("\n--- Full Demo Simulation Finished ---")

    # Clean up dummy directories
    print("\n--- Cleaning up demo directories ---")
    if os.path.exists(DEMO_TEMP_PROJECT_DIR):
        shutil.rmtree(DEMO_TEMP_PROJECT_DIR)
        print(f"Removed: {DEMO_TEMP_PROJECT_DIR}")
    if os.path.exists(DEMO_APK_OUTPUT_DIR):
        shutil.rmtree(DEMO_APK_OUTPUT_DIR)
        print(f"Removed: {DEMO_APK_OUTPUT_DIR}")
    if os.path.exists(DEMO_KNOWLEDGE_BASE_DIR):
        shutil.rmtree(DEMO_KNOWLEDGE_BASE_DIR)
        print(f"Removed: {DEMO_KNOWLEDGE_BASE_DIR}")