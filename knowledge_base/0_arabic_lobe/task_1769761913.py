import os
import re
from typing import List, Dict, Any

# Define a simple structure for representing an Android Activity
class AndroidActivity:
    def __init__(self, name: str, layout_resource: str = None, onCreate_logic: str = ""):
        self.name = name
        self.layout_resource = layout_resource
        self.onCreate_logic = onCreate_logic

    def __str__(self):
        return f"Activity(name='{self.name}', layout='{self.layout_resource}', onCreate='{self.onCreate_logic}')"

class ArabicAPKBuilder:
    def __init__(self, project_name: str = "ArabicApp", package_name: str = "com.example.arabicapp"):
        self.project_name = project_name
        self.package_name = package_name
        self.activities: Dict[str, AndroidActivity] = {}
        self.main_activity_name: str = "MainActivity"

    def add_activity(self, activity_name: str, layout_resource: str = None, onCreate_logic: str = ""):
        """Adds a new Android Activity to the APK structure."""
        if activity_name in self.activities:
            print(f"Warning: Activity '{activity_name}' already exists. Overwriting.")
        self.activities[activity_name] = AndroidActivity(activity_name, layout_resource, onCreate_logic)
        if not self.main_activity_name:
            self.main_activity_name = activity_name

    def generate_manifest_xml(self) -> str:
        """Generates a basic AndroidManifest.xml file."""
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
"""
        for activity_name, activity in self.activities.items():
            intent_filter = ""
            if activity_name == self.main_activity_name:
                intent_filter = """
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>"""
            manifest_content += f"""
        <activity android:name=".{activity_name}" android:label="@string/{activity_name.lower()}">
{intent_filter}
        </activity>"""
        manifest_content += """
    </application>
</manifest>"""
        return manifest_content

    def generate_activity_java_code(self, activity: AndroidActivity) -> str:
        """Generates Java code for an Android Activity."""
        layout_setting = ""
        if activity.layout_resource:
            layout_setting = f"setContentView(R.layout.{activity.layout_resource});\n        "

        onCreate_method = f"""
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        {layout_setting}{activity.onCreate_logic}
    }}"""

        java_code = f"""
package {self.package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity.name} extends AppCompatActivity {{
{onCreate_method}
}}
"""
        return java_code

    def generate_project_structure(self, output_dir: str):
        """Generates the basic directory structure for an Android project."""
        project_root = os.path.join(output_dir, self.project_name)
        java_dir = os.path.join(project_root, "app", "src", "main", "java", *self.package_name.split('.'))
        res_layout_dir = os.path.join(project_root, "app", "src", "main", "res", "layout")
        res_values_dir = os.path.join(project_root, "app", "src", "main", "res", "values")
        manifest_dir = os.path.join(project_root, "app", "src", "main")

        os.makedirs(java_dir, exist_ok=True)
        os.makedirs(res_layout_dir, exist_ok=True)
        os.makedirs(res_values_dir, exist_ok=True)

        # Write Manifest
        manifest_path = os.path.join(manifest_dir, "AndroidManifest.xml")
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(self.generate_manifest_xml())
            print(f"Generated: {manifest_path}")

        # Write Activities
        for activity_name, activity in self.activities.items():
            activity_java_path = os.path.join(java_dir, f"{activity_name}.java")
            with open(activity_java_path, "w", encoding="utf-8") as f:
                f.write(self.generate_activity_java_code(activity))
                print(f"Generated: {activity_java_path}")

        # Create dummy layout files if specified
        for activity in self.activities.values():
            if activity.layout_resource:
                layout_file_path = os.path.join(res_layout_dir, f"{activity.layout_resource}.xml")
                if not os.path.exists(layout_file_path):
                    with open(layout_file_path, "w", encoding="utf-8") as f:
                        f.write(f"<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\"\n    xmlns:app=\"http://schemas.android.com/apk/res-auto\"\n    xmlns:tools=\"http://schemas.android.com/tools\"\n    android:layout_width=\"match_parent\"\n    android:layout_height=\"match_parent\"\n    tools:context=\".{activity.name}\">\n    <!-- Content for {activity.layout_resource} -->\n</LinearLayout>")
                    print(f"Generated: {layout_file_path}")

        # Write basic strings.xml
        strings_path = os.path.join(res_values_dir, "strings.xml")
        if not os.path.exists(strings_path):
            with open(strings_path, "w", encoding="utf-8") as f:
                f.write(f"""<resources>
    <string name="app_name">{self.project_name}</string>
    <string name="mainactivity">Main Activity</string>
</resources>""")
            print(f"Generated: {strings_path}")

        # Write basic styles.xml
        styles_path = os.path.join(res_values_dir, "styles.xml")
        if not os.path.exists(styles_path):
            with open(styles_path, "w", encoding="utf-8") as f:
                f.write(f"""<resources>
    <!-- Base application theme. -->
    <style name="Theme.{self.project_name}" parent="Theme.AppCompat.Light.DarkActionBar">
        <!-- Primary brand color. -->
        <item name="colorPrimary">#6200EE</item>
        <item name="colorPrimaryVariant">#3700B3</item>
        <item name="colorOnPrimary">#FFFFFF</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">#03DAC6</item>
        <item name="colorSecondaryVariant">#03DAC6</item>
        <item name="colorOnSecondary">#000000</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor">#000000</item>
        <!-- Customize your theme here. -->
    </style>
