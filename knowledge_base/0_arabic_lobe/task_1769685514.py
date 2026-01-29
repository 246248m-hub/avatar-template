import os
import re
import subprocess
import shutil
from pathlib import Path

# Assume these are defined elsewhere and accessible
# KNOWLEDGE_BASE_DIR = Path("path/to/your/knowledge_base")
# DEMO_PROJECT_BASE_DIR = Path("path/to/your/demo_projects")

def extract_android_components(natural_language_description: str) -> dict:
    """
    Extracts Android components (Activities, Services, BroadcastReceivers, ContentProviders)
    and their basic configurations from a natural language description.

    Args:
        natural_language_description: A string describing the desired Android application components.

    Returns:
        A dictionary where keys are component types (e.g., 'activities', 'services')
        and values are lists of dictionaries, each representing a component with its name
        and potential attributes.
    """
    components = {
        "activities": [],
        "services": [],
        "broadcast_receivers": [],
        "content_providers": []
    }

    # Simple keyword-based extraction for demonstration.
    # A more robust solution would involve advanced NLP techniques.

    # Activities
    activity_matches = re.findall(r"create an activity named ([\w_]+)", natural_language_description, re.IGNORECASE)
    for match in activity_matches:
        components["activities"].append({"name": match})

    # Services
    service_matches = re.findall(r"implement a service called ([\w_]+)", natural_language_description, re.IGNORECASE)
    for match in service_matches:
        components["services"].append({"name": match})

    # Broadcast Receivers
    receiver_matches = re.findall(r"set up a broadcast receiver for ([\w_]+)", natural_language_description, re.IGNORECASE)
    for match in receiver_matches:
        components["broadcast_receivers"].append({"name": match, "action": match}) # Simplified to use the matched word as action

    # Content Providers (more complex, requiring data schema)
    # For simplicity, we'll just look for a mention and assign a placeholder name
    if "add a content provider" in natural_language_description.lower():
        components["content_providers"].append({"name": "MyContentProvider", "authority": "com.example.provider"}) # Placeholder

    return components

def generate_android_manifest_xml(package_name: str, components: dict) -> str:
    """
    Generates a basic AndroidManifest.xml content based on extracted components.

    Args:
        package_name: The package name of the Android application.
        components: A dictionary of Android components.

    Returns:
        A string representing the content of AndroidManifest.xml.
    """
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
"""

    # Add activities
    for activity in components.get("activities", []):
        manifest_content += f"""
        <activity android:name=".{activity['name']}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""

    # Add services
    for service in components.get("services", []):
        manifest_content += f"""
        <service android:name=".{service['name']}" />
"""

    # Add broadcast receivers
    for receiver in components.get("broadcast_receivers", []):
        manifest_content += f"""
        <receiver android:name=".{receiver['name']}">
            <intent-filter>
                <action android:name="{receiver.get('action', '')}" />
            </intent-filter>
        </receiver>
"""

    # Add content providers
    for provider in components.get("content_providers", []):
        manifest_content += f"""
        <provider android:name=".{provider['name']}"
            android:authorities="{provider.get('authority', '')}"
            android:exported="false" />
"""

    manifest_content += """
    </application>
</manifest>
"""
    return manifest_content

