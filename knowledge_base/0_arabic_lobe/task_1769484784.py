import os
import shutil
import subprocess
from pathlib import Path

# --- Constants ---
JAVA_PROJECT_DIR = "generated_android_project"
TEMP_JAVA_FILE = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", "com", "example", "myapp", "MainActivity.java")
MANIFEST_FILE = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "AndroidManifest.xml")
GRADLE_BUILD_FILE = os.path.join(JAVA_PROJECT_DIR, "app", "build.gradle")
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable is not set. Please set it to your Android SDK path.")

ADB_PATH = os.path.join(ANDROID_SDK_ROOT, "platform-tools", "adb")

# --- Lobe 3: Arabic NLP Processing ---

class ArabicNlpProcessor:
    """
    Processes Arabic natural language input to extract intent and parameters
    for APK generation.
    """
    def __init__(self):
        # In a real scenario, this would involve sophisticated NLP models
        # for intent recognition, entity extraction, etc.
        # For this demo, we'll use simple keyword matching.
        pass

    def parse_request(self, natural_language_request: str) -> dict:
        """
        Parses an Arabic natural language request to determine the desired
        APK structure and content.

        Args:
            natural_language_request: The user's request in Arabic.

        Returns:
            A dictionary containing parsed intent and parameters.
        """
        parsed_data = {"intent": "unknown", "parameters": {}}

        if "إنشاء تطبيق بسيط" in natural_language_request:
            parsed_data["intent"] = "create_simple_app"
            if "بعنوان" in natural_language_request:
                title_index = natural_language_request.find("بعنوان") + len("بعنوان")
                title_end_index = natural_language_request.find("و", title_index) if "و" in natural_language_request[title_index:] else len(natural_language_request)
                app_title = natural_language_request[title_index:title_end_index].strip()
                parsed_data["parameters"]["app_title"] = app_title

        elif "تطبيق يعرض نص" in natural_language_request:
            parsed_data["intent"] = "display_text_app"
            if "النص هو" in natural_language_request:
                text_index = natural_language_request.find("النص هو") + len("النص هو")
                displayed_text = natural_language_request[text_index:].strip()
                parsed_data["parameters"]["displayed_text"] = displayed_text
            if "بعنوان" in natural_language_request:
                title_index = natural_language_request.find("بعنوان") + len("بعنوان")
                title_end_index = natural_language_request.find("النص", title_index) if "النص" in natural_language_request[title_index:] else len(natural_language_request)
                app_title = natural_language_request[title_index:title_end_index].strip()
                parsed_data["parameters"]["app_title"] = app_title

        return parsed_data

# --- Lobe 4: Code Generation ---

