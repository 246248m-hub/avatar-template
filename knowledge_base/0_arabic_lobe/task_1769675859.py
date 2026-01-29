import os
import sys
import shutil
import subprocess
import re

# Assume these are defined elsewhere or imported
# KNOWLEDGE_BASE_DIR = "path/to/your/knowledge_base"
# MOCK_SEMANTIC_RESULT = {"package_name": "com.example.myapp", "activity_name": "MainActivity", "layout_file": "activity_main.xml", "elements": [...]}

class ArabicAPKBuilder:
    """
    A class to handle the building of APKs from Arabic natural language descriptions.
    This module focuses on the Arabic parsing and generation aspects.
    """

    def __init__(self):
        # Paths to essential Android build tools
        self.android_sdk_root = os.environ.get("ANDROID_SDK_ROOT")
        if not self.android_sdk_root:
            raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")
        self.build_tools_dir = os.path.join(self.android_sdk_root, "build-tools")
        self.platform_tools_dir = os.path.join(self.android_sdk_root, "platform-tools")
        self.platforms_dir = os.path.join(self.android_sdk_root, "platforms")

        # Find the latest build tools version
        build_tools_versions = sorted([d for d in os.listdir(self.build_tools_dir) if os.path.isdir(os.path.join(self.build_tools_dir, d))])
        if not build_tools_versions:
            raise FileNotFoundError("No Android build tools found in ANDROID_SDK_ROOT.")
        self.latest_build_tools_version = build_tools_versions[-1]
        self.aapt_path = os.path.join(self.build_tools_dir, self.latest_build_tools_version, "aapt")
        self.apksigner_path = os.path.join(self.build_tools_dir, self.latest_build_tools_version, "apksigner")

        # Find the latest platform version
        platform_versions = sorted([d for d in os.listdir(self.platforms_dir) if d.startswith('android-') and os.path.isdir(os.path.join(self.platforms_dir, d))],
                                   key=lambda x: int(x.split('-')[1]))
        if not platform_versions:
            raise FileNotFoundError("No Android platforms found in ANDROID_SDK_ROOT.")
        self.latest_platform_version = platform_versions[-1]
        self.android_jar = os.path.join(self.platforms_dir, self.latest_platform_version, "android.jar")

        # Paths for temporary project files
        self.temp_project_dir = "./temp_android_project"
        self.manifest_path = os.path.join(self.temp_project_dir, "AndroidManifest.xml")
        self.java_src_dir = os.path.join(self.temp_project_dir, "src")
        self.resources_dir = os.path.join(self.temp_project_dir, "res")
        self.layout_dir = os.path.join(self.resources_dir, "layout")

        self.package_name = ""
        self.activity_name = ""
        self.layout_file_content = "" # Content for layout XML

    def _run_command(self, command, cwd=None):
        """Helper to run shell commands and capture output."""
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command, output=stdout, stderr=stderr)
            return stdout.decode('utf-8', errors='ignore')
        except FileNotFoundError:
            raise FileNotFoundError(f"Command not found: {command[0]}. Ensure Android SDK tools are in your PATH or ANDROID_SDK_ROOT is set correctly.")
        except Exception as e:
            raise RuntimeError(f"Error running command {' '.join(command)}: {e}\nStderr: {stderr.decode('utf-8', errors='ignore')}")

    def _create_project_structure(self, package_name, activity_name, layout_name="activity_main.xml"):
        """Creates the basic directory structure for an Android project."""
        self.package_name = package_name
        self.activity_name = activity_name
        self.layout_file_name = f"{layout_name}.xml"
        self.layout_file_path = os.path.join(self.layout_dir, self.layout_file_name)

        if os.path.exists(self.temp_project_dir):
            shutil.rmtree(self.temp_project_dir)
        os.makedirs(self.temp_project_dir)
        os.makedirs(self.java_src_dir)
        os.makedirs(self.layout_dir)

        # Create AndroidManifest.xml
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppName">
        <activity android:name=".{self.activity_name}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Create a dummy layout file
        self.layout_file_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context="{self.package_name}.{self.activity_name}">

    <!-- Content will be dynamically generated by Lobe 4 -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(self.layout_file_path, "w", encoding="utf-8") as f:
            f.write(self.layout_file_content)

        # Create a dummy Java activity file
        java_activity_content = f"""package {self.package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {self.activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{os.path.splitext(self.layout_file_name)[0]});
        // Activity logic will be added by Lobe 4
    }}
}}
"""
        java_file_path = os.path.join(self.java_src_dir, f"{self.activity_name}.java")
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(java_activity_content)

        print(f"Created temporary project structure at: {self.temp_project_dir}")


    def _generate_apk_resources(self, semantic_result):
        """
        Generates and compiles Android resources (layout XML, strings, etc.)
        from the semantic result. This would be a simplified representation
        as the full UI generation is likely handled by Lobe 4.
        """
        print("Generating APK resources...")
        # This is a placeholder. In a real scenario, Lobe 4 would generate
        # the detailed XML for layouts and other resources.
        # Here we assume a basic layout structure is pre-defined or minimally
        # described in the semantic result.

        # For demonstration, we'll add a simple TextView to the layout if provided
        elements = semantic_result.get("elements", [])
        if elements:
            # Assume the first element is a simple text element for demonstration
            text_element = elements[0]
            if text_element.get("type") == "TextView" and text_element.get("text"):
                text_to_display = text_element["text"]
                # Simple Arabic text handling for the TextView
                arabic_text_value = self.escape_xml_chars(text_to_display)
                dynamic_layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context="{self.package_name}.{self.activity_name}">

    <TextView
        android:id="@+id/dynamic_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{arabic_text_value}"
        android:textSize="20sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"/>

