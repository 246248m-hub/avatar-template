import os
import subprocess
import shutil
from pathlib import Path

# Define constants for project paths
BASE_PROJECT_DIR = "base_android_project"
SOURCE_DIR = os.path.join(BASE_PROJECT_DIR, "app", "src", "main")
MANIFEST_PATH = os.path.join(SOURCE_DIR, "AndroidManifest.xml")
JAVA_DIR = os.path.join(SOURCE_DIR, "java")
RESOURCES_DIR = os.path.join(SOURCE_DIR, "res")

class ArabicAndroidProjectBuilder:
    """
    A module to build Android APKs with Arabic language support from natural language descriptions.
    """
    def __init__(self, project_name="MyArabicApp"):
        self.project_name = project_name
        self.base_project_path = Path(BASE_PROJECT_DIR)
        self.source_dir = Path(SOURCE_DIR)
        self.manifest_path = Path(MANIFEST_PATH)
        self.java_dir = Path(JAVA_DIR)
        self.resources_dir = Path(RESOURCES_DIR)
        self.app_package_name = f"com.example.{project_name.lower()}"

    def create_base_project_structure(self):
        """
        Creates the basic directory structure for an Android project.
        This is a simplified representation, a real build would use Android Studio's Gradle.
        """
        print(f"Creating base project structure for: {self.project_name}")
        self.base_project_path.mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "main" / "res").mkdir(parents=True, exist_ok=True)
        (self.base_project_path / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)

        # Create a dummy AndroidManifest.xml
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.app_package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyArabicApp">

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
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Create a dummy strings.xml
        strings_content = f"""
<resources>
    <string name="app_name">{self.project_name}</string>
</resources>
"""
        with open(os.path.join(self.resources_dir, "values", "strings.xml"), "w", encoding="utf-8") as f:
            f.write(strings_content)

        print("Base project structure created.")

    def add_arabic_support(self):
        """
        Ensures basic Arabic language support is configured.
        In a real scenario, this would involve adding locale resources and
        potentially specific Arabic fonts or UI adjustments.
        For this simplified module, we assume the base Android setup handles it.
        """
        print("Adding Arabic language support (configuration check).")
        # In a real system, this might involve:
        # 1. Checking/adding Arabic resource directories (e.g., res/values-ar/)
        # 2. Ensuring font support for Arabic characters.
        # For this example, we assume a default configuration is sufficient.
        print("Arabic support configuration check complete.")

    def generate_activity_code(self, activity_name="MainActivity", layout_name="activity_main"):
        """
        Generates a simple Java/Kotlin Activity file.
        This function will be enhanced by Lobe 4_code_generation_lobe.
        """
        activity_package_path = Path(JAVA_DIR) / self.app_package_name.replace('.', os.sep)
        activity_package_path.mkdir(parents=True, exist_ok=True)

        activity_file_content = f"""
package {self.app_package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});

        // Placeholder for dynamic Arabic content
        TextView dynamicText = findViewById(R.id.dynamic_text_view); // Assuming such an ID exists in layout
        if (dynamicText != null) {{
            dynamicText.setText("مرحبا بالعالم"); // Hello World in Arabic
        }}
    }}
}}
"""
        activity_file_path = activity_package_path / f"{activity_name}.java"
        with open(activity_file_path, "w", encoding="utf-8") as f:
            f.write(activity_file_content)
        print(f"Generated Activity: {activity_file_path}")
        return activity_file_path

    def generate_layout_file(self, layout_name="activity_main"):
        """
        Generates a simple XML layout file.
        This function will be enhanced by Lobe 4_code_generation_lobe.
        """
        layout_dir = self.resources_dir / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)

        layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{layout_name.replace('activity_', '').capitalize()}Activity">

    <TextView
        android:id="@+id/dynamic_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_file_path = layout_dir / f"{layout_name}.xml"
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"Generated Layout: {layout_file_path}")
        return layout_file_path

    def build_project(self, output_dir="output_apks"):
        """
        Simulates the building of the APK.
        In a real scenario, this would invoke Gradle.
        This function is a placeholder and relies on external tools or a full SDK setup.
        """
        print("\n--- Simulating APK Build Process ---")
        # This is a highly simplified simulation.
        # A real build would involve:
        # 1. Setting up a Gradle project structure.
        # 2. Running `./gradlew assembleDebug` or `./gradlew assembleRelease`.
        # 3. Handling build dependencies and compilation errors.

        # For demonstration, we'll just create a dummy APK file.
        # A real implementation would call a subprocess like:
        # try:
        #     subprocess.run(["./gradlew", "assembleDebug"], cwd=self.base_project_path, check=True)
        #     print("Gradle build successful.")
        #     # Find the APK file and copy it.
        # except FileNotFoundError:
        #     print("Error: Gradle command not found. Ensure Android SDK and Gradle are installed and in PATH.")
        # except subprocess.CalledProcessError as e:
        #     print(f"Gradle build failed: {e}")
        #     return False

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        dummy_apk_path = output_dir_path / f"{self.project_name.lower().replace(' ', '_')}.apk"

        try:
            # Create a placeholder file to represent the APK
            with open(dummy_apk_path, "w") as f:
                f.write(f"This is a dummy APK file for {self.project_name}.\n")
                f.write("In a real scenario, this would be a compiled Android application.\n")
            print(f"Dummy APK created at: {dummy_apk_path}")
            return True
        except Exception as e:
            print(f"Failed to create dummy APK: {e}")
            return False

    def cleanup_project(self):
        """
        Removes the generated project directory.
        """
        print(f"\n--- Cleaning up project directory: {self.base_project_path} ---")
        if self.base_project_path.exists():
            try:
                shutil.rmtree(self.base_project_path)
                print(f"Successfully removed {self.base_project_path}")
            except OSError as e:
                print(f"Error removing directory {self.base_project_path}: {e}")
        else:
            print(f"Project directory {self.base_project_path} not found, skipping cleanup.")

# Example Usage (for demonstration purposes, will be integrated into the main loop)
if __name__ == "__main__":
    # This section is for demonstrating the ArabicAndroidProjectBuilder module in isolation.
    # It will be replaced by the orchestrated execution from the GRAND OBJECTIVE.

    print("--- ArabicAndroidProjectBuilder Module Demonstration ---")

    builder = ArabicAndroidProjectBuilder(project_name="My Arabic Greeting App")

    # Step 1: Create base project structure
    builder.create_base_project_structure()

    # Step 2: Add Arabic support (simulated)
    builder.add_arabic_support()

    # Step 3: Generate Activity and Layout (will be driven by Lobe 4)
    activity_file = builder.generate_activity_code()
    layout_file = builder.generate_layout_file()

    # Step 4: Simulate APK build (will be driven by Lobe 8)
    apk_built = builder.build_project()

    if apk_built:
        print("\nAPK build simulation successful.")
    else:
        print("\nAPK build simulation failed.")

    # Step 5: Cleanup
    builder.cleanup_project()

    print("\n--- ArabicAndroidProjectBuilder Module Demonstration Finished ---")