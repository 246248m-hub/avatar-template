import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

# --- Constants ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable is not set.")

AAPT2_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "aapt2")
APK_BUILDER_SCRIPT = "build_apk.sh"  # Assumes a shell script for simplicity

# --- Helper Functions ---
def find_package_name(manifest_path):
    """Parses AndroidManifest.xml to find the package name."""
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        return root.get('package')
    except ET.ParseError:
        print(f"Error parsing manifest: {manifest_path}")
        return None
    except FileNotFoundError:
        print(f"Manifest file not found: {manifest_path}")
        return None

def compile_java_code(src_dir, output_dir, classpath):
    """Compiles Java source files using javac."""
    java_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(src_dir) for f in fn if f.endswith('.java')]
    if not java_files:
        print("No Java files found to compile.")
        return True

    javac_cmd = [
        "javac",
        "-d", output_dir,
        "-classpath", classpath,
        *java_files
    ]

    try:
        subprocess.run(javac_cmd, check=True, capture_output=True, text=True)
        print(f"Java compilation successful. Classes in: {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Java compilation failed: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def package_dex(classes_dir, output_dex_path, dx_tool_path):
    """Converts Java class files to Dalvik Executable (DEX) format using dx."""
    dex_cmd = [
        dx_tool_path,
        "--dex",
        f"--output={output_dex_path}",
        classes_dir
    ]
    try:
        subprocess.run(dex_cmd, check=True, capture_output=True, text=True)
        print(f"DEX packaging successful. DEX file: {output_dex_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"DEX packaging failed: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def build_apk_from_dex_and_resources(dex_path, res_dir, manifest_path, output_apk_path, aapt2_path, signing_key_alias="mykey", signing_key_store="mykeystore.jks", signing_key_password="password", store_password="password"):
    """
    Builds an APK using AAPT2 for resource compilation and a basic script for packaging.
    This function simulates the core APK building process.
    """
    print("\n--- Starting APK build process ---")

    # Create a temporary directory for intermediate files
    temp_build_dir = os.path.join(os.path.dirname(output_apk_path), "temp_apk_build")
    os.makedirs(temp_build_dir, exist_ok=True)

    # 1. Compile resources with AAPT2
    print("Compiling resources with AAPT2...")
    compiled_res_dir = os.path.join(temp_build_dir, "res_compiled")
    os.makedirs(compiled_res_dir, exist_ok=True)
    aapt2_link_cmd = [
        aapt2_path, "link",
        "-o", os.path.join(temp_build_dir, "resources.zip"),
        "--manifest", manifest_path,
        "--auto-add-overlay",
        res_dir
    ]
    try:
        subprocess.run(aapt2_link_cmd, check=True, capture_output=True, text=True)
        print("Resource linking successful.")
    except subprocess.CalledProcessError as e:
        print(f"Resource linking failed: {e}")
        print(f"Stderr: {e.stderr}")
        shutil.rmtree(temp_build_dir)
        return False

    # 2. Package the APK (using a simplified approach, a real build would use apksigner etc.)
    # In a real scenario, you'd use `apksigner` and `zipalign`.
    # For this example, we'll simulate by creating a directory structure and zipping it.
    print("Packaging APK structure...")
    apk_staging_dir = os.path.join(temp_build_dir, "apk_staging")
    os.makedirs(apk_staging_dir, exist_ok=True)

    # Copy compiled resources (from zip to a temp folder)
    extract_res_dir = os.path.join(apk_staging_dir, "res")
    os.makedirs(extract_res_dir, exist_ok=True)
    subprocess.run(["unzip", os.path.join(temp_build_dir, "resources.zip"), "-d", extract_res_dir], check=True)

    # Copy DEX file
    os.makedirs(os.path.join(apk_staging_dir, "smali"), exist_ok=True)
    shutil.copy(dex_path, os.path.join(apk_staging_dir, "smali", "classes.dex"))

    # Copy AndroidManifest.xml
    shutil.copy(manifest_path, os.path.join(apk_staging_dir, "AndroidManifest.xml"))

    # Create the APK by zipping the staging directory
    # Note: This is a very basic simulation. Real APKs require signing and zipaligning.
    print("Creating APK archive (simulated)...")
    try:
        # Create a zip archive that mimics an APK structure
        subprocess.run([
            "zip", "-j", "-X", output_apk_path,
            os.path.join(apk_staging_dir, "AndroidManifest.xml"),
            os.path.join(apk_staging_dir, "res", "*"),
            os.path.join(apk_staging_dir, "smali", "*")
        ], check=True, capture_output=True, text=True)
        print(f"APK created at: {output_apk_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"APK creation failed: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    finally:
        # Cleanup intermediate build directory
        shutil.rmtree(temp_build_dir)
        print("Intermediate build files cleaned up.")


class APKBuilderLobe:
    def __init__(self, android_sdk_root, dx_tool_path):
        self.android_sdk_root = android_sdk_root
        self.aapt2_path = os.path.join(android_sdk_root, "build-tools", "current", "aapt2")
        if not os.path.exists(self.aapt2_path):
            raise FileNotFoundError(f"aapt2 not found at: {self.aapt2_path}")
        self.dx_tool_path = dx_tool_path
        if not os.path.exists(self.dx_tool_path):
            raise FileNotFoundError(f"dx tool not found at: {self.dx_tool_path}")

    def build_apk(self, src_dir, res_dir, manifest_path, output_apk_path):
        """
        Orchestrates the APK building process from source code and resources.
        This includes Java compilation, DEX conversion, and resource packaging.
        """
        print(f"\n--- Initiating APK Build for: {output_apk_path} ---")

        # Create temporary directories for compilation and DEX
        temp_dir = os.path.join(os.path.dirname(output_apk_path), "temp_build_artifacts")
        os.makedirs(temp_dir, exist_ok=True)
        classes_dir = os.path.join(temp_dir, "classes")
        dex_output_path = os.path.join(temp_dir, "classes.dex")
        os.makedirs(classes_dir, exist_ok=True)

        # 1. Compile Java code
        # For simplicity, assume Android dependencies are handled by the environment or build system.
        # A real-world scenario would require managing JARs and build configurations.
        print("Compiling Java sources...")
        java_compile_success = compile_java_code(src_dir, classes_dir, "") # Empty classpath for now, needs proper setup
        if not java_compile_success:
            print("Java compilation failed. Aborting APK build.")
            shutil.rmtree(temp_dir)
            return False

        # 2. Convert compiled classes to DEX
        print("Converting Java classes to DEX...")
        dex_package_success = package_dex(classes_dir, dex_output_path, self.dx_tool_path)
        if not dex_package_success:
            print("DEX packaging failed. Aborting APK build.")
            shutil.rmtree(temp_dir)
            return False

        # 3. Build the final APK using compiled DEX and resources
        print("Building final APK...")
        apk_build_success = build_apk_from_dex_and_resources(
            dex_output_path,
            res_dir,
            manifest_path,
            output_apk_path,
            self.aapt2_path
        )

        # Cleanup temporary build artifacts
        print("Cleaning up temporary build artifacts...")
        shutil.rmtree(temp_dir)
        print("Temporary build artifacts removed.")

        if apk_build_success:
            print(f"APK built successfully at: {output_apk_path}")
            return True
        else:
            print(f"APK build failed.")
            return False

# Example Usage (assuming you have an Android SDK configured and a project structure)
if __name__ == "__main__":
    # --- Setup Dummy Environment ---
    temp_project_dir = "dummy_android_project"
    src_dir = os.path.join(temp_project_dir, "app", "src", "main", "java")
    res_dir = os.path.join(temp_project_dir, "app", "src", "main", "res")
    manifest_path = os.path.join(temp_project_dir, "app", "src", "main", "AndroidManifest.xml")
    output_apk_path = "output.apk"

    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    # Create a dummy Java file
    dummy_java_content = """
package com.example.myapp;

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming R is generated
    }
}
"""
    with open(os.path.join(src_dir, "MainActivity.java"), "w") as f:
        f.write(dummy_java_content)

    # Create a dummy AndroidManifest.xml
    dummy_manifest_content = """
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">
    <application android:label="@string/app_name">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(manifest_path, "w") as f:
        f.write(dummy_manifest_content)

    # Create a dummy res/layout/activity_main.xml (needed for R.layout.activity_main)
    os.makedirs(os.path.join(res_dir, "layout"), exist_ok=True)
    dummy_layout_content = """
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    <!-- Content here -->
</LinearLayout>
"""
    with open(os.path.join(res_dir, "layout", "activity_main.xml"), "w") as f:
        f.write(dummy_layout_content)

    # Find dx tool path (common location)
    dx_tool_path = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "dx")
    if not os.path.exists(dx_tool_path):
        print(f"Could not find dx tool at {dx_tool_path}. Please ensure it's in your SDK's build-tools.")
    else:
        try:
            apk_builder = APKBuilderLobe(ANDROID_SDK_ROOT, dx_tool_path)
            apk_generated = apk_builder.build_apk(src_dir, res_dir, manifest_path, output_apk_path)

            if apk_generated:
                print(f"\n--- APK Building Process Demo Completed Successfully. APK generated at: {output_apk_path} ---")
            else:
                print("\n--- APK Building Process Demo Failed ---")

        except EnvironmentError as e:
            print(f"Error setting up APK builder: {e}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        finally:
            # --- Cleanup dummy environment ---
            print("\n--- Cleaning up dummy environment ---")
            if os.path.exists(temp_project_dir):
                shutil.rmtree(temp_project_dir)
                print("Dummy project environment removed.")
            if os.path.exists(output_apk_path):
                os.remove(output_apk_path)
                print("Output APK removed.")