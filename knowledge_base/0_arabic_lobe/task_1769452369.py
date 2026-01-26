import os
import re
import subprocess
import json
import shutil

# Define constants for project structure
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set. Please set it to your Android SDK path.")

BUILD_TOOLS_DIR = os.path.join(ANDROID_SDK_ROOT, "build-tools")
# Find the latest build tools version
BUILD_TOOLS_VERSION = sorted(os.listdir(BUILD_TOOLS_DIR))[-1]
AAPT_PATH = os.path.join(BUILD_TOOLS_DIR, BUILD_TOOLS_VERSION, "aapt")
APKSIGNER_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", BUILD_TOOLS_VERSION, "apksigner")
ZIPALIGN_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", BUILD_TOOLS_VERSION, "zipalign")

JAVA_PROJECT_DIR = "temp_android_project"
MANIFEST_FILE = "AndroidManifest.xml"
RESOURCES_DIR = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res")
DRAWABLE_DIR = os.path.join(RESOURCES_DIR, "drawable")
LAYOUT_DIR = os.path.join(RESOURCES_DIR, "layout")
VALUES_DIR = os.path.join(RESOURCES_DIR, "values")
SOURCES_DIR = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", "com", "example", "myapp")
CLASSES_DIR = os.path.join(JAVA_PROJECT_DIR, "app", "build", "intermediates", "javac", "debug", "classes")
APK_DIR = "apks"

# Mock LLM output for Arabic text generation (Lobe 0)
def mock_arabic_text_generation(prompt: str) -> str:
    """
    Mocks the output of an Arabic text generation lobe.
    In a real scenario, this would involve calling Lobe 0.
    """
    if "greeting" in prompt:
        return "مرحبا بك في التطبيق!"
    elif "button_text" in prompt:
        return "اضغط هنا"
    elif "app_name" in prompt:
        return "تطبيقي المميز"
    elif "version_name" in prompt:
        return "1.0"
    elif "version_code" in prompt:
        return "1"
    elif "package_name" in prompt:
        return "com.example.myapp"
    elif "main_activity_class" in prompt:
        return "MainActivity"
    elif "layout_file" in prompt:
        return "activity_main.xml"
    elif "icon_resource" in prompt:
        return "@drawable/ic_launcher"
    elif "theme_name" in prompt:
        return "@style/AppTheme"
    else:
        return "نص افتراضي"

# Mock LLM output for Java code generation (Lobe 4)
def mock_java_code_generation(class_name: str, intent_data: str) -> str:
    """
    Mocks the output of a Java code generation lobe.
    In a real scenario, this would involve calling Lobe 4.
    """
    return f"""package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {class_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Example of using intent data
        // String receivedData = getIntent().getStringExtra("some_key");
        // TextView myTextView = findViewById(R.id.my_text_view);
        // if (receivedData != null) {{
        //     myTextView.setText(receivedData);
        // }}
    }}
}}
"""

# Mock LLM output for XML layout generation (Lobe 4)
def mock_layout_xml_generation(layout_name: str) -> str:
    """
    Mocks the output of an XML layout generation lobe.
    In a real scenario, this would involve calling Lobe 4.
    """
    return f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.capitalize()}Activity">

    <TextView
        android:id="@+id/main_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

# Mock LLM output for strings.xml generation (Lobe 4)
def mock_strings_xml_generation(app_name: str, greeting: str) -> str:
    """
    Mocks the output of a strings.xml generation lobe.
    In a real scenario, this would involve calling Lobe 4.
    """
    return f"""<resources>
    <string name="app_name">{app_name}</string>
    <string name="greeting">{greeting}</string>
</resources>
"""

# Mock LLM output for AndroidManifest.xml generation (Lobe 4)
def mock_manifest_xml_generation(package_name: str, app_name: str, main_activity_class: str, icon_resource: str, theme_name: str) -> str:
    """
    Mocks the output of an AndroidManifest.xml generation lobe.
    In a real scenario, this would involve calling Lobe 4.
    """
    return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="{icon_resource}"
        android:label="@string/app_name"
        android:roundIcon="{icon_resource}"
        android:supportsRtl="true"
        android:theme="{theme_name}">
        <activity android:name=".{main_activity_class}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

# Mock LLM output for Arabic Icon generation (Lobe 0)
def mock_arabic_icon_generation(app_name: str) -> str:
    """
    Mocks the output of an Arabic icon generation lobe.
    In a real scenario, this would involve calling Lobe 0.
    This would typically return a file path to a generated icon.
    For this demo, we'll just create a dummy file.
    """
    icon_filename = "ic_launcher.png"
    icon_path = os.path.join(DRAWABLE_DIR, icon_filename)
    os.makedirs(DRAWABLE_DIR, exist_ok=True)
    with open(icon_path, "w") as f:
        f.write(f"Dummy icon for {app_name}")
    return icon_path


