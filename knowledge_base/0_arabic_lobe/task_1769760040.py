import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Any

# Assume these are defined and imported from other lobes/modules
# For demonstration purposes, we'll define them here with minimal functionality

class ArabicParser:
    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        # In a real scenario, this would load and process NLP models for Arabic
        pass

    def parse_apk_description(self, arabic_description: str) -> Dict[str, Any]:
        """
        Parses an Arabic description to extract APK components and metadata.
        This is a simplified placeholder. A real implementation would use advanced NLP.
        """
        apk_config = {
            "package_name": "com.example.myapp",
            "version_name": "1.0",
            "app_name": "تطبيق تجريبي",
            "permissions": [],
            "activities": [],
            "layouts": {},
            "strings": {},
            "dependencies": [],
            "assets": []
        }

        # Extremely basic keyword extraction for demonstration
        if "إنشاء تطبيق" in arabic_description:
            match_app_name = re.search(r"تطبيق باسم (.+?)(؟|\.|،)", arabic_description)
            if match_app_name:
                apk_config["app_name"] = match_app_name.group(1).strip()

            match_package = re.search(r"مع اسم حزمة (.+?)(؟|\.|،)", arabic_description)
            if match_package:
                apk_config["package_name"] = match_package.group(1).strip()

            if "يستخدم الأذونات" in arabic_description:
                permissions_match = re.search(r"يستخدم الأذونات التالية: (.*?)(؟|\.|،)", arabic_description)
                if permissions_match:
                    apk_config["permissions"] = [p.strip() for p in permissions_match.group(1).split('،')]

            if "يحتوي على الأنشطة" in arabic_description:
                activities_match = re.search(r"يحتوي على الأنشطة: (.*?)(؟|\.|،)", arabic_description)
                if activities_match:
                    apk_config["activities"] = [a.strip() for a in activities_match.group(1).split('،')]

            if "يحتوي على تنسيق" in arabic_description:
                layout_match = re.search(r"يحتوي على تنسيق (.*?) باسم (.*?)(؟|\.|،)", arabic_description)
                if layout_match:
                    layout_type = layout_match.group(1).strip()
                    layout_name = layout_match.group(2).strip()
                    apk_config["layouts"][layout_name] = {"type": layout_type} # Placeholder for more details

            if "يحتوي على سلاسل نصية" in arabic_description:
                strings_match = re.search(r"يحتوي على سلاسل نصية: (.*?)(؟|\.|،)", arabic_description)
                if strings_match:
                    string_pairs = strings_match.group(1).split('،')
                    for pair in string_pairs:
                        if ":" in pair:
                            key, value = pair.split(":", 1)
                            apk_config["strings"][key.strip()] = value.strip()

            if "يعتمد على المكتبات" in arabic_description:
                dependencies_match = re.search(r"يعتمد على المكتبات التالية: (.*?)(؟|\.|،)", arabic_description)
                if dependencies_match:
                    apk_config["dependencies"] = [d.strip() for d in dependencies_match.group(1).split('،')]

            if "يحتوي على أصول" in arabic_description:
                assets_match = re.search(r"يحتوي على أصول: (.*?)(؟|\.|،)", arabic_description)
                if assets_match:
                    apk_config["assets"] = [a.strip() for a in assets_match.group(1).split('،')]

        # Fallback for simpler descriptions
        if "إنشاء تطبيق بسيط" in arabic_description:
            apk_config["app_name"] = "تطبيق بسيط"
            apk_config["package_name"] = "com.example.simpleapp"
            apk_config["activities"] = ["MainActivity"]

        return apk_config

