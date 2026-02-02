import os
import json
import subprocess
from pathlib import Path

# Assume these helper functions are defined elsewhere and available
# from core_utils import execute_command, create_directory_if_not_exists, load_json, save_json, cleanup_directory

# Placeholder for actual NLP model integration
def analyze_arabic_text_for_ui_elements(text: str) -> dict:
    """
    Analyzes Arabic natural language text to identify potential UI elements
    (e.g., buttons, text fields, labels, layouts) and their properties.

    Args:
        text: The Arabic natural language input.

    Returns:
        A dictionary representing the parsed UI elements and their configurations.
        Example:
        {
            "elements": [
                {"type": "TextView", "text": "مرحباً بالعالم", "id": "welcome_text", "layout_gravity": "center"},
                {"type": "Button", "text": "اضغط هنا", "id": "submit_button", "on_click": "handleSubmit"}
            ],
            "layout": {"orientation": "vertical", "gravity": "center"}
        }
    """
    # --- REAL LOGIC START ---
    # This is a simplified mock. In a real scenario, this would involve
    # sophisticated NLP models trained for Arabic UI element extraction.
    # For demonstration, we'll use keywords and simple pattern matching.

    ui_config = {"elements": [], "layout": {"orientation": "vertical"}}

    # Simple keyword-based parsing for demonstration
    keywords_to_element = {
        "زر": "Button",
        "حقل نص": "EditText",
        "عنوان": "TextView",
        "صورة": "ImageView",
        "قائمة": "ListView"
    }

    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        element_added = False
        for keyword, element_type in keywords_to_element.items():
            if keyword in line:
                parts = line.split(f" {keyword} ")
                if len(parts) > 1:
                    element_name = parts[0].strip()
                    element_properties_str = parts[1].strip()

                    # Further parsing of properties
                    properties = {}
                    if element_type == "TextView" or element_type == "Button":
                        properties["text"] = element_name # Using the name before keyword as text
                        if "بمعرف" in element_properties_str:
                            prop_parts = element_properties_str.split(" بمعرف ")
                            if len(prop_parts) > 1:
                                properties["id"] = prop_parts[1].strip()
                        if "في المنتصف" in element_properties_str:
                            properties["layout_gravity"] = "center"
                    elif element_type == "EditText":
                         if "بمعرف" in element_properties_str:
                            prop_parts = element_properties_str.split(" بمعرف ")
                            if len(prop_parts) > 1:
                                properties["id"] = prop_parts[1].strip()
                    # Add more specific property parsing as needed

                    ui_config["elements"].append({"type": element_type, **properties})
                    element_added = True
                    break # Move to next line once an element is identified

        if not element_added and "اتجاه عمودي" in line:
            ui_config["layout"]["orientation"] = "vertical"
        elif not element_added and "اتجاه أفقي" in line:
            ui_config["layout"]["orientation"] = "horizontal"

    return ui_config
    # --- REAL LOGIC END ---

def generate_android_manifest(package_name: str, ui_config: dict) -> str:
    """
    Generates a basic AndroidManifest.xml content based on UI configuration.

    Args:
        package_name: The package name for the Android application.
        ui_config: The parsed UI configuration from analyze_arabic_text_for_ui_elements.

    Returns:
        A string containing the XML content for AndroidManifest.xml.
    """
    # --- REAL LOGIC START ---
    manifest_template = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppName">  <!-- Placeholder theme -->

        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    # This function currently generates a static manifest.
    # In a more advanced scenario, it could dynamically add permissions,
    # services, or other components based on ui_config if that data were available.
    # For now, it serves as a structural placeholder.
    return manifest_template
    # --- REAL LOGIC END ---

