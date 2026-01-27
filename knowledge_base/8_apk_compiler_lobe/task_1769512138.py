import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

# Assume these are defined and accessible from other lobes
# KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
# TEMPLATE_DIR = Path("./templates")
# ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
# JAVA_HOME = os.environ.get("JAVA_HOME")

class APKCompiler:
    """
    This module is responsible for compiling generated code into an APK.
    It interfaces with the Android build tools (aapt, dx/d8, apkbuilder, apksigner).
    """
    def __init__(self, android_sdk_root: Path, java_home: Path, build_tools_version: str):
        self.android_sdk_root = android_sdk_root
        self.java_home = java_home
        self.build_tools_path = self.android_sdk_root / "build-tools" / build_tools_version
        self.platform_tools_path = self.android_sdk_root / "platform-tools"
        self.aapt_path = self.build_tools_path / "aapt"
        self.dx_d8_path = self.build_tools_path / ("dx" if os.name == "nt" else "d8") # dx for older SDKs, d8 for newer
        self.apkbuilder_path = self.build_tools_path / "apkbuilder"
        self.apksigner_path = self.platform_tools_path / "apksigner"
        self.jarsigner_path = self.java_home / "bin" / "jarsigner"

        if not all([self.aapt_path.exists(), self.dx_d8_path.exists(), self.apkbuilder_path.exists(), self.apksigner_path.exists(), self.jarsigner_path.exists()]):
            missing = [p for p in [self.aapt_path, self.dx_d8_path, self.apkbuilder_path, self.apksigner_path, self.jarsigner_path] if not p.exists()]
            raise FileNotFoundError(f"Missing essential build tools: {missing}")

    def _run_command(self, command: list[str], cwd: Path = None) -> subprocess.CompletedProcess:
        """Helper to run shell commands and capture output."""
        print(f"Executing command: {' '.join(command)}")
        process = subprocess.run(command, capture_output=True, text=True, check=True, cwd=cwd)
        if process.stdout:
            print("STDOUT:\n", process.stdout)
        if process.stderr:
            print("STDERR:\n", process.stderr)
        return process

    def compile_apk(self, manifest_path: Path, resource_dir: Path, source_dir: Path, output_apk_path: Path, staged_dir: Path):
        """
        Compiles source code and resources into a final APK.

        Args:
            manifest_path: Path to the AndroidManifest.xml file.
            resource_dir: Path to the compiled resources directory (e.g., res/).
            source_dir: Path to the compiled Java/Kotlin source files (.class or .dex).
            output_apk_path: The desired path for the final APK.
            staged_dir: A temporary directory to stage intermediate build artifacts.
        """
        staged_dir.mkdir(parents=True, exist_ok=True)
        resources_path = staged_dir / "resources"
        classes_dex_path = staged_dir / "classes.dex"
        unsigned_apk_path = staged_dir / "unsigned.apk"
        signed_apk_path = staged_dir / "signed.apk"

        # 1. Compile resources using AAPT
        print("\n--- Compiling resources with AAPT ---")
        aapt_command = [
            str(self.aapt_path),
            "package",
            "-f",  # Force overwrite
            "-m",  # Generate only R.java, don't compile
            "-J", str(staged_dir / "java_gen"), # Java source output for R.java
            "-M", str(manifest_path),
            "-S", str(resource_dir),
            "-I", str(self.android_sdk_root / "platforms" / "android-30"), # Example API level, adjust as needed
            "-F", str(unsigned_apk_path) # Output the APK structure directly
        ]
        self._run_command(aapt_command, cwd=staged_dir)

        # Note: AAPT now directly packages resources into the APK structure for newer versions.
        # For older versions, you might have needed to extract resources and then rebuild.
        # The command above should create an APK with just resources if no classes are present.

        # 2. Compile Java bytecode to Dalvik Executable (DEX) format
        print("\n--- Compiling Java bytecode to DEX ---")
        # Assuming source_dir contains .class files
        if list(source_dir.glob("*.class")):
            dx_d8_command = [
                str(self.dx_d8_path),
                "--dex",
                f"--output={classes_dex_path}",
                str(source_dir)
            ]
            self._run_command(dx_d8_command, cwd=staged_dir)
        else:
            print("No .class files found in source directory. Skipping DEX compilation.")


        # 3. Create the unsigned APK using Apkbuilder (if DEX files exist)
        print("\n--- Creating unsigned APK ---")
        if classes_dex_path.exists():
            apkbuilder_command = [
                str(self.apkbuilder_path),
                str(unsigned_apk_path),
                f"-f={manifest_path}", # Manifest file
                f"-r={resource_dir}", # Compiled resources
                f"-d={classes_dex_path}", # DEX file
                "-v" # Verbose output
            ]
            # Apkbuilder expects the APK file as the first argument, which it will create/overwrite.
            # We'll create a temporary one and then sign it later.
            # A better approach for newer SDKs might be to use `java -jar bundletool.jar build-apks ...`
            # but Apkbuilder is more direct for simple cases.
            # The AAPT command above should have already created a basic APK structure.
            # If Apkbuilder is used to *add* classes to an existing APK structure:
            apkbuilder_add_command = [
                str(self.apkbuilder_path),
                str(unsigned_apk_path),
                f"-d={classes_dex_path}", # Add DEX file to existing APK
                "-v"
            ]
            self._run_command(apkbuilder_add_command, cwd=staged_dir)
        else:
            print("No DEX files to add. Unsigned APK will only contain resources.")
            # If no classes, AAPT should have already created the APK with resources.

        # 4. Sign the APK
        print("\n--- Signing the APK ---")
        # For simplicity, using a debug keystore. In production, use a proper keystore.
        # Path to debug.keystore and its password/alias can be found in Android SDK documentation.
        # For automated builds, a release keystore should be provided.
        debug_keystore = Path.home() / ".android" / "debug.keystore"
        if not debug_keystore.exists():
            raise FileNotFoundError(f"Debug keystore not found at {debug_keystore}. Please generate one or provide a release keystore.")

        jarsigner_command = [
            str(self.jarsigner_path),
            "-verbose",
            "-sigalg", "SHA1withRSA",
            "-digestalg", "SHA1",
            "-keystore", str(debug_keystore),
            "-storepass", "android", # Default password for debug keystore
            str(unsigned_apk_path),
            "androiddebugkey" # Default alias for debug keystore
        ]
        self._run_command(jarsigner_command, cwd=staged_dir)

        # 5. Align the APK (optional but recommended)
        print("\n--- Aligning the APK ---")
        # This step is often handled by zipalign, which is usually in platform-tools.
        zipalign_path = self.platform_tools_path / "zipalign"
        if not zipalign_path.exists():
             print("zipalign not found, skipping alignment.")
        else:
            aligned_apk_path = staged_dir / "aligned.apk"
            zipalign_command = [
                str(zipalign_path),
                "-v",
                "4", # Alignment
                str(unsigned_apk_path),
                str(aligned_apk_path)
            ]
            self._run_command(zipalign_command, cwd=staged_dir)
            # The aligned APK is the one we want to copy to the final destination.
            final_unsigned_path = aligned_apk_path
        else:
            final_unsigned_path = unsigned_apk_path


        # 6. Use apksigner for final signing (recommended over jarsigner for Android)
        print("\n--- Final signing with apksigner ---")
        apksigner_command = [
            str(self.apksigner_path),
            "sign",
            "--ks", str(debug_keystore),
            "--ks-key-alias", "androiddebugkey",
            "--ks-pass", "pass:android",
            f"--out={signed_apk_path}",
            str(final_unsigned_path)
        ]
        self._run_command(apksigner_command, cwd=staged_dir)


        # Move the final signed APK to the desired output path
        if signed_apk_path.exists():
            os.rename(signed_apk_path, output_apk_path)
            print(f"Successfully created signed APK at: {output_apk_path}")
        else:
            raise RuntimeError("Apksigner failed to produce a signed APK.")

        # Clean up staged directory if not needed for debugging
        # import shutil
        # shutil.rmtree(staged_dir)


