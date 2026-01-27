import os
import subprocess
import re
from pathlib import Path

# --- Constants ---
PROJECT_ROOT = Path(__file__).parent.parent
APKS_DIR = PROJECT_ROOT / "generated_apks"
JAVA_SOURCE_DIR = PROJECT_ROOT / "generated_java_source"
ANDROID_MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

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

# --- Lobe 0: Arabic NLP and APK Structure Generation ---

class ArabicNLPProcessor:
    """
    Processes Arabic natural language to extract intents and parameters
    for generating Android application structures.
    """
    def __init__(self):
        self.intent_patterns = {
            "create_app": re.compile(r"أنشئ تطبيقاً باسم (.*)"),
            "add_activity": re.compile(r"أضف شاشة باسم (.*?) إلى التطبيق"),
            "set_package_name": re.compile(r"اسم الحزمة هو (.*)"),
            "set_app_name": re.compile(r"اسم التطبيق هو (.*)"),
            "add_button": re.compile(r"أضف زر (.*?) إلى شاشة (.*?)"),
            "add_text_view": re.compile(r"أضف نص (.*?) إلى شاشة (.*?)"),
        }
        self.current_app_config = {}
        self.current_activity_config = {}

    def parse_arabic_command(self, command: str) -> dict:
        """
        Parses an Arabic command to identify intent and extract parameters.
        """
        for intent, pattern in self.intent_patterns.items():
            match = pattern.search(command)
            if match:
                params = match.groups()
                return {"intent": intent, "params": params}
        return {"intent": "unknown", "params": None}

    def process_commands(self, commands: list[str]) -> dict:
        """
        Processes a list of Arabic commands to build an app configuration.
        """
        for command in commands:
            parsed_command = self.parse_arabic_command(command)
            intent = parsed_command["intent"]
            params = parsed_command["params"]

            if intent == "create_app":
                app_name = params[0] if params else "MyAwesomeApp"
                self.current_app_config = {
                    "app_name": app_name,
                    "package_name": f"com.example.{app_name.lower().replace(' ', '')}",
                    "activities": {},
                    "strings": {"app_name": app_name}
                }
                print(f"Initialized app: {app_name}")
            elif intent == "set_package_name" and self.current_app_config:
                self.current_app_config["package_name"] = params[0] if params else self.current_app_config.get("package_name")
                print(f"Set package name to: {self.current_app_config['package_name']}")
            elif intent == "set_app_name" and self.current_app_config:
                app_name = params[0] if params else self.current_app_config.get("app_name")
                self.current_app_config["app_name"] = app_name
                self.current_app_config["strings"]["app_name"] = app_name
                print(f"Set app name to: {app_name}")
            elif intent == "add_activity" and self.current_app_config:
                activity_name = params[0] if params else "NewActivity"
                self.current_activity_config = {
                    "name": activity_name,
                    "layout_elements": []
                }
                self.current_app_config["activities"][activity_name] = self.current_activity_config
                print(f"Added activity: {activity_name}")
            elif intent == "add_button" and self.current_app_config and self.current_activity_config:
                button_text, target_activity = params if params and len(params) == 2 else ("New Button", self.current_activity_config["name"])
                if target_activity == self.current_activity_config["name"]:
                    self.current_activity_config["layout_elements"].append({"type": "button", "text": button_text})
                    print(f"Added button '{button_text}' to activity '{target_activity}'")
                else:
                    print(f"Cannot add button to non-current activity '{target_activity}'. Current is '{self.current_activity_config['name']}'.")
            elif intent == "add_text_view" and self.current_app_config and self.current_activity_config:
                text_content, target_activity = params if params and len(params) == 2 else ("Hello World", self.current_activity_config["name"])
                if target_activity == self.current_activity_config["name"]:
                    self.current_activity_config["layout_elements"].append({"type": "text_view", "text": text_content})
                    print(f"Added text view '{text_content}' to activity '{target_activity}'")
                else:
                    print(f"Cannot add text view to non-current activity '{target_activity}'. Current is '{self.current_activity_config['name']}'.")
            else:
                print(f"Command not understood or context missing: {command}")
        return self.current_app_config

