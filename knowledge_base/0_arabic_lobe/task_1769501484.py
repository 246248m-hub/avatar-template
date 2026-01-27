import os
import shutil
import re

# Assume these constants are defined elsewhere and represent paths
# For demonstration, we'll define them here.
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"
JAVA_PROJECT_DIR = "generated_android_project"
APK_OUTPUT_DIR = "generated_apks"
KNOWLEDGE_BASE_DIR = "knowledge_base"
ARABIC_GRAMMAR_RULES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_grammar_rules.json")
ARABIC_VOCABULARY_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_vocabulary.json")
DEFAULT_PACKAGE_NAME = "com.example.generatedapp"
DEFAULT_ACTIVITY_NAME = "MainActivity"

class ArabicParser:
    """
    Parses Arabic natural language input into structured data
    suitable for Android project generation.
    """
    def __init__(self, grammar_rules_path=ARABIC_GRAMMAR_RULES_FILE, vocabulary_path=ARABIC_VOCABULARY_FILE):
        self.grammar_rules = self._load_knowledge(grammar_rules_path)
        self.vocabulary = self._load_knowledge(vocabulary_path)
        # Basic tokenization and morphological analysis (simplified)
        self.arabic_regex = re.compile(r'[\u0600-\u06FF]+')

    def _load_knowledge(self, file_path):
        """Loads JSON knowledge base files."""
        # In a real scenario, this would load actual JSON data.
        # For this demo, we'll return dummy data.
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('{}') # Write empty JSON object if file doesn't exist
        return {} # Placeholder for loaded data

    def tokenize_and_analyze(self, text):
        """
        Tokenizes Arabic text and performs a simplified morphological analysis.
        Returns a list of tokens with potential semantic tags.
        """
        tokens = self.arabic_regex.findall(text)
        analyzed_tokens = []
        for token in tokens:
            # Simplified analysis: look for keywords in vocabulary
            tag = "unknown"
            for word, info in self.vocabulary.items():
                if token == word:
                    tag = info.get("type", "unknown")
                    break
            analyzed_tokens.append({"token": token, "tag": tag})
        return analyzed_tokens

    def parse_nlp_input(self, nl_input: str) -> dict:
        """
        Parses Arabic natural language input to extract project configuration.
        Example: "أنشئ تطبيق أندرويد باسم 'تطبيقي الأول' مع شاشة رئيسية تسمى 'الشاشة الرئيسية'"
        (Create an Android app named 'My First App' with a main screen called 'Main Screen')

        Returns a dictionary containing parsed project details.
        """
        parsed_data = {
            "package_name": DEFAULT_PACKAGE_NAME,
            "activity_name": DEFAULT_ACTIVITY_NAME,
            "app_name": None,
            "ui_elements": [],
            "permissions": []
        }

        analyzed_tokens = self.tokenize_and_analyze(nl_input)

        # Simplified parsing logic based on keywords and patterns
        app_name_found = False
        activity_name_found = False

        for i, token_info in enumerate(analyzed_tokens):
            token = token_info["token"]
            tag = token_info["tag"]

            if token == "أنشئ" and tag == "verb":
                # Look for "تطبيق أندرويد" (Android application)
                if i + 2 < len(analyzed_tokens) and analyzed_tokens[i+1]["token"] == "تطبيق" and analyzed_tokens[i+2]["token"] == "أندرويد":
                    # Look for app name specified with "باسم" (named)
                    if i + 4 < len(analyzed_tokens) and analyzed_tokens[i+4]["token"] == "باسم":
                        # Extract app name from quotes or following words
                        potential_app_name = []
                        for j in range(i + 5, len(analyzed_tokens)):
                            if analyzed_tokens[j]["token"] == "مع" or analyzed_tokens[j]["token"] == "بـ":
                                break
                            if analyzed_tokens[j]["token"].startswith("'") and analyzed_tokens[j]["token"].endswith("'"):
                                potential_app_name.append(analyzed_tokens[j]["token"][1:-1])
                            elif analyzed_tokens[j]["token"] not in ["و", "ثم"]: # Ignore conjunctions
                                potential_app_name.append(analyzed_tokens[j]["token"])
                        if potential_app_name:
                            parsed_data["app_name"] = " ".join(potential_app_name)
                            app_name_found = True

                # Look for a primary activity name if not specified with app name
                if not app_name_found and i + 2 < len(analyzed_tokens) and analyzed_tokens[i+2]["token"] == "باسم":
                    potential_activity_name = []
                    for j in range(i + 3, len(analyzed_tokens)):
                        if analyzed_tokens[j]["token"] == "و" or analyzed_tokens[j]["token"] == "ثم":
                            break
                        if analyzed_tokens[j]["token"].startswith("'") and analyzed_tokens[j]["token"].endswith("'"):
                            potential_activity_name.append(analyzed_tokens[j]["token"][1:-1])
                        elif analyzed_tokens[j]["token"] not in ["و", "ثم"]:
                            potential_activity_name.append(analyzed_tokens[j]["token"])
                    if potential_activity_name:
                        parsed_data["activity_name"] = " ".join(potential_activity_name)
                        activity_name_found = True


            elif token == "مع" and tag == "preposition":
                # Look for UI elements or permissions following "مع"
                if i + 1 < len(analyzed_tokens):
                    next_token_info = analyzed_tokens[i+1]
                    if next_token_info["tag"] == "noun":
                        # Example: "مع شاشة رئيسية" (with a main screen)
                        if next_token_info["token"] == "شاشة":
                            if i + 2 < len(analyzed_tokens) and analyzed_tokens[i+2]["token"] == "رئيسية":
                                parsed_data["ui_elements"].append({"type": "activity", "name": "MainActivity", "is_main": True})
                                activity_name_found = True
                        # Example: "مع أذونات الكاميرا" (with camera permissions)
                        elif next_token_info["token"] == "أذونات":
                            if i + 2 < len(analyzed_tokens) and analyzed_tokens[i+2]["tag"] == "noun":
                                parsed_data["permissions"].append(f"android.permission.{analyzed_tokens[i+2]['token'].upper()}")

            elif token == "بـ" and tag == "preposition":
                # Look for activity name if not already found, e.g., "بـ 'الشاشة الرئيسية'"
                if not activity_name_found and i + 1 < len(analyzed_tokens) and analyzed_tokens[i+1]["token"].startswith("'") and analyzed_tokens[i+1]["token"].endswith("'"):
                    parsed_data["activity_name"] = analyzed_tokens[i+1]["token"][1:-1]
                    activity_name_found = True

        # Post-processing and defaults
        if not parsed_data["app_name"]:
            parsed_data["app_name"] = "GeneratedApp" # Default app name if not specified
        if not parsed_data["activity_name"]:
            parsed_data["activity_name"] = "MainActivity" # Default activity name

        # Ensure main activity is present if none was explicitly defined as main
        if not any(elem.get("is_main") for elem in parsed_data["ui_elements"]):
            parsed_data["ui_elements"].insert(0, {"type": "activity", "name": parsed_data["activity_name"], "is_main": True})

        return parsed_data

