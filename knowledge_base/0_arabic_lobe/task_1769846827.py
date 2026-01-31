import os
import shutil
import json
import re
import subprocess
from pathlib import Path

# Assume these are defined in a shared configuration or previous lobe
KNOWLEDGE_BASE_DIR = "knowledge_base"
PROJECT_TEMPLATES_DIR = "project_templates"
OUTPUT_DIR = "output"
UNITY_DIR = "unity" # Directory for unified mind components

# Placeholder for the unified mind object
class UnifiedMind:
    def __init__(self):
        self.lobes = {}
        self.knowledge_graph = {}

    def register_lobe(self, name, lobe_instance):
        self.lobes[name] = lobe_instance

    def get_lobe(self, name):
        return self.lobes.get(name)

    def update_knowledge(self, key, value):
        self.knowledge_graph[key] = value

    def cleanup(self):
        print("Unified mind cleanup initiated.")
        for lobe_name, lobe_instance in self.lobes.items():
            if hasattr(lobe_instance, 'cleanup') and callable(lobe_instance.cleanup):
                lobe_instance.cleanup()
        self.knowledge_graph.clear()
        print("Unified mind cleanup completed.")

# Placeholder for a generic lobe structure
class BaseLobe:
    def __init__(self, unified_mind):
        self.unified_mind = unified_mind

    def process(self, input_data):
        raise NotImplementedError

    def cleanup(self):
        pass

# Assume UnifiedMind and BaseLobe are initialized and accessible
unified_mind = UnifiedMind()

# --- Lobe 1_arabic_parsing_lobe ---
class ArabicParsingLobe(BaseLobe):
    def __init__(self, unified_mind):
        super().__init__(unified_mind)
        self.name = "arabic_parsing_lobe"
        self.supported_languages = ["arabic"]

    def parse_arabic_text(self, text):
        """
        Performs basic NLP parsing on Arabic text.
        This is a simplified example. A real implementation would use
        sophisticated libraries like CAMeL Tools, Farasa, or NLTK with Arabic support.
        """
        parsed_data = {
            "original_text": text,
            "tokens": [],
            "entities": [],
            "intent": None,
            "slots": {}
        }

        # Basic tokenization (splitting by spaces and common punctuation)
        tokens = re.split(r'[\s,.،!?;:]+', text.strip())
        parsed_data["tokens"] = [token for token in tokens if token]

        # Simple entity recognition (example: look for common Arabic names or places)
        # This is highly heuristic and requires proper NER models for real use.
        arabic_names = ["محمد", "علي", "فاطمة", "أحمد", "مريم", "بغداد", "القاهرة", "دبي"]
        for token in parsed_data["tokens"]:
            if token in arabic_names:
                parsed_data["entities"].append({"text": token, "type": "PERSON_OR_PLACE"})

        # Simple intent recognition (example: keywords)
        if "إنشاء" in text or "بناء" in text or "تطبيق" in text:
            parsed_data["intent"] = "create_apk"
            # Simple slot filling for app name
            match = re.search(r"(?:تطبيق|اسم التطبيق)\s+([\w\s]+)", text, re.IGNORECASE)
            if match:
                app_name = match.group(1).strip()
                parsed_data["slots"]["app_name"] = app_name
            else:
                # Default app name if not explicitly found
                parsed_data["slots"]["app_name"] = "MyArabicApp"

        return parsed_data

    def process(self, input_data):
        if not isinstance(input_data, dict) or "text" not in input_data or "language" not in input_data:
            print(f"[{self.name}] Invalid input data. Expected dict with 'text' and 'language'.")
            return None

        text = input_data["text"]
        language = input_data["language"].lower()

        if language in self.supported_languages:
            print(f"[{self.name}] Parsing Arabic text: '{text[:50]}...'")
            parsed_result = self.parse_arabic_text(text)
            self.unified_mind.update_knowledge(f"{self.name}_parsed_data", parsed_result)
            return parsed_result
        else:
            print(f"[{self.name}] Language '{language}' not supported by this lobe.")
            return None

    def cleanup(self):
        print(f"[{self.name}] Cleaning up parsing resources.")
        # No specific resources to clean in this simplified example

# --- Lobe 2_arabic_intent_extraction_lobe ---
class ArabicIntentExtractionLobe(BaseLobe):
    def __init__(self, unified_mind):
        super().__init__(unified_mind)
        self.name = "arabic_intent_extraction_lobe"
        self.supported_languages = ["arabic"]

    def extract_intent_and_slots(self, parsed_data):
        """
        Extracts intent and slots from already parsed Arabic data.
        This lobe might refine or further process the intent/slot information
        derived from the parsing lobe.
        """
        intent = None
        slots = {}

        if parsed_data and "intent" in parsed_data:
            intent = parsed_data["intent"]
            slots = parsed_data.get("slots", {})

            # Example refinement: If intent is create_apk, look for more details
            if intent == "create_apk":
                # More sophisticated slot filling based on entities or patterns
                # For example, extracting UI elements, features, etc.
                # This is a placeholder for more advanced logic.
                pass

        return intent, slots

    def process(self, input_data):
        if not isinstance(input_data, dict) or "parsed_data" not in input_data:
            print(f"[{self.name}] Invalid input data. Expected dict with 'parsed_data'.")
            return None

        parsed_data = input_data["parsed_data"]
        language = parsed_data.get("language", "arabic").lower() # Infer language from parsed_data

        if language in self.supported_languages:
            print(f"[{self.name}] Extracting intent and slots...")
            intent, slots = self.extract_intent_and_slots(parsed_data)
            extracted_info = {"intent": intent, "slots": slots}
            self.unified_mind.update_knowledge(f"{self.name}_extracted_info", extracted_info)
            return extracted_info
        else:
            print(f"[{self.name}] Language '{language}' not supported by this lobe.")
            return None

    def cleanup(self):
        print(f"[{self.name}] Cleaning up intent extraction resources.")