class CodeGenerator:
    """
    Generates Java code and Android project structure for APKs.
    """
    def __init__(self, project_root: str = JAVA_PROJECT_DIR):
        self.project_root = Path(project_root)
        self.app_dir = self.project_root / "app"
        self.java_dir = self.app_dir / "src" / "main" / "java" / "com" / "example" / "myapp"
        self.res_dir = self.app_dir / "src" / "main" / "res"
        self.layout_dir = self.res_dir / "layout"

    def create_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.app_dir.mkdir(parents=True, exist_ok=True)
        self.java_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir.mkdir(parents=True, exist_ok=True)
        self.layout_dir.mkdir(parents=True, exist_ok=True)

    def generate_java_code(self, app_title: str = "MyApp", displayed_text: str = "Hello, World!") -> str:
        """Generates the MainActivity.java code."""
        package_name = "com.example.myapp"
        class_name = "MainActivity"
        java_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {class_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.text_view);
        textView.setText("{displayed_text}");
        setTitle("{app_title}");
    }}
}}
"""
        return java_code

    def generate_layout_file(self) -> str:
        """Generates the activity_main.xml layout file."""
        layout_xml = """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Default Text"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        return layout_xml

    def generate_manifest_file(self, app_title: str = "My App") -> str:
        """Generates the AndroidManifest.xml file."""
        manifest_xml = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">

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
        # Replace app_name dynamically if needed, though it's often defined in strings.xml
        # For simplicity here, we'll rely on the default app_name.
        return manifest_xml

    def generate_gradle_build_file(self) -> str:
        """Generates a basic app/build.gradle file."""
        gradle_content = """
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.myapp'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
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

    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
        return gradle_content

    def create_apk_project(self, app_title: str, displayed_text: str):
        """
        Creates a complete Android project structure and files for a given app.
        """
        self.create_project_structure()

        # Write Java code
        java_code = self.generate_java_code(app_title=app_title, displayed_text=displayed_text)
        (self.java_dir / "MainActivity.java").write_text(java_code, encoding="utf-8")

        # Write layout file
        layout_xml = self.generate_layout_file()
        (self.layout_dir / "activity_main.xml").write_text(layout_xml, encoding="utf-8")

        # Write manifest file
        manifest_xml = self.generate_manifest_file(app_title=app_title)
        (self.project_root / "app" / "src" / "main" / "AndroidManifest.xml").write_text(manifest_xml, encoding="utf-8")

        # Write build.gradle file
        gradle_build_content = self.generate_gradle_build_file()
        (self.app_dir / "build.gradle").write_text(gradle_build_content, encoding="utf-8")

        # Create a dummy build.gradle for the root project
        (self.project_root / "build.gradle").write_text("plugins { id 'com.android.application' version '8.2.0' apply false }\n", encoding="utf-8")
        # Create a settings.gradle file
        (self.project_root / "settings.gradle").write_text("rootProject.name = \"MyApp\"\ninclude ':app'\n", encoding="utf-8")
        # Create a proguard-rules.pro file (can be empty for demo)
        (self.app_dir / "proguard-rules.pro").write_text("", encoding="utf-8")


# --- Lobe 8: APK Compiler ---

class ApkCompiler:
    """
    Compiles the generated Android project into an APK.
    """
    def __init__(self, project_path: str = JAVA_PROJECT_DIR):
        self.project_path = Path(project_path)
        self.gradle_wrapper_path = self.project_path / "gradlew"

    def _run_command(self, command: list, cwd: str) -> subprocess.CompletedProcess:
        """Helper to run a command and return its output."""
        print(f"Running command: {' '.join(command)} in {cwd}")
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error code {e.returncode}")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            raise

    def build_apk(self) -> Path:
        """
        Builds the APK using Gradle.

        Returns:
            The path to the generated APK file.
        """
        if not self.gradle_wrapper_path.exists():
            # Download Gradle wrapper if it doesn't exist
            print("Gradle wrapper not found. Downloading...")
            download_gradle_cmd = [
                "gradle", "--version" # This command will prompt to download wrapper if missing
            ]
            try:
                self._run_command(download_gradle_cmd, cwd=str(self.project_path))
            except Exception as e:
                print(f"Failed to download or run Gradle wrapper: {e}")
                raise

            # Make gradlew executable on Linux/macOS
            if os.name != 'nt':
                os.chmod(self.gradle_wrapper_path, 0o755)

        # Command to assemble the debug APK
        assemble_debug_command = ["./gradlew", "assembleDebug"]
        self._run_command(assemble_debug_command, cwd=str(self.project_path))

        # Find the generated APK
        # The path to the APK can vary slightly depending on Gradle version and build flavor.
        # For 'assembleDebug', it's typically in app/build/outputs/apk/debug/
        apk_path = self.project_path / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"

        if not apk_path.exists():
            raise FileNotFoundError(f"APK file not found at expected location: {apk_path}")

        return apk_path

    def install_apk(self, apk_path: Path, device_serial: str = None):
        """
        Installs the generated APK on a connected Android device or emulator.

        Args:
            apk_path: The path to the APK file.
            device_serial: The serial number of the target device. If None,
                           adb will choose the default device.
        """
        if not os.path.exists(ADB_PATH):
            raise FileNotFoundError(f"adb executable not found at: {ADB_PATH}")

        command = [ADB_PATH, "install", str(apk_path)]
        if device_serial:
            command.extend(["-s", device_serial])

        self._run_command(command, cwd=str(self.project_path.parent)) # Run from a parent directory
        print(f"APK installed successfully: {apk_path}")

    def uninstall_apk(self, package_name: str = "com.example.myapp", device_serial: str = None):
        """
        Uninstalls an APK from a connected Android device or emulator.

        Args:
            package_name: The package name of the app to uninstall.
            device_serial: The serial number of the target device.
        """
        if not os.path.exists(ADB_PATH):
            raise FileNotFoundError(f"adb executable not found at: {ADB_PATH}")

        command = [ADB_PATH, "uninstall", package_name]
        if device_serial:
            command.extend(["-s", device_serial])

        try:
            self._run_command(command, cwd=str(self.project_path.parent))
            print(f"App uninstalled successfully: {package_name}")
        except subprocess.CalledProcessError as e:
            if "Failure [DELETE_FAILED_INTERNAL_ERROR]" in e.stderr or "does not exist" in e.stderr:
                print(f"App '{package_name}' not found or already uninstalled.")
            else:
                raise


# --- Workflow Integration ---

def generate_apk_code_module_demo():
    """Demonstrates the integration of Arabic NLP and Code Generation for APKs."""
    nlp_processor = ArabicNlpProcessor()
    code_generator = CodeGenerator()

    # Example Arabic requests
    requests = [
        "قم بإنشاء تطبيق بسيط بعنوان 'تطبيقي الأول' ويعرض النص 'أهلاً بالعالم!'",
        "أريد تطبيقاً يعرض النص 'رسالة مهمة' بعنوان 'تنبيه'",
        "إنشاء تطبيق بسيط" # Basic creation, will use defaults
    ]

    for request in requests:
        print(f"\n--- Processing Request: '{request}' ---")
        parsed_data = nlp_processor.parse_request(request)
        print(f"Parsed Data: {parsed_data}")

        intent = parsed_data.get("intent")
        parameters = parsed_data.get("parameters", {})

        if intent == "create_simple_app":
            app_title = parameters.get("app_title", "My Simple App")
            displayed_text = "Welcome!" # Default for simple app
            code_generator.create_apk_project(app_title=app_title, displayed_text=displayed_text)
            print(f"Generated project structure for '{app_title}' with default text.")

        elif intent == "display_text_app":
            app_title = parameters.get("app_title", "Text Display App")
            displayed_text = parameters.get("displayed_text", "No text provided.")
            code_generator.create_apk_project(app_title=app_title, displayed_text=displayed_text)
            print(f"Generated project structure for '{app_title}' displaying '{displayed_text}'.")

        else:
            print("Unknown intent or insufficient parameters.")

    print("\n--- Code Generation Module Demo Finished ---")

def apk_compiler_module_demo():
    """Demonstrates the APK compilation and installation process."""
    # Ensure project exists from previous step or create a dummy one
    if not os.path.exists(JAVA_PROJECT_DIR):
        print("Creating a dummy project for APK compilation demo...")
        dummy_code_generator = CodeGenerator()
        dummy_code_generator.create_apk_project(app_title="DemoApp", displayed_text="Testing compilation")

    compiler = ApkCompiler(project_path=JAVA_PROJECT_DIR)

    try:
        # Clean up any previous installations
        print("\n--- Attempting to uninstall previous version ---")
        compiler.uninstall_apk()

        print("\n--- Building APK ---")
        apk_file_path = compiler.build_apk()
        print(f"APK built successfully: {apk_file_path}")

        print("\n--- Installing APK ---")
        # You might want to specify a device_serial if you have multiple devices/emulators connected
        # For example: compiler.install_apk(apk_file_path, device_serial="emulator-5554")
        compiler.install_apk(apk_file_path)
        print("APK installed successfully.")

    except Exception as e:
        print(f"\n--- APK Compilation/Installation Failed ---")
        print(f"Error: {e}")

    finally:
        # Optional: Clean up the generated project directory after demo
        # print("\n--- Cleaning up generated project directory ---")
        # if os.path.exists(JAVA_PROJECT_DIR):
        #     shutil.rmtree(JAVA_PROJECT_DIR)
        #     print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")
        pass


# --- Main Workflow ---

def main_workflow():
    """
    Executes the grand objective workflow:
    1. Parse Arabic NLP requests.
    2. Generate code for Android APKs based on parsed requests.
    3. Compile the generated code into an APK.
    """

    # Lobe 3: Arabic NLP Processor (simulated)
    print("--- Initiating Lobe 3: Arabic NLP Processor ---")
    nlp_processor = ArabicNlpProcessor()
    # Example Arabic request for demonstration
    arabic_request = "أريد تطبيقاً بسيطاً يعرض النص 'مرحباً بكم في العالم الرقمي' ويكون عنوانه 'تطبيقي الجديد'."
    parsed_data = nlp_processor.parse_request(arabic_request)
    print(f"Input Arabic Request: '{arabic_request}'")
    print(f"Parsed Data: {parsed_data}")

    # Lobe 4: Code Generation Lobe (simulated integration)
    print("\n--- Initiating Lobe 4: Code Generation Lobe ---")
    if parsed_data["intent"] in ["create_simple_app", "display_text_app"]:
        app_title = parsed_data["parameters"].get("app_title", "My App")
        displayed_text = parsed_data["parameters"].get("displayed_text", "Hello, World!")
        code_generator = CodeGenerator()
        code_generator.create_apk_project(app_title=app_title, displayed_text=displayed_text)
        print(f"Successfully generated Android project structure for '{app_title}' at '{JAVA_PROJECT_DIR}'.")
    else:
        print("Could not generate code due to unknown intent or missing parameters.")

    # Lobe 8: APK Compiler Lobe (simulated integration)
    print("\n--- Initiating Lobe 8: APK Compiler Lobe ---")
    if os.path.exists(JAVA_PROJECT_DIR):
        apk_compiler = ApkCompiler(project_path=JAVA_PROJECT_DIR)
        try:
            # Uninstall previous version if it exists
            apk_compiler.uninstall_apk()
            # Build the APK
            apk_path = apk_compiler.build_apk()
            print(f"APK generated successfully: {apk_path}")
            # Install the APK (optional, uncomment to install)
            # apk_compiler.install_apk(apk_path)
            # print("APK installed on device/emulator.")
        except Exception as e:
            print(f"Error during APK compilation or installation: {e}")
    else:
        print("Skipping APK compilation as project directory was not created.")

    print("\n--- Unified Mind Evolution Process Simulated ---")

if __name__ == "__main__":
    # To run the full demo, ensure you have:
    # 1. Android SDK installed and ANDROID_SDK_ROOT environment variable set.
    # 2. Gradle installed (or it will be downloaded by the wrapper).
    # 3. A connected Android device or running emulator.

    # Example of how to run specific lobe demos:
    # generate_apk_code_module_demo()
    # apk_compiler_module_demo()

    # Run the main workflow to simulate the integrated process
    main_workflow()