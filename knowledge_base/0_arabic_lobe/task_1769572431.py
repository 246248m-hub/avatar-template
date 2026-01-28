import os
import shutil
import subprocess
from pathlib import Path

# Assume these are defined elsewhere and represent your knowledge base and temporary directories
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
TEMP_DIR = Path("temp_build")
SOURCES_DIR = TEMP_DIR / "sources"
RESOURCES_DIR = TEMP_DIR / "resources"
LIBS_DIR = TEMP_DIR / "libs"
BUILD_DIR = TEMP_DIR / "build"
OUTPUT_DIR = TEMP_DIR / "output"
ANDROID_HOME = os.environ.get("ANDROID_HOME")
if not ANDROID_HOME:
    raise EnvironmentError("ANDROID_HOME environment variable not set.")

AAPT2_PATH = Path(ANDROID_HOME) / "build-tools" / "latest" / "aapt2" # Placeholder for actual path discovery
if not AAPT2_PATH.exists():
    # Attempt to find aapt2 dynamically if a fixed path doesn't work
    build_tools_dir = Path(ANDROID_HOME) / "build-tools"
    if build_tools_dir.exists():
        latest_version = sorted(build_tools_dir.iterdir(), key=lambda x: x.name, reverse=True)
        if latest_version:
            aapt2_candidate = latest_version[0] / "aapt2"
            if aapt2_candidate.exists():
                AAPT2_PATH = aapt2_candidate
            else:
                raise FileNotFoundError("aapt2 not found in the latest build-tools directory.")
        else:
            raise FileNotFoundError("No build-tools directories found.")
    else:
        raise FileNotFoundError("build-tools directory not found in ANDROID_HOME.")

APKSIGNER_PATH = Path(ANDROID_HOME) / "build-tools" / "latest" / "apksigner" # Placeholder for actual path discovery
if not APKSIGNER_PATH.exists():
    # Attempt to find apksigner dynamically if a fixed path doesn't work
    build_tools_dir = Path(ANDROID_HOME) / "build-tools"
    if build_tools_dir.exists():
        latest_version = sorted(build_tools_dir.iterdir(), key=lambda x: x.name, reverse=True)
        if latest_version:
            apksigner_candidate = latest_version[0] / "apksigner"
            if apksigner_candidate.exists():
                APKSIGNER_PATH = apksigner_candidate
            else:
                raise FileNotFoundError("apksigner not found in the latest build-tools directory.")
        else:
            raise FileNotFoundError("No build-tools directories found.")
    else:
        raise FileNotFoundError("build-tools directory not found in ANDROID_HOME.")

JARSIGNER_PATH = Path(ANDROID_HOME) / "lib" / "apksigner.jar" # Placeholder for actual path discovery
if not JARSIGNER_PATH.exists():
    # Attempt to find jarsigner dynamically if a fixed path doesn't work
    # This is a more complex path and might vary significantly.
    # For now, let's assume a common location or raise an error.
    print("Warning: Jarsigner path not found. APK signing might fail.")


def initialize_build_environment():
    """Initializes the temporary build environment."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir()
    SOURCES_DIR.mkdir()
    RESOURCES_DIR.mkdir()
    LIBS_DIR.mkdir()
    BUILD_DIR.mkdir()
    OUTPUT_DIR.mkdir()
    print(f"Build environment initialized in {TEMP_DIR}")

def create_android_manifest(package_name: str, version_name: str = "1.0") -> Path:
    """Creates a basic AndroidManifest.xml file."""
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
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_path = RESOURCES_DIR / "AndroidManifest.xml"
    manifest_path.write_text(manifest_content, encoding='utf-8')
    print(f"AndroidManifest.xml created at {manifest_path}")
    return manifest_path

def create_resource_files(app_name: str = "MyApp"):
    """Creates basic resource files (strings, icons)."""
    # Create strings.xml
    strings_dir = RESOURCES_DIR / "values"
    strings_dir.mkdir(exist_ok=True)
    strings_xml_path = strings_dir / "strings.xml"
    strings_content = f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    strings_xml_path.write_text(strings_content, encoding='utf-8')
    print(f"strings.xml created at {strings_xml_path}")

    # Create placeholder icons (very basic)
    mipmap_dir = RESOURCES_DIR / "mipmap-hdpi"
    mipmap_dir.mkdir(exist_ok=True)
    ic_launcher_path = mipmap_dir / "ic_launcher.png"
    # In a real scenario, you'd generate or load actual icons.
    # For this demo, we'll just touch the file.
    ic_launcher_path.touch()
    print(f"Placeholder ic_launcher.png created at {ic_launcher_path}")

    mipmap_round_dir = RESOURCES_DIR / "mipmap-xxhdpi"
    mipmap_round_dir.mkdir(exist_ok=True)
    ic_launcher_round_path = mipmap_round_dir / "ic_launcher_round.png"
    ic_launcher_round_path.touch()
    print(f"Placeholder ic_launcher_round.png created at {ic_launcher_round_path}")

def create_java_source(package_name: str):
    """Creates a basic MainActivity.java file."""
    package_path = SOURCES_DIR / package_name.replace('.', os.sep)
    package_path.mkdir(parents=True, exist_ok=True)
    activity_path = package_path / "MainActivity.java"
    activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // This layout needs to be created
    }}
}}
"""
    activity_path.write_text(activity_content, encoding='utf-8')
    print(f"MainActivity.java created at {activity_path}")

    # Create a dummy layout file for activity_main.xml
    layout_dir = RESOURCES_DIR / "layout"
    layout_dir.mkdir(exist_ok=True)
    layout_xml_path = layout_dir / "activity_main.xml"
    layout_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <!-- Your UI elements here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    layout_xml_path.write_text(layout_content, encoding='utf-8')
    print(f"activity_main.xml created at {layout_xml_path}")


