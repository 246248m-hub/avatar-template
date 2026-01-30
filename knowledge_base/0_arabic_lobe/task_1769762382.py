import re
import os
import json
import subprocess
from typing import List, Dict, Any

# Assume existence of a LanguageLobe for Arabic processing.
# This is a placeholder for demonstration purposes.
class LanguageLobe:
    def __init__(self):
        pass

    def process_natural_language_arabic(self, text: str) -> Dict[str, Any]:
        """
        Simulates processing Arabic natural language input.
        In a real scenario, this would involve sophisticated NLP techniques
        like tokenization, POS tagging, named entity recognition, dependency parsing, etc.
        For this demo, we'll extract simple keywords and intent.
        """
        intent = "unknown"
        entities = {}

        if "إنشاء تطبيق" in text or "بناء تطبيق" in text:
            intent = "create_app"
            # Extract app name if present
            match_app_name = re.search(r"(?:لـ|اسم التطبيق هو)\s+([\w\s]+)", text)
            if match_app_name:
                entities["app_name"] = match_app_name.group(1).strip()
            else:
                entities["app_name"] = "MyNewApp" # Default name

            # Extract basic description or features
            description_match = re.search(r"وصفه (?:هو|هو\s*:)\s*(.+)", text)
            if description_match:
                entities["description"] = description_match.group(1).strip()

        elif "تعديل تطبيق" in text or "تحديث تطبيق" in text:
            intent = "modify_app"
            match_app_name = re.search(r"(?:التطبيق|للتطبيق)\s+([\w\s]+)", text)
            if match_app_name:
                entities["app_name"] = match_app_name.group(1).strip()
            else:
                entities["app_name"] = "TargetApp"

            # Extract modification details
            modification_match = re.search(r"(?:مع|بـ)\s+(.+)", text)
            if modification_match:
                entities["modification_details"] = modification_match.group(1).strip()

        elif "عرض شاشة" in text or "وصف الشاشة" in text:
            intent = "describe_screen"
            match_screen_name = re.search(r"(?:الشاشة|اسم الشاشة)\s+([\w\s]+)", text)
            if match_screen_name:
                entities["screen_name"] = match_screen_name.group(1).strip()
            else:
                entities["screen_name"] = "DefaultScreen"

        # Basic keyword extraction as a fallback or supplementary
        keywords = re.findall(r"\b\w+\b", text, re.UNICODE)
        entities["keywords"] = list(set(keywords)) # Remove duplicates

        return {"intent": intent, "entities": entities}

