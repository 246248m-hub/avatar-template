import os
import re
from pathlib import Path
import subprocess
import shutil

# Assume these are defined elsewhere or will be defined in other lobes
# For now, let's define them as placeholders to make the code runnable
BUILD_TOOLS_DIR = Path("build_tools")
TEMP_DIR = Path("temp")
PROJECT_TEMPLATES_DIR = Path("project_templates")
GRADLE_PROPERTIES_TEMPLATE = "org.gradle.jvmargs=-Xmx2048m\n"
GRADLE_WRAPPER_PROPERTIES_TEMPLATE = "distributionBase=GRADLE_USER_HOME\ndistributionPath=wrapper/dists\ndistributionUrl=https\://services.gradle.org/distributions/gradle-7.5.1-bin.zip\nzipStorePath=wrapper/dists\nzipStoreBase=GRADLE_USER_HOME\n"
APP_BUILD_GRADLE_TEMPLATE = """
plugins {{
    id 'com.android.application'
    id 'kotlin-android'
}}

android {{
    compileSdk 33
    defaultConfig {{
        applicationId "{app_id}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}
    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.core:core:1.5.0'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
ANDROID_MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:package="{app_id}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.YourAppName">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
MAIN_ACTIVITY_TEMPLATE = """package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
"""
STRINGS_XML_TEMPLATE = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
STRINGS_XML_ROUND_ICON_TEMPLATE = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
DRAWABLE_IC_LAUNCHER_TEMPLATE = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x00@\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x01sBIT\x00\x08\xb0\x85\x80\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\x97\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xe2\xea\x00\x00\x00\x0eIDATx\x9cc\xfc\xff\xff?\x03\x86\x07\xa1\x96A\x80\x08\xa0\xa00F\x90 \x01\x89\x81\x14\x04\x11\x00\x00\x00\x00IEND\xaeB`\x82"
DRAWABLE_IC_LAUNCHER_ROUND_TEMPLATE = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x00@\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x01sBIT\x00\x08\xb0\x85\x80\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\x97\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xe2\xea\x00\x00\x00\x0eIDATx\x9cc\xfc\xff\xff?\x03\x86\x07\xa1\x96A\x80\x08\xa0\xa00F\x90 \x01\x89\x81\x14\x04\x11\x00\x00\x00\x00IEND\xaeB`\x82"
LAYOUT_ACTIVITY_MAIN_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
GRADLEW_TEMPLATE = """#!/ Gradle wrapper script

##############################################################################
##
##  Gradle start up script for UN*X
##
##############################################################################

default_delay=5
default_debug_port=5005

# The user is the owner of the file.
USER_ID=`/usr/bin/id -u`
# The group is the group that owns the file.
GROUP_ID=`/usr/bin/id -g`

# Use the JAVA_HOME option to set the Java executable
if [ -z "$JAVA_HOME" ] ; then
  JAVA_CMD="java"
else
  JAVA_CMD="$JAVA_HOME/bin/java"
fi

# Set the GRADLE_APP_HOME environment variable
if [ -z "$GRADLE_APP_HOME" ]; then
    GRADLE_APP_HOME="."
fi

# Use the org.gradle.jvmargs option to pass JVM arguments
if [ -z "$ORG_GRADLE_JVM_ARGS" ] ; then
    # Use default JVM args if none are provided
    export ORG_GRADLE_JVM_ARGS="-Xmx64m -Xms64m"
fi

# Execute Gradle
exec "$JAVA_CMD" $ORG_GRADLE_JVM_ARGS -classpath org.gradle.wrapper.GradleWrapperMain org.gradle.wrapper.GradleWrapperMain "$@"
"""
GRADLEW_BAT_TEMPLATE = """@REM Gradle start up script for Windows

@if "%DEBUG_ гридл%" == "true" @end
    @echo "Starting a Gradle script for project"
    @REM
    @REM Uncomment the following line to enable the debugging output and set the
    @REMebug port.
    @REM set DEBUG_PORT=5005
    @REM @echo "Now using cable from %DEBUG_PORT% to connect to the process."
@end

@REM  Setting environment variables for the Gradle script.

SET JAVA_CMD=java

if not "%JAVA_HOME%" == "" goto java_home_set
echo JAVA_HOME is not set. Trying to use the java executable on your path.
goto exec_gradle
:java_home_set
echo JAVA_HOME is set to "%JAVA_HOME%"
SET JAVA_CMD="%JAVA_HOME%/bin/java"

