import os
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assume KNOWLEDGE_BASE_DIR is defined elsewhere, e.g.:
# KNOWLEDGE_BASE_DIR = "/path/to/your/knowledge_base"

def extract_java_code_from_arabic(arabic_text: str) -> tuple[str, str]:
    """
    Extracts Java code snippets and their descriptions from Arabic text.

    Args:
        arabic_text: The input Arabic text containing code and descriptions.

    Returns:
        A tuple containing two strings:
        - The extracted Java code.
        - The extracted Arabic description.
    """
    java_code = ""
    description = ""
    code_block_started = False
    code_pattern = re.compile(r'^java\n(.*?)\n$', re.DOTALL | re.MULTILINE)
    description_pattern = re.compile(r'^(.*?)\njava', re.DOTALL)

    match = code_pattern.search(arabic_text)
    if match:
        java_code = match.group(1).strip()

    match = description_pattern.search(arabic_text)
    if match:
        description = match.group(1).strip()

    # Refine extraction if the above patterns aren't perfect,
    # assuming descriptions precede code blocks.
    if not description and java_code:
        parts = arabic_text.split("java")
        if len(parts) > 0:
            description = parts[0].strip()
        if len(parts) > 1 and not java_code:
            # If code wasn't captured by the specific pattern, try to get it here
            code_segment = parts[1].split("")[0].strip()
            if code_segment:
                java_code = code_segment

    # A more robust approach might involve a dedicated Arabic NLP parser
    # to better distinguish code from natural language.
    # For now, we rely on markdown-like delimiters and heuristics.

    logging.info(f"Extracted Java code snippet (length: {len(java_code)}).")
    logging.info(f"Extracted Arabic description (length: {len(description)}).")

    return java_code, description

def generate_android_manifest_xml(package_name: str, app_name: str = "MyApp") -> str:
    """
    Generates a basic AndroidManifest.xml content.

    Args:
        package_name: The package name for the Android application.
        app_name: The name of the application.

    Returns:
        A string containing the XML content for AndroidManifest.xml.
    """
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name}">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    logging.info(f"Generated basic AndroidManifest.xml for package: {package_name}")
    return manifest_content

def create_android_project_structure(base_path: str, package_name: str):
    """
    Creates the basic directory structure for an Android project.

    Args:
        base_path: The root directory for the new project.
        package_name: The package name, used to derive directory paths.
    """
    package_path = os.path.join(base_path, "app", "src", "main", "java", *package_name.split('.'))
    resource_path = os.path.join(base_path, "app", "src", "main", "res")
    values_path = os.path.join(resource_path, "values")
    layout_path = os.path.join(resource_path, "layout")

    os.makedirs(package_path, exist_ok=True)
    os.makedirs(resource_path, exist_ok=True)
    os.makedirs(values_path, exist_ok=True)
    os.makedirs(layout_path, exist_ok=True)

    # Create essential placeholder files
    with open(os.path.join(base_path, "build.gradle"), "w") as f:
        f.write("// Project level build.gradle\n")
    with open(os.path.join(base_path, "settings.gradle"), "w") as f:
        f.write("rootProject.name = 'MyApp'\n")
    with open(os.path.join(base_path, "app", "build.gradle"), "w") as f:
        f.write("// App level build.gradle\n")
    with open(os.path.join(base_path, "app", "src", "main", "AndroidManifest.xml"), "w") as f:
        f.write(generate_android_manifest_xml(package_name))
    with open(os.path.join(values_path, "strings.xml"), "w") as f:
        f.write(f'<resources><string name="app_name">{package_name.split(".")[-1].capitalize()}</string></resources>')
    with open(os.path.join(layout_path, "activity_main.xml"), "w") as f:
        f.write(f'<resources><TextView android:layout_width=\"wrap_content\" android:layout_height=\"wrap_content\" text=\"Hello World!\" /></resources>')

    # Create a dummy MainActivity if it doesn't exist in the extracted code
    main_activity_path = os.path.join(package_path, "MainActivity.java")
    if not os.path.exists(main_activity_path):
        with open(main_activity_path, "w") as f:
            f.write(f"package {package_name};\n\n"
                    "import androidx.appcompat.app.AppCompatActivity;\n"
                    "import android.os.Bundle;\n\n"
                    f"public class MainActivity extends AppCompatActivity {{\n"
                    "    @Override\n"
                    "    protected void onCreate(Bundle savedInstanceState) {\n"
                    "        super.onCreate(savedInstanceState);\n"
                    "        setContentView(R.layout.activity_main);\n"
                    "    }\n"
                    "}\n")

    logging.info(f"Created Android project structure at: {base_path}")