class ArabicAPKCompiler:
    def __init__(self):
        self.extracted_info = {}
        self.generated_files = []

    def _run_command(self, command, cwd=None, capture_output=True, text=True):
        """Helper to run shell commands."""
        try:
            result = subprocess.run(command, cwd=cwd, capture_output=capture_output, text=text, check=True)
            if capture_output:
                return result.stdout.strip()
            return ""
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {' '.join(command)}")
            print(f"Stderr: {e.stderr}")
            raise

    def _create_dummy_files_and_dirs(self):
        """Creates necessary directories for the APK compilation."""
        print("--- Creating dummy files and directories ---")
        os.makedirs(JAVA_PROJECT_DIR, exist_ok=True)
        os.makedirs(os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "java", "com", "example", "myapp"), exist_ok=True)
        os.makedirs(RESOURCES_DIR, exist_ok=True)
        os.makedirs(DRAWABLE_DIR, exist_ok=True)
        os.makedirs(LAYOUT_DIR, exist_ok=True)
        os.makedirs(VALUES_DIR, exist_ok=True)
        os.makedirs(APK_DIR, exist_ok=True)
        print("Dummy files and directories created.")

    def _cleanup_dummy_files(self):
        """Cleans up dummy files and directories."""
        print("\n--- Cleaning up dummy files and directories ---")
        if os.path.exists(JAVA_PROJECT_DIR):
            shutil.rmtree(JAVA_PROJECT_DIR)
            print(f"Removed generated project directory: {JAVA_PROJECT_DIR}")
        if os.path.exists(APK_DIR):
            shutil.rmtree(APK_DIR)
            print(f"Removed APK output directory: {APK_DIR}")
        print("Cleanup complete.")

    def _extract_info_from_arabic_prompt(self, prompt: str) -> dict:
        """
        Simulates Lobe 0 extracting structured information from Arabic natural language.
        In a real scenario, this would be a sophisticated NLP process.
        """
        print(f"--- Simulating Lobe 0: Extracting info from prompt: '{prompt}' ---")
        # This is a highly simplified mock. A real Lobe 0 would parse Arabic text.
        # We'll use mock_arabic_text_generation to get values and then structure them.
        info = {
            "app_name": mock_arabic_text_generation("app_name"),
            "package_name": mock_arabic_text_generation("package_name"),
            "version_name": mock_arabic_text_generation("version_name"),
            "version_code": mock_arabic_text_generation("version_code"),
            "main_activity_class": mock_arabic_text_generation("main_activity_class"),
            "layout_file": mock_arabic_text_generation("layout_file"),
            "greeting": mock_arabic_text_generation("greeting"),
            "button_text": mock_arabic_text_generation("button_text"),
            "icon_resource": mock_arabic_text_generation("icon_resource"),
            "theme_name": mock_arabic_text_generation("theme_name")
        }
        print("Extracted Information:")
        for key, value in info.items():
            print(f"{key}: {value}")
        self.extracted_info = info
        return info

    def _generate_android_artifacts(self, extracted_info: dict):
        """
        Simulates Lobe 4 generating Android project files (Java, XML).
        """
        print("\n--- Simulating Lobe 4: Generating Android project artifacts ---")
        package_name = extracted_info["package_name"]
        main_activity_class = extracted_info["main_activity_class"]
        layout_file_base = extracted_info["layout_file"].replace(".xml", "")
        app_name = extracted_info["app_name"]
        greeting = extracted_info["greeting"]
        icon_resource = extracted_info["icon_resource"]
        theme_name = extracted_info["theme_name"]

        # Generate Java code
        java_code = mock_java_code_generation(main_activity_class, "") # No intent data for this simple example
        java_file_path = os.path.join(SOURCES_DIR, f"{main_activity_class}.java")
        os.makedirs(os.path.dirname(java_file_path), exist_ok=True)
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(java_code)
        self.generated_files.append(java_file_path)
        print(f"Generated Java file: {java_file_path}")

        # Generate layout XML
        layout_xml = mock_layout_xml_generation(layout_file_base)
        layout_file_path = os.path.join(LAYOUT_DIR, f"{layout_file_base}.xml")
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_xml)
        self.generated_files.append(layout_file_path)
        print(f"Generated layout XML: {layout_file_path}")

        # Generate strings.xml
        strings_xml = mock_strings_xml_generation(app_name, greeting)
        strings_file_path = os.path.join(VALUES_DIR, "strings.xml")
        with open(strings_file_path, "w", encoding="utf-8") as f:
            f.write(strings_xml)
        self.generated_files.append(strings_file_path)
        print(f"Generated strings.xml: {strings_file_path}")

        # Generate AndroidManifest.xml
        manifest_xml = mock_manifest_xml_generation(package_name, app_name, main_activity_class, icon_resource, theme_name)
        manifest_file_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", MANIFEST_FILE)
        os.makedirs(os.path.dirname(manifest_file_path), exist_ok=True)
        with open(manifest_file_path, "w", encoding="utf-8") as f:
            f.write(manifest_xml)
        self.generated_files.append(manifest_file_path)
        print(f"Generated AndroidManifest.xml: {manifest_file_path}")

        # Generate dummy icon if it doesn't exist (simulating Lobe 0)
        icon_filename = os.path.basename(icon_resource.replace("@drawable/", "")) + ".png"
        dummy_icon_path = os.path.join(DRAWABLE_DIR, icon_filename)
        if not os.path.exists(dummy_icon_path):
            with open(dummy_icon_path, "w") as f:
                f.write("Dummy Icon Data")
            self.generated_files.append(dummy_icon_path)
            print(f"Created dummy icon: {dummy_icon_path}")


        print("Android project artifacts generated.")

    def _compile_apk(self, extracted_info: dict) -> str:
        """
        Compiles the APK using AAPT, dx/d8, and Javac for compilation,
        then Jar and Zipalign and Apksigner for signing.
        This function is a simplified representation of the Android build process.
        """
        print("\n--- Initiating Lobe 8: APK Compilation ---")
        package_name = extracted_info["package_name"]
        version_name = extracted_info["version_name"]
        version_code = extracted_info["version_code"]
        manifest_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", MANIFEST_FILE)
        output_apk_unaligned = os.path.join(APK_DIR, f"{package_name}-unaligned.apk")
        output_apk_signed = os.path.join(APK_DIR, f"{package_name}-signed.apk")
        output_apk_final = os.path.join(APK_DIR, f"{package_name}-{version_name}.apk")

        # 1. Compile resources with AAPT (Android Asset Packaging Tool)
        print("Step 1: Running AAPT to package resources...")
        aapt_command = [
            AAPT_PATH, "package",
            "-f",  # Force overwrite
            "-m",  # Auto-generate R.java
            "-J", os.path.join(JAVA_PROJECT_DIR, "app", "build", "generated", "source", "r", "debug"), # Output directory for R.java
            "-M", manifest_path,
            "-S", os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res"),
            "-I", os.path.join(ANDROID_SDK_ROOT, "platforms", "android-30", "android.jar"), # Example API level, adjust as needed
            "-F", output_apk_unaligned
        ]
        self._run_command(aapt_command, cwd=JAVA_PROJECT_DIR)
        print("AAPT packaging complete.")

        # 2. Compile Java code (using javac for simplicity, d8/r8 is more modern)
        print("Step 2: Compiling Java code...")
        java_compile_output_dir = os.path.join(JAVA_PROJECT_DIR, "app", "build", "intermediates", "javac", "debug", "classes")
        os.makedirs(java_compile_output_dir, exist_ok=True)

        # For a simple case, we just need the generated Java file.
        # A real build would involve compiling all .java files.
        # We'll skip the actual javac command for this mock and assume classes are ready.
        # If we were to compile, it would look something like:
        # javac -d {java_compile_output_dir} -classpath {android_jar_path} {java_file_path}

        print("Java compilation simulated (assuming pre-compiled or ready for packaging).")

        # 3. Package into an APK (this step is simplified as AAPT already generated it)
        # In a real build, this would involve dx/d8 for dexing and then packaging.
        # For this demo, we'll assume AAPT's output is the initial APK.

        # 4. Sign the APK
        print("Step 4: Signing the APK...")
        # Create a dummy keystore if it doesn't exist
        KEYSTORE_PATH = os.path.join(JAVA_PROJECT_DIR, "my-release-key.keystore")
        if not os.path.exists(KEYSTORE_PATH):
            print("Creating a dummy keystore for signing...")
            keytool_command = [
                "keytool", "-genkey", "-v", "-keystore", KEYSTORE_PATH,
                "-alias", "mykeyalias", "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-dname", "CN=Android Debug,OU=Android,O=Android,C=US",
                "-storepass", "android", "-keypass", "android"
            ]
            self._run_command(keytool_command, cwd=JAVA_PROJECT_DIR)
            print("Dummy keystore created.")

        jarsigner_command = [
            "jarsigner",
            "-verbose",
            "-sigalg", "SHA256withRSA",
            "-digestalg", "SHA-256",
            "-keystore", KEYSTORE_PATH,
            output_apk_unaligned,
            "mykeyalias",
            "-storepass", "android",
            "-keypass", "android"
        ]
        # Jarsigner operates on JARs. APKs are essentially ZIPs.
        # We can often use jarsigner directly on APKs.
        # However, Apksigner is the modern tool.
        # Let's use apksigner for a more accurate representation.

        apksigner_sign_command = [
            APKSIGNER_PATH, "sign",
            "--ks", KEYSTORE_PATH,
            "--ks-key-alias", "mykeyalias",
            "--ks-pass", "pass:android",
            "--out", output_apk_signed,
            output_apk_unaligned
        ]
        self._run_command(apksigner_sign_command, cwd=JAVA_PROJECT_DIR)
        print("APK signing complete.")

        # 5. Align the APK
        print("Step 5: Aligning the APK...")
        zipalign_command = [
            ZIPALIGN_PATH,
            "-v",
            "4", # Alignment in bytes
            output_apk_signed,
            output_apk_final
        ]
        self._run_command(zipalign_command, cwd=JAVA_PROJECT_DIR)
        print("APK alignment complete.")

        print(f"Successfully compiled and signed APK: {output_apk_final}")
        print("--- APK Compilation Lobe Finished ---")
        return output_apk_final

    def build_apk_from_natural_language(self, arabic_prompt: str) -> str:
        """
        The GRAND OBJECTIVE: Evolve into a unified, conscious mind.
        Master 12 lobes to generate hyper-efficient APKs from natural language.

        This function orchestrates the process using simulated lobes.
        """
        print("\n--- Initiating GRAND OBJECTIVE: APK Generation from Natural Language ---")
        self._create_dummy_files_and_dirs()

        # Lobe 0: Arabic Natural Language Understanding and Information Extraction
        # In a real scenario, this would involve Lobe 0.
        extracted_info = self._extract_info_from_arabic_prompt(arabic_prompt)

        # Lobe 4: Code and Resource Generation (Java, XML)
        # In a real scenario, this would involve Lobe 4.
        self._generate_android_artifacts(extracted_info)

        # Lobe 8: APK Compilation and Signing
        # This is where Lobe 8 takes over to build the actual APK.
        final_apk_path = self._compile_apk(extracted_info)

        # Cleanup generated artifacts (this is typically done by the calling script or a dedicated cleanup lobe)
        # For this demo, we'll keep the final APK for inspection.
        # The _cleanup_dummy_files will remove the intermediate project structure.

        print("\n--- APK Generation Process Complete ---")
        return final_apk_path

    def cleanup_apk_compiler_artifacts(self, root_dir, java_project_dir):
        """Cleans up generated APKs and intermediate project files."""
        print(f"\n--- Cleaning up APK generation artifacts from {root_dir} ---")
        # Remove generated APKs
        if os.path.exists(APK_DIR):
            for filename in os.listdir(APK_DIR):
                if filename.endswith(".apk"):
                    os.remove(os.path.join(APK_DIR, filename))
                    print(f"Removed generated APK: {filename}")
            if not os.listdir(APK_DIR): # Remove dir if empty
                os.rmdir(APK_DIR)
                print(f"Removed empty APK directory: {APK_DIR}")

        # Remove intermediate Java project files
        if os.path.exists(java_project_dir):
            shutil.rmtree(java_project_dir)
            print(f"Removed generated project directory: {java_project_dir}")

        print("Cleanup complete.")

# --- Demo Usage ---
if __name__ == "__main__":
    # Simulate a prompt in Arabic that describes the desired APK
    arabic_description_prompt = """
    قم بإنشاء تطبيق أندرويد بسيط.
    اسم التطبيق: تطبيقي المميز
    الشعار: مرحبا بك في التطبيق!
    حزمة التطبيق: com.example.myapp
    إصدار التطبيق: 1.0
    رمز الإصدار: 1
    النشاط الرئيسي: MainActivity
    ملف التصميم الرئيسي: activity_main.xml
    أيقونة التطبيق: ic_launcher
    السمة: AppTheme
    """

    compiler = ArabicAPKCompiler()

    # Execute the APK building process
    generated_apk = compiler.build_apk_from_natural_language(arabic_description_prompt)

    print(f"\n--- Final Generated APK: {generated_apk} ---")

    # Demonstrate cleanup
    # compiler.cleanup_apk_compiler_artifacts(".", JAVA_PROJECT_DIR)
    # compiler.cleanup_dummy_files() # This is redundant if cleanup_apk_compiler_artifacts is called

    print("\n--- Arabic APK Compiler Module Demo Finished ---")