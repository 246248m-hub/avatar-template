import os
import shutil
import subprocess
import sys
import json
from pathlib import Path

# Define constants for project structure and file names
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
APP_NAME = "GeneratedApp"
MANIFEST_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml"
BUILD_GRADLE_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle"
MAIN_ACTIVITY_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "generatedapp" / "MainActivity.java"
RES_LAYOUT_MAIN_PATH = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"

# --- Lobe 0_language_lobe Integration ---
# Assuming language_lobe provides a function to process natural language into structured data.
# For this example, we'll mock its output.
def process_natural_language_to_structure(prompt: str) -> dict:
    """
    Mocks the output of Lobe 0_language_lobe.
    In a real scenario, this would involve NLP processing.
    """
    # This is a simplified example. Real output would be more complex.
    if "create an app with a button that says 'Hello World'" in prompt.lower():
        return {
            "app_name": "HelloWorldApp",
            "ui_elements": [
                {"type": "button", "text": "Hello World", "id": "helloButton"}
            ],
            "logic": {
                "button_click": {
                    "action": "show_toast",
                    "message": "Hello from the button!"
                }
            }
        }
    elif "create a simple calculator app" in prompt.lower():
        return {
            "app_name": "CalculatorApp",
            "ui_elements": [
                {"type": "EditText", "id": "inputField", "hint": "Enter expression"},
                {"type": "Button", "text": "=", "id": "calculateButton"}
            ],
            "logic": {
                "calculateButton_click": {
                    "action": "evaluate_expression",
                    "input_id": "inputField",
                    "output_id": "resultDisplay" # Assuming a resultDisplay TextView would be added
                }
            }
        }
    else:
        return {
            "app_name": "DefaultApp",
            "ui_elements": [],
            "logic": {}
        }

# --- Lobe 0_arabic_lobe Integration ---
# Assuming arabic_lobe provides functions for text generation and parsing in Arabic.
# For this example, we'll mock its output.
def generate_arabic_text(prompt: str, knowledge_base_dir: Path) -> str:
    """
    Mocks the output of Lobe 0_arabic_lobe for generating Arabic text.
    """
    if "welcome message" in prompt.lower():
        return "مرحباً بك في التطبيق!"
    elif "greeting" in prompt.lower():
        return "السلام عليكم"
    else:
        return "نص عربي افتراضي"

def parse_arabic_text(text: str) -> dict:
    """
    Mocks the output of Lobe 0_arabic_lobe for parsing Arabic text.
    """
    if "مرحباً بك في التطبيق!" in text:
        return {"type": "greeting", "content": "Welcome"}
    elif "السلام عليكم" in text:
        return {"type": "greeting", "content": "Peace be upon you"}
    else:
        return {"type": "unknown", "content": text}

# --- Lobe 12_apk_generator_lobe ---
class APKGeneratorLobe:
    def __init__(self, output_dir: Path = Path("./generated_apks")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.android_sdk_root = os.environ.get("ANDROID_SDK_ROOT")
        if not self.android_sdk_root:
            raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set. Please set it to your Android SDK location.")
        self.build_tools_dir = Path(self.android_sdk_root) / "build-tools"
        self.latest_build_tools = self._get_latest_build_tools()
        if not self.latest_build_tools:
            raise EnvironmentError("No Android build-tools found. Please install them via the SDK Manager.")
        self.aapt_path = self.latest_build_tools / "aapt"
        self.dx_path = self.latest_build_tools / "dx.bat" if sys.platform == "win32" else self.latest_build_tools / "dx"
        self.apksigner_path = Path(self.android_sdk_root) / "build-tools" / self.latest_build_tools.name / "apksigner"
        self.keytool_path = Path(self.android_sdk_root) / "platform-tools" / "keytool"
        self.jks_path = Path("./debug.keystore")

        self.dummy_project_root = Path("./dummy_android_project")

    def _get_latest_build_tools(self) -> Path | None:
        """Finds the latest installed Android build-tools version."""
        build_tools_versions = sorted([d for d in self.build_tools_dir.iterdir() if d.is_dir()], key=lambda x: x.name, reverse=True)
        return build_tools_versions[0] if build_tools_versions else None

    def _run_command(self, command: list[str], cwd: Path | None = None, env: dict | None = None):
        """Runs a command and returns its output and error."""
        print(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            env=env,
            text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Command failed with error code {process.returncode}")
            print(f"Stdout:\n{stdout}")
            print(f"Stderr:\n{stderr}")
            raise RuntimeError(f"Command failed: {' '.join(command)}")
        return stdout, stderr

    def _create_dummy_project_structure(self, app_data: dict):
        """Creates a basic Android project structure from a template."""
        if self.dummy_project_root.exists():
            shutil.rmtree(self.dummy_project_root)
        self.dummy_project_root.mkdir(parents=True)

        # Copy a minimal Android project template
        # In a real scenario, this template would be more robust.
        # For demonstration, we'll create files on the fly.

        project_base = self.dummy_project_root / app_data.get("app_name", APP_NAME)
        project_base.mkdir(parents=True)

        app_module = project_base / "app"
        app_module.mkdir(parents=True)
        app_src = app_module / "src"
        app_src.mkdir(parents=True)
        main_dir = app_src / "main"
        main_dir.mkdir(parents=True)
        java_dir = main_dir / "java" / "com" / "example" / app_data.get("app_name", APP_NAME).lower()
        java_dir.mkdir(parents=True)
        res_dir = main_dir / "res"
        res_layout_dir = res_dir / "layout"
        res_layout_dir.mkdir(parents=True)

        # Create AndroidManifest.xml
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_data.get('app_name', APP_NAME).lower()}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_data.get('app_name', APP_NAME)}">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
        """
        (main_dir / "AndroidManifest.xml").write_text(manifest_content)

        # Create strings.xml
        strings_content = f"""
