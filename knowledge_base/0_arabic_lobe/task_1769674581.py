import os
import json
import shutil
from pathlib import Path

# Assume these exist and are accessible
from lobe_0_language_lobe import ArabicLanguageModel
from lobe_8_apk_compiler_lobe import ApkCompilerLobe

# Mock data structures for demonstration
class MockArabicParser:
    def parse(self, text):
        print(f"Mock parsing: {text}")
        # Simulate parsing Arabic text into a structured representation
        if "بناء تطبيق" in text:
            return {"action": "build_app", "app_name": text.split("بناء تطبيق")[-1].strip(), "features": []}
        elif "إضافة ميزة" in text:
            return {"action": "add_feature", "feature_name": text.split("إضافة ميزة")[-1].strip()}
        return {"action": "unknown", "original_text": text}

class MockFeatureGenerator:
    def generate_code_for_feature(self, feature_data):
        print(f"Mock generating code for feature: {feature_data}")
        # Simulate generating placeholder code for a feature
        return f"// Placeholder code for {feature_data['feature_name']}\n"

class MockAndroidManifestGenerator:
    def generate_manifest(self, app_name, features):
        print(f"Mock generating AndroidManifest.xml for {app_name} with features: {features}")
        # Simulate generating a basic AndroidManifest.xml
        manifest_content = f"""<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.{app_name.lower().replace(' ', '')}">
    <application android:label="{app_name}">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        return manifest_content

class MockLayoutGenerator:
    def generate_layout(self, feature_name):
        print(f"Mock generating layout for feature: {feature_name}")
        # Simulate generating a basic layout XML
        return f"<LinearLayout xmlns:android='http://schemas.android.com/apk/res/android' android:layout_width='match_parent' android:layout_height='match_parent' android:orientation='vertical'>\n    <TextView android:text='{feature_name}' android:layout_width='wrap_content' android:layout_height='wrap_content'/>\n</LinearLayout>"

class ArabicAppBuilderLobe:
    def __init__(self, output_dir="generated_apks"):
        self.output_dir = Path(output_dir)
        self.parser = MockArabicParser()
        self.feature_generator = MockFeatureGenerator()
        self.manifest_generator = MockAndroidManifestGenerator()
        self.layout_generator = MockLayoutGenerator()
        self.apk_compiler = ApkCompilerLobe(output_apk_dir=self.output_dir) # Assuming ApkCompilerLobe is available

    def process_arabic_request(self, arabic_text: str, project_root_dir: Path = Path("temp_arabic_project")):
        """
        Processes natural language Arabic requests to build and compile an APK.

        Args:
            arabic_text (str): The natural language instruction in Arabic.
            project_root_dir (Path): The directory to create the temporary project files.
        """
        print(f"--- Processing Arabic Request: '{arabic_text}' ---")

        if project_root_dir.exists():
            print(f"Cleaning existing project directory: {project_root_dir}")
            shutil.rmtree(project_root_dir)
        project_root_dir.mkdir(parents=True, exist_ok=True)

        parsed_data = self.parser.parse(arabic_text)

        if parsed_data["action"] == "build_app":
            app_name = parsed_data["app_name"]
            print(f"Initiating build for app: {app_name}")

            # --- Android Project Structure Setup ---
            android_project_path = project_root_dir / "android_app"
            android_project_path.mkdir(parents=True, exist_ok=True)

            # Manifest file
            manifest_path = android_project_path / "AndroidManifest.xml"
            manifest_content = self.manifest_generator.generate_manifest(app_name, [])
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest_content)
            print(f"Generated: {manifest_path}")

            # Main Activity (placeholder)
            main_activity_path = android_project_path / "src" / "main" / "java" / "com" / "example" / app_name.lower().replace(' ', '') / "MainActivity.java"
            main_activity_path.parent.mkdir(parents=True, exist_ok=True)
            main_activity_content = f"""package com.example.{app_name.lower().replace(' ', '')};

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming a default layout
    }}
}}
"""
            with open(main_activity_path, "w", encoding="utf-8") as f:
                f.write(main_activity_content)
            print(f"Generated: {main_activity_path}")

            # Default main layout
            default_layout_path = android_project_path / "res" / "layout" / "activity_main.xml"
            default_layout_path.parent.mkdir(parents=True, exist_ok=True)
            default_layout_content = f"<LinearLayout xmlns:android='http://schemas.android.com/apk/res/android' android:layout_width='match_parent' android:layout_height='match_parent' android:orientation='vertical'>\n    <TextView android:text='Welcome to {app_name}' android:layout_width='wrap_content' android:layout_height='wrap_content'/>\n</LinearLayout>"
            with open(default_layout_path, "w", encoding="utf-8") as f:
                f.write(default_layout_content)
            print(f"Generated: {default_layout_path}")

            # --- Feature Integration (if any in initial request) ---
            # This part could be more sophisticated, allowing for iterative additions
            # For now, we'll assume features are added in subsequent calls or as part of the initial build command.
            if "features" in parsed_data and parsed_data["features"]:
                self.integrate_features(android_project_path, parsed_data["features"])

            # --- Compile APK ---
            print(f"\nAttempting to compile APK for {app_name}...")
            try:
                # Assuming ApkCompilerLobe expects a path to a project directory
                # This might require a more structured input for ApkCompilerLobe if it expects specific project formats.
                # For demonstration, we'll pass the root of our temporary Android project.
                apk_path = self.apk_compiler.compile_apk(project_root_dir=android_project_path)
                print(f"Successfully compiled APK: {apk_path}")
            except Exception as e:
                print(f"Failed to compile APK: {e}")

        elif parsed_data["action"] == "add_feature":
            feature_name = parsed_data["feature_name"]
            print(f"Request to add feature: {feature_name}")
            # In a real scenario, this would involve finding an existing project and modifying it.
            # For this demo, we'll assume it's part of a larger build flow and will be handled when 'build_app' is called again or iteratively.
            print("Feature addition is typically part of the 'build_app' process or handled iteratively.")

        else:
            print("Unknown Arabic request.")

        print("\n--- Arabic App Builder Lobe Finished ---")

    def integrate_features(self, android_project_path: Path, features: list):
        """
        Integrates generated feature code into the Android project structure.

        Args:
            android_project_path (Path): The root of the generated Android project.
            features (list): A list of feature dictionaries.
        """
        for feature in features:
            feature_code = self.feature_generator.generate_code_for_feature(feature)
            feature_layout_xml = self.layout_generator.generate_layout(feature['feature_name'])

            # Example: Create a new Activity for each feature
            feature_activity_name = feature['feature_name'].replace(" ", "")
            feature_activity_path = android_project_path / "src" / "main" / "java" / "com" / "example" / android_project_path.name.lower().replace(' ', '') / f"{feature_activity_name}Activity.java"
            feature_activity_path.parent.mkdir(parents=True, exist_ok=True)

            feature_activity_content = f"""package com.example.{android_project_path.name.lower().replace(' ', '')};

