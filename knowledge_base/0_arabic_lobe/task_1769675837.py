import os
import re
import subprocess
import shutil
from pathlib import Path

# Constants for file paths and project structure
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set. Please set it to your Android SDK location.")

GRADLE_WRAPPER = Path("./gradlew")
BUILD_GRADLE = Path("./app/build.gradle")
MAIN_ACTIVITY_JAVA = Path("./app/src/main/java/com/example/myapp/MainActivity.java")
MANIFEST_XML = Path("./app/src/main/AndroidManifest.xml")
APP_PACKAGE_NAME = "com.example.myapp"
DUMMY_PROJECT_ROOT = Path("./temp_android_project")

class ApkBuilder:
    """
    A class to manage the building of Android APKs from natural language.
    This module focuses on the integration of Arabic NLP results into
    a functional Android project structure.
    """

    def __init__(self, temp_project_dir: Path = DUMMY_PROJECT_ROOT):
        self.temp_project_dir = temp_project_dir
        self.project_root = temp_project_dir / "app"
        self.src_dir = self.project_root / "src" / "main" / "java" / APP_PACKAGE_NAME.replace('.', '/')
        self.resources_dir = self.project_root / "src" / "main" / "res"
        self.manifest_path = self.project_root / "src" / "main" / "AndroidManifest.xml"
        self.build_gradle_path = self.project_root / "build.gradle"

    def _create_directory_structure(self):
        """Creates the basic directory structure for an Android project."""
        print(f"Creating project structure in: {self.temp_project_dir}")
        self.temp_project_dir.mkdir(parents=True, exist_ok=True)
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.src_dir.mkdir(parents=True, exist_ok=True)
        self.resources_dir.mkdir(parents=True, exist_ok=True)

    def _create_gradle_wrapper(self):
        """Copies the gradlew script and properties to the project."""
        gradlew_src = Path("./gradlew")
        gradlew_properties_src = Path("./gradlew.properties")
        if gradlew_src.exists() and gradlew_properties_src.exists():
            shutil.copy(gradlew_src, self.temp_project_dir / "gradlew")
            shutil.copy(gradlew_properties_src, self.temp_project_dir / "gradlew.properties")
            (self.temp_project_dir / "gradlew").chmod(0o755) # Make gradlew executable
            print("Gradle wrapper created.")
        else:
            raise FileNotFoundError("gradlew or gradlew.properties not found in the root directory.")

    def _create_build_gradle(self, app_name: str = "MyApp", version_code: int = 1, version_name: str = "1.0"):
        """Creates a basic app/build.gradle file."""
        build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{APP_PACKAGE_NAME}'
    compileSdk 34

    defaultConfig {{
        applicationId "{APP_PACKAGE_NAME}"
        minSdk 24
        targetSdk 34
        versionCode {version_code}
        versionName "{version_name}"

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

    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        with open(self.build_gradle_path, "w", encoding="utf-8") as f:
            f.write(build_gradle_content)
        print("build.gradle created.")

    def _create_main_activity(self, activity_name: str = "MainActivity", package_name: str = APP_PACKAGE_NAME):
        """Creates a basic MainActivity.java file."""
        activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()}); // Assuming a layout file

        // Example: Setting text from a resource or hardcoded string
        TextView welcomeText = findViewById(R.id.welcome_text_view);
        welcomeText.setText("Hello from {activity_name}!");
    }}
}}
"""
        main_activity_file = self.src_dir / f"{activity_name}.java"
        with open(main_activity_file, "w", encoding="utf-8") as f:
            f.write(activity_content)
        print(f"{activity_name}.java created.")

    def _create_layout_file(self, activity_name: str = "MainActivity"):
        """Creates a basic activity_main.xml layout file."""
        layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/welcome_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_dir = self.resources_dir / "layout"
        layout_dir.mkdir(exist_ok=True)
        layout_file = layout_dir / f"activity_{activity_name.lower()}.xml"
        with open(layout_file, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"activity_{activity_name.lower()}.xml created.")


    def _create_manifest(self, activity_name: str = "MainActivity", package_name: str = APP_PACKAGE_NAME):
        """Creates a basic AndroidManifest.xml file."""
        manifest_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp"
        tools:targetApi="31">
        <activity
            android:name=".{activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        # Create necessary resource directories for manifest if they don't exist
        (self.resources_dir / "xml").mkdir(exist_ok=True)
        # Create dummy data_extraction_rules.xml and backup_rules.xml
        with open(self.resources_dir / "xml" / "data_extraction_rules.xml", "w") as f:
            f.write("<resources/>")
        with open(self.resources_dir / "xml" / "backup_rules.xml", "w") as f:
            f.write("<resources/>")

        # Create dummy values/strings.xml and values/themes.xml
        values_dir = self.resources_dir / "values"
        values_dir.mkdir(exist_ok=True)
        with open(values_dir / "strings.xml", "w") as f:
            f.write(f"<resources><string name=\"app_name\">{package_name.split('.')[-1].capitalize()}</string></resources>")
        with open(values_dir / "themes.xml", "w") as f:
            f.write(f"<resources><style name=\"Theme.{package_name.split('.')[-1].capitalize()}\" parent=\"Theme.Material3.DayNight.NoActionBar\"><!-- Customize your theme here. --></style></resources>")


        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print("AndroidManifest.xml created.")

    def _setup_project(self, app_name: str = "MyApp", version_code: int = 1, version_name: str = "1.0"):
        """Sets up the entire Android project structure."""
        print(f"Setting up Android project in: {self.temp_project_dir}")
        self._create_directory_structure()
        self._create_gradle_wrapper()
        self._create_build_gradle(app_name=app_name, version_code=version_code, version_name=version_name)
        self._create_main_activity()
        self._create_layout_file()
        self._create_manifest()
        print("Project setup complete.")

    def build_apk(self, semantic_result: dict) -> str | None:
        """
        Builds an APK from the provided semantic result.
        The semantic_result is expected to be a dictionary that can be
        interpreted to generate an Android application.
        This is a placeholder for more advanced semantic parsing and code generation.
        For now, it will create a minimal functional app.
        """
        app_name = semantic_result.get("app_name", "GeneratedApp")
        activity_name = semantic_result.get("activity_name", "MainActivity")
        package_name = semantic_result.get("package_name", APP_PACKAGE_NAME)
        version_code = semantic_result.get("version_code", 1)
        version_name = semantic_result.get("version_name", "1.0")

        print(f"Attempting to build APK for: {app_name} with package: {package_name}")

        try:
            self._setup_project(app_name=app_name, version_code=version_code, version_name=version_name)

            # Ensure the correct package name is used in MainActivity and Manifest
            # This is a simplified approach; a robust solution would involve code generation from semantic_result
            if package_name != APP_PACKAGE_NAME:
                # Update MainActivity with the correct package name
                main_activity_path = self.src_dir.parent / package_name.replace('.', '/') / f"{activity_name}.java"
                main_activity_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(self.src_dir / f"{activity_name}.java", main_activity_path)
                self.src_dir = main_activity_path.parent # Update self.src_dir to the new location

                # Update Manifest with the correct package name
                self.manifest_path.write_text(
                    self.manifest_path.read_text().replace(f'namespace \'{APP_PACKAGE_NAME}\'', f'namespace \'{package_name}\'')
                )
                self.manifest_path.write_text(
                    self.manifest_path.read_text().replace(f'applicationId "{APP_PACKAGE_NAME}"', f'applicationId "{package_name}"')
                )
                self.manifest_path.write_text(
                    self.manifest_path.read_text().replace(f'package="{APP_PACKAGE_NAME}"', f'package="{package_name}"')
                )
                self.manifest_path.write_text(
                    self.manifest_path.read_text().replace(f'android:name=".{activity_name}"', f'android:name=".{activity_name}"')
                )

            # Build the APK using Gradle
            print("Starting APK build process...")
            gradlew_command = [
                str(self.temp_project_dir / "gradlew"),
                "assembleDebug", # Use assembleDebug for development builds
                "-p", str(self.temp_project_dir / "app") # Specify the module to build
            ]
            # Ensure ANDROID_SDK_ROOT is set for gradlew to find SDK components
            env = os.environ.copy()
            env["ANDROID_SDK_ROOT"] = ANDROID_SDK_ROOT

            result = subprocess.run(gradlew_command, capture_output=True, text=True, cwd=self.temp_project_dir, env=env)

            if result.returncode == 0:
                print("APK build successful!")
                # Find the generated APK
                apk_path = None
                for root, _, files in os.walk(self.temp_project_dir / "app" / "build" / "outputs" / "apk" / "debug"):
                    for file in files:
                        if file.endswith(".apk"):
                            apk_path = Path(root) / file
                            break
                    if apk_path:
                        break
                if apk_path:
                    print(f"APK generated at: {apk_path}")
                    # Copy the APK to a more stable location or return its path
                    destination_dir = Path("./generated_apks")
                    destination_dir.mkdir(exist_ok=True)
                    final_apk_path = destination_dir / f"{app_name.lower().replace(' ', '_')}_{version_name}.apk"
                    shutil.copy(apk_path, final_apk_path)
                    print(f"APK copied to: {final_apk_path}")
                    return str(final_apk_path)
                else:
                    print("Could not find generated APK file.")
                    return None
            else:
                print("APK build failed.")
                print("Gradle stdout:")
                print(result.stdout)
                print("Gradle stderr:")
                print(result.stderr)
                return None
        except FileNotFoundError as e:
            print(f"Error: Required file not found - {e}")
            print("Please ensure Android SDK is correctly configured and gradlew scripts are present.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during APK build: {e}")
            return None

    def cleanup(self):
        """Cleans up the temporary project directory."""
        print(f"Cleaning up temporary project directory: {self.temp_project_dir}")
        if self.temp_project_dir.exists():
            try:
                shutil.rmtree(self.temp_project_dir)
                print("Cleanup complete.")
            except OSError as e:
                print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    # Example Usage:
    builder = ApkBuilder()

    # Mock semantic result from Arabic NLP lobe
    # This represents a simplified interpretation of what Arabic NLP could provide
    # For a real scenario, this would come from Lobe 0_arabic_lobe
    mock_semantic_result = {
        "app_name": "Arabic Greeting App",
        "activity_name": "GreetingActivity",
        "package_name": "com.example.arabicgreeting",
        "version_code": 2,
        "version_name": "1.1",
        "arabic_text_to_display": "أهلاً بك في التطبيق!" # Example of Arabic content
    }

    # The build_apk method would ideally take this semantic_result and use it
    # to dynamically generate Java code, layouts, and manifest entries.
    # For this example, we are using a pre-defined structure and just demonstrating the build process.
    # A more advanced version would parse 'arabic_text_to_display' and insert it into the layout/activity.

    generated_apk_path = None
    try:
        # In a real scenario, Lobe 0_arabic_lobe would generate mock_semantic_result
        # and Lobe 4_code_generation_lobe would use it to create source files.
        # This ApkBuilder would then compile those generated files.
        # For demonstration, we are calling build_apk directly with a mock result.
        generated_apk_path = builder.build_apk(mock_semantic_result)

        if generated_apk_path:
            print(f"\nDemo: APK generation successful. APK located at: {generated_apk_path}")
        else:
            print("\nDemo: APK generation failed.")
    except Exception as e:
        print(f"Demo failed: {e}")
    finally:
        builder.cleanup()