class APKStructureGenerator:
    """
    Generates the necessary Android project structure based on the app configuration.
    """
    def __init__(self, app_config: dict):
        self.app_config = app_config
        self.package_name = app_config.get("package_name", "com.example.defaultapp")
        self.app_name = app_config.get("app_name", "DefaultApp")
        self.project_dir = JAVA_SOURCE_DIR / self.app_name.lower().replace(" ", "_")
        self.package_path = Path(*self.package_name.split('.'))
        self.src_main_java_dir = self.project_dir / "app" / "src" / "main" / "java" / self.package_path
        self.res_layout_dir = self.project_dir / "app" / "src" / "main" / "res" / "layout"
        self.res_values_dir = self.project_dir / "app" / "src" / "main" / "res" / "values"
        self.manifest_path = self.project_dir / "app" / "src" / "main" / "AndroidManifest.xml"

    def create_project_directories(self):
        """
        Creates the directory structure for the Android project.
        """
        print(f"Creating project directory: {self.project_dir}")
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.src_main_java_dir.mkdir(parents=True, exist_ok=True)
        self.res_layout_dir.mkdir(parents=True, exist_ok=True)
        self.res_values_dir.mkdir(parents=True, exist_ok=True)

    def generate_manifest(self):
        """
        Generates the AndroidManifest.xml file.
        """
        print(f"Generating AndroidManifest.xml at: {self.manifest_path}")
        manifest_content = ANDROID_MANIFEST_TEMPLATE.format(package_name=self.package_name)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

    def generate_layout_file(self, activity_name: str, elements: list):
        """
        Generates a layout XML file for a given activity.
        """
        layout_filename = f"activity_{activity_name.lower()}.xml"
        layout_path = self.res_layout_dir / layout_filename
        print(f"Generating layout file: {layout_path}")

        layout_content = '<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent">\n'

        y_offset = 50
        for i, element in enumerate(elements):
            element_type = element["type"]
            element_text = element.get("text", "Element")
            element_id = f"{element_type}_{i+1}"
            layout_params = f'android:layout_width="wrap_content" android:layout_height="wrap_content" android:id="@+id/{element_id}"'
            constraint_params = 'app:layout_constraintTop_toTopOf="parent"'

            if element_type == "button":
                layout_content += f'    <Button {layout_params} {constraint_params} android:text="{element_text}" app:layout_constraintStart_toStartOf="parent" android:layout_marginStart="16dp" app:layout_constraintTop_toTopOf="parent" android:layout_marginTop="{y_offset}dp"/>\n'
            elif element_type == "text_view":
                layout_content += f'    <TextView {layout_params} {constraint_params} android:text="{element_text}" app:layout_constraintStart_toStartOf="parent" android:layout_marginStart="16dp" android:layout_marginTop="{y_offset}dp"/>\n'
            y_offset += 80 # Simple offset for element placement

        layout_content += '</androidx.constraintlayout.widget.ConstraintLayout>'

        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content)

    def generate_string_resources(self):
        """
        Generates the strings.xml file.
        """
        strings_path = self.res_values_dir / "strings.xml"
        print(f"Generating strings.xml at: {strings_path}")

        string_content = '<resources>\n'
        for key, value in self.app_config.get("strings", {}).items():
            string_content += f'    <string name="{key}">{value}</string>\n'
        string_content += '</resources>'

        with open(strings_path, "w", encoding="utf-8") as f:
            f.write(string_content)

    def generate_activity_java_files(self):
        """
        Generates basic Java activity files.
        """
        for activity_name, activity_config in self.app_config.get("activities", {}).items():
            activity_filename = f"{activity_name}.java"
            activity_path = self.src_main_java_dir / activity_filename
            print(f"Generating Java activity file: {activity_path}")

            java_content = f"""package {self.package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()});
    }}
}}
"""
            with open(activity_path, "w", encoding="utf-8") as f:
                f.write(java_content)

    def build_structure(self):
        """
        Orchestrates the generation of the entire Android project structure.
        """
        print("\n--- Initiating APK Structure Generation ---")
        self.create_project_directories()
        self.generate_manifest()
        self.generate_string_resources()

        if not self.app_config.get("activities"):
            print("No activities defined. Creating a default MainActivity.")
            self.app_config["activities"] = {"MainActivity": {"layout_elements": []}}

        for activity_name, activity_config in self.app_config.get("activities", {}).items():
            self.generate_layout_file(activity_name, activity_config.get("layout_elements", []))

        self.generate_activity_java_files()
        print("\n--- APK Structure Generation Complete ---")

# --- Lobe 4: Code Generation (Placeholder for actual Java/Kotlin generation logic) ---

class CodeGenerator:
    """
    Placeholder for the code generation lobe.
    In a real scenario, this would generate Java/Kotlin source code
    and potentially a basic Gradle build file.
    """
    def __init__(self, app_config: dict):
        self.app_config = app_config
        self.project_root = JAVA_SOURCE_DIR / self.app_config.get("app_name", "default_app").lower().replace(" ", "_")

    def generate_code(self):
        """
        Simulates code generation. In reality, this would produce actual
        source files and build scripts.
        """
        print("\n--- Initiating Code Generation (Simulated) ---")
        if not self.project_root.exists():
            print(f"Project root '{self.project_root}' does not exist. Skipping simulated code generation.")
            return False

        # Simulate creation of some dummy source files
        (self.project_root / "app" / "build.gradle").touch()
        (self.project_root / "app" / "src" / "main" / "java" / "com" / "example" / "dummy").mkdir(parents=True, exist_ok=True)
        (self.project_root / "app" / "src" / "main" / "java" / "com" / "example" / "dummy" / "DummyClass.java").touch()

        print("Simulated code generation: Created dummy build.gradle and DummyClass.java")
        print("\n--- Code Generation Complete (Simulated) ---")
        return True

