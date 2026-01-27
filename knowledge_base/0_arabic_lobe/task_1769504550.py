import os
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

# Assume these are defined elsewhere or imported
# KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
# APK_BUILD_DIR = Path("./build/apk")
# APP_SPEC_DIR = Path("./app_specs")
# ANDROID_HOME = os.environ.get("ANDROID_HOME")
# JAVA_HOME = os.environ.get("JAVA_HOME")

class ArabicAPKBuilder:
    """
    A module responsible for building APKs specifically for Arabic language applications,
    leveraging natural language specifications.
    """

    def __init__(self, knowledge_base_dir: Path, apk_build_dir: Path, app_spec_dir: Path, android_home: str, java_home: str):
        self.knowledge_base_dir = knowledge_base_dir
        self.apk_build_dir = apk_build_dir
        self.app_spec_dir = app_spec_dir
        self.android_home = android_home
        self.java_home = java_home

        if not self.android_home or not self.java_home:
            raise EnvironmentError("ANDROID_HOME and JAVA_HOME must be set.")

        self.sdk_tools_dir = Path(self.android_home) / "build-tools"
        self.platform_tools_dir = Path(self.android_home) / "platform-tools"
        self.gradle_wrapper_path = None # Will be determined during build

        self._setup_environment()

    def _setup_environment(self):
        """
        Sets up the necessary environment variables and checks for required tools.
        """
        if not self.sdk_tools_dir.exists():
            raise FileNotFoundError(f"Android build tools not found at {self.sdk_tools_dir}")
        if not self.platform_tools_dir.exists():
            raise FileNotFoundError(f"Android platform tools not found at {self.platform_tools_dir}")

        # Add relevant directories to PATH for subprocesses
        os.environ["PATH"] = f"{os.environ['PATH']}:{self.platform_tools_dir}:{Path(self.java_home) / 'bin'}"

    def _find_latest_build_tools(self) -> Path:
        """
        Finds the latest installed Android SDK build-tools version.
        """
        build_tools_versions = sorted(list(self.sdk_tools_dir.iterdir()), key=lambda x: x.name, reverse=True)
        if not build_tools_versions:
            raise FileNotFoundError("No Android build tools found.")
        return build_tools_versions[0]

    def _generate_android_project_structure(self, app_spec: dict, project_path: Path):
        """
        Generates a basic Android project structure based on the app specification.
        This is a simplified representation; a real implementation would be much more complex.
        """
        project_path.mkdir(parents=True, exist_ok=True)
        app_name = app_spec.get("name", "MyApp").replace(" ", "")
        package_name = app_spec.get("package_name", f"com.example.{app_name.lower()}")
        min_sdk = app_spec.get("min_sdk", 21)
        target_sdk = app_spec.get("target_sdk", 33)
        compile_sdk = app_spec.get("compile_sdk", 33)

        # Create basic manifest
        manifest_path = project_path / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <uses-sdk android:minSdkVersion="{min_sdk}" android:targetSdkVersion="{target_sdk}" />

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
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Create basic strings.xml
        strings_path = project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        strings_path.parent.mkdir(parents=True, exist_ok=True)
        strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
        with open(strings_path, "w", encoding="utf-8") as f:
            f.write(strings_content)

        # Create basic MainActivity.java
        java_dir = project_path / "app" / "src" / "main" / "java" / package_name.replace(".", os.sep)
        java_dir.mkdir(parents=True, exist_ok=True)
        main_activity_path = java_dir / "MainActivity.java"
        main_activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists
    }}
}}
"""
        with open(main_activity_path, "w", encoding="utf-8") as f:
            f.write(main_activity_content)

        # Create basic build.gradle (app level)
        app_gradle_path = project_path / "app" / "build.gradle"
        app_gradle_path.parent.mkdir(parents=True, exist_ok=True)
        app_gradle_content = f"""
plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{package_name}'
    compileSdk {compile_sdk}

    defaultConfig {{
        applicationId "{package_name}"
        minSdk {min_sdk}
        targetSdk {target_sdk}
        versionCode 1
        versionName "1.0"
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
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1' // Example dependency
    // Add other dependencies based on app_spec
}}
"""
        with open(app_gradle_path, "w", encoding="utf-8") as f:
            f.write(app_gradle_content)

        # Create basic settings.gradle
        settings_gradle_path = project_path / "settings.gradle"
        settings_gradle_content = f"""
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{app_name}"
include ':app'
"""
        with open(settings_gradle_path, "w", encoding="utf-8") as f:
            f.write(settings_gradle_content)

        # Create top-level build.gradle
        top_level_gradle_path = project_path / "build.gradle"
        top_level_gradle_content = f"""
buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath 'com.android.tools.build:gradle:7.4.2' // Example Gradle version
        // Add other buildscript dependencies
    }}
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
"""
        with open(top_level_gradle_path, "w", encoding="utf-8") as f:
            f.write(top_level_gradle_content)

        # Create Gradle wrapper
        gradle_wrapper_path = project_path / "gradlew"
        if not gradle_wrapper_path.exists():
            try:
                subprocess.run(["gradle", "--version"], cwd=project_path, check=True, capture_output=True)
                # If gradle command exists and works, assume wrapper is generated or can be generated
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Attempt to download/generate wrapper if gradle command is not directly available
                # This part is complex and might require external tools or specific Gradle setup
                print("Warning: Gradle wrapper generation might fail if Gradle is not installed or configured.")
                # For simplicity, we'll assume the user has Gradle installed or will set it up.
                # A more robust solution would download the wrapper scripts.

        # Placeholder for layout files and other resources
        # In a real scenario, these would be generated based on the 'ui' or 'layout'
        # sections of the app_spec.

        self.gradle_wrapper_path = project_path / "gradlew"


    def _process_arabic_nlp_elements(self, app_spec: dict, project_path: Path):
        """
        Processes natural language elements for Arabic support and integrates them
        into the Android project structure (e.g., strings, layouts, code).
        """
        app_name = app_spec.get("name", "MyApp")
        package_name = app_spec.get("package_name", f"com.example.{app_name.lower()}")
        arabic_strings = app_spec.get("arabic_strings", {})

        if arabic_strings:
            strings_dir = project_path / "app" / "src" / "main" / "res"
            # Create values-ar directory for Arabic resources
            ar_values_dir = strings_dir / "values-ar"
            ar_values_dir.mkdir(parents=True, exist_ok=True)
            ar_strings_path = ar_values_dir / "strings.xml"

            root = ET.Element("resources")
            for key, value in arabic_strings.items():
                string_elem = ET.SubElement(root, "string", name=key)
                string_elem.text = value

            tree = ET.ElementTree(root)
            with open(ar_strings_path, "wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=True)

            # Update default strings.xml to include app name in Arabic if specified
            default_strings_path = strings_dir / "values" / "strings.xml"
            if default_strings_path.exists():
                tree = ET.parse(default_strings_path)
                root = tree.getroot()
                app_name_elem = root.find("./string[@name='app_name']")
                if app_name_elem is not None and "app_name_arabic" in arabic_strings:
                    # Assuming the default app_name needs to be overridden or complemented
                    # For simplicity, we'll just ensure app_name_arabic is added if present
                    pass # Logic for overriding app name might be more complex

                # Add other Arabic strings to the default if not already handled by values-ar
                for key, value in arabic_strings.items():
                    if key not in [s.get("name") for s in root.findall("./string")]:
                         string_elem = ET.SubElement(root, "string", name=key)
                         string_elem.text = value

                with open(default_strings_path, "wb") as f:
                    tree.write(f, encoding="utf-8", xml_declaration=True)


        # Further integration could involve:
        # - Parsing layout specifications for RTL support.
        # - Generating Java/Kotlin code that handles Arabic text display, input, etc.
        # - Incorporating Arabic fonts.

    def generate_apk_from_spec(self, app_spec: dict) -> str | None:
        """
        Generates an APK from a natural language app specification.
        """
        app_name = app_spec.get("name", "MyApp").replace(" ", "")
        package_name = app_spec.get("package_name", f"com.example.{app_name.lower()}")
        project_dir_name = f"{app_name}_{package_name.replace('.', '_')}"
        project_path = self.app_spec_dir / project_dir_name

        print(f"Generating Android project structure for '{app_name}' at: {project_path}")
        try:
            self._generate_android_project_structure(app_spec, project_path)
            self._process_arabic_nlp_elements(app_spec, project_path)

            if not self.gradle_wrapper_path or not self.gradle_wrapper_path.exists():
                 # Attempt to create wrapper if it doesn't exist after initial setup
                 # This assumes 'gradle' command is available in PATH
                 try:
                     subprocess.run(["gradle", "wrapper"], cwd=project_path, check=True, capture_output=True)
                     self.gradle_wrapper_path = project_path / "gradlew"
                     if not self.gradle_wrapper_path.exists():
                         raise FileNotFoundError("Gradle wrapper script (gradlew) not found after generation attempt.")
                 except (subprocess.CalledProcessError, FileNotFoundError) as e:
                     print(f"Error creating Gradle wrapper: {e}. Ensure Gradle is installed and in PATH.")
                     return None


            print(f"Building APK for '{app_name}' using Gradle...")
            build_command = [str(self.gradle_wrapper_path), "assembleDebug"]
            result = subprocess.run(build_command, cwd=project_path, check=True, capture_output=True, text=True, encoding='utf-8')

            print("Gradle build output:\n", result.stdout)
            if result.stderr:
                print("Gradle build errors:\n", result.stderr)

            # Find the generated APK
            # The exact path can vary based on Gradle version and setup
            apk_path = None
            potential_apk_dirs = [
                project_path / "app" / "build" / "outputs" / "apk" / "debug",
                project_path / "app" / "build" / "outputs" / "apk" / "release" # less likely for debug build
            ]
            for apk_dir in potential_apk_dirs:
                if apk_dir.exists():
                    for file in apk_dir.glob("*.apk"):
                        if package_name in str(file): # Basic check to ensure it's the correct app
                            apk_path = file
                            break
                if apk_path:
                    break

            if apk_path:
                self.apk_build_dir.mkdir(parents=True, exist_ok=True)
                final_apk_path = self.apk_build_dir / f"{app_name.lower()}_{package_name.replace('.', '_')}.apk"
                import shutil
                shutil.copy(apk_path, final_apk_path)
                print(f"Successfully generated APK for '{app_name}' at: {final_apk_path}")
                return str(final_apk_path)
            else:
                print(f"Error: Could not find generated APK for '{app_name}' in expected locations.")
                return None

        except EnvironmentError as e:
            print(f"Environment setup error: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Dependency not found error: {e}. Make sure JAVA_HOME and ANDROID_SDK_ROOT are set correctly and build tools exist.")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Gradle build failed: {e}")
            print("Stdout:\n", e.stdout)
            print("Stderr:\n", e.stderr)
            return None
        except Exception as e:
            print(f"An unexpected error occurred during APK generation: {e}")
            return None


if __name__ == "__main__":
    # This is a placeholder for demonstration. In a real scenario,
    # these paths and environment variables would be dynamically managed.

    try:
        # Ensure necessary environment variables are set
        ANDROID_HOME = os.environ.get("ANDROID_HOME")
        JAVA_HOME = os.environ.get("JAVA_HOME")

        if not ANDROID_HOME:
            print("Error: ANDROID_HOME environment variable is not set.")
        if not JAVA_HOME:
            print("Error: JAVA_HOME environment variable is not set.")

        if ANDROID_HOME and JAVA_HOME:
            KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
            APK_BUILD_DIR = Path("./build/apk")
            APP_SPEC_DIR = Path("./app_specs")

            # Create directories if they don't exist
            KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
            APK_BUILD_DIR.mkdir(parents=True, exist_ok=True)
            APP_SPEC_DIR.mkdir(parents=True, exist_ok=True)

            print("--- Initializing Arabic APK Builder ---")
            arabic_builder = ArabicAPKBuilder(
                knowledge_base_dir=KNOWLEDGE_BASE_DIR,
                apk_build_dir=APK_BUILD_DIR,
                app_spec_dir=APP_SPEC_DIR,
                android_home=ANDROID_HOME,
                java_home=JAVA_HOME
            )

            # Define a sample Arabic app specification
            sample_app_spec_arabic = {
                "name": "ArabicGreetingApp",
                "package_name": "com.example.arabicgreeting",
                "min_sdk": 21,
                "target_sdk": 33,
                "compile_sdk": 33,
                "arabic_strings": {
                    "app_name": "تطبيق التحية العربي", # Arabic app name
                    "greeting_message": "أهلاً بك في تطبيقنا!", # Arabic greeting
                    "button_text_hello": "قل مرحباً" # Arabic button text
                },
                # 'ui': { ... } # would define layout elements here
            }

            # Save the spec to a file
            spec_file_path = APP_SPEC_DIR / "arabic_greeting_app_spec.json"
            import json
            with open(spec_file_path, "w", encoding="utf-8") as f:
                json.dump(sample_app_spec_arabic, f, ensure_ascii=False, indent=4)

            print(f"\n--- Generating Arabic APK from spec: {spec_file_path} ---")
            generated_apk_path = arabic_builder.generate_apk_from_spec(sample_app_spec_arabic)

            if generated_apk_path:
                print(f"\nSuccessfully generated Arabic APK at: {generated_apk_path}")
            else:
                print("\nFailed to generate Arabic APK.")

            # --- Second example with different spec ---
            sample_app_spec_arabic_2 = {
                "name": "SimpleCalendar",
                "package_name": "com.example.simplecalendar",
                "min_sdk": 23,
                "target_sdk": 34,
                "compile_sdk": 34,
                "arabic_strings": {
                    "app_name": "التقويم البسيط",
                    "today_button": "اليوم",
                    "next_month_button": "الشهر القادم",
                    "month_names": "يناير,فبراير,مارس,أبريل,مايو,يونيو,يوليو,أغسطس,سبتمبر,أكتوبر,نوفمبر,ديسمبر"
                },
                # 'ui': {
                #     'layout_type': 'linear',
                #     'orientation': 'vertical',
                #     'children': [
                #         {'type': 'TextView', 'id': 'month_title', 'text': '@string/month_names'},
                #         {'type': 'Button', 'id': 'btn_today', 'text': '@string/today_button'}
                #     ]
                # }
            }

            spec_file_path_2 = APP_SPEC_DIR / "simple_calendar_spec.json"
            with open(spec_file_path_2, "w", encoding="utf-8") as f:
                json.dump(sample_app_spec_arabic_2, f, ensure_ascii=False, indent=4)

            print(f"\n--- Generating second Arabic APK from spec: {spec_file_path_2} ---")
            generated_apk_path_2 = arabic_builder.generate_apk_from_spec(sample_app_spec_arabic_2)

            if generated_apk_path_2:
                print(f"\nSuccessfully generated second APK at: {generated_apk_path_2}")
            else:
                print("\nFailed to generate second APK.")

            # Clean up dummy files (optional, for testing)
            # print("\n--- Cleaning up dummy files ---")
            # import shutil
            # try:
            #     shutil.rmtree(APP_SPEC_DIR)
            #     shutil.rmtree(Path("./build"))
            #     print("Dummy files cleaned up.")
            # except OSError as e:
            #     print(f"Error during cleanup: {e}")


            print("\n--- Arabic APK Builder Module Demo Finished ---")

    except EnvironmentError as e:
        print(f"Environment setup error: {e}")
    except FileNotFoundError as e:
        print(f"Dependency not found error: {e}. Make sure JAVA_HOME and ANDROID_SDK_ROOT are set correctly and build tools exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")