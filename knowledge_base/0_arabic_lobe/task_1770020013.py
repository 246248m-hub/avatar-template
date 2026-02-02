import os
import subprocess
import xml.etree.ElementTree as ET

def parse_arabic_manifest(manifest_path):
    """
    Parses an AndroidManifest.xml file to extract relevant Arabic language information.

    Args:
        manifest_path (str): The path to the AndroidManifest.xml file.

    Returns:
        dict: A dictionary containing extracted Arabic language configurations,
              or None if parsing fails.
    """
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        application_tag = root.find('application')

        if application_tag is None:
            print(f"Error: '<application>' tag not found in {manifest_path}")
            return None

        arabic_config = {}

        # Extract default locale if specified
        locale_tag = application_tag.find(".//meta-data[@android:name='default-locale']")
        if locale_tag is not None:
            arabic_config['default_locale'] = locale_tag.get('{http://schemas.android.com/apk/res/android}value')

        # Extract supported locales if specified
        supported_locales_tag = application_tag.find(".//meta-data[@android:name='supported-locales']")
        if supported_locales_tag is not None:
            arabic_config['supported_locales'] = supported_locales_tag.get('{http://schemas.android.com/apk/res/android}value').split(',')

        # Check for any explicit Arabic language support declarations (e.g., in activities)
        # This is a basic example; more complex parsing might be needed for specific frameworks
        activities = application_tag.findall('activity')
        for activity in activities:
            if 'android:name' in activity.attrib:
                activity_name = activity.attrib['android:name']
                # Example: Look for specific intent filters related to Arabic
                intent_filters = activity.findall('intent-filter')
                for intent_filter in intent_filters:
                    actions = intent_filter.findall('action')
                    categories = intent_filter.findall('category')
                    for action in actions:
                        if action.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.action.VIEW':
                            for category in categories:
                                if category.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.category.DEFAULT':
                                    if 'android.intent.category.BROWSABLE' not in [c.get('{http://schemas.android.com/apk/res/android}name') for c in categories]:
                                        # This is a simplified heuristic. A real-world scenario
                                        # would involve deeper analysis of intent data schemes.
                                        if any('arabic' in attr_val.lower() for attr_val in [a.get('{http://schemas.android.com/apk/res/android}name') for a in intent_filter.findall('*')] if attr_val):
                                            arabic_config.setdefault('activity_arabic_focus', []).append(activity_name)
                                            break # Found relevant intent for this activity

        return arabic_config

    except ET.ParseError as e:
        print(f"Error parsing AndroidManifest.xml: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: AndroidManifest.xml not found at {manifest_path}")
        return None