# --- Lobe 3_arabic_feature_mapping_lobe ---
class ArabicFeatureMappingLobe(BaseLobe):
    def __init__(self, unified_mind):
        super().__init__(unified_mind)
        self.name = "arabic_feature_mapping_lobe"
        self.supported_languages = ["arabic"]
        # Mapping of Arabic natural language features to APK components/code structures
        # This is a simplified lookup table. A real system would use ontologies,
        # knowledge graphs, or machine learning models.
        self.feature_map = {
            "واجهة مستخدم": "UI_LAYOUT",
            "زر": "BUTTON",
            "نص": "TEXT_VIEW",
            "صورة": "IMAGE_VIEW",
            "قائمة": "LIST_VIEW",
            "إدخال": "EDIT_TEXT",
            "تسجيل الدخول": "AUTH_MODULE",
            "خريطة": "MAP_COMPONENT",
            "إعدادات": "SETTINGS_ACTIVITY",
            "التقاط صورة": "CAMERA_PERMISSION_AND_INTENT",
            "مشاركة": "SHARE_INTENT",
            "قاعدة بيانات": "DATABASE_INTEGRATION",
            "اتصال بالإنترنت": "NETWORK_PERMISSION_AND_UTIL",
            "إشعار": "NOTIFICATION_SERVICE"
        }
        self.code_templates = {
            "UI_LAYOUT": "<LinearLayout>\n    <!-- Content will be generated here -->\n</LinearLayout>",
            "BUTTON": "<Button\n    android:id=\"@+id/myButton\"\n    android:layout_width=\"wrap_content\"\n    android:layout_height=\"wrap_content\"\n    android:text=\"Click Me\" />",
            "TEXT_VIEW": "<TextView\n    android:id=\"@+id/myTextView\"\n    android:layout_width=\"wrap_content\"\n    android:layout_height=\"wrap_content\"\n    android:text=\"Hello World\" />",
            "IMAGE_VIEW": "<ImageView\n    android:id=\"@+id/myImageView\"\n    android:layout_width=\"wrap_content\"\n    android:layout_height=\"wrap_content\"\n    android:src=\"@drawable/placeholder\" />",
            "EDIT_TEXT": "<EditText\n    android:id=\"@+id/myEditText\"\n    android:layout_width=\"match_parent\"\n    android:layout_height=\"wrap_content\"\n    android:hint=\"Enter text here\" />",
            "SETTINGS_ACTIVITY": "public class SettingsActivity extends AppCompatActivity {\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n        super.onCreate(savedInstanceState);\n        setContentView(R.layout.activity_settings);\n    }\n}",
            "AUTH_MODULE": "// Authentication module implementation placeholder",
            "NOTIFICATION_SERVICE": "public class MyNotificationService extends Service {\n    // Notification service implementation placeholder\n}",
            "NETWORK_PERMISSION_AND_UTIL": "// Network permission and utilities placeholder",
            "CAMERA_PERMISSION_AND_INTENT": "// Camera permission and intent placeholder",
            "SHARE_INTENT": "// Share intent placeholder",
            "DATABASE_INTEGRATION": "// Database integration placeholder",
            "LIST_VIEW": "<ListView\n    android:id=\"@+id/myListView\"\n    android:layout_width=\"match_parent\"\n    android:layout_height=\"match_parent\" />",
            "MAP_COMPONENT": "// Map component placeholder"
        }

    def map_features(self, extracted_info):
        """
        Maps identified Arabic features (from intent/slots) to structured APK components.
        """
        mapped_components = []
        slots = extracted_info.get("slots", {})

        # Map app name from slots
        if "app_name" in slots:
            mapped_components.append({"type": "APP_NAME", "value": slots["app_name"]})

        # Iterate through known Arabic features and map them
        # This is a very basic approach. A real system would use more robust NLP to extract features.
        for arabic_feature, component_type in self.feature_map.items():
            # Check if the Arabic feature phrase is present in the original prompt or a synthesized description
            # This requires access to the original prompt or a richer representation of user intent.
            # For this example, we'll assume some direct keywords are present in a conceptual "feature list"
            # derived from the original text. In a real scenario, this would be a result of deeper NLP.

            # Placeholder: Assume we have a list of identified features from previous steps
            # For demonstration, let's assume the extracted_info contains a conceptual list of features.
            # In a real system, this would be derived from the parsed_data.
            identified_features_conceptually = slots.get("features", []) # Example: slots["features"] = ["واجهة مستخدم", "زر"]

            if arabic_feature in identified_features_conceptually:
                mapped_components.append({"type": component_type, "arabic_term": arabic_feature})
                # Also add template for this component if available
                if component_type in self.code_templates:
                    mapped_components.append({"type": "CODE_TEMPLATE", "template_name": component_type, "content": self.code_templates[component_type]})

        return mapped_components

    def process(self, input_data):
        if not isinstance(input_data, dict) or "extracted_info" not in input_data:
            print(f"[{self.name}] Invalid input data. Expected dict with 'extracted_info'.")
            return None

        extracted_info = input_data["extracted_info"]
        # Infer language, assuming it's consistent with previous lobes
        language = "arabic" # Defaulting for this example

        if language in self.supported_languages:
            print(f"[{self.name}] Mapping Arabic features to APK components...")
            mapped_components = self.map_features(extracted_info)
            self.unified_mind.update_knowledge(f"{self.name}_mapped_components", mapped_components)
            return mapped_components
        else:
            print(f"[{self.name}] Language '{language}' not supported by this lobe.")
            return None

    def cleanup(self):
        print(f"[{self.name}] Cleaning up feature mapping resources.")