def generate_layout_xml(ui_config: dict, layout_name: str = "activity_main") -> str:
    """
    Generates an Android XML layout file content from the UI configuration.

    Args:
        ui_config: The parsed UI configuration from analyze_arabic_text_for_ui_elements.
        layout_name: The name of the layout file (e.g., "activity_main").

    Returns:
        A string containing the XML content for the layout file.
    """
    # --- REAL LOGIC START ---
    layout_elements_xml = []
    layout_attrs = {
        "xmlns:android": "http://schemas.android.com/apk/res/android",
        "xmlns:app": "http://schemas.android.com/apk/res-auto", # For potential custom attributes
        "xmlns:tools": "http://schemas.android.com/tools",
        "android:layout_width": "match_parent",
        "android:layout_height": "match_parent",
        "android:padding": "16dp",
        "tools:context": ".MainActivity" # Placeholder context
    }

    if "layout" in ui_config and ui_config["layout"].get("orientation"):
        layout_attrs["android:orientation"] = ui_config["layout"]["orientation"]
        # If orientation is vertical or horizontal, it's likely a LinearLayout
        layout_tag = "LinearLayout"
    else:
        # Default to ConstraintLayout if no orientation is specified or it's a more complex layout
        layout_tag = "androidx.constraintlayout.widget.ConstraintLayout"
        # ConstraintLayout attributes might be different, but for simplicity, we keep common ones.

    # Add elements
    for element in ui_config.get("elements", []):
        element_type = element.get("type")
        element_attrs = {
            "android:layout_width": "wrap_content",
            "android:layout_height": "wrap_content",
        }

        if element_type == "TextView":
            if "text" in element:
                element_attrs["android:text"] = element["text"]
            if "id" in element:
                element_attrs["android:id"] = f"@{element['id']}"
            if "layout_gravity" in element:
                element_attrs["android:gravity"] = element["layout_gravity"] # Using gravity for simplicity

        elif element_type == "Button":
            if "text" in element:
                element_attrs["android:text"] = element["text"]
            if "id" in element:
                element_attrs["android:id"] = f"@{element['id']}"
            if "layout_gravity" in element:
                element_attrs["android:gravity"] = element["layout_gravity"]
            # Add on_click handler if provided in config (would need to map to Java/Kotlin code)
            # if "on_click" in element:
            #     element_attrs["android:onClick"] = element["on_click"]

        elif element_type == "EditText":
            if "id" in element:
                element_attrs["android:id"] = f"@{element['id']}"
            # Add hint, input type etc. if available in config
            # element_attrs["android:hint"] = "Enter text here"
            # element_attrs["android:inputType"] = "text"

        # Convert attributes to XML string
        attr_string = " ".join([f'{k}="{v}"' for k, v in element_attrs.items()])
        layout_elements_xml.append(f"<{element_type} {attr_string} />")

    # Assemble the full layout XML
    layout_header_attrs = " ".join([f'{k}="{v}"' for k, v in layout_attrs.items()])
    layout_content = "\n    ".join(layout_elements_xml)
    full_layout_xml = f"""<{layout_tag} {layout_header_attrs}>
    {layout_content}
</{layout_tag}>
"""
    return full_layout_xml
    # --- REAL LOGIC END ---

def generate_activity_java(activity_name: str = "MainActivity") -> str:
    """
    Generates a basic MainActivity.java content.

    Args:
        activity_name: The name of the activity class.

    Returns:
        A string containing the Java code for the activity.
    """
    # --- REAL LOGIC START ---
    java_code = f"""package com.example.generatedapp; // Placeholder package

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assumes layout file is activity_main.xml

        // Example: Adding an OnClickListener to a button if one was defined in XML
        // Button myButton = findViewById(R.id.submit_button); // Assuming a button with id 'submit_button'
        // if (myButton != null) {{
        //     myButton.setOnClickListener(new View.OnClickListener() {{
        //         @Override
        //         public void onClick(View v) {{
        //             // Handle button click
        //             Toast.makeText(getApplicationContext(), "Button clicked!", Toast.LENGTH_SHORT).show();
        //         }}
        //     }});
        // }}
    }}

    // Example of an onClick handler that could be referenced from XML
    // public void handleSubmit(View view) {{
    //     Toast.makeText(this, "Form Submitted!", Toast.LENGTH_SHORT).show();
    // }}
}}
"""
    return java_code
    # --- REAL LOGIC START ---


