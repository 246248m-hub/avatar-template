import os
import shutil

# Constants for template files
ANDROID_MANIFEST_TEMPLATE = "AndroidManifest.xml.template"
ACTIVITY_TEMPLATE = "Activity.java.template"
LAYOUT_TEMPLATE = "layout.xml.template"
BUILD_GRADLE_TEMPLATE = "build.gradle.template"

# Constants for directories
KNOWLEDGE_BASE_DIR = "knowledge_base"
GENERATED_CODE_DIR = "generated_code"
JAVA_PROJECT_DIR = os.path.join(GENERATED_CODE_DIR, "app", "src", "main", "java", "com", "example", "myapp")
RESOURCES_DIR = os.path.join(GENERATED_CODE_DIR, "app", "src", "main", "res")
LAYOUT_DIR = os.path.join(RESOURCES_DIR, "layout")

def create_dummy_template_files():
    """Creates dummy template files for demonstration."""
    template_content = {
        ANDROID_MANIFEST_TEMPLATE: "<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"com.example.myapp\">\n    <application>\n        <activity android:name=\".MainActivity\">\n            <intent-filter>\n                <action android:name=\"android.intent.action.MAIN\"/>\n                <category android:name=\"android.intent.category.LAUNCHER\"/>\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>",
        ACTIVITY_TEMPLATE: "package com.example.myapp;\n\nimport androidx.appcompat.app.AppCompatActivity;\nimport android.os.Bundle;\n\npublic class MainActivity extends AppCompatActivity {\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n        super.onCreate(savedInstanceState);\n        setContentView(R.layout.activity_main);\n    }\n}",
        LAYOUT_TEMPLATE: "<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\" xmlns:tools=\"http://schemas.android.com/tools\" android:layout_width=\"match_parent\" android:layout_height=\"match_parent\" tools:context=\".MainActivity\">\n    <!-- Layout content will be generated here -->\n</LinearLayout>",
        BUILD_GRADLE_TEMPLATE: "plugins {\n    id 'com.android.application'\n    id 'org.jetbrains.kotlin.android'\n}\n\nandroid {\n    namespace 'com.example.myapp'\n    compileSdk 33\n\n    defaultConfig {\n        applicationId \"com.example.myapp\"\n        minSdk 24\n        targetSdk 33\n        versionCode 1\n        versionName \"1.0\"\n\n        testInstrumentationRunner \"androidx.test.runner.AndroidJUnitRunner\"\n    }\n\n    buildTypes {\n        release {\n            minifyEnabled false\n            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'\n        }\n    }\n    compileOptions {\n        sourceCompatibility JavaVersion.VERSION_1_8\n        targetCompatibility JavaVersion.VERSION_1_8\n    }\n}\n\ndependencies {\n\n    implementation 'androidx.core:core-ktx:1.9.0'\n    implementation 'androidx.appcompat:appcompat:1.6.1'\n    implementation 'com.google.android.material:material:1.10.0'\n    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'\n    testImplementation 'junit:junit:4.13.2'\n    androidTestImplementation 'androidx.test.ext:junit:1.1.5'\n    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'\n}"
    }
    for filename, content in template_content.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created dummy template file: {filename}")

