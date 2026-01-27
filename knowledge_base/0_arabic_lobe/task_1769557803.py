import os
import shutil
from pathlib import Path

# Assume these constants and helper functions are defined elsewhere
# For example: KNOWLEDGE_BASE_DIR, APK_TEMPLATE_DIR, build_apk_from_project

# --- Lobe 1_arabic_parser_lobe ---
class ArabicParser:
    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.arabic_grammar = self._load_grammar()

    def _load_grammar(self) -> dict:
        # In a real scenario, this would load a sophisticated grammar
        # For demonstration, let's simulate a simple grammar structure
        return {
            "commands": {
                "create_app": {"description": "Create a new application", "params": ["app_name", "package_name"]},
                "add_activity": {"description": "Add a new activity", "params": ["activity_name", "layout_name"]},
                "add_button": {"description": "Add a button to a layout", "params": ["button_text", "on_click_action"]},
            },
            "keywords": {
                "app": "create_app",
                "screen": "add_activity",
                "button": "add_button",
                "named": None, # placeholder for naming
                "with_layout": None, # placeholder for layout
                "when_clicked": None, # placeholder for action
            }
        }

    def parse_natural_language(self, text: str) -> dict:
        tokens = text.lower().split()
        parsed_command = {}
        command_type = None
        params = {}

        # Simple keyword-based parsing
        for i, token in enumerate(tokens):
            if token in self.arabic_grammar["keywords"]:
                mapped_command = self.arabic_grammar["keywords"][token]
                if mapped_command and mapped_command.startswith("add_"): # Handling sub-commands within a flow
                    if command_type and command_type != mapped_command:
                        # Detect potential new command or error
                        pass
                    command_type = mapped_command
                elif mapped_command and mapped_command.startswith("create_"):
                    command_type = mapped_command

        if command_type:
            parsed_command["command"] = command_type
            command_info = self.arabic_grammar["commands"].get(command_type)
            if command_info:
                current_param_index = 0
                for j, token in enumerate(tokens):
                    if token in self.arabic_grammar["keywords"] and self.arabic_grammar["keywords"][token] is not None:
                        continue # Skip keywords that map to commands
                    elif token == "named":
                        if j + 1 < len(tokens):
                            params[command_info["params"][current_param_index]] = tokens[j+1]
                            current_param_index += 1
                    elif token == "with_layout":
                        if j + 1 < len(tokens):
                            params["layout_name"] = tokens[j+1] # Assuming layout_name is always the next for simplicity
                            current_param_index +=1 # Adjusting if layout_name is an explicit param
                    elif token == "when_clicked":
                        if j + 1 < len(tokens):
                            params["on_click_action"] = tokens[j+1]
                            current_param_index +=1 # Adjusting if on_click_action is an explicit param
                    elif command_type == "create_app" and current_param_index < len(command_info["params"]):
                         if tokens[j] not in ["app", "named"]: # Avoid adding "app" or "named" as parameter
                             params[command_info["params"][current_param_index]] = tokens[j]
                             current_param_index += 1
                    elif command_type == "add_activity" and current_param_index < len(command_info["params"]):
                        if tokens[j] not in ["screen", "named", "with_layout"]:
                            params[command_info["params"][current_param_index]] = tokens[j]
                            current_param_index += 1
                    elif command_type == "add_button" and current_param_index < len(command_info["params"]):
                         if tokens[j] not in ["button", "with_layout", "when_clicked"]:
                            params[command_info["params"][current_param_index]] = tokens[j]
                            current_param_index += 1
                parsed_command["params"] = params

        return parsed_command

