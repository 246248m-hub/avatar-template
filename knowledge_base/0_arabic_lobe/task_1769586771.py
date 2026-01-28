import os
import re
import subprocess
from pathlib import Path
import shutil

# --- Configuration ---
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable is not set.")

AAPT2_PATH = Path(ANDROID_SDK_ROOT) / "build-tools" / os.listdir(Path(ANDROID_SDK_ROOT) / "build-tools")[0] / "aapt2"
APKSIGNER_PATH = Path(ANDROID_SDK_ROOT) / "build-tools" / os.listdir(Path(ANDROID_SDK_ROOT) / "build-tools")[0] / "apksigner"
ZIPALIGN_PATH = Path(ANDROID_SDK_ROOT) / "build-tools" / os.listdir(Path(ANDROID_SDK_ROOT) / "build-tools")[0] / "zipalign"
KEYSTORE_PATH = Path.home() / ".android" / "debug.keystore"
KEYSTORE_ALIAS = "androiddebugkey"
KEYSTORE_PASSWORD = "android"
KEYSTORE_KEY_ALIAS_PASSWORD = "android"

# --- Helper Functions ---

def create_directory_if_not_exists(path: Path):
    """Creates a directory if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)

def clean_directory(path: Path):
    """Removes all contents of a directory."""
    if path.exists():
        shutil.rmtree(path)
    create_directory_if_not_exists(path)

def generate_manifest_xml(package_name: str, version_code: int, version_name: str) -> str:
    """Generates a basic AndroidManifest.xml content."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}"
    android:versionCode="{version_code}"
    android:versionName="{version_name}">

    <application android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <!-- Placeholder for activities, services, etc. -->
    </application>
