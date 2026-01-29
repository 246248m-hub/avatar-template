import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any

# Assuming these are defined elsewhere or will be defined in other lobes
# For demonstration purposes, defining them here.
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    # This is a placeholder. In a real scenario, this would be handled robustly.
    # For the purpose of this module, we'll assume it's set or a dummy path is used.
    print("Warning: ANDROID_SDK_ROOT is not set. Using a placeholder.")
    ANDROID_SDK_ROOT = Path("/tmp/dummy_android_sdk")
    os.makedirs(ANDROID_SDK_ROOT, exist_ok=True)
    # Create dummy SDK components if they don't exist to avoid immediate errors
    os.makedirs(ANDROID_SDK_ROOT / "build-tools", exist_ok=True)
    os.makedirs(ANDROID_SDK_ROOT / "platforms", exist_ok=True)
    os.makedirs(ANDROID_SDK_ROOT / "cmdline-tools", exist_ok=True)


class ArabicAPKBuilder:
    """
    A module designed to take Arabic natural language descriptions
    and generate hyper-efficient APKs. This is a simplified representation.
    """

    def __init__(self, sdk_root: str):
        self.sdk_root = sdk_root
        self.platform_tools = Path(sdk_root) / "platform-tools"
        self.build_tools_dir = self._get_latest_build_tools()
        self.android_jar = self._find_android_jar()

        if not self.build_tools_dir:
            raise EnvironmentError("Android build tools not found. Ensure ANDROID_SDK_ROOT is set and has build-tools installed.")
        if not self.android_jar:
            raise EnvironmentError("android.jar not found. Ensure ANDROID_SDK_ROOT is set and has platform installed.")

    def _get_latest_build_tools(self) -> Path | None:
        """Finds the latest installed Android build tools version."""
        build_tools_path = Path(self.sdk_root) / "build-tools"
        if not build_tools_path.exists():
            return None
        versions = sorted([d for d in build_tools_path.iterdir() if d.is_dir()], key=lambda x: x.name, reverse=True)
        return versions[0] if versions else None

    def _find_android_jar(self) -> Path | None:
        """Finds the android.jar for a common API level (e.g., 30)."""
        # This is a simplified search. A real system might need to be more robust
        # about finding the correct API level based on project requirements.
        platforms_path = Path(self.sdk_root) / "platforms"
        if not platforms_path.exists():
            return None
        # Look for a common recent API level, e.g., 30
        api_level_path = platforms_path / "android-30"
        if api_level_path.exists():
            android_jar_path = api_level_path / "android.jar"
            if android_jar_path.exists():
                return android_jar_path
        # Fallback to searching all platforms if specific one isn't found
        for platform_dir in sorted([d for d in platforms_path.iterdir() if d.is_dir()], key=lambda x: x.name, reverse=True):
            android_jar_path = platform_dir / "android.jar"
            if android_jar_path.exists():
                return android_jar_path
        return None

    def generate_android_project_structure(self, project_name: str, output_dir: Path) -> Path:
        """
        Generates a basic Android project structure.
        In a real scenario, this would parse Arabic NLP to define activities, layouts, etc.
        """
        project_root = output_dir / project_name
        src_dir = project_root / "src"
        res_dir = project_root / "res"
        manifest_path = project_root / "AndroidManifest.xml"

        project_root.mkdir(parents=True, exist_ok=True)
        src_dir.mkdir(parents=True, exist_ok=True)
        res_dir.mkdir(parents=True, exist_ok=True)

        # Basic AndroidManifest.xml
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{project_name.lower()}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <!-- Add activities here based on NLP -->
    </application>
</manifest>
"""
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Basic strings.xml
        strings_path = res_dir / "values" / "strings.xml"
        strings_path.parent.mkdir(parents=True, exist_ok=True)
        strings_content = """
<resources>
    <string name="app_name">MyArabicApp</string>
