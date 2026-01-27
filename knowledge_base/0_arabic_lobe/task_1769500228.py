import os
import shutil
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Constants ---
ARABIC_NLP_MODULE_DIR = "arabic_nlp_module"
JAVA_SOURCE_DIR = os.path.join(ARABIC_NLP_MODULE_DIR, "src", "main", "java", "com", "example", "arabicapp")
JAVA_MAIN_ACTIVITY_PATH = os.path.join(JAVA_SOURCE_DIR, "MainActivity.java")
APP_NAME = "ArabicApp"
PACKAGE_NAME = "com.example.arabicapp"

# --- Helper Functions ---

def create_directory_structure():
    """Creates the necessary directory structure for the Java project."""
    logging.info("Creating directory structure for Java project.")
    os.makedirs(JAVA_SOURCE_DIR, exist_ok=True)

def generate_java_code(prompt_text: str) -> str:
    """
    Generates Java code for a simple Android Activity based on natural language input.
    This is a placeholder for a more sophisticated NLP-to-code generation.
    For now, it will create a basic Android Activity structure.
    """
    logging.info(f"Generating Java code for prompt: '{prompt_text}'")

    # Basic template for an Android MainActivity.java
    java_code_template = f"""
package {PACKAGE_NAME};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("Hello from Arabic App! Your input: {prompt_text}");
    }}
}}
"""
    return java_code_template

def create_gradle_files():
    """Creates essential Gradle files for an Android project."""
    logging.info("Creating Gradle files.")
    # Basic build.gradle (app level)
    build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{PACKAGE_NAME}'
    compileSdk 33

    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
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
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "build.gradle"), "w") as f:
        f.write(build_gradle_content)

    # Basic settings.gradle
    settings_gradle_content = f"""
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{APP_NAME}"
include ':app'
"""
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "settings.gradle"), "w") as f:
        f.write(settings_gradle_content)

    # Basic AndroidManifest.xml
    android_manifest_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{APP_NAME}"
        tools:targetApi="31">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    # Create res/values directory and files for strings and themes
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "values"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "values", "strings.xml"), "w") as f:
        f.write('<resources><string name="app_name">ArabicApp</string></resources>')

    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "values", "themes"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "values", "themes", "theme.xml"), "w") as f:
        f.write(f'<resources><style name="Theme.{APP_NAME}" parent="Theme.Material3.DayNight.NoActionBar"><property name="colorPrimary">@color/purple_500</property><property name="colorOnPrimary">@color/white</property><property name="colorSecondary">@color/teal_200</property><property name="colorOnSecondary">@color/black</property></style></resources>')

    # Create res/layout directory and activity_main.xml
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "layout"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "layout", "activity_main.xml"), "w") as f:
        f.write(f'<resources><androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity"><TextView android:id="@+id/textView" android:layout_width="wrap_content" android:layout_height="wrap_content" text="Hello World!" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent" /></androidx.constraintlayout.widget.ConstraintLayout></resources>')

    # Create ic_launcher and ic_launcher_round (placeholders)
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-hdpi"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-hdpi", "ic_launcher.png"), "w") as f:
        f.write("placeholder_ic_launcher") # Dummy file
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-mdpi"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-mdpi", "ic_launcher.png"), "w") as f:
        f.write("placeholder_ic_launcher") # Dummy file
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-xhdpi"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-xhdpi", "ic_launcher.png"), "w") as f:
        f.write("placeholder_ic_launcher") # Dummy file
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-xxhdpi"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-xxhdpi", "ic_launcher.png"), "w") as f:
        f.write("placeholder_ic_launcher") # Dummy file
    os.makedirs(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-xxxhdpi"), exist_ok=True)
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "res", "mipmap-xxxhdpi", "ic_launcher.png"), "w") as f:
        f.write("placeholder_ic_launcher") # Dummy file

    # Create the AndroidManifest.xml file
    with open(os.path.join(ARABIC_NLP_MODULE_DIR, "app", "src", "main", "AndroidManifest.xml"), "w") as f:
        f.write(android_manifest_content)


def clean_up_android_project(project_dir: str):
    """Cleans up generated Android project files."""
    logging.info(f"Cleaning up Android project directory: {project_dir}")
    if os.path.exists(project_dir):
        try:
            shutil.rmtree(project_dir)
            logging.info(f"Successfully removed directory: {project_dir}")
        except OSError as e:
            logging.error(f"Error removing directory {project_dir}: {e}")