</resources>""")
            print(f"Generated: {styles_path}")

        print(f"\n--- Project structure for '{self.project_name}' generated in '{output_dir}' ---")


# --- Lobe 5_xml_to_activity_mapper ---
# This lobe's responsibility is to parse XML layouts and map them to Android Activity definitions.
# It will infer activity names and layout resource names from the XML.
# It also needs to handle potential Arabic text within the XML and associate it with UI elements.

class XmlToActivityMapper:
    def __init__(self, arabic_parser_module):
        # Injecting the ArabicParser to understand Arabic text and its context.
        self.arabic_parser = arabic_parser_module

    def parse_layout_xml(self, xml_content: str, activity_name_hint: str = "Activity") -> AndroidActivity:
        """
        Parses an XML layout string and creates an AndroidActivity definition.
        It infers the layout resource name and attempts to generate basic onCreate logic
        if Arabic text elements are found.
        """
        layout_resource_name = None
        onCreate_logic_parts = []

        # Simple regex to find the root layout tag name.
        root_tag_match = re.search(r"<(\w+)", xml_content)
        if root_tag_match:
            # Extracting the tag name and converting to snake_case for resource naming convention.
            layout_resource_name = re.sub(r'(?<!^)(?=[A-Z])', '_', root_tag_match.group(1)).lower()
            # Remove namespaces or prefixes if present
            layout_resource_name = re.sub(r'^.*?[:]', '', layout_resource_name)


        # Placeholder for Arabic text analysis. In a real scenario, this would involve
        # Lobe 0_arabic_lobe or a similar parsing mechanism.
        # For demonstration, we'll look for common Android UI elements that might contain Arabic text.
        arabic_elements = re.findall(r'(?:android:text|android:hint)="([^"]*?[\u0600-\u06FF]+[^"]*?)"', xml_content, re.IGNORECASE)

        if arabic_elements:
            for element_text in arabic_elements:
                # Use the Arabic parser to understand the meaning/intent of the text.
                # This is a crucial integration point.
                parsed_data = self.arabic_parser.parse_arabic_text(element_text)
                if parsed_data and parsed_data.get('intent'):
                    # Example: If Arabic text is "تسجيل الدخول" (Login),
                    # we might generate code to set up a login button listener.
                    intent = parsed_data['intent']
                    if "login" in intent.lower() or "تسجيل" in intent.lower():
                        # This is a simplified example. Actual code generation would be more complex.
                        # We are trying to infer actions from Arabic text.
                        onCreate_logic_parts.append(f"// Found login intent from Arabic text: '{element_text}'")
                        # Example: findViewById(R.id.login_button).setOnClickListener(...)
                    elif "search" in intent.lower() or "بحث" in intent.lower():
                        onCreate_logic_parts.append(f"// Found search intent from Arabic text: '{element_text}'")
                    # Add more mappings for other intents

        # Construct a default activity name if not explicitly provided or inferrable.
        activity_name = activity_name_hint.capitalize()
        if layout_resource_name:
            # Try to derive an activity name from the layout name, e.g., 'activity_main' -> 'MainActivity'
            name_parts = layout_resource_name.split('_')
            if name_parts[0] == 'activity' and len(name_parts) > 1:
                activity_name = "".join(word.capitalize() for word in name_parts[1:])
            else:
                activity_name = "".join(word.capitalize() for word in name_parts)


        # If no layout resource was found, create a dummy one for the activity.
        if not layout_resource_name:
            layout_resource_name = f"activity_{activity_name.lower()}"
            print(f"Warning: No root layout tag found in XML. Using default layout resource name: '{layout_resource_name}'")

        onCreate_logic = "\n        ".join(onCreate_logic_parts)

        return AndroidActivity(activity_name, layout_resource_name, onCreate_logic)

    def map_xml_to_activities(self, xml_files: List[str]) -> Dict[str, AndroidActivity]:
        """
        Iterates through a list of XML layout file paths, parses each, and returns a dictionary
        mapping activity names to AndroidActivity objects.
        """
        activities_map = {}
        for xml_file_path in xml_files:
            if not os.path.exists(xml_file_path):
                print(f"Warning: XML file not found: {xml_file_path}")
                continue
            try:
                with open(xml_file_path, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                    # Attempt to infer activity name from filename if possible
                    base_name = os.path.basename(xml_file_path).replace('.xml', '')
                    activity_hint = base_name.replace('activity_', '').replace('_', '').capitalize()
                    android_activity = self.parse_layout_xml(xml_content, activity_name_hint=activity_hint)
                    activities_map[android_activity.name] = android_activity
                    print(f"Mapped '{xml_file_path}' to Activity: {android_activity.name} (Layout: {android_activity.layout_resource})")
            except Exception as e:
                print(f"Error parsing XML file {xml_file_path}: {e}")
        return activities_map


# --- Dummy Arabic Parser Module (Placeholder for Lobe 0_arabic_lobe) ---
# This class simulates the functionality of Lobe 0_arabic_lobe for demonstration purposes.
# In a real implementation, this would be the actual Lobe 0.
class DummyArabicParser:
    def parse_arabic_text(self, text: str) -> Dict[str, Any]:
        """
        Simulates parsing Arabic text to extract intent and keywords.
        This is a highly simplified example.
        """
        text = text.strip()
        intent = "unknown"
        keywords = []

        # Simple keyword matching for demonstration
        if "تسجيل" in text or "دخول" in text:
            intent = "login_intent"
            keywords = ["login", "account", "signin"]
        elif "بحث" in text or "اوجد" in text:
            intent = "search_intent"
            keywords = ["search", "find", "query"]
        elif "إرسال" in text or "رسالة" in text:
            intent = "send_message_intent"
            keywords = ["message", "send", "chat"]
        elif "حفظ" in text or "تخزين" in text:
            intent = "save_intent"
            keywords = ["save", "store", "record"]

        # Basic sentiment analysis simulation
        sentiment = "neutral"
        if "جميل" in text or "رائع" in text:
            sentiment = "positive"
        elif "سيء" in text or "مشكلة" in text:
            sentiment = "negative"

        return {
            "original_text": text,
            "intent": intent,
            "keywords": keywords,
            "sentiment": sentiment,
            "arabic_script_present": bool(re.search(r'[\u0600-\u06FF]', text))
        }

# --- Example Usage ---
if __name__ == '__main__':
    # Initialize the dummy Arabic parser
    arabic_parser_instance = DummyArabicParser()

    # Initialize the XML to Activity Mapper, injecting the Arabic parser
    xml_mapper = XmlToActivityMapper(arabic_parser_instance)

    # Create dummy XML layout files for demonstration
    os.makedirs("temp_layouts", exist_ok=True)
    with open("temp_layouts/activity_login.xml", "w", encoding="utf-8") as f:
        f.write("""<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    tools:context=".LoginActivity">
    <EditText android:id="@+id/username_edit" android:layout_width='match_parent' android:layout_height='wrap_content' android:hint='اسم المستخدم'/>
    <EditText android:id="@+id/password_edit" android:layout_width='match_parent' android:layout_height='wrap_content' android:hint='كلمة المرور'/>
    <Button android:id="@+id/login_button" android:layout_width='wrap_content' android:layout_height='wrap_content' android:text='تسجيل الدخول'/>