</resources>
"""
        with open(strings_path, "w", encoding="utf-8") as f:
            f.write(strings_content)

        # Basic ic_launcher.png (dummy)
        launcher_icon_path = res_dir / "mipmap-hdpi" / "ic_launcher.png"
        launcher_icon_path.parent.mkdir(parents=True, exist_ok=True)
        # Create a tiny dummy PNG file
        with open(launcher_icon_path, "wb") as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\x92\x00\x00\x00\x00IDATx\x9cc\xfc\xff\xff?\x03\x00\x08\xfc\x02\xfe\xa7\x7f0\xea\x00\x00\x00\x00IEND\xaeB`\x82')

        print(f"Generated project structure at: {project_root}")
        return project_root

    def compile_apk(self, project_root: Path, apk_output_path: Path) -> bool:
        """
        Compiles the Android project into an APK using aapt and dx/d8.
        This is a simplified compilation flow.
        """
        print(f"Compiling project at: {project_root}")
        project_name = project_root.name

        # 1. Generate resources and R.java using aapt (or aapt2)
        # We'll use aapt for simplicity here, assuming it's available in build-tools
        aapt_command = [
            str(self.build_tools_dir / "aapt"),
            "package",
            "-f",  # Force overwrite
            "-m",  # Enable manifest merging
            "-J",  # Output R.java to a directory
            str(project_root / "src"),  # Directory for R.java
            "-M", str(project_root / "AndroidManifest.xml"),
            "-S", str(project_root / "res"),
            "-I", str(self.android_jar)
        ]
        print(f"Running aapt: {' '.join(aapt_command)}")
        try:
            subprocess.run(aapt_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"aapt failed with error code {e.returncode}:")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False

        # 2. Compile Java source files to .class files
        # This requires setting up a classpath correctly. For simplicity,
        # we'll assume a single main activity and compile it.
        # A real scenario would compile all Java/Kotlin files in src/.
        java_files = list(project_root.glob("src/**/*.java"))
        if not java_files:
            print("No Java files found to compile.")
            # Create a dummy Java file if none exists, to make compilation proceed
            dummy_java_path = project_root / "src" / "com" / "example" / project_name.lower() / "MainActivity.java"
            dummy_java_path.parent.mkdir(parents=True, exist_ok=True)
            dummy_java_content = f"""
