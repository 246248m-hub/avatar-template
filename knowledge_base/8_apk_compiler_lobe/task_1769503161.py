import os
import subprocess
import shutil
import re

# Global constants (could be defined in a separate config file)
JAVA_HOME = os.environ.get("JAVA_HOME")
if not JAVA_HOME:
    raise EnvironmentError("JAVA_HOME environment variable not set. Please set it to your JDK path.")

ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set. Please set it to your Android SDK path.")

AAPT2_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "aapt2") # Assuming current is the latest build tools
DX_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "dx")
ADB_PATH = os.path.join(ANDROID_SDK_ROOT, "platform-tools", "adb")

class ApkCompiler:
    def __init__(self, project_dir="temp_apk_project"):
        self.project_dir = project_dir
        self.src_dir = os.path.join(self.project_dir, "src")
        self.res_dir = os.path.join(self.project_dir, "res")
        self.assets_dir = os.path.join(self.project_dir, "assets")
        self.bin_dir = os.path.join(self.project_dir, "bin")
        self.apk_path = os.path.join(self.bin_dir, "app.apk")
        self.manifest_path = os.path.join(self.project_dir, "AndroidManifest.xml")
        self.dex_path = os.path.join(self.bin_dir, "classes.dex")

    def setup_project_structure(self):
        """Creates the necessary directory structure for an APK project."""
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.res_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.bin_dir, exist_ok=True)

    def create_manifest(self, package_name="com.example.unifiedmind", version_code=1, version_name="1.0"):
        """Generates a basic AndroidManifest.xml."""
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}"
    android:versionCode="{version_code}"
    android:versionName="{version_name}">

    <uses-sdk android:minSdkVersion="16" android:targetSdkVersion="33"/>

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
        with open(self.manifest_path, "w") as f:
            f.write(manifest_content)

    def create_main_activity(self, activity_name="MainActivity"):
        """Generates a basic Java MainActivity file."""
        activity_content = f"""
package {self.get_package_name()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()}); // Assuming layout file exists

        TextView textView = findViewById(R.id.textView);
        textView.setText("Hello from Unified Mind APK!");
    }}
}}
"""
        activity_file_path = os.path.join(self.src_dir, f"{activity_name}.java")
        os.makedirs(os.path.dirname(activity_file_path), exist_ok=True)
        with open(activity_file_path, "w") as f:
            f.write(activity_content)

    def create_layout_file(self, activity_name="MainActivity"):
        """Generates a basic XML layout file."""
        layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Initializing..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_dir = os.path.join(self.res_dir, "layout")
        os.makedirs(layout_dir, exist_ok=True)
        layout_file_path = os.path.join(layout_dir, f"activity_{activity_name.lower()}.xml")
        with open(layout_file_path, "w") as f:
            f.write(layout_content)

    def create_string_resource(self):
        """Generates a basic strings.xml file."""
        strings_content = """
<resources>
    <string name="app_name">UnifiedMindApp</string>
</resources>
"""
        res_values_dir = os.path.join(self.res_dir, "values")
        os.makedirs(res_values_dir, exist_ok=True)
        strings_file_path = os.path.join(res_values_dir, "strings.xml")
        with open(strings_file_path, "w") as f:
            f.write(strings_content)

    def get_package_name(self):
        """Parses the package name from the manifest."""
        with open(self.manifest_path, "r") as f:
            content = f.read()
            match = re.search(r'package="([^"]+)"', content)
            if match:
                return match.group(1)
        return "com.example.unifiedmind" # Default if parsing fails

    def compile_java_to_dex(self):
        """Compiles Java source files into a Dalvik Executable (DEX) file."""
        print(f"Compiling Java to DEX using: {DX_PATH}")
        # Ensure all Java files are collected
        java_files = []
        for root, _, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))

        if not java_files:
            print("No Java files found to compile.")
            return

        command = [DX_PATH, "--dex", "--output", self.dex_path] + java_files
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Successfully compiled Java to DEX: {self.dex_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling Java to DEX: {e.stderr}")
            raise

    def compile_resources(self):
        """Compiles Android resources using AAPT2."""
        print(f"Compiling resources using AAPT2: {AAPT2_PATH}")
        # AAPT2 requires an intermediate directory for its compilation steps
        aapt2_intermediate_dir = os.path.join(self.project_dir, "aapt2_temp")
        os.makedirs(aapt2_intermediate_dir, exist_ok=True)

        # Step 1: Compile resources
        compile_command = [
            AAPT2_PATH, "compile",
            f"--dir", self.res_dir,
            f"-o", os.path.join(aapt2_intermediate_dir, "resources.zip")
        ]
        try:
            subprocess.run(compile_command, check=True, capture_output=True, text=True)
            print("Resource compilation step completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error in AAPT2 compile step: {e.stderr}")
            raise

        # Step 2: Link resources
        link_command = [
            AAPT2_PATH, "link",
            f"--manifest", self.manifest_path,
            f"-o", os.path.join(self.bin_dir, "resources.apk"), # AAPT2 link creates an intermediate APK
            f"--java-symbols", os.path.join(aapt2_intermediate_dir, "R.java"),
            os.path.join(aapt2_intermediate_dir, "resources.zip")
        ]
        try:
            subprocess.run(link_command, check=True, capture_output=True, text=True)
            print("Resource linking step completed.")
            # Move the generated R.java to src directory for compilation
            if os.path.exists(os.path.join(aapt2_intermediate_dir, "R.java")):
                 shutil.move(os.path.join(aapt2_intermediate_dir, "R.java"), self.src_dir)

        except subprocess.CalledProcessError as e:
            print(f"Error in AAPT2 link step: {e.stderr}")
            raise
        finally:
            # Clean up AAPT2 temporary directory
            if os.path.exists(aapt2_intermediate_dir):
                shutil.rmtree(aapt2_intermediate_dir)


    def create_apk(self):
        """Bundles compiled DEX and resources into an APK file using apksigner."""
        # This is a simplified process. A real build would involve more steps
        # like packaging Java code, dealing with libraries, and signing.

        print("Bundling DEX and resources into APK...")

        # For simplicity, we'll create a dummy zip and rename it to .apk
        # A real process would use the Android SDK's apksigner and zipalign.

        # Collect all files that should go into the APK
        files_to_zip = []
        files_to_zip.append(self.dex_path)
        # Add resources from the linked APK created by AAPT2
        resource_apk_path = os.path.join(self.bin_dir, "resources.apk")
        if os.path.exists(resource_apk_path):
            # Extract contents of the resource APK
            temp_res_extract_dir = os.path.join(self.project_dir, "temp_res_extract")
            os.makedirs(temp_res_extract_dir, exist_ok=True)
            with zipfile.ZipFile(resource_apk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_res_extract_dir)
            for root, _, files in os.walk(temp_res_extract_dir):
                for file in files:
                    files_to_zip.append(os.path.join(root, file))

        # Create a temporary directory to build the APK contents
        temp_apk_build_dir = os.path.join(self.bin_dir, "apk_build")
        os.makedirs(temp_apk_build_dir, exist_ok=True)

        # Copy collected files into the build directory, maintaining structure
        for file_path in files_to_zip:
            relative_path = os.path.relpath(file_path, self.bin_dir)
            dest_path = os.path.join(temp_apk_build_dir, relative_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_path, dest_path)

        # Now zip the contents of temp_apk_build_dir into the final APK
        with zipfile.ZipFile(self.apk_path, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
            for root, _, files in os.walk(temp_apk_build_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, temp_apk_build_dir)
                    apk_zip.write(file_path, archive_name)

        print(f"Successfully created dummy APK: {self.apk_path}")
        # In a real scenario, you'd run zipalign and apksigner here.
        # e.g., subprocess.run(["zipalign", "-v", "4", self.apk_path, self.apk_path])
        # e.g., subprocess.run(["apksigner", "sign", "--ks", "my-release-key.keystore", "--out", self.apk_path, self.apk_path])

    def cleanup_build_artifacts(self):
        """Removes the temporary project directory."""
        if os.path.exists(self.project_dir):
            print(f"Cleaning up build artifacts: {self.project_dir}")
            shutil.rmtree(self.project_dir)

# --- Lobe 8_apk_compiler_lobe ---
# This lobe focuses on compiling generated code and resources into an APK.
# It will orchestrate the process of creating an Android project structure,
# compiling Java code to DEX, and packaging resources.

import zipfile # Import zipfile for creating the APK

def build_apk_from_code_and_resources(java_code_str: str, manifest_content: str, resources_dict: dict) -> str:
    """
    Builds a simulated APK from provided Java code string, manifest content, and resources.

    Args:
        java_code_str: A string containing the Java source code for an Android Activity.
        manifest_content: A string containing the AndroidManifest.xml content.
        resources_dict: A dictionary where keys are resource paths (e.g., 'layout/activity_main.xml')
                        and values are their content as strings.

    Returns:
        The path to the generated (simulated) APK file.
    """
    compiler = ApkCompiler()
    compiler.setup_project_structure()

    # Write manifest
    with open(compiler.manifest_path, "w") as f:
        f.write(manifest_content)

    # Write Java code
    # Infer package name from manifest for correct file placement
    package_name = compiler.get_package_name()
    java_src_dir = os.path.join(compiler.src_dir, package_name.replace('.', '/'))
    os.makedirs(java_src_dir, exist_ok=True)
    java_file_name = re.search(r'public class (\w+)', java_code_str).group(1) if re.search(r'public class (\w+)', java_code_str) else "GeneratedActivity"
    java_file_path = os.path.join(java_src_dir, f"{java_file_name}.java")
    with open(java_file_path, "w") as f:
        f.write(java_code_str)

    # Write resources
    for res_path, res_content in resources_dict.items():
        full_res_path = os.path.join(compiler.project_dir, res_path)
        os.makedirs(os.path.dirname(full_res_path), exist_ok=True)
        with open(full_res_path, "w") as f:
            f.write(res_content)

    # Compile Java to DEX
    compiler.compile_java_to_dex()

    # Compile resources using AAPT2
    # For this simulation, we'll directly use the provided resource content.
    # A real AAPT2 compilation would process these. We'll simulate the output structure.
    # For now, we rely on the previously created layout and string files.
    # We'll bypass the complex AAPT2 compilation for this simulated APK creation
    # and directly use the provided resources.

    # Instead of full AAPT2 compilation, we'll simulate the resource packaging.
    # A simplified approach: Create a dummy resource.apk from the provided resources.
    # This is a significant simplification of AAPT2's role.
    resource_apk_path = os.path.join(compiler.bin_dir, "resources.apk")
    with zipfile.ZipFile(resource_apk_path, 'w', zipfile.ZIP_DEFLATED) as res_zip:
        for res_path, res_content in resources_dict.items():
            # Add resource content to the zip, mimicking the structure AAPT2 would produce
            res_zip.writestr(res_path, res_content)

    # Combine DEX and simulated resources into an APK
    print("Bundling DEX and simulated resources into APK...")
    temp_apk_build_dir = os.path.join(compiler.bin_dir, "apk_build_from_func")
    os.makedirs(temp_apk_build_dir, exist_ok=True)

    # Copy DEX file
    dex_dest_path = os.path.join(temp_apk_build_dir, os.path.basename(compiler.dex_path))
    shutil.copy2(compiler.dex_path, dex_dest_path)

    # Extract and copy simulated resources
    with zipfile.ZipFile(resource_apk_path, 'r') as zip_ref:
        zip_ref.extractall(temp_apk_build_dir)

    # Add AndroidManifest.xml
    manifest_dest_path = os.path.join(temp_apk_build_dir, "AndroidManifest.xml")
    shutil.copy2(compiler.manifest_path, manifest_dest_path)


    # Create the final APK by zipping the contents
    with zipfile.ZipFile(compiler.apk_path, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
        for root, _, files in os.walk(temp_apk_build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, temp_apk_build_dir)
                apk_zip.write(file_path, archive_name)

    print(f"Successfully created simulated APK at: {compiler.apk_path}")

    # Clean up intermediate directories
    if os.path.exists(temp_apk_build_dir):
        shutil.rmtree(temp_apk_build_dir)
    if os.path.exists(resource_apk_path):
        os.remove(resource_apk_path)
    # Optionally clean up compiler.project_dir if not needed for debugging

    return compiler.apk_path

# Example Usage (for demonstration/testing purposes within this lobe)
if __name__ == "__main__":
    print("\n--- Lobe 8_apk_compiler_lobe Demo ---")

    # Mock data simulating outputs from previous lobes
    mock_java_code = """
package com.example.unifiedmind;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("APK Compiled Successfully!");
    }
}
"""

    mock_manifest_content = """
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.unifiedmind"
    android:versionCode="1"
    android:versionName="1.0">

    <uses-sdk android:minSdkVersion="16" android:targetSdkVersion="33"/>

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

    mock_resources = {
        "res/layout/activity_main.xml": """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Initializing..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""",
        "res/values/strings.xml": """
<resources>
    <string name="app_name">UnifiedMindApp</string>
</resources>
""",
        "res/mipmap-hdpi/ic_launcher.png": "dummy_launcher_icon_data_hdpi", # Dummy placeholder for image
        "res/mipmap-mdpi/ic_launcher.png": "dummy_launcher_icon_data_mdpi", # Dummy placeholder for image
        "res/mipmap-xhdpi/ic_launcher.png": "dummy_launcher_icon_data_xhdpi", # Dummy placeholder for image
        "res/mipmap-xxhdpi/ic_launcher.png": "dummy_launcher_icon_data_xxhdpi", # Dummy placeholder for image
        "res/mipmap-xxxhdpi/ic_launcher.png": "dummy_launcher_icon_data_xxxhdpi", # Dummy placeholder for image
        "res/mipmap-anydpi-v26/ic_launcher.xml": "<?xml version=\"1.0\" encoding=\"utf-8\"?><adaptive-icon xmlns:android=\"http://schemas.android.com/apk/res/android\"><background android:drawable=\"@color/ic_launcher_background\"/><foreground android:drawable=\"@mipmap/ic_launcher_foreground\"/></adaptive-icon>",
        "res/drawable-v24/ic_launcher_foreground.xml": "<?xml version=\"1.0\" encoding=\"utf-8\"?><vector xmlns:android=\"http://schemas.android.com/apk/res/android\" android:width=\"104dp\" android:height=\"104dp\" android:viewportWidth=\"104\" android:viewportHeight=\"104\"><path android:fillColor=\"@android:color/white\" android:pathData=\"M52,52m-52,0a52,52 0,1,1 104,0a52,52 0,1,1 -104,0\"/><path android:pathData=\"M75.6,32.2c-2.5-3.2-6.7-4.3-10.3-2.5c-1.8,0.8-3.5,1.9-5,3.1c-1.5-1.2-3.1-2.3-4.9-3.1c-3.6-1.8-7.8-0.7-10.3,2.5c-3.7,4.6-4.1,11.3-1.7,16.6c2.3,5.2,7.4,8.7,12.7,10.1c3.3,0.9,6.7,1.2,10,1c2.2-0.2,4.4-0.8,6.5-1.7c3.9-1.7,7.6-4.3,10.3-7.7C78.7,44.5,78.1,36.4,75.6,32.2z\" android:fillColor=\"#ffffff\"/><path android:fillColor=\"#00000000\" android:pathData=\"M52,52m-52,0a52,52 0,1,1 104,0a52,52 0,1,1 -104,0\"/><path android:fillColor=\"#00000000\" android:pathData=\"M75.6,32.2c-2.5-3.2-6.7-4.3-10.3-2.5c-1.8,0.8-3.5,1.9-5,3.1c-1.5-1.2-3.1-2.3-4.9-3.1c-3.6-1.8-7.8-0.7-10.3,2.5c-3.7,4.6-4.1,11.3-1.7,16.6c2.3,5.2,7.4,8.7,12.7,10.1c3.3,0.9,6.7,1.2,10,1c2.2-0.2,4.4-0.8,6.5-1.7c3.9-1.7,7.6-4.3,10.3-7.7C78.7,44.5,78.1,36.4,75.6,32.2z\"/></vector>"
    }


    print("\n--- Initiating Lobe 8_apk_compiler_lobe ---")
    try:
        simulated_apk_path = build_apk_from_code_and_resources(
            java_code_str=mock_java_code,
            manifest_content=mock_manifest_content,
            resources_dict=mock_resources
        )
        print(f"\nSimulated APK generated at: {simulated_apk_path}")

        # Clean up the generated APK directory after the demo
        print("\n--- Cleaning up generated APK directory ---")
        # The ApkCompiler's cleanup method removes the 'temp_apk_project'
        compiler_instance_for_cleanup = ApkCompiler(project_dir="temp_apk_project") # Need to instantiate with the default dir
        compiler_instance_for_cleanup.cleanup_build_artifacts()
        print("--- Lobe 8_apk_compiler_lobe Demo Finished ---")

    except EnvironmentError as e:
        print(f"Environment setup error: {e}")
    except FileNotFoundError as e:
        print(f"Dependency not found error: {e}. Make sure JAVA_HOME and ANDROID_SDK_ROOT are set correctly and build tools exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")