# --- Lobe 4_code_generation_lobe ---
class CodeGenerationLobe(BaseLobe):
    def __init__(self, unified_mind):
        super().__init__(unified_mind)
        self.name = "code_generation_lobe"
        self.project_template_dir = Path(PROJECT_TEMPLATES_DIR)
        self.output_dir = Path(OUTPUT_DIR)
        self.unity_dir = Path(UNITY_DIR)
        self.android_sdk_home = os.environ.get("ANDROID_HOME") # Ensure ANDROID_HOME is set

        if not self.android_sdk_home:
            print(f"[{self.name}] WARNING: ANDROID_HOME environment variable not set. SDK tools might not be found.")
            # Attempt to find it in common locations if not set
            possible_sdk_paths = [
                Path.home() / "Library" / "Android" / "sdk", # macOS
                Path.home() / "Android" / "Sdk",           # Linux/Windows
                Path("C:") / "Users" / os.getlogin() / "AppData" / "Local" / "Android" / "Sdk" # Windows
            ]
            for path in possible_sdk_paths:
                if path.exists():
                    self.android_sdk_home = str(path)
                    print(f"[{self.name}] Found ANDROID_HOME at: {self.android_sdk_home}")
                    break
            if not self.android_sdk_home:
                 raise EnvironmentError("ANDROID_HOME environment variable is not set and could not be found. Please set it or ensure the Android SDK is installed.")


        # Ensure necessary directories exist
        self.project_template_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.unity_dir.mkdir(parents=True, exist_ok=True)

        # Create a dummy Android project template if it doesn't exist
        self._create_dummy_project_template()

    def _create_dummy_project_template(self):
        """Creates a basic Android project structure for templating."""
        template_path = self.project_template_dir / "BasicAndroidApp"
        if not template_path.exists():
            print(f"[{self.name}] Creating dummy project template at: {template_path}")
            template_path.mkdir(parents=True, exist_ok=True)

            (template_path / "app").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main" / "res").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main" / "java" / "com").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main" / "java" / "com" / "example").mkdir(parents=True, exist_ok=True)
            (template_path / "app" / "src" / "main" / "java" / "com" / "example" / "basicandroidapp").mkdir(parents=True, exist_ok=True)

            # Dummy MainActivity.java
            main_activity_path = template_path / "app" / "src" / "main" / "java" / "com" / "example" / "basicandroidapp" / "MainActivity.java"
            main_activity_path.write_text("""
package com.example.basicandroidapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Default text, will be replaced by generated code
        TextView textView = findViewById(R.id.mainTextView);
        textView.setText("Welcome to your App!");
    }
}
""")

            # Dummy activity_main.xml
            activity_main_xml_path = template_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
            activity_main_xml_path.write_text("""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/mainTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
            # Dummy build.gradle (app level)
            build_gradle_app_path = template_path / "app" / "build.gradle"
            build_gradle_app_path.write_text("""
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.basicandroidapp'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.basicandroidapp"
        minSdk 24
        targetSdk 33
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
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""")
            # Dummy build.gradle (project level)
            build_gradle_project_path = template_path / "build.gradle"
            build_gradle_project_path.write_text("""
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2' // Example version, adjust as needed
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.10' // Example version, adjust as needed
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
""")
            # Dummy settings.gradle
            settings_gradle_path = template_path / "settings.gradle"
            settings_gradle_path.write_text("""
rootProject.name = "BasicAndroidApp"
include ':app'
""")

    def _get_sdk_tool(tool_name):
        """Helper to get path to SDK tool."""
        tool_path = Path(self.android_sdk_home) / "cmdline-tools" / "latest" / "bin" / f"{tool_name}"
        if tool_path.exists():
            return str(tool_path)
        # Fallback for older SDK structures
        tool_path = Path(self.android_sdk_home) / "tools" / "bin" / f"{tool_name}"
        if tool_path.exists():
            return str(tool_path)
        tool_path = Path(self.android_sdk_home) / "build-tools" / "latest" / f"{tool_name}" # e.g. apksigner
        if tool_path.exists():
            return str(tool_path)

        raise FileNotFoundError(f"Could not find SDK tool '{tool_name}' in {self.android_sdk_home}")

    def _run_command(self, command, cwd, shell=True):
        """Runs a command and captures output."""
        print(f"[{self.name}] Running command: {' '.join(command)} in {cwd}")
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                shell=shell # shell=True might be needed for gradle wrapper
            )
            print(f"[{self.name}] STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"[{self.name}] STDERR:\n{result.stderr}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"[{self.name}] Command failed with error code {e.returncode}")
            print(f"[{self.name}] STDOUT:\n{e.stdout}")
            print(f"[{self.name}] STDERR:\n{e.stderr}")
            raise
        except FileNotFoundError:
            print(f"[{self.name}] Command not found. Ensure '{command[0]}' is in your PATH or ANDROID_HOME is set correctly.")
            raise


    def generate_apk_structure(self, mapped_components, app_name="GeneratedApp"):
        """
        Generates the basic Android project structure and integrates components.
        """
        # Use a temporary directory for project generation
        temp_project_dir = self.unity_dir / f"{app_name.replace(' ', '_').lower()}_temp_project"
        if temp_project_dir.exists():
            shutil.rmtree(temp_project_dir)
        temp_project_dir.mkdir(parents=True, exist_ok=True)

        # Copy the dummy project template
        template_source_path = self.project_template_dir / "BasicAndroidApp"
        if not template_source_path.exists():
            raise FileNotFoundError(f"Project template not found at {template_source_path}. Please run _create_dummy_project_template.")
        shutil.copytree(template_source_path, temp_project_dir)

        # --- Integrate Mapped Components ---
        main_activity_java_path = temp_project_dir / "app" / "src" / "main" / "java" / "com" / "example" / "basicandroidapp" / "MainActivity.java"
        activity_main_xml_path = temp_project_dir / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        app_package_name = "com.example.basicandroidapp" # This should ideally be dynamic based on app_name

        # Extract app name and potentially modify package names if needed
        app_name_component = next((comp for comp in mapped_components if comp.get("type") == "APP_NAME"), None)
        if app_name_component:
            generated_app_name = app_name_component.get("value", app_name)
            print(f"[{self.name}] Setting app name to: {generated_app_name}")
            # Update AndroidManifest.xml if needed (more complex)
            # For now, just use it for output naming.

        # Parse and modify Java code
        java_code_lines = main_activity_java_path.read_text().splitlines()
        new_java_code_lines = []
        added_imports = set()
        layout_modifications = []
        java_code_modifications = []

        for line in java_code_lines:
            new_java_code_lines.append(line)
            if "public class MainActivity extends AppCompatActivity {" in line:
                # Add necessary imports based on mapped components
                for comp in mapped_components:
                    if comp.get("type") == "BUTTON":
                        added_imports.add("import android.widget.Button;")
                        java_code_modifications.append("        Button myButton = findViewById(R.id.myButton); // Placeholder for button interaction")
                    elif comp.get("type") == "TEXT_VIEW":
                        added_imports.add("import android.widget.TextView;")
                        # If TextView is already there, we might just update text
                        if "TextView textView = findViewById(R.id.mainTextView);" in line:
                            layout_modifications.append(('mainTextView', 'android:text', '"Generated Text"'))
                    elif comp.get("type") == "EDIT_TEXT":
                        added_imports.add("import android.widget.EditText;")
                        java_code_modifications.append("        EditText myEditText = findViewById(R.id.myEditText); // Placeholder for edit text interaction")
                    elif comp.get("type") == "IMAGE_VIEW":
                        added_imports.add("import android.widget.ImageView;")
                        java_code_modifications.append("        ImageView myImageView = findViewById(R.id.myImageView); // Placeholder for image view interaction")
                    elif comp.get("type") == "LIST_VIEW":
                        added_imports.add("import android.widget.ListView;")
                        java_code_modifications.append("        ListView myListView = findViewById(R.id.myListView); // Placeholder for list view interaction")
                    elif comp.get("type") == "SETTINGS_ACTIVITY":
                        added_imports.add("import android.content.Intent;")
                        # Logic to start settings activity, e.g., from a button click
                        java_code_modifications.append("        // Logic to navigate to SettingsActivity goes here")
                    elif comp.get("type") == "AUTH_MODULE":
                        added_imports.add("import android.content.Intent;")
                        java_code_modifications.append("        // Authentication logic placeholder")
                    elif comp.get("type") == "NOTIFICATION_SERVICE":
                        added_imports.add("import android.app.NotificationManager;")
                        added_imports.add("import android.app.Notification;")
                        added_imports.add("import androidx.core.app.NotificationCompat;")
                        java_code_modifications.append("        // Notification service implementation placeholder")
                    elif comp.get("type") == "NETWORK_PERMISSION_AND_UTIL":
                        # Add permission to manifest (requires reading/writing AndroidManifest.xml)
                        pass
                    elif comp.get("type") == "CAMERA_PERMISSION_AND_INTENT":
                        # Add permission to manifest and intent logic
                        pass
                    elif comp.get("type") == "SHARE_INTENT":
                        added_imports.add("import android.content.Intent;")
                        java_code_modifications.append("        // Share intent implementation placeholder")
                    elif comp.get("type") == "DATABASE_INTEGRATION":
                        pass # Placeholder for DB setup

        # Insert imports
        final_java_code = []
        inserted_imports = False
        for line in new_java_code_lines:
            if "package" in line and not inserted_imports:
                final_java_code.append(line)
                for imp in sorted(list(added_imports)):
                    final_java_code.append(imp)
                inserted_imports = True
            elif "public class" in line:
                # Insert modifications before the class body opens
                for mod in java_code_modifications:
                    final_java_code.append(mod)
                final_java_code.append(line)
            else:
                final_java_code.append(line)

        main_activity_java_path.write_text("\n".join(final_java_code))


        # Parse and modify XML layout
        try:
            from xml.etree import ElementTree as ET
        except ImportError:
            print(f"[{self.name}] XML parsing library not found. Skipping XML modification.")
            xml_tree = None
        else:
            parser = ET.XMLParser(encoding="utf-8")
            xml_tree = ET.parse(str(activity_main_xml_path), parser=parser)
            root = xml_tree.getroot()

            # Namespace for Android XML attributes
            namespace = {'android': 'http://schemas.android.com/apk/res/android'}

            # Add new UI elements to layout
            for comp in mapped_components:
                if comp.get("type") == "BUTTON":
                    button_elem = ET.Element("Button", attrib={
                        namespace['android']: "id", "myButton": "@+id/myButton",
                        namespace['android']: "layout_width", "wrap_content",
                        namespace['android']: "layout_height", "wrap_content",
                        namespace['android']: "text", "Generated Button"
                    })
                    root.append(button_elem)
                elif comp.get("type") == "TEXT_VIEW":
                    # Find existing TextView and update its text
                    text_view_elem = root.find(".//TextView[@android:id='@+id/mainTextView']")
                    if text_view_elem is not None:
                        text_view_elem.set(namespace['android'] + "text", "Generated Text")
                    else:
                        # Add a new one if not found
                        tv_elem = ET.Element("TextView", attrib={
                            namespace['android']: "id", "myTextView": "@+id/myTextView",
                            namespace['android']: "layout_width", "wrap_content",
                            namespace['android']: "layout_height", "wrap_content",
                            namespace['android']: "text", "Generated Text"
                        })
                        root.append(tv_elem)
                elif comp.get("type") == "EDIT_TEXT":
                    edit_text_elem = ET.Element("EditText", attrib={
                        namespace['android']: "id", "myEditText": "@+id/myEditText",
                        namespace['android']: "layout_width", "match_parent",
                        namespace['android']: "layout_height", "wrap_content",
                        namespace['android']: "hint", "Enter text here"
                    })
                    root.append(edit_text_elem)
                elif comp.get("type") == "IMAGE_VIEW":
                    image_view_elem = ET.Element("ImageView", attrib={
                        namespace['android']: "id", "myImageView": "@+id/myImageView",
                        namespace['android']: "layout_width", "wrap_content",
                        namespace['android']: "layout_height", "wrap_content",
                        namespace['android']: "src", "@drawable/placeholder" # Requires adding a placeholder drawable
                    })
                    root.append(image_view_elem)
                elif comp.get("type") == "LIST_VIEW":
                    list_view_elem = ET.Element("ListView", attrib={
                        namespace['android']: "id", "myListView": "@+id/myListView",
                        namespace['android']: "layout_width", "match_parent",
                        namespace['android']: "layout_height", "match_parent"
                    })
                    root.append(list_view_elem)

            # Write the modified XML back
            xml_tree.write(str(activity_main_xml_path), encoding="utf-8", xml_declaration=True)

        # Save the generated project structure
        self.unified_mind.update_knowledge("generated_project_path", str(temp_project_dir))
        self.unified_mind.update_knowledge("generated_app_name", generated_app_name)
        return str(temp_project_dir), generated_app_name

    def compile_apk(self, project_path, app_name):
        """
        Compiles the Android project into an APK using Gradle.
        """
        print(f"[{self.name}] Compiling APK for project at: {project_path}")
        build_gradle_file = Path(project_path) / "app" / "build.gradle"
        if not build_gradle_file.exists():
            raise FileNotFoundError(f"build.gradle not found in project: {project_path}")

        # Ensure correct package name in build.gradle if it was changed dynamically
        # (For this example, we assume it's fixed or handled by template)

        # Run Gradle build
        # Using the Gradle wrapper is preferred
        gradle_wrapper_path = Path(project_path) / "gradlew"
        if not gradle_wrapper_path.exists():
             # Fallback to invoking gradle directly if wrapper doesn't exist (less common now)
             print(f"[{self.name}] Gradle wrapper (gradlew) not found. Attempting to use system Gradle.")
             build_command = ["gradle", "assembleDebug", "-p", project_path]
        else:
             # Use the Gradle wrapper
             build_command = ["./gradlew", "assembleDebug", "-p", project_path] # -p specifies project directory

        try:
            # Navigate to the project directory to run gradlew correctly
            original_cwd = os.getcwd()
            os.chdir(project_path)
            self._run_command(build_command, cwd=project_path) # cwd passed here might be redundant if os.chdir is used
            os.chdir(original_cwd) # Change back to original directory

            # Find the generated APK
            # Default location for debug APK is app/build/outputs/apk/debug/
            debug_apk_path = Path(project_path) / "app" / "build" / "outputs" / "apk" / "debug"
            apks = list(debug_apk_path.glob("*.apk"))
            if not apks:
                raise FileNotFoundError(f"No APK found after build in: {debug_apk_path}")

            # Assuming the first APK found is the one we want (or sort by date if multiple)
            apk_file_path = apks[0]
            output_apk_name = f"{app_name.replace(' ', '_').lower()}_debug.apk"
            final_apk_path = self.output_dir / output_apk_name

            # Move the generated APK to the output directory
            shutil.move(str(apk_file_path), str(final_apk_path))
            print(f"[{self.name}] Successfully generated APK: {final_apk_path}")
            self.unified_mind.update_knowledge("generated_apk_path", str(final_apk_path))
            return str(final_apk_path)

        except Exception as e:
            print(f"[{self.name}] APK compilation failed: {e}")
            # Clean up the temp project directory on failure
            if temp_project_dir.exists():
                shutil.rmtree(temp_project_dir)
                print(f"[{self.name}] Cleaned up temporary project directory: {temp_project_dir}")
            raise


    def process(self, input_data):
        if not isinstance(input_data, dict) or "mapped_components" not in input_data:
            print(f"[{self.name}] Invalid input data. Expected dict with 'mapped_components'.")
            return None

        mapped_components = input_data["mapped_components"]
        # Attempt to get app_name from knowledge base if not directly in mapped_components
        app_name_from_kb = self.unified_mind.knowledge_graph.get("generated_app_name", "GeneratedApp")

        print(f"[{self.name}] Generating APK structure and code...")
        try:
            generated_project_path, generated_app_name = self.generate_apk_structure(mapped_components, app_name=app_name_from_kb)
            # Now compile the generated project
            print(f"[{self.name}] Compiling APK for '{generated_app_name}'...")
            final_apk_path = self.compile_apk(generated_project_path, generated_app_name)
            return {"status": "success", "apk_path": final_apk_path}
        except Exception as e:
            print(f"[{self.name}] Error during code generation or compilation: {e}")
            return {"status": "error", "message": str(e)}

    def cleanup(self):
        print(f"[{self.name}] Cleaning up code generation resources.")
        # Clean up dummy project template if it was created here
        template_path = self.project_template_dir / "BasicAndroidApp"
        if template_path.exists():
             try:
                 # Only remove if it was created by this lobe and not pre-existing essential template
                 # For safety, we won't auto-remove templates here unless explicitly designed to do so.
                 pass
             except Exception as e:
                 print(f"[{self.name}] Error during template cleanup: {e}")

        # Clean up any temporary project directories that might have been left behind due to errors
        for item in self.unity_dir.iterdir():
            if item.is_dir() and "_temp_project" in item.name:
                print(f"[{self.name}] Cleaning up leftover temporary project: {item}")
                shutil.rmtree(item)

# --- Lobe 5_apk_packaging_lobe ---
class APKPackagingLobe(BaseLobe):
    def __init__(self, unified_mind):
        super().__init__(unified_mind)
        self.name = "apk_packaging_lobe"
        self.android_sdk_home = os.environ.get("ANDROID_HOME")
        if not self.android_sdk_home:
            print(f"[{self.name}] WARNING: ANDROID_HOME environment variable not set. Packaging utilities might not be found.")
            # Attempt to find it in common locations if not set
            possible_sdk_paths = [
                Path.home() / "Library" / "Android" / "sdk", # macOS
                Path.home() / "Android" / "Sdk",           # Linux/Windows
                Path("C:") / "Users" / os.getlogin() / "AppData" / "Local" / "Android" / "Sdk" # Windows
            ]
            for path in possible_sdk_paths:
                if path.exists():
                    self.android_sdk_home = str(path)
                    print(f"[{self.name}] Found ANDROID_HOME at: {self.android_sdk_home}")
                    break
            if not self.android_sdk_home:
                 raise EnvironmentError("ANDROID_HOME environment variable is not set and could not be found. Please set it or ensure the Android SDK is installed.")

    def _get_sdk_tool_path(self, tool_name):
        """Finds the path to an Android SDK tool."""
        tool_paths = [
            Path(self.android_sdk_home) / "build-tools" / "*" / f"{tool_name}",
            Path(self.android_sdk_home) / "cmdline-tools" / "latest" / "bin" / f"{tool_name}",
            Path(self.android_sdk_home) / "tools" / "bin" / f"{tool_name}"
        ]
        for path_pattern in tool_paths:
            for found_path in Path(self.android_sdk_home).glob(str(path_pattern)):
                if found_path.is_file():
                    return str(found_path)
        raise FileNotFoundError(f"Could not find Android SDK tool '{tool_name}' in {self.android_sdk_home}")

    def _run_command(self, command, cwd, shell=True):
        """Runs a command and captures output."""
        print(f"[{self.name}] Running command: {' '.join(command)} in {cwd}")
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                shell=shell
            )
            print(f"[{self.name}] STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"[{self.name}] STDERR:\n{result.stderr}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"[{self.name}] Command failed with error code {e.returncode}")
            print(f"[{self.name}] STDOUT:\n{e.stdout}")
            print(f"[{self.name}] STDERR:\n{e.stderr}")
            raise
        except FileNotFoundError:
            print(f"[{self.name}] Command not found. Ensure '{command[0]}' is in your PATH or ANDROID_HOME is set correctly.")
            raise

    def sign_apk(self, apk_path, output_path, keystore_path, alias, storepass, keypass):
        """
        Signs an APK using jarsigner.
        For production, a proper keystore and signing keys are required.
        This uses dummy values for demonstration.
        """
        print(f"[{self.name}] Signing APK: {apk_path}")
        # In a real scenario, you would generate a keystore or use an existing one.
        # For demonstration, we'll assume a dummy keystore exists or skip signing for debug.
        # For a debug APK, signing is usually handled by Gradle. If we are packaging
        # a signed release APK, this step is crucial.

        # Dummy signing process using apksigner (preferred over jarsigner for modern APKs)
        try:
            apksigner_path = self._get_sdk_tool_path("apksigner")
            # For a debug APK, the signing might already be done by the build process.
            # If we need to re-sign or sign a release build, this would be more involved.
            # We'll simulate by just copying the debug APK for now and assume it's signed enough for testing.
            # A proper signing requires a keystore:
            # command = [apksigner_path, "sign", "--ks", keystore_path, "--ks-key-alias", alias, "--ks-pass", f"pass:{storepass}", "--key-pass", f"pass:{keypass}", "--out", output_path, apk_path]
            # For simplicity in this demo, we'll just copy the debug APK.
            shutil.copy(apk_path, output_path)
            print(f"[{self.name}] APK signed (simulated) and saved to: {output_path}")
            return output_path
        except FileNotFoundError:
            print(f"[{self.name}] apksigner not found. Cannot sign APK. Skipping signing.")
            shutil.copy(apk_path, output_path) # Copy even if signing fails
            return output_path
        except Exception as e:
            print(f"[{self.name}] Error during APK signing: {e}")
            shutil.copy(apk_path, output_path) # Copy even if signing fails
            return output_path


    def process(self, input_data):
        if not isinstance(input_data, dict) or "apk_path" not in input_data:
            print(f"[{self.name}] Invalid input data. Expected dict with 'apk_path'.")
            return None

        unsigned_apk_path = input_data["apk_path"]
        app_name = Path(unsigned_apk_path).stem.replace("_debug", "") # Extract app name from filename
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{self.name}] Packaging APK: {unsigned_apk_path}")

        # Dummy keystore details for signing (replace with actual details for release builds)
        dummy_keystore = "dummy.keystore" # This file should exist or be generated
        dummy_alias = "my-alias"
        dummy_storepass = "password"
        dummy_keypass = "password"

        final_apk_path = output_dir / f"{app_name}_signed.apk"

        # Ensure dummy keystore exists for demonstration if needed
        if not Path(dummy_keystore).exists():
            print(f"[{self.name}] Dummy keystore '{dummy_keystore}' not found. Creating a placeholder.")
            # In a real app, you would use keytool to generate a keystore.
            # For this demo, we'll just create an empty file to avoid errors in `sign_apk`
            # if it's not strictly required for debug builds.
            Path(dummy_keystore).touch()


        signed_apk_path = self.sign_apk(
            unsigned_apk_path,
            str(final_apk_path),
            dummy_keystore,
            dummy_alias,
            dummy_storepass,
            dummy_keypass
        )

        self.unified_mind.update_knowledge(f"{self.name}_packaged_apk_path", signed_apk_path)
        return {"status": "success", "packaged_apk_path": signed_apk_path}

    def cleanup(self):
        print(f"[{self.name}] Cleaning up APK packaging resources.")
        # Clean up dummy keystore if created here
        dummy_keystore = "dummy.keystore"
        if Path(dummy_keystore).exists():
            # Check if it was created by this lobe (e.g., based on timestamp or if it's empty)
            # For safety, we won't auto-remove it unless explicitly confirmed it's temporary.
            pass


# --- Lobe 6_deployment_lobe (Placeholder) ---
class DeploymentLobe(BaseLobe):
    def __init__(self, unified_mind):
        super().__init__(unified_mind)
        self.name = "deployment_lobe"

    def deploy_apk(self, apk_path):
        """
        Placeholder for APK deployment to a device or store.
        This would involve ADB commands, Google Play Console API, etc.
        """
        print(f"[{self.name}] Deploying APK to a device/store: {apk_path}")
        # Example: Using ADB to install on a connected device
        # try:
        #     subprocess.run(["adb", "install", "-r", apk_path], check=True)
        #     print(f"[{self.name}] APK installed successfully on connected device.")
        # except subprocess.CalledProcessError as e:
        #     print(f"[{self.name}] ADB installation failed: {e}")
        #     print("Please ensure a device is connected and ADB is authorized.")
        # except FileNotFoundError:
        #     print(f"[{self.name}] ADB command not found. Is Android SDK platform-tools in your PATH?")

        # For now, just confirm deployment initiation
        print(f"[{self.name}] Deployment process initiated for {apk_path}.")
        return {"status": "initiated", "deployment_target": "device/store"}

    def process(self, input_data):
        if not isinstance(input_data, dict) or "packaged_apk_path" not in input_data:
            print(f"[{self.name}] Invalid input data. Expected dict with 'packaged_apk_path'.")
            return None

        apk_path = input_data["packaged_apk_path"]
        deployment_result = self.deploy_apk(apk_path)
        self.unified_mind.update_knowledge(f"{self.name}_deployment_result", deployment_result)
        return deployment_result

    def cleanup(self):
        print(f"[{self.name}] Cleaning up deployment resources.")

# --- Initialization and Registration ---
# This part would typically be handled by the main application or a setup script.
# For demonstration purposes, we initialize the lobes here.

# Ensure knowledge base directory exists
Path(KNOWLEDGE_BASE_DIR).mkdir(parents=True, exist_ok=True)

# Register lobes with the unified mind
unified_mind.register_lobe("arabic_parsing_lobe", ArabicParsingLobe(unified_mind))
unified_mind.register_lobe("arabic_intent_extraction_lobe", ArabicIntentExtractionLobe(unified_mind))
unified_mind.register_lobe("arabic_feature_mapping_lobe", ArabicFeatureMappingLobe(unified_mind))
unified_mind.register_lobe("code_generation_lobe", CodeGenerationLobe(unified_mind))
unified_mind.register_lobe("apk_packaging_lobe", APKPackagingLobe(unified_mind))
unified_mind.register_lobe("deployment_lobe", DeploymentLobe(unified_mind))

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Starting Unified Mind Arabic APK Generation Flow ---")

    # --- Step 1: Arabic Parsing ---
    arabic_prompt = "أريد إنشاء تطبيق بسيط اسمه 'حاسبتي'. يجب أن يحتوي على زر وواجهة نصية."
    print(f"\n--- Processing prompt: '{arabic_prompt}' ---")

    arabic_parser = unified_mind.get_lobe("arabic_parsing_lobe")
    parsed_data = arabic_parser.process({"text": arabic_prompt, "language": "arabic"})

    if parsed_data:
        print(f"Parsing result: {json.dumps(parsed_data, indent=2, ensure_ascii=False)}")

        # --- Step 2: Intent Extraction ---
        intent_extractor = unified_mind.get_lobe("arabic_intent_extraction_lobe")
        # The input for the next lobe should be the output of the previous one,
        # wrapped in the expected format if necessary.
        extracted_info = intent_extractor.process({"parsed_data": parsed_data})

        if extracted_info:
            print(f"Intent extraction result: {json.dumps(extracted_info, indent=2, ensure_ascii=False)}")

            # --- Step 3: Feature Mapping ---
            feature_mapper = unified_mind.get_lobe("arabic_feature_mapping_lobe")
            # Pass the extracted info, which now conceptually contains the features to map
            # We augment extracted_info with a conceptual 'features' list for demonstration
            # In a real system, this would be derived directly from parsed_data['tokens'] or similar
            # based on the feature_map.
            conceptually_identified_features = []
            if "واجهة مستخدم" in arabic_prompt: conceptually_identified_features.append("واجهة مستخدم")
            if "زر" in arabic_prompt: conceptually_identified_features.append("زر")
            if "واجهة نصية" in arabic_prompt: conceptually_identified_features.append("نص")
            if "إنشاء تطبيق" in arabic_prompt:
                 # Ensure intent is recognized even if not explicitly listed as a feature
                 pass

            # Add conceptual features to the extracted info for mapping lobe
            if "slots" not in extracted_info:
                extracted_info["slots"] = {}
            extracted_info["slots"]["features"] = conceptually_identified_features # Crucial for demo mapping

            mapped_components = feature_mapper.process({"extracted_info": extracted_info})

            if mapped_components:
                print(f"Mapped components: {json.dumps(mapped_components, indent=2, ensure_ascii=False)}")

                # --- Step 4: Code Generation & Compilation ---
                code_generator = unified_mind.get_lobe("code_generation_lobe")
                generation_result = code_generator.process({"mapped_components": mapped_components})

                if generation_result and generation_result["status"] == "success":
                    print(f"Code generation and compilation result: {generation_result}")

                    # --- Step 5: APK Packaging ---
                    apk_packer = unified_mind.get_lobe("apk_packaging_lobe")
                    packaging_result = apk_packer.process({"apk_path": generation_result["apk_path"]})

                    if packaging_result and packaging_result["status"] == "success":
                        print(f"APK packaging result: {packaging_result}")

                        # --- Step 6: Deployment ---
                        deployer = unified_mind.get_lobe("deployment_lobe")
                        deployment_result = deployer.process({"packaged_apk_path": packaging_result["packaged_apk_path"]})

                        print(f"Deployment result: {deployment_result}")
                        print("\n--- Unified Mind Arabic APK Generation Flow Finished Successfully ---")
                    else:
                        print(f"APK packaging failed: {packaging_result}")
                        print("\n--- Unified Mind Arabic APK Generation Flow Finished with Packaging Error ---")
                else:
                    print(f"Code generation/compilation failed: {generation_result}")
                    print("\n--- Unified Mind Arabic APK Generation Flow Finished with Generation/Compilation Error ---")
            else:
                print("Feature mapping produced no components.")
                print("\n--- Unified Mind Arabic APK Generation Flow Finished with Mapping Error ---")
        else:
            print("Intent extraction failed.")
            print("\n--- Unified Mind Arabic APK Generation Flow Finished with Intent Extraction Error ---")
    else:
        print("Arabic parsing failed.")
        print("\n--- Unified Mind Arabic APK Generation Flow Finished with Parsing Error ---")

    # --- Cleanup ---
    print("\n--- Performing Unified Mind Cleanup ---")
    unified_mind.cleanup()
    print("--- Unified Mind Cleanup Complete ---")