<resources>
    <string name="app_name">{app_data.get('app_name', APP_NAME)}</string>
    <string name="hello_world">Hello World!</string>
</resources>
        """
        (main_dir / "values" / "strings.xml").mkdir(parents=True, exist_ok=True)
        (main_dir / "values" / "strings.xml").write_text(strings_content)


        # Create build.gradle (simplified)
        build_gradle_content = """
plugins {
    id 'com.android.application'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.generatedapp"
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
}

dependencies {
    // Add necessary dependencies here if needed
}
        """
        (project_base.parent / "build.gradle").write_text(build_gradle_content) # Project level build.gradle
        (app_module / "build.gradle").write_text(build_gradle_content) # App level build.gradle


        # Create MainActivity.java
        activity_name = "MainActivity"
        main_activity_path = java_dir / f"{activity_name}.java"
        package_name = f"com.example.{app_data.get('app_name', APP_NAME).lower()}"

        main_activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;
import android.widget.Button;
import android.view.View;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Add UI element logic here based on app_data
        Button helloButton = findViewById(R.id.helloButton); // Example for HelloWorldApp
        if (helloButton != null) {{
            helloButton.setOnClickListener(new View.OnClickListener() {{
                @Override
                public void onClick(View v) {{
                    Toast.makeText(this@MainActivity, "Hello from the button!", Toast.LENGTH_SHORT).show();
                }}
            }});
        }}

        // More logic can be added here based on app_data['logic']
        // For example, a calculator implementation would go here.
    }}
}}
        """
        main_activity_path.write_text(main_activity_content)

        # Create activity_main.xml
        activity_main_content = """
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <!-- Add UI elements from app_data here -->
    <Button
        android:id="@+id/helloButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me"
        app:layout_constraintTop_toBottomOf="@id/textView"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="20dp"/>

</androidx.constraintlayout.widget.ConstraintLayout>
        """
        (res_layout_dir / "activity_main.xml").write_text(activity_main_content)

        print(f"Dummy Android project created at: {self.dummy_project_root}")

    def _compile_apk(self, app_dir: Path, output_apk_path: Path):
        """Compiles the Android project into an APK."""
        print(f"\n--- Compiling APK for: {app_dir} ---")

        # 1. Compile Java code to Dalvik bytecode (dx tool)
        print("Compiling Java to Dalvik bytecode (dx)...")
        java_files = list(app_dir.rglob("*.java"))
        if not java_files:
            raise FileNotFoundError("No Java files found in the project.")

        classes_dex_path = self.dummy_project_root / "classes.dex"
        # Ensure dx uses the correct classpath. For a simple project, this might be just the source dir.
        # In a real build system (like Gradle), this is handled automatically.
        dx_command = [str(self.dx_path), "--dex", "--output", str(classes_dex_path)] + [str(f) for f in java_files]
        self._run_command(dx_command, cwd=self.dummy_project_root)

        # 2. Compile resources using AAPT (Android Asset Packaging Tool)
        print("Compiling resources with AAPT...")
        resources_dir = app_dir / "src" / "main" / "res"
        assets_dir = app_dir / "src" / "main" / "assets"
        android_manifest = app_dir / "src" / "main" / "AndroidManifest.xml"

        resources_ap_path = self.dummy_project_root / "resources.ap_"
        aapt_command = [
            str(self.aapt_path), "a",
            "-o", str(resources_ap_path),
            str(android_manifest),
            "-S", str(resources_dir),
            "-A", str(assets_dir) if assets_dir.exists() else ""
        ]
        # Filter out empty strings from command if assets_dir doesn't exist
        aapt_command = [arg for arg in aapt_command if arg]
        self._run_command(aapt_command, cwd=self.dummy_project_root)

        # 3. Create unsigned APK
        print("Creating unsigned APK...")
        unsigned_apk_path = self.dummy_project_root / "unsigned.apk"
        apk_tool_command = [
            sys.executable, "-m", "apktool", "build", str(app_dir), "-o", str(unsigned_apk_path), "--only-main-classes"
        ]
        # Using apktool for a more robust build process than manual aapt/dx if available
        try:
            self._run_command(apk_tool_command, cwd=self.dummy_project_root)
        except Exception as e:
            print(f"apktool failed, falling back to manual build steps if possible. Error: {e}")
            # Fallback to manual creation if apktool is not available or fails
            # This part would be more complex, involving zip creation and signing.
            # For simplicity, we'll raise an error if apktool fails and a fallback isn't implemented.
            raise RuntimeError("APK compilation failed. Please ensure 'apktool' is installed and accessible in your PATH, or a manual build fallback is implemented.") from e


        # 4. Sign the APK with a debug key
        print("Signing APK with debug key...")
        if not self.jks_path.exists():
            print("Debug keystore not found. Creating one...")
            keytool_command = [
                str(self.keytool_path), "-genkey", "-v", "-keystore", str(self.jks_path),
                "-alias", "debugkey", "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
                "-dname", "CN=Android Debug,O=Android,C=US", "-storepass", "android", "-keypass", "android"
            ]
            self._run_command(keytool_command)

        apksigner_command = [
            str(self.apksigner_path), "sign",
            "--ks", str(self.jks_path),
            "--ks-key-alias", "debugkey",
            "--ks-pass", "pass:android",
            "--key-pass", "pass:android",
            str(unsigned_apk_path),
            "-o", str(output_apk_path)
        ]
        self._run_command(apksigner_command)

        print(f"APK successfully generated at: {output_apk_path}")

    def generate_apk(self, natural_language_prompt: str, knowledge_base_dir: Path = Path("./knowledge_base")) -> Path:
        """
        Generates an APK from a natural language prompt.
        This function integrates with Lobe 0_language_lobe and Lobe 0_arabic_lobe.
        """
        print(f"\n--- Starting APK Generation for prompt: '{natural_language_prompt}' ---")

        # Step 1: Process natural language into a structured representation (using Lobe 0_language_lobe mock)
        app_structure_data = process_natural_language_to_structure(natural_language_prompt)
        app_name = app_structure_data.get("app_name", APP_NAME)
        print(f"App structure data: {app_structure_data}")

        # Step 2: Incorporate Arabic text generation if specified or inferred
        # This is a placeholder. Real integration would depend on how the prompt implies Arabic content.
        arabic_greeting_prompt = "Provide a welcome message in Arabic."
        arabic_welcome_text = generate_arabic_text(arabic_greeting_prompt, knowledge_base_dir)
        parsed_arabic_text = parse_arabic_text(arabic_welcome_text)
        print(f"Generated Arabic text: '{arabic_welcome_text}' (Parsed: {parsed_arabic_text})")

        # If the prompt suggests UI elements that need Arabic text, map them.
        # For example, if "show a welcome message" implies using the generated Arabic text.
        for element in app_structure_data.get("ui_elements", []):
            if element.get("type") == "TextView" and element.get("text") == "Welcome!": # Example mapping
                element["text"] = arabic_welcome_text

        # Step 3: Create a dummy Android project structure based on the structured data
        self._create_dummy_project_structure(app_structure_data)

        # Step 4: Compile the Android project into an APK
        output_apk_filename = f"{app_name.lower().replace(' ', '_')}.apk"
        output_apk_path = self.output_dir / output_apk_filename

        try:
            self._compile_apk(self.dummy_project_root / app_name, output_apk_path)
            print(f"\n--- APK Generation Successful: {output_apk_path} ---")
            return output_apk_path
        except Exception as e:
            print(f"\n--- APK Generation Failed: {e} ---")
            raise
        finally:
            # Clean up the dummy project
            if self.dummy_project_root.exists():
                print(f"\n--- Cleaning up dummy project directory: {self.dummy_project_root} ---")
                shutil.rmtree(self.dummy_project_root)