def create_dummy_knowledge_base():
    """Creates a dummy knowledge base directory."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Created dummy knowledge base directory: {KNOWLEDGE_BASE_DIR}")
    # Add some dummy Arabic text files for demonstration
    arabic_texts = {
        "hello_world.txt": "مرحبا بالعالم!",
        "button_label.txt": "زر",
        "text_view_content.txt": "نص عرض"
    }
    for filename, content in arabic_texts.items():
        with open(os.path.join(KNOWLEDGE_BASE_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created dummy Arabic file: {os.path.join(KNOWLEDGE_BASE_DIR, filename)}")


def cleanup_template_files():
    """Cleans up dummy template files."""
    template_files = [
        ANDROID_MANIFEST_TEMPLATE,
        ACTIVITY_TEMPLATE,
        LAYOUT_TEMPLATE,
        BUILD_GRADLE_TEMPLATE,
    ]
    for template_file in template_files:
        if os.path.exists(template_file):
            os.remove(template_file)
            print(f"Removed template file: {template_file}")
    print("--- Template Cleanup Finished ---")

def cleanup_dummy_files():
    """Cleans up dummy generated files and directories."""
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
        print(f"Removed dummy knowledge base directory: {KNOWLEDGE_BASE_DIR}")
    if os.path.exists(GENERATED_CODE_DIR):
        shutil.rmtree(GENERATED_CODE_DIR)
        print(f"Removed dummy generated code directory: {GENERATED_CODE_DIR}")
    print("--- Dummy File Cleanup Finished ---")

def parse_arabic_request(natural_language_request: str, knowledge_base_path: str) -> dict:
    """
    Parses an Arabic natural language request and maps it to structured parameters
    for APK generation. This is a placeholder for a more sophisticated NLP model.

    Args:
        natural_language_request: The Arabic input string.
        knowledge_base_path: Path to the knowledge base for potential lookups.

    Returns:
        A dictionary containing parsed parameters for APK generation.
        Example: {'activity_name': 'MainActivity', 'layout_elements': ['TextView', 'Button'], 'button_text': 'انقر هنا'}
    """
    print(f"Parsing Arabic request: '{natural_language_request}' with knowledge base: {knowledge_base_path}")
    parsed_params = {
        "activity_name": "MainActivity",
        "layout_elements": [],
        "button_text": "Submit",
        "text_view_content": "Welcome!"
    }

    # Basic keyword matching for demonstration
    if "شاشة رئيسية" in natural_language_request or "main screen" in natural_language_request:
        parsed_params["activity_name"] = "MainActivity"
    elif "شاشة تسجيل الدخول" in natural_language_request or "login screen" in natural_language_request:
        parsed_params["activity_name"] = "LoginActivity"

    if "زر" in natural_language_request or "button" in natural_language_request:
        parsed_params["layout_elements"].append("Button")
        # Attempt to extract button text if specified
        if "زر بعنوان" in natural_language_request:
            parts = natural_language_request.split("زر بعنوان")
            if len(parts) > 1:
                button_text_candidate = parts[1].strip().split(".")[0].split("!")[0]
                parsed_params["button_text"] = button_text_candidate
        elif "with text" in natural_language_request:
            parts = natural_language_request.split("with text")
            if len(parts) > 1:
                button_text_candidate = parts[1].strip().split(".")[0].split("!")[0]
                parsed_params["button_text"] = button_text_candidate
        else:
            # Look up default button text from knowledge base if available
            button_file = os.path.join(knowledge_base_path, "button_label.txt")
            if os.path.exists(button_file):
                with open(button_file, "r", encoding="utf-8") as f:
                    parsed_params["button_text"] = f.read().strip()

    if "نص" in natural_language_request or "text view" in natural_language_request:
        parsed_params["layout_elements"].append("TextView")
        if "بعرض النص" in natural_language_request:
            parts = natural_language_request.split("بعرض النص")
            if len(parts) > 1:
                text_content_candidate = parts[1].strip().split(".")[0].split("!")[0]
                parsed_params["text_view_content"] = text_content_candidate
        elif "displaying" in natural_language_request:
            parts = natural_language_request.split("displaying")
            if len(parts) > 1:
                text_content_candidate = parts[1].strip().split(".")[0].split("!")[0]
                parsed_params["text_view_content"] = text_content_candidate
        else:
            # Look up default text content from knowledge base if available
            text_file = os.path.join(knowledge_base_path, "text_view_content.txt")
            if os.path.exists(text_file):
                with open(text_file, "r", encoding="utf-8") as f:
                    parsed_params["text_view_content"] = f.read().strip()

    return parsed_params

def generate_android_project_structure(base_dir: str, package_name: str = "com.example.myapp"):
    """
    Generates the basic directory structure for an Android project.

    Args:
        base_dir: The root directory where the project structure will be created.
        package_name: The package name for the Android application.
    """
    print(f"Generating Android project structure in: {base_dir}")
    os.makedirs(JAVA_PROJECT_DIR, exist_ok=True)
    os.makedirs(LAYOUT_DIR, exist_ok=True)
    print(f"Created directory: {JAVA_PROJECT_DIR}")
    print(f"Created directory: {LAYOUT_DIR}")

def create_android_manifest(package_name: str, activity_name: str, manifest_template_path: str, output_path: str):
    """
    Generates AndroidManifest.xml from a template.

    Args:
        package_name: The package name of the application.
        activity_name: The name of the main activity.
        manifest_template_path: Path to the AndroidManifest.xml template.
        output_path: Path where the generated AndroidManifest.xml will be saved.
    """
    print(f"Generating AndroidManifest.xml from template: {manifest_template_path}")
    with open(manifest_template_path, 'r', encoding='utf-8') as f:
        manifest_content = f.read()

    manifest_content = manifest_content.replace("package=\"com.example.myapp\"", f"package=\"{package_name}\"")
    # This is a simplified replacement for activity. In a real scenario,
    # you'd parse the manifest template more robustly or have placeholders.
    # For now, we assume the template already has a placeholder activity.
    # If we need to dynamically add activities based on parsed params,
    # this logic would need to be more advanced.

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"Generated AndroidManifest.xml at: {output_path}")

def create_activity_file(activity_name: str, activity_template_path: str, output_dir: str, package_name: str):
    """
    Generates an Activity Java file from a template.

    Args:
        activity_name: The name of the activity to create.
        activity_template_path: Path to the Activity template.
        output_dir: The directory to save the generated activity file.
        package_name: The package name of the application.
    """
    print(f"Generating {activity_name}.java from template: {activity_template_path}")
    with open(activity_template_path, 'r', encoding='utf-8') as f:
        activity_content = f.read()

    activity_content = activity_content.replace("package com.example.myapp", f"package {package_name}")
    activity_content = activity_content.replace("public class MainActivity", f"public class {activity_name}")
    activity_content = activity_content.replace("setContentView(R.layout.activity_main)", f"setContentView(R.layout.{activity_name.lower()})") # Assuming layout file matches activity name

    activity_file_path = os.path.join(output_dir, f"{activity_name}.java")
    with open(activity_file_path, 'w', encoding='utf-8') as f:
        f.write(activity_content)
    print(f"Generated {activity_file_path}")

def create_layout_file(layout_name: str, layout_template_path: str, output_dir: str, parsed_params: dict):
    """
    Generates an XML layout file from a template and populates it with elements.

    Args:
        layout_name: The name of the layout file (e.g., 'activity_main').
        layout_template_path: Path to the layout template.
        output_dir: The directory to save the generated layout file.
        parsed_params: Dictionary containing parsed parameters from NLP.
    """
    print(f"Generating layout file '{layout_name}.xml' from template: {layout_template_path}")
    with open(layout_template_path, 'r', encoding='utf-8') as f:
        layout_content = f.read()

    layout_elements_str = ""
    if "layout_elements" in parsed_params:
        for element in parsed_params["layout_elements"]:
            if element == "Button":
                button_text = parsed_params.get("button_text", "Default Button")
                layout_elements_str += f'    <Button\n        android:id="@+id/button"\n        android:layout_width="wrap_content"\n        android:layout_height="wrap_content"\n        android:text="{button_text}" />\n'
            elif element == "TextView":
                text_content = parsed_params.get("text_view_content", "Default Text")
                layout_elements_str += f'    <TextView\n        android:id="@+id/textView"\n        android:layout_width="wrap_content"\n        android:layout_height="wrap_content"\n        android:text="{text_content}" />\n'

    # Replace a placeholder comment or find a suitable spot to insert elements
    # For simplicity, we'll replace a specific comment. A more robust parser would be needed.
    layout_content = layout_content.replace("<!-- Layout content will be generated here -->", layout_elements_str)

    layout_file_path = os.path.join(output_dir, f"{layout_name}.xml")
    with open(layout_file_path, 'w', encoding='utf-8') as f:
        f.write(layout_content)
    print(f"Generated layout file at: {layout_file_path}")

def create_build_gradle_file(build_gradle_template_path: str, output_path: str, package_name: str):
    """
    Generates the build.gradle file from a template.

    Args:
        build_gradle_template_path: Path to the build.gradle template.
        output_path: Path where the generated build.gradle will be saved.
        package_name: The package name of the application.
    """
    print(f"Generating build.gradle from template: {build_gradle_template_path}")
    with open(build_gradle_template_path, 'r', encoding='utf-8') as f:
        gradle_content = f.read()

    gradle_content = gradle_content.replace("namespace 'com.example.myapp'", f"namespace '{package_name}'")
    gradle_content = gradle_content.replace("applicationId \"com.example.myapp\"", f"applicationId \"{package_name}\"")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(gradle_content)
    print(f"Generated build.gradle at: {output_path}")

# --- Demo Execution ---

if __name__ == "__main__":
    print("--- Initializing Arabic Parser and Generator Module ---")

    # Create dummy files and directories for demonstration
    create_dummy_template_files()
    create_dummy_knowledge_base()

    # --- Lobe 0_language_lobe simulation ---
    # This simulates Lobe 0 getting input and processing it
    test_prompt_1 = "أنشئ لي شاشة رئيسية مع زر."
    test_prompt_2 = "اريد شاشة تحتوي على نص ترحيبي وزر تسجيل الدخول."
    test_prompt_3 = "Build a login screen with a button labeled 'الدخول'."
    test_prompt_4 = "Create a simple screen displaying 'مرحبا بكم في التطبيق'."
    test_prompt_5 = "Generate a main activity with a button." # Testing English mixed with Arabic context

    # Example 1: Basic Arabic request
    print("\n--- Demo Case 1: Basic Arabic Request ---")
    parsed_data_1 = parse_arabic_request(test_prompt_1, KNOWLEDGE_BASE_DIR)
    print(f"Parsed data for prompt 1: {parsed_data_1}")

    # Example 2: More specific Arabic request
    print("\n--- Demo Case 2: Specific Arabic Request ---")
    parsed_data_2 = parse_arabic_request(test_prompt_2, KNOWLEDGE_BASE_DIR)
    print(f"Parsed data for prompt 2: {parsed_data_2}")

    # Example 3: English request with Arabic context (simulated by keyword presence)
    print("\n--- Demo Case 3: English Request with Arabic Context ---")
    parsed_data_3 = parse_arabic_request(test_prompt_3, KNOWLEDGE_BASE_DIR)
    print(f"Parsed data for prompt 3: {parsed_data_3}")

    # Example 4: Request for TextView content
    print("\n--- Demo Case 4: TextView Content Request ---")
    parsed_data_4 = parse_arabic_request(test_prompt_4, KNOWLEDGE_BASE_DIR)
    print(f"Parsed data for prompt 4: {parsed_data_4}")

    # Example 5: Mixed language request
    print("\n--- Demo Case 5: Mixed Language Request ---")
    parsed_data_5 = parse_arabic_request(test_prompt_5, KNOWLEDGE_BASE_DIR)
    print(f"Parsed data for prompt 5: {parsed_data_5}")

    # --- Lobe 6_synthesis_lobe simulation ---
    # This demonstrates how synthesis lobe might use the parsed data to
    # generate project structure and files.

    print("\n--- Simulating Synthesis for Parsed Data 1 ---")
    # Ensure clean state for generation
    if os.path.exists(GENERATED_CODE_DIR):
        shutil.rmtree(GENERATED_CODE_DIR)
    os.makedirs(GENERATED_CODE_DIR, exist_ok=True)

    package_name_1 = "com.example.myapp.generated1"
    activity_name_1 = parsed_data_1.get("activity_name", "MainActivity")
    layout_name_1 = activity_name_1.lower()

    generate_android_project_structure(GENERATED_CODE_DIR, package_name_1)
    create_android_manifest(package_name_1, activity_name_1, ANDROID_MANIFEST_TEMPLATE, os.path.join(GENERATED_CODE_DIR, "AndroidManifest.xml"))
    create_activity_file(activity_name_1, ACTIVITY_TEMPLATE, JAVA_PROJECT_DIR, package_name_1)
    create_layout_file(layout_name_1, LAYOUT_TEMPLATE, LAYOUT_DIR, parsed_data_1)
    create_build_gradle_file(BUILD_GRADLE_TEMPLATE, os.path.join(GENERATED_CODE_DIR, "build.gradle"), package_name_1)

    print("\n--- Simulating Synthesis for Parsed Data 3 (English with Arabic label) ---")
    if os.path.exists(GENERATED_CODE_DIR):
        shutil.rmtree(GENERATED_CODE_DIR)
    os.makedirs(GENERATED_CODE_DIR, exist_ok=True)

    package_name_3 = "com.example.myapp.generated3"
    activity_name_3 = parsed_data_3.get("activity_name", "LoginActivity") # Based on prompt parsing
    layout_name_3 = activity_name_3.lower()

    generate_android_project_structure(GENERATED_CODE_DIR, package_name_3)
    create_android_manifest(package_name_3, activity_name_3, ANDROID_MANIFEST_TEMPLATE, os.path.join(GENERATED_CODE_DIR, "AndroidManifest.xml"))
    create_activity_file(activity_name_3, ACTIVITY_TEMPLATE, JAVA_PROJECT_DIR, package_name_3)
    create_layout_file(layout_name_3, LAYOUT_TEMPLATE, LAYOUT_DIR, parsed_data_3)
    create_build_gradle_file(BUILD_GRADLE_TEMPLATE, os.path.join(GENERATED_CODE_DIR, "build.gradle"), package_name_3)


    # Clean up dummy files
    print("\n--- Cleaning up dummy files ---")
    cleanup_template_files()
    cleanup_dummy_files()

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")