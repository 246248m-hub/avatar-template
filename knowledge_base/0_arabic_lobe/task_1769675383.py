import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# --- Constants ---
GENERATED_APKS_DIR = Path("./generated_apks")
GENERATED_PROJECTS_DIR = Path("./generated_projects")
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")

if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

AAPT2_PATH = Path(ANDROID_SDK_ROOT) / "build-tools" / "current" / "aapt2"
ADB_PATH = Path(ANDROID_SDK_ROOT) / "platform-tools" / "adb"

# --- Helper Functions ---

def ensure_directory_exists(dir_path: Path):
    """Ensures that a given directory path exists, creating it if necessary."""
    dir_path.mkdir(parents=True, exist_ok=True)

def execute_command(command: List[str], cwd: Path = None, capture_output: bool = False, text: bool = True) -> subprocess.CompletedProcess:
    """Executes a given command using subprocess and returns the result."""
    try:
        process = subprocess.run(command, cwd=cwd, capture_output=capture_output, text=text, check=True)
        if capture_output:
            print(f"Command output: {process.stdout}")
        return process
    except FileNotFoundError:
        raise FileNotFoundError(f"Command not found: {command[0]}. Is it in your PATH or SDK correctly configured?")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}")
        print(f"Return code: {e.returncode}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        raise

# --- Lobe 8: APK Compiler ---

class ApkCompilerLobe:
    """
    Lobe responsible for compiling generated Android projects into APKs.
    It utilizes AAPT2 for resource processing and dx/d8 for DEX compilation,
    and jarsigner/apksigner for signing.
    """

    def __init__(self, knowledge_base_dir: Path, generated_projects_dir: Path, generated_apks_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.generated_projects_dir = generated_projects_dir
        self.generated_apks_dir = generated_apks_dir
        self.android_jar = self._find_android_jar()

        ensure_directory_exists(self.generated_apks_dir)
        ensure_directory_exists(self.generated_projects_dir)
        ensure_directory_exists(self.knowledge_base_dir)

    def _find_android_jar(self) -> Path:
        """Finds the android.jar for the target SDK version."""
        # This is a simplified approach. A more robust solution would involve
        # querying the SDK configuration for the correct platform version.
        platform_tools_dir = Path(ANDROID_SDK_ROOT) / "platforms"
        # Look for the highest API level available
        api_levels = sorted([d for d in platform_tools_dir.iterdir() if d.is_dir() and d.name.startswith("android-")], key=lambda x: int(x.name.split('-')[1]), reverse=True)
        if not api_levels:
            raise FileNotFoundError("Could not find any Android platform SDKs in your ANDROID_SDK_ROOT.")

        target_platform_dir = api_levels[0]
        android_jar_path = target_platform_dir / "android.jar"
        if not android_jar_path.exists():
            raise FileNotFoundError(f"android.jar not found at {android_jar_path}. Ensure your Android SDK is properly installed.")
        return android_jar_path

    def _compile_resources(self, project_dir: Path):
        """Compiles Android resources using AAPT2."""
        print(f"\n--- Compiling resources for project: {project_dir.name} ---")
        build_dir = project_dir / "build"
        res_dir = project_dir / "res"
        manifest_path = project_dir / "AndroidManifest.xml"
        aapt2_compile_command = [
            str(AAPT2_PATH), "compile",
            "--dir", str(res_dir),
            "-o", str(build_dir / "resources.zip")
        ]
        execute_command(aapt2_compile_command, cwd=project_dir)

        aapt2_link_command = [
            str(AAPT2_PATH), "link",
            str(build_dir / "resources.zip"),
            "--manifest", str(manifest_path),
            "-I", str(self.android_jar),
            "-o", str(build_dir / f"{project_dir.name}.resources.apk")
        ]
        execute_command(aapt2_link_command, cwd=project_dir)
        print("Resource compilation complete.")

    def _compile_dex(self, project_dir: Path):
        """Compiles Java/Kotlin source files into DEX bytecode."""
        print(f"\n--- Compiling DEX for project: {project_dir.name} ---")
        src_dir = project_dir / "src"
        build_dir = project_dir / "build"
        classes_dex_dir = build_dir / "classes_dex"
        ensure_directory_exists(classes_dex_dir)

        # This is a placeholder for actual Java/Kotlin compilation.
        # In a real scenario, you'd invoke javac and then d8/dx.
        # For this example, we'll assume a single dummy Java file that
        # would be compiled. A more complete implementation would require
        # a full build system like Gradle or a direct compilation flow.

        # Example of direct compilation (requires Java Development Kit)
        # Ensure you have a dummy Java file in src/ or that your project structure
        # generates compiled .class files.
        # For simplicity, we'll simulate DEX generation.
        # The 'd8' tool is part of the Android build tools and is used for DEX compilation.

        # Assuming compiled .class files are in project_dir/classes
        # If not, you'd first need to compile Java source using 'javac'
        # For a true NLP-to-APK, this step would involve a full compiler chain.

        # Simplified DEX compilation command using d8
        # This command assumes .class files are available in a 'classes' subdirectory
        # or that you are providing a library jar.
        # For this demo, we'll create a dummy structure.
        if not (project_dir / "classes").exists():
            (project_dir / "classes").mkdir()
            # Create a dummy Java file for demonstration purposes if it doesn't exist
            dummy_java_content = """
public class MainActivity {
    public static void main(String[] args) {
        System.out.println("Hello, APK!");
    }
}
            """
            dummy_java_file = project_dir / "src" / "MainActivity.java"
            ensure_directory_exists(dummy_java_file.parent)
            if not dummy_java_file.exists():
                dummy_java_file.write_text(dummy_java_content)
                try:
                    # Compile the dummy Java file
                    javac_command = ["javac", str(dummy_java_file), "-d", str(project_dir / "classes")]
                    execute_command(javac_command, cwd=project_dir)
                except Exception as e:
                    print(f"Warning: Could not compile dummy Java file. DEX compilation might fail. Error: {e}")


        d8_command = [
            str(Path(ANDROID_SDK_ROOT) / "build-tools" / "current" / "d8"),
            str(project_dir / "classes"), # Directory containing .class files
            "--output", str(classes_dex_dir)
        ]
        try:
            execute_command(d8_command, cwd=project_dir)
            print("DEX compilation complete.")
        except Exception as e:
            print(f"Error during DEX compilation: {e}")
            raise

    def _build_apk(self, project_dir: Path, apk_output_path: Path):
        """Assembles the APK using AAPT2 and signs it."""
        print(f"\n--- Building and Signing APK for project: {project_dir.name} ---")
        build_dir = project_dir / "build"
        resources_apk = build_dir / f"{project_dir.name}.resources.apk"
        classes_dex_dir = build_dir / "classes_dex"

        # Assemble the unsigned APK
        apk_builder_command = [
            str(AAPT2_PATH), "link",
            "-o", str(apk_output_path.with_suffix(".unsigned.apk")),
            "--static-lib", # Required for building standalone APKs
            str(resources_apk),
            str(classes_dex_dir / "classes.dex"), # Link the main DEX file
            "-I", str(self.android_jar)
        ]
        execute_command(apk_builder_command, cwd=project_dir)
        unsigned_apk_path = apk_output_path.with_suffix(".unsigned.apk")

        # Signing the APK (using a dummy debug key for demonstration)
        # In a real application, you'd use a proper signing process.
        print("Signing the APK with a dummy debug key...")
        jarsigner_command = [
            "jarsigner",
            "-verbose",
            "-sigalg", "SHA1withRSA",
            "-digestalg", "SHA1",
            "-keystore", str(self.knowledge_base_dir / "debug.keystore"), # Dummy keystore
            "-storepass", "android",
            "-keypass", "android",
            str(unsigned_apk_path),
            "androiddebugkey"
        ]
        # Create a dummy keystore if it doesn't exist
        if not (self.knowledge_base_dir / "debug.keystore").exists():
            keytool_command = [
                "keytool",
                "-genkey", "-v",
                "-keystore", str(self.knowledge_base_dir / "debug.keystore"),
                "-alias", "androiddebugkey",
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-dname", "CN=Android Debug,O=Android,C=US",
                "-storepass", "android",
                "-keypass", "android"
            ]
            execute_command(keytool_command, cwd=self.knowledge_base_dir)

        try:
            execute_command(jarsigner_command, cwd=project_dir)
            print("APK signed successfully.")
        except FileNotFoundError:
            print("Warning: 'jarsigner' command not found. APK will not be signed.")
            print("Please ensure your Java Development Kit (JDK) is installed and 'jarsigner' is in your PATH.")
            print("Skipping signing and alignment.")
            shutil.move(unsigned_apk_path, apk_output_path) # Move unsigned apk if signing fails
            return
        except Exception as e:
            print(f"Error during jarsigner: {e}")
            print("Skipping signing and alignment.")
            shutil.move(unsigned_apk_path, apk_output_path) # Move unsigned apk if signing fails
            return

        # Aligning the APK (optional but recommended)
        print("Aligning the APK...")
        zipalign_command = [
            str(Path(ANDROID_SDK_ROOT) / "build-tools" / "current" / "zipalign"),
            "-v",
            "4",
            str(unsigned_apk_path),
            str(apk_output_path)
        ]
        try:
            execute_command(zipalign_command, cwd=project_dir)
            print(f"APK built and signed successfully: {apk_output_path}")
        except Exception as e:
            print(f"Error during zipalign: {e}")
            print("APK might be unsigned or incorrectly aligned.")
            # Fallback: If zipalign fails, use the signed but unaligned APK
            shutil.move(unsigned_apk_path, apk_output_path)

        # Clean up the unsigned APK
        if unsigned_apk_path.exists():
            unsigned_apk_path.unlink()


    def demo_compilation(self, project_name: str):
        """Runs the full compilation process for a given project."""
        project_dir = self.generated_projects_dir / project_name
        if not project_dir.exists():
            print(f"Error: Project directory '{project_dir}' not found.")
            return

        apk_output_path = self.generated_apks_dir / f"{project_name}.apk"

        try:
            self._compile_resources(project_dir)
            self._compile_dex(project_dir)
            self._build_apk(project_dir, apk_output_path)
            print(f"\nDemo compilation finished. APK generated at: {apk_output_path}")
        except Exception as e:
            print(f"\nDemo compilation failed: {e}")
        finally:
            # Clean up intermediate build artifacts if desired
            # For now, we keep them to inspect
            pass


# --- Main Execution ---

if __name__ == "__main__":
    # Ensure necessary directories exist
    ensure_directory_exists(GENERATED_APKS_DIR)
    ensure_directory_exists(GENERATED_PROJECTS_DIR)
    ensure_directory_exists(KNOWLEDGE_BASE_DIR)

    # --- Placeholder for Lobe 0_arabic_lobe and Lobe 0_language_lobe ---
    # In a real scenario, these lobes would have generated a project structure.
    # For this demo, we'll create a dummy project structure.

    DUMMY_PROJECT_NAME = "MyArabicApp"
    DUMMY_PROJECT_ROOT = GENERATED_PROJECTS_DIR / DUMMY_PROJECT_NAME
    DUMMY_PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    # Create dummy AndroidManifest.xml
    manifest_content = """
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myarabicapp">

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
    (DUMMY_PROJECT_ROOT / "AndroidManifest.xml").write_text(manifest_content)

    # Create dummy res/values/strings.xml
    (DUMMY_PROJECT_ROOT / "res" / "values").mkdir(parents=True, exist_ok=True)
    strings_content = """
<resources>
    <string name="app_name">تطبيقي العربي</string>
</resources>
"""
    (DUMMY_PROJECT_ROOT / "res" / "values" / "strings.xml").write_text(strings_content)

    # Create dummy src/MainActivity.java
    (DUMMY_PROJECT_ROOT / "src").mkdir(parents=True, exist_ok=True)
    main_activity_content = """
package com.example.myarabicapp;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists for layout
        TextView textView = findViewById(R.id.hello_text);
        textView.setText("مرحبا بالعالم!");
    }
}
"""
    (DUMMY_PROJECT_ROOT / "src" / "MainActivity.java").write_text(main_activity_content)

    # Create dummy res/layout/activity_main.xml (required by MainActivity)
    (DUMMY_PROJECT_ROOT / "res" / "layout").mkdir(parents=True, exist_ok=True)
    activity_main_layout_content = """
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center">

    <TextView
        android:id="@+id/hello_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp" />
</LinearLayout>
"""
    (DUMMY_PROJECT_ROOT / "res" / "layout" / "activity_main.xml").write_text(activity_main_layout_content)


    print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe ---")

    # Instantiate and run the demo for the APK Compiler Lobe
    apk_compiler_lobe = ApkCompilerLobe(
        knowledge_base_dir=KNOWLEDGE_BASE_DIR,
        generated_projects_dir=GENERATED_PROJECTS_DIR,
        generated_apks_dir=GENERATED_APKS_DIR
    )
    apk_compiler_lobe.demo_compilation(DUMMY_PROJECT_NAME)

    print("\n--- APK Compiler Module Demo Finished ---")

    # Clean up dummy project directory after demo
    print("\n--- Cleaning up dummy project directory ---")
    if DUMMY_PROJECT_ROOT.exists():
        print(f"Removing dummy project directory: {DUMMY_PROJECT_ROOT}")
        shutil.rmtree(DUMMY_PROJECT_ROOT)