# --- Lobe 4_code_generation_lobe ---
class CodeGenerator:
    def __init__(self, apk_template_dir: Path):
        self.apk_template_dir = apk_template_dir
        self.java_template = self._load_template("java_activity_template.java")
        self.xml_template = self._load_template("xml_layout_template.xml")
        self.gradle_template = self._load_template("build_gradle_template.gradle")
        self.manifest_template = self._load_template("AndroidManifest.xml.template")

    def _load_template(self, filename: str) -> str:
        template_path = self.apk_template_dir / filename
        if not template_path.exists():
            # In a real system, this would raise a more specific error
            raise FileNotFoundError(f"Template file not found: {template_path}")
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_java_activity(self, activity_name: str, package_name: str) -> str:
        # Basic replacement, a real generator would be more sophisticated
        return self.java_template.replace("{{ACTIVITY_NAME}}", activity_name).replace("{{PACKAGE_NAME}}", package_name)

    def generate_xml_layout(self, layout_name: str, elements: list = None) -> str:
        # Basic replacement, a real generator would be more sophisticated
        if elements is None:
            elements = []
        element_str = "\n".join(elements)
        return self.xml_template.replace("{{LAYOUT_NAME}}", layout_name).replace("{{LAYOUT_ELEMENTS}}", element_str)

    def generate_gradle_build_script(self, app_name: str, package_name: str) -> str:
        return self.gradle_template.replace("{{APP_NAME}}", app_name).replace("{{PACKAGE_NAME}}", package_name)

    def generate_manifest(self, package_name: str, activities: list) -> str:
        activity_declarations = "\n".join([f'        <activity android:name=".{activity}" />' for activity in activities])
        return self.manifest_template.replace("{{PACKAGE_NAME}}", package_name).replace("{{ACTIVITIES}}", activity_declarations)

