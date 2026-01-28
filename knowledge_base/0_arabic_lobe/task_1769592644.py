import os
import xml.etree.ElementTree as ET

class AndroidManifestParser:
    def __init__(self, manifest_path="AndroidManifest.xml"):
        self.manifest_path = manifest_path
        self.tree = None
        self.root = None

    def parse(self):
        """Parses the AndroidManifest.xml file."""
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"AndroidManifest.xml not found at {self.manifest_path}")
        self.tree = ET.parse(self.manifest_path)
        self.root = self.tree.getroot()

    def get_package_name(self):
        """Retrieves the package name from the manifest."""
        if self.root is None:
            self.parse()
        return self.root.get('package')

    def get_activities(self):
        """Retrieves a list of all activities defined in the manifest."""
        if self.root is None:
            self.parse()
        activities = []
        for application in self.root.findall('application'):
            for activity in application.findall('activity'):
                activities.append({
                    'name': activity.get('{http://schemas.android.com/apk/res/android}name'),
                    'label': activity.get('{http://schemas.android.com/apk/res/android}label')
                })
        return activities

    def get_main_launcher_activity(self):
        """Finds the activity that is set as the main launcher."""
        if self.root is None:
            self.parse()
        for application in self.root.findall('application'):
            for activity in application.findall('activity'):
                for intent_filter in activity.findall('intent-filter'):
                    actions = intent_filter.findall('action')
                    categories = intent_filter.findall('category')
                    is_main = any(action.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.action.MAIN' for action in actions)
                    is_launcher = any(category.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.category.LAUNCHER' for category in categories)
                    if is_main and is_launcher:
                        return activity.get('{http://schemas.android.com/apk/res/android}name')
        return None

    def update_package_name(self, new_package_name):
        """Updates the package name in the manifest."""
        if self.root is None:
            self.parse()
        self.root.set('package', new_package_name)
        self.save()

    def add_activity(self, activity_name, label=None):
        """Adds a new activity to the manifest."""
        if self.root is None:
            self.parse()
        application_node = self.root.find('application')
        if application_node is None:
            application_node = ET.SubElement(self.root, 'application')

        activity_element = ET.SubElement(application_node, 'activity', {
            '{http://schemas.android.com/apk/res/android}name': activity_name
        })
        if label:
            activity_element.set('{http://schemas.android.com/apk/res/android}label', label)
        self.save()

    def save(self, output_path="AndroidManifest.xml"):
        """Saves the modified manifest to a file."""
        if self.tree is None:
            raise ValueError("Manifest not parsed yet. Call parse() first.")
        self.tree.write(output_path, encoding='utf-8', xml_declaration=True)


class ArabicAPKBuilder:
    def __init__(self, project_name="MyArabicApp", package_name="com.example.myarabicapp", output_dir="build"):
        self.project_name = project_name
        self.package_name = package_name
        self.output_dir = output_dir
        self.manifest_parser = AndroidManifestParser()
        self.generated_code_files = {} # {filename: content}

    def setup_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        if not os.path.exists(self.output_dir):
            os.makedirs(os.path.join(self.output_dir, "app", "src", "main", "java", *self.package_name.split('.')))
            os.makedirs(os.path.join(self.output_dir, "app", "src", "main", "res", "layout"))
            os.makedirs(os.path.join(self.output_dir, "app", "src", "main", "res", "values"))

    def create_android_manifest(self):
        """Creates a basic AndroidManifest.xml file."""
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{self.project_name}">

        <!-- Main Launcher Activity will be added dynamically -->

    </application>
</manifest>
"""
        manifest_path = os.path.join(self.output_dir, "app", "src", "main", "AndroidManifest.xml")
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        self.manifest_parser = AndroidManifestParser(manifest_path)
        self.manifest_parser.parse()

    def create_string_resources(self):
        """Creates basic string resources, including app_name."""
        values_dir = os.path.join(self.output_dir, "app", "src", "main", "res", "values")
        strings_xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{self.project_name}</string>
    <!-- Other strings will be added here -->
</resources>
"""
        with open(os.path.join(values_dir, "strings.xml"), "w", encoding="utf-8") as f:
            f.write(strings_xml_content)

    def generate_main_activity(self, prompt_text="مرحباً بالعالم"):
        """Generates the main activity for displaying Arabic text."""
        activity_name = "MainActivity"
        java_package_path = os.path.join(self.output_dir, "app", "src", "main", "java", *self.package_name.split('.'))
        activity_file_path = os.path.join(java_package_path, f"{activity_name}.java")

        activity_java_code = f"""package {self.package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textViewGreeting);
        textView.setText("{prompt_text}");
    }}
}}
"""
        self.generated_code_files[activity_file_path] = activity_java_code

        # Create layout file
        layout_file_path = os.path.join(self.output_dir, "app", "src", "main", "res", "layout", "activity_main.xml")
        layout_xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/textViewGreeting"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text=""
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        self.generated_code_files[layout_file_path] = layout_xml_content

        # Add activity to manifest
        self.manifest_parser.add_activity(f".{activity_name}", label="@string/app_name")

        # Set this activity as the main launcher
        intent_filter_code = """
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
"""
        # This is a simplification. In a real scenario, you'd modify the existing activity entry
        # or add the intent filter more programmatically. For this example, we'll manually
        # update the manifest content string and re-parse if needed, or better, add a method
        # to AndroidManifestParser to add intent filters.

        # Let's add a method to AndroidManifestParser for this
        self.manifest_parser.add_intent_filter_to_activity(f".{activity_name}", intent_filter_code)
        self.manifest_parser.save() # Save the updated manifest

        return activity_name

    def build_apk(self):
        """Simulates the APK building process by saving generated files."""
        self.setup_project_structure()
        self.create_android_manifest()
        self.create_string_resources()

        # Example: Generate main activity for a prompt like "مرحباً بالعالم"
        main_activity_name = self.generate_main_activity("مرحباً بالعالم")

        # Write all generated code files
        for file_path, content in self.generated_code_files.items():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"--- APK build simulation complete for '{self.project_name}' ---")
        print(f"Project structure created in: {os.path.abspath(self.output_dir)}")
        print(f"Generated files:")
        for file_path in self.generated_code_files:
            print(f"- {os.path.abspath(file_path)}")
        print(f"AndroidManifest.xml generated/updated at: {os.path.abspath(self.output_dir)}/app/src/main/AndroidManifest.xml")


# Example usage (demonstrates the module's functionality)
if __name__ == "__main__":
    # This part is for demonstration and would not be in the final exported module
    # when it's integrated into the grand objective.

    # Mocking the existence of a KNOWLEDGE_BASE_DIR for demonstration if needed
    KNOWLEDGE_BASE_DIR = "./knowledge_base"
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)

    # --- Demonstration of Lobe 0_arabic_lobe ---
    print("--- Arabic Lobe Demonstration ---")
    # In a real scenario, this would involve complex Arabic parsing
    # For this demo, we'll just simulate processing a prompt.
    class MockArabicGenerator:
        def process_arabic_input(self, prompt):
            print(f"Mock processing Arabic prompt: '{prompt}'")
            # Simulate generating some structured output or code snippet
            if "مرحبا بالعالم" in prompt:
                return {"activity_name": "MainActivity", "layout_id": "textViewGreeting", "text_to_display": "مرحباً بالعالم"}
            return {}

    arabic_generator = MockArabicGenerator()
    prompt_5 = "أريد عرض نص 'مرحبا بالعالم' على الشاشة"
    processed_data = arabic_generator.process_arabic_input(prompt_5)

    # --- Demonstration of Lobe 4_code_generation_lobe (simplified) ---
    print("\n--- Simplified Code Generation Lobe Demonstration ---")
    # This would typically be more sophisticated, translating NLP to code
    # Here, we assume processed_data directly informs APK building.

    # --- Demonstration of Lobe 6_synthesis_lobe (simplified) ---
    print("\n--- Initiating APK Build with Lobe 8_apk_compiler_lobe ---")

    # Assume processed_data from Arabic Lobe informs the APK Builder
    app_builder = ArabicAPKBuilder(
        project_name="HelloArabicApp",
        package_name="com.arabic.hello.world",
        output_dir="./build_output"
    )
    if processed_data and 'text_to_display' in processed_data:
        # We can pass the generated text directly to the builder
        app_builder.generate_main_activity(prompt_text=processed_data['text_to_display'])

    # The build_apk method now encapsulates the creation of project structure, manifest,
    # resources, and Java/XML code.
    app_builder.build_apk()

    # --- Mocking cleanup for demonstration ---
    print("\n--- Mocking Cleanup ---")
    # In a real integration, this would remove temporary files if any were created.
    # For now, we'll just print a message.
    print("Mock cleanup executed.")

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

    # --- Demonstration of Lobe 8_apk_compiler_lobe ---
    print("\n--- APK Compiler Lobe Demonstration ---")

    class MockDebugKeystore:
        def __init__(self):
            self.message = "Mocking debug.keystore"

    # Simulate the condition checked in Lobe 8
    global_vars = {}
    global_vars['__builtins__'] = {}
    global_vars['__builtins__']['print'] = lambda *args, **kwargs: print(*args, **kwargs)
    global_vars['__builtins__']['print'].__self__ = MockDebugKeystore() # Mocking print behavior

    debug_keystore_path = None # In a real scenario, this would be a Path object
    # Simulate the condition check:
    if global_vars.get('__builtins__', {}).get('print', lambda *args, **kwargs: None).__self__.message.split('\n')[-1] == "Mocking debug.keystore":
        print("Simulating debug.keystore cleanup...")
        # In a real scenario:
        # if debug_keystore_path and debug_keystore_path.exists():
        #     debug_keystore_path.unlink()
        #     if debug_keystore_path.parent and not list(debug_keystore_path.parent.iterdir()):
        #         debug_keystore_path.parent.rmdir()
        print("Mocked debug.keystore cleaned up.")

    print("\n--- APK Compiler Lobe Demonstration Finished ---")