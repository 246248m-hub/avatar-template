import os
import re
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Assume these are defined in other lobes or globally
# For demonstration, we'll define them here
KNOWLEDGE_BASE_DIR = "./knowledge_base"
PROJECT_ROOT = "./generated_apk"
APP_NAME = "MyArabicApp"
PACKAGE_NAME = "com.example.myarabicapp"

def create_directory_if_not_exists(path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def generate_kotlin_activity(activity_name, layout_name, content_elements=None):
    """Generates a basic Kotlin Activity file content."""
    if content_elements is None:
        content_elements = []

    content_str = "\n".join(content_elements)

    kotlin_template = f"""
package {PACKAGE_NAME}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

class {activity_name} : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.{layout_name})
        // Add dynamic content or logic here based on requirements
        // Example: findViewById<TextView>(R.id.my_text_view).text = "Hello from Arabic!"
    }}
}}
"""
    return kotlin_template

def generate_xml_layout(layout_name, elements):
    """Generates a basic XML layout file content."""
    root = ET.Element("LinearLayout", {"xmlns:android": "http://schemas.android.com/apk/res/android",
                                       "xmlns:app": "http://schemas.android.com/apk/res-auto",
                                       "xmlns:tools": "http://schemas.android.com/tools",
                                       "android:layout_width": "match_parent",
                                       "android:layout_height": "match_parent",
                                       "android:orientation": "vertical",
                                       "tools:context": f".{APP_NAME}"})

    for element_xml in elements:
        try:
            # This is a simple way to append XML strings. A more robust solution would parse and append ET.Elements.
            # For now, assuming elements are valid XML snippets.
            # A better approach: Parse each snippet into an ET.Element and append it to the root.
            pass # Placeholder for actual element parsing and appending
        except Exception as e:
            print(f"Warning: Could not parse element '{element_xml}': {e}")

    # For now, we'll just create a minimal layout if no elements are provided,
    # or try to create a root element if the elements list is not empty.
    if not elements:
        root = ET.Element("LinearLayout", {"xmlns:android": "http://schemas.android.com/apk/res/android",
                                           "android:layout_width": "match_parent",
                                           "android:layout_height": "match_parent",
                                           "android:orientation": "vertical",
                                           "android:gravity": "center"})
        tv = ET.SubElement(root, "TextView")
        tv.set("android:layout_width", "wrap_content")
        tv.set("android:layout_height", "wrap_content")
        tv.set("android:text", "Welcome!")
        tv.set("android:textSize", "24sp")
    else:
        # In a real scenario, parse and append each element from the 'elements' list
        # Example:
        # for element_xml_str in elements:
        #     try:
        #         sub_root = ET.fromstring(element_xml_str)
        #         root.append(sub_root)
        #     except ET.ParseError as e:
        #         print(f"Error parsing XML element: {element_xml_str} - {e}")
        pass # Placeholder for actual element appending

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

class ArabicNLPModule:
    """
    Module for handling Arabic Natural Language Processing tasks related to APK generation.
    Focuses on parsing Arabic text, identifying UI components, and generating structured data
    for code generation.
    """
    def __init__(self):
        self.knowledge_base_dir = KNOWLEDGE_BASE_DIR
        self.arabic_keywords = self._load_arabic_keywords()
        self.ui_component_map = {
            "زر": "Button",
            "نص": "TextView",
            "صورة": "ImageView",
            "حقل إدخال": "EditText",
            "قائمة": "ListView",
            "جدول": "RecyclerView",
            "شاشة": "Activity",
            "عنوان": "Toolbar"
        }
        self.attribute_map = {
            "عرض": "android:layout_width",
            "ارتفاع": "android:layout_height",
            "نص": "android:text",
            "لون": "android:textColor",
            "حجم الخط": "android:textSize",
            "معرف": "android:id",
            "توسيط": "android:gravity",
            "اتجاه": "android:orientation",
            "تسمية": "android:hint"
        }

    def _load_arabic_keywords(self):
        """Loads keywords and their corresponding NLP tags from the knowledge base."""
        keywords = {}
        keywords_file = os.path.join(self.knowledge_base_dir, "arabic_keywords.json")
        if os.path.exists(keywords_file):
            with open(keywords_file, 'r', encoding='utf-8') as f:
                keywords = json.load(f)
        else:
            print(f"Warning: Arabic keywords file not found at {keywords_file}. Using default keywords.")
            # Default keywords if file is missing
            keywords = {
                "ui_elements": {
                    "زر": "Button", "نص": "TextView", "صورة": "ImageView", "حقل إدخال": "EditText",
                    "قائمة": "ListView", "جدول": "RecyclerView", "شاشة": "Activity", "عنوان": "Toolbar"
                },
                "attributes": {
                    "عرض": "android:layout_width", "ارتفاع": "android:layout_height", "نص": "android:text",
                    "لون": "android:textColor", "حجم الخط": "android:textSize", "معرف": "android:id",
                    "توسيط": "android:gravity", "اتجاه": "android:orientation", "تسمية": "android:hint"
                },
                "values": {
                    "كامل": "match_parent", "تلقائي": "wrap_content", "عمودي": "vertical",
                    "أفقي": "horizontal", "منتصف": "center", "أبيض": "#FFFFFF", "أسود": "#000000"
                },
                "actions": {
                    "انقر": "OnClickListener", "عرض": "visibility"
                }
            }
        return keywords

    def parse_arabic_description(self, arabic_description: str):
        """
        Parses an Arabic description to identify UI elements, their attributes, and values.

        Args:
            arabic_description: A string containing the Arabic description of the UI.

        Returns:
            A structured dictionary representing the parsed UI elements and their properties.
        """
        parsed_ui = {"layouts": [], "activities": []}
        current_layout = None
        current_activity = None

        # Split description into potential sentences or phrases
        phrases = re.split(r'[.،!؟;]', arabic_description)
        phrases = [p.strip() for p in phrases if p.strip()]

        for phrase in phrases:
            words = phrase.split()
            element_type = None
            element_name = None
            attributes = {}
            is_layout_definition = False
            is_activity_definition = False

            # Check for UI element keywords
            for keyword, component_type in self.ui_component_map.items():
                if keyword in phrase:
                    element_type = component_type
                    # Try to extract a name or label for the element
                    # This is a heuristic and might need more sophisticated NLP
                    words_after_keyword = phrase.split(keyword, 1)[-1].strip()
                    if words_after_keyword:
                        # Simple approach: take the first few words as potential name
                        element_name = " ".join(words_after_keyword.split()[:3]) # Heuristic name extraction
                        # Clean up potential trailing punctuation if not handled by sentence splitting
                        element_name = re.sub(r'[.،!؟;]$', '', element_name).strip()
                    else:
                        element_name = f"{keyword}_default_name" # Fallback name

                    if element_type == "Activity":
                        is_activity_definition = True
                        current_activity = {"name": element_name, "layout": None, "elements": []}
                        parsed_ui["activities"].append(current_activity)
                        break # Assume one activity per phrase for now

                    elif element_type == "LinearLayout" or element_type == "ConstraintLayout": # Example layout types
                        is_layout_definition = True
                        current_layout = {"name": element_name, "elements": []}
                        parsed_ui["layouts"].append(current_layout)
                        break # Assume one layout definition per phrase for now

                    else: # Regular UI element
                        if current_activity and not is_activity_definition:
                            current_activity["elements"].append({"type": element_type, "name": element_name, "attributes": {}})
                            element_data = current_activity["elements"][-1]
                        elif current_layout and not is_layout_definition:
                            current_layout["elements"].append({"type": element_type, "name": element_name, "attributes": {}})
                            element_data = current_layout["elements"][-1]
                        else:
                            # If no current layout/activity context, create a generic element or skip
                            # For now, let's associate it with the last defined activity/layout if possible
                            if parsed_ui["activities"]:
                                last_activity = parsed_ui["activities"][-1]
                                last_activity["elements"].append({"type": element_type, "name": element_name, "attributes": {}})
                                element_data = last_activity["elements"][-1]
                            elif parsed_ui["layouts"]:
                                last_layout = parsed_ui["layouts"][-1]
                                last_layout["elements"].append({"type": element_type, "name": element_name, "attributes": {}})
                                element_data = last_layout["elements"][-1]
                            else:
                                print(f"Warning: UI element '{element_name}' ({element_type}) found without an active layout or activity context.")
                                continue

                        # Process attributes within the same phrase
                        for attr_keyword, attr_name in self.attribute_map.items():
                            if attr_keyword in phrase:
                                # Try to extract the value associated with the attribute
                                # This is a simplified approach. More complex regex might be needed.
                                # Example: "زر بعرض تلقائي" -> attr_keyword="عرض", attr_name="android:layout_width", value="wrap_content"
                                try:
                                    value_part = phrase.split(attr_keyword, 1)[1]
                                    # Look for values after the attribute keyword
                                    for val_keyword, val_name in self.keywords.get("values", {}).items():
                                        if val_keyword in value_part:
                                            attributes[attr_name] = val_name
                                            break
                                    else: # If no specific value keyword found, try to get a descriptive word
                                        potential_value = value_part.split()[0] if value_part.split() else None
                                        if potential_value and not any(kw in potential_value for kw in self.ui_component_map.keys()) and not any(kw in potential_value for kw in self.attribute_map.keys()):
                                            # Avoid picking other keywords as values
                                            attributes[attr_name] = potential_value.strip('.,;:')
                                except IndexError:
                                    pass # Attribute keyword might be at the end of the phrase

                        if element_data:
                            element_data["attributes"].update(attributes)
                        break # Found an element type, move to next phrase

            # If the phrase defined an activity or layout, it's handled above.
            # If it was a regular UI element, it's also handled.
            # Additional logic might be needed for relationships between elements,
            # or for attributes that span multiple phrases.

        # Post-processing: Assign default layouts to activities if not specified
        for activity in parsed_ui["activities"]:
            if activity["layout"] is None and activity["elements"]:
                # Create a default layout for the activity if it has elements but no explicit layout
                activity_layout_name = f"{activity['name'].lower()}_layout"
                activity["layout"] = activity_layout_name
                # Move activity's direct elements into this new layout
                layout_elements = activity["elements"]
                activity["elements"] = [] # Clear direct elements, now they belong to the layout
                parsed_ui["layouts"].append({"name": activity_layout_name, "elements": layout_elements})
            elif activity["layout"] is None and not activity["elements"]:
                # Create a minimal default layout for activities with no specified elements
                activity_layout_name = f"{activity['name'].lower()}_layout"
                activity["layout"] = activity_layout_name
                parsed_ui["layouts"].append({"name": activity_layout_name, "elements": []})


        return parsed_ui

    def generate_apk_structure_data(self, parsed_ui_data):
        """
        Translates the parsed UI data into a structured format suitable for code generation.
        This function is a placeholder for more complex logic.
        """
        apk_structure = {
            "activities": [],
            "layouts": [],
            "other_files": [] # e.g., manifest, strings.xml
        }

        for layout_data in parsed_ui_data.get("layouts", []):
            layout_xml_elements = []
            for element in layout_data.get("elements", []):
                attrs_str = " ".join([f"{k}='{v}'" for k, v in element["attributes"].items()])
                layout_xml_elements.append(f"<{element['type']} {attrs_str} />")

            apk_structure["layouts"].append({
                "name": layout_data["name"],
                "xml_content": "\n".join(layout_xml_elements)
            })

        for activity_data in parsed_ui_data.get("activities", []):
            activity_name = activity_data["name"]
            layout_name = activity_data.get("layout")
            activity_elements_for_kotlin = []

            if layout_name:
                # Find the corresponding layout
                layout_info = next((l for l in apk_structure["layouts"] if l["name"] == layout_name), None)
                if layout_info:
                    # Extract element definitions for Kotlin code (e.g., IDs for findViewById)
                    for element in layout_data.get("elements", []):
                        element_id = element["attributes"].get("android:id")
                        if element_id:
                            activity_elements_for_kotlin.append(f"// View with ID: {element_id}")
                        else:
                            activity_elements_for_kotlin.append(f"// Element: {element['type']}")
            else:
                # If no layout is explicitly linked but activity has elements,
                # we would have created a default layout in parsing step.
                # This case might indicate an inconsistency or a need for more robust linking.
                pass # Error handling or default behavior might be needed here


            apk_structure["activities"].append({
                "name": activity_name,
                "layout_name": layout_name,
                "kotlin_content": generate_kotlin_activity(
                    activity_name,
                    layout_name if layout_name else f"{activity_name.lower()}_layout",
                    activity_elements_for_kotlin
                )
            })

        # Add basic AndroidManifest.xml structure (simplified)
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{PACKAGE_NAME}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{APP_NAME}">

        <activity android:name=".{APP_NAME}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <!-- Add other activities here -->
"""
        for activity_data in apk_structure["activities"]:
            if activity_data["name"] != APP_NAME: # Avoid duplicating the main launcher activity
                manifest_content += f'        <activity android:name=".{activity_data["name"]}" />\n'

        manifest_content += """    </application>
</manifest>
"""
        apk_structure["other_files"].append({
            "name": "AndroidManifest.xml",
            "content": manifest_content
        })

        # Add a basic strings.xml
        strings_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{APP_NAME}</string>
    <!-- Add other strings here -->
</resources>
""".format(APP_NAME=APP_NAME)
        apk_structure["other_files"].append({
            "name": "strings.xml",
            "content": strings_content
        })


        return apk_structure

class ArabicAPKBuilder:
    """
    Orchestrates the process of building APK structures from Arabic descriptions.
    Integrates with ArabicNLPModule and prepares data for code generation.
    """
    def __init__(self):
        self.arabic_nlp_module = ArabicNLPModule()
        self.project_root = PROJECT_ROOT
        self.app_name = APP_NAME
        self.package_name = PACKAGE_NAME

    def build_from_description(self, arabic_description: str):
        """
        Takes an Arabic description, parses it, and generates the necessary
        data structure for building an APK.

        Args:
            arabic_description: The natural language description of the desired APK.

        Returns:
            A dictionary containing the structured data for the APK components.
        """
        print("--- Parsing Arabic Description ---")
        parsed_ui_data = self.arabic_nlp_module.parse_arabic_description(arabic_description)
        print(f"Parsed UI Data: {json.dumps(parsed_ui_data, indent=2)}")

        print("\n--- Generating APK Structure Data ---")
        apk_structure_data = self.arabic_nlp_module.generate_apk_structure_data(parsed_ui_data)
        print("APK Structure Data Generated.")

        return apk_structure_data

    def create_project_files(self, apk_structure_data):
        """
        Creates the directory structure and writes the generated files to disk.
        This is the actual file generation step, bridging to the next lobes.
        """
        print(f"\n--- Creating Project Files at: {self.project_root} ---")
        create_directory_if_not_exists(self.project_root)
        create_directory_if_not_exists(os.path.join(self.project_root, "app", "src", "main", "java", *self.package_name.split('.')))
        create_directory_if_not_exists(os.path.join(self.project_root, "app", "src", "main", "res", "layout"))
        create_directory_if_not_exists(os.path.join(self.project_root, "app", "src", "main", "res", "values"))
        create_directory_if_not_exists(os.path.join(self.project_root, "app", "src", "main"))

        # Write AndroidManifest.xml
        manifest_info = next((f for f in apk_structure_data.get("other_files", []) if f["name"] == "AndroidManifest.xml"), None)
        if manifest_info:
            manifest_path = os.path.join(self.project_root, "app", "src", "main", manifest_info["name"])
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest_info["content"])
            print(f"Created: {manifest_path}")

        # Write strings.xml
        strings_info = next((f for f in apk_structure_data.get("other_files", []) if f["name"] == "strings.xml"), None)
        if strings_info:
            strings_path = os.path.join(self.project_root, "app", "src", "main", "res", "values", strings_info["name"])
            with open(strings_path, "w", encoding="utf-8") as f:
                f.write(strings_info["content"])
            print(f"Created: {strings_path}")

        # Write Layout XML files
        for layout_data in apk_structure_data.get("layouts", []):
            layout_filename = f"{layout_data['name']}.xml"
            layout_path = os.path.join(self.project_root, "app", "src", "main", "res", "layout", layout_filename)
            # Generate XML content
            root_element = ET.Element("LinearLayout", {"xmlns:android": "http://schemas.android.com/apk/res/android",
                                                        "xmlns:app": "http://schemas.android.com/apk/res-auto",
                                                        "xmlns:tools": "http://schemas.android.com/tools",
                                                        "android:layout_width": "match_parent",
                                                        "android:layout_height": "match_parent",
                                                        "android:orientation": "vertical",
                                                        "tools:context": f".{self.app_name}"}) # Placeholder context

            for element_data in layout_data.get("elements", []):
                element_attrs = element_data.get("attributes", {})
                # Basic attribute mapping and value resolution
                processed_attrs = {}
                for key, value in element_attrs.items():
                    if key.startswith("android:id"):
                        # Ensure IDs are valid resource names
                        processed_attrs[key] = "@+id/" + value.replace(" ", "_").lower()
                    elif key.startswith("android:textSize"):
                        # Ensure text size has units
                        if not value.endswith(("sp", "dp", "px")):
                            processed_attrs[key] = f"{value}sp"
                        else:
                            processed_attrs[key] = value
                    elif key.startswith("android:layout_width") or key.startswith("android:layout_height"):
                        # Map common values
                        if value == "match_parent":
                            processed_attrs[key] = "match_parent"
                        elif value == "wrap_content":
                            processed_attrs[key] = "wrap_content"
                        else:
                            processed_attrs[key] = value # Assume it's a dimension or specific value
                    else:
                        processed_attrs[key] = value

                ET.SubElement(root_element, element_data["type"], processed_attrs)

            # If no elements were added, create a default TextView
            if len(root_element) == 0:
                ET.SubElement(root_element, "TextView", {"android:layout_width": "wrap_content",
                                                         "android:layout_height": "wrap_content",
                                                         "android:text": "Default Layout",
                                                         "android:gravity": "center"})

            rough_string = ET.tostring(root_element, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            pretty_xml_content = reparsed.toprettyxml(indent="  ")

            with open(layout_path, "w", encoding="utf-8") as f:
                f.write(pretty_xml_content)
            print(f"Created: {layout_path}")


        # Write Kotlin Activity files
        for activity_data in apk_structure_data.get("activities", []):
            activity_filename = f"{activity_data['name']}.kt"
            activity_path = os.path.join(self.project_root, "app", "src", "main", "java", *self.package_name.split('.'), activity_filename)

            # Construct Kotlin content
            layout_name_for_kotlin = activity_data.get('layout_name')
            if not layout_name_for_kotlin:
                layout_name_for_kotlin = f"{activity_data['name'].lower()}_layout" # Fallback

            # Generate content for the Kotlin activity.
            # This part needs to dynamically build the activity code based on parsed data.
            # For now, we use the generic generator.
            kotlin_code_content = generate_kotlin_activity(
                activity_data["name"],
                layout_name_for_kotlin
                # The third argument for content_elements needs to be derived from parsed_ui_data
                # based on what's inside the associated layout, e.g., views that need manipulation.
            )

            with open(activity_path, "w", encoding="utf-8") as f:
                f.write(kotlin_code_content)
            print(f"Created: {activity_path}")

        print("\n--- APK Project Structure Created ---")
        return True # Indicate success

# --- Demo Usage ---
if __name__ == "__main__":
    # Ensure knowledge base directory exists for demonstration
    create_directory_if_not_exists(KNOWLEDGE_BASE_DIR)
    # Create a dummy keywords file for testing the loader
    dummy_keywords = {
        "ui_elements": {
            "زر": "Button", "نص": "TextView", "صورة": "ImageView", "حقل إدخال": "EditText",
            "شاشة": "Activity", "عنوان": "Toolbar", "تصميم": "Layout"
        },
        "attributes": {
            "عرض": "android:layout_width", "ارتفاع": "android:layout_height", "نص": "android:text",
            "لون": "android:textColor", "حجم الخط": "android:textSize", "معرف": "android:id",
            "توسيط": "android:gravity", "اتجاه": "android:orientation", "تلميح": "android:hint"
        },
        "values": {
            "كامل": "match_parent", "تلقائي": "wrap_content", "عمودي": "vertical",
            "أفقي": "horizontal", "منتصف": "center", "أبيض": "#FFFFFF", "أسود": "#000000",
            "كبير": "24sp", "صغير": "14sp"
        },
        "actions": {
            "عند النقر": "OnClickListener", "إظهار": "visibility"
        }
    }
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "arabic_keywords.json"), "w", encoding="utf-8") as f:
        json.dump(dummy_keywords, f, ensure_ascii=False, indent=4)

    builder = ArabicAPKBuilder()

    # Example Arabic description
    arabic_input_1 = """
    إنشاء شاشة رئيسية اسمها "الصفحة الرئيسية".
    يجب أن تحتوي الشاشة على نص كبير يقول "مرحباً بالعالم" ومعرف "welcome_text".
    أضف زر باسم "ابدأ الآن" ومعرف "start_button" يعرض نص "ابدأ".
    """

    arabic_input_2 = """
    تصميم شاشة تسجيل الدخول.
    الشاشة يجب أن تحتوي على حقل إدخال للنص يقول "اسم المستخدم" ويكون معرفه "username_field".
    يجب أن يكون حقل الإدخال بعرض كامل وتلميح "أدخل اسم المستخدم هنا".
    أضف حقل إدخال آخر لكلمة المرور بمعرف "password_field" وتلميح "كلمة المرور".
    يوجد زر "تسجيل الدخول" بمعرف "login_button" ويعرض نص "دخول".
    """

    print("\n--- Processing Arabic Input 1 ---")
    apk_data_1 = builder.build_from_description(arabic_input_1)
    builder.create_project_files(apk_data_1)

    print("\n\n--- Processing Arabic Input 2 ---")
    apk_data_2 = builder.build_from_description(arabic_input_2)
    builder.create_project_files(apk_data_2)

    print("\n--- Demo Finished ---")

    # Clean up dummy files and directory
    try:
        os.remove(os.path.join(KNOWLEDGE_BASE_DIR, "arabic_keywords.json"))
        os.rmdir(KNOWLEDGE_BASE_DIR)
    except OSError as e:
        print(f"Error cleaning up: {e}")

    import shutil
    try:
        shutil.rmtree(PROJECT_ROOT)
    except OSError as e:
        print(f"Error cleaning up project directory: {e}")