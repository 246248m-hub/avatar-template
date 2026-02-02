import os
import re
import shutil

# --- Configuration ---
# A placeholder for the directory where APKs will be generated.
# In a real system, this would be dynamically managed or configured.
GENERATED_APK_DIR = "generated_apks"
# A placeholder for the directory containing the Android project template.
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"

# --- Helper Functions ---

def load_template(template_name):
    """Loads the content of a template file."""
    template_path = os.path.join(ANDROID_PROJECT_TEMPLATE_DIR, template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(filepath, content):
    """Saves content to a file, creating directories if necessary."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_in_template(template_content, placeholder, value):
    """Replaces a placeholder in template content with a given value."""
    return template_content.replace(placeholder, str(value))

def create_android_project_structure(project_name, base_package_name):
    """Creates a basic Android project directory structure."""
    project_dir = os.path.join(GENERATED_APK_DIR, project_name)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)

    package_dir_parts = base_package_name.split('.')
    app_src_main_java_path = os.path.join(project_dir, 'app', 'src', 'main', 'java', *package_dir_parts)
    os.makedirs(app_src_main_java_path)

    # Create AndroidManifest.xml placeholder
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_filepath = os.path.join(project_dir, 'app', 'src', 'main', 'AndroidManifest.xml')
    save_file(manifest_filepath, manifest_content.format(package_name=base_package_name))

    # Create strings.xml placeholder
    strings_content = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    strings_filepath = os.path.join(project_dir, 'app', 'src', 'main', 'res', 'values', 'strings.xml')
    save_file(strings_filepath, strings_content.format(app_name=project_name))

    print(f"Created basic Android project structure at: {project_dir}")
    return project_dir

# --- Arabic Specific Logic ---

def extract_app_details_from_arabic(arabic_prompt):
    """
    Parses an Arabic natural language prompt to extract application name and base package.
    This is a simplified example and would require more sophisticated NLP for real-world use.
    """
    app_name = "MyArabicApp"
    base_package = "com.example.myarabicapp"

    # Simple pattern: "إنشاء تطبيق اسمه {اسم التطبيق}" (Create an app named {app name})
    name_match = re.search(r"إنشاء تطبيق اسمه\s+([\w\s]+)", arabic_prompt)
    if name_match:
        app_name = name_match.group(1).strip()

    # Simple pattern: "بحزمة أساسية {اسم الحزمة}" (with base package {package name})
    package_match = re.search(r"بحزمة أساسية\s+([\w.]+)", arabic_prompt)
    if package_match:
        base_package = package_match.group(1).strip()

    # Further refine package name if needed (e.g., replace spaces with underscores)
    app_name_for_package = re.sub(r'\s+', '_', app_name).lower()
    if not base_package or base_package == "com.example.myarabicapp":
        base_package = f"com.example.{app_name_for_package}"

    print(f"Parsed App Name: {app_name}")
    print(f"Parsed Base Package: {base_package}")
    return app_name, base_package

def generate_activity_code_from_arabic(activity_description_arabic, base_package_name, activity_name="MainActivity"):
    """
    Generates basic Java/Kotlin Activity code from Arabic description.
    This function would evolve to generate more complex UI and logic.
    """
    # Placeholder for actual Java/Kotlin code generation.
    # In a full implementation, this would involve templates and more advanced parsing.
    java_code_template = """
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{layout_name}); // Assumes a layout file

        TextView welcomeText = findViewById(R.id.welcome_text); // Assumes a TextView with this ID
        welcomeText.setText("أهلاً بك في تطبيق: {app_title}!");

        // Add logic based on activity_description_arabic if provided
        // For now, just a placeholder message.
        System.out.println("Activity created with description: {activity_description_arabic}");
    }}
}}
"""
    # Simplified layout name generation
    layout_name = activity_name.replace("Activity", "").lower()

    # Extract app title from base_package_name or use a default if needed.
    # This is a very basic approach. A more robust system would track app context.
    app_title_parts = base_package_name.split('.')
    app_title = app_title_parts[-1].replace('_', ' ').title() if app_title_parts else "My App"


    activity_code = java_code_template.format(
        package_name=base_package_name,
        activity_name=activity_name,
        layout_name=layout_name,
        app_title=app_title,
        activity_description_arabic=activity_description_arabic
    )
    return activity_code

def generate_layout_xml_from_arabic(layout_description_arabic, layout_name="activity_main"):
    """
    Generates basic Android layout XML from Arabic description.
    This would evolve to generate more complex UI elements and constraints.
    """
    # Placeholder for actual XML layout generation.
    xml_template = """<?xml version="1.0" encoding="utf-8"?>
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
        android:text="رسالة ترحيب"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <!-- Add more UI elements based on layout_description_arabic if provided -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    # Simplified activity name derivation from layout name
    activity_name = layout_name.replace("activity_", "").capitalize() + "Activity"

    layout_xml = xml_template.format(activity_name=activity_name)
    return layout_xml

# --- Main Lobe Function ---