</LinearLayout>""")

    with open("temp_layouts/activity_home.xml", "w", encoding="utf-8") as f:
        f.write("""<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".HomeActivity">
    <TextView android:layout_width='wrap_content' android:layout_height='wrap_content' android:text='مرحبا بك!'/>
    <Button android:layout_width='wrap_content' android:layout_height='wrap_content' android:text='بحث عن منتجات'/>
</RelativeLayout>""")

    with open("temp_layouts/settings_screen.xml", "w", encoding="utf-8") as f:
        f.write("""<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".SettingsActivity">
    <TextView android:layout_width='match_parent' android:layout_height='match_parent' android:text='إعدادات التطبيق'/>
</FrameLayout>""")

    # List of dummy XML layout files
    layout_files = [
        "temp_layouts/activity_login.xml",
        "temp_layouts/activity_home.xml",
        "temp_layouts/settings_screen.xml"
    ]

    # Map the XML files to AndroidActivity objects
    activities_data = xml_mapper.map_xml_to_activities(layout_files)

    # Initialize the APK Builder
    apk_builder = ArabicAPKBuilder(project_name="MyArabicApp", package_name="com.example.myarabicapp")

    # Add the parsed activities to the APK Builder
    for activity_name, activity_obj in activities_data.items():
        apk_builder.add_activity(activity_name, activity_obj.layout_resource, activity_obj.onCreate_logic)

    # Set a default main activity if not already set by mapping logic
    if not apk_builder.main_activity_name and activities_data:
        apk_builder.main_activity_name = list(activities_data.keys())[0]
        print(f"Setting default main activity to: {apk_builder.main_activity_name}")

    # Generate the project structure
    output_directory = "generated_apk_project"
    os.makedirs(output_directory, exist_ok=True)
    apk_builder.generate_project_structure(output_directory)

    print("\n--- XmlToActivityMapper Module Demo Finished ---")

    # Clean up dummy files
    print("\n--- Cleaning up dummy layout files ---")
    if os.path.exists("temp_layouts"):
        import shutil
        shutil.rmtree("temp_layouts")
        print("Dummy layout directory removed.")

    # This module successfully maps XML layouts to Activity definitions,
    # integrating with a (simulated) Arabic parser to infer potential logic from Arabic text.
    # It sets the stage for Lobe 4_code_generation_lobe to use these definitions
    # to generate actual Java/Kotlin code for the Android Activities.

    # Interlinking to the next logical step:
    # The output of this module (the `apk_builder` object with its `activities` populated)
    # is what Lobe 4_code_generation_lobe would consume.
    print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---")