</manifest>
"""

# --- Lobe 4: Code Generation Lobe ---

class CodeGenerator:
    """
    This lobe is responsible for generating basic Java/Kotlin code structures
    and Android resource files based on natural language input processed by
    previous lobes. It focuses on generating boilerplate code for simple APKs.
    """

    def __init__(self, output_dir: Path = Path("generated_apk_source")):
        self.output_dir = output_dir
        self.source_dir = self.output_dir / "src" / "main"
        self.res_dir = self.source_dir / "res"
        self.java_dir = self.source_dir / "java"
        self.package_dir = None

        create_directory_if_not_exists(self.output_dir)
        create_directory_if_not_exists(self.source_dir)
        create_directory_if_not_exists(self.res_dir)
        create_directory_if_not_exists(self.java_dir)

    def generate_package_structure(self, package_name: str):
        """Creates the Java package directory structure."""
        self.package_dir = self.java_dir / Path(package_name.replace('.', '/'))
        create_directory_if_not_exists(self.package_dir)

    def generate_main_activity(self, package_name: str, activity_name: str = "MainActivity"):
        """Generates a basic MainActivity.java file."""
        activity_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()}); // Assuming a layout file
    }}
}}
"""
        activity_file = self.package_dir / f"{activity_name}.java"
        with open(activity_file, "w", encoding="utf-8") as f:
            f.write(activity_content)
        print(f"Generated {activity_file}")

    def generate_layout_file(self, activity_name: str):
        """Generates a basic activity layout XML file."""
        layout_name = f"activity_{activity_name.lower()}.xml"
        layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context="{self.package_dir.parent.name}.{activity_name}">

    <!-- Placeholder for UI elements -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_dir = self.res_dir / "layout"
        create_directory_if_not_exists(layout_dir)
        layout_file = layout_dir / layout_name
        with open(layout_file, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"Generated {layout_file}")

    def generate_string_resources(self, app_name: str = "MyApp"):
        """Generates a basic strings.xml file."""
        strings_content = f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
        values_dir = self.res_dir / "values"
        create_directory_if_not_exists(values_dir)
        strings_file = values_dir / "strings.xml"
        with open(strings_file, "w", encoding="utf-8") as f:
            f.write(strings_content)
        print(f"Generated {strings_file}")

    def generate_manifest(self, package_name: str, version_code: int = 1, version_name: str = "1.0"):
        """Generates the AndroidManifest.xml file."""
        manifest_content = generate_manifest_xml(package_name, version_code, version_name)
        manifest_file = self.source_dir / "AndroidManifest.xml"
        with open(manifest_file, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"Generated {manifest_file}")

    def generate_build_gradle(self, package_name: str):
        """Generates a basic build.gradle file."""
        build_gradle_content = f"""plugins {{
    id 'com.android.application'
    id 'java'
}}

android {{
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        build_gradle_file = self.output_dir / "build.gradle"
        with open(build_gradle_file, "w", encoding="utf-8") as f:
            f.write(build_gradle_content)
        print(f"Generated {build_gradle_file}")

    def generate_gradle_wrapper(self):
        """Generates Gradle wrapper files."""
        # This is a simplified approach. In a real scenario, you'd copy from a template or use Gradle CLI.
        gradle_wrapper_properties_content = "distributionBase=GRADLE_USER_HOME\ndistributionPath=wrapper/dists\ngarbageCollection=auto\nnetwork.decompression=false\nnetwork.retries=3\nnetwork.timeout=15\nsnapshots.fetch=auto\nsnapshots.store=auto\n"
        gradle_wrapper_properties_file = self.output_dir / "gradlew-wrapper.properties"
        with open(gradle_wrapper_properties_file, "w", encoding="utf-8") as f:
            f.write(gradle_wrapper_properties_content)

        # Create gradlew and gradlew.bat scripts (simplified placeholders)
        with open(self.output_dir / "gradlew", "w") as f:
            f.write("#!/bin/bash\nexec java -Dorg.gradle.native=false -jar \"$GRADLE_USER_HOME/gradle/your_gradle_version/bin/gradle\" \"$@\"\n")
        with open(self.output_dir / "gradlew.bat", "w") as f:
            f.write("@echo off\nif not exist \"%GRADLE_USER_HOME%\\gradle\\your_gradle_version\\bin\\gradle.bat\" goto gnw\ncall \"%GRADLE_USER_HOME%\\gradle\\your_gradle_version\\bin\\gradle.bat\" %*\ngoto :EOF\n:gnw\necho ERROR: GRADLE_USER_HOME is not set.\ngoto :EOF\n")

        print("Generated Gradle wrapper files (simplified).")


    def generate_app_structure(self, package_name: str, app_name: str = "MyApp", version_code: int = 1, version_name: str = "1.0"):
        """Generates the complete source code structure for a basic APK."""
        self.generate_package_structure(package_name)
        self.generate_main_activity(package_name)
        self.generate_layout_file("MainActivity")
        self.generate_string_resources(app_name)
        self.generate_manifest(package_name, version_code, version_name)
        self.generate_build_gradle(package_name)
        self.generate_gradle_wrapper()

        print(f"\nAPK source structure generated in: {self.output_dir}")
        print(f"Package name: {package_name}")
        print(f"App name: {app_name}")

    def build_apk(self, package_name: str, output_apk_path: Path):
        """
        Builds the APK using Gradle.
        This function orchestrates the process of compiling the generated source code
        into an APK.
        """
        print("\n--- Starting APK build process ---")

        # Ensure the build directory is clean
        clean_directory(self.output_dir / "build")

        # Run Gradle build command
        gradle_command = ["./gradlew", "assembleDebug"]
        print(f"Running Gradle command: {' '.join(gradle_command)} in {self.output_dir}")

        try:
            # Execute the Gradle wrapper
            process = subprocess.run(
                gradle_command,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                check=True
            )
            print("Gradle build output:")
            print(process.stdout)
            if process.stderr:
                print("Gradle build errors:")
                print(process.stderr)

            # Find the generated APK
            debug_apk_path = self.output_dir / "app" / "build" / "outputs" / "apk" / "debug" / f"app-debug.apk"
            if debug_apk_path.exists():
                shutil.move(str(debug_apk_path), str(output_apk_path))
                print(f"\nSuccessfully built and moved APK to: {output_apk_path}")
            else:
                raise FileNotFoundError("Generated APK not found at expected location.")

        except subprocess.CalledProcessError as e:
            print(f"Error during Gradle build: {e}")
            print("Stderr:")
            print(e.stderr)
            print("Stdout:")
            print(e.stdout)
            raise
        except FileNotFoundError:
            print("Error: gradlew command not found. Make sure you are in the correct directory or Gradle is installed.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            raise

    def sign_apk(self, apk_path: Path, output_signed_apk_path: Path):
        """
        Signs the APK using the debug keystore.
        This step is crucial for installing the APK on a device.
        """
        print("\n--- Signing APK ---")

        if not KEYSTORE_PATH.exists():
            raise FileNotFoundError(f"Debug keystore not found at: {KEYSTORE_PATH}")

        command = [
            str(APKSIGNER_PATH),
            "sign",
            "--ks", str(KEYSTORE_PATH),
            "--ks-key-alias", KEYSTORE_ALIAS,
            "--ks-pass", f"pass:{KEYSTORE_PASSWORD}",
            "--key-pass", f"pass:{KEYSTORE_KEY_ALIAS_PASSWORD}",
            "--out", str(output_signed_apk_path),
            str(apk_path)
        ]

        print(f"Executing command: {' '.join(command)}")
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            print("ApkSigner output:")
            print(process.stdout)
            if process.stderr:
                print("ApkSigner errors:")
                print(process.stderr)
            print(f"Successfully signed APK: {output_signed_apk_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error signing APK: {e}")
            print("Stderr:")
            print(e.stderr)
            print("Stdout:")
            print(e.stdout)
            raise
        except FileNotFoundError:
            print(f"Error: apksigner not found at {APKSIGNER_PATH}. Ensure ANDROID_SDK_ROOT is set correctly and build-tools are installed.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during APK signing: {e}")
            raise

    def align_apk(self, signed_apk_path: Path, output_aligned_apk_path: Path):
        """
        Aligns the signed APK using zipalign.
        This is an optimization step for APKs.
        """
        print("\n--- Aligning APK ---")

        # Create a temporary directory for alignment output
        temp_aligned_dir = self.output_dir / "aligned_temp"
        create_directory_if_not_exists(temp_aligned_dir)
        aligned_apk_intermediate = temp_aligned_dir / output_aligned_apk_path.name

        command = [
            str(ZIPALIGN_PATH),
            "-v",
            "4",
            str(signed_apk_path),
            str(aligned_apk_intermediate)
        ]

        print(f"Executing command: {' '.join(command)}")
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            print("Zipalign output:")
            print(process.stdout)
            if process.stderr:
                print("Zipalign errors:")
                print(process.stderr)

            shutil.move(str(aligned_apk_intermediate), str(output_aligned_apk_path))
            print(f"Successfully aligned APK: {output_aligned_apk_path}")
            shutil.rmtree(temp_aligned_dir) # Clean up temporary directory

        except subprocess.CalledProcessError as e:
            print(f"Error aligning APK: {e}")
            print("Stderr:")
            print(e.stderr)
            print("Stdout:")
            print(e.stdout)
            if temp_aligned_dir.exists():
                shutil.rmtree(temp_aligned_dir)
            raise
        except FileNotFoundError:
            print(f"Error: zipalign not found at {ZIPALIGN_PATH}. Ensure ANDROID_SDK_ROOT is set correctly and build-tools are installed.")
            if temp_aligned_dir.exists():
                shutil.rmtree(temp_aligned_dir)
            raise
        except Exception as e:
            print(f"An unexpected error occurred during APK alignment: {e}")
            if temp_aligned_dir.exists():
                shutil.rmtree(temp_aligned_dir)
            raise

    def generate_and_build_apk(self, package_name: str, app_name: str, output_apk_path: Path):
        """
        Orchestrates the generation of source code and the subsequent build process.
        """
        self.generate_app_structure(package_name, app_name)
        self.build_apk(package_name, output_apk_path.with_name(f"{output_apk_path.stem}_unsigned{output_apk_path.suffix}"))
        unsigned_apk_path = output_apk_path.with_name(f"{output_apk_path.stem}_unsigned{output_apk_path.suffix}")
        self.sign_apk(unsigned_apk_path, output_apk_path.with_name(f"{output_apk_path.stem}_signed{output_apk_path.suffix}"))
        signed_apk_path = output_apk_path.with_name(f"{output_apk_path.stem}_signed{output_apk_path.suffix}")
        self.align_apk(signed_apk_path, output_apk_path)

        # Clean up intermediate files
        if unsigned_apk_path.exists():
            unsigned_apk_path.unlink()
        if signed_apk_path.exists():
            signed_apk_path.unlink()
        print("\n--- Intermediate APK files cleaned up ---")

        print(f"\nFinal APK generated at: {output_apk_path}")

# --- Example Usage ---
if __name__ == "__main__":
    # Mocking Arabic to Package Name conversion (Lobe 0_language_lobe interaction)
    # In a real scenario, this would be driven by Arabic NLP output.
    arabic_package_name_mapping = {
        "تطبيق_حاسبة_بسيط": "com.example.simplecalculator",
        "لعبة_الذاكرة": "com.example.memorygame",
        "قارئ_الأخبار": "com.example.newsreader"
    }

    # Mocking Arabic to App Name conversion
    arabic_app_name_mapping = {
        "تطبيق_حاسبة_بسيط": "Simple Calculator",
        "لعبة_الذاكرة": "Memory Game",
        "قارئ_الأخبار": "News Reader"
    }

    # Sample Arabic phrases that might be processed
    test_arabic_phrases = [
        "أنشئ لي تطبيق حاسبة بسيط",
        "أريد لعبة ذاكرة",
        "برمج قارئ الأخبار"
    ]

    for phrase in test_arabic_phrases:
        print(f"\n--- Processing Arabic Phrase: '{phrase}' ---")

        # --- Simulate NLP Processing (Lobe 0_language_lobe) ---
        # This is a very basic simulation. A real NLP lobe would parse the phrase
        # and extract intents and entities.
        package_name = "com.example.defaultapp"
        app_name = "Default App"
        if "حاسبة بسيط" in phrase:
            package_name = arabic_package_name_mapping["تطبيق_حاسبة_بسيط"]
            app_name = arabic_app_name_mapping["تطبيق_حاسبة_بسيط"]
            print(f"Detected intent: Create Calculator App. Package: {package_name}, App Name: {app_name}")
        elif "لعبة ذاكرة" in phrase:
            package_name = arabic_package_name_mapping["لعبة_الذاكرة"]
            app_name = arabic_app_name_mapping["لعبة_الذاكرة"]
            print(f"Detected intent: Create Memory Game App. Package: {package_name}, App Name: {app_name}")
        elif "قارئ الأخبار" in phrase:
            package_name = arabic_package_name_mapping["قارئ_الأخبار"]
            app_name = arabic_app_name_mapping["قارئ_الأخبار"]
            print(f"Detected intent: Create News Reader App. Package: {package_name}, App Name: {app_name}")
        else:
            print("Could not determine app type from phrase, using defaults.")

        # --- Instantiate CodeGenerator (Lobe 4_code_generation_lobe) ---
        code_generator = CodeGenerator(output_dir=Path(f"temp_apk_build_{package_name.split('.')[-1]}"))
        output_apk_filename = f"{package_name.split('.')[-1]}.apk"
        output_apk_path = Path(output_apk_filename)

        # --- Generate and Build APK ---
        try:
            code_generator.generate_and_build_apk(package_name, app_name, output_apk_path)
            print(f"\n--- Successfully generated APK for: '{phrase}' ---")
        except Exception as e:
            print(f"\n--- Failed to generate APK for: '{phrase}' ---")
            print(f"Error: {e}")

        # --- Clean up generated source directory for the next iteration ---
        if code_generator.output_dir.exists():
            print(f"Cleaning up source directory: {code_generator.output_dir}")
            shutil.rmtree(code_generator.output_dir)

    print("\n--- Lobe 4_code_generation_lobe Demo Finished ---")