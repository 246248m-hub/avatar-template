import os
import zipfile
import shutil
from pathlib import Path

# Placeholder for a more sophisticated APK building process
class APKBuilder:
    def __init__(self, project_root="apk_project"):
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.assets_dir = self.project_root / "assets"
        self.res_dir = self.project_root / "res"
        self.manifest_path = self.project_root / "AndroidManifest.xml"
        self.apk_path = None

    def _create_project_structure(self):
        self.project_root.mkdir(exist_ok=True)
        self.src_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
        self.res_dir.mkdir(exist_ok=True)

    def _create_manifest(self, app_name="MyApp"):
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_name.lower()}">
    <application
        android:label="{app_name}"
        android:icon="@mipmap/ic_launcher">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

    def _create_main_activity(self, app_name="MyApp"):
        activity_content = f"""
package com.example.{app_name.lower()};

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming a basic layout exists
    }}
}}
"""
        with open(self.src_dir / "MainActivity.java", "w", encoding="utf-8") as f:
            f.write(activity_content)

    def _create_layout_file(self):
        # A very basic layout
        layout_content = """
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello from Arabic App!" />
</LinearLayout>
"""
        res_layout_dir = self.res_dir / "layout"
        res_layout_dir.mkdir(exist_ok=True)
        with open(res_layout_dir / "activity_main.xml", "w", encoding="utf-8") as f:
            f.write(layout_content)

    def _create_resources(self):
        # Mocking mipmap directory for launcher icon
        mipmap_dir = self.res_dir / "mipmap-anydpi-v26"
        mipmap_dir.mkdir(exist_ok=True)
        # Minimal placeholder for launcher icon (not a real image)
        with open(mipmap_dir / "ic_launcher.xml", "w", encoding="utf-8") as f:
            f.write("<adaptive-icon xmlns:android=\"http://schemas.android.com/apk/res/android\"></adaptive-icon>")


    def build_apk(self, prompt_data):
        """
        Builds a mock APK structure based on prompt data.
        In a real scenario, this would involve compiling Java/Kotlin code,
        compiling resources, and packaging into an APK.
        """
        app_name = prompt_data.get("app_name", "MyApp")
        self._create_project_structure()
        self._create_manifest(app_name)
        self._create_main_activity(app_name)
        self._create_layout_file()
        self._create_resources()

        # Simulate APK creation by zipping the project
        self.apk_path = self.project_root.parent / f"{app_name.lower()}.apk"
        with zipfile.ZipFile(self.apk_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.project_root):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.project_root)
                    zipf.write(file_path, arcname=arcname)

        print(f"Mock APK generated at: {self.apk_path}")
        return str(self.apk_path)

    def _cleanup_project(self):
        if self.project_root.exists():
            shutil.rmtree(self.project_root)
        if self.apk_path and Path(self.apk_path).exists():
            Path(self.apk_path).unlink()

class ArabicAPKGenerator:
    def __init__(self):
        self.apk_builder = APKBuilder()
        # In a real scenario, this would be loaded from KNOWLEDGE_BASE_DIR
        self.arabic_keywords_mapping = {
            "اسم التطبيق": "app_name",
            "رسالة الترحيب": "welcome_message",
            "لون الخلفية": "background_color"
        }

    def parse_arabic_prompt(self, prompt: str) -> dict:
        """
        Parses an Arabic natural language prompt to extract parameters for APK generation.
        This is a simplified parser. A real implementation would use NLP techniques.
        """
        extracted_params = {}
        words = prompt.split()
        for i, word in enumerate(words):
            if word in self.arabic_keywords_mapping:
                key = self.arabic_keywords_mapping[word]
                # Simple logic to capture the next word as a value
                if i + 1 < len(words):
                    value = words[i+1]
                    # Basic type conversion or validation could be added here
                    if key == "background_color":
                        # Mock color, actual color parsing needed for real apps
                        extracted_params[key] = f"#{value}" # Example: 'احمر' -> '#red'
                    else:
                        extracted_params[key] = value
        return extracted_params

    def generate_apk_from_arabic_prompt(self, arabic_prompt: str) -> str | None:
        """
        Generates an APK from an Arabic natural language prompt.
        """
        print(f"\n--- Processing Arabic Prompt: '{arabic_prompt}' ---")
        try:
            apk_params = self.parse_arabic_prompt(arabic_prompt)
            print(f"Extracted parameters: {apk_params}")

            # Basic validation and defaults
            if "app_name" not in apk_params:
                print("Warning: App name not specified, using default 'ArabicApp'.")
                apk_params["app_name"] = "ArabicApp"

            # The APKBuilder will use these parameters to construct the mock APK
            generated_apk_path = self.apk_builder.build_apk(apk_params)
            return generated_apk_path

        except Exception as e:
            print(f"Error during APK generation: {e}")
            return None
        finally:
            # In a real scenario, cleanup might happen elsewhere or be conditional
            # For this demo, we clean up the project files after attempt
            self.apk_builder._cleanup_project()


# --- Example Usage ---
if __name__ == "__main__":
    arabic_generator = ArabicAPKGenerator()

    # Example 1: Simple prompt
    prompt_1 = "أنشئ تطبيق باسم 'عربـي' مع رسالة ترحيب 'أهلا بك'"
    apk_path_1 = arabic_generator.generate_apk_from_arabic_prompt(prompt_1)

    if apk_path_1:
        print(f"\nSUCCESS: APK generated at: {apk_path_1}")
    else:
        print("\nFAILURE: APK generation failed for prompt 1.")

    # Example 2: Prompt with color (mocked)
    prompt_2 = "أنشئ تطبيق باسم 'لونـي' بلون خلفية 'أزرق'"
    apk_path_2 = arabic_generator.generate_apk_from_arabic_prompt(prompt_2)

    if apk_path_2:
        print(f"\nSUCCESS: APK generated at: {apk_path_2}")
    else:
        print("\nFAILURE: APK generation failed for prompt 2.")

    # Example 3: Prompt without app name
    prompt_3 = "أريد تطبيق بسيط برسالة 'مرحبا'"
    apk_path_3 = arabic_generator.generate_apk_from_arabic_prompt(prompt_3)

    if apk_path_3:
        print(f"\nSUCCESS: APK generated at: {apk_path_3}")
    else:
        print("\nFAILURE: APK generation failed for prompt 3.")

    print("\n--- Arabic APK Generation Module Demo Finished ---")