class ArabicAPKCompilerLobe:
    """
    Lobe responsible for taking parsed NLP input and generating an Android APK structure.
    """
    def __init__(self, template_dir=ANDROID_PROJECT_TEMPLATE_DIR, project_dir=JAVA_PROJECT_DIR, output_dir=APK_OUTPUT_DIR):
        self.template_dir = template_dir
        self.project_dir = project_dir
        self.output_dir = output_dir
        self.arabic_parser = ArabicParser()

        os.makedirs(self.output_dir, exist_ok=True)

    def create_android_project_structure(self, parsed_config: dict) -> str:
        """
        Creates the directory structure and initial files for an Android project
        based on the parsed configuration.
        """
        app_name = parsed_config.get("app_name", "GeneratedApp")
        package_name = parsed_config.get("package_name", DEFAULT_PACKAGE_NAME)
        activity_name = parsed_config.get("activity_name", "MainActivity")
        permissions = parsed_config.get("permissions", [])
        ui_elements = parsed_config.get("ui_elements", [])

        # Clean up previous project if it exists
        if os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)
        os.makedirs(self.project_dir)

        # Create the basic Android project structure (simplified)
        src_dir = os.path.join(self.project_dir, "app", "src", "main")
        java_dir = os.path.join(src_dir, "java")
        res_dir = os.path.join(src_dir, "res")
        manifest_path = os.path.join(src_dir, "AndroidManifest.xml")
        gradle_build_path = os.path.join(self.project_dir, "build.gradle")
        app_gradle_path = os.path.join(self.project_dir, "app", "build.gradle")

        os.makedirs(java_dir, exist_ok=True)
        os.makedirs(res_dir, exist_ok=True)

        # Create package directory
        package_path = os.path.join(java_dir, *package_name.split('.'))
        os.makedirs(package_path, exist_ok=True)

        # Create main activity file
        activity_file_path = os.path.join(package_path, f"{activity_name}.java")
        self._create_activity_file(activity_file_path, package_name, activity_name, ui_elements)

        # Create layout file for the main activity
        layout_dir = os.path.join(res_dir, "layout")
        os.makedirs(layout_dir, exist_ok=True)
        layout_name = f"activity_{activity_name.lower()}"
        self._create_layout_file(os.path.join(layout_dir, f"{layout_name}.xml"), activity_name)

        # Create AndroidManifest.xml
        self._create_manifest_file(manifest_path, package_name, activity_name, permissions)

        # Create dummy build.gradle files (very simplified)
        with open(gradle_build_path, "w", encoding="utf-8") as f:
            f.write('buildscript {\n    repositories {\n        google()\n        mavenCentral()\n    }\n    dependencies {\n        classpath "com.android.tools.build:gradle:7.0.0" # Example version\n    }\n}\n\ntasks.register("clean", Delete) {\n    delete rootProject.buildDir\n}\n')
        with open(app_gradle_path, "w", encoding="utf-8") as f:
            f.write('plugins { id "com.android.application" }\n\nandroid {\n    compileSdk 32 # Example SDK version\n    defaultConfig {\n        applicationId "'+ package_name +'"\n        minSdk 21\n        targetSdk 32\n        versionCode 1\n        versionName "1.0"\n    }\n    buildTypes {\n        release {\n            minifyEnabled false\n            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"\n        }\n    }\n    compileOptions {\n        sourceCompatibility JavaVersion.VERSION_1_8\n        targetCompatibility JavaVersion.VERSION_1_8\n    }\n}\n\ndependencies {\n    implementation "androidx.core:core-ktx:1.6.0"\n    implementation "androidx.appcompat:appcompat:1.3.1"\n    implementation "com.google.android.material:material:1.4.0"\n    implementation "androidx.constraintlayout:constraintlayout:2.1.1"\n}\n')

        print(f"Android project structure created at: {self.project_dir}")
        return self.project_dir

    def _create_activity_file(self, file_path: str, package_name: str, activity_name: str, ui_elements: list):
        """Generates a basic Java Activity file."""
        layout_name = f"activity_{activity_name.lower()}"
        has_main_activity = any(elem.get("is_main") for elem in ui_elements)

        content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Example import

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});

        // Example of accessing a UI element
        // TextView welcomeText = findViewById(R.id.welcome_text);
        // welcomeText.setText("Welcome to {activity_name}!");

        System.out.println("'{activity_name}' created.");
    }}
}}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created activity file: {file_path}")

    def _create_layout_file(self, file_path: str, activity_name: str):
        """Generates a basic XML layout file."""
        # Simple layout with a TextView
        content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello from {activity_name}!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created layout file: {file_path}")

    def _create_manifest_file(self, file_path: str, package_name: str, activity_name: str, permissions: list):
        """Generates a basic AndroidManifest.xml file."""
        permission_declarations = "\n".join([f'    <uses-permission android:name="{perm}" />' for perm in permissions])

        content = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