def arabic_apk_generator_lobe(natural_language_prompt: str) -> str:
    """
    This Lobe's objective is to take an Arabic natural language prompt
    and generate a hyper-efficient APK structure.

    It will perform the following steps:
    1. Parse the Arabic prompt to extract application details (name, package).
    2. Generate a basic Android project structure.
    3. Generate Activity and Layout code based on parsed information and prompt details.
    4. Place generated code into the project structure.

    Args:
        natural_language_prompt (str): The Arabic prompt describing the desired APK.

    Returns:
        str: A success message indicating the path to the generated project, or an error message.
    """
    print(f"\n--- Arabic APK Generator Lobe Activated ---")
    print(f"Processing prompt: '{natural_language_prompt}'")

    if not os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        # In a real scenario, this would download or manage templates.
        # For this example, we'll create a dummy template directory.
        os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR, exist_ok=True)
        print(f"Created dummy Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        # We will create dummy essential files within the create_android_project_structure if they don't exist.

    try:
        # Step 1: Parse Arabic prompt for app details
        app_name, base_package_name = extract_app_details_from_arabic(natural_language_prompt)

        # Step 2: Generate Android project structure
        # We'll simulate creating a project within the GENERATED_APK_DIR
        project_root = create_android_project_structure(app_name, base_package_name)

        # Step 3 & 4: Generate and place Activity and Layout code
        # This part is highly simplified. A real system would parse more from the prompt
        # to define activities, layouts, and their content.

        # Assume the prompt implies a main activity with a simple welcome message.
        # A more complex prompt could specify multiple activities, buttons, etc.
        main_activity_name = "MainActivity"
        main_activity_description = "شاشة ترحيب بسيطة" # Simplified description
        main_layout_name = f"activity_{main_activity_name.replace('Activity', '').lower()}"

        # Generate Activity code
        activity_code = generate_activity_code_from_arabic(
            main_activity_description,
            base_package_name,
            main_activity_name
        )
        activity_filepath = os.path.join(project_root, 'app', 'src', 'main', 'java', *base_package_name.split('.'), f"{main_activity_name}.java")
        save_file(activity_filepath, activity_code)
        print(f"Generated and saved Activity: {activity_filepath}")

        # Generate Layout XML
        layout_xml = generate_layout_xml_from_arabic(
            main_activity_description,
            main_layout_name
        )
        layout_dir = os.path.join(project_root, 'app', 'src', 'main', 'res', 'layout')
        os.makedirs(layout_dir, exist_ok=True)
        layout_filepath = os.path.join(layout_dir, f"{main_layout_name}.xml")
        save_file(layout_filepath, layout_xml)
        print(f"Generated and saved Layout XML: {layout_filepath}")

        # Note: This Lobe does NOT compile the APK. It generates the project structure and source files.
        # The next Lobe (e.g., APK Compiler) would handle compilation.

        return f"Successfully generated Android project structure for '{app_name}' at: {project_root}. APK compilation is the next step."

    except FileNotFoundError as e:
        return f"Error: Template file not found. Ensure '{ANDROID_PROJECT_TEMPLATE_DIR}' is set up correctly. Details: {e}"
    except Exception as e:
        return f"An error occurred during APK generation: {e}"

# --- Demo/Testing ---

def cleanup_android_project_template():
    """Cleans up the dummy Android project template directory if it was created by the demo."""
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR) and os.path.isdir(ANDROID_PROJECT_TEMPLATE_DIR):
        # Check if it's empty or contains only dummy files created by this demo
        if not os.listdir(ANDROID_PROJECT_TEMPLATE_DIR): # Simplistic check
            shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
            print(f"Cleaned up dummy template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")

def run_arabic_apk_generator_demo():
    """Demonstrates the functionality of the Arabic APK Generator Lobe."""
    print("\n--- Arabic APK Generator Lobe Demo ---")

    # Ensure the generated APKs directory exists
    os.makedirs(GENERATED_APK_DIR, exist_ok=True)

    # Example Arabic prompt
    arabic_prompt_1 = "أريد إنشاء تطبيق اسمه 'تطبيقي الأول' بحزمة أساسية 'com.myapps.firstapp'."
    result_1 = arabic_apk_generator_lobe(arabic_prompt_1)
    print(f"Result 1: {result_1}")

    arabic_prompt_2 = "أنشئ تطبيقًا لدفتر ملاحظات بسيط يسمى 'مفكرتي' بحزمة أساسية com.notes.my."
    result_2 = arabic_apk_generator_lobe(arabic_prompt_2)
    print(f"Result 2: {result_2}")

    # Example with implicit package name derivation
    arabic_prompt_3 = "قم بإنشاء تطبيق للصور يسمى 'معرضي'."
    result_3 = arabic_apk_generator_lobe(arabic_prompt_3)
    print(f"Result 3: {result_3}")

    print("\n--- Arabic APK Generator Lobe Demo Complete ---")
    # Clean up the dummy template directory after the demo if it was created.
    # In a real system, templates would be managed more robustly.
    # cleanup_android_project_template() # Uncomment if you want to clean up the dummy template dir

if __name__ == "__main__":
    # This part is for demonstration and testing the module in isolation.
    # In the grand objective, this Lobe would be called by a higher-level orchestrator.
    run_arabic_apk_generator_demo()

    # Clean up the generated projects after demo
    if os.path.exists(GENERATED_APK_DIR) and os.path.isdir(GENERATED_APK_DIR):
        print(f"\n--- Cleaning up generated projects in {GENERATED_APK_DIR} ---")
        # Be careful with recursive deletion in a real scenario!
        # For demo purposes, we can remove the whole directory.
        # shutil.rmtree(GENERATED_APK_DIR)
        # print(f"Cleaned up: {GENERATED_APK_DIR}")
        pass # Keep generated projects for inspection after demo run.