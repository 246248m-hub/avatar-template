import os
import subprocess
import shutil
from pathlib import Path

# Assume these paths are defined elsewhere and accessible
# For demonstration purposes, let's define them here
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    # Fallback for local testing if ANDROID_SDK_ROOT is not set
    # This path will likely need to be adjusted based on your system
    ANDROID_SDK_ROOT = Path.home() / "Android/Sdk"
    if not ANDROID_SDK_ROOT.exists():
        raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set and default path not found. Please set ANDROID_SDK_ROOT.")

BUILD_TOOLS_DIR = ANDROID_SDK_ROOT / "build-tools"
# Dynamically find the latest build tools version
try:
    latest_build_tools_version = sorted(os.listdir(BUILD_TOOLS_DIR))[-1]
    APKSIGNER_PATH = BUILD_TOOLS_DIR / latest_build_tools_version / "apksigner"
    AAPT2_PATH = BUILD_TOOLS_DIR / latest_build_tools_VERSION / "aapt2"
except IndexError:
    raise FileNotFoundError("No Android build-tools found. Please ensure you have installed them via the SDK Manager.")


class ApkCompilerLobe:
    def __init__(self, project_root: Path, output_dir: Path):
        self.project_root = project_root
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _run_command(self, command, cwd=None):
        """Helper to run shell commands and capture output."""
        print(f"Running command: {' '.join(command)}")
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error code {e.returncode}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            raise

    def compile_apk(self, manifest_path: Path, resource_dir: Path, source_dir: Path, output_apk_name: str):
        """
        Compiles a basic Android APK from provided manifest, resources, and source code.
        This is a simplified example and assumes a pre-structured project.
        """
        print(f"\n--- Compiling APK for: {output_apk_name} ---")

        # 1. Compile resources using AAPT2
        print("\n--- Compiling resources with AAPT2 ---")
        aapt2_compile_dir = self.project_root / "aapt2_compiled_res"
        aapt2_compile_dir.mkdir(parents=True, exist_ok=True)
        compiled_res_file = aapt2_compile_dir / "resources.zip"

        aapt2_command = [
            str(AAPT2_PATH), "compile",
            "--dir", str(resource_dir),
            "-o", str(compiled_res_file)
        ]
        self._run_command(aapt2_command, cwd=self.project_root)

        # 2. Link resources
        print("\n--- Linking resources with AAPT2 ---")
        link_out_dir = self.project_root / "aapt2_linked_res"
        link_out_dir.mkdir(parents=True, exist_ok=True)
        linked_res_apk_part = link_out_dir / "linked.apk"

        aapt2_link_command = [
            str(AAPT2_PATH), "link",
            "--manifest", str(manifest_path),
            str(compiled_res_file),
            "-o", str(linked_res_apk_part),
            "--java-compile-moto", # This flag enables Java compilation in AAPT2 link stage
            "--auto-add-overlay",
            "--no-version-vectors",
            # Assuming a basic AndroidManifest.xml structure that doesn't need specific SDK version flags for this example
        ]
        self._run_command(aapt2_link_command, cwd=self.project_root)

        # 3. Compile Java sources (if any)
        # This part is highly simplified. A real build process would use javac and dx/d8.
        # For this basic example, we'll assume Java compilation is handled by AAPT2 link or
        # that we are only dealing with pre-compiled .dex files for simplicity.
        # In a full system, you'd call `javac` here to compile .java files into .class,
        # and then `d8` (from build-tools) to convert .class files to .dex files.
        print("\n--- (Skipping explicit Java compilation for this simplified demo) ---")
        print("In a real scenario, Java sources would be compiled here using javac and then d8.")

        # 4. Create APK
        # This step would typically involve packaging compiled code (dex files), resources, assets, etc.
        # For simplicity, we'll use apksigner to directly sign the linked resource file as a placeholder for the final APK.
        # A proper build would use `aapt2` to 'convert' the linked resource file to an intermediate APK,
        # then add compiled dex files, assets, etc., and then sign.
        print("\n--- Creating and Signing APK ---")
        final_apk_path = self.output_dir / f"{output_apk_name}.apk"

        # For this basic example, we'll rename the linked resource file to .apk.
        # This is NOT a fully functional APK but a placeholder for demonstration of signing.
        # A real build process would involve a more complex `aapt2 create` or similar.
        shutil.move(str(linked_res_apk_part), str(final_apk_path))

        # 5. Sign the APK (using a debug key for simplicity)
        # You would typically have a debug.keystore or a production keystore.
        # For this demo, let's assume a dummy keystore for signing.
        # The Android SDK usually comes with a debug.keystore at $HOME/.android/debug.keystore
        debug_keystore_path = Path.home() / ".android" / "debug.keystore"
        if not debug_keystore_path.exists():
            print(f"Warning: Debug keystore not found at {debug_keystore_path}. APK signing may fail or use a placeholder.")
            # Fallback: If no keystore, apksigner might fail. For this demo, we'll proceed but log.
            # In a real application, you'd need to handle keystore creation or management.

        apksigner_command = [
            str(APKSIGNER_PATH), "sign",
            "--ks", str(debug_keystore_path) if debug_keystore_path.exists() else "dummy.keystore", # Use dummy if not found
            "--ks-key-alias", "androiddebugkey",
            "--ks-pass", "pass:android",
            "--key-pass", "pass:android",
            "--out", str(final_apk_path),
            str(final_apk_path) # Input APK is the same as output for signing in-place or overwriting
        ]

        try:
            self._run_command(apksigner_command)
            print(f"Successfully signed APK: {final_apk_path}")
        except Exception as e:
            print(f"APK signing failed: {e}")
            print("Proceeding without successful signing. The generated file might not be installable.")

        return final_apk_path