class CodeGenerator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = self.project_root / "app" / "src" / "main"
        self.manifest_path = self.src_dir / "AndroidManifest.xml"
        self.java_dir = self.src_dir / "java" / "com" / "example" / "myapp" # Simplified package
        self.res_dir = self.src_dir / "res"
        self.layout_dir = self.res_dir / "layout"
        self.values_dir = self.res_dir / "values"

    def _create_directories(self):
        self.java_dir.mkdir(parents=True, exist_ok=True)
        self.layout_dir.mkdir(parents=True, exist_ok=True)
        self.values_dir.mkdir(parents=True, exist_ok=True)

    def _generate_manifest(self, apk_config: Dict[str, Any]):
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{apk_config.get('package_name', 'com.example.defaultapp')}">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33" />
"""
        for permission in apk_config.get('permissions', []):
            manifest_content += f'    <uses-permission android:name="android.permission.{permission}" />\n'

        manifest_content += f"""
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/{apk_config.get('app_name_key', 'app_name')}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppTheme">
"""
        for activity in apk_config.get('activities', ['MainActivity']):
            is_launcher = "true" if activity == "MainActivity" else "false"
            manifest_content += f"""
        <activity android:name=".{activity}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""
        manifest_content += "    </application>\n</manifest>"

        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

    def _generate_string_resources(self, apk_config: Dict[str, Any]):
        strings_xml_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