# Example Usage within the context of other lobes
def build_apk_module(manifest_content: str, resources_data: dict, java_code: str, output_dir: Path, temp_dir: Path, build_tools_version: str = "30.0.3"):
    """
    Orchestrates the APK compilation process.

    Args:
        manifest_content: String content of AndroidManifest.xml.
        resources_data: Dictionary representing resources (e.g., {'res/layout/activity_main.xml': '<LinearLayout ...>'}).
        java_code: String containing the Java/Kotlin code for the app.
        output_dir: Directory to save the final APK.
        temp_dir: Directory for temporary build artifacts.
        build_tools_version: The version of Android SDK build tools to use.
    """
    ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
    JAVA_HOME = os.environ.get("JAVA_HOME")

    if not ANDROID_SDK_ROOT:
        raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")
    if not JAVA_HOME:
        raise EnvironmentError("JAVA_HOME environment variable not set.")

    android_sdk_root_path = Path(ANDROID_SDK_ROOT)
    java_home_path = Path(JAVA_HOME)

    try:
        compiler = APKCompiler(android_sdk_root_path, java_home_path, build_tools_version)

        # --- Prepare project structure in temp_dir ---
        project_root = temp_dir / "apk_build_project"
        project_root.mkdir(parents=True, exist_ok=True)

        manifest_path = project_root / "AndroidManifest.xml"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        resource_dir = project_root / "res"
        resource_dir.mkdir(exist_ok=True)
        for res_file_path, res_content in resources_data.items():
            target_path = resource_dir / Path(res_file_path).relative_to("res")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(res_content)

        source_dir = project_root / "src"
        source_dir.mkdir(exist_ok=True)
        # For simplicity, assume Java code is compiled to .class files beforehand
        # In a real scenario, Lobe 4_code_generation_lobe would handle this,
        # and potentially output .java files that we'd then compile here.
        # For this example, we assume .class files are available in a specific structure.
        # Let's assume for now that `java_code` is actually the *path* to compiled .class files.
        # A more robust solution would integrate javac.
        # If `java_code` is the actual source code string, it needs to be saved and compiled first.

        # For demonstration: Save the Java code and compile it to .class files
        java_file_path = source_dir / "MainActivity.java" # Assume a single main activity for simplicity
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(java_code)

        # Compile Java to .class using javac
        javac_command = [
            str(java_home_path / "bin" / "javac"),
            "-d", str(source_dir), # Output directory for .class files
            "-cp", str(android_sdk_root_path / "platforms" / "android-30" / "android.jar"), # Example classpath
            str(java_file_path)
        ]
        print(f"\n--- Compiling Java source to .class ---")
        subprocess.run(javac_command, check=True)
        compiled_classes_dir = source_dir # This directory now contains .class files

        # --- Compile APK ---
        output_apk_path = output_dir / "app-release.apk"
        staged_dir = temp_dir / "apk_staged_build"

        compiler.compile_apk(
            manifest_path=manifest_path,
            resource_dir=resource_dir,
            source_dir=compiled_classes_dir, # Path containing .class files
            output_apk_path=output_apk_path,
            staged_dir=staged_dir
        )

        print(f"\nAPK successfully built and saved to: {output_apk_path}")
        return output_apk_path

    except FileNotFoundError as e:
        print(f"Build tool not found: {e}. Ensure Android SDK and build tools are correctly configured.")
        raise
    except subprocess.CalledProcessError as e:
        print(f"Build command failed: {e}")
        print(f"Command: {e.cmd}")
        print(f"Stderr: {e.stderr}")
        raise
    except EnvironmentError as e:
        print(f"Environment configuration error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during APK compilation: {e}")
        raise