:exec_gradle
@REM  Get the location of this script.
SET STOCK_HOME=%~dp0

@REM  Determine if the script is running in debug mode.
SET DEBUG_ гридл=false
if not "%GRADLE_DEBUG_ гридл%" == "" SET DEBUG_ гридл=true

@REM  Set the default JVM arguments.
if not "%ORG_GRADLE_JVM_ARGS%" == "" goto arguments_set
REM  Default JVM args if none are provided.
SET ORG_GRADLE_JVM_ARGS=-Xmx64m -Xms64m
:arguments_set

@REM  Execute Gradle.
"%JAVA_CMD%" %ORG_GRADLE_JVM_ARGS% -classpath "%STOCK_HOME%gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*
"""

# Mocking a debug.keystore for the purpose of compilation
MOCK_DEBUG_KEYSTORE_CONTENT = b"This is a mock debug.keystore file."

class ArabicCodeGenerator:
    def __init__(self):
        self.project_name_counter = 0
        self.default_app_name = "MyArabicApp"
        self.default_app_id = "com.example.myarabicapp"

    def _generate_project_name(self):
        self.project_name_counter += 1
        return f"arabic_apk_project_{self.project_name_counter}"

    def _create_directory_structure(self, project_path: Path):
        """Creates the basic Android project directory structure."""
        (project_path / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "drawable").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "mipmap-hdpi").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "mipmap-mdpi").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "mipmap-xhdpi").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "mipmap-xxhdpi").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "mipmap-xxxhdpi").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)
        (project_path / "gradle").mkdir(parents=True, exist_ok=True)
        (project_path / "gradle" / "wrapper").mkdir(parents=True, exist_ok=True)
        (project_path / "app").mkdir(parents=True, exist_ok=True)


    def _write_file(self, file_path: Path, content: str):
        """Writes content to a file, creating parent directories if they don't exist."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_binary_file(self, file_path: Path, content: bytes):
        """Writes binary content to a file, creating parent directories if they don't exist."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)

    def _generate_gradle_files(self, project_path: Path, app_id: str, package_name: str):
        """Generates the necessary Gradle build files."""
        self._write_file(project_path / "build.gradle", APP_BUILD_GRADLE_TEMPLATE.format(app_id=app_id))
        self._write_file(project_path / "gradle.properties", GRADLE_PROPERTIES_TEMPLATE)
        self._write_file(project_path / "gradle" / "wrapper" / "gradle-wrapper.properties", GRADLE_WRAPPER_PROPERTIES_TEMPLATE)
        self._write_file(project_path / "gradlew", GRADLEW_TEMPLATE)
        self._write_file(project_path / "gradlew.bat", GRADLEW_BAT_TEMPLATE)
        os.chmod(project_path / "gradlew", 0o755)

        # Create app-level build.gradle
        self._write_file(project_path / "app" / "build.gradle", APP_BUILD_GRADLE_TEMPLATE.format(app_id=app_id))

    def _generate_android_manifest(self, project_path: Path, app_id: str, app_name: str):
        """Generates the AndroidManifest.xml."""
        manifest_path = project_path / "app" / "src" / "main" / "AndroidManifest.xml"
        self._write_file(manifest_path, ANDROID_MANIFEST_TEMPLATE.format(app_id=app_id))

    def _generate_activity_files(self, project_path: Path, package_name: str):
        """Generates the MainActivity.java file."""
        activity_path = project_path / "app" / "src" / "main" / "java" / package_name.replace('.', '/') / "MainActivity.java"
        self._write_file(activity_path, MAIN_ACTIVITY_TEMPLATE.format(package_name=package_name))

    def _generate_resources(self, project_path: Path, app_name: str):
        """Generates string resources and icon files."""
        self._write_file(project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml", STRINGS_XML_TEMPLATE.format(app_name=app_name))
        self._write_binary_file(project_path / "app" / "src" / "main" / "res" / "drawable" / "ic_launcher.png", DRAWABLE_IC_LAUNCHER_TEMPLATE)
        self._write_binary_file(project_path / "app" / "src" / "main" / "res" / "drawable" / "ic_launcher_round.png", DRAWABLE_IC_LAUNCHER_ROUND_TEMPLATE)

        # For other mipmap densities, copy the base icons or use smaller versions if available
        for density in ["hdpi", "mdpi", "xhdpi", "xxhdpi", "xxxhdpi"]:
            self._write_binary_file(project_path / "app" / "src" / "main" / "res" / f"mipmap-{density}" / "ic_launcher.png", DRAWABLE_IC_LAUNCHER_TEMPLATE)
            self._write_binary_file(project_path / "app" / "src" / "main" / "res" / f"mipmap-{density}" / "ic_launcher_round.png", DRAWABLE_IC_LAUNCHER_ROUND_TEMPLATE)

    def _generate_layout_files(self, project_path: Path):
        """Generates the activity_main.xml layout file."""
        layout_path = project_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        self._write_file(layout_path, LAYOUT_ACTIVITY_MAIN_TEMPLATE)

    def _create_mock_debug_keystore(self, project_path: Path):
        """Creates a mock debug.keystore file for the signing configuration."""
        debug_keystore_dir = project_path / ".android"
        debug_keystore_dir.mkdir(parents=True, exist_ok=True)
        debug_keystore_path = debug_keystore_dir / "debug.keystore"
        self._write_binary_file(debug_keystore_path, MOCK_DEBUG_KEYSTORE_CONTENT)
        print(f"Created mock debug.keystore at: {debug_keystore_path}")
        return debug_keystore_path

    def _run_gradle_build(self, project_path: Path):
        """Runs the Gradle build command to create the APK."""
        print(f"Running Gradle build for project at: {project_path}")
        current_dir = os.getcwd()
        os.chdir(project_path)

        try:
            # Attempt to build the APK. This requires a JDK and Android SDK to be installed and configured.
            # We'll use the command line for this.
            # The 'assembleDebug' task will generate an unsigned APK.
            # For a signed APK, 'assembleRelease' would be used, requiring signing keys.
            # For this module's objective, generating an unsigned APK is sufficient to demonstrate compilation.
            # We'll assume Gradle wrapper is executable.
            gradlew_command = ["./gradlew", "assembleDebug"]
            if os.name == 'nt':  # Windows
                gradlew_command = ["gradlew.bat", "assembleDebug"]

            # Capture output to check for success/failure
            result = subprocess.run(gradlew_command, capture_output=True, text=True, check=True)
            print("Gradle build successful.")
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)

            # Locate the generated APK
            apk_path = None
            for root, dirs, files in os.walk("app/build/outputs/apk/debug"):
                for file in files:
                    if file.endswith(".apk"):
                        apk_path = Path(root) / file
                        break
                if apk_path:
                    break

            if apk_path and apk_path.exists():
                print(f"Successfully generated unsigned APK: {apk_path}")
                return apk_path
            else:
                print("APK file not found after build.")
                return None

        except subprocess.CalledProcessError as e:
            print(f"Gradle build failed.")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return code: {e.returncode}")
            print(f"STDOUT:\n{e.stdout}")
            print(f"STDERR:\n{e.stderr}")
            return None
        except FileNotFoundError:
            print("Error: gradlew or gradlew.bat not found. Ensure it's executable and in the project root.")
            print("Please ensure that Java Development Kit (JDK) and Android SDK are installed and configured correctly.")
            return None
        finally:
            os.chdir(current_dir)

    def generate_arabic_apk(self, arabic_text: str, output_dir: Path = Path("output_apks")) -> Path | None:
        """
        Generates a basic Android APK with Arabic text embedded, if applicable,
        or a generic app structure that can be further populated.

        Args:
            arabic_text (str): The Arabic text to potentially embed.
                               Currently, this is used for app naming and resource strings.
            output_dir (Path): The directory where the generated APK will be saved.

        Returns:
            Path | None: The path to the generated APK file, or None if an error occurred.
        """
        if not arabic_text:
            print("Warning: No Arabic text provided. Generating a default app structure.")
            app_name = self.default_app_name
            app_id = self.default_app_id
        else:
            # Basic sanitization for app name and ID.
            # A more robust Arabic string processing lobe would be ideal here.
            sanitized_name = re.sub(r'[^\w\s]', '', arabic_text).strip()
            if not sanitized_name:
                app_name = self.default_app_name
            else:
                app_name = sanitized_name
            # Convert to lowercase and replace spaces for app ID
            app_id = "com.example." + re.sub(r'\s+', '', sanitized_name.lower())
            if len(app_id) > 30: # Basic length constraint for app_id
                app_id = app_id[:30]


        project_name = self._generate_project_name()
        project_path = Path(project_name)
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"--- Creating project: {project_name} ---")
        self._create_directory_structure(project_path)
        self._generate_gradle_files(project_path, app_id, app_id.replace('com.example.', ''))
        self._generate_android_manifest(project_path, app_id, app_name)
        self._generate_activity_files(project_path, app_id.replace('com.example.', '')) # Package name from app_id
        self._generate_resources(project_path, app_name)
        self._generate_layout_files(project_path)

        # Mock the debug keystore for signing during the build process
        mock_keystore_path = self._create_mock_debug_keystore(project_path)

        print(f"--- Building APK for project: {project_name} ---")
        generated_apk_path = self._run_gradle_build(project_path)

        if generated_apk_path and generated_apk_path.exists():
            final_apk_name = f"{app_name.replace(' ', '_').lower()}_debug.apk"
            final_apk_path = output_dir / final_apk_name
            try:
                shutil.move(str(generated_apk_path), str(final_apk_path))
                print(f"Moved generated APK to: {final_apk_path}")
            except Exception as e:
                print(f"Error moving APK: {e}")
                final_apk_path = None
            finally:
                # Clean up the project directory
                print(f"\n--- Cleaning up project directory: {project_path} ---")
                if project_path.exists():
                    shutil.rmtree(project_path)
                    print(f"Removed project directory: {project_path}")
                # Clean up the mock keystore
                if mock_keystore_path and mock_keystore_path.exists():
                    try:
                        mock_keystore_path.unlink()
                        mock_keystore_path.parent.rmdir() # Remove the .android directory
                        print(f"Removed mock debug.keystore: {mock_keystore_path}")
                    except OSError as e:
                        print(f"Error removing mock keystore: {e}")
            return final_apk_path
        else:
            print("APK generation failed.")
            # Clean up the project directory even on failure
            print(f"\n--- Cleaning up failed project directory: {project_path} ---")
            if project_path.exists():
                shutil.rmtree(project_path)
                print(f"Removed project directory: {project_path}")
            if mock_keystore_path and mock_keystore_path.exists():
                try:
                    mock_keystore_path.unlink()
                    mock_keystore_path.parent.rmdir()
                    print(f"Removed mock debug.keystore: {mock_keystore_path}")
                except OSError as e:
                    print(f"Error removing mock keystore: {e}")
            return None

# Example of how this module might be used (this part would not be in the raw output)
if __name__ == "__main__":
    # Ensure necessary build tools and directories exist for the demo
    BUILD_TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    PROJECT_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    print("--- Initiating Lobe 4_code_generation_lobe demo ---")
    arabic_generator = ArabicCodeGenerator()

    # Test case 1: Basic Arabic text
    arabic_phrase_1 = "تطبيق عربي بسيط"
    print(f"\nGenerating APK for: '{arabic_phrase_1}'")
    generated_apk_1 = arabic_generator.generate_arabic_apk(arabic_phrase_1)
    if generated_apk_1:
        print(f"Successfully generated APK: {generated_apk_1}")
    else:
        print("Failed to generate APK.")

    # Test case 2: Another Arabic phrase
    arabic_phrase_2 = "مرحبا بالعالم"
    print(f"\nGenerating APK for: '{arabic_phrase_2}'")
    generated_apk_2 = arabic_generator.generate_arabic_apk(arabic_phrase_2, output_dir=Path("output_apks/another_batch"))
    if generated_apk_2:
        print(f"Successfully generated APK: {generated_apk_2}")
    else:
        print("Failed to generate APK.")

    # Test case 3: Empty input (should generate default app)
    print("\nGenerating APK with empty input (default app).")
    generated_apk_3 = arabic_generator.generate_arabic_apk("")
    if generated_apk_3:
        print(f"Successfully generated APK: {generated_apk_3}")
    else:
        print("Failed to generate APK.")

    print("\n--- Lobe 4_code_generation_lobe demo finished ---")

    # Clean up demo project templates and directories if they were created by the demo itself
    print("\n--- Cleaning up demo directories ---")
    if BUILD_TOOLS_DIR.exists():
        shutil.rmtree(BUILD_TOOLS_DIR)
        print(f"Removed demo directory: {BUILD_TOOLS_DIR}")
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print(f"Removed demo directory: {TEMP_DIR}")
    if PROJECT_TEMPLATES_DIR.exists():
        shutil.rmtree(PROJECT_TEMPLATES_DIR)
        print(f"Removed demo directory: {PROJECT_TEMPLATES_DIR}")
    if Path("output_apks").exists():
        shutil.rmtree("output_apks")
        print("Removed demo output directory: output_apks")