# Example Usage (requires a dummy project structure for manifest and resources)
if __name__ == "__main__":
    # This section is for demonstration and testing the ApkCompilerLobe
    # It requires creating dummy project files.

    # Create temporary directories for the demo
    DEMO_PROJECT_DIR = Path("./dummy_android_project")
    DEMO_OUTPUT_DIR = Path("./apk_output")

    if DEMO_PROJECT_DIR.exists():
        shutil.rmtree(DEMO_PROJECT_DIR)
    DEMO_PROJECT_DIR.mkdir(parents=True, exist_ok=True)

    if DEMO_OUTPUT_DIR.exists():
        shutil.rmtree(DEMO_OUTPUT_DIR)
    DEMO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create a minimal AndroidManifest.xml
    manifest_content = """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp"
    android:versionCode="1"
    android:versionName="1.0">
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
    manifest_path = DEMO_PROJECT_DIR / "AndroidManifest.xml"
    manifest_path.write_text(manifest_content)

    # Create dummy resources directory and files
    resources_dir = DEMO_PROJECT_DIR / "res"
    resources_dir.mkdir(parents=True, exist_ok=True)

    # Create mipmap directory and a dummy icon file
    mipmap_dir = resources_dir / "mipmap-hdpi"
    mipmap_dir.mkdir(parents=True, exist_ok=True)
    (mipmap_dir / "ic_launcher.png").touch() # Placeholder for icon

    # Create values directory and strings.xml
    values_dir = resources_dir / "values"
    values_dir.mkdir(parents=True, exist_ok=True)
    strings_content = """
<resources>
    <string name="app_name">My Arabic App</string>
</resources>
"""
    (values_dir / "strings.xml").write_text(strings_content)

    # Create dummy source directory (no actual Java code for this simplified example)
    source_dir = DEMO_PROJECT_DIR / "src" / "main" / "java" / "com" / "example" / "myapp"
    source_dir.mkdir(parents=True, exist_ok=True)
    # (source_dir / "MainActivity.java").touch() # Placeholder if we were compiling Java

    try:
        apk_compiler = ApkCompilerLobe(project_root=DEMO_PROJECT_DIR, output_dir=DEMO_OUTPUT_DIR)
        generated_apk_path = apk_compiler.compile_apk(
            manifest_path=manifest_path,
            resource_dir=resources_dir,
            source_dir=source_dir, # This is not used in the simplified compile, but good for structure
            output_apk_name="my_arabic_app"
        )
        print(f"\nDemo APK generated at: {generated_apk_path}")

    except EnvironmentError as e:
        print(f"Setup Error: {e}")
        print("Please ensure Android SDK is installed and ANDROID_SDK_ROOT is set correctly.")
    except FileNotFoundError as e:
        print(f"Build Tools Error: {e}")
        print("Please ensure you have installed Android build-tools via the SDK Manager.")
    except Exception as e:
        print(f"An unexpected error occurred during APK compilation: {e}")

    finally:
        # Clean up dummy project
        if DEMO_PROJECT_DIR.exists():
            print(f"\nRemoving dummy project directory: {DEMO_PROJECT_DIR}")
            shutil.rmtree(DEMO_PROJECT_DIR)
        # Keep generated APKs for inspection

        print("\n--- Android APK Compiler Lobe Demo Finished ---")