# Placeholder for demonstration purposes, assuming it's called by other lobes.
# In a real system, KNOWLEDGE_BASE_DIR and TEMPLATE_DIR would be initialized.
# KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
# TEMPLATE_DIR = Path("./templates")

# Example of how this module might be used:
if __name__ == "__main__":
    # Mock environment variables for testing
    if "ANDROID_SDK_ROOT" not in os.environ:
        print("ANDROID_SDK_ROOT not set. Mocking for demonstration.")
        # In a real environment, this should point to your Android SDK installation
        # For example: os.environ["ANDROID_SDK_ROOT"] = "/path/to/your/android-sdk"
        # For this example, we'll create dummy files to avoid immediate FileNotFoundError
        dummy_sdk_root = Path("./dummy_android_sdk")
        dummy_sdk_root.mkdir(exist_ok=True)
        (dummy_sdk_root / "build-tools").mkdir(exist_ok=True)
        (dummy_sdk_root / "build-tools" / "30.0.3").mkdir(exist_ok=True)
        (dummy_sdk_root / "build-tools" / "30.0.3" / "aapt").touch()
        (dummy_sdk_root / "build-tools" / "30.0.3" / "d8").touch()
        (dummy_sdk_root / "build-tools" / "30.0.3" / "apkbuilder").touch()
        (dummy_sdk_root / "platforms").mkdir(exist_ok=True)
        (dummy_sdk_root / "platforms" / "android-30").mkdir(exist_ok=True)
        (dummy_sdk_root / "platforms" / "android-30" / "android.jar").touch()
        (dummy_sdk_root / "platform-tools").mkdir(exist_ok=True)
        (dummy_sdk_root / "platform-tools" / "apksigner").touch()
        (dummy_sdk_root / "platform-tools" / "zipalign").touch()
        os.environ["ANDROID_SDK_ROOT"] = str(dummy_sdk_root)

    if "JAVA_HOME" not in os.environ:
        print("JAVA_HOME not set. Mocking for demonstration.")
        # In a real environment, this should point to your JDK installation
        # For example: os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
        dummy_java_home = Path("./dummy_jdk")
        dummy_java_home.mkdir(exist_ok=True)
        (dummy_java_home / "bin").mkdir(exist_ok=True)
        (dummy_java_home / "bin" / "javac").touch()
        (dummy_java_home / "bin" / "jarsigner").touch()
        os.environ["JAVA_HOME"] = str(dummy_java_home)

    # Mock debug keystore
    debug_keystore_path = Path.home() / ".android" / "debug.keystore"
    if not debug_keystore_path.exists():
        print(f"Mocking debug.keystore at {debug_keystore_path}")
        debug_keystore_path.parent.mkdir(parents=True, exist_ok=True)
        debug_keystore_path.touch()

    # --- Define mock inputs ---
    mock_manifest = """
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

    mock_resources = {
        "res/values/strings.xml": '<resources><string name="app_name">My App</string></resources>',
        "res/layout/activity_main.xml": '<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity"><TextView android:text="Hello, World!" android:layout_width="wrap_content" android:layout_height="wrap_content"/></LinearLayout>'
    }

    mock_java_code = """
    package com.example.myapp;

    import android.os.Bundle;
    import androidx.appcompat.app.AppCompatActivity;
    import android.widget.TextView;

    public class MainActivity extends AppCompatActivity {

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
            // Example: find a TextView and set text
            TextView tv = findViewById(R.id.myTextView); // Assuming an ID is present, though not in mock XML
            // If TextView ID is not in XML, this would cause a runtime error.
            // For demonstration, we'll assume it's there or skip setting text if not found.
            // In a real scenario, IDs would be generated in R.java by AAPT.
            // Let's simplify and just use a generic TextView.
             TextView greetingTextView = new TextView(this);
             greetingTextView.setText("Hello from generated code!");
             setContentView(greetingTextView); // Overwrite layout for simplicity or add to existing
        }
    }
    """
    # Note: The mock Java code needs a TextView with ID "myTextView" to work as intended.
    # Since our mock XML doesn't define it, let's adjust the Java code to be simpler for this test,
    # or ensure R.java generation is properly handled by AAPT.
    # For this demo, we'll let the compiler run, even if the Java code might have a lookup error.
    # A better mock would ensure R.java is generated and then used.

    # Let's refine the mock Java code for better compatibility with the mock XML.
    # The mock XML has a TextView without an ID. AAPT would generate an ID for it.
    # For simplicity, let's assume the TextView is the *only* element and thus `findViewById` might not work directly without R.java.
    # A simpler approach for this demo is to create the TextView programmatically.
    mock_java_code_simplified = """
    package com.example.myapp;

    import android.os.Bundle;
    import androidx.appcompat.app.AppCompatActivity;
    import android.widget.TextView;
    import android.view.Gravity;

    public class MainActivity extends AppCompatActivity {

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            // setContentView(R.layout.activity_main); // Using the layout file directly

            // Create a TextView programmatically for simplicity in this mock example
            TextView textView = new TextView(this);
            textView.setText("Hello, World from generated APK!");
            textView.setTextSize(24);
            textView.setGravity(Gravity.CENTER);
            setContentView(textView);
        }
    }
    """


    output_directory = Path("./output_apks")
    temp_directory = Path("./temp_build")

    output_directory.mkdir(exist_ok=True)
    temp_directory.mkdir(exist_ok=True)

    try:
        built_apk_path = build_apk_module(
            manifest_content=mock_manifest,
            resources_data=mock_resources,
            java_code=mock_java_code_simplified, # Use the simplified version
            output_dir=output_directory,
            temp_dir=temp_directory,
            build_tools_version="30.0.3" # Specify a common build tools version
        )
        print(f"\n--- APK Compilation Demo Finished ---")
        print(f"Generated APK path: {built_apk_path}")

    except Exception as e:
        print(f"\n--- APK Compilation Demo Failed ---")
        print(f"Error: {e}")

    finally:
        # Clean up dummy files if they were created
        if 'dummy_sdk_root' in locals() and dummy_sdk_root.exists():
            print("Cleaning up dummy SDK environment...")
            import shutil
            shutil.rmtree(dummy_sdk_root)
        if 'dummy_java_home' in locals() and dummy_java_home.exists():
            print("Cleaning up dummy JDK environment...")
            import shutil
            shutil.rmtree(dummy_java_home)
        if 'debug_keystore_path' in locals() and debug_keystore_path.exists() and "Mocking debug.keystore" in globals().get('__builtins__', {}).get('print', lambda *args, **kwargs: None).__self__.message.split('\n')[-1]:
             print("Cleaning up mocked debug.keystore...")
             debug_keystore_path.unlink()
             debug_keystore_path.parent.rmdir()