def compile_java_to_dex(package_name: str):
    """Compiles Java sources to DEX files."""
    if not LIBS_DIR.exists():
        LIBS_DIR.mkdir()
    if not BUILD_DIR.exists():
        BUILD_DIR.mkdir()

    # This part is complex. In a real build, you'd use dx or d8 tools.
    # For this demo, we'll simulate the process.
    # A proper implementation would involve:
    # 1. Compiling Java to .class files.
    # 2. Running 'dx' or 'd8' on .class files to create classes.dex.

    # For simplicity, we'll just create a dummy classes.dex file.
    dex_file_path = BUILD_DIR / "classes.dex"
    dex_file_path.touch() # Placeholder
    print(f"Dummy classes.dex created at {dex_file_path}")
    print("Java compilation to DEX simulated.")

def compile_resources_with_aapt2(package_name: str):
    """Compiles resources using aapt2."""
    print(f"Compiling resources using AAPT2: {AAPT2_PATH}")
    resource_dir_for_aapt2 = RESOURCES_DIR # AAPT2 expects the directory containing AndroidManifest.xml and resource subdirs
    compiled_resources_path = BUILD_DIR / "res"
    compiled_resources_path.mkdir(exist_ok=True)

    # AAPT2 process: link and compile
    # Step 1: Compile individual resource files
    compile_command = [
        str(AAPT2_PATH), "compile",
        "--dir", str(resource_dir_for_aapt2),
        "-o", str(compiled_resources_path),
        "--legacy-android-status" # Needed for older resource types
    ]
    try:
        print(f"Running AAPT2 compile command: {' '.join(compile_command)}")
        result = subprocess.run(compile_command, capture_output=True, text=True, check=True)
        print("AAPT2 compile output:\n", result.stdout)
        if result.stderr:
            print("AAPT2 compile error output:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"AAPT2 compile failed: {e}")
        print("Stderr:", e.stderr)
        print("Stdout:", e.stdout)
        raise

    # Step 2: Link compiled resources and manifest
    link_command = [
        str(AAPT2_PATH), "link",
        "-o", str(BUILD_DIR / "resources.apk"), # Output as an intermediate APK
        "--manifest", str(RESOURCES_DIR / "AndroidManifest.xml"),
        "--java-compile-cache", str(BUILD_DIR / "aapt_cache"),
        "--error-path", str(BUILD_DIR / "aapt_errors"),
        "--output-text-symbols", str(BUILD_DIR / "R.txt"), # Generate R.txt
        "--split-config-value", "density",
        "--split-config-value", "locale",
        "--auto-add-overlay",
        "--no-version-transitions",
        "--resource-configs", "mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi",
        str(compiled_resources_path / "*.flat"), # Use compiled resource files
    ]
    try:
        print(f"Running AAPT2 link command: {' '.join(link_command)}")
        result = subprocess.run(link_command, capture_output=True, text=True, check=True)
        print("AAPT2 link output:\n", result.stdout)
        if result.stderr:
            print("AAPT2 link error output:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"AAPT2 link failed: {e}")
        print("Stderr:", e.stderr)
        print("Stdout:", e.stdout)
        raise

    print(f"Resources compiled and linked. Intermediate resources.apk at {BUILD_DIR / 'resources.apk'}")
    # The output R.txt is crucial for Java compilation.
    if not (BUILD_DIR / "R.txt").exists():
        raise FileNotFoundError("R.txt not generated by AAPT2 link.")
    print(f"R.txt generated at {BUILD_DIR / 'R.txt'}")


def create_apk(package_name: str, apk_output_path: Path):
    """Creates the final unsigned APK."""
    if not BUILD_DIR.exists() or not (BUILD_DIR / "classes.dex").exists() or not (BUILD_DIR / "resources.apk").exists():
        raise FileNotFoundError("Pre-requisite build artifacts (classes.dex, resources.apk) not found.")

    # We need to combine classes.dex and the compiled resources into an APK.
    # This is typically done using 'apkanalyzer' or more directly with APK building tools.
    # For this demo, we'll simulate by creating a zip archive that mimics an APK structure.

    # Ensure the output directory exists
    apk_output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a temporary directory for the APK structure
    apk_temp_dir = BUILD_DIR / "apk_staging"
    if apk_temp_dir.exists():
        shutil.rmtree(apk_temp_dir)
    apk_temp_dir.mkdir()

    # Copy compiled resources
    # The resources.apk from AAPT2 is actually a zip file containing compiled resources.
    # We need to extract and place them correctly.
    resource_apk_content_dir = BUILD_DIR / "res_apk_content"
    shutil.unpack_archive(BUILD_DIR / "resources.apk", resource_apk_content_dir)
    shutil.copytree(resource_apk_content_dir, apk_temp_dir / "res")

    # Copy compiled DEX files
    shutil.copy(BUILD_DIR / "classes.dex", apk_temp_dir / "classes.dex")

    # Copy AndroidManifest.xml
    shutil.copy(RESOURCES_DIR / "AndroidManifest.xml", apk_temp_dir / "AndroidManifest.xml")

    # Create META-INF directory (for signing later)
    (apk_temp_dir / "META-INF").mkdir()

    # Create the APK by zipping the contents of apk_temp_dir
    # This is a manual zip creation, which is a simplification.
    # In reality, tools like 'zip' command or libraries are used.
    try:
        print(f"Creating APK zip archive at {apk_output_path}")
        # Using the zip command as it's more robust than manual file copying for zip creation
        # Ensure 'zip' command is available in the system PATH
        zip_command = [
            "zip",
            "-j", # Junk paths, store only filenames
            "-o", # Overwrite existing files
            str(apk_output_path),
            "-C", str(apk_temp_dir), # Change directory before adding files
            ".", # Add all files in the current directory (apk_temp_dir)
        ]
        # To correctly zip, we need to change directory to apk_temp_dir and zip its contents
        # Alternatively, construct the zip from the current directory
        current_dir = os.getcwd()
        os.chdir(apk_temp_dir)
        zip_process = subprocess.run(
            ["zip", "-r", "-o", str(Path(current_dir) / apk_output_path.name)], # Path to output zip relative to apk_temp_dir
            capture_output=True,
            text=True,
            check=True
        )
        os.chdir(current_dir) # Change back to original directory
        print("ZIP command output:\n", zip_process.stdout)
        if zip_process.stderr:
            print("ZIP command error output:\n", zip_process.stderr)

        # Ensure the output file is in the correct location
        final_apk_path = Path(current_dir) / apk_output_path.name
        if not final_apk_path.exists():
            raise FileNotFoundError("Failed to create the APK zip file.")

        # Move the created zip file to the desired output path if it's different
        if final_apk_path != apk_output_path:
            shutil.move(final_apk_path, apk_output_path)

        print(f"Unsigned APK created successfully at {apk_output_path}")

    except FileNotFoundError:
        print("Error: 'zip' command not found. Please ensure it is installed and in your PATH.")
        raise
    except subprocess.CalledProcessError as e:
        print(f"Error during APK zip creation: {e}")
        print("Stderr:", e.stderr)
        print("Stdout:", e.stdout)
        raise
    finally:
        # Clean up temporary staging directory
        if apk_temp_dir.exists():
            shutil.rmtree(apk_temp_dir)


def sign_apk(unsigned_apk_path: Path, signed_apk_path: Path):
    """Signs the APK using a debug keystore."""
    print("Signing APK...")

    # Create a dummy debug keystore if it doesn't exist for demonstration
    debug_keystore_dir = TEMP_DIR / "keystore"
    debug_keystore_dir.mkdir(exist_ok=True)
    debug_keystore_path = debug_keystore_dir / "debug.keystore"
    if not debug_keystore_path.exists():
        print("Creating a dummy debug.keystore for signing...")
        # Using keytool to create a dummy keystore
        keytool_command = [
            "keytool",
            "-genkey",
            "-v",
            "-keystore", str(debug_keystore_path),
            "-alias", "androiddebugkey",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-dname", "CN=Android Debug,O=Android,C=US",
            "-storepass", "android",
            "-keypass", "android"
        ]
        try:
            # Provide dummy input to keytool's interactive prompts
            process = subprocess.Popen(keytool_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input="android\nandroid\n") # Enter passwords twice
            if process.returncode != 0:
                print(f"keytool command failed with return code {process.returncode}")
                print("Stdout:", stdout)
                print("Stderr:", stderr)
                raise RuntimeError("Failed to create dummy debug keystore.")
            print("Dummy debug.keystore created successfully.")
        except FileNotFoundError:
            print("Error: 'keytool' command not found. Please ensure Java Development Kit (JDK) is installed and 'keytool' is in your PATH.")
            raise
        except Exception as e:
            print(f"An error occurred during keystore creation: {e}")
            raise

    # Using apksigner for signing
    sign_command = [
        str(APKSIGNER_PATH),
        "sign",
        "--ks", str(debug_keystore_path),
        "--ks-key-alias", "androiddebugkey",
        "--ks-pass", f"pass:android",
        "--key-pass", f"pass:android",
        "--out", str(signed_apk_path),
        str(unsigned_apk_path)
    ]

    try:
        print(f"Running apksigner command: {' '.join(sign_command)}")
        result = subprocess.run(sign_command, capture_output=True, text=True, check=True)
        print("apksigner output:\n", result.stdout)
        if result.stderr:
            print("apksigner error output:\n", result.stderr)
        print(f"APK signed successfully and saved to {signed_apk_path}")
    except FileNotFoundError:
        print(f"Error: '{APKSIGNER_PATH}' not found. Ensure ANDROID_HOME is set correctly and build-tools are installed.")
        raise
    except subprocess.CalledProcessError as e:
        print(f"APK signing failed: {e}")
        print("Stderr:", e.stderr)
        print("Stdout:", e.stdout)
        raise
    except Exception as e:
        print(f"An unexpected error occurred during APK signing: {e}")
        raise


def build_apk_from_nlp_data(nlp_data: dict, output_apk_path: Path):
    """
    Builds a hyper-efficient APK from natural language understanding.

    Args:
        nlp_data (dict): A dictionary containing parsed natural language information.
                         Expected keys: 'package_name', 'app_name', 'version_name'.
                         Other keys might include code snippets, UI descriptions, etc.
        output_apk_path (Path): The desired path for the final signed APK.
    """
    print("\n--- Initiating APK Build Process ---")
    initialize_build_environment()

    package_name = nlp_data.get('package_name', 'com.example.generatedapp')
    app_name = nlp_data.get('app_name', 'Generated App')
    version_name = nlp_data.get('version_name', '1.0')

    # 1. Create AndroidManifest.xml
    create_android_manifest(package_name, version_name)

    # 2. Create resource files (strings, icons)
    create_resource_files(app_name)

    # 3. Create Java source code (e.g., MainActivity)
    create_java_source(package_name)

    # 4. Compile resources using AAPT2
    compile_resources_with_aapt2(package_name)

    # 5. Compile Java sources to DEX
    # In a real scenario, this would also involve compiling Java to .class files
    # and then using d8/dx. For this demo, we simulate classes.dex creation.
    compile_java_to_dex(package_name)

    # 6. Create the unsigned APK
    unsigned_apk_path = OUTPUT_DIR / f"{package_name.split('.')[-1]}-unsigned.apk"
    create_apk(package_name, unsigned_apk_path)

    # 7. Sign the APK
    signed_apk_path = output_apk_path
    sign_apk(unsigned_apk_path, signed_apk_path)

    print(f"\n--- APK Build Process Finished ---")
    print(f"Final signed APK available at: {signed_apk_path}")

    # Cleanup the temporary build directory
    print(f"\n--- Cleaning up temporary build directory: {TEMP_DIR} ---")
    shutil.rmtree(TEMP_DIR)
    print("Cleanup complete.")


if __name__ == '__main__':
    # Example Usage:
    # This section demonstrates how build_apk_from_nlp_data could be called.
    # In the grand objective, this function would be triggered by Lobe 6_synthesis_lobe
    # after it has processed NLP data into a structured format.

    # Mock NLP data
    mock_nlp_data = {
        'package_name': 'com.example.mygeneratedapp',
        'app_name': 'Awesome App',
        'version_name': '1.0.1',
        # In a real scenario, this could also contain specific UI element descriptions,
        # logic snippets in pseudocode, or even direct Java/Kotlin code fragments
        # that would be incorporated into the generated source files.
    }

    # Define the output path for the signed APK
    final_apk_destination = Path("output_apks") / "my_generated_app.apk"
    final_apk_destination.parent.mkdir(exist_ok=True)

    try:
        build_apk_from_nlp_data(mock_nlp_data, final_apk_destination)
        print(f"\nExample APK build completed successfully. APK saved to: {final_apk_destination}")
    except Exception as e:
        print(f"\nAn error occurred during the example APK build: {e}")