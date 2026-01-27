import os
import shutil
import subprocess

# Placeholder for actual Android SDK path, assumes it's in PATH for this example
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT") or "/usr/local/android-sdk"
AAPT2_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "aapt2")
APKsigner_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "apksigner")
ZIPALIGN_PATH = os.path.join(ANDROID_SDK_ROOT, "build-tools", "current", "zipalign")

# --- Configuration ---
TEMP_BUILD_DIR = "temp_apk_build"
RELEASE_KEYSTORE = "release.keystore"
KEYSTORE_ALIAS = "my-release-key"
KEYSTORE_PASSWORD = "password"
KEY_ALIAS_PASSWORD = "password"

class ApkCompiler:
    def __init__(self, temp_build_dir=TEMP_BUILD_DIR):
        self.temp_build_dir = temp_build_dir
        self.unzipped_apk_dir = os.path.join(self.temp_build_dir, "unzipped_apk")
        self.signed_apk_path = os.path.join(self.temp_build_dir, "signed_release.apk")
        self.aligned_apk_path = os.path.join(self.temp_build_dir, "aligned_release.apk")

    def setup_build_environment(self):
        """
        Prepares the directory structure for building an APK.
        Creates a temporary build directory and the unzip directory.
        """
        if os.path.exists(self.temp_build_dir):
            shutil.rmtree(self.temp_build_dir)
        os.makedirs(self.unzipped_apk_dir)
        os.makedirs(os.path.dirname(self.signed_apk_path))
        print(f"Build environment set up in: {self.temp_build_dir}")

    def extract_apk_contents(self, apk_path):
        """
        Extracts the contents of a given APK file to a temporary directory.
        This simulates having a base APK structure to modify.
        """
        if not os.path.exists(apk_path):
            raise FileNotFoundError(f"APK file not found at: {apk_path}")

        print(f"Extracting APK contents from: {apk_path}")
        shutil.unpack_archive(apk_path, self.unzipped_apk_dir, "zip")
        print(f"APK contents extracted to: {self.unzipped_apk_dir}")

    def modify_apk_contents(self, arabic_code_path):
        """
        Integrates modified Arabic code (e.g., compiled resources, manifest updates)
        into the unzipped APK structure.
        This function is a placeholder for more complex modifications,
        such as injecting Arabic resources or updating the AndroidManifest.xml.
        """
        print(f"Modifying APK contents with Arabic code from: {arabic_code_path}")
        # In a real scenario, this would involve:
        # 1. Merging Arabic resources (e.g., layouts, strings) into the unzipped APK's resources directory.
        # 2. Potentially updating the AndroidManifest.xml for Arabic language support.
        # 3. Recompiling any Java/Kotlin source code if applicable and placing the .dex files.

        # For this demonstration, we'll simulate adding a dummy Arabic resource file.
        arabic_resources_dir = os.path.join(self.unzipped_apk_dir, "res", "values-ar")
        os.makedirs(arabic_resources_dir, exist_ok=True)
        with open(os.path.join(arabic_resources_dir, "strings.xml"), "w", encoding="utf-8") as f:
            f.write("""<resources>
    <string name="app_name">تطبيق عربي</string>
    <string name="hello_world">أهلاً بالعالم!</string>
</resources>""")
        print("Simulated Arabic resources added.")

        # Re-pack the modified contents into a new APK (intermediate step before signing)
        intermediate_apk_path = os.path.join(self.temp_build_dir, "modified_unsigned.apk")
        print(f"Repacking modified APK to: {intermediate_apk_path}")
        shutil.make_archive(os.path.splitext(intermediate_apk_path)[0], 'zip', self.unzipped_apk_dir)
        os.rename(os.path.splitext(intermediate_apk_path)[0] + '.zip', intermediate_apk_path)
        print("Repacking complete.")
        return intermediate_apk_path

    def sign_apk(self, unsigned_apk_path):
        """
        Signs the unsigned APK using a release keystore.
        Requires a release keystore, alias, and passwords.
        """
        if not os.path.exists(RELEASE_KEYSTORE):
            print(f"Warning: Release keystore '{RELEASE_KEYSTORE}' not found. Skipping signing.")
            print("Please create a release.keystore for actual signing.")
            # For demonstration, return the unsigned APK path if keystore is missing
            return unsigned_apk_path

        print(f"Signing APK: {unsigned_apk_path} with alias '{KEYSTORE_ALIAS}'")
        command = [
            APKsinger_PATH,
            "--ks", RELEASE_KEYSTORE,
            "--ks-pass", f"pass:{KEYSTORE_PASSWORD}",
            "--key-pass", f"pass:{KEY_ALIAS_PASSWORD}",
            "--out", self.signed_apk_path,
            unsigned_apk_path
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"APK signed successfully. Signed APK saved to: {self.signed_apk_path}")
            return self.signed_apk_path
        except subprocess.CalledProcessError as e:
            print(f"Error signing APK: {e}")
            print(f"Stderr: {e.stderr}")
            raise

    def zip_align_apk(self, signed_apk_path):
        """
        Performs zipalign on the signed APK to optimize it for distribution.
        """
        print(f"Performing zipalign on APK: {signed_apk_path}")
        command = [
            ZIPALIGN_PATH,
            "-v",  # Verbose output
            "4",   # Alignment in bytes
            signed_apk_path,
            self.aligned_apk_path
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Zipalign successful. Aligned APK saved to: {self.aligned_apk_path}")
            return self.aligned_apk_path
        except subprocess.CalledProcessError as e:
            print(f"Error during zipalign: {e}")
            print(f"Stderr: {e.stderr}")
            raise

    def build_apk(self, base_apk_path, arabic_code_output_dir):
        """
        Orchestrates the entire APK building process:
        1. Sets up the build environment.
        2. Extracts the base APK.
        3. Modifies the APK contents with Arabic code.
        4. Signs the modified APK.
        5. Zipaligns the signed APK.
        Returns the path to the final, aligned APK.
        """
        self.setup_build_environment()
        self.extract_apk_contents(base_apk_path)
        modified_unsigned_apk = self.modify_apk_contents(arabic_code_output_dir)
        signed_apk = self.sign_apk(modified_unsigned_apk)
        final_apk_path = self.zip_align_apk(signed_apk)
        return final_apk_path

    def cleanup_build_artifacts(self):
        """
        Removes the temporary build directory.
        """
        if os.path.exists(self.temp_build_dir):
            print(f"Cleaning up build artifacts in: {self.temp_build_dir}")
            shutil.rmtree(self.temp_build_dir)
            print("Build artifacts cleaned.")

# --- Demo Section ---
def demo_apk_compiler():
    """
    Demonstrates the functionality of the ApkCompiler.
    Requires a placeholder base APK file (e.g., an existing small Android app).
    """
    print("\n--- Initiating Lobe 8_apk_compiler_lobe Demo ---")

    # Create a dummy base APK for demonstration purposes.
    # In a real scenario, this would be a valid APK generated from Lobe 4.
    # For this demo, we'll create a minimal structure and zip it.
    base_apk_demo_dir = os.path.join(TEMP_BUILD_DIR, "base_apk_source")
    os.makedirs(os.path.join(base_apk_demo_dir, "res", "values"), exist_ok=True)
    with open(os.path.join(base_apk_demo_dir, "res", "values", "strings.xml"), "w") as f:
        f.write('<resources><string name="app_name">BaseApp</string></resources>')
    with open(os.path.join(base_apk_demo_dir, "AndroidManifest.xml"), "w") as f:
        f.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.baseapp"><application android:label="@string/app_name"><activity android:name=".MainActivity"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>')
    with open(os.path.join(base_apk_demo_dir, "classes.dex"), "w") as f: # Dummy file
        f.write("dex content")
    with open(os.path.join(base_apk_demo_dir, "resources.arsc"), "w") as f: # Dummy file
        f.write("arsc content")

    dummy_base_apk_path = os.path.join(TEMP_BUILD_DIR, "base_app.apk")
    shutil.make_archive(os.path.splitext(dummy_base_apk_path)[0], 'zip', base_apk_demo_dir)
    os.rename(os.path.splitext(dummy_base_apk_path)[0] + '.zip', dummy_base_apk_path)
    print(f"Created dummy base APK for demo at: {dummy_base_apk_path}")

    # Simulate output from Lobe 4 (code generation) - typically a directory of compiled assets/resources.
    # For this demo, we just need a path to a directory that could contain Arabic code/resources.
    arabic_code_output_dir_demo = os.path.join(TEMP_BUILD_DIR, "generated_arabic_assets")
    os.makedirs(arabic_code_output_dir_demo, exist_ok=True)
    print(f"Simulated Arabic code output directory: {arabic_code_output_dir_demo}")

    apk_compiler = ApkCompiler()
    try:
        final_apk_path = apk_compiler.build_apk(dummy_base_apk_path, arabic_code_output_dir_demo)
        print(f"\nSimulated APK generated successfully at: {final_apk_path}")
        print(f"The generated APK is a modified version of '{dummy_base_apk_path}' with Arabic resources.")
    except Exception as e:
        print(f"\nAPK compilation failed: {e}")
    finally:
        # Clean up the dummy base APK and its source directory
        if os.path.exists(dummy_base_apk_path):
            os.remove(dummy_base_apk_path)
        if os.path.exists(base_apk_demo_dir):
            shutil.rmtree(base_apk_demo_dir)
        # Clean up the build artifacts after the demo
        apk_compiler.cleanup_build_artifacts()

    print("\n--- Lobe 8_apk_compiler_lobe Demo Finished ---")

if __name__ == "__main__":
    # Ensure necessary paths are set or provide placeholders if not found
    if not ANDROID_SDK_ROOT or not os.path.exists(AAPT2_PATH) or not os.path.exists(APKsinger_PATH) or not os.path.exists(ZIPALIGN_PATH):
        print("WARNING: Android SDK build tools (aapt2, apksigner, zipalign) not found in expected locations.")
        print("Please set the ANDROID_SDK_ROOT environment variable or adjust paths.")
        print("Demo will run with simulated signing/zipaligning steps.")
        # Mocking paths if they don't exist to allow code execution for demonstration logic
        os.makedirs(TEMP_BUILD_DIR, exist_ok=True)
        AAPT2_PATH = shutil.which("aapt2") or "mock_aapt2"
        APKsinger_PATH = shutil.which("apksigner") or "mock_apksigner"
        ZIPALIGN_PATH = shutil.which("zipalign") or "mock_zipalign"

    # Create a dummy keystore for the demo if it doesn't exist
    if not os.path.exists(RELEASE_KEYSTORE):
        print(f"Creating a dummy keystore: {RELEASE_KEYSTORE}")
        try:
            # This command requires keytool, which is part of the JDK.
            # It's a placeholder; a real keystore generation is more involved.
            subprocess.run([
                "keytool", "-genkeypair",
                "-alias", KEYSTORE_ALIAS,
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-keystore", RELEASE_KEYSTORE,
                "-storepass", KEYSTORE_PASSWORD,
                "-keypass", KEY_ALIAS_PASSWORD,
                "-dname", "CN=Android Debug, OU=Android, O=Android, C=US"
            ], check=True, capture_output=True, text=True)
            print("Dummy keystore created.")
        except FileNotFoundError:
            print("keytool not found. Skipping dummy keystore creation.")
            print("Signing will be skipped in the demo if keystore is missing.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating dummy keystore: {e}")
            print(f"Stderr: {e.stderr}")
            print("Signing will be skipped in the demo if keystore is missing.")


    demo_apk_compiler()