# Assume existence of a CodeGenerationLobe that can generate Python/Java snippets.
# This is a placeholder for demonstration purposes.
class CodeGenerationLobe:
    def __init__(self):
        pass

    def generate_android_xml_layout(self, screen_name: str, elements: List[Dict[str, str]]) -> str:
        """
        Simulates generating Android XML layout code.
        """
        layout_content = f'<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"\n'
        layout_content += f'    xmlns:tools="http://schemas.android.com/tools"\n'
        layout_content += f'    android:layout_width="match_parent"\n'
        layout_content += f'    android:layout_height="match_parent"\n'
        layout_content += f'    android:orientation="vertical"\n'
        layout_content += f'    tools:context=".{screen_name.capitalize()}Activity">\n\n'

        for element in elements:
            element_type = element.get("type", "TextView")
            element_id = element.get("id", f"id_{element_type.lower()}_{screen_name}")
            text = element.get("text", "")
            layout_width = element.get("layout_width", "wrap_content")
            layout_height = element.get("layout_height", "wrap_content")
            margin_top = element.get("margin_top", "0dp")

            layout_content += f'    <{element_type}\n'
            layout_content += f'        android:id="@+id/{element_id}"\n'
            layout_content += f'        android:layout_width="{layout_width}"\n'
            layout_content += f'        android:layout_height="{layout_height}"\n'
            if text:
                layout_content += f'        android:text="{text}"\n'
            if margin_top != "0dp":
                layout_content += f'        android:layout_marginTop="{margin_top}"\n'
            layout_content += f'    />\n\n'

        layout_content += '</LinearLayout>'
        return layout_content

    def generate_android_activity_java(self, activity_name: str, layout_name: str, elements_to_bind: List[Dict[str, str]]) -> str:
        """
        Simulates generating Android Activity Java code.
        """
        java_content = f'package com.example.{activity_name.lower()};\n\n'
        java_content += 'import androidx.appcompat.app.AppCompatActivity;\n'
        java_content += 'import android.os.Bundle;\n'
        java_content += 'import android.widget.TextView;\n' # Example for TextView binding
        # Add imports for other UI elements as needed
        java_content += '\n'
        java_content += f'public class {activity_name.capitalize()}Activity extends AppCompatActivity {{\n\n'
        java_content += '    @Override\n'
        java_content += f'    protected void onCreate(Bundle savedInstanceState) {{\n'
        java_content += '        super.onCreate(savedInstanceState);\n'
        java_content += f'        setContentView(R.layout.{layout_name});\n\n'

        for element in elements_to_bind:
            element_id = element.get("id")
            element_type = element.get("type", "TextView")
            if element_id:
                java_content += f'        {element_type} {element_id} = findViewById(R.id.{element_id});\n'
                # Example: Set initial text if available in the Arabic processing
                if element.get("initial_text"):
                    java_content += f'        {element_id}.setText("{element.get("initial_text")}");\n'

        java_content += '    }\n'
        java_content += '}\n'
        return java_content

    def generate_android_manifest(self, app_name: str, activities: List[str]) -> str:
        """
        Simulates generating the AndroidManifest.xml file.
        """
        manifest_content = '<?xml version="1.0" encoding="utf-8"?>\n'
        manifest_content += f'<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.{app_name.lower()}">\n\n'
        manifest_content += '    <application\n'
        manifest_content += f'        android:allowBackup="true"\n'
        manifest_content += f'        android:icon="@mipmap/ic_launcher"\n'
        manifest_content += f'        android:label="@string/app_name"\n'
        manifest_content += f'        android:roundIcon="@mipmap/ic_launcher_round"\n'
        manifest_content += f'        android:supportsRtl="true"\n'
        manifest_content += f'        android:theme="@style/Theme.{app_name}">\n\n'

        for activity in activities:
            manifest_content += f'        <activity android:name=".{activity.capitalize()}Activity">\n'
            if activity.lower() == "main": # Assuming the first activity is the launcher
                manifest_content += '            <intent-filter>\n'
                manifest_content += '                <action android:name="android.intent.action.MAIN" />\n'
                manifest_content += '                <category android:name="android.intent.category.LAUNCHER" />\n'
                manifest_content += '            </intent-filter>\n'
            manifest_content += '        </activity>\n\n'

        manifest_content += '    </application>\n'
        manifest_content += '</manifest>\n'
        return manifest_content


