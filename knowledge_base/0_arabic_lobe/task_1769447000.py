import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

# --- Constants ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT", "/Users/your_user/Library/Android/sdk")
BUILD_TOOLS_DIR = os.path.join(ANDROID_SDK_ROOT, "build-tools")
AAPT_PATH = None
for version in sorted(os.listdir(BUILD_TOOLS_DIR), reverse=True):
    potential_aapt = os.path.join(BUILD_TOOLS_DIR, version, "aapt")
    if os.path.exists(potential_aapt):
        AAPT_PATH = potential_aapt
        break
    potential_aapt_win = os.path.join(BUILD_TOOLS_DIR, version, "aapt.exe")
    if os.path.exists(potential_aapt_win):
        AAPT_PATH = potential_aapt_win
        break

if not AAPT_PATH:
    raise EnvironmentError("Could not find AAPT in your Android SDK build-tools. Please set ANDROID_SDK_ROOT.")

DUMMY_APK_DIR = "./dummy_apk_output"
JAVA_PROJECT_DIR = "./generated_java_project"
MANIFEST_TEMPLATE_PATH = "./manifest_template.xml"
RESOURCE_DIR_TEMPLATE = "./resource_template"

# --- Helper Functions ---

def create_directory_if_not_exists(dir_path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

def copy_template_files(src_dir, dest_dir):
    """Copies files from a source directory to a destination directory."""
    if os.path.exists(src_dir):
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
        print(f"Copied template files from {src_dir} to {dest_dir}")
    else:
        print(f"Warning: Template directory not found at {src_dir}")

def compile_manifest(output_manifest_path, package_name, activities, services, permissions):
    """Generates and compiles an AndroidManifest.xml file."""
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    {permissions}

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">

        {activities}
        {services}

    </application>
</manifest>
"""
    permission_tags = "\n    ".join([f'<uses-permission android:name="android.permission.{p}"/>' for p in permissions])
    activity_tags = "\n        ".join([f'<activity android:name=".{activity_name}"></activity>' for activity_name in activities])
    service_tags = "\n        ".join([f'<service android:name=".{service_name}"></service>' for service_name in services])

    final_manifest_content = manifest_content.format(
        package_name=package_name,
        permissions=permission_tags,
        activities=activity_tags,
        services=service_tags
    )

    with open(output_manifest_path, "w", encoding="utf-8") as f:
        f.write(final_manifest_content)
    print(f"Generated manifest file: {output_manifest_path}")

def create_java_files_from_ast(java_project_dir, ast_nodes):
    """Creates Java source files from an Abstract Syntax Tree (AST) representation."""
    # This is a placeholder. In a real scenario, this would involve parsing the AST
    # and generating corresponding Java code.
    print("Creating placeholder Java files from AST...")
    create_directory_if_not_exists(os.path.join(java_project_dir, "app", "src", "main", "java", "com", "example", "generated"))
    for node in ast_nodes:
        if node.get("type") == "activity":
            activity_name = node.get("name", "PlaceholderActivity")
            file_path = os.path.join(java_project_dir, "app", "src", "main", "java", "com", "example", "generated", f"{activity_name}.java")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"package com.example.generated;\n\n")
                f.write(f"import androidx.appcompat.app.AppCompatActivity;\n")
                f.write(f"import android.os.Bundle;\n\n")
                f.write(f"public class {activity_name} extends AppCompatActivity {{\n")
                f.write(f"    @Override\n")
                f.write(f"    protected void onCreate(Bundle savedInstanceState) {{\n")
                f.write(f"        super.onCreate(savedInstanceState);\n")
                f.write(f"        // TODO: Implement actual activity logic based on AST\n")
                f.write(f"        setContentView(R.layout.activity_{activity_name.lower()}); // Placeholder layout\n")
                f.write(f"    }}\n")
                f.write(f"}}\n")
            print(f"Created placeholder Java file: {file_path}")
        elif node.get("type") == "service":
            service_name = node.get("name", "PlaceholderService")
            file_path = os.path.join(java_project_dir, "app", "src", "main", "java", "com", "example", "generated", f"{service_name}.java")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"package com.example.generated;\n\n")
                f.write(f"import android.app.Service;\n")
                f.write(f"import android.content.Intent;\n")
                f.write(f"import android.os.IBinder;\n\n")
                f.write(f"public class {service_name} extends Service {{\n")
                f.write(f"    @Override\n")
                f.write(f"    public IBinder onBind(Intent intent) {{\n")
                f.write(f"        return null;\n")
                f.write(f"    }}\n")
                f.write(f"    @Override\n")
                f.write(f"    public void onCreate() {{\n")
                f.write(f"        super.onCreate();\n")
                f.write(f"        // TODO: Implement actual service logic based on AST\n")
                f.write(f"    }}\n")
                f.write(f"}}\n")
            print(f"Created placeholder Java file: {file_path}")
    print("Placeholder Java file creation finished.")

def create_resource_files(resource_dir, app_name, activities, strings):
    """Creates basic resource files (strings.xml, layouts)."""
    create_directory_if_not_exists(os.path.join(resource_dir, "values"))
    create_directory_if_not_exists(os.path.join(resource_dir, "layout"))

    # strings.xml
    strings_xml_path = os.path.join(resource_dir, "values", "strings.xml")
    string_tags = f'<string name="app_name">{app_name}</string>\n'
    for key, value in strings.items():
        string_tags += f'    <string name="{key}">{value}</string>\n'
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(f"<resources>\n{string_tags}</resources>")
    print(f"Created strings.xml: {strings_xml_path}")

    # Layouts for activities (placeholder)
    for activity_name in activities:
        layout_file_path = os.path.join(resource_dir, "layout", f"activity_{activity_name.lower()}.xml")
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(f"<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\"\n")
            f.write(f"    xmlns:app=\"http://schemas.android.com/apk/res-auto\"\n")
            f.write(f"    xmlns:tools=\"http://schemas.android.com/tools\"\n")
            f.write(f"    android:layout_width=\"match_parent\"\n")
            f.write(f"    android:layout_height=\"match_parent\"\n")
            f.write(f"    tools:context=\".generated.{activity_name}\">\n")
            f.write(f"    <!-- TODO: Add actual layout for {activity_name} -->\n")
            f.write(f"</LinearLayout>")
        print(f"Created placeholder layout: {layout_file_path}")

def assemble_apk(project_dir, output_apk_path):
    """Assembles an APK from a given project directory."""
    # This is a simplified assembly process. In a real scenario,
    # you'd typically use Gradle or the Android command-line tools.
    # For demonstration, we'll simulate by creating a dummy APK.
    print(f"Simulating APK assembly for project: {project_dir}")
    create_directory_if_not_exists(DUMMY_APK_DIR)
    dummy_apk_path = os.path.join(DUMMY_APK_DIR, output_apk_path)
    with open(dummy_apk_path, "w") as f:
        f.write("This is a dummy APK file.\n")
    print(f"Created dummy APK at: {dummy_apk_path}")
    return dummy_apk_path

def extract_apk_info(apk_path):
    """Extracts information from an APK using AAPT."""
    print(f"Extracting information from APK: {apk_path}")
    try:
        result = subprocess.run(
            [AAPT_PATH, "dump", "badging", apk_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        output_lines = result.stdout.splitlines()
        apk_info = {}
        for line in output_lines:
            if "package:" in line:
                parts = line.split("'")
                apk_info['package_name'] = parts[1]
                apk_info['version_name'] = parts[3]
                apk_info['version_code'] = int(parts[5])
            elif "activity" in line and "name=" in line:
                start_index = line.find("name=") + 5
                end_index = line.find("'", start_index)
                activity_name = line[start_index:end_index]
                if 'activities' not in apk_info:
                    apk_info['activities'] = []
                apk_info['activities'].append(activity_name)
        print("APK info extracted successfully.")
        return apk_info
    except FileNotFoundError:
        print(f"Error: AAPT not found at {AAPT_PATH}. Ensure ANDROID_SDK_ROOT is set correctly.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running AAPT: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during AAPT execution: {e}")
        return None

def cleanup_apk_compiler_artifacts(knowledge_base_dir, java_project_dir):
    """Cleans up generated artifacts."""
    print("Cleaning up APK compiler artifacts...")
    if os.path.exists(JAVA_PROJECT_DIR):
        shutil.rmtree(JAVA_PROJECT_DIR)
        print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")
    if os.path.exists(DUMMY_APK_DIR):
        shutil.rmtree(DUMMY_APK_DIR)
        print(f"Removed dummy APK output directory: {DUMMY_APK_DIR}")
    if os.path.exists(MANIFEST_TEMPLATE_PATH):
        os.remove(MANIFEST_TEMPLATE_PATH)
        print(f"Removed manifest template: {MANIFEST_TEMPLATE_PATH}")
    if os.path.exists(RESOURCE_DIR_TEMPLATE):
        shutil.rmtree(RESOURCE_DIR_TEMPLATE)
        print(f"Removed resource template directory: {RESOURCE_DIR_TEMPLATE}")
    print("APK compiler artifacts cleanup finished.")

# --- Main Lobe Function ---

def arabic_apk_generation_lobe(nlp_output_ast, app_config, all_generated_files):
    """
    Lobe responsible for generating APKs from NLP output (AST).

    Args:
        nlp_output_ast (dict): The Abstract Syntax Tree generated from NLP analysis.
                               Expected to contain 'package_name', 'activities',
                               'services', 'permissions', 'strings', and 'app_name'.
        app_config (dict): Configuration for the APK generation, e.g., target build tools.
        all_generated_files (list): A list to store paths of all generated files.
    """
    print("\n--- Arabic APK Generation Lobe Initiating ---")

    package_name = nlp_output_ast.get("package_name", "com.example.generatedapp")
    activities = nlp_output_ast.get("activities", [])
    services = nlp_output_ast.get("services", [])
    permissions = nlp_output_ast.get("permissions", [])
    strings = nlp_output_ast.get("strings", {})
    app_name = nlp_output_ast.get("app_name", "MyGeneratedApp")

    # 1. Setup Project Structure
    create_directory_if_not_exists(JAVA_PROJECT_DIR)
    # In a real scenario, this would involve creating a more complete Android project structure
    # with build.gradle files, etc. For this demo, we'll focus on essential components.
    create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main"))
    create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res"))
    create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "assets"))
    create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "jni"))

    # 2. Generate Manifest File
    manifest_output_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "AndroidManifest.xml")
    compile_manifest(manifest_output_path, package_name, activities, services, permissions)
    all_generated_files.append(manifest_output_path)

    # 3. Generate Java Source Files
    # Assuming nlp_output_ast contains a representation of Java classes/activities/services
    create_java_files_from_ast(JAVA_PROJECT_DIR, nlp_output_ast.get("java_ast", []))

    # 4. Generate Resource Files
    resource_output_dir = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res")
    create_resource_files(resource_output_dir, app_name, activities, strings)
    all_generated_files.append(resource_output_dir) # Add the whole resource directory path


    # 5. Assemble APK (Simulated)
    print("\n--- Simulating APK Assembly ---")
    # In a real implementation, this would involve calling Gradle or Android SDK build tools.
    # For this demo, we'll create a dummy APK file.
    dummy_apk_name = f"{package_name.replace('.', '_')}.apk"
    dummy_apk_path = assemble_apk(JAVA_PROJECT_DIR, dummy_apk_name)
    all_generated_files.append(dummy_apk_path)

    print(f"\n--- Arabic APK Generation Lobe Finished ---")
    print(f"Generated dummy APK: {dummy_apk_path}")

    # The APK compilation process is simulated.
    # In a full implementation, this lobe would return the path to the compiled APK.
    return dummy_apk_path


# --- Demo Usage (Illustrative) ---
if __name__ == "__main__":
    # Example NLP output AST
    sample_nlp_ast = {
        "package_name": "com.myarabicapp.translate",
        "app_name": "مترجمي",
        "activities": ["MainActivity", "SettingsActivity"],
        "services": ["TranslationService"],
        "permissions": ["INTERNET", "ACCESS_NETWORK_STATE"],
        "strings": {
            "greeting_message": "أهلاً بك!",
            "settings_title": "الإعدادات"
        },
        "java_ast": [
            {"type": "activity", "name": "MainActivity"},
            {"type": "activity", "name": "SettingsActivity"},
            {"type": "service", "name": "TranslationService"}
        ]
    }

    # Example app configuration
    sample_app_config = {
        "build_tools_version": "33.0.0" # Example version
    }

    generated_files = []

    # Simulate calling the Lobe
    compiled_apk_path = arabic_apk_generation_lobe(sample_nlp_ast, sample_app_config, generated_files)

    print("\n--- APK Compiler Lobe Demo Output ---")
    print(f"Generated APK path: {compiled_apk_path}")
    print(f"All generated files: {generated_files}")

    # Example of extracting information from the generated APK (using the dummy)
    if compiled_apk_path and os.path.exists(compiled_apk_path):
        extracted_info = extract_apk_info(compiled_apk_path)
        if extracted_info:
            print("\n--- Extracted APK Information ---")
            for key, value in extracted_info.items():
                print(f"{key}: {value}")

    # Cleanup generated artifacts
    print("\n--- Cleaning up APK generation artifacts ---")
    cleanup_apk_compiler_artifacts(".", JAVA_PROJECT_DIR)
    print("Cleanup complete.")