def create_android_project_structure(project_path: Path, package_name: str, components: dict) -> None:
    """
    Creates the basic directory structure for an Android project and places
    a rudimentary AndroidManifest.xml.

    Args:
        project_path: The root directory for the new Android project.
        package_name: The package name for the application.
        components: A dictionary of Android components.
    """
    app_dir = project_path / "app"
    manifest_dir = app_dir / "src" / "main"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    manifest_content = generate_android_manifest_xml(package_name, components)
    with open(manifest_dir / "AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Create placeholder Java/Kotlin directories
    java_dir = manifest_dir / "java"
    package_dir_parts = package_name.split('.')
    current_java_dir = java_dir
    for part in package_dir_parts:
        current_java_dir = current_java_dir / part
    current_java_dir.mkdir(parents=True, exist_ok=True)

    # Create dummy component files (optional but good for structure)
    for comp_type, comp_list in components.items():
        for comp in comp_list:
            comp_name = comp['name']
            dummy_file_path = current_java_dir / f"{comp_name}.java" # Assuming Java for simplicity
            with open(dummy_file_path, "w", encoding="utf-8") as f:
                f.write(f"package {package_name};\n\n")
                if comp_type == "activities":
                    f.write("import androidx.appcompat.app.AppCompatActivity;\n\n")
                    f.write(f"public class {comp_name} extends AppCompatActivity {{\n    // TODO: Implement activity logic\n}}\n")
                elif comp_type == "services":
                    f.write("import android.app.Service;\nimport android.content.Intent;\nimport android.os.IBinder;\n\n")
                    f.write(f"public class {comp_name} extends Service {{\n    @Override\n    public IBinder onBind(Intent intent) {{ return null; }}\n    // TODO: Implement service logic\n}}\n")
                elif comp_type == "broadcast_receivers":
                    f.write("import android.content.BroadcastReceiver;\nimport android.content.Context;\nimport android.content.Intent;\n\n")
                    f.write(f"public class {comp_name} extends BroadcastReceiver {{\n    @Override\n    public void onReceive(Context context, Intent intent) {{ // TODO: Implement receiver logic }}\n}}\n")
                elif comp_type == "content_providers":
                    f.write("import android.content.ContentProvider;\nimport android.content.ContentValues;\nimport android.database.Cursor;\nimport android.net.Uri;\n\n")
                    f.write(f"public class {comp_name} extends ContentProvider {{\n    // TODO: Implement content provider logic\n    @Override\n    public boolean onCreate() {{ return false; }}\n    @Override\n    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {{ return null; }}\n    @Override\n    public String getType(Uri uri) {{ return null; }}\n    @Override\n    public Uri insert(Uri uri, ContentValues values) {{ return null; }}\n    @Override\n    public int delete(Uri uri, String selection, String[] selectionArgs) {{ return 0; }}\n    @Override\n    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {{ return 0; }}\n}}\n")


class Lobe3ArabicNLPIntegrationModule:
    """
    Lobe 3 focuses on integrating Arabic NLP capabilities to understand
    and generate structured data for Android application components from
    natural language descriptions, specifically in Arabic.
    """

    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        # In a real scenario, this would load Arabic NLP models, dictionaries, etc.
        print(f"Initializing Lobe 3: Arabic NLP Integration Module with KB: {self.knowledge_base_dir}")

    def process_arabic_description(self, arabic_description: str, package_name: str) -> dict:
        """
        Processes an Arabic natural language description to extract Android
        component information.

        Args:
            arabic_description: The Arabic text describing desired components.
            package_name: The target package name for the Android application.

        Returns:
            A dictionary containing extracted Android components.
        """
        print(f"\n--- Lobe 3: Processing Arabic description ---")
        print(f"Arabic Input: \"{arabic_description}\"")
        print(f"Target Package: {package_name}")

        # Placeholder for Arabic NLP processing.
        # This is where actual Arabic tokenization, intent recognition,
        # entity extraction (component names, properties) would happen.
        # For this example, we'll use English keyword extraction as a proxy
        # but imagine this logic is adapted for Arabic.

        # A simplified approach assuming some Arabic words map to English concepts.
        # In reality, you'd use an Arabic NLP library.
        english_proxy_description = arabic_description.replace("نشاط", "activity").replace("خدمة", "service").replace("مستقبل بث", "broadcast receiver").replace("مزود محتوى", "content provider")
        # This is a very crude mapping. Proper Arabic NLP is needed.

        extracted_components = extract_android_components(english_proxy_description)

        print(f"Extracted Components (Arabic Processing Proxy): {extracted_components}")
        return extracted_components

    def demonstrate(self, temp_project_root: Path):
        """
        Demonstrates the functionality of the Arabic NLP Integration Module.
        """
        print("\n--- Lobe 3: Arabic NLP Integration Module Demo ---")
        arabic_prompt = "أريد إنشاء نشاط يسمى MainActivity وأن أضيف خدمة اسمها MyBackgroundService."
        package_name = "com.example.arabicapp"

        # 1. Process Arabic description to extract components
        components_data = self.process_arabic_description(arabic_prompt, package_name)

        # 2. Create basic Android project structure with manifest
        print("\n--- Lobe 3: Creating Android project structure ---")
        create_android_project_structure(temp_project_root, package_name, components_data)
        print(f"Created basic project structure at: {temp_project_root}")
        manifest_path = temp_project_root / "app" / "src" / "main" / "AndroidManifest.xml"
        if manifest_path.exists():
            print(f"AndroidManifest.xml generated at: {manifest_path}")
            with open(manifest_path, 'r', encoding='utf-8') as f:
                print("--- AndroidManifest.xml Content ---")
                print(f.read())
                print("-------------------------------------")
        else:
            print("Error: AndroidManifest.xml was not generated.")

        print("\n--- Lobe 3: Arabic NLP Integration Module Demo Finished ---")
        return components_data # Return for potential chaining


# Example of how Lobe 3 might be used or integrated (for testing purposes)
if __name__ == "__main__":
    # Setup for demonstration
    DEMO_ROOT = Path("./demo_lobe_3")
    DEMO_ROOT.mkdir(exist_ok=True)
    DUMMY_KB_DIR = DEMO_ROOT / "knowledge_base"
    DUMMY_KB_DIR.mkdir(exist_ok=True)
    DUMMY_PROJECT_ROOT = DEMO_ROOT / "dummy_android_project"

    # Clean up previous runs
    if DUMMY_PROJECT_ROOT.exists():
        shutil.rmtree(DUMMY_PROJECT_ROOT)
    DUMMY_PROJECT_ROOT.mkdir()

    lobe3 = Lobe3ArabicNLPIntegrationModule(knowledge_base_dir=DUMMY_KB_DIR)
    extracted_info = lobe3.demonstrate(temp_project_root=DUMMY_PROJECT_ROOT)

    # Clean up dummy project
    print("\n--- Cleaning up dummy project ---")
    if DUMMY_PROJECT_ROOT.exists():
        print(f"Removing dummy project directory: {DUMMY_PROJECT_ROOT}")
        shutil.rmtree(DUMMY_PROJECT_ROOT)

    print("\n--- Lobe 3: Arabic NLP Integration Module Demo Finished ---")