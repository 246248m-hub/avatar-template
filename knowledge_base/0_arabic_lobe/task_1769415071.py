import re
import os
import json
import logging
from typing import Dict, List, Tuple, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Constants ---
JAVA_PROJECT_DIR = "temp_java_project"
MANIFEST_TEMPLATE_PATH = "templates/AndroidManifest.xml.template"
GRADLE_BUILD_TEMPLATE_PATH = "templates/build.gradle.template"
APP_BUILD_GRADLE_TEMPLATE_PATH = "templates/app/build.gradle.template"
SETTINGS_GRADLE_TEMPLATE_PATH = "templates/settings.gradle.template"
GRADLE_WRAPPER_PROPERTIES_TEMPLATE_PATH = "templates/gradle/wrapper/gradle-wrapper.properties.template"
GRADLEW_TEMPLATE_PATH = "templates/gradlew"
GRADLEW_BAT_TEMPLATE_PATH = "templates/gradlew.bat"
MAIN_ACTIVITY_TEMPLATE_PATH = "templates/MainActivity.java.template"
STRINGS_XML_TEMPLATE_PATH = "templates/res/values/strings.xml.template"
COLORS_XML_TEMPLATE_PATH = "templates/res/values/colors.xml.template"
THEMES_XML_TEMPLATE_PATH = "templates/res/values/themes.xml.template"

class Lobe2ArabicParser:
    """
    Lobe 2: Arabic Parser.
    This lobe is responsible for parsing natural language Arabic input
    and extracting structured information relevant for APK generation.
    It identifies key components like package names, activity names,
    permissions, UI elements, and their properties.
    """

    def __init__(self):
        logging.info("Lobe 2 (Arabic Parser) initialized.")

    def parse_arabic_prompt(self, arabic_prompt: str) -> Dict[str, Any]:
        """
        Parses an Arabic natural language prompt to extract structured APK
        configuration.

        Args:
            arabic_prompt: The natural language Arabic prompt describing the APK.

        Returns:
            A dictionary containing structured information extracted from the prompt.
        """
        logging.info(f"Parsing Arabic prompt: '{arabic_prompt[:50]}...'")

        parsed_data = {
            "package_name": None,
            "app_name": "MyArabicApp",
            "activities": [],
            "permissions": [],
            "ui_elements": [],
            "version_code": 1,
            "version_name": "1.0"
        }

        # --- Basic Parsing Rules (Illustrative - needs robust NLP for real-world) ---

        # Package Name
        package_match = re.search(r"اسم الحزمة الخاص بك هو ([\w.]+)", arabic_prompt)
        if package_match:
            parsed_data["package_name"] = package_match.group(1)
            logging.info(f"Extracted package name: {parsed_data['package_name']}")

        # App Name
        app_name_match = re.search(r"اسم التطبيق هو ([\w\s]+)", arabic_prompt)
        if app_name_match:
            parsed_data["app_name"] = app_name_match.group(1).strip()
            logging.info(f"Extracted app name: {parsed_data['app_name']}")

        # Permissions
        permissions_match = re.findall(r"يتطلب صلاحية ([\w.]+)", arabic_prompt)
        if permissions_match:
            parsed_data["permissions"] = [f"android.permission.{perm.upper()}" for perm in permissions_match]
            logging.info(f"Extracted permissions: {parsed_data['permissions']}")

        # Activities (simple rule: assume one main activity if not specified)
        activity_match = re.search(r"الشاشة الرئيسية تسمى ([\w]+)", arabic_prompt)
        if activity_match:
            activity_name = activity_match.group(1)
            parsed_data["activities"].append({"name": activity_name, "is_main": True})
            logging.info(f"Extracted main activity: {activity_name}")
        else:
            # Default main activity if none specified
            parsed_data["activities"].append({"name": "MainActivity", "is_main": True})
            logging.info("No specific main activity found, defaulting to 'MainActivity'.")

        # UI Elements (very basic example: button and text)
        buttons = re.findall(r"زر مكتوب عليه \"(.*?)\" اسمه (\w+)", arabic_prompt)
        for text, name in buttons:
            parsed_data["ui_elements"].append({"type": "Button", "text": text, "id": name})
            logging.info(f"Extracted Button: text='{text}', id='{name}'")

        text_views = re.findall(r"نص يعرض \"(.*?)\" اسمه (\w+)", arabic_prompt)
        for text, name in text_views:
            parsed_data["ui_elements"].append({"type": "TextView", "text": text, "id": name})
            logging.info(f"Extracted TextView: text='{text}', id='{name}'")

        # Version Code
        version_code_match = re.search(r"رقم الإصدار هو (\d+)", arabic_prompt)
        if version_code_match:
            parsed_data["version_code"] = int(version_code_match.group(1))
            logging.info(f"Extracted version code: {parsed_data['version_code']}")

        # Version Name
        version_name_match = re.search(r"اسم الإصدار هو ([\d.]+)", arabic_prompt)
        if version_name_match:
            parsed_data["version_name"] = version_name_match.group(1)
            logging.info(f"Extracted version name: {parsed_data['version_name']}")

        # --- Data Validation and Cleanup ---
        if not parsed_data["package_name"]:
            logging.warning("Package name not found in prompt. Defaulting to 'com.example.arabicapp'.")
            parsed_data["package_name"] = "com.example.arabicapp"
            # Ensure the default package name is added to the activities if no specific activity was found.
            if not any(a.get("is_main") for a in parsed_data["activities"]):
                parsed_data["activities"].append({"name": "MainActivity", "is_main": True})


        # Ensure a main activity exists, default if necessary and package name is available.
        if not any(a.get("is_main") for a in parsed_data["activities"]) and parsed_data["package_name"]:
            logging.warning("No main activity explicitly defined. Adding 'MainActivity' as main.")
            parsed_data["activities"].append({"name": "MainActivity", "is_main": True})

        # Fallback for activity name if it wasn't extracted and package name exists
        if parsed_data["activities"] and not parsed_data["activities"][0].get("name") and parsed_data["package_name"]:
            parsed_data["activities"][0]["name"] = "MainActivity"
            logging.info("Activity name was missing, defaulted to 'MainActivity'.")


        logging.info("Arabic prompt parsing completed.")
        return parsed_data

