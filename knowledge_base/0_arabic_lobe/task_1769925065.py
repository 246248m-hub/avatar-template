import os
import shutil

# --- Lobe 0: Arabic Parser Lobe ---
def parse_arabic_to_android_xml(arabic_text):
    """
    Parses a simplified Arabic description into Android XML layout attributes.
    This is a highly simplified example. A real implementation would involve
    more sophisticated NLP and potentially a grammar.

    Args:
        arabic_text (str): A string containing Arabic descriptions of UI elements
                           and their properties.

    Returns:
        str: A string representing Android XML layout attributes.
    """
    xml_attributes = ""
    lines = arabic_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "نص" in line and "في المنتصف" in line:
            parts = line.split("نص")
            if len(parts) > 1:
                text_content = parts[1].strip().split("في المنتصف")[0].strip()
                xml_attributes += f'        android:text="{text_content}"\n'
                xml_attributes += '        app:layout_constraintStart_toStartOf="parent"\n'
                xml_attributes += '        app:layout_constraintEnd_toEndOf="parent"\n'
                xml_attributes += '        app:layout_constraintTop_toTopOf="parent"\n'

        elif "زر" in line and "أسفل" in line:
            parts = line.split("زر")
            if len(parts) > 1:
                button_text = parts[1].strip().split("أسفل")[0].strip()
                xml_attributes += f'        android:text="{button_text}"\n'
                xml_attributes += '        app:layout_constraintStart_toStartOf="parent"\n'
                xml_attributes += '        app:layout_constraintEnd_toEndOf="parent"\n'
                # Assuming it's anchored to the bottom of a parent or another element
                xml_attributes += '        app:layout_constraintBottom_toBottomOf="parent"\n' # Simplified

        elif "صورة" in line and "فوق" in line:
            parts = line.split("صورة")
            if len(parts) > 1:
                image_src = parts[1].strip().split("فوق")[0].strip()
                # In a real scenario, you'd map 'image_src' to a drawable resource
                xml_attributes += f'        android:src="@drawable/{image_src.replace(" ", "_").lower()}"\n'
                xml_attributes += '        app:layout_constraintStart_toStartOf="parent"\n'
                xml_attributes += '        app:layout_constraintEnd_toEndOf="parent"\n'
                # Assuming it's anchored to the top of a parent or another element
                xml_attributes += '        app:layout_constraintTop_toTopOf="parent"\n' # Simplified

    return xml_attributes

# --- Lobe 1: Arabic Generator Lobe ---
def generate_arabic_layout_description(xml_attributes):
    """
    Generates a simplified Arabic description from Android XML layout attributes.
    This is a reverse of the parser, also highly simplified.

    Args:
        xml_attributes (str): A string containing Android XML layout attributes.

    Returns:
        str: A simplified Arabic description.
    """
    arabic_description = ""
    lines = xml_attributes.strip().split('\n')
    element_type = "عنصر"
    element_properties = {}

    for line in lines:
        line = line.strip()
        if line.startswith("android:text="):
            text = line.split('"')[1]
            if element_type == "عنصر": # Inferring type from context if needed
                element_type = "نص"
            element_properties['text'] = text
        elif line.startswith("android:src="):
            src = line.split('"')[1].split('@drawable/')[1].replace('_', ' ')
            if element_type == "عنصر":
                element_type = "صورة"
            element_properties['src'] = src
        elif line.startswith("app:layout_constraintBottom_toBottomOf="):
            element_properties['position'] = "أسفل"
        elif line.startswith("app:layout_constraintTop_toTopOf="):
            element_properties['position'] = "فوق"
        elif line.startswith("app:layout_constraintStart_toStartOf=") or line.startswith("app:layout_constraintEnd_toEndOf="):
            if "parent" in line:
                if 'alignment' not in element_properties:
                    element_properties['alignment'] = []
                if "start" in line and "parent" in line:
                    element_properties['alignment'].append("على اليسار")
                if "end" in line and "parent" in line:
                    element_properties['alignment'].append("على اليمين")

    if element_type == "نص":
        description = f"نص {element_properties.get('text', '')}"
        if 'position' in element_properties:
            description += f" {element_properties['position']}"
        if 'alignment' in element_properties:
            description += f" {' و '.join(element_properties['alignment'])}"
        arabic_description += description + "\n"
    elif element_type == "صورة":
        description = f"صورة {element_properties.get('src', '')}"
        if 'position' in element_properties:
            description += f" {element_properties['position']}"
        if 'alignment' in element_properties:
            description += f" {' و '.join(element_properties['alignment'])}"
        arabic_description += description + "\n"
    elif "button" in xml_attributes.lower(): # Crude inference for button
        element_type = "زر"
        button_text = ""
        for attr in element_properties.keys():
            if attr == 'text':
                button_text = element_properties[attr]
                break
        description = f"زر {button_text}"
        if 'position' in element_properties:
            description += f" {element_properties['position']}"
        if 'alignment' in element_properties:
            description += f" {' و '.join(element_properties['alignment'])}"
        arabic_description += description + "\n"


    return arabic_description.strip()

