import os
import re
import subprocess
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

class ArabicApkGenerator:
    def __init__(self, template_dir="templates", output_dir="generated_apks"):
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        os.makedirs(self.output_dir, exist_ok=True)

    def parse_arabic_description(self, description):
        """
        Parses Arabic natural language descriptions to extract app features.
        Currently focuses on identifying UI elements and their basic properties.
        """
        app_name = "MyArabicApp"
        ui_elements = []

        # Basic parsing for app name (can be expanded)
        name_match = re.search(r"اسم التطبيق هو (.+?)\.", description)
        if name_match:
            app_name = name_match.group(1).strip()

        # Parsing for text fields
        if "حقل نصي" in description or "حقل ادخال" in description:
            field_label = "Enter Text"
            field_type = "EditText"
            if "لاضافة ملاحظة" in description:
                field_label = "Note"
            ui_elements.append({"type": field_type, "label": field_label, "id": "editText1"})

        # Parsing for buttons
        if "زر للحفظ" in description or "زر للاضافة" in description or "زر للارسال" in description:
            button_text = "Save"
            if "زر للحفظ" in description:
                button_text = "Save"
            elif "زر للاضافة" in description:
                button_text = "Add"
            elif "زر للارسال" in description:
                button_text = "Send"
            ui_elements.append({"type": "Button", "text": button_text, "id": "button1"})

        # More complex parsing can be added here for layouts, images, etc.

        return {"app_name": app_name, "ui_elements": ui_elements}

    def generate_layout_xml(self, ui_elements, app_name):
        """Generates an Android XML layout file from parsed UI elements."""
        layout_template = self.env.get_template("activity_main.xml.j2")
        layout_content = layout_template.render(ui_elements=ui_elements, app_name=app_name)

        layout_file_path = os.path.join(self.output_dir, f"res/layout/activity_main.xml")
        os.makedirs(os.path.dirname(layout_file_path), exist_ok=True)
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_content)
        return layout_file_path

    def generate_manifest_xml(self, app_name):
        """Generates a basic AndroidManifest.xml file."""
        manifest_template = self.env.get_template("AndroidManifest.xml.j2")
        manifest_content = manifest_template.render(package_name=f"com.example.{app_name.lower().replace(' ', '')}")

        manifest_file_path = os.path.join(self.output_dir, "AndroidManifest.xml")
        with open(manifest_file_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        return manifest_file_path

    def generate_activity_java(self, app_name, ui_elements):
        """Generates a basic Java Activity file."""
        activity_template = self.env.get_template("MainActivity.java.j2")
        activity_content = activity_template.render(app_name=app_name, ui_elements=ui_elements, package_name=f"com.example.{app_name.lower().replace(' ', '')}")

        activity_file_path = os.path.join(self.output_dir, f"java/com/example/{app_name.lower().replace(' ', '')}/MainActivity.java")
        os.makedirs(os.path.dirname(activity_file_path), exist_ok=True)
        with open(activity_file_path, "w", encoding="utf-8") as f:
            f.write(activity_content)
        return activity_file_path

    def create_project_structure(self, app_data):
        """Creates the necessary directory structure for an Android project."""
        app_name = app_data["app_name"]
        package_name_part = app_name.lower().replace(' ', '')
        project_root = os.path.join(self.output_dir, f"{app_name.replace(' ', '')}Project")
        os.makedirs(os.path.join(project_root, "app/src/main/res/layout"), exist_ok=True)
        os.makedirs(os.path.join(project_root, f"app/src/main/java/com/example/{package_name_part}"), exist_ok=True)
        return project_root, f"com.example.{package_name_part}"

    def generate_apk(self, arabic_description):
        """
        Orchestrates the generation of an APK from an Arabic description.
        This is a simplified process and would involve more sophisticated
        build tools and configurations for a real-world scenario.
        """
        print(f"\n--- Generating APK for: '{arabic_description}' ---")
        app_data = self.parse_arabic_description(arabic_description)
        app_name = app_data["app_name"]
        ui_elements = app_data["ui_elements"]

        project_root, package_name = self.create_project_structure(app_data)

        # Generate layout
        layout_path = self.generate_layout_xml(ui_elements, app_name)
        print(f"Generated layout file: {layout_path}")

        # Generate manifest
        manifest_path = self.generate_manifest_xml(app_name)
        print(f"Generated manifest file: {manifest_path}")

        # Generate activity
        activity_path = self.generate_activity_java(app_name, ui_elements)
        print(f"Generated activity file: {activity_path}")

        print(f"Project structure created at: {project_root}")
        print("Note: Actual APK compilation requires an Android SDK and build tools.")
        print("This function generates the source files and project structure.")
        return project_root, app_name

    def cleanup_generated_apks(self):
        """Cleans up the generated APKs and project structures."""
        print("\n--- Cleaning up generated APKs and project structures ---")
        for item in os.listdir(self.output_dir):
            item_path = os.path.join(self.output_dir, item)
            if os.path.isdir(item_path):
                try:
                    import shutil
                    shutil.rmtree(item_path)
                    print(f"Removed directory: {item_path}")
                except OSError as e:
                    print(f"Error removing directory {item_path}: {e}")
            else:
                try:
                    os.remove(item_path)
                    print(f"Removed file: {item_path}")
                except OSError as e:
                    print(f"Error removing file {item_path}: {e}")
        print("Cleanup complete.")


# --- Example Usage ---
if __name__ == "__main__":
    # Ensure templates directory exists and contains necessary Jinja2 templates
    # For demonstration purposes, let's create dummy templates if they don't exist
    if not os.path.exists("templates"):
        os.makedirs("templates")

    # Create dummy activity_main.xml.j2
    if not os.path.exists("templates/activity_main.xml.j2"):
        with open("templates/activity_main.xml.j2", "w", encoding="utf-8") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{{ app_name }}"
        android:textSize="24sp"
        android:layout_gravity="center_horizontal"
        android:layout_marginBottom="24dp"/>

    {% for element in ui_elements %}
        {% if element.type == 'EditText' %}
            <EditText
                android:id="@+id/{{ element.id }}"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:hint="{{ element.label }}"
                android:layout_marginBottom="16dp"/>
        {% elif element.type == 'Button' %}
            <Button
                android:id="@+id/{{ element.id }}"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="{{ element.text }}"
                android:layout_marginBottom="16dp"/>
        {% endif %}
    {% endfor %}

</LinearLayout>
""")

    # Create dummy AndroidManifest.xml.j2
    if not os.path.exists("templates/AndroidManifest.xml.j2"):
        with open("templates/AndroidManifest.xml.j2", "w", encoding="utf-8") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{{ package_name }}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{{ app_name | replace(' ', '') }}"
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
""")

    # Create dummy MainActivity.java.j2
    if not os.path.exists("templates/MainActivity.java.j2"):
        with open("templates/MainActivity.java.j2", "w", encoding="utf-8") as f:
            f.write("""package {{ package_name }};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Find UI elements
        {% for element in ui_elements %}
            {% if element.type == 'EditText' %}
                EditText {{ element.id }} = findViewById(R.id.{{ element.id }});
            {% elif element.type == 'Button' %}
                Button {{ element.id }} = findViewById(R.id.{{ element.id }});
            {% endif %}
        {% endfor %}

        // Set up button listeners
        {% for element in ui_elements %}
            {% if element.type == 'Button' %}
                {{ element.id }}.setOnClickListener(v -> {
                    // Action for {{ element.text }} button
                    {% if element.text == 'Save' %}
                        // Example: get text from EditText and show a toast
                        {% for inner_element in ui_elements %}
                            {% if inner_element.type == 'EditText' %}
                                String note = {{ inner_element.id }}.getText().toString();
                                Toast.makeText(this, "Note saved: " + note, Toast.LENGTH_LONG).show();
                                break; // Assuming only one EditText for simplicity
                            {% endif %}
                        {% endfor %}
                    {% else %}
                        Toast.makeText(this, "{{ element.text }} button clicked", Toast.LENGTH_SHORT).show();
                    {% endif %}
                });
            {% endif %}
        {% endfor %}
    }
}
""")


    arabic_generator = ArabicApkGenerator()

    # Example 1: Simple note-taking app
    arabic_description_1 = "اسم التطبيق هو مفكرة بسيطة. يجب ان يكون هناك حقل نصي لاضافة ملاحظة وزر للحفظ."
    project_root_1, app_name_1 = arabic_generator.generate_apk(arabic_description_1)

    # Example 2: App with a title and a send button
    arabic_description_2 = "اسم التطبيق هو رسالة. يجب ان يكون هناك حقل ادخال للرسالة وزر للارسال."
    project_root_2, app_name_2 = arabic_generator.generate_apk(arabic_description_2)

    # Clean up the generated files after demonstrations
    arabic_generator.cleanup_generated_apks()

    print("\n--- Arabic APK Generation Module Demo Finished ---")