import android.app.Activity;
import android.os.Bundle;
import android.view.View;

public class {feature_activity_name}Activity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{feature_activity_name.lower()}_layout); // Using feature-specific layout
    }}
}}
"""
            with open(feature_activity_path, "w", encoding="utf-8") as f:
                f.write(feature_activity_content)
            print(f"Generated feature activity: {feature_activity_path}")

            # Create feature-specific layout
            feature_layout_path = android_project_path / "res" / "layout" / f"{feature_activity_name.lower()}_layout.xml"
            with open(feature_layout_path, "w", encoding="utf-8") as f:
                f.write(feature_layout_xml)
            print(f"Generated feature layout: {feature_layout_path}")

            # TODO: Update AndroidManifest.xml to include new activities and potentially navigation.
            # TODO: Integrate feature_code into appropriate Java/Kotlin files if it's not just UI.

# Example Usage (for testing this lobe in isolation):
if __name__ == "__main__":
    # Mock ApkCompilerLobe for standalone testing
    class MockApkCompilerLobe:
        def __init__(self, output_apk_dir="generated_apks"):
            self.output_apk_dir = Path(output_apk_dir)
            self.output_apk_dir.mkdir(parents=True, exist_ok=True)

        def compile_apk(self, project_root_dir: Path):
            print(f"Mock compiling APK from: {project_root_dir}")
            apk_name = f"{project_root_dir.name}.apk"
            apk_path = self.output_apk_dir / apk_name
            # Simulate creating a dummy APK file
            with open(apk_path, "w") as f:
                f.write(f"Mock APK content for {project_root_dir.name}")
            print(f"Mock APK created at: {apk_path}")
            return apk_path

    # Instantiate the ArabicAppBuilderLobe with the mock compiler
    builder_lobe = ArabicAppBuilderLobe(output_dir="test_apks")
    builder_lobe.apk_compiler = MockApkCompilerLobe(output_apk_dir="test_apks")

    # --- Test Case 1: Build a simple app ---
    arabic_request_1 = "بناء تطبيق حسابي بسيط"
    builder_lobe.process_arabic_request(arabic_request_1)

    # --- Test Case 2: Build an app with a feature (demonstrative, feature integration needs enhancement) ---
    # Note: In a real system, this would likely be an iterative process.
    # For this demo, we'll simulate building an app and then *imagine* adding a feature later.
    # A more advanced flow would parse features within the "build app" command or handle iterative updates.

    # Let's simulate a request that includes features directly, though parsing needs to be more robust.
    # For now, we'll use a simplified approach where features are parsed if present.
    arabic_request_2_data = {"action": "build_app", "app_name": "تطبيق الملاحظات", "features": [{"feature_name": "عرض الملاحظات"}, {"feature_name": "إضافة ملاحظة"}]}
    # Mocking the parser to return this structure for demonstration
    builder_lobe.parser = MockArabicParser() # Reset to default mock
    builder_lobe.parser.parse = lambda text: arabic_request_2_data if "تطبيق الملاحظات" in text else MockArabicParser().parse(text)

    arabic_request_2 = "بناء تطبيق الملاحظات مع ميزة عرض الملاحظات وميزة إضافة ملاحظة"
    builder_lobe.process_arabic_request(arabic_request_2, project_root_dir=Path("temp_notes_app"))

    # Clean up dummy project directories
    if Path("temp_arabic_project").exists():
        shutil.rmtree("temp_arabic_project")
    if Path("temp_notes_app").exists():
        shutil.rmtree("temp_notes_app")