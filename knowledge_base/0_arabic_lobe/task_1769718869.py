import os
import shutil
import subprocess
from pathlib import Path

# --- Configuration ---
TEMP_DIR = Path("./temp_arabic_project")
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

BUILD_TOOLS_DIR = Path(ANDROID_SDK_ROOT) / "build-tools"
# Find the latest build-tools version
try:
    BUILD_TOOLS_VERSION = max(
        [
            d.name
            for d in BUILD_TOOLS_DIR.iterdir()
            if d.is_dir() and d.name.replace(".", "").isdigit()
        ]
    )
    AAPT_PATH = BUILD_TOOLS_DIR / BUILD_TOOLS_VERSION / "aapt"
    AAPT2_PATH = BUILD_TOOLS_DIR / BUILD_TOOLS_VERSION / "aapt2"
except ValueError:
    raise FileNotFoundError(
        "No Android build-tools found. Please install them via Android Studio SDK Manager."
    )

if not AAPT_PATH.exists() and not AAPT2_PATH.exists():
    raise FileNotFoundError(
        f"aapt or aapt2 not found in {BUILD_TOOLS_DIR / BUILD_TOOLS_VERSION}. "
        "Ensure build-tools are correctly installed."
    )
AAPT_CMD = str(AAPT2_PATH) if AAPT2_PATH.exists() else str(AAPT_PATH)

