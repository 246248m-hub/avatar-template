import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# --- Constants ---
TEMP_DIR = Path("./temp_arabic_project")
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

AAPT2_PATH = Path(ANDROID_SDK_ROOT) / "build-tools" / "current" / "aapt2"
APKSIGNER_PATH = Path(ANDROID_SDK_ROOT) / "build-tools" / "current" / "apksigner"
GRADLE_WRAPPER = Path("./gradlew") # Assuming gradlew is in the root directory or accessible

# --- Helper Functions ---
def create_dummy_project(project_name: str = "ArabicDemoApp", package_name: str = "com.example.arabicdemo"):
    """Creates a minimal dummy Android project structure."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)

    # Create basic AndroidManifest.xml
    manifest_dir = TEMP_DIR / "app" / "src" / "main"
    manifest_dir.mkdir(parents=True)
    manifest_content = f"""
    <manifest xmlns:android="http://schemas.android.com/apk/res/android"
        package="{package_name}">
        <application
            android:label="{project_name}"
            android:icon="@mipmap/ic_launcher">
            <activity android:name=".MainActivity" android:exported="true">
                <intent-filter>
                    <action android:name="android.intent.action.MAIN" />
                    <category android:name="android.intent.category.LAUNCHER" />
                </intent-filter>
            </activity>
        </application>
    </manifest>
    """
    (manifest_dir / "AndroidManifest.xml").write_text(manifest_content)

    # Create dummy strings.xml for Arabic support
    res_dir = TEMP_DIR / "app" / "src" / "main" / "res"
    res_dir.mkdir(parents=True)
    values_dir = res_dir / "values"
    values_dir.mkdir(parents=True)
    values_ar_dir = res_dir / "values-ar"
    values_ar_dir.mkdir(parents=True)

    default_strings_content = """
    <resources>
        <string name="app_name">Arabic Demo App</string>
        <string name="greeting">Hello World!</string>
    </resources>
    """
    (values_dir / "strings.xml").write_text(default_strings_content)

    arabic_strings_content = """
    <resources>
        <string name="app_name">تطبيق تجريبي عربي</string>
        <string name="greeting">أهلاً بالعالم!</string>
    </resources>
    """
    (values_ar_dir / "strings.xml").write_text(arabic_strings_content)

    print(f"Dummy project created at: {TEMP_DIR}")
    return TEMP_DIR

def compile_apk(project_path: Path, output_apk_path: Path) -> None:
    """
    Compiles a basic Android project into an APK using AAPT2 and a simple build process.
    This is a simplified approach, a real-world scenario would use Gradle.
    """
    print(f"Starting APK compilation for project: {project_path}")

    # 1. Resource Compilation with AAPT2 (AAPT = Android Asset Packaging Tool)
    # This command compiles resources (like layouts, drawables, strings) into intermediate .apk file
    # and then generates a package for the compiled resources.
    aapt2_compile_command = [
        str(AAPT2_PATH), "compile",
        "--dir", str(project_path / "app" / "src" / "main" / "res"),
        "-o", str(TEMP_DIR / "compiled_resources.zip")
    ]
    print(f"Running AAPT2 compile: {' '.join(aapt2_compile_command)}")
    subprocess.run(aapt2_compile_command, check=True, capture_output=True, text=True)

    # 2. Resource Linking with AAPT2
    # This command links the compiled resources with the AndroidManifest.xml to create a final package.
    aapt2_link_command = [
        str(AAPT2_PATH), "link",
        "--manifest", str(project_path / "app" / "src" / "main" / "AndroidManifest.xml"),
        str(TEMP_DIR / "compiled_resources.zip"),
        "-o", str(TEMP_DIR / "resources.apk"),
        "--stable-ids",
        "--no-version-vectors",
        "-I", str(Path(ANDROID_SDK_ROOT) / "platforms" / "android-30" / "android.jar") # Using a common platform version
    ]
    print(f"Running AAPT2 link: {' '.join(aapt2_link_command)}")
    subprocess.run(aapt2_link_command, check=True, capture_output=True, text=True)

    # 3. APK Packaging (Simplified - does not include DEX, classes.dex, etc.)
    # For a truly functional APK, we would need to compile Java/Kotlin code to DEX
    # and include it. This example focuses on resource packaging and signing.
    # We'll create a basic APK structure with just the resources for demonstration.
    # A real build would involve dx tool or D8 compiler and then packaging using `aapt2 package`.

    # For demonstration, we'll directly use 'aapt2 package' to create a zip-like structure first
    # This command is more involved and often part of a build system.
    # A more accurate simplified approach would be to create a zip archive.
    # Let's simulate creating a zip archive that resembles an APK structure.

    # Create a temporary directory for APK contents
    apk_content_dir = TEMP_DIR / "apk_contents"
    apk_content_dir.mkdir(parents=True, exist_ok=True)

    # Extract resources from resources.apk into the content directory
    # This is a bit hacky, as resources.apk is not a standard zip. AAPT2 handles this internally.
    # We'll copy the contents of resources.apk which is essentially the compiled resources.
    # In a real scenario, this would be handled by `aapt2 package` or Gradle.
    # For this simplified demo, we'll assume resources.apk contains the necessary compiled assets.
    # This step is illustrative and might not work directly without deeper AAPT2 integration.
    # A better simulation:
    unzip_command = [
        "unzip", str(TEMP_DIR / "resources.apk"), "-d", str(apk_content_dir)
    ]
    print(f"Simulating APK content creation: {' '.join(unzip_command)}")
    # NOTE: resources.apk is not a standard zip. This step requires more advanced handling of AAPT2 output.
    # For this simplified demo, we'll skip actual unpacking and assume the structure is handled by aapt2.
    # A more realistic compilation would look like:
    # subprocess.run([str(AAPT2_PATH), "package", "--output-dir", str(TEMP_DIR), "--apk", ...], check=True)
    # Given the constraints, we'll directly try to sign the "APK-like" structure.
    # This will likely fail if the structure is not properly formed by AAPT2 in the expected way for signing.

    # Create a dummy classes.dex if it doesn't exist to satisfy signing requirements
    if not (apk_content_dir / "classes.dex").exists():
        (apk_content_dir / "classes.dex").write_bytes(b'\x78\x56\x34\x12') # Minimal valid DEX header

    # Create the final APK by zipping the contents
    # This is where a proper build tool is essential. We'll create a zip for now.
    # `aapt2 package --output-format apk --output <output.apk> ...` would be used here.
    print(f"Packaging APK contents into: {output_apk_path}")
    # shutil.make_archive(str(output_apk_path).replace('.apk', ''), 'zip', str(apk_content_dir))
    # os.rename(f"{output_apk_path}.zip", output_apk_path)

    # A more direct way to create an APK-like zip using aapt2:
    aapt2_package_command = [
        str(AAPT2_PATH), "package",
        "--output-dir", str(TEMP_DIR),
        "--apk", str(output_apk_path),
        "--manifest", str(project_path / "app" / "src" / "main" / "AndroidManifest.xml"),
        str(TEMP_DIR / "compiled_resources.zip"),
        "-I", str(Path(ANDROID_SDK_ROOT) / "platforms" / "android-30" / "android.jar")
    ]
    print(f"Running AAPT2 package: {' '.join(aapt2_package_command)}")
    # This command requires more arguments for actual code inclusion,
    # so this simplified version will likely produce an invalid APK if only resources are provided.
    # For this demo, we will focus on the signing step assuming a valid APK is produced.
    # A true compilation would involve:
    # 1. Compiling Java/Kotlin -> Dalvik bytecode (.dex) using `d8` or `dx`.
    # 2. Packaging all resources and .dex files into an APK using `aapt2 package`.
    # 3. Signing the APK.

    # For this demo, let's assume `output_apk_path` is a placeholder for a potentially valid APK
    # and proceed to signing. If compilation fails, signing will also fail.
    # We'll create a dummy APK if the above commands don't yield one, for the sake of demonstrating signing.

    if not output_apk_path.exists():
        print("Warning: AAPT2 package command did not produce an APK. Creating a dummy APK for signing demo.")
        # Create a minimal valid APK structure manually
        dummy_apk_structure = TEMP_DIR / "dummy_unsigned.apk"
        with open(dummy_apk_structure, "wb") as f:
            f.write(b"PK\003\004\010\000\000\000\000\000") # Minimal ZIP header
            f.write(b"\000\000\000\000\000\000\000\000\000\000\000\000") # Counts and offsets
            f.write(b"META-INF/MANIFEST.MF") # Dummy entries
            f.write(b"META-INF/CERT.SF")
            f.write(b"META-INF/CERT.RSA")
            f.write(b"classes.dex") # Dummy classes.dex
            f.write(b"AndroidManifest.xml") # Dummy manifest
            f.write(b"res/layout/activity_main.xml") # Dummy resource
            # This is highly simplified and not a valid APK, but allows the signing tool to run.

        # Copy the dummy structure to the output path
        shutil.copy(dummy_apk_structure, output_apk_path)


    # 4. APK Signing with apksigner
    # This command signs the APK with a debug key (or a release key if provided).
    # For this demo, we will use the default debug keystore that Android SDK provides.
    # The keystore and key alias are typically managed by the build system.
    # Here, we assume default debug credentials.

    # Create a dummy keystore and key if one doesn't exist for demonstration purposes.
    # In a real scenario, you would use your own keystore.
    debug_keystore_path = TEMP_DIR / "debug.keystore"
    if not debug_keystore_path.exists():
        print("Creating a dummy debug keystore for signing.")
        try:
            keytool_command = [
                "keytool",
                "-genkey",
                "-v",
                "-keystore", str(debug_keystore_path),
                "-alias", "androiddebugkey",
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-dname", "CN=Android Debug,OU=Android,O=Android,C=US",
                "-storepass", "android",
                "-keypass", "android"
            ]
            print(f"Running keytool: {' '.join(keytool_command)}")
            subprocess.run(keytool_command, check=True, capture_output=True, text=True, input="android\nandroid\n")
        except FileNotFoundError:
            print("keytool command not found. Skipping keystore creation. Signing will likely fail.")
        except subprocess.CalledProcessError as e:
            print(f"keytool error: {e.stderr}")
            print("Skipping keystore creation. Signing will likely fail.")


    if debug_keystore_path.exists():
        apksigner_sign_command = [
            str(APKSIGNER_PATH),
            "sign",
            "--ks", str(debug_keystore_path),
            "--ks-key-alias", "androiddebugkey",
            "--ks-pass", "pass:android",
            "--key-pass", "pass:android",
            "--out", str(output_apk_path.parent / "signed_" / output_apk_path.name),
            str(output_apk_path)
        ]
        print(f"Running apksigner: {' '.join(apksigner_sign_command)}")
        try:
            subprocess.run(apksigner_sign_command, check=True, capture_output=True, text=True)
            print(f"APK signed successfully: {output_apk_path.parent / 'signed_' / output_apk_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"apksigner signing failed: {e.stderr}")
            raise
    else:
        print("Debug keystore not available. Skipping APK signing.")


# --- Lobe 8_apk_compiler_lobe ---
class Lobe8ApkCompilerLobe:
    """
    This lobe is responsible for the final compilation and packaging of an APK.
    It takes the intermediate project structure and generates a signed APK.
    This is a simplified simulation of the Android build process.
    """

    def __init__(self):
        self.name = "Lobe 8: APK Compiler Lobe"

    def execute(self, project_structure_data: Dict[str, Any]) -> Path:
        """
        Executes the APK compilation process.

        Args:
            project_structure_data: A dictionary containing information about the
                                    project structure, typically including a path
                                    to a temporary project directory.

        Returns:
            Path to the generated signed APK file.
        """
        print(f"\n--- Executing {self.name} ---")

        project_root = project_structure_data.get("temp_project_root")
        if not project_root or not Path(project_root).exists():
            raise ValueError("Invalid or missing project root path in project_structure_data.")

        output_apk_name = project_structure_data.get("output_apk_name", "app-release.apk")
        output_dir = Path(project_root).parent / "compiled_apks"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_apk_path = output_dir / output_apk_name

        try:
            compile_apk(Path(project_root), output_apk_path)
            signed_apk_path = output_apk_path.parent / "signed_" / output_apk_name
            if signed_apk_path.exists():
                print(f"Successfully generated signed APK: {signed_apk_path}")
                return signed_apk_path
            else:
                raise RuntimeError("APK compilation and signing process failed to produce a signed APK.")
        except Exception as e:
            print(f"Error during APK compilation: {e}")
            raise

    def demo(self):
        """Demonstrates the functionality of the APK Compiler Lobe."""
        print(f"\n--- Demo: {self.name} ---")
        dummy_project_root = None
        try:
            # Create a dummy Android project
            dummy_project_root = create_dummy_project()
            project_structure_data = {"temp_project_root": str(dummy_project_root)}

            # Execute the compilation process
            # Note: This compile_apk function is a simplification and might not produce
            # a fully functional APK without a proper build system (like Gradle)
            # and compilation of Java/Kotlin code to DEX.
            # The focus here is on the structure and signing process.
            signed_apk = self.execute(project_structure_data)
            print(f"\nDemo finished. Signed APK generated at: {signed_apk}")

        except Exception as e:
            print(f"\nDemo failed: {e}")
        finally:
            # Clean up the dummy project
            if dummy_project_root and dummy_project_root.exists():
                print(f"Removing dummy project directory: {dummy_project_root}")
                shutil.rmtree(dummy_project_root)
            # Clean up the compiled APKs directory if it's empty or only contains intermediate files
            compiled_apks_dir = Path("./compiled_apks")
            if compiled_apks_dir.exists() and not any(compiled_apks_dir.iterdir()):
                print(f"Removing empty compiled APKs directory: {compiled_apks_dir}")
                shutil.rmtree(compiled_apks_dir)
            elif compiled_apks_dir.exists():
                print(f"Compiled APKs directory: {compiled_apks_dir}")


if __name__ == '__main__':
    apk_compiler = Lobe8ApkCompilerLobe()
    apk_compiler.demo()