{permission_declarations}

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp"> {/* Theme name can be dynamic */}

        <activity android:name=".{activity_name}"
            android:exported="true"> {/* Make exported for launch */}
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created AndroidManifest.xml: {file_path}")

    def compile_apk(self, project_path: str) -> str:
        """
        Simulates the compilation of an Android project into an APK.
        In a real scenario, this would involve calling the Android SDK's
        build tools (e.g., Gradle).
        """
        print(f"\n--- Simulating APK compilation for project: {project_path} ---")

        # In a real implementation, you would execute Gradle commands here:
        # subprocess.run(["gradlew", "assembleDebug"], cwd=project_path, check=True)
        # Or for release:
        # subprocess.run(["gradlew", "assembleRelease"], cwd=project_path, check=True)

        # For this demo, we'll just create a dummy APK file.
        dummy_apk_name = f"{os.path.basename(os.path.dirname(project_path))}_debug.apk"
        dummy_apk_path = os.path.join(self.output_dir, dummy_apk_name)

        # Create a dummy APK file
        with open(dummy_apk_path, "w") as f:
            f.write("This is a dummy APK file.\n")
            f.write(f"Project path: {project_path}\n")
            f.write(f"Compiled from project: {os.path.basename(project_path)}\n")

        print(f"Simulated APK generated at: {dummy_apk_path}")
        return dummy_apk_path

    def process_nl_to_apk(self, nl_input: str) -> str:
        """
        Orchestrates the process from natural language input to a generated APK.
        """
        print(f"\n--- Processing Natural Language Input for APK Generation ---")
        print(f"Input: '{nl_input}'")

        # Step 1: Parse the natural language input
        parsed_config = self.arabic_parser.parse_nlp_input(nl_input)
        print(f"Parsed Configuration: {parsed_config}")

        # Step 2: Create the Android project structure
        project_path = self.create_android_project_structure(parsed_config)

        # Step 3: Compile the project into an APK (simulated)
        apk_path = self.compile_apk(project_path)

        print(f"\n--- APK Generation Process Finished ---")
        return apk_path

