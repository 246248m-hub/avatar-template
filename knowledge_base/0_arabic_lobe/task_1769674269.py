import os
import re
import json
import subprocess
import shutil
from pathlib import Path

# Assuming common_utils.py exists and contains necessary helper functions
# like 'extract_apk_info', 'create_dummy_project', 'generate_gradle_files' etc.
# For this example, we'll define some placeholder functions if they are not provided.

def extract_apk_info(project_path: Path) -> dict:
    """
    Placeholder function to simulate extracting APK information from a project.
    In a real scenario, this would parse build files (e.g., build.gradle)
    or the generated APK itself.
    """
    print(f"Simulating extraction of APK info from: {project_path}")
    # Simulate reading some info
    try:
        with open(project_path / "app" / "build.gradle", "r", encoding="utf-8") as f:
            gradle_content = f.read()
            app_name_match = re.search(r"applicationId\s+['\"]([^'\"]+)['\"]", gradle_content)
            version_name_match = re.search(r"versionName\s+['\"]([^'\"]+)['\"]", gradle_content)
            version_code_match = re.search(r"versionCode\s+(\d+)", gradle_content)

            return {
                "application_id": app_name_match.group(1) if app_name_match else "com.example.app",
                "version_name": versionName_match.group(1) if versionName_match else "1.0",
                "version_code": int(versionCode_match.group(1)) if versionCode_match else 1,
                "project_path": str(project_path)
            }
    except FileNotFoundError:
        print("build.gradle not found. Returning default info.")
        return {
            "application_id": "com.example.app.default",
            "version_name": "1.0.default",
            "version_code": 1,
            "project_path": str(project_path)
        }


def create_dummy_project(project_root: Path, package_name: str, app_name: str = "MyApp", version_name: str = "1.0", version_code: int = 1) -> None:
    """
    Creates a basic Android project structure for demonstration.
    """
    print(f"Creating dummy Android project at: {project_root}")
    os.makedirs(project_root / "app" / "src" / "main" / "java" / package_name.replace('.', '/'), exist_ok=True)
    os.makedirs(project_root / "app" / "src" / "main" / "res" / "values", exist_ok=True)

    # Create basic AndroidManifest.xml
    manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package_name}">
    <application android:allowBackup="true" android:label="@string/app_name" android:roundIcon="@mipmap/ic_launcher_round" android:icon="@mipmap/ic_launcher" android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    with open(project_root / "app" / "src" / "main" / "AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # Create strings.xml
    strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    with open(project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml", "w", encoding="utf-8") as f:
        f.write(strings_content)

    # Create MainActivity.java
    main_activity_content = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming activity_main.xml exists (not created here for simplicity)

        TextView textView = findViewById(R.id.textView); // Assuming a TextView with id 'textView' exists
        textView.setText("Hello from {app_name}!");
    }}
}}
"""
    with open(project_root / "app" / "src" / "main" / "java" / package_name.replace('.', '/') / "MainActivity.java", "w", encoding="utf-8") as f:
        f.write(main_activity_content)

    # Create a dummy activity_main.xml (optional but good practice)
    activity_main_content = """
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp" />

</LinearLayout>
"""
    os.makedirs(project_root / "app" / "src" / "main" / "res" / "layout", exist_ok=True)
    with open(project_root / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml", "w", encoding="utf-8") as f:
        f.write(activity_main_content)


    # Create build.gradle for the app module
    app_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin is also used or can be
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId '{package_name}'
        minSdk 24
        targetSdk 34
        versionCode {version_code}
        versionName '{version_name}'
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
    with open(project_root / "app" / "build.gradle", "w", encoding="utf-8") as f:
        f.write(app_gradle_content)

    # Create settings.gradle
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
rootProject.name = "{app_name.replace(' ', '')}"
include ':app'
"""
    with open(project_root / "settings.gradle", "w", encoding="utf-8") as f:
        f.write(settings_gradle_content)

    # Create a dummy build.gradle (project level)
    build_gradle_project_content = f"""
buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath("com.android.tools.build:gradle:8.1.1") // Specify your AGP version
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.10") // Specify your Kotlin version
    }}
}}
allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
"""
    with open(project_root / "build.gradle", "w", encoding="utf-8") as f:
        f.write(build_gradle_project_content)

    print("Dummy project structure created.")