# --- Helper Functions ---
def create_dummy_android_project(project_root: Path):
    """Creates a minimal Android project structure."""
    project_root.mkdir(parents=True, exist_ok=True)
    manifest_path = project_root / "AndroidManifest.xml"
    src_path = project_root / "src"
    src_path.mkdir(exist_ok=True)
    res_path = project_root / "res"
    res_path.mkdir(exist_ok=True)
    res_values_path = res_path / "values"
    res_values_path.mkdir(exist_ok=True)

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(
            """<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.arabicapp">
    <application android:label="Arabic App" android:icon="@drawable/app_icon">
    </application>
</manifest>"""
        )

    # Create a dummy app icon
    icon_path = res_path / "drawable" / "app_icon.png"
    icon_path.parent.mkdir(exist_ok=True)
    # Create a blank 1x1 PNG file (a simple way to have a valid image)
    with open(icon_path, "wb") as f:
        f.write(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\x93\x00\x00\x00\x04sBIT\x08\xb1\x8f\x86\x00\x00\x00\x02rG?B\x00\x00\x00\nIDATx\x9cc\xfc\xff\xff?\x03\x00\x08\xfb\x02\xfe\xa7\x98\x03\x00\x00\x00\x00IEND\xaeB`\x82"
        )


    with open(res_values_path / "strings.xml", "w", encoding="utf-8") as f:
        f.write(
            """<resources>
    <string name="app_name">Arabic App</string>
</resources>"""
        )

    print(f"Dummy Android project created at: {project_root}")

def generate_arabic_resource_file(project_root: Path, text_content: str):
    """Generates an Arabic string resource file."""
    res_values_path = project_root / "res" / "values"
    res_values_path.mkdir(parents=True, exist_ok=True)
    strings_xml_path = res_values_path / "arabic_strings.xml"
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(f"<resources><string name=\"arabic_greeting\">{text_content}</string></resources>")
    print(f"Arabic strings resource created: {strings_xml_path}")
    return strings_xml_path

def compile_resources_with_aapt(project_root: Path, output_dir: Path):
    """Compiles Android resources using AAPT/AAPT2."""
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Compiling resources for project: {project_root}")
    command = [
        AAPT_CMD,
        "crunch",
        "-S",
        str(project_root / "res"),
        "-o",
        str(output_dir),
        "--auto-add-overlay",
        "--no-crunch-images"
    ]

    # AAPT2 specific flags might be needed if using AAPT2 and it complains
    if AAPT_CMD.endswith("aapt2"):
        command.extend(["--legacy-android"]) # Often helpful for compatibility

    try:
        # Run AAPT to compile resources. This typically creates an 'resources.ap_' file.
        # For modern AAPT2, it's more about asset packing.
        # This part is simplified as AAPT's direct output for resource compilation varies.
        # The goal is to have processed resources ready for packaging.
        # A more robust approach might involve using Gradle or a dedicated Android build tool.

        # For simplicity, we'll simulate the output by creating a placeholder and
        # assuming AAPT does its job of processing R.java etc. in a real build.
        # In a real scenario, AAPT would generate compiled resources and potentially R.java.
        # We are focusing on the *intent* of resource compilation here for the Arabic strings.

        # If AAPT2 is used, it typically generates intermediate files that are then
        # used by other tools. The 'crunch' command focuses on optimizing images.
        # For generating the resource table, a compile step is usually involved.
        # A simplified AAPT2 compilation might look like this (though this is more for libraries):
        # aapt2 compile -o compiled_resources.zip res
        # aapt2 link -o resources.ap_ --manifest AndroidManifest.xml compiled_resources.zip

        # Given the constraint of *raw* Python code without external build systems,
        # we'll assume the objective is to have the Arabic strings integrated.
        # The most direct AAPT command that relates to resource processing for APKs
        # is often part of a larger build process.
        # Let's try a command that might process resources and manifest.

        # AAPT2 compile command for resources:
        compiled_resources_path = output_dir / "compiled_resources.zip"
        compile_cmd = [AAPT_CMD, "compile", "-o", str(compiled_resources_path), str(project_root / "res")]
        if AAPT_CMD.endswith("aapt2"):
             subprocess.run(compile_cmd, check=True, cwd=project_root, capture_output=True, text=True)

        # AAPT2 link command (combines compiled resources and manifest):
        linked_resources_path = output_dir / "resources.ap_"
        link_cmd = [
            AAPT_CMD, "link",
            "-o", str(linked_resources_path),
            "--manifest", str(project_root / "AndroidManifest.xml"),
            str(compiled_resources_path)
        ]
        if AAPT_CMD.endswith("aapt2"):
            subprocess.run(link_cmd, check=True, cwd=project_root, capture_output=True, text=True)
        else: # For older AAPT
            # Older AAPT's 'crunch' or direct manifest processing might be used,
            # but linking is more complex and usually involves generating R.java.
            # We'll simulate a minimal successful processing.
            print("Using older AAPT. Resource linking simulation...")
            # In a real scenario, AAPT would generate R.java and compiled resources.
            # For this demo, we'll just create a placeholder for the compiled resources.
            with open(output_dir / "resources.ap_", "w") as f:
                f.write("Simulated compiled resources")


        print(f"Resources compiled successfully. Output: {output_dir}")
        return output_dir / "resources.ap_"

    except subprocess.CalledProcessError as e:
        print(f"Resource compilation failed: {e}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        raise

class ArabicAPKCompiler:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.processed_resources_dir = project_root / "processed_res"
        self.apk_output_dir = project_root / "apk_output"
        self.apk_output_dir.mkdir(parents=True, exist_ok=True)
        self.processed_resources_dir.mkdir(parents=True, exist_ok=True)

    def process_arabic_strings(self, natural_language_arabic_string: str) -> Path:
        """
        Generates an Android XML resource file containing the Arabic string.
        This simulates integrating natural language directly into resources.
        """
        print(f"Processing Arabic string: '{natural_language_arabic_string}'")
        resource_file_path = generate_arabic_resource_file(self.project_root, natural_language_arabic_string)
        return resource_file_path

    def compile_android_resources(self) -> Path:
        """
        Uses AAPT/AAPT2 to compile the Android resources, including the generated Arabic strings.
        Returns the path to the compiled resource archive.
        """
        print("Compiling Android resources with AAPT/AAPT2...")
        try:
            compiled_resource_archive = compile_resources_with_aapt(
                self.project_root, self.processed_resources_dir
            )
            return compiled_resource_archive
        except Exception as e:
            print(f"Error during resource compilation: {e}")
            raise

    def build_apk(self, compiled_resource_archive: Path) -> Path:
        """
        Simulates the final APK building step.
        In a real scenario, this would involve dx/d8 for code, packaging, and signing.
        Here, we will package the manifest and the compiled resources into a basic APK file.
        This is a highly simplified representation.
        """
        print("Building APK (simplified)...")
        apk_path = self.apk_output_dir / "ArabicApp.apk"

        # This is a placeholder. A real APK build involves:
        # 1. Compiling Java/Kotlin code to .dex files.
        # 2. Packaging compiled resources, assets, and .dex files into an unsigned APK.
        # 3. Signing the APK.

        # For this demo, we'll create a dummy APK file that contains the manifest and resources.
        # We'll use 'zip' command as a stand-in for APK packaging.
        try:
            # Ensure manifest is accessible
            manifest_path = self.project_root / "AndroidManifest.xml"
            if not manifest_path.exists():
                raise FileNotFoundError("AndroidManifest.xml not found.")

            # Create a temporary directory to stage APK contents
            staging_dir = self.project_root / "apk_staging"
            staging_dir.mkdir(exist_ok=True)

            # Copy processed resources
            # AAPT/AAPT2 output is usually in 'resources.ap_' which is a zip file.
            # We need to extract or directly use its contents.
            # For simplicity, we'll assume resources.ap_ contains processed resource files directly.
            # In reality, it's a binary blob.

            # A more realistic simulation would involve `aapt package` for older AAPT
            # or using `aapt2 link` to create the resources.ap_ and then adding it.
            # For modern SDKs, this is handled by Gradle.

            # Let's simulate by just packaging the manifest and a dummy resource file.
            # If compiled_resource_archive is resources.ap_, we can treat it as a package.
            # However, creating a valid zip for APK requires specific structure.

            # A pragmatic approach for this demo:
            # Use the manifest and the compiled resource archive (if it's a zip)
            # Or, simulate creating an APK from scratch using zip.

            # Let's create a simple zip file as a placeholder for the APK.
            # This zip will contain the manifest.

            # Create a dummy file to represent compiled classes (like classes.dex)
            dummy_dex_path = staging_dir / "classes.dex"
            with open(dummy_dex_path, "w") as f:
                f.write("Dummy DEX content")

            # Copy manifest
            shutil.copy(manifest_path, staging_dir / "AndroidManifest.xml")

            # If compiled_resource_archive is a valid zip (e.g., resources.ap_ from AAPT2),
            # we might want to extract its contents.
            # For older AAPT, it generates an R.java and a binary resource table.
            # Let's assume resources.ap_ is a ZIP archive for simplicity.
            if compiled_resource_archive.suffix == ".ap_" and compiled_resource_archive.exists():
                 # Extract contents of resources.ap_ into staging_dir/res
                res_output_path = staging_dir / "res"
                res_output_path.mkdir(exist_ok=True)
                with subprocess.Popen(["unzip", "-q", str(compiled_resource_archive), "-d", str(res_output_path)]) as proc:
                    proc.wait()
                if proc.returncode != 0:
                    print(f"Warning: Failed to extract {compiled_resource_archive}. APK might be incomplete.")


            # Create the APK using zip command
            # This command creates an unsigned APK.
            # The order of files in the zip can matter for some tools, but for a basic APK,
            # manifest, classes.dex, and res/ are common top-level items.
            zip_command = ["zip", "-j", "-o", str(apk_path)] # -j = junk paths, -o = overwrite
            files_to_zip = [
                staging_dir / "AndroidManifest.xml",
                dummy_dex_path
            ]
            if (staging_dir / "res").exists():
                 # Add all contents of the staging_dir/res directory recursively
                 for root, _, files in os.walk(staging_dir / "res"):
                    for file in files:
                        filepath = Path(root) / file
                        # Add path relative to staging_dir
                        relative_path = filepath.relative_to(staging_dir)
                        files_to_zip.append((filepath, relative_path))


            # Execute zip command with files
            final_zip_command = ["zip", "-j", "-o", str(apk_path)]
            for item in files_to_zip:
                if isinstance(item, tuple): # Handle paths with relative paths for zip
                    filepath, relative_path = item
                    final_zip_command.extend([f"{filepath}", f"{relative_path}"])
                else:
                    final_zip_command.append(str(item))

            # We need to ensure the files are added correctly to the zip archive.
            # The `zip` command syntax for adding specific files with new paths is tricky.
            # A common way is to `cd` into the directory.
            current_dir = os.getcwd()
            os.chdir(staging_dir)
            zip_command_cd = ["zip", "-j", "-o", str(apk_path.relative_to(staging_dir))] # relative path for output file
            zip_command_cd.extend([
                "AndroidManifest.xml",
                "classes.dex"
            ])
            if (Path("res")).exists():
                zip_command_cd.extend(["res/*"]) # Add contents of res directory

            subprocess.run(zip_command_cd, check=True, capture_output=True, text=True)
            os.chdir(current_dir) # Return to original directory

            print(f"APK built successfully (unsigned): {apk_path}")
            return apk_path

        except FileNotFoundError as e:
            print(f"Error during APK build: File not found - {e}")
            raise
        except subprocess.CalledProcessError as e:
            print(f"Error during APK build: Subprocess failed.")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            raise
        finally:
            # Clean up staging directory
            if staging_dir.exists():
                shutil.rmtree(staging_dir)


# --- Main Execution Logic ---
if __name__ == "__main__":
    print("--- Arabic APK Compiler Module Demo ---")

    # Define a natural language Arabic phrase
    arabic_phrase = "مرحبا بالعالم" # "Hello World" in Arabic

    # --- Step 1: Create a dummy Android project ---
    try:
        create_dummy_android_project(TEMP_DIR)
    except Exception as e:
        print(f"Failed to create dummy project: {e}")
        exit(1)

    # --- Step 2: Initialize the ArabicAPKCompiler ---
    try:
        apk_compiler = ArabicAPKCompiler(TEMP_DIR)
    except EnvironmentError as e:
        print(f"Configuration error: {e}")
        print("Please ensure ANDROID_SDK_ROOT is set and build-tools are installed.")
        exit(1)
    except FileNotFoundError as e:
        print(f"Build tool not found: {e}")
        print("Please ensure Android SDK build-tools are installed via Android Studio SDK Manager.")
        exit(1)


    # --- Step 3: Process the Arabic string and generate resources ---
    try:
        generated_resource_file = apk_compiler.process_arabic_strings(arabic_phrase)
        print(f"Generated Arabic resource file: {generated_resource_file}")
    except Exception as e:
        print(f"Failed to process Arabic strings: {e}")
        # Clean up dummy project
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
        exit(1)

    # --- Step 4: Compile Android resources ---
    compiled_resource_archive = None
    try:
        compiled_resource_archive = apk_compiler.compile_android_resources()
        print(f"Compiled resource archive: {compiled_resource_archive}")
    except Exception as e:
        print(f"Failed to compile Android resources: {e}")
        # Clean up dummy project
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
        exit(1)

    # --- Step 5: Build the APK ---
    final_apk_path = None
    try:
        final_apk_path = apk_compiler.build_apk(compiled_resource_archive)
        print(f"Final APK generated at: {final_apk_path}")
    except Exception as e:
        print(f"Failed to build APK: {e}")
        # Clean up dummy project
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
        exit(1)

    print("\n--- Arabic APK Compiler Module Demo Finished ---")

    # Clean up the dummy project
    if TEMP_DIR.exists():
        print(f"Removing dummy project directory: {TEMP_DIR}")
        shutil.rmtree(TEMP_DIR)