# Core Lobe 2_natural_language_processing_lobe Functions
def process_arabic_description(user_prompt: str, app_name: str = "MyGeneratedApp") -> dict:
    """
    This is the primary function for Lobe 2. It takes natural language input
    in Arabic, analyzes it, and orchestrates the generation of relevant code
    and configuration files for an Android APK.

    Args:
        user_prompt: The natural language description of the desired app in Arabic.
        app_name: The desired name for the generated application.

    Returns:
        A dictionary containing the generated code artifacts and configuration.
        Example:
        {
            "package_name": "com.example.mygeneratedapp",
            "manifest_xml": "<?xml version=\"1.0\" encoding=\"utf-8\"?>...",
            "layout_xml": "<LinearLayout xmlns:android=\"...\"...",
            "activity_java": "package com.example.generatedapp;\nimport ...",
            "ui_config": {"elements": [...], "layout": {...}}
        }
    """
    # --- REAL LOGIC START ---
    package_name = f"com.example.{app_name.lower().replace(' ', '')}"

    # 1. Analyze Arabic text for UI elements and app structure
    # This calls the core NLP function for parsing Arabic into structured data.
    ui_config = analyze_arabic_text_for_ui_elements(user_prompt)

    # 2. Generate Android Manifest
    # Uses the package name and potentially app-wide configurations from ui_config
    # to create the manifest.
    manifest_xml = generate_android_manifest(package_name, ui_config)

    # 3. Generate Layout XML
    # Translates the parsed UI elements from ui_config into an Android XML layout file.
    # We'll assume a primary layout named 'activity_main' for simplicity.
    layout_xml = generate_layout_xml(ui_config, layout_name="activity_main")

    # 4. Generate Activity Java Code
    # Creates a basic Java activity file that inflates the generated layout.
    # This could be extended to generate Kotlin.
    activity_java = generate_activity_java(activity_name="MainActivity")

    generated_artifacts = {
        "package_name": package_name,
        "manifest_xml": manifest_xml,
        "layout_xml": layout_xml,
        "activity_java": activity_java,
        "ui_config": ui_config # Also return the parsed config for further use
    }

    return generated_artifacts
    # --- REAL LOGIC END ---

# Example Usage (for testing within this lobe)
if __name__ == "__main__":
    print("--- Lobe 2: Natural Language Processing Lobe Demo ---")

    # Example Arabic prompt describing a simple app
    arabic_prompt_1 = """
    إنشاء تطبيق بسيط.
    شاشة رئيسية بها عنوان 'مرحباً بالعالم' في المنتصف.
    وزر 'اضغط هنا' بمعرف submit_button.
    يجب أن تكون العناصر مرتبة في اتجاه عمودي.
    """
    app_name_1 = "HelloArabicApp"

    print(f"\nProcessing prompt 1: '{arabic_prompt_1}'")
    generated_data_1 = process_arabic_description(arabic_prompt_1, app_name=app_name_1)

    print("\n--- Generated Artifacts (Prompt 1) ---")
    print(f"Package Name: {generated_data_1['package_name']}")
    print("\nManifest XML:")
    print(generated_data_1['manifest_xml'][:200] + "...") # Print first 200 chars
    print("\nLayout XML:")
    print(generated_data_1['layout_xml'][:200] + "...")
    print("\nActivity Java:")
    print(generated_data_1['activity_java'][:200] + "...")
    print("\nUI Config:")
    print(json.dumps(generated_data_1['ui_config'], indent=2, ensure_ascii=False))


    # Another example with different elements
    arabic_prompt_2 = """
    إنشاء واجهة مستخدم مع زر 'إرسال' بمعرف send_btn.
    حقل نص 'أدخل اسمك' بمعرف name_input.
    وعنوان 'شكراً لك' بمعرف thank_you_text.
    """
    app_name_2 = "UserFormApp"

    print(f"\n---")
    print(f"\nProcessing prompt 2: '{arabic_prompt_2}'")
    generated_data_2 = process_arabic_description(arabic_prompt_2, app_name=app_name_2)

    print("\n--- Generated Artifacts (Prompt 2) ---")
    print(f"Package Name: {generated_data_2['package_name']}")
    print("\nLayout XML:")
    print(generated_data_2['layout_xml'][:200] + "...")
    print("\nUI Config:")
    print(json.dumps(generated_data_2['ui_config'], indent=2, ensure_ascii=False))

    print("\n--- Lobe 2 Demo Finished ---")