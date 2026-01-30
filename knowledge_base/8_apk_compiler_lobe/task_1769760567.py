import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# Define constants for paths and project structure
JAVA_HOME = os.environ.get("JAVA_HOME")
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
GRADLE_HOME = os.environ.get("GRADLE_HOME")

if not all([JAVA_HOME, ANDROID_SDK_ROOT, GRADLE_HOME]):
    raise EnvironmentError("JAVA_HOME, ANDROID_SDK_ROOT, and GRADLE_HOME must be set.")

GRADLE_EXECUTABLE = Path(GRADLE_HOME) / "bin" / "gradle"
ANDROID_GRADLE_PLUGIN_VERSION = "7.4.2"  # Example version
KOTLIN_VERSION = "1.6.21"  # Example version
TARGET_SDK_VERSION = 33
COMPILE_SDK_VERSION = 33
MIN_SDK_VERSION = 21

class ApkCompilerError(Exception):
    """Custom exception for APK compilation errors."""
    pass

class ApkBuilder:
    """
    A module responsible for building an Android APK from a given project structure.
    It leverages Gradle for the build process.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.build_output_dir = self.project_root / "app" / "build" / "outputs" / "apk"

    def _run_gradle_command(self, command: List[str]):
        """Executes a Gradle command within the project directory."""
        if not GRADLE_EXECUTABLE.exists():
            raise ApkCompilerError(f"Gradle executable not found at {GRADLE_EXECUTABLE}")

        env = os.environ.copy()
        env["JAVA_HOME"] = JAVA_HOME
        env["ANDROID_HOME"] = ANDROID_SDK_ROOT
        env["PATH"] = f"{env['PATH']}:{GRADLE_HOME}/bin"

        try:
            process = subprocess.run(
                [str(GRADLE_EXECUTABLE), *command],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            print(f"Gradle command '{' '.join(command)}' successful.")
            print(f"Stdout:\n{process.stdout}")
            if process.stderr:
                print(f"Stderr:\n{process.stderr}")
        except subprocess.CalledProcessError as e:
            raise ApkCompilerError(
                f"Gradle command '{' '.join(command)}' failed with exit code {e.returncode}.\n"
                f"Stdout:\n{e.stdout}\n"
                f"Stderr:\n{e.stderr}"
            ) from e
        except FileNotFoundError:
            raise ApkCompilerError(f"Gradle executable not found. Ensure GRADLE_HOME is set correctly.")


    def create_project_structure(self, app_name: str, package_name: str, main_activity_name: str = "MainActivity"):
        """
        Creates a basic Android project structure with Gradle build files.
        """
        # Create root project directory
        self.project_root.mkdir(parents=True, exist_ok=True)

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

rootProject.name = "{app_name}"
include ':app'
"""
        (self.project_root / "settings.gradle").write_text(settings_gradle_content)

        # Create build.gradle (project level)
        project_build_gradle_content = f"""
plugins {{
    id 'com.android.application' version '{ANDROID_GRADLE_PLUGIN_VERSION}' apply false
    id 'org.jetbrains.kotlin.android' version '{KOTLIN_VERSION}' apply false
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
"""
        (self.project_root / "build.gradle").write_text(project_build_gradle_content)

        # Create app module directory
        app_dir = self.project_root / "app"
        app_dir.mkdir(exist_ok=True)

        # Create app/build.gradle
        app_build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{package_name}'
    compileSdk {COMPILE_SDK_VERSION}

    defaultConfig {{
        applicationId "{package_name}"
        minSdk {MIN_SDK_VERSION}
        targetSdk {TARGET_SDK_VERSION}
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
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        (app_dir / "build.gradle").write_text(app_build_gradle_content)

        # Create app/proguard-rules.pro
        (app_dir / "proguard-rules.pro").write_text("-dontwarn **")

        # Create app/src/main directory
        main_src_dir = app_dir / "src" / "main"
        main_src_dir.mkdir(parents=True, exist_ok=True)

        # Create AndroidManifest.xml
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
        android:theme="@style/Theme.{app_name}"
        tools:targetApi="31">
        <activity
            android:name=".{main_activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
        (main_src_dir / "AndroidManifest.xml").write_text(manifest_content)

        # Create res/values/strings.xml
        res_values_dir = main_src_dir / "res" / "values"
        res_values_dir.mkdir(parents=True, exist_ok=True)
        strings_xml_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
        (res_values_dir / "strings.xml").write_text(strings_xml_content)

        # Create res/values/themes.xml
        themes_xml_content = f"""
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.{app_name}" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
        <!-- Secondary brand color. -->
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <!-- Status bar color. -->
        <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
        <!-- Customize theme elements for Material Components -->
        <item name="materialAlertDialogTheme">@style/ThemeOverlay.App.MaterialAlertDialog</item>
    </style>

    <!-- MaterialAlertDialog theme -->
    <style name="ThemeOverlay.App.MaterialAlertDialog" parent="ThemeOverlay.Material3.MaterialAlertDialog.Centered">
        <item name="materialAlertDialogTitleTextStyle">@style/MaterialAlertDialog.App.Title.Text</item>
        <item name="materialAlertDialogBodyTextStyle">@style/MaterialAlertDialog.App.Body.Text</item>
        <item name="buttonBarPositiveButtonStyle">@style/PositiveButton.App.MaterialAlert</item>
        <item name="buttonBarNegativeButtonStyle">@style/NegativeButton.App.MaterialAlert</item>
        <item name="buttonBarNeutralButtonStyle">@style/NeutralButton.App.MaterialAlert</item>
    </style>
    <style name="MaterialAlertDialog.App.Title.Text" parent="MaterialAlertDialog.MaterialComponents.Title.Text">
        <item name="android:textSize">20sp</item>
        <item name="android:textStyle">bold</item>
    </style>
    <style name="MaterialAlertDialog.App.Body.Text" parent="MaterialAlertDialog.MaterialComponents.Body.Text">
        <item name="android:textSize">14sp</item>
    </style>
    <style name="PositiveButton.App.MaterialAlert" parent="Widget.MaterialComponents.Button.TextButton.Dialog">
        <item name="android:textColor">@color/purple_500</item>
        <item name="android:textStyle">bold</item>
    </style>
    <style name="NegativeButton.App.MaterialAlert" parent="Widget.MaterialComponents.Button.TextButton.Dialog">
        <item name="android:textColor">@color/purple_500</item>
    </style>
    <style name="NeutralButton.App.MaterialAlert" parent="Widget.MaterialComponents.Button.TextButton.Dialog">
        <item name="android:textColor">@color/teal_700</item>
    </style>
</resources>
"""
        (res_values_dir / "themes.xml").write_text(themes_xml_content)

        # Create res/values/colors.xml
        colors_xml_content = """
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
        (res_values_dir / "colors.xml").write_text(colors_xml_content)

        # Create drawable and mipmap directories with placeholder icons
        for res_type in ["drawable", "mipmap-hdpi", "mipmap-mdpi", "mipmap-xhdpi", "mipmap-xxhdpi", "mipmap-xxxhdpi"]:
            (main_src_dir / "res" / res_type).mkdir(parents=True, exist_ok=True)

        # Create placeholder ic_launcher.png (requires Pillow or similar to generate actual image, using dummy for now)
        # In a real scenario, you'd copy actual icon files.
        (main_src_dir / "res" / "mipmap-hdpi" / "ic_launcher.png").touch()
        (main_src_dir / "res" / "mipmap-mdpi" / "ic_launcher.png").touch()
        (main_src_dir / "res" / "mipmap-xhdpi" / "ic_launcher.png").touch()
        (main_src_dir / "res" / "mipmap-xxhdpi" / "ic_launcher.png").touch()
        (main_src_dir / "res" / "mipmap-xxxhdpi" / "ic_launcher.png").touch()
        (main_src_dir / "res" / "mipmap-hdpi" / "ic_launcher_round.png").touch()
        (main_src_dir / "res" / "mipmap-mdpi" / "ic_launcher_round.png").touch()
        (main_src_dir / "res" / "mipmap-xhdpi" / "ic_launcher_round.png").touch()
        (main_src_dir / "res" / "mipmap-xxhdpi" / "ic_launcher_round.png").touch()
        (main_src_dir / "res" / "mipmap-xxxhdpi" / "ic_launcher_round.png").touch()


        # Create Java/Kotlin source directory
        kotlin_src_dir = main_src_dir / "kotlin" / package_name.replace('.', os.sep)
        kotlin_src_dir.mkdir(parents=True, exist_ok=True)

        # Create MainActivity.kt
        main_activity_content = f"""
package {package_name}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class {main_activity_name} : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main) // Assuming layout file exists
    }}
}}
"""
        (kotlin_src_dir / f"{main_activity_name}.kt").write_text(main_activity_content)

        # Create app/src/main/res/layout/activity_main.xml
        layout_dir = main_src_dir / "res" / "layout"
        layout_dir.mkdir(exist_ok=True)
        activity_main_layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{main_activity_name}">

    <!-- Add your UI elements here -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        (layout_dir / "activity_main.xml").write_text(activity_main_layout_content)


    def build_apk(self, build_type: str = "release") -> Path:
        """
        Builds the Android APK using Gradle.

        Args:
            build_type: The build type (e.g., 'release', 'debug'). Defaults to 'release'.

        Returns:
            The path to the generated APK file.

        Raises:
            ApkCompilerError: If the build process fails.
        """
        print(f"--- Building APK for project: {self.project_root} ---")
        self._run_gradle_command(["clean", build_type])

        # Find the generated APK
        apk_path = None
        expected_apk_dir = self.build_output_dir / build_type
        if expected_apk_dir.exists():
            for item in expected_apk_dir.iterdir():
                if item.is_file() and item.suffix == ".apk":
                    apk_path = item
                    break

        if apk_path:
            print(f"APK successfully built: {apk_path}")
            return apk_path
        else:
            raise ApkCompilerError(f"APK file not found in expected directory: {expected_apk_dir}")

    def clean_project(self):
        """Cleans the build artifacts of the project."""
        print(f"--- Cleaning project: {self.project_root} ---")
        self._run_gradle_command(["clean"])
        print("Project cleaned.")