# Example Usage (for testing the lobe itself)
if __name__ == "__main__":
    # Ensure dummy directories and files exist for the parser to run
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    with open(ARABIC_GRAMMAR_RULES_FILE, "w", encoding="utf-8") as f:
        f.write('{"create": {"verb": "create", "object": "app"}, "named": {"preposition": "named"}}')
    with open(ARABIC_VOCABULARY_FILE, "w", encoding="utf-8") as f:
        f.write('{"تطبيق": {"type": "noun", "meaning": "application"}, "أندرويد": {"type": "noun", "meaning": "android"}, "باسم": {"type": "preposition", "meaning": "named"}, "شاشة": {"type": "noun", "meaning": "screen"}, "رئيسية": {"type": "adjective", "meaning": "main"}, "مع": {"type": "preposition", "meaning": "with"}, "أذونات": {"type": "noun", "meaning": "permissions"}, "الكاميرا": {"type": "noun", "meaning": "camera"}}')

    # Clean up previous runs
    if os.path.exists(JAVA_PROJECT_DIR):
        shutil.rmtree(JAVA_PROJECT_DIR)
    if os.path.exists(APK_OUTPUT_DIR):
        shutil.rmtree(APK_OUTPUT_DIR)

    apk_compiler_lobe = ArabicAPKCompilerLobe()

    # Test case 1: Simple app creation
    nl_input_1 = "أنشئ تطبيق أندرويد باسم 'تطبيقي الأول' مع شاشة رئيسية"
    print(f"\n--- Test Case 1: {nl_input_1} ---")
    generated_apk_1 = apk_compiler_lobe.process_nl_to_apk(nl_input_1)
    print(f"Generated APK path: {generated_apk_1}")

    # Test case 2: App with permissions
    nl_input_2 = "أنشئ تطبيق أندرويد جديد مع أذونات الكاميرا"
    print(f"\n--- Test Case 2: {nl_input_2} ---")
    generated_apk_2 = apk_compiler_lobe.process_nl_to_apk(nl_input_2)
    print(f"Generated APK path: {generated_apk_2}")

    # Test case 3: Explicit activity naming
    nl_input_3 = "أنشئ تطبيق أندرويد باسم 'My App' مع شاشة رئيسية بـ 'الشاشة الرئيسية'"
    print(f"\n--- Test Case 3: {nl_input_3} ---")
    generated_apk_3 = apk_compiler_lobe.process_nl_to_apk(nl_input_3)
    print(f"Generated APK path: {generated_apk_3}")

    # Clean up dummy files generated by the parser for the demo
    print("\n--- Cleaning up dummy knowledge base files ---")
    if os.path.exists(ARABIC_GRAMMAR_RULES_FILE):
        os.remove(ARABIC_GRAMMAR_RULES_FILE)
    if os.path.exists(ARABIC_VOCABULARY_FILE):
        os.remove(ARABIC_VOCABULARY_FILE)
    if os.path.exists(KNOWLEDGE_BASE_DIR) and not os.listdir(KNOWLEDGE_BASE_DIR):
        os.rmdir(KNOWLEDGE_BASE_DIR)

    print("\n--- Arabic APK Compiler Lobe Demo Finished ---")