if __name__ == '__main__':
    # --- DEMO USAGE ---
    print("--- Lobe 12_apk_generator_lobe Demo ---")

    # Ensure ANDROID_SDK_ROOT is set in your environment
    if not os.environ.get("ANDROID_SDK_ROOT"):
        print("WARNING: ANDROID_SDK_ROOT environment variable is not set.")
        print("Please set it to your Android SDK location (e.g., export ANDROID_SDK_ROOT=/path/to/android-sdk).")
        # sys.exit(1) # Uncomment to exit if not set

    try:
        apk_generator = APKGeneratorLobe()

        # Example 1: Simple app with a button
        prompt_1 = "Create an app with a button that says 'Hello World' and shows a toast when clicked."
        generated_apk_path_1 = apk_generator.generate_apk(prompt_1)
        print(f"\nGenerated APK 1: {generated_apk_path_1}")

        # Example 2: App with Arabic welcome message (simulated integration)
        prompt_2 = "Create a simple app displaying a welcome message."
        generated_apk_path_2 = apk_generator.generate_apk(prompt_2)
        print(f"\nGenerated APK 2: {generated_apk_path_2}")

        # Example 3: A more complex app structure (mocked)
        prompt_3 = "Create a simple calculator app."
        generated_apk_path_3 = apk_generator.generate_apk(prompt_3)
        print(f"\nGenerated APK 3: {generated_apk_path_3}")

    except EnvironmentError as e:
        print(f"Environment error during APK Generator demo: {e}")
    except RuntimeError as e:
        print(f"Runtime error during APK Generator demo: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during APK Generator demo: {e}")

    print("\n--- APK Generator Lobe Demo Finished ---")