package com.example.{project_name.lower()};

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // setContentView(R.layout.activity_main); // Assuming layout exists
    }}
}}
"""
            with open(dummy_java_path, "w", encoding="utf-8") as f:
                f.write(dummy_java_content)
            java_files = [dummy_java_path]
            print("Created a dummy MainActivity.java for compilation.")


        classes_dir = project_root / "classes"
        classes_dir.mkdir(parents=True, exist_ok=True)

        javac_command = [
            "javac",
            "-d", str(classes_dir),
            "-classpath", str(self.android_jar),
            "-sourcepath", str(project_root / "src"),
        ] + [str(f) for f in java_files]

        print(f"Running javac: {' '.join(javac_command)}")
        try:
            # Need to ensure JAVA_HOME is set for javac to work.
            # For simplicity, assuming it's set in the environment.
            subprocess.run(javac_command, check=True, capture_output=True, text=True)
        except FileNotFoundError:
            print("Error: 'javac' command not found. Ensure JAVA_HOME is set and JDK is in PATH.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"javac failed with error code {e.returncode}:")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False

        # 3. Convert .class files to .dex files using dx or d8
        # d8 is preferred and part of recent build-tools.
        d8_command = [
            str(self.build_tools_dir / "d8"),
            str(classes_dir),
            "--output", str(project_root / "dex")
        ]
        print(f"Running d8: {' '.join(d8_command)}")
        try:
            subprocess.run(d8_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"d8 failed with error code {e.returncode}:")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False

        # 4. Create the APK
        # This typically involves zipalign and then signing.
        # For simplicity, we'll just package the resources and dex files.
        # A full build process uses apksigner for signing.

        # Create an unsigned APK
        apk_dir = project_root / "apk_build"
        apk_dir.mkdir(parents=True, exist_ok=True)

        # Add resources
        res_archive_path = apk_dir / "resources.ap_".replace('_', '') # aapt creates resources.ap_
        aapt2_command = [
            str(self.build_tools_dir / "aapt2"),
            "compile",
            "-o", str(res_archive_path),
            str(project_root / "res")
        ]
        print(f"Running aapt2 compile: {' '.join(aapt2_command)}")
        try:
            subprocess.run(aapt2_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"aapt2 compile failed with error code {e.returncode}:")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False

        # Link resources
        final_res_path = apk_dir / "resources.arsc"
        aapt2_link_command = [
            str(self.build_tools_dir / "aapt2"),
            "link",
            "-o", str(project_root / project_name.lower() + ".apk"), # Directly output to final APK name
            "--manifest", str(project_root / "AndroidManifest.xml"),
            "-R", str(res_archive_path),
            "-I", str(self.android_jar)
        ]
        print(f"Running aapt2 link: {' '.join(aapt2_link_command)}")
        try:
            subprocess.run(aapt2_link_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"aapt2 link failed with error code {e.returncode}:")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return False

        # Adding DEX files to the APK (this part is complex with direct APK manipulation)
        # A simpler approach is to use the `dx` tool (or `d8`) to create classes.dex
        # and then use `apkbuilder` to create the final APK.

        # Using apkbuilder to assemble the APK
        apkbuilder_command = [
            "apkbuilder", # This command is deprecated in favor of apksigner and jarjar, but might exist.
            str(apk_output_path),
            "-v",
            "-u", # Unsigned APK
            "-z", str(project_root / project_name.lower() + ".zip"), # Intermediate zip file
            "-f", str(project_root / project_name.lower() + ".apk"), # Final APK path
            str(project_root / "AndroidManifest.xml"),
            str(project_root / "res"),
            str(project_root / "assets"), # Assuming assets dir might exist
            str(project_root / "libs"),   # Assuming libs dir might exist
            str(project_root / "classes.dex") # This is where dex files are added.
                                             # The output of d8 is a directory, not classes.dex directly.
                                             # This implies a need to package dex files into classes.dex.
        ]
        # Let's re-evaluate: aapt2 link creates the APK directly if all inputs are provided.
        # However, it doesn't include the DEX files.

        # A more common flow involves `dx` (or `d8`) and then `apkbuilder` or `jarjar`.
        # Let's try a flow that uses d8 output and then packages.
        # The output of `d8 --output dir` is typically a `classes.dex` file inside `dir`.
        dex_output_path = project_root / "dex"
        if not (dex_output_path / "classes.dex").exists():
            print("Error: classes.dex not found in output directory.")
            return False

        # We need to bundle the DEX file and resources into the APK.
        # The `aapt2 link` command might not be the best for the final step with DEX.
        # Let's use the older `apkbuilder` if available or simulate the process.
        # Many modern SDKs recommend `apkanalyzer` and `apksigner`.

        # For this example, we'll simulate a simplified APK creation by zipping
        # the contents and renaming to .apk. This bypasses signing and zipaligning.
        # A real process would be:
        # 1. `aapt2 link` -> intermediate .apk without code
        # 2. `d8` -> classes.dex
        # 3. `zipalign` -> aligned .apk
        # 4. `apksigner` -> signed .apk

        # Let's try to use aapt2 to create the APK structure and then add dex.
        # This part is challenging without a full build system.
        # A common toolchain involves:
        # `aapt2 compile` -> .AAPT2
        # `aapt2 link` -> resources.apk (contains resources and manifest)
        # `d8` -> classes.dex
        # `jar` -> create a jar with resources.apk and classes.dex
        # `zipalign` -> align the jar
        # `apksigner` -> sign the aligned jar

        # Given the constraints, let's assume a simplified `apkbuilder` exists or
        # we can construct a basic zip archive.

        # A more direct approach with `aapt2 link` can generate an APK.
        # However, it doesn't inherently embed the DEX files.
        # The standard `gradle` build system handles this complexity.

        # Let's simulate a final APK creation by creating a zip archive of contents.
        # This is NOT a valid APK for installation but demonstrates packaging.
        final_apk_staging_dir = project_root / "apk_staging"
        final_apk_staging_dir.mkdir(parents=True, exist_ok=True)

        # Copy dex files
        dex_dest_dir = final_apk_staging_dir / "dex"
        shutil.copytree(dex_output_path, dex_dest_dir)

        # Copy compiled Java classes (if needed for other tools, but d8 consumes .class)
        # For a simpler APK, we'd copy the contents of `classes_dir`
        # for this simplified model, we rely on the dex files.

        # Copy compiled resources (from aapt2 link output)
        # The output of aapt2 link is usually the APK itself or an intermediate file.
        # If aapt2 link produced an intermediate file, we would extract it.
        # For this simplified version, assume `aapt2 link` created `project_root/project_name.apk`
        # which is a valid zip file containing resources and manifest.

        # We need to merge `classes.dex` into the APK created by `aapt2 link`.
        # This is usually done via `jarjar` or similar tools.

        # Let's simulate by copying the resources.apk and classes.dex into a zip.
        # THIS IS A GROSS SIMPLIFICATION.
        print("Simulating APK creation by creating a zip archive...")
        resource_apk_path = project_root / (project_name.lower() + ".apk") # From aapt2 link
        if not resource_apk_path.exists():
            print(f"Error: Intermediate APK from aapt2 link not found at {resource_apk_path}")
            return False

        # Extract resources from the intermediate APK
        temp_resource_extract = tempfile.mkdtemp()
        with subprocess.Popen(['unzip', str(resource_apk_path), '-d', temp_resource_extract], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            stdout, stderr = proc.communicate()
            if proc.returncode != 0:
                print(f"Failed to unzip intermediate APK: {stderr.decode()}")
                shutil.rmtree(temp_resource_extract)
                return False

        # Create the final APK by adding DEX files to extracted resources
        # This is where tools like `apkbuilder` or `jarjar` would be used.
        # For this demo, we'll create a zip and rename it.
        final_zip_path = project_root / (project_name.lower() + "_unsigned.apk")
        print(f"Creating unsigned APK at: {final_zip_path}")
        with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add resources and manifest from extracted folder
            for root_dir, _, files in os.walk(temp_resource_extract):
                for file in files:
                    file_path = Path(root_dir) / file
                    arcname = file_path.relative_to(temp_resource_extract)
                    zf.write(file_path, arcname)

            # Add DEX files
            for dex_file in (dex_output_path).glob("classes*.dex"):
                zf.write(dex_file, f"classes{str(dex_file.suffix).replace('.dex','')}.dex") # Ensure correct naming

        shutil.rmtree(temp_resource_extract)
        shutil.move(final_zip_path, apk_output_path)
        print(f"Successfully created unsigned APK at: {apk_output_path}")

        # In a real scenario, the following steps would occur:
        # 1. zipalign (using the SDK's zipalign tool)
        # 2. apksigner (using the SDK's apksigner tool) with a keystore

        return True


# Example usage (within a larger Lobe orchestration)
if __name__ == "__main__":
    # This part would be orchestrated by other lobes.
    # For standalone testing:
    try:
        builder = ArabicAPKBuilder(sdk_root=str(ANDROID_SDK_ROOT))

        # Use a temporary directory for project creation
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            project_name = "MyArabicDemoApp"
            project_root = builder.generate_android_project_structure(project_name, tmp_path)
            output_apk_path = tmp_path / f"{project_name.lower()}.apk"

            if builder.compile_apk(project_root, output_apk_path):
                print(f"\n--- APK Compilation Successful ---")
                print(f"Generated APK: {output_apk_path}")
            else:
                print(f"\n--- APK Compilation Failed ---")

    except EnvironmentError as e:
        print(f"Environment Error: {e}")
        print("Please ensure ANDROID_SDK_ROOT is set correctly and contains necessary SDK components (build-tools, platforms).")
    except FileNotFoundError as e:
        print(f"File Not Found Error: {e}")
        print("Ensure required tools like 'javac', 'apkbuilder' (or equivalent) are in your system's PATH.")
    except Exception as e:
        print(f"An unexpected error occurred during demo: {e}")