def generate_arabic_resources(locale_code="ar"):
    """
    Generates placeholder Arabic resource files (strings.xml) for a given locale.

    Args:
        locale_code (str): The locale code for which to generate resources (e.g., "ar").

    Returns:
        tuple: A tuple containing the path to the generated strings.xml file and
               a dictionary of the generated string content, or (None, None) if failed.
    """
    resource_dir = f"res/values-{locale_code}"
    os.makedirs(resource_dir, exist_ok=True)
    strings_xml_path = os.path.join(resource_dir, "strings.xml")

    # Basic Arabic strings for demonstration
    arabic_strings = {
        "app_name": "تطبيق عربي",
        "hello_world": "مرحبا بالعالم",
        "next_button": "التالي",
        "previous_button": "السابق"
    }

    try:
        with open(strings_xml_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<resources xmlns:tools="http://schemas.android.com/tools">\n')
            for key, value in arabic_strings.items():
                f.write(f'    <string name="{key}">{value}</string>\n')
            f.write('</resources>\n')
        print(f"Generated Arabic strings.xml at: {strings_xml_path}")
        return strings_xml_path, arabic_strings
    except IOError as e:
        print(f"Error writing Arabic strings.xml: {e}")
        return None, None

def integrate_arabic_language_support(project_root_dir, arabic_config):
    """
    Integrates Arabic language support into an Android project by modifying
    the AndroidManifest.xml and adding Arabic resource files.

    Args:
        project_root_dir (str): The root directory of the Android project.
        arabic_config (dict): Configuration dictionary obtained from parse_arabic_manifest.
    """
    manifest_path = os.path.join(project_root_dir, "app", "src", "main", "AndroidManifest.xml")

    if not os.path.exists(manifest_path):
        print(f"Error: AndroidManifest.xml not found at {manifest_path}")
        return

    # Ensure Arabic resources directory exists
    if arabic_config.get('supported_locales') and "ar" in arabic_config['supported_locales']:
        generate_arabic_resources("ar")
    elif arabic_config.get('default_locale') == "ar":
        generate_arabic_resources("ar")
    else:
        # If no explicit Arabic locale, still generate if it seems implied by manifest
        # (This is a heuristic and can be refined)
        if any("arabic" in str(v).lower() for v in arabic_config.values() if isinstance(v, str)):
             generate_arabic_resources("ar")


    # Modify AndroidManifest.xml if needed (e.g., setting default locale)
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        application_tag = root.find('application')

        if application_tag is None:
            print(f"Error: '<application>' tag not found in {manifest_path} for modification.")
            return

        # Set default locale if specified and not already present
        if arabic_config.get('default_locale') == "ar":
            default_locale_tag = application_tag.find(".//meta-data[@android:name='default-locale']")
            if default_locale_tag is None:
                new_meta_data = ET.SubElement(application_tag, 'meta-data')
                new_meta_data.set('android:name', 'default-locale')
                new_meta_data.set('android:value', 'ar')
                print("Added 'default-locale' meta-data for Arabic.")
            else:
                current_value = default_locale_tag.get('{http://schemas.android.com/apk/res/android}value')
                if current_value != 'ar':
                    default_locale_tag.set('{http://schemas.android.com/apk/res/android}value', 'ar')
                    print("Updated 'default-locale' meta-data to Arabic.")

        # Add supported locales if specified and not already present
        if arabic_config.get('supported_locales') and "ar" in arabic_config['supported_locales']:
            supported_locales_tag = application_tag.find(".//meta-data[@android:name='supported-locales']")
            if supported_locales_tag is None:
                new_meta_data = ET.SubElement(application_tag, 'meta-data')
                new_meta_data.set('android:name', 'supported-locales')
                new_meta_data.set('android:value', ','.join(arabic_config['supported_locales']))
                print("Added 'supported-locales' meta-data.")
            else:
                current_value = supported_locales_tag.get('{http://schemas.android.com/apk/res/android}value')
                if 'ar' not in current_value.split(','):
                    supported_locales_tag.set('{http://schemas.android.com/apk/res/android}value', f"{current_value},ar")
                    print("Added Arabic to 'supported-locales' meta-data.")

        # Write the modified manifest back
        tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
        print(f"Successfully updated AndroidManifest.xml at: {manifest_path}")

    except ET.ParseError as e:
        print(f"Error parsing AndroidManifest.xml for modification: {e}")
    except FileNotFoundError:
        print(f"Error: AndroidManifest.xml not found at {manifest_path} during modification.")
    except Exception as e:
        print(f"An unexpected error occurred during manifest modification: {e}")


def demo_arabic_nlp_and_apk_generation():
    """
    Demonstrates the integration of Arabic NLP and APK generation logic.
    This function acts as a placeholder and orchestrator for the language lobe's functionality.
    """
    print("\n--- Starting Arabic NLP and APK Generation Demo ---")

    # 1. Simulate NLP processing to identify Arabic language needs.
    # In a real scenario, this would involve analyzing natural language prompts.
    # For this demo, we'll use a simulated prompt and its hypothetical interpretation.
    simulated_nl_prompt = "Build an Android app that displays 'Hello World' in Arabic and has a button to proceed."
    print(f"Simulated Natural Language Prompt: '{simulated_nl_prompt}'")

    # Hypothetical NLP analysis results:
    # This is where Lobe 0_language_lobe would provide structured data.
    # For this demo, we hardcode a plausible output that indicates Arabic requirements.
    nlp_analysis_output = {
        "language": "arabic",
        "ui_elements": {
            "text": ["مرحبا بالعالم", "التالي"],
            "layout_direction": "rtl" # Right-to-left for Arabic
        },
        "features": ["internationalization"]
    }
    print(f"Simulated NLP Analysis Output: {nlp_analysis_output}")

    # 2. Based on NLP analysis, configure project structure and manifest.
    # This step would typically involve Lobe 4_code_generation_lobe and Lobe 6_synthesis_lobe.
    # We'll simulate the creation of a dummy project structure.
    dummy_project_root = "dummy_arabic_app"
    os.makedirs(os.path.join(dummy_project_root, "app", "src", "main", "res", "values"), exist_ok=True)
    os.makedirs(os.path.join(dummy_project_root, "app", "src", "main", "java", "com", "example", "arabicapp"), exist_ok=True)

    # Create a dummy AndroidManifest.xml
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.arabicapp">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_path = os.path.join(dummy_project_root, "app", "src", "main", "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Simulate parsing the initial manifest to see what's there.
    print("\n--- Parsing initial AndroidManifest.xml ---")
    initial_arabic_config = parse_arabic_manifest(manifest_path)
    print(f"Initial Arabic Configuration: {initial_arabic_config}")

    # 3. Integrate Arabic language support based on NLP output.
    # This involves modifying the manifest and creating resource files.
    print("\n--- Integrating Arabic Language Support ---")
    # Simulate a more refined arabic_config based on NLP analysis
    integrated_arabic_config = {
        'default_locale': 'ar',
        'supported_locales': ['en', 'ar'],
        'activity_arabic_focus': ['.MainActivity'] # Indicates MainActivity is relevant for Arabic
    }
    integrate_arabic_language_support(dummy_project_root, integrated_arabic_config)

    # 4. Simulate APK compilation.
    # This is where Lobe 8_apk_compiler_lobe would take over.
    # We'll call a placeholder function that represents this step.
    print("\n--- Simulating APK Compilation ---")
    generated_apk_path = simulate_apk_compilation(dummy_project_root)

    if generated_apk_path:
        print(f"\nAPK successfully generated (simulated) at: {generated_apk_path}")
    else:
        print("\nAPK generation process failed (simulated).")

    # Clean up the dummy project created for this demo run
    print("\n--- Cleaning up dummy project ---")
    cleanup_android_project_template(dummy_project_root)
    print("\n--- Arabic NLP and APK Generation Demo Finished ---")


def simulate_apk_compilation(project_root_dir):
    """
    Simulates the process of compiling an Android project into an APK.
    In a real scenario, this would call the Android build tools (e.g., Gradle).

    Args:
        project_root_dir (str): The root directory of the Android project.

    Returns:
        str: The path to the simulated APK file, or None if simulation fails.
    """
    print(f"Attempting to simulate APK compilation for: {project_root_dir}")

    # In a real scenario, you'd execute Gradle commands:
    # try:
    #     subprocess.run(["./gradlew", "assembleDebug"], cwd=project_root_dir, check=True)
    #     # Find the generated APK file
    #     apk_path = os.path.join(project_root_dir, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
    #     if os.path.exists(apk_path):
    #         return apk_path
    #     else:
    #         print("Error: Could not find generated APK after build.")
    #         return None
    # except subprocess.CalledProcessError as e:
    #     print(f"Error during Gradle build: {e}")
    #     return None
    # except FileNotFoundError:
    #     print("Error: gradlew command not found. Ensure you are in a valid Android project directory.")
    #     return None

    # For simulation, we'll just create a dummy file and print success.
    simulated_apk_dir = os.path.join(project_root_dir, "app", "build", "outputs", "apk", "debug")
    os.makedirs(simulated_apk_dir, exist_ok=True)
    simulated_apk_path = os.path.join(simulated_apk_dir, "app-debug-simulated.apk")
    try:
        with open(simulated_apk_path, "w") as f:
            f.write("This is a simulated APK file.")
        print("Simulated APK compilation successful. Created dummy APK file.")
        return simulated_apk_path
    except IOError as e:
        print(f"Error creating simulated APK file: {e}")
        return None


def cleanup_android_project_template(project_root_dir):
    """
    Removes a dummy Android project directory.

    Args:
        project_root_dir (str): The root directory of the dummy project to remove.
    """
    import shutil
    if os.path.exists(project_root_dir):
        try:
            shutil.rmtree(project_root_dir)
            print(f"Removed directory: {project_root_dir}")
        except OSError as e:
            print(f"Error removing directory {project_root_dir}: {e}")
    else:
        print(f"Directory {project_root_dir} not found for cleanup.")


# Example of how Lobe 0_language_lobe might call this functionality:
# (This part is for demonstration and would be integrated into the main execution flow)
if __name__ == '__main__':
    # Mocking environment variables for demonstration if not set
    if not os.environ.get("ANDROID_SDK_ROOT"):
        print("ANDROID_SDK_ROOT not set. Using a dummy path for demonstration.")
        os.environ["ANDROID_SDK_ROOT"] = "/dummy/android/sdk" # Replace with your actual SDK path if needed

    # This function call is part of the "demo_arabic_nlp_and_apk_generation"
    # which is designed to be triggered by higher-level lobes.
    # For direct execution of this script, you might call it like this:
    demo_arabic_nlp_and_apk_generation()

    # You can also test individual functions:
    # print("\n--- Testing individual functions ---")
    # dummy_manifest_path = "temp_manifest_test/AndroidManifest.xml"
    # os.makedirs("temp_manifest_test", exist_ok=True)
    # with open(dummy_manifest_path, "w") as f:
    #     f.write("""<?xml version="1.0" encoding="utf-8"?>
    # <manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.test">
    #     <application android:label="@string/app_name">
    #         <meta-data android:name="default-locale" android:value="en"/>
    #         <meta-data android:name="supported-locales" android:value="en,fr"/>
    #         <activity android:name=".MainActivity"/>
    #     </application>
    # </manifest>""")
    #
    # parsed_config = parse_arabic_manifest(dummy_manifest_path)
    # print(f"Parsed config from dummy manifest: {parsed_config}")
    #
    # integrate_arabic_language_support("temp_manifest_test", {'default_locale': 'ar', 'supported_locales': ['en', 'ar']})
    #
    # print("\n--- Cleaning up temp manifest test ---")
    # cleanup_android_project_template("temp_manifest_test")