class ArabicNLPBuilder:
    """
    A module for processing Arabic natural language to generate Android APK components.
    This acts as a conceptual bridge between Lobe 0 (Language) and Lobe 8 (APK Compiler).
    """
    def __init__(self, project_base_dir: str):
        self.project_base_dir = project_base_dir
        self.current_package_name = None
        self.generated_code = {} # Stores generated Java code and XML

    def process_arabic_instruction(self, arabic_instruction: str):
        """
        Processes an Arabic natural language instruction to generate APK components.

        Args:
            arabic_instruction: The Arabic text containing instructions for app development.
        """
        logging.info(f"Processing Arabic instruction: '{arabic_instruction[:50]}...'")

        # 1. Extract package name and app name
        # This is a simplified extraction. A more advanced NLP model would be needed.
        package_match = re.search(r'لإنشاء تطبيق باسم ([\w.]+)', arabic_instruction)
        app_name_match = re.search(r'اسم التطبيق هو ([\w\s]+)', arabic_instruction)

        if package_match:
            self.current_package_name = package_match.group(1)
            logging.info(f"Identified package name: {self.current_package_name}")
        else:
            logging.warning("Could not identify package name from instruction. Using a default.")
            self.current_package_name = "com.example.generatedapp"

        app_name = "GeneratedApp"
        if app_name_match:
            app_name = app_name_match.group(1).strip()
            logging.info(f"Identified app name: {app_name}")

        # 2. Create project structure
        project_path = os.path.join(self.project_base_dir, app_name.replace(" ", "_").lower())
        os.makedirs(project_path, exist_ok=True)
        create_android_project_structure(project_path, self.current_package_name)
        logging.info(f"Created project structure at: {project_path}")

        # 3. Extract Java code and descriptions
        java_code, description = extract_java_code_from_arabic(arabic_instruction)

        if java_code:
            # Assume the extracted code is for MainActivity unless specified otherwise
            # A more sophisticated parser would identify components by name.
            activity_file_path = os.path.join(project_path, "app", "src", "main", "java", *self.current_package_name.split('.'))
            if not os.path.exists(activity_file_path):
                os.makedirs(activity_file_path, exist_ok=True)
            main_activity_java_path = os.path.join(activity_file_path, "MainActivity.java")

            # Check if we are overwriting a default MainActivity or adding new code
            existing_content = ""
            if os.path.exists(main_activity_java_path):
                with open(main_activity_java_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()

            if "MainActivity" in existing_content or "public class MainActivity" in existing_content:
                # Try to merge or replace relevant parts of MainActivity
                # This is a placeholder for complex code merging logic
                logging.warning("Detected existing MainActivity. Basic replacement will occur. Advanced merging not implemented.")
                with open(main_activity_java_path, "w", encoding='utf-8') as f:
                    # Simple replacement for demonstration; a real system would parse and merge
                    f.write(f"package {self.current_package_name};\n\n")
                    f.write(java_code)
                self.generated_code["MainActivity.java"] = java_code
            else:
                # Write extracted code to a new file or as MainActivity
                with open(main_activity_java_path, "w", encoding='utf-8') as f:
                    f.write(f"package {self.current_package_name};\n\n")
                    f.write(java_code)
                self.generated_code["MainActivity.java"] = java_code

            logging.info(f"Saved extracted Java code to: {main_activity_java_path}")

        # 4. Handle descriptions for resources (e.g., layouts, strings)
        # This part requires more advanced parsing to map descriptions to specific resource files.
        # For now, we'll log the description and acknowledge it.
        if description:
            logging.info(f"Description provided: {description}")
            # In a real scenario, this description would be used to generate or modify
            # XML files (e.g., activity_main.xml, strings.xml) or other resources.
            # Example: if description talks about a button, parse that and update activity_main.xml.

        logging.info("Finished processing Arabic instruction.")

    def get_generated_project_path(self) -> str | None:
        """Returns the path of the last generated project."""
        if self.current_package_name:
            app_name = self.current_package_name.split('.')[-1].capitalize()
            return os.path.join(self.project_base_dir, app_name.replace(" ", "_").lower())
        return None

    def cleanup_project(self, project_path: str):
        """
        Cleans up a generated project directory.

        Args:
            project_path: The path to the project directory to remove.
        """
        if os.path.exists(project_path):
            try:
                import shutil
                shutil.rmtree(project_path)
                logging.info(f"Successfully cleaned up project directory: {project_path}")
            except Exception as e:
                logging.error(f"Error cleaning up project directory {project_path}: {e}")
        else:
            logging.warning(f"Project directory not found for cleanup: {project_path}")

# Example Usage (for demonstration within this module's scope):
if __name__ == "__main__":
    # Define a dummy KNOWLEDGE_BASE_DIR for the example
    KNOWLEDGE_BASE_DIR = "./dummy_knowledge_base"
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

    # Define a temporary directory for generated projects
    GENERATED_PROJECTS_ROOT = "./generated_android_projects"
    os.makedirs(GENERATED_PROJECTS_ROOT, exist_ok=True)

    builder = ArabicNLPBuilder(GENERATED_PROJECTS_ROOT)

    # Example Arabic instruction incorporating Java code
    arabic_instruction_1 = """
    أريد إنشاء تطبيق أندرويد باسم com.example.myapp.
    اسم التطبيق هو My Awesome App.
    الكود التالي يجب أن يكون في MainActivity:
    java
    import android.widget.TextView;
    import android.util.Log;

    public class MainActivity extends AppCompatActivity {
        private static final String TAG = "MainActivity";

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            // Use a predefined layout
            setContentView(R.layout.activity_main);

            TextView textView = findViewById(R.id.textView); // Assuming an element with this ID exists
            textView.setText("Hello from Arabic NLP!");
            Log.d(TAG, "MainActivity created and text set.");
        }
    }
    
    الوصف: هذا الكود يقوم بتهيئة الشاشة الرئيسية ويعرض رسالة ترحيب مخصصة.
    """

    print("\n--- Processing Instruction 1 ---")
    builder.process_arabic_instruction(arabic_instruction_1)
    project_path_1 = builder.get_generated_project_path()
    print(f"Generated project at: {project_path_1}")

    # Example Arabic instruction for a different app, potentially adding a new activity or modifying existing
    arabic_instruction_2 = """
    قم بتعديل التطبيق com.example.myapp.
    أضف زرًا إلى الشاشة الرئيسية.
    java
    // Modified MainActivity snippet
    import android.widget.Button;
    import android.view.View;
    import android.widget.Toast;

    // ... (rest of the MainActivity code)

            Button myButton = findViewById(R.id.myButton); // Assuming this button ID will be added to layout
            myButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Toast.makeText(MainActivity.this, "Button Clicked!", Toast.LENGTH_SHORT).show();
                    Log.d(TAG, "Custom button clicked.");
                }
            });
    // ... (rest of the MainActivity code)
    
    الوصف: يجب أن يظهر زر جديد عند تشغيل التطبيق، وعند الضغط عليه يعرض رسالة قصيرة.
    """
    # Note: This instruction implies modifying the layout and potentially the MainActivity.
    # The current `extract_java_code_from_arabic` is basic and might not perfectly handle
    # incremental updates or layout modifications without explicit instructions.
    # The `process_arabic_instruction` will likely overwrite MainActivity based on current logic.
    print("\n--- Processing Instruction 2 (demonstrating overwriting/basic update) ---")
    builder.process_arabic_instruction(arabic_instruction_2)
    project_path_2 = builder.get_generated_project_path() # Should be the same path as project_path_1 if package is same
    print(f"Updated project structure at: {project_path_2}")


    # Clean up generated projects
    print("\n--- Cleaning up all generated projects ---")
    if project_path_1:
        builder.cleanup_project(project_path_1)
    if project_path_2 and project_path_2 != project_path_1: # Avoid double cleanup if paths are same
         builder.cleanup_project(project_path_2)

    # Clean up dummy directories
    if os.path.exists(GENERATED_PROJECTS_ROOT):
        try:
            import shutil
            shutil.rmtree(GENERATED_PROJECTS_ROOT)
            logging.info(f"Cleaned up root directory: {GENERATED_PROJECTS_ROOT}")
        except Exception as e:
            logging.error(f"Error cleaning up {GENERATED_PROJECTS_ROOT}: {e}")
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        try:
            import shutil
            shutil.rmtree(KNOWLEDGE_BASE_DIR)
            logging.info(f"Cleaned up root directory: {KNOWLEDGE_BASE_DIR}")
        except Exception as e:
            logging.error(f"Error cleaning up {KNOWLEDGE_BASE_DIR}: {e}")

    print("\n--- Arabic NLP Builder Module Demo Finished ---")