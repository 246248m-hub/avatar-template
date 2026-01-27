import os
import subprocess
from pathlib import Path

# Assume KNOWLEDGE_BASE_DIR is defined and accessible, similar to other lobes.
# For demonstration, we'll define it here.
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
if not KNOWLEDGE_BASE_DIR.exists():
    KNOWLEDGE_BASE_DIR.mkdir()

def extract_arabic_components(natural_language_prompt: str) -> dict:
    """
    Analyzes an Arabic natural language prompt to extract key components
    required for APK generation. This includes UI elements, their properties,
    and basic logic.

    Args:
        natural_language_prompt: The input prompt in Arabic.

    Returns:
        A dictionary containing extracted components like 'ui_elements',
        'layout_instructions', 'event_handlers', etc.
    """
    # This is a placeholder for actual NLP processing.
    # In a real scenario, this would involve:
    # 1. Tokenization and POS tagging of Arabic text.
    # 2. Named Entity Recognition (NER) to identify UI elements (buttons, text fields, etc.).
    # 3. Dependency parsing to understand relationships between words and phrases.
    # 4. Semantic role labeling to identify actions and their targets.
    # 5. Rule-based or ML-based extraction of layout, styling, and interaction logic.

    extracted_data = {
        "ui_elements": [],
        "layout_instructions": [],
        "event_handlers": [],
        "permissions": []
    }

    # Example extraction logic (highly simplified for demonstration)
    # A real implementation would use sophisticated Arabic NLP libraries.
    if "زر" in natural_language_prompt and "اضغط" in natural_language_prompt:
        extracted_data["ui_elements"].append({"type": "Button", "id": "submit_button", "text": "اضغط هنا"})
        extracted_data["event_handlers"].append({"element_id": "submit_button", "event": "onClick", "action": "show_message"})
        extracted_data["permissions"].append("INTERNET") # Example: if message display requires network

    if "حقل نص" in natural_language_prompt or "ادخل" in natural_language_prompt:
        extracted_data["ui_elements"].append({"type": "EditText", "id": "user_input", "hint": "ادخل النص"})
        extracted_data["layout_instructions"].append({"element_id": "user_input", "position": "top"})

    if "رسالة" in natural_language_prompt:
        extracted_data["ui_elements"].append({"type": "TextView", "id": "message_display", "text": ""})
        extracted_data["layout_instructions"].append({"element_id": "message_display", "position": "center"})

    print(f"DEBUG: Extracted Arabic components: {extracted_data}")
    return extracted_data

def assemble_android_manifest(permissions: list) -> str:
    """
    Generates a basic AndroidManifest.xml content based on extracted permissions.

    Args:
        permissions: A list of required Android permissions.

    Returns:
        A string containing the XML content of AndroidManifest.xml.
    """
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.generatedapp">

    <uses-permission android:name="android.permission.INTERNET"/>
"""
    # Add other permissions if specified
    for perm in permissions:
        manifest_content += f'    <uses-permission android:name="android.permission.{perm}"/>\n'

    manifest_content += """
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp">
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
    return manifest_content

def generate_layout_xml(ui_elements: list, layout_instructions: list) -> str:
    """
    Generates a basic activity_main.xml layout file content.

    Args:
        ui_elements: A list of UI elements with their types and properties.
        layout_instructions: A list of instructions for element positioning.

    Returns:
        A string containing the XML content for activity_main.xml.
    """
    layout_start = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">
"""
    layout_elements = []
    element_map = {elem['id']: elem for elem in ui_elements}
    pos_map = {inst['element_id']: inst['position'] for inst in layout_instructions}

    for elem_data in ui_elements:
        elem_id = elem_data.get("id", f"generated_id_{len(layout_elements)}")
        elem_type = elem_data.get("type", "TextView")
        elem_text = elem_data.get("text", "")
        elem_hint = elem_data.get("hint", "")
        elem_attrs = f'android:id="@+id/{elem_id}"'

        if elem_type == "Button":
            elem_attrs += f' android:text="{elem_text}"'
            layout_elements.append(f'<Button {elem_attrs} app:layout_constraintTop_toTopOf="parent" app:layout_constraintStart_toStartOf="parent"/>')
        elif elem_type == "EditText":
            elem_attrs += f' android:hint="{elem_hint}" android:inputType="text"'
            layout_elements.append(f'<EditText {elem_attrs} app:layout_constraintTop_toTopOf="parent" app:layout_constraintStart_toStartOf="parent"/>')
        elif elem_type == "TextView":
            elem_attrs += f' android:text="{elem_text}"'
            layout_elements.append(f'<TextView {elem_attrs} app:layout_constraintTop_toTopOf="parent" app:layout_constraintStart_toStartOf="parent"/>')
        else:
            layout_elements.append(f'<!-- Unsupported element type: {elem_type} -->')

    # Basic positioning logic (very rudimentary)
    for i, elem_id in enumerate(element_map.keys()):
        if i < len(layout_elements):
            position = pos_map.get(elem_id, "top")
            constraint_layout_params = ""
            if position == "top":
                constraint_layout_params = 'app:layout_constraintTop_toTopOf="parent"'
            elif position == "center":
                constraint_layout_params = 'app:layout_constraintTop_toTopOf="parent" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent"'

            # Replace the placeholder constraint with actual positioning
            layout_elements[i] = layout_elements[i].replace('app:layout_constraintTop_toTopOf="parent" app:layout_constraintStart_toStartOf="parent"', constraint_layout_params)


    layout_end = """