"""
        # Add app name as a string resource
        app_name_key = "app_name"
        app_name_value = apk_config.get('app_name', 'My Application')
        strings_xml_content += f'    <string name="{app_name_key}">{app_name_value}</string>\n'
        apk_config['app_name_key'] = app_name_key # Store key for manifest

        for key, value in apk_config.get('strings', {}).items():
            strings_xml_content += f'    <string name="{key}">{value}</string>\n'

        strings_xml_content += "</resources>"

        with open(self.values_dir / "strings.xml", "w", encoding="utf-8") as f:
            f.write(strings_xml_content)

    def _generate_layout_file(self, layout_name: str, layout_content: str):
        layout_xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">
    <!-- Content for {layout_name} -->
    {layout_content}
</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(self.layout_dir / f"{layout_name}.xml", "w", encoding="utf-8") as f:
            f.write(layout_xml_content)

    def _generate_activity_file(self, activity_name: str, layout_name: str):
        activity_java_content = f"""package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});
    }}
}}
"""
        with open(self.java_dir / f"{activity_name}.java", "w", encoding="utf-8") as f:
            f.write(activity_java_content)

    def generate_apk_structure(self, arabic_description: str) -> Path:
        """
        Generates the basic directory structure and essential files for an Android APK
        based on the parsed Arabic description.
        """
        self._create_directories()

        # Assume a parser exists to get apk_config from arabic_description
        # In a real scenario, this would come from Lobe 0 or a dedicated parser module
        parser = ArabicParser(Path("./knowledge_base")) # Placeholder KB dir
        apk_config = parser.parse_apk_description(arabic_description)

        # Generate AndroidManifest.xml
        self._generate_manifest(apk_config)

        # Generate strings.xml
        self._generate_string_resources(apk_config)

        # Generate layout files if specified
        for layout_name, details in apk_config.get('layouts', {}).items():
            # Placeholder content for layouts, could be more sophisticated
            layout_content = f"<TextView android:layout_width='wrap_content' android:layout_height='wrap_content' android:text='@string/{layout_name}_title'/>"
            self._generate_layout_file(layout_name, layout_content)

        # Generate Activity files
        for activity_name in apk_config.get('activities', ['MainActivity']):
            # Infer layout name for simplicity, e.g., activity_main for MainActivity
            layout_for_activity = activity_name.lower().replace("activity", "")
            if not layout_for_activity: layout_for_activity = "activity_main" # Default

            # Check if a specific layout was defined for this activity
            found_layout_name = None
            for layout_name, details in apk_config.get('layouts', {}).items():
                if layout_name.lower() == f"activity_{layout_for_activity}".lower() or layout_name.lower() == layout_for_activity.lower():
                    found_layout_name = layout_name
                    break
            if not found_layout_name: # Fallback if not explicitly mapped
                found_layout_name = f"activity_{layout_for_activity}"
                # Ensure this layout is also created if it doesn't exist from apk_config
                if found_layout_name not in apk_config.get('layouts', {}):
                     self._generate_layout_file(found_layout_name, f"<TextView android:layout_width='wrap_content' android:layout_height='wrap_content' android:text='@string/{found_layout_name}_title'/>")


            self._generate_activity_file(activity_name, found_layout_name)


        # Note: Dependencies and Assets would require more complex handling
        # (e.g., downloading libraries, copying files) and are placeholders here.

        return self.project_root

# --- Lobe 4: Code Generation ---

class ArabicAPKGenerator:
    """
    This lobe is responsible for translating Arabic descriptions into executable APK structures.
    It orchestrates the parsing and code generation processes.
    """
    def __init__(self, project_base_dir: Path = Path("./generated_apks")):
        self.project_base_dir = project_base_dir
        self.current_project_path: Path = None

    def generate_apk_structure(self, arabic_description: str) -> Path:
        """
        Initiates the process of generating an Android APK structure from an Arabic description.
        """
        if not self.project_base_dir.exists():
            self.project_base_dir.mkdir(parents=True, exist_ok=True)

        # Create a unique project directory for this APK
        timestamp = Path.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"apk_{timestamp}"
        self.current_project_path = self.project_base_dir / project_name
        self.current_project_path.mkdir(parents=True, exist_ok=True)

        # Initialize the CodeGenerator with the new project path
        code_generator = CodeGenerator(self.current_project_path)

        # Generate the APK structure (manifest, activities, layouts, strings)
        generated_path = code_generator.generate_apk_structure(arabic_description)

        return generated_path

    def cleanup_project(self):
        """
        Cleans up the last generated project directory.
        """
        if self.current_project_path and self.current_project_path.exists():
            print(f"Cleaning up project directory: {self.current_project_path}")
            shutil.rmtree(self.current_project_path)
            self.current_project_path = None

# Example Usage (for testing this lobe in isolation)
if __name__ == "__main__":
    print("--- Testing Lobe 4: ArabicAPKGenerator ---")

    # Mock knowledge base directory
    Path("./knowledge_base").mkdir(exist_ok=True)

    generator = ArabicAPKGenerator()

    # Example 1: Simple app description
    arabic_description_1 = "قم بإنشاء تطبيق باسم 'دفتري' مع اسم حزمة com.example.myjournal. يستخدم الأذونات التالية: INTERNET، READ_EXTERNAL_STORAGE. يحتوي على الأنشطة: MainActivity، SettingsActivity. يحتوي على تنسيق activity_main باسم main_layout. يحتوي على سلاسل نصية: app_title: دفتري، welcome_message: أهلاً بك في دفتري."
    print(f"\n--- Generating APK structure for: '{arabic_description_1[:50]}...' ---")
    try:
        project_path_1 = generator.generate_apk_structure(arabic_description_1)
        print(f"Project generated at: {project_path_1}")
        # You would typically move to Lobe 8 (Compiler) from here
    except Exception as e:
        print(f"Demo 1 failed: {e}")
    finally:
        generator.cleanup_project()

    # Example 2: Another description with different components
    arabic_description_2 = "إنشاء تطبيق باسم 'ملاحظاتي' مع اسم حزمة com.example.mynotes. يحتوي على الأنشطة: NoteListActivity، AddNoteActivity. يحتوي على تنسيق note_list باسم list_layout. يحتوي على سلاسل نصية: app_name: ملاحظاتي، empty_list_text: لا توجد ملاحظات."
    print(f"\n--- Generating APK structure for: '{arabic_description_2[:50]}...' ---")
    try:
        project_path_2 = generator.generate_apk_structure(arabic_description_2)
        print(f"Project generated at: {project_path_2}")
    except Exception as e:
        print(f"Demo 2 failed: {e}")
    finally:
        generator.cleanup_project()

    # Example 3: Minimal description
    arabic_description_3 = "إنشاء تطبيق بسيط"
    print(f"\n--- Generating APK structure for: '{arabic_description_3}' ---")
    try:
        project_path_3 = generator.generate_apk_structure(arabic_description_3)
        print(f"Project generated at: {project_path_3}")
    except Exception as e:
        print(f"Demo 3 failed: {e}")
    finally:
        generator.cleanup_project()

    print("\n--- ArabicAPKGenerator Module Demo Finished ---")

    # Clean up mock knowledge base directory
    if Path("./knowledge_base").exists():
        shutil.rmtree("./knowledge_base")