# --- Lobe 2: UI Element Mapping Lobe ---
def map_arabic_to_xml_tag(arabic_description_part):
    """
    Maps simplified Arabic descriptions of UI elements to their corresponding
    XML tags.

    Args:
        arabic_description_part (str): A part of the Arabic description.

    Returns:
        str: The corresponding XML tag name (e.g., "TextView", "Button", "ImageView").
    """
    if "نص" in arabic_description_part:
        return "TextView"
    elif "زر" in arabic_description_part:
        return "Button"
    elif "صورة" in arabic_description_part:
        return "ImageView"
    else:
        return "View" # Default or placeholder

# --- Lobe 3: Constraint Layout Generator Lobe ---
def generate_constraint_layout_xml(ui_elements_data):
    """
    Generates a ConstraintLayout XML string from a list of UI element descriptions.

    Args:
        ui_elements_data (list): A list of dictionaries, where each dictionary
                                 describes a UI element (tag, attributes).

    Returns:
        str: The complete ConstraintLayout XML string.
    """
    xml_content = '<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity">\n'

    for element in ui_elements_data:
        tag = element["tag"]
        attributes = element["attributes"]
        xml_content += f'    <{tag}\n'
        xml_content += '        android:id="@+id/' + f"{tag.lower()}_0" + '"\n' # Simple ID generation
        for attr, value in attributes.items():
            xml_content += f'        {attr}="{value}"\n'
        xml_content += f'    />\n'

    xml_content += '</androidx.constraintlayout.widget.ConstraintLayout>'
    return xml_content

# --- Lobe 4: Code Generation Lobe (Placeholder for now) ---
# This lobe would generate Java/Kotlin code to interact with the UI elements.
# For this example, we'll focus on the XML generation.
def generate_android_code(layout_xml_content):
    """
    Placeholder for generating Android activity/fragment code.
    This function would parse the layout_xml_content and generate Java/Kotlin
    code to reference and manipulate UI elements.
    """
    print("\n--- Lobe 4: Code Generation Lobe ---")
    print("Placeholder: Generating Android code from XML is not implemented in this demo.")
    print("In a real scenario, this would involve parsing the XML and creating Java/Kotlin.")
    return "// Placeholder for generated Android code"