def generate_gradle_files(project_path: Path, package_name: str, app_name: str, version_name: str, version_code: int):
    """
    Generates essential Gradle files for an Android project.
    This is a simplified version of create_dummy_project's Gradle generation.
    """
    print(f"Generating Gradle files for: {project_path}")

    # Ensure app/build.gradle exists and is updated
    app_gradle_path = project_path / "app" / "build.gradle"
    if not app_gradle_path.exists():
        os.makedirs(project_path / "app", exist_ok=True)

    app_gradle_content = f"""
plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId '{package_name}'
        minSdk 24
        targetSdk 34
        versionCode {version_code}
        versionName '{version_name}'
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
    with open(app_gradle_path, "w", encoding="utf-8") as f:
        f.write(app_gradle_content)

    # Ensure settings.gradle exists
    settings_gradle_path = project_path / "settings.gradle"
    if not settings_gradle_path.exists():
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
rootProject.name = "{app_name.replace(' ', '')}"
include ':app'
"""
        with open(settings_gradle_path, "w", encoding="utf-8") as f:
            f.write(settings_gradle_content)

    # Ensure top-level build.gradle exists
    top_level_build_gradle_path = project_path / "build.gradle"
    if not top_level_build_gradle_path.exists():
        build_gradle_project_content = f"""
buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath("com.android.tools.build:gradle:8.1.1") // Specify your AGP version
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.10") // Specify your Kotlin version
    }}
}}
allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
"""
        with open(top_level_build_gradle_path, "w", encoding="utf-8") as f:
            f.write(build_gradle_project_content)

    print("Gradle files ensured/generated.")