# --- Lobe 3_project_structure_lobe ---
class ProjectStructureManager:
    def __init__(self, project_root: Path, package_name: str):
        self.project_root = project_root
        self.package_name = package_name
        self.source_dir = project_root / "app" / "src" / "main" / "java" / package_name.replace('.', os.sep)
        self.res_dir = project_root / "app" / "src" / "main" / "res"
        self.layout_dir = self.res_dir / "layout"
        self.manifest_file = project_root / "app" / "src" / "main" / "AndroidManifest.xml"
        self.build_gradle_file = project_root / "app" / "build.gradle"

    def create_project_dirs(self):
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir.mkdir(parents=True, exist_ok=True)
        self.layout_dir.mkdir(parents=True, exist_ok=True)

    def write_file(self, filepath: Path, content: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def add_activity_files(self, activity_name: str, layout_name: str, java_content: str, xml_content: str):
        activity_java_path = self.source_dir / f"{activity_name}.java"
        layout_xml_path = self.layout_dir / f"{layout_name}.xml"
        self.write_file(activity_java_path, java_content)
        self.write_file(layout_xml_path, xml_content)

    def update_manifest(self, manifest_content: str):
        self.write_file(self.manifest_file, manifest_content)

    def update_build_gradle(self, gradle_content: str):
        self.write_file(self.build_gradle_file, gradle_content)

# --- Main Integration Logic ---

class APKBuilder:
    def __init__(self, knowledge_base_dir: Path, apk_template_dir: Path):
        self.language_lobe = ArabicParser(knowledge_base_dir)
        self.code_generation_lobe = CodeGenerator(apk_template_dir)
        self.generation_result = {}

    def generate_apk(self, natural_language_prompt: str, project_output_dir: Path, app_name: str = "MyApp") -> dict:
        self.generation_result.clear()

        # 1. Parse Arabic Natural Language
        parsed_command = self.language_lobe.parse_natural_language(natural_language_prompt)
        print(f"Parsed command: {parsed_command}")

        if not parsed_command or "command" not in parsed_command:
            self.generation_result["status"] = "failed"
            self.generation_result["error"] = "Could not parse the Arabic command."
            return self.generation_result

        command_type = parsed_command["command"]
        params = parsed_command.get("params", {})

        # Determine package name from prompt or default
        package_name = params.get("package_name", f"com.example.{app_name.lower().replace(' ', '')}")
        if 'app_name' in params:
            app_name = params["app_name"] # Update app_name if provided

        project_root = project_output_dir / f"{app_name.replace(' ', '_')}_project"
        project_manager = ProjectStructureManager(project_root, package_name)
        project_manager.create_project_dirs()

        activities = []
        project_files = {} # To store generated file contents before writing

        if command_type == "create_app":
            print(f"Creating app: {app_name} with package: {package_name}")
            # Generate initial build.gradle and manifest
            gradle_content = self.code_generation_lobe.generate_gradle_build_script(app_name, package_name)
            project_manager.update_build_gradle(gradle_content)
            self.generation_result["build_gradle"] = gradle_content

            # Assume a default main activity for app creation
            main_activity_name = params.get("main_activity", "MainActivity")
            main_layout_name = params.get("main_layout", "activity_main")
            activities.append(main_activity_name)

            java_content = self.code_generation_lobe.generate_java_activity(main_activity_name, package_name)
            xml_content = self.code_generation_lobe.generate_xml_layout(main_layout_name)
            project_manager.add_activity_files(main_activity_name, main_layout_name, java_content, xml_content)
            project_files[f"src/{package_name.replace('.', os.sep)}/{main_activity_name}.java"] = java_content
            project_files[f"res/layout/{main_layout_name}.xml"] = xml_content

            # Generate manifest later, after all activities are known
            self.generation_result["initial_files"] = {
                f"build.gradle": gradle_content
            }

        elif command_type == "add_activity":
            activity_name = params.get("activity_name", "NewActivity")
            layout_name = params.get("layout_name", f"activity_{activity_name.lower()}")
            activities.append(activity_name)

            java_content = self.code_generation_lobe.generate_java_activity(activity_name, package_name)
            xml_content = self.code_generation_lobe.generate_xml_layout(layout_name)
            project_manager.add_activity_files(activity_name, layout_name, java_content, xml_content)
            project_files[f"src/{package_name.replace('.', os.sep)}/{activity_name}.java"] = java_content
            project_files[f"res/layout/{layout_name}.xml"] = xml_content
            self.generation_result["added_activity"] = {
                "name": activity_name,
                "layout": layout_name,
                "java_file": java_content,
                "xml_file": xml_content
            }

        elif command_type == "add_button":
            # This command is usually part of adding an activity or modifying a layout
            # For simplicity, let's assume it modifies the last added layout
            button_text = params.get("button_text", "Click Me")
            on_click_action = params.get("on_click_action", "handleButtonClick")

            # This is a placeholder - actual layout modification requires parsing XML
            # For now, we'll just note it. A real implementation would read existing XML,
            # parse it, add the button element, and write it back.
            button_element = f'<Button android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="{button_text}" android:id="@+id/button_{on_click_action}" />'
            print(f"Adding button to a layout (implementation pending): {button_text} with action {on_click_action}")
            # In a more advanced version, this would update an existing XML file.
            # For this demo, we'll just add it to the generation result.
            self.generation_result["button_to_add"] = {
                "text": button_text,
                "action": on_click_action,
                "element_xml": button_element
            }
            # We would need to fetch the last generated layout, parse it, add the button, and save.
            # This requires a more robust file handling and XML parsing within the module.

        else:
            self.generation_result["status"] = "failed"
            self.generation_result["error"] = f"Unsupported command type: {command_type}"
            return self.generation_result

        # Update manifest with all discovered activities
        manifest_content = self.code_generation_lobe.generate_manifest(package_name, activities)
        project_manager.update_manifest(manifest_content)
        project_files[f"AndroidManifest.xml"] = manifest_content
        self.generation_result["manifest"] = manifest_content

        # Write all generated project files
        for relative_path, content in project_files.items():
            filepath = project_root / relative_path
            # Ensure parent directories exist if not already created
            filepath.parent.mkdir(parents=True, exist_ok=True)
            project_manager.write_file(filepath, content)


        # Lobe 8_apk_compiler_lobe would be called here to build the APK
        # For now, we just confirm project structure is created.
        self.generation_result["project_path"] = str(project_root)
        self.generation_result["status"] = "success"
        self.generation_result["generated_files_preview"] = {
            k: v[:100] + "..." for k, v in project_files.items() # Preview of first 100 chars
        }

        print(f"\n--- Project structure created at: {project_root} ---")
        return self.generation_result


if __name__ == '__main__':
    # This is a placeholder for running the module independently for testing.
    # In the grand objective, this would be orchestrated by a higher-level module.

    # Mock directories and files for demonstration
    MOCK_KNOWLEDGE_BASE_DIR = Path("./mock_kb")
    MOCK_APK_TEMPLATE_DIR = Path("./mock_apk_templates")
    MOCK_PROJECT_OUTPUT_DIR = Path("./generated_projects")

    MOCK_KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    MOCK_APK_TEMPLATE_DIR.mkdir(exist_ok=True)
    MOCK_PROJECT_OUTPUT_DIR.mkdir(exist_ok=True)

    # Create dummy template files
    (MOCK_APK_TEMPLATE_DIR / "java_activity_template.java").write_text(
        """package {{PACKAGE_NAME}};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class {{ACTIVITY_NAME}} extends AppCompatActivity {

    private static final String TAG = "{{ACTIVITY_NAME}}";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{{LAYOUT_NAME}});
        Log.d(TAG, "Activity created with layout: {{LAYOUT_NAME}}");
        // Further logic for {{ACTIVITY_NAME}} goes here
    }
}
"""
    )

    (MOCK_APK_TEMPLATE_DIR / "xml_layout_template.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{{LAYOUT_NAME}}">

    <!-- {{LAYOUT_ELEMENTS}} -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    )
    (MOCK_APK_TEMPLATE_DIR / "build_gradle_template.gradle").write_text(
        """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace '{{PACKAGE_NAME}}'
    compileSdk 33

    defaultConfig {
        applicationId "{{PACKAGE_NAME}}"
        minSdk 21
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
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    )
    (MOCK_APK_TEMPLATE_DIR / "AndroidManifest.xml.template").write_text(
        """<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{{PACKAGE_NAME}}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppName"> <!-- Theme name might need adjustment -->

        {{ACTIVITIES}}

    </application>
</manifest>
"""
    )


    # Instantiate and run the APKBuilder
    apk_builder = APKBuilder(MOCK_KNOWLEDGE_BASE_DIR, MOCK_APK_TEMPLATE_DIR)

    # Test Case 1: Create a new app
    print("--- Test Case 1: Create a new app ---")
    prompt_1 = "أنشئ تطبيقًا جديدًا باسم 'My Awesome App' وحزمة 'com.example.myawesomeapp'"
    generation_result_1 = apk_builder.generate_apk(prompt_1, MOCK_PROJECT_OUTPUT_DIR, app_name="My Awesome App")
    print(f"Generation Result 1: {generation_result_1}\n")

    # Test Case 2: Add a new activity to an existing project structure
    print("--- Test Case 2: Add a new activity ---")
    prompt_2 = "أضف شاشة جديدة باسم 'SettingsScreen' مع تصميم 'settings_layout'"
    # For this test to work realistically, we need to have a project structure already
    # Let's re-initialize the builder to ensure a clean state for demonstration,
    # or simulate passing project context. For now, we'll assume a new project
    # context from the prompt. The `generate_apk` method will create a new dir.
    apk_builder_2 = APKBuilder(MOCK_KNOWLEDGE_BASE_DIR, MOCK_APK_TEMPLATE_DIR)
    generation_result_2 = apk_builder_2.generate_apk(prompt_2, MOCK_PROJECT_OUTPUT_DIR, app_name="MySecondApp")
    print(f"Generation Result 2: {generation_result_2}\n")

    # Test Case 3: Add a button (demonstrates partial functionality as layout modification is complex)
    print("--- Test Case 3: Add a button (demonstrates partial functionality) ---")
    prompt_3 = "أضف زرًا 'تسجيل الدخول' عندما يتم النقر عليه قم بتنفيذ 'loginAction'"
    apk_builder_3 = APKBuilder(MOCK_KNOWLEDGE_BASE_DIR, MOCK_APK_TEMPLATE_DIR)
    generation_result_3 = apk_builder_3.generate_apk(prompt_3, MOCK_PROJECT_OUTPUT_DIR, app_name="AppWithButton")
    print(f"Generation Result 3: {generation_result_3}\n")

    # Clean up mock directories (optional)
    # shutil.rmtree(MOCK_KNOWLEDGE_BASE_DIR)
    # shutil.rmtree(MOCK_APK_TEMPLATE_DIR)
    # shutil.rmtree(MOCK_PROJECT_OUTPUT_DIR)