# --- Helper functions to create dummy project structure and files ---

def _create_directory_if_not_exists(path: str):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def _create_file_with_content(filepath: str, content: str):
    """Creates a file with the given content."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Created file: {filepath}")

def _read_template(template_path: str) -> str:
    """Reads content from a template file."""
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"Template file not found: {template_path}")
        raise

def _populate_template(template_content: str, replacements: Dict[str, str]) -> str:
    """Populates a template string with given replacements."""
    for key, value in replacements.items():
        template_content = template_content.replace(f"{{{{ {key} }}}}", str(value))
    return template_content

def setup_android_project_structure(config: Dict[str, Any]):
    """Sets up the basic Android project structure and essential files."""
    logging.info("Setting up Android project structure...")
    _create_directory_if_not_exists(JAVA_PROJECT_DIR)
    _create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", config["package_name"].replace(".", os.sep)))
    _create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "values"))
    _create_directory_if_not_exists(os.path.join(JAVA_PROJECT_DIR, "gradle", "wrapper"))

    # Create AndroidManifest.xml
    manifest_template = _read_template(MANIFEST_TEMPLATE_PATH)
    manifest_replacements = {
        "package_name": config["package_name"],
        "version_code": config["version_code"],
        "version_name": config["version_name"],
        "app_name": config.get("app_name", "MyApp"),
        "permissions": "\n".join([f'    <uses-permission android:name="{perm}" />' for perm in config.get("permissions", [])]),
        "activities": "\n".join([
            f'        <activity android:name=".{act["name"]}" {"android:exported=\"true\"" if act.get("is_main") else ""}>'
            f'            <intent-filter>{"" if not act.get("is_main") else """\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />"""}\n            </intent-filter>\n        </activity>'
            for act in config.get("activities", [])
        ])
    }
    populated_manifest = _populate_template(manifest_template, manifest_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "AndroidManifest.xml"), populated_manifest)

    # Create build.gradle (Project level)
    build_gradle_template = _read_template(GRADLE_BUILD_TEMPLATE_PATH)
    build_gradle_replacements = {
        "kotlin_version": "1.7.10" # Example version
    }
    populated_build_gradle = _populate_template(build_gradle_template, build_gradle_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "build.gradle"), populated_build_gradle)

    # Create app/build.gradle (Module level)
    app_build_gradle_template = _read_template(APP_BUILD_GRADLE_TEMPLATE_PATH)
    app_build_gradle_replacements = {
        "compile_sdk": "33", # Example version
        "build_tools_sdk": "33.0.0", # Example version
        "min_sdk": "21", # Example version
        "target_sdk": "33", # Example version
        "version_code": config["version_code"],
        "version_name": config["version_name"],
        "application_id": config["package_name"],
        "java_source_compatibility": "1.8",
        "kotlin_source_compatibility": "1.8"
    }
    populated_app_build_gradle = _populate_template(app_build_gradle_template, app_build_gradle_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "app", "build.gradle"), populated_app_build_gradle)

    # Create settings.gradle
    settings_gradle_template = _read_template(SETTINGS_GRADLE_TEMPLATE_PATH)
    settings_gradle_replacements = {
        "project_dir": JAVA_PROJECT_DIR
    }
    populated_settings_gradle = _populate_template(settings_gradle_template, settings_gradle_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "settings.gradle"), populated_settings_gradle)

    # Create gradle/wrapper/gradle-wrapper.properties
    gradle_wrapper_properties_template = _read_template(GRADLE_WRAPPER_PROPERTIES_TEMPLATE_PATH)
    gradle_wrapper_properties_replacements = {
        "gradle_version": "7.5" # Example version
    }
    populated_gradle_wrapper_properties = _populate_template(gradle_wrapper_properties_template, gradle_wrapper_properties_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.properties"), populated_gradle_wrapper_properties)

    # Create gradlew and gradlew.bat
    gradlew_content = _read_template(GRADLEW_TEMPLATE_PATH)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "gradlew"), gradlew_content)
    os.chmod(os.path.join(JAVA_PROJECT_DIR, "gradlew"), 0o755) # Make executable

    gradlew_bat_content = _read_template(GRADLEW_BAT_TEMPLATE_PATH)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "gradlew.bat"), gradlew_bat_content)

    # Create placeholder Java files for activities
    main_activity_template = _read_template(MAIN_ACTIVITY_TEMPLATE_PATH)
    main_activity_replacements = {
        "package_name": config["package_name"],
        "activity_name": config["activities"][0]["name"] if config.get("activities") else "MainActivity",
        "layout_name": f"activity_{config['activities'][0]['name'].lower()}" if config.get("activities") else "activity_main"
    }
    populated_main_activity = _populate_template(main_activity_template, main_activity_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", config["package_name"].replace(".", os.sep), f"{main_activity_replacements['activity_name']}.java"), populated_main_activity)

    # Create placeholder resources
    strings_xml_template = _read_template(STRINGS_XML_TEMPLATE_PATH)
    strings_xml_replacements = {
        "app_name": config.get("app_name", "MyApp")
    }
    populated_strings_xml = _populate_template(strings_xml_template, strings_xml_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "values", "strings.xml"), populated_strings_xml)

    colors_xml_template = _read_template(COLORS_XML_TEMPLATE_PATH)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "values", "colors.xml"), colors_xml_template)

    themes_xml_template = _read_template(THEMES_XML_TEMPLATE_PATH)
    # Dynamically set theme name based on app name if needed, otherwise use default.
    theme_name = f"{config.get('app_name', 'MyApp').replace(' ', '')}Theme"
    themes_xml_replacements = {
        "theme_name": theme_name,
        "primary_color": "#6200EE",
        "primary_dark_color": "#3700B3",
        "secondary_color": "#03DAC5"
    }
    populated_themes_xml = _populate_template(themes_xml_template, themes_xml_replacements)
    _create_file_with_content(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "values", "themes.xml"), populated_themes_xml)

    logging.info("Android project structure setup complete.")


class Lobe1ArabicNLPIntegration:
    """
    Lobe 1: Arabic NLP Integration.
    This lobe bridges the gap between raw Arabic text and structured data.
    It leverages Lobe 2 for parsing and prepares the data for subsequent lobes.
    """

    def __init__(self):
        self.arabic_parser = Lobe2ArabicParser()
        logging.info("Lobe 1 (Arabic NLP Integration) initialized.")

    def process_arabic_prompt_for_apk(self, arabic_prompt: str) -> Dict[str, Any]:
        """
        Processes an Arabic natural language prompt to generate a structured
        configuration suitable for APK generation.

        Args:
            arabic_prompt: The natural language Arabic prompt.

        Returns:
            A dictionary containing the structured configuration.
        """
        logging.info(f"Initiating Lobe 1 processing for prompt: '{arabic_prompt[:50]}...'")

        # Use Lobe 2 to parse the Arabic prompt
        parsed_config = self.arabic_parser.parse_arabic_prompt(arabic_prompt)

        # --- Further integration steps can be added here ---
        # For example, validating extracted data against predefined schemas,
        # enriching data, or performing more complex linguistic analysis.

        if not parsed_config.get("package_name"):
            logging.error("Critical: Package name is missing after parsing. Cannot proceed.")
            raise ValueError("Package name is essential for APK generation.")

        logging.info("Lobe 1 processing complete. Structured configuration generated.")
        return parsed_config

    def run_demo(self):
        """Demonstrates the functionality of Lobe 1."""
        print("\n--- Lobe 1 (Arabic NLP Integration) Demo ---")
        test_prompt = (
            "أريد إنشاء تطبيق أندرويد. اسم التطبيق هو 'تطبيقي العربي'. "
            "اسم الحزمة الخاص بك هو com.example.myarabicapp. "
            "الشاشة الرئيسية تسمى HomePage. "
            "يتطلب صلاحية INTERNET و ACCESS_NETWORK_STATE. "
            "يحتوي على زر مكتوب عليه \"اضغط هنا\" اسمه btn_click_me. "
            "يحتوي على نص يعرض \"أهلاً بالعالم\" اسمه txt_welcome. "
            "رقم الإصدار هو 5. اسم الإصدار هو 1.2."
        )
        print(f"Test Arabic Prompt:\n{test_prompt}\n")

        try:
            structured_config = self.process_arabic_prompt_for_apk(test_prompt)
            print("\n--- Parsed Structured Configuration ---")
            print(json.dumps(structured_config, indent=4, ensure_ascii=False))

            # Simulate setting up the project structure based on the parsed config
            print("\n--- Simulating Project Structure Setup ---")
            setup_android_project_structure(structured_config)
            print("Project structure simulated successfully.")

            print("\n--- Lobe 1 Demo Finished ---")
        except Exception as e:
            logging.error(f"An error occurred during Lobe 1 demo: {e}")
            print(f"An error occurred: {e}")


# Example of how this lobe might be used (can be called by other lobes)
if __name__ == "__main__":
    # This block will not be executed when imported by other modules.
    # It's for direct testing of this lobe.

    lobe1 = Lobe1ArabicNLPIntegration()
    lobe1.run_demo()

    # --- Clean up dummy project created by demo ---
    print("\n--- Cleaning up dummy project ---")
    if os.path.exists(JAVA_PROJECT_DIR):
        try:
            import shutil
            shutil.rmtree(JAVA_PROJECT_DIR)
            logging.info(f"Removed directory: {JAVA_PROJECT_DIR}")
            print(f"Removed dummy project directory: {JAVA_PROJECT_DIR}")
        except OSError as e:
            logging.error(f"Error removing directory {JAVA_PROJECT_DIR}: {e}")
            print(f"Error removing directory {JAVA_PROJECT_DIR}: {e}")
    else:
        print("Dummy project directory not found for cleanup.")