</androidx.constraintlayout.widget.ConstraintLayout>
"""
    return layout_start + "\n".join(layout_elements) + layout_end

def generate_main_activity_java(event_handlers: list) -> str:
    """
    Generates a basic MainActivity.java content.

    Args:
        event_handlers: A list of event handlers to be implemented.

    Returns:
        A string containing the Java code for MainActivity.java.
    """
    java_code = """package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import android.widget.EditText; // Import EditText
import android.widget.Button; // Import Button

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

"""
    # Implement event handlers
    for handler in event_handlers:
        element_id = handler.get("element_id")
        event_type = handler.get("event")
        action = handler.get("action")

        if element_id and event_type == "onClick":
            java_code += f"""
        Button {element_id}Button = findViewById(R.id.{element_id});
        {element_id}Button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                // Action: {action}
"""
            if action == "show_message":
                java_code += """
                EditText userInputField = findViewById(R.id.user_input); // Assuming user_input is an EditText
                String message = "رسالة من التطبيق!";
                if (userInputField != null && userInputField.getText().length() > 0) {
                    message = userInputField.getText().toString();
                }
                Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
"""
            # Add more actions here
            java_code += """
            }
        }});
"""

    java_code += """
    }
}
"""
    return java_code

class Lobe3_arabic_processor:
    def __init__(self):
        print("Lobe 3: Arabic Processor Initialized.")

    def process_prompt(self, natural_language_prompt: str, output_dir: Path):
        """
        Processes the Arabic natural language prompt to generate Android project components.

        Args:
            natural_language_prompt: The input prompt in Arabic.
            output_dir: The directory where generated files will be saved.
        """
        print(f"\n--- Lobe 3: Processing Arabic Prompt ---")
        print(f"Prompt: '{natural_language_prompt}'")

        # 1. Extract components from Arabic prompt
        extracted_components = extract_arabic_components(natural_language_prompt)
        ui_elements = extracted_components.get("ui_elements", [])
        layout_instructions = extracted_components.get("layout_instructions", [])
        event_handlers = extracted_components.get("event_handlers", [])
        permissions = extracted_components.get("permissions", [])

        if not ui_elements and not layout_instructions and not event_handlers:
            print("No significant UI or interaction components extracted. Skipping APK generation for this prompt.")
            return

        # 2. Generate Android Manifest
        manifest_content = assemble_android_manifest(permissions)
        manifest_path = output_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"Generated: {manifest_path}")

        # 3. Generate Layout XML
        layout_xml_content = generate_layout_xml(ui_elements, layout_instructions)
        layout_path = output_dir / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        layout_path.parent.mkdir(parents=True, exist_ok=True)
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_xml_content)
        print(f"Generated: {layout_path}")

        # 4. Generate MainActivity Java
        main_activity_java_content = generate_main_activity_java(event_handlers)
        java_dir = output_dir / "app" / "src" / "main" / "java" / "com" / "example" / "generatedapp"
        java_dir.mkdir(parents=True, exist_ok=True)
        main_activity_java_path = java_dir / "MainActivity.java"
        with open(main_activity_java_path, "w", encoding="utf-8") as f:
            f.write(main_activity_java_content)
        print(f"Generated: {main_activity_java_path}")

        print("--- Lobe 3: Arabic Prompt Processing Complete ---")

# Example Usage (can be called from another lobe)
if __name__ == "__main__":
    # Create a dummy output directory for demonstration
    DEMO_OUTPUT_DIR = Path("./generated_android_project")
    DEMO_OUTPUT_DIR.mkdir(exist_ok=True)
    (DEMO_OUTPUT_DIR / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
    (DEMO_OUTPUT_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "generatedapp").mkdir(parents=True, exist_ok=True)


    arabic_processor = Lobe3_arabic_processor()

    # Example Arabic prompts
    prompt_1 = "انشئ تطبيقاً بسيطاً يحتوي على زر اضغط عليه لعرض رسالة ترحيبية."
    prompt_2 = "اريد شاشة بها حقل نصي لادخال اسمي وزر ليقول مرحباً باسمي."
    prompt_3 = "قم ببناء واجهة بها زر واحد فقط."

    arabic_processor.process_prompt(prompt_1, DEMO_OUTPUT_DIR)
    arabic_processor.process_prompt(prompt_2, DEMO_OUTPUT_DIR)
    arabic_processor.process_prompt(prompt_3, DEMO_OUTPUT_DIR)

    print("\n--- Lobe 3 Demo Finished ---")

    # Clean up dummy directory
    # import shutil
    # shutil.rmtree(DEMO_OUTPUT_DIR)