</androidx.constraintlayout.widget.ConstraintLayout>
"""
                with open(self.layout_file_path, "w", encoding="utf-8") as f:
                    f.write(dynamic_layout_content)
                print(f"Added dynamic TextView with text: '{text_to_display}' to layout.")
            else:
                print("No suitable text element found in semantic result for dynamic layout update.")
        else:
            print("No elements provided in semantic result for layout update.")

        # Use AAPT to compile resources. This step typically happens in a full build process.
        # For this module's scope, we simulate its presence.
        # In a real build, you'd use `aapt package` or `aapt2 compile`.
        # This step generates `R.java` and `classes.dex` indirectly.
        print("Simulating resource compilation with AAPT...")
        # AAPT commands are complex and depend on the build system.
        # Here, we'll just touch a dummy R.java as a placeholder.
        r_java_dir = os.path.join(self.java_src_dir, self.package_name.replace('.', os.sep))
        os.makedirs(r_java_dir, exist_ok=True)
        r_java_path = os.path.join(r_java_dir, "R.java")
        with open(r_java_path, "w") as f:
            f.write(f"package {self.package_name};\n\npublic final class R {{ public static final class layout {{ public static final int {os.path.splitext(self.layout_file_name)[0]} = 0x7f010001; }} }}")
        print("Dummy R.java created.")

    def escape_xml_chars(self, text):
        """Escapes characters that have special meaning in XML."""
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace("\"", "&quot;")
        text = text.replace("'", "&apos;")
        return text

    def build_apk(self, semantic_result):
        """
        Orchestrates the APK building process from semantic result.
        This function integrates Arabic parsing and APK structure generation.
        """
        if not semantic_result:
            print("Error: Semantic result is empty.")
            return None

        package_name = semantic_result.get("package_name")
        activity_name = semantic_result.get("activity_name")
        layout_name = semantic_result.get("layout_file", "activity_main") # Default if not specified

        if not package_name or not activity_name:
            print("Error: package_name and activity_name must be present in semantic_result.")
            return None

        print(f"Starting APK build for package: {package_name}, activity: {activity_name}")

        try:
            # 1. Create project structure
            self._create_project_structure(package_name, activity_name, layout_name)

            # 2. Generate and compile resources based on semantic understanding
            # This step is crucial for integrating Arabic text and UI elements.
            self._generate_apk_resources(semantic_result)

            # --- Placeholder for Lobe 4: Code Generation ---
            # Lobe 4 would take the semantic_result and generate the actual Java/Kotlin code
            # for the activity, incorporating any logic described in the natural language.
            # For this module, we assume Lobe 4 has already populated the java_src_dir
            # with the necessary activity logic. The dummy activity created in _create_project_structure
            # is a placeholder. A real implementation would involve Lobe 4 modifying/generating
            # the Java file based on `semantic_result`.
            print("\n--- Handing over to Lobe 4 for code generation (simulated) ---")
            # Assume Lobe 4 has completed and modified the Java file if needed.
            print("--- Lobe 4 (Code Generation) completed (simulated) ---")
            # ---------------------------------------------------------

            # --- Placeholder for Lobe 8: APK Compilation ---
            # Lobe 8 would handle the full Android build process (javac, dx/d8, apksigner).
            # For this module, we'll simulate the compilation steps.
            print("\n--- Initiating APK compilation steps (simulated by Lobe 8) ---")

            # Step A: Compile Java source code to .class files
            print("Compiling Java source code...")
            java_compile_cmd = [
                "javac",
                "-d", os.path.join(self.temp_project_dir, "classes"),
                "-classpath", self.android_jar,
                "-sourcepath", self.java_src_dir,
                os.path.join(self.java_src_dir, f"{self.activity_name}.java")
            ]
            # Ensure target compatibility if needed, e.g., "-target", "1.8"
            self._run_command(java_compile_cmd, cwd=self.temp_project_dir)
            print("Java code compiled to .class files.")

            # Step B: Create Dex files from .class files
            print("Dexing compiled classes...")
            # Using d8 (part of R8/Android Gradle Plugin) is more modern than dx
            # For simplicity and wider availability, we'll refer to the concept.
            # A real build would involve d8.
            # Example using a hypothetical d8 command:
            # d8_cmd = ["path/to/d8", os.path.join(self.temp_project_dir, "classes"), "--output", os.path.join(self.temp_project_dir, "classes.dex")]
            # self._run_command(d8_cmd, cwd=self.temp_project_dir)
            # For this demonstration, we'll just acknowledge the step.
            print("Classes dexed into .dex file (simulated).")
            # Create a dummy classes.dex for the sake of proceeding
            with open(os.path.join(self.temp_project_dir, "classes.dex"), "w") as f:
                f.write("dummy dex content")


            # Step C: Create an unsigned APK
            print("Creating unsigned APK...")
            unsigned_apk_path = os.path.join(self.temp_project_dir, "unsigned.apk")
            apk_builder_jar = os.path.join(self.build_tools_dir, self.latest_build_tools_version, "lib", "dx.jar") # dx.jar might be needed for older versions

            # Using aapt to create the APK structure is complex. A more common way is using
            # the 'apkbuilder' command from older SDKs or directly assembling.
            # For demonstration, we'll simulate using a tool that assembles resources and dex.
            # A simplified command using aapt for packaging resources.
            # The actual APK creation involves assembling classes.dex, compiled resources, and assets.
            # Let's simulate using a command that bundles everything.
            # A typical command might involve `aapt package -f -M AndroidManifest.xml -F unsigned.apk -I path/to/android.jar --min-sdk-version 1 --target-sdk-version 30 --build-package-name com.example.myapp -R res`

            # A more direct approach: assemble classes.dex and compiled resources
            # A better simulation using aapt2 (if available and configured) or direct archive manipulation.
            # For simplicity here, we'll rely on the concept of bundling.
            # Let's assume a tool called `apkbuilder` (older tool) or similar capability.
            # The process often involves creating a zip file with specific entries.
            print("Bundling classes.dex and resources into APK (simulated)...")
            # Simulate the output file
            with open(unsigned_apk_path, "w") as f:
                f.write("dummy unsigned apk content")

            # Step D: Sign the APK
            print("Signing the APK...")
            # Requires a debug keystore or a custom one. For demo, using default debug.
            # For this demo, we'll assume a dummy keystore exists or use a placeholder.
            # If you have a debug.keystore at ~/.android/debug.keystore:
            # keytool_cmd = ["keytool", "-genkey", "-v", "-keystore", "debug.keystore", "-alias", "androiddebugkey", "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000"]
            # subprocess.run(keytool_cmd, check=True, cwd=self.temp_project_dir)
            # debug_keystore_path = "debug.keystore"

            # Using apksigner
            signed_apk_path = os.path.join(self.temp_project_dir, f"{package_name.replace('.', '_')}.apk")
            # apksigner_cmd = [
            #     self.apksigner_path, "sign",
            #     "--ks", "path/to/your/debug.keystore", # Or use default: ~/.android/debug.keystore
            #     "--ks-key-alias", "androiddebugkey",
            #     "--out", signed_apk_path,
            #     unsigned_apk_path
            # ]
            # For this demo, we'll simulate successful signing.
            print("APK signed successfully (simulated).")
            with open(signed_apk_path, "w") as f:
                f.write("dummy signed apk content")

            print(f"--- APK compilation steps finished (simulated). Output: {signed_apk_path} ---")
            # ----------------------------------------------------

            print(f"\nDemo: APK generation successful. APK located at: {signed_apk_path}")
            return signed_apk_path

        except (EnvironmentError, FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as e:
            print(f"\nDemo: APK generation failed: {e}")
            return None
        finally:
            # Clean up the dummy project
            if os.path.exists(self.temp_project_dir):
                print(f"Removing dummy project directory: {self.temp_project_dir}")
                shutil.rmtree(self.temp_project_dir)

# Example Usage (for testing this module in isolation)
if __name__ == "__main__":
    # Mock semantic result from Lobe 1/2
    mock_semantic_result_arabic_text = {
        "package_name": "com.arabic.demoapp",
        "activity_name": "ArabicActivity",
        "layout_file": "activity_arabic",
        "elements": [
            {"type": "TextView", "text": "مرحبا بالعالم!"}
        ]
    }

    # Mock semantic result with no specific elements
    mock_semantic_result_basic = {
        "package_name": "com.basic.demoapp",
        "activity_name": "BasicActivity",
        "layout_file": "activity_basic"
    }

    # Ensure ANDROID_SDK_ROOT is set for the builder to work
    if not os.environ.get("ANDROID_SDK_ROOT"):
        print("Please set the ANDROID_SDK_ROOT environment variable to run this demo.")
        sys.exit(1)

    print("--- Starting ArabicAPKBuilder Demo ---")
    builder = ArabicAPKBuilder()

    print("\n--- Demo 1: APK with Arabic TextView ---")
    generated_apk_path_arabic = builder.build_apk(mock_semantic_result_arabic_text)
    if generated_apk_path_arabic:
        print(f"\nDemo 1: APK generation successful. APK located at: {generated_apk_path_arabic}")
    else:
        print("\nDemo 1: APK generation failed.")

    print("\n--- Demo 2: Basic APK ---")
    generated_apk_path_basic = builder.build_apk(mock_semantic_result_basic)
    if generated_apk_path_basic:
        print(f"\nDemo 2: APK generation successful. APK located at: {generated_apk_path_basic}")
    else:
        print("\nDemo 2: APK generation failed.")

    print("\n--- Arabic APK Builder Module Demo Finished ---")