# --- Lobe 5: APK Builder Lobe (Placeholder for now) ---
# This lobe would orchestrate the build process to create an APK.
def build_apk(generated_code, layout_xml_content):
    """
    Placeholder for the APK building process.
    This function would typically:
    1. Create a temporary Android project structure.
    2. Place the generated XML and code into the appropriate directories.
    3. Execute Android build tools (like Gradle) to compile and package the APK.
    """
    print("\n--- Lobe 5: APK Builder Lobe ---")
    print("Placeholder: Actual APK building is a complex process involving Android SDK and build tools.")
    print("This function would orchestrate Gradle builds.")

    # --- Dummy APK building simulation ---
    dummy_project_dir = "dummy_android_project"
    dummy_app_dir = os.path.join(dummy_project_dir, "app")
    dummy_res_dir = os.path.join(dummy_app_dir, "src", "main", "res")
    dummy_layout_dir = os.path.join(dummy_res_dir, "layout")
    dummy_values_dir = os.path.join(dummy_res_dir, "values")
    dummy_java_dir = os.path.join(dummy_app_dir, "src", "main", "java", "com", "example", "myapp")

    os.makedirs(dummy_layout_dir, exist_ok=True)
    os.makedirs(dummy_values_dir, exist_ok=True)
    os.makedirs(dummy_java_dir, exist_ok=True)

    # Create dummy layout file
    with open(os.path.join(dummy_layout_dir, "activity_main.xml"), "w", encoding="utf-8") as f:
        f.write(layout_xml_content)
        print(f"Created dummy layout file: {os.path.join(dummy_layout_dir, 'activity_main.xml')}")

    # Create dummy strings.xml
    with open(os.path.join(dummy_values_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write('<resources>\n    <string name="app_name">My Arabic App</string>\n</resources>')
        print(f"Created dummy strings.xml: {os.path.join(dummy_values_dir, 'strings.xml')}")

    # Create dummy MainActivity.java (very basic)
    with open(os.path.join(dummy_java_dir, "MainActivity.java"), "w", encoding="utf-8") as f:
        f.write("""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
""")
        print(f"Created dummy MainActivity.java: {os.path.join(dummy_java_dir, 'MainActivity.java')}")

    # Simulate APK creation
    output_apk_path = os.path.join(dummy_project_dir, "app-release.apk")
    print(f"\n--- Simulating APK build ---")
    print(f"Dummy APK would be generated at: {output_apk_path}")
    print("This process normally involves Gradle wrapper execution.")
    print(f"Created dummy 'android_template' directory structure at: {dummy_project_dir}")

    return output_apk_path

# --- Helper function for cleanup ---
def cleanup_dummy_files():
    """Removes dummy directories created for demonstration."""
    dummy_project_dir = "dummy_android_project"
    if os.path.exists(dummy_project_dir):
        shutil.rmtree(dummy_project_dir)
        print(f"Cleaned up dummy project directory: {dummy_project_dir}")

# --- Main execution flow ---
if __name__ == "__main__":
    print("--- Arabic Layout Parser and Generator Module Demo ---")

    # Example Arabic input describing a simple layout
    arabic_input_1 = """
    نص أهلاً وسهلاً في المنتصف
    زر اضغط هنا أسفل
    """

    arabic_input_2 = """
    صورة لوگو فوق
    نص عنوان التطبيق في المنتصف
    """

    # --- Step 1: Parse Arabic to XML Attributes (Lobe 0) ---
    print("\n--- Step 1: Parsing Arabic to XML Attributes (Lobe 0) ---")
    xml_attributes_1 = parse_arabic_to_android_xml(arabic_input_1)
    print(f"Parsed Arabic:\n{arabic_input_1}\nGenerated XML Attributes:\n{xml_attributes_1}")

    xml_attributes_2 = parse_arabic_to_android_xml(arabic_input_2)
    print(f"\nParsed Arabic:\n{arabic_input_2}\nGenerated XML Attributes:\n{xml_attributes_2}")

    # --- Step 2: Map to XML Tags and Structure Layout (Lobe 2 & 3) ---
    print("\n--- Step 2: Mapping to XML Tags and Structuring Layout (Lobe 2 & 3) ---")
    ui_elements_1 = []
    # Crude splitting for demonstration; a real parser would be smarter
    for line in arabic_input_1.strip().split('\n'):
        if line.strip():
            tag = map_arabic_to_xml_tag(line)
            # Re-parse attributes for this specific line
            # In a more complex system, this would be a more direct mapping
            attributes_str = parse_arabic_to_android_xml(line)
            attributes_dict = {}
            for attr_line in attributes_str.strip().split('\n'):
                if '=' in attr_line:
                    key, value = attr_line.split('=', 1)
                    attributes_dict[key.strip()] = value.strip().strip('"')
            ui_elements_1.append({"tag": tag, "attributes": attributes_dict})

    constraint_layout_xml_1 = generate_constraint_layout_xml(ui_elements_1)
    print(f"Generated ConstraintLayout XML for input 1:\n{constraint_layout_xml_1}")

    ui_elements_2 = []
    for line in arabic_input_2.strip().split('\n'):
        if line.strip():
            tag = map_arabic_to_xml_tag(line)
            attributes_str = parse_arabic_to_android_xml(line)
            attributes_dict = {}
            for attr_line in attributes_str.strip().split('\n'):
                if '=' in attr_line:
                    key, value = attr_line.split('=', 1)
                    attributes_dict[key.strip()] = value.strip().strip('"')
            ui_elements_2.append({"tag": tag, "attributes": attributes_dict})

    constraint_layout_xml_2 = generate_constraint_layout_xml(ui_elements_2)
    print(f"\nGenerated ConstraintLayout XML for input 2:\n{constraint_layout_xml_2}")

    # --- Step 3: Generate Android Code (Lobe 4 - Placeholder) ---
    generated_code_placeholder = generate_android_code(constraint_layout_xml_1)

    # --- Step 4: Build APK (Lobe 5 - Placeholder Simulation) ---
    output_apk_path = build_apk(generated_code_placeholder, constraint_layout_xml_1)

    # --- Step 5: Demonstrate Reverse (Generator Lobe 1) ---
    print("\n--- Step 5: Demonstrating Arabic Generator (Lobe 1) from XML ---")
    # Using the generated XML from the first example
    generated_arabic_1 = generate_arabic_layout_description(constraint_layout_xml_1)
    print(f"Generated Arabic from XML 1:\n{generated_arabic_1}")

    generated_arabic_2 = generate_arabic_layout_description(constraint_layout_xml_2)
    print(f"\nGenerated Arabic from XML 2:\n{generated_arabic_2}")

    # Clean up dummy files
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()

    print("\n--- Arabic Layout Parser and Generator Module Demo Finished ---")