class ArabicNLPtoAPKModule:
    """
    This module simulates the process of taking Arabic natural language input,
    processing it with NLP (conceptually), and generating a foundational structure
    for an Android APK.
    """
    def __init__(self):
        self.output_dir = ARABIC_NLP_MODULE_DIR

    def process_arabic_prompt(self, arabic_prompt: str):
        """
        Takes an Arabic natural language prompt, performs (simulated) NLP
        processing, and initiates the Android project structure creation.
        """
        logging.info(f"Received Arabic prompt: '{arabic_prompt}'")
        if not arabic_prompt:
            logging.warning("Arabic prompt is empty. Cannot generate APK structure.")
            return

        # --- Step 1: Simulate Arabic NLP Processing ---
        # In a real scenario, this would involve advanced NLP models to
        # understand intent, extract entities, and determine UI/functionality.
        # For this module, we'll simply use the prompt text as input to the Java code.
        logging.info("Simulating Arabic NLP processing...")
        processed_text_for_code = arabic_prompt # Direct usage for simplicity

        # --- Step 2: Initialize Android Project Structure ---
        logging.info("Initializing Android project structure...")
        self._initialize_android_project(processed_text_for_code)

        logging.info("Arabic NLP to APK structure generation complete.")

    def _initialize_android_project(self, code_input_text: str):
        """
        Creates the basic directory and file structure for an Android application.
        This includes Java source files, Gradle build files, and manifest.
        """
        logging.info("Creating Android project structure...")
        # Clean up any previous runs
        clean_up_android_project(self.output_dir)

        # Create main directories
        create_directory_structure()

        # Generate Java code
        java_code = generate_java_code(code_input_text)
        with open(JAVA_MAIN_ACTIVITY_PATH, "w") as f:
            f.write(java_code)
        logging.info(f"Created Java source file: {JAVA_MAIN_ACTIVITY_PATH}")

        # Create Gradle files and other essential Android resources
        create_gradle_files()

        logging.info(f"Android project structure created in: {self.output_dir}")

    def build_apk(self):
        """
        Attempts to build the APK using Gradle. This requires a JDK and
        Android SDK to be installed and configured on the system.
        """
        logging.info("Attempting to build APK using Gradle...")
        if not os.path.exists(os.path.join(self.output_dir, "build.gradle")):
            logging.error("build.gradle file not found. Cannot build APK.")
            return

        try:
            # Navigate to the project directory and run the Gradle build command
            # This command assumes you have Android SDK and JDK configured in your PATH
            # and that the gradle wrapper (if used) is available.
            # For simplicity, we'll try to use the system's 'gradlew' if available,
            # or fall back to 'gradle' command.
            gradle_command = ["./gradlew", "assembleDebug"]
            if not os.path.exists(os.path.join(self.output_dir, "gradlew")):
                # If gradlew is not present, try using the 'gradle' command directly
                gradle_command = ["gradle", "assembleDebug"]
                logging.warning("gradlew not found, attempting to use 'gradle' command. Ensure Gradle is in your PATH.")

            process = subprocess.run(
                gradle_command,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit code yet
            )

            if process.returncode == 0:
                logging.info("APK build successful!")
                logging.info(f"Gradle Output:\n{process.stdout}")
                # Find the generated APK
                apk_path = None
                for root, dirs, files in os.walk(os.path.join(self.output_dir, "app", "build", "outputs", "apk", "debug")):
                    for file in files:
                        if file.endswith(".apk"):
                            apk_path = os.path.join(root, file)
                            break
                    if apk_path:
                        break
                if apk_path:
                    logging.info(f"Generated APK found at: {apk_path}")
                else:
                    logging.warning("Could not locate the generated APK file.")
            else:
                logging.error("APK build failed!")
                logging.error(f"Gradle Error Code: {process.returncode}")
                logging.error(f"Gradle Output:\n{process.stdout}")
                logging.error(f"Gradle Error Output:\n{process.stderr}")

        except FileNotFoundError:
            logging.error("Gradle command not found. Please ensure Gradle is installed and in your PATH, or that gradlew is available in the project directory.")
        except Exception as e:
            logging.error(f"An error occurred during the APK build process: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    logging.info("--- Arabic NLP to APK Module Demo ---")

    # Instantiate the module
    arabic_nlp_to_apk = ArabicNLPtoAPKModule()

    # Example Arabic prompt
    arabic_prompt = "أريد إنشاء تطبيق يعرض رسالة ترحيبية مع اسمي." # "I want to create an app that displays a welcome message with my name."

    # Process the prompt and generate the initial Android project structure
    arabic_nlp_to_apk.process_arabic_prompt(arabic_prompt)

    # Attempt to build the APK
    # NOTE: This step requires a working Android SDK and JDK installation.
    # It will also try to execute Gradle commands, which might need 'gradlew'
    # to be present or the 'gradle' command to be in the system's PATH.
    # If you don't have these configured, the build_apk() step will likely fail.
    print("\n--- Attempting to build APK (requires JDK and Android SDK) ---")
    arabic_nlp_to_apk.build_apk()
    print("--- APK Build Attempt Finished ---\n")

    # Clean up the generated Android project directory after demonstration
    # print("--- Cleaning up generated Android project ---")
    # clean_up_android_project(ARABIC_NLP_MODULE_DIR)
    # print("--- Cleanup Finished ---")

    print("\n--- Arabic NLP to APK Module Demo Finished ---")