def build_apk(project_path: Path, output_dir: Path, task_name: str = "assembleRelease") -> Path:
    """
    Builds an APK for the given Android project using Gradle.
    Returns the path to the generated APK.
    """
    print(f"Attempting to build APK for project at: {project_path} with task: {task_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find the Gradle wrapper executable
    gradle_wrapper_script = "gradlew"
    if os.name == 'nt': # Windows
        gradle_wrapper_script = "gradlew.bat"

    gradlew_path = project_path / gradle_wrapper_script
    if not gradlew_path.exists():
        raise FileNotFoundError(f"Gradle wrapper not found at {gradlew_path}. Make sure the project is properly initialized.")

    # Construct the command
    # Using the Gradle wrapper is the recommended way to build Android projects.
    # We need to run it from the project's root directory.
    command = [
        str(gradlew_path),
        task_name,
        f"-p", str(project_path), # Specify the project directory
        f"--output-dir", str(output_dir), # This might not be directly supported by all Gradle tasks
        f"--project-dir", str(project_path) # Explicitly set project directory
    ]

    # For simplicity and to ensure output goes to a known place, we'll rely on
    # Gradle's default output locations within the build directory.
    # The actual APK path will be determined after the build.

    try:
        # Execute the Gradle build command
        # We'll capture stdout and stderr to diagnose issues
        result = subprocess.run(
            [str(gradlew_path), task_name],
            cwd=str(project_path),  # Run from the project's root directory
            capture_output=True,
            text=True,
            check=True  # Raise an exception if the command fails
        )
        print("Gradle build output:")
        print(result.stdout)
        if result.stderr:
            print("Gradle build error output:")
            print(result.stderr)

        # After successful build, find the APK.
        # The typical location is project_path/app/build/outputs/apk/<build_type>/app-<build_type>.apk
        apk_path = None
        if task_name == "assembleRelease":
            potential_apk_dir = project_path / "app" / "build" / "outputs" / "apk" / "release"
        elif task_name == "assembleDebug":
            potential_apk_dir = project_path / "app" / "build" / "outputs" / "apk" / "debug"
        else: # Fallback for other tasks or if build type is not explicitly "release" or "debug"
             potential_apk_dir = project_path / "app" / "build" / "outputs" / "apk"
             # We might need to be more specific if other tasks are used
             if (project_path / "app" / "build" / "outputs" / "apk" / "release").exists():
                 potential_apk_dir = project_path / "app" / "build" / "outputs" / "apk" / "release"
             elif (project_path / "app" / "build" / "outputs" / "apk" / "debug").exists():
                 potential_apk_dir = project_path / "app" / "build" / "outputs" / "apk" / "debug"


        if potential_apk_dir.exists():
            for item in potential_apk_dir.iterdir():
                if item.is_file() and item.suffix == ".apk":
                    # Copy the APK to the desired output directory
                    final_apk_path = output_dir / item.name
                    shutil.copy2(item, final_apk_path)
                    apk_path = final_apk_path
                    print(f"Successfully built and copied APK to: {apk_path}")
                    return apk_path

        if not apk_path:
             print(f"Warning: Could not find generated APK in expected location: {potential_apk_dir}")
             # Attempt to find any APK in a broader search
             for apk_file in project_path.rglob("*.apk"):
                 if "build" in str(apk_file): # Ensure it's from a build output
                    final_apk_path = output_dir / apk_file.name
                    shutil.copy2(apk_file, final_apk_path)
                    apk_path = final_apk_path
                    print(f"Found and copied an APK to: {apk_path}")
                    return apk_path

        if not apk_path:
            raise FileNotFoundError("APK file not found after successful Gradle build.")

    except subprocess.CalledProcessError as e:
        print(f"Gradle build failed with exit code {e.returncode}")
        print("--- Standard Output ---")
        print(e.stdout)
        print("--- Standard Error ---")
        print(e.stderr)
        raise RuntimeError(f"APK build process failed: {e.stderr}") from e
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during APK build: {e}")
        raise

    return apk_path # Should have returned by now if successful


class ApkCompilerLobe:
    def __init__(self):
        self.name = "apk_compiler_lobe"
        self.last_thought = "Initialized ApkCompilerLobe."
        self.project_root = Path("temp_android_project") # Temporary directory for project
        self.output_apk_dir = Path("generated_apks")

    def _cleanup_project(self):
        """Removes the temporary project directory."""
        if self.project_root.exists():
            print(f"Cleaning up dummy project directory: {self.project_root}")
            shutil.rmtree(self.project_root)

    def compile_apk_from_nlp_output(self, nlp_output: dict) -> Path:
        """
        Takes structured NLP output and compiles an APK.

        Args:
            nlp_output (dict): A dictionary containing structured information
                                derived from natural language, e.g.:
                                {
                                    "package_name": "com.example.myapp",
                                    "app_name": "My Awesome App",
                                    "version_name": "1.2.3",
                                    "version_code": 12,
                                    "features": ["basic_ui", "network_request"], # Simplified
                                    "language": "ar"
                                }

        Returns:
            Path: The path to the generated APK file.
        """
        self.last_thought = "Starting APK compilation process."
        print(f"\n--- {self.name} ---")
        print(f"Received NLP output: {json.dumps(nlp_output, indent=2)}")

        try:
            package_name = nlp_output.get("package_name", f"com.example.{nlp_output.get('app_name', 'app').lower().replace(' ', '')}")
            app_name = nlp_output.get("app_name", "GeneratedApp")
            version_name = nlp_output.get("version_name", "1.0")
            version_code = nlp_output.get("version_code", 1)
            language = nlp_output.get("language", "en") # Used for potential localization later

            if not package_name or not app_name:
                raise ValueError("Package name and App name are required for APK compilation.")

            # 1. Create or prepare the Android project structure
            self._cleanup_project() # Clean up from previous runs
            self.project_root.mkdir(parents=True, exist_ok=True)
            
            # Use a simplified project creation that focuses on essentials for building
            create_dummy_project(self.project_root, package_name, app_name, version_name, version_code)
            # Ensure build files are correctly set up
            generate_gradle_files(self.project_root, package_name, app_name, version_name, version_code)

            # 2. (Placeholder for Lobe 4 - Code Generation)
            # In a real system, Lobe 4 would have generated/modified Java/Kotlin code
            # and resource files based on 'nlp_output["features"]' and 'nlp_output["language"]'.
            # For this demo, we assume 'create_dummy_project' provides a basic structure.
            # If features were more complex, we'd need to inject code here.
            # Example: if "network_request" in nlp_output.get("features", []):
            #             # Inject code for network requests into MainActivity.java or a new class.
            #             pass

            # 3. Build the APK using Gradle
            print("Initiating Gradle build process...")
            self.output_apk_dir.mkdir(parents=True, exist_ok=True)
            generated_apk_path = build_apk(self.project_root, self.output_apk_dir, task_name="assembleRelease") # Or "assembleDebug"

            # 4. Extract APK information (optional, but good for verification)
            apk_info = extract_apk_info(self.project_root)
            print(f"Extracted APK Info: {json.dumps(apk_info, indent=2)}")

            self.last_thought = f"Successfully compiled APK: {generated_apk_path}"
            print(f"--- {self.name} finished successfully ---")
            return generated_apk_path

        except (ValueError, FileNotFoundError, RuntimeError) as e:
            self.last_thought = f"Error during APK compilation: {e}"
            print(f"--- {self.name} encountered an error ---")
            print(f"Error: {e}")
            self._cleanup_project() # Ensure cleanup even on error
            raise # Re-raise the exception for the orchestrator
        except Exception as e:
            self.last_thought = f"An unexpected error occurred: {e}"
            print(f"--- {self.name} encountered an unexpected error ---")
            print(f"Error: {e}")
            self._cleanup_project()
            raise

# Example Usage (for testing this lobe in isolation)
if __name__ == "__main__":
    print("--- Testing ApkCompilerLobe ---")
    compiler_lobe = ApkCompilerLobe()

    # Simulate NLP output for a simple Arabic app
    sample_nlp_output_ar = {
        "package_name": "com.example.arabicdemo",
        "app_name": "تطبيق عربي",
        "version_name": "1.0.1",
        "version_code": 2,
        "language": "ar",
        "features": ["basic_ui", "arabic_text_display"] # Assuming Lobe 4 would handle this
    }

    try:
        # Before running, ensure you have Android SDK and NDK set up and Gradle is available in PATH
        # or the gradlew script is correctly placed within the project.
        # For this demo, we assume 'gradlew' is executable.
        
        # Make sure Android SDK environment variables are set if running outside Android Studio
        # Example:
        # os.environ['ANDROID_HOME'] = '/path/to/your/android/sdk'
        # os.environ['JAVA_HOME'] = '/path/to/your/java/jdk'
        # os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['ANDROID_HOME'] + '/tools:' + os.environ['ANDROID_HOME'] + '/platform-tools'


        print("\n--- Compiling Arabic Demo APK ---")
        apk_path_ar = compiler_lobe.compile_apk_from_nlp_output(sample_nlp_output_ar)
        print(f"\nGenerated APK for Arabic Demo: {apk_path_ar}")

        # Simulate NLP output for a basic English app
        sample_nlp_output_en = {
            "package_name": "com.example.englishapp",
            "app_name": "English App",
            "version_name": "2.5.0",
            "version_code": 25,
            "language": "en",
            "features": ["basic_ui"]
        }

        print("\n--- Compiling English Demo APK ---")
        apk_path_en = compiler_lobe.compile_apk_from_nlp_output(sample_nlp_output_en)
        print(f"\nGenerated APK for English Demo: {apk_path_en}")

    except Exception as e:
        print(f"\n--- DEMO FAILED ---")
        print(f"An error occurred during the demo: {e}")
    finally:
        # Final cleanup
        compiler_lobe._cleanup_project()
        if compiler_lobe.output_apk_dir.exists():
            print(f"Keeping generated APKs in: {compiler_lobe.output_apk_dir}")
            # Optionally clean up APKs if needed: shutil.rmtree(compiler_lobe.output_apk_dir)

    print("\n--- ApkCompilerLobe Demo Finished ---")