# --- Lobe 8: APK Compiler ---

class APKCompiler:
    """
    Simulates the APK compilation process using Android build tools.
    Requires Android SDK and Gradle to be installed and configured.
    """
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.apk_output_dir = APKS_DIR / self.project_dir.name
        self.apk_output_dir.mkdir(parents=True, exist_ok=True)

    def compile_apk(self) -> Path | None:
        """
        Attempts to compile the Android project into an APK.
        This is a simulated process and relies on external tools.
        """
        print("\n--- Initiating APK Compilation (Simulated) ---")
        if not self.project_dir.exists():
            print(f"Project directory '{self.project_dir}' not found. Cannot compile.")
            return None

        print(f"Attempting to build APK for project at: {self.project_dir}")
        # In a real scenario, this would involve running Gradle commands:
        # command = ["gradlew", "assembleDebug", "-p", str(self.project_dir / "app")]
        # try:
        #     subprocess.run(command, cwd=str(self.project_dir), check=True, capture_output=True, text=True)
        #     print("Gradle build successful.")
        # except subprocess.CalledProcessError as e:
        #     print(f"Gradle build failed: {e}")
        #     print(f"Stderr: {e.stderr}")
        #     return None
        # except FileNotFoundError:
        #     print("Error: gradlew not found. Ensure Android SDK and Gradle are configured correctly.")
        #     return None

        # --- Simulated compilation ---
        print("Simulating APK compilation...")
        simulated_apk_path = self.apk_output_dir / f"{self.project_dir.name}-debug.apk"
        try:
            with open(simulated_apk_path, "w") as f:
                f.write("This is a simulated APK file.\n")
            print(f"Simulated APK created at: {simulated_apk_path}")
            print("\n--- APK Compilation Complete (Simulated) ---")
            return simulated_apk_path
        except Exception as e:
            print(f"Error during simulated APK creation: {e}")
            return None

# --- Orchestration and Integration ---

def generate_apk_from_arabic(arabic_commands: list[str]) -> Path | None:
    """
    Orchestrates the process of generating an APK from Arabic natural language commands.
    """
    print("\n--- Starting Grand Objective Component: Arabic NLP to APK Generation ---")

    # Lobe 0: Arabic NLP Processing
    nlp_processor = ArabicNLPProcessor()
    app_config = nlp_processor.process_commands(arabic_commands)

    if not app_config or not app_config.get("app_name"):
        print("Failed to generate app configuration from Arabic commands. Aborting.")
        return None

    print(f"\nGenerated App Configuration: {app_config}")

    # Lobe 6 (implicitly calls Lobe 0): APK Structure Generation
    apk_generator = APKStructureGenerator(app_config)
    apk_generator.build_structure()

    # Lobe 4: Code Generation (Simulated)
    code_gen = CodeGenerator(app_config)
    code_generated_successfully = code_gen.generate_code()

    if not code_generated_successfully:
        print("Simulated code generation failed. Cannot proceed to compilation.")
        return None

    # Lobe 8: APK Compiler (Simulated)
    compiler = APKCompiler(code_gen.project_root)
    compiled_apk_path = compiler.compile_apk()

    print("\n--- Grand Objective Component: Arabic NLP to APK Generation Complete ---")
    return compiled_apk_path

if __name__ == "__main__":
    # Example Usage
    arabic_input = [
        "أنشئ تطبيقاً باسم رحلة سعيدة",
        "اسم الحزمة هو com.example.happyjourney",
        "أضف شاشة باسم معلومات الرحلة",
        "أضف نص رحلتك تبدأ هنا! إلى شاشة معلومات الرحلة",
        "أضف زر ابدأ إلى شاشة معلومات الرحلة",
        "أضف شاشة باسم خيارات الرحلة",
        "أضف نص اختر وجهتك إلى شاشة خيارات الرحلة",
    ]

    print("--- Testing Arabic NLP and APK Structure Generation ---")
    generated_apk = generate_apk_from_arabic(arabic_input)

    if generated_apk:
        print(f"\nSuccessfully generated APK: {generated_apk}")
    else:
        print("\nFailed to generate APK.")

    # Clean up dummy files and directories
    print("\n--- Cleaning up generated project directories and APKs ---")
    import shutil

    def cleanup_generated_dirs():
        for dir_to_clean in [JAVA_SOURCE_DIR, APKS_DIR]:
            if dir_to_clean.exists():
                try:
                    shutil.rmtree(dir_to_clean)
                    print(f"Cleaned up: {dir_to_clean}")
                except OSError as e:
                    print(f"Error cleaning up {dir_to_clean}: {e}")

    cleanup_generated_dirs()
    print("\n--- Demo Finished ---")