class ArabicNLPComponent:
    """
    Module for processing Arabic natural language and extracting structured data
    for Android APK generation.
    """
    def __init__(self, language_lobe: LanguageLobe, code_generation_lobe: CodeGenerationLobe):
        self.language_lobe = language_lobe
        self.code_generation_lobe = code_generation_lobe

    def parse_arabic_request(self, arabic_text: str) -> Dict[str, Any]:
        """
        Parses the Arabic natural language request using the LanguageLobe
        and returns a structured representation of the intent and entities.
        """
        processed_data = self.language_lobe.process_natural_language_arabic(arabic_text)
        return processed_data

    def generate_screen_layout_xml(self, screen_description: str) -> str:
        """
        Generates an Android XML layout based on a simplified screen description
        extracted from Arabic text.
        This is a conceptual mapping. A real implementation would need more
        sophisticated parsing to map descriptions to UI elements.
        """
        # For demonstration, we'll try to extract simple elements
        elements = []
        # Simple heuristic: if "حقل نص" (text field) is mentioned, create an EditText.
        # If "زر" (button) is mentioned, create a Button.
        # If "نص" (text) is mentioned, create a TextView.
        # This would be vastly more complex in a real system.

        # Split description into potential element descriptions
        potential_elements = re.split(r'[، و ]+', screen_description)

        for item in potential_elements:
            item_lower = item.lower()
            if "حقل نص" in item_lower:
                element_name_match = re.search(r"حقل نص\s+([\w\s]+)", item)
                element_text = ""
                if element_name_match:
                    element_name = element_name_match.group(1).strip()
                    match_hint = re.search(r"يحمل النص\s+([\w\s]+)", item)
                    if match_hint:
                        element_text = match_hint.group(1).strip()
                else:
                    element_name = "username_field" # Default

                elements.append({
                    "type": "EditText",
                    "id": f"{element_name.replace(' ', '_')}_et",
                    "layout_width": "match_parent",
                    "layout_height": "wrap_content",
                    "margin_top": "16dp",
                    "hint": element_text if element_text else "Enter text"
                })
            elif "زر" in item_lower:
                element_name_match = re.search(r"زر\s+([\w\s]+)", item)
                button_text = "Click Me"
                if element_name_match:
                    button_name = element_name_match.group(1).strip()
                    match_button_label = re.search(r"يكون اسمه\s+([\w\s]+)", item)
                    if match_button_label:
                        button_text = match_button_label.group(1).strip()
                else:
                    button_name = "submit_button"

                elements.append({
                    "type": "Button",
                    "id": f"{button_name.replace(' ', '_')}_btn",
                    "layout_width": "wrap_content",
                    "layout_height": "wrap_content",
                    "margin_top": "16dp",
                    "text": button_text
                })
            elif "نص" in item_lower and "عنوان" not in item_lower: # Avoid interpreting "عنوان" as just text
                element_name_match = re.search(r"نص\s+([\w\s]+)", item)
                text_content = ""
                if element_name_match:
                    element_name = element_name_match.group(1).strip()
                    match_value = re.search(r"قيمته\s+([\w\s]+)", item)
                    if match_value:
                        text_content = match_value.group(1).strip()
                else:
                    element_name = "info_text"

                elements.append({
                    "type": "TextView",
                    "id": f"{element_name.replace(' ', '_')}_tv",
                    "layout_width": "wrap_content",
                    "layout_height": "wrap_content",
                    "margin_top": "8dp",
                    "text": text_content if text_content else "Information"
                })
            elif "عنوان" in item_lower: # Treat as a prominent TextView
                element_name_match = re.search(r"عنوان\s+([\w\s]+)", item)
                title_text = "App Title"
                if element_name_match:
                    title_text = element_name_match.group(1).strip()

                elements.append({
                    "type": "TextView",
                    "id": "app_title_tv",
                    "layout_width": "match_parent",
                    "layout_height": "wrap_content",
                    "margin_top": "32dp",
                    "text": title_text,
                    "style": "TextAppearance.AppCompat.Large" # Conceptual style
                })


        # If no elements are parsed, create a default one
        if not elements:
            elements.append({
                "type": "TextView",
                "id": "default_tv",
                "layout_width": "wrap_content",
                "layout_height": "wrap_content",
                "text": "Default Screen Content"
            })

        # We need a screen name to pass to the generator, use a default if not provided
        screen_name = "Main" # Default for layout generation

        return self.code_generation_lobe.generate_android_xml_layout(screen_name, elements)

    def generate_activity_java(self, activity_name: str, layout_elements_info: List[Dict[str, Any]]) -> str:
        """
        Generates Android Activity Java code based on the activity name and
        information about UI elements in its layout.
        """
        # Extract IDs and types for binding
        elements_to_bind = []
        for element in layout_elements_info:
            elements_to_bind.append({
                "id": element.get("id"),
                "type": element.get("type"),
                "initial_text": element.get("text", "") # Pass initial text if available
            })
        return self.code_generation_lobe.generate_android_activity_java(activity_name, activity_name.lower(), elements_to_bind)

    def create_apk_structure(self, app_name: str, processed_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the creation of a basic APK structure (files and directories)
        based on the processed Arabic request.
        Returns a dictionary representing the project structure and content.
        """
        project_structure = {
            "app_name": app_name,
            "manifest": "",
            "java_src": {},
            "res": {
                "layout": {},
                "values": {}
            }
        }

        activities = []
        layout_files_content = {}

        # Handle different intents
        intent = processed_request.get("intent")
        entities = processed_request.get("entities", {})

        if intent == "create_app":
            app_description = entities.get("description", "A new Android application.")
            # For simplicity, we'll create a single main activity and screen
            main_activity_name = "MainActivity"
            activities.append(main_activity_name)

            # Generate a default layout for the main screen
            # In a real scenario, this would be more nuanced, parsing description for elements
            default_screen_description = "A title and a text field and a submit button."
            layout_xml = self.generate_screen_layout_xml(default_screen_description)
            layout_files_content["activity_main.xml"] = layout_xml

            # Extract UI elements from the generated XML to pass to Java generation
            # This requires parsing the generated XML, a simplified approach here:
            generated_layout_elements = self._parse_generated_xml_for_elements(layout_xml)
            java_activity_code = self.generate_activity_java(main_activity_name, generated_layout_elements)
            project_structure["java_src"][f"{main_activity_name}.java"] = java_activity_code

            # Generate manifest
            manifest_content = self.code_generation_lobe.generate_android_manifest(app_name, activities)
            project_structure["manifest"] = manifest_content

            # Basic values/strings.xml (conceptual)
            project_structure["res"]["values"]["strings.xml"] = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <string name="app_name">{app_name}</string>\n</resources>'.format(app_name=app_name)


        elif intent == "describe_screen":
            screen_name = entities.get("screen_name", "NewScreen")
            # If a description is provided (e.g., "وصف الشاشة الرئيسية: تحتوي على عنوان وزر")
            # we'd use that. For now, we assume the Arabic text directly describes it.
            # This part is highly dependent on how `process_natural_language_arabic`
            # extracts screen descriptions. Let's assume it can return a structured description.

            # Placeholder for structured screen description extraction
            # If entities contains a 'screen_description' key:
            # screen_description_text = entities.get("screen_description", "A welcome message and a button.")
            # For this demo, we'll re-use generate_screen_layout_xml with a placeholder:
            screen_description_text = "A title 'Welcome' and a button 'Go'."
            layout_xml = self.generate_screen_layout_xml(screen_description_text)
            layout_filename = f"screen_{screen_name.lower().replace(' ', '_')}.xml"
            layout_files_content[layout_filename] = layout_xml

            # Create a corresponding activity for this screen
            activity_name = f"{screen_name.capitalize()}Activity"
            activities.append(activity_name)
            generated_layout_elements = self._parse_generated_xml_for_elements(layout_xml)
            java_activity_code = self.generate_activity_java(activity_name, generated_layout_elements)
            project_structure["java_src"][f"{activity_name}.java"] = java_activity_code

            # Update manifest if this is a new activity
            if not project_structure["manifest"]: # If manifest wasn't created by 'create_app'
                manifest_content = self.code_generation_lobe.generate_android_manifest(app_name, activities)
                project_structure["manifest"] = manifest_content
            else:
                # If manifest exists, we'd need to parse it and add the new activity
                # For simplicity here, we assume manifest is generated only once for 'create_app'
                pass

        elif intent == "modify_app":
            # This would involve reading existing project files, parsing, and applying changes.
            # For this demo, we'll simulate by re-generating with some modifications.
            print("Modification intent detected. (Simulation: Re-generating basic structure)")
            # In a real scenario, you'd fetch existing project structure from storage.
            app_name = entities.get("app_name", "ModifiedApp")
            modification_details = entities.get("modification_details", "Add a new feature.")

            main_activity_name = "MainActivity"
            activities.append(main_activity_name)

            # Simulate modification by adding more elements to the default screen
            modified_screen_description = "A title, a text field, a submit button, and a text view for status."
            layout_xml = self.generate_screen_layout_xml(modified_screen_description)
            layout_files_content["activity_main.xml"] = layout_xml

            generated_layout_elements = self._parse_generated_xml_for_elements(layout_xml)
            java_activity_code = self.generate_activity_java(main_activity_name, generated_layout_elements)
            project_structure["java_src"][f"{main_activity_name}.java"] = java_activity_code

            manifest_content = self.code_generation_lobe.generate_android_manifest(app_name, activities)
            project_structure["manifest"] = manifest_content
            project_structure["res"]["values"]["strings.xml"] = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <string name="app_name">{app_name}</string>\n</resources>'.format(app_name=app_name)

        else:
            print(f"Unknown intent '{intent}' for APK structure creation.")
            return {}

        project_structure["res"]["layout"] = layout_files_content
        return project_structure

    def _parse_generated_xml_for_elements(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        A rudimentary parser to extract element IDs and types from generated XML.
        In a real system, a proper XML parser (like ElementTree) would be used.
        This is for demonstration to feed into the Java code generation.
        """
        elements = []
        # Regex to find <ElementType android:id="@+id/element_id" ... />
        # This is a simplified regex and might fail on complex XML.
        pattern = re.compile(r"<(\w+)\s+android:id=\"@\+id/(\w+)\"[^>]*>", re.IGNORECASE)
        matches = pattern.finditer(xml_content)
        for match in matches:
            element_type = match.group(1)
            element_id = match.group(2)
            # Try to find 'android:text' for initial text in Java
            text_match = re.search(rf"android:text=\"(.*?)\"", xml_content[match.end():], re.IGNORECASE)
            initial_text = text_match.group(1) if text_match else ""
            elements.append({"type": element_type, "id": element_id, "text": initial_text})
        return elements


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize lobes (placeholders)
    language_lobe = LanguageLobe()
    code_generation_lobe = CodeGenerationLobe()

    # Instantiate the Arabic NLP Component
    arabic_nlp_component = ArabicNLPComponent(language_lobe, code_generation_lobe)

    print("--- Testing Arabic NLP Component ---")

    # Test case 1: Create a new app
    arabic_request_create = "أريد إنشاء تطبيق جديد اسمه 'تطبيقي الأول' ووصفه هو 'هذا تطبيق بسيط لعرض رسالة ترحيب'."
    print(f"\nProcessing request: {arabic_request_create}")
    processed_data_create = arabic_nlp_component.parse_arabic_request(arabic_request_create)
    print(f"Parsed data: {json.dumps(processed_data_create, indent=2)}")

    app_structure_create = arabic_nlp_component.create_apk_structure(
        processed_data_create["entities"].get("app_name", "DefaultApp"),
        processed_data_create
    )
    print("\nGenerated App Structure (Create App):")
    print(json.dumps(app_structure_create, indent=2, sort_keys=True))

    # Test case 2: Describe a screen
    arabic_request_screen = "وصف الشاشة الرئيسية: تحتوي على عنوان 'مرحباً بكم' وزر 'بدء'."
    print(f"\nProcessing request: {arabic_request_screen}")
    processed_data_screen = arabic_nlp_component.parse_arabic_request(arabic_request_screen)
    print(f"Parsed data: {json.dumps(processed_data_screen, indent=2)}")

    # For describe_screen, we need an app name context if it's not creating a new app.
    # Let's assume a default app name for this scenario.
    app_structure_screen = arabic_nlp_component.create_apk_structure("MyAppContext", processed_data_screen)
    print("\nGenerated App Structure (Describe Screen):")
    print(json.dumps(app_structure_screen, indent=2, sort_keys=True))

    # Test case 3: Modify an app
    arabic_request_modify = "تعديل التطبيق 'تطبيقي الأول' بإضافة ميزة تسجيل الدخول."
    print(f"\nProcessing request: {arabic_request_modify}")
    processed_data_modify = arabic_nlp_component.parse_arabic_request(arabic_request_modify)
    print(f"Parsed data: {json.dumps(processed_data_modify, indent=2)}")

    app_structure_modify = arabic_nlp_component.create_apk_structure(
        processed_data_modify["entities"].get("app_name", "ModifiedApp"),
        processed_data_modify
    )
    print("\nGenerated App Structure (Modify App):")
    print(json.dumps(app_structure_modify, indent=2, sort_keys=True))

    # --- Conceptual interaction with other lobes ---
    print("\n--- Conceptual interaction with other lobes (Simulated) ---")

    # Lobe 0_language_lobe interaction is demonstrated by LanguageLobe usage.
    print("Lobe 0_language_lobe: Processed Arabic text using LanguageLobe.")

    # Lobe 6_synthesis_lobe would take the app_structure and potentially
    # orchestrate building it into an APK using Lobe 8_apk_compiler_lobe.
    # For now, we just show the structure it would receive.
    print("Lobe 6_synthesis_lobe: Would receive the 'app_structure' dictionary.")
    # Example conceptual call:
    # from lobe_6_synthesis_lobe import SynthesisLobe
    # synthesis_lobe = SynthesisLobe()
    # synthesis_lobe.process_project_structure(app_structure_create)

    # Lobe 8_apk_compiler_lobe would take the output from SynthesisLobe
    # and build the actual APK.
    print("Lobe 8_apk_compiler_lobe: Would receive compiled project files from SynthesisLobe to build APK.")
    # Example conceptual call:
    # from lobe_8_apk_compiler_lobe import ApkCompilerLobe
    # apk_compiler_lobe = ApkCompilerLobe()
    # apk_path = apk_compiler_lobe.compile_project(app_structure_create)
    # print(f"Conceptual APK path: {apk_path}")

    print("\n--- Arabic NLP Component Demo Finished ---")