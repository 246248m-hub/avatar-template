import os
import shutil
import subprocess
from pathlib import Path

# Assume these are defined elsewhere or will be populated by other lobes
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
DUMMY_PROJECT_ROOT = Path("dummy_android_project")
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
GRADLE_PATH = Path(ANDROID_SDK_ROOT) / "cmdline-tools" / "latest" / "bin" / "gradle" if ANDROID_SDK_ROOT else None

class ArabicProjectBuilder:
    """
    This lobe is responsible for constructing the basic Android project structure
    and populating it with initial Arabic-specific configurations.
    It acts as a bridge between the NLP understanding of the desired APK and
    the actual file system representation of an Android project.
    """

    def __init__(self, project_name: str = "ArabicApp"):
        self.project_name = project_name
        self.project_root = DUMMY_PROJECT_ROOT / project_name
        self.app_module_root = self.project_root / "app"
        self.manifest_path = self.app_module_root / "src" / "main" / "AndroidManifest.xml"
        self.main_activity_path = self.app_module_root / "src" / "main" / "java" / self.get_package_path() / "MainActivity.java"
        self.gradle_build_path = self.app_module_root / "build.gradle"
        self.app_gradle_path = self.project_root / "build.gradle"

    def get_package_name(self) -> str:
        """Generates a default package name based on the project name."""
        # Simple transformation for demonstration. In a real scenario, this
        # might be derived from user input or NLP analysis.
        return f"com.example.{self.project_name.lower().replace(' ', '')}"

    def get_package_path(self) -> Path:
        """Converts the package name into a file system path."""
        return Path(self.get_package_name().replace('.', os.sep))

    def initialize_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        print(f"Initializing project structure at: {self.project_root}")
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.app_module_root.mkdir(parents=True, exist_ok=True)
        (self.app_module_root / "src" / "main" / "java" / self.get_package_path()).mkdir(parents=True, exist_ok=True)
        (self.app_module_root / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
        (self.app_module_root / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)
        (self.project_root / "gradlew").touch()
        (self.project_root / "gradlew.bat").touch()

    def create_gradle_files(self):
        """Creates essential Gradle build files."""
        print("Creating Gradle build files.")

        # Root build.gradle
        root_build_gradle_content = f"""
buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath "com.android.tools.build:gradle:7.0.0" // Example version
    }}
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

task clean(type: Delete) {{
    delete rootProject.buildDir
}}
"""
        with open(self.app_gradle_path, "w", encoding="utf-8") as f:
            f.write(root_build_gradle_content)

        # App module build.gradle
        app_build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'kotlin-android'
}}

android {{
    namespace '{self.get_package_name()}'
    compileSdk 33 // Example SDK version
    defaultConfig {{
        applicationId "{self.get_package_name()}"
        minSdk 21 // Example min SDK
        targetSdk 33 // Example target SDK
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
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1' // Example dependency
    implementation 'com.google.android.material:material:1.10.0' // Example dependency
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4' // Example dependency
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        with open(self.gradle_build_path, "w", encoding="utf-8") as f:
            f.write(app_build_gradle_content)

    def create_manifest(self):
        """Creates the AndroidManifest.xml file with basic configurations."""
        print("Creating AndroidManifest.xml.")
        manifest_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="{self.get_package_name()}">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.ArabicApp"
        tools:targetApi="31">
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

    def create_main_activity(self):
        """Creates a basic MainActivity.java file."""
        print("Creating MainActivity.java.")
        main_activity_content = f"""
package {self.get_package_name()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // TODO: Set layout dynamically based on NLP interpretation
        setContentView(R.layout.activity_main); // Default layout
    }}
}}
"""
        with open(self.main_activity_path, "w", encoding="utf-8") as f:
            f.write(main_activity_content)

    def create_default_resources(self):
        """Creates default layout and values resources."""
        print("Creating default resources.")
        # activity_main.xml
        layout_content = """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/greetingTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="مرحبا بالعالم!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(self.app_module_root / "src" / "main" / "res" / "layout" / "activity_main.xml", "w", encoding="utf-8") as f:
            f.write(layout_content)

        # values/strings.xml
        strings_content = """
<resources>
    <string name="app_name">Arabic App</string>
</resources>
"""
        with open(self.app_module_root / "src" / "main" / "res" / "values" / "strings.xml", "w", encoding="utf-8") as f:
            f.write(strings_content)

        # values/themes.xml (basic theme)
        themes_content = """
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.ArabicApp" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <!-- Primary brand color. -->
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
        <!-- Customize your theme here. -->
    </style>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
        with open(self.app_module_root / "src" / "main" / "res" / "values" / "themes.xml", "w", encoding="utf-8") as f:
            f.write(themes_content)

    def build_project(self) -> Path:
        """
        Constructs the entire Android project structure and files.
        Returns the path to the root of the generated project.
        """
        print("\n--- Initiating Lobe 5: ArabicProjectBuilder ---")
        if self.project_root.exists():
            print(f"Removing existing project at {self.project_root} to start fresh.")
            shutil.rmtree(self.project_root)

        self.initialize_project_structure()
        self.create_gradle_files()
        self.create_manifest()
        self.create_main_activity()
        self.create_default_resources()
        print("Basic Android project structure and core files created.")
        print(f"Project root: {self.project_root}")
        print("\n--- Lobe 5: ArabicProjectBuilder FINISHED ---")
        return self.project_root

# Example Usage (for demonstration purposes, typically called by another lobe)
if __name__ == "__main__":
    # Ensure dummy project directory exists for cleanup later
    DUMMY_PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    try:
        # This is a placeholder for when the user's request is processed and
        # a project name is determined.
        generated_project_path = ArabicProjectBuilder("My Arabic App").build_project()

        # In a real workflow, this path would be passed to the next lobe
        # (e.g., Lobe 8_apk_compiler_lobe)
        print(f"\nSuccessfully built project at: {generated_project_path}")

    except Exception as e:
        print(f"\nError during ArabicProjectBuilder demo: {e}")
    finally:
        # Clean up the dummy project
        if DUMMY_PROJECT_ROOT.exists():
            print(f"\n--- Cleaning up dummy project directory: {DUMMY_PROJECT_ROOT} ---")
            shutil.rmtree(DUMMY_PROJECT_ROOT)