import os
import subprocess
import json
import xml.etree.ElementTree as ET

class ArabicAPKBuilder:
    def __init__(self, project_root="arabic_apk_project"):
        self.project_root = project_root
        self.manifest_path = os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml")
        self.gradle_build_path = os.path.join(project_root, "app", "build.gradle")
        self.gradle_project_path = os.path.join(project_root, "build.gradle")
        self.settings_gradle_path = os.path.join(project_root, "settings.gradle")

    def create_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "java", "com", "example", "arabicapp"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "res", "values"), exist_ok=True)
        print(f"Project structure created at {self.project_root}")

    def create_manifest(self, app_name="ArabicApp", package_name="com.example.arabicapp"):
        """Creates a basic AndroidManifest.xml file."""
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

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
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"AndroidManifest.xml created at {self.manifest_path}")

        # Add app_name to strings.xml
        strings_xml_path = os.path.join(self.project_root, "app", "src", "main", "res", "values", "strings.xml")
        strings_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
        """
        with open(strings_xml_path, "w", encoding="utf-8") as f:
            f.write(strings_content)
        print(f"strings.xml created at {strings_xml_path}")

    def create_gradle_files(self, min_sdk=21, target_sdk=33, compile_sdk=33, android_gradle_plugin_version="7.3.1", kotlin_version="1.7.10"):
        """Creates basic app/build.gradle, build.gradle, and settings.gradle files."""

        app_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace 'com.example.arabicapp'
    compileSdk {compile_sdk}

    defaultConfig {{
        applicationId "com.example.arabicapp"
        minSdk {min_sdk}
        targetSdk {target_sdk}
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {{
            useSupportLibrary true
        }}
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
    buildFeatures {{
        compose true
    }}
    composeOptions {{
        kotlinCompilerExtensionVersion '1.3.0' // Example version, adjust as needed
    }}
    packagingOptions {{
        resources {{
            excludes += '/META-INF/{'kotlinx-coroutines.kotlin_module'}'
        }}
    }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.5.1'
    implementation 'androidx.activity:activity-compose:1.6.1'
    implementation platform('androidx.compose:compose-bom:2022.10.00')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.4'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.0'
    androidTestImplementation platform('androidx.compose:compose-bom:2022.10.00')
    androidTestImplementation 'androidx.compose.ui:ui-test-junit4'
    debugImplementation 'androidx.compose.ui:ui-tooling'
    debugImplementation 'androidx.compose.ui:ui-test-manifest'
}}
        """
        with open(self.gradle_build_path, "w", encoding="utf-8") as f:
            f.write(app_gradle_content)
        print(f"app/build.gradle created at {self.gradle_build_path}")

        project_gradle_content = f"""
buildscript {{
    ext.kotlin_version = '{kotlin_version}'
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath "com.android.tools.build:gradle:{android_gradle_plugin_version}"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
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
        with open(self.gradle_project_path, "w", encoding="utf-8") as f:
            f.write(project_gradle_content)
        print(f"build.gradle created at {self.gradle_project_path}")

        settings_gradle_content = f"""
pluginManagement {{
    repositories {{
        gradlePluginPortal()
        google()
        mavenCentral()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "ArabicApp"
include ':app'
        """
        with open(self.settings_gradle_path, "w", encoding="utf-8") as f:
            f.write(settings_gradle_content)
        print(f"settings.gradle created at {self.settings_gradle_path}")


    def create_main_activity(self, app_title="تطبيق عربي"):
        """Creates a basic MainActivity.kt file with Arabic text support."""
        activity_content = f"""
package com.example.arabicapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.sp
import com.example.arabicapp.ui.theme.ArabicAppTheme

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            ArabicAppTheme {{
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {{
                    Greeting(name = "{app_title}")
                }}
            }}
        }}
    }}
}}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {{
    Text(
        text = name,
        modifier = modifier,
        style = MaterialTheme.typography.headlineMedium,
        textAlign = TextAlign.Center,
        fontSize = 32.sp
    )
}}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {{
    ArabicAppTheme {{
        Greeting("{app_title}")
    }}
}}
        """
        java_dir = os.path.join(self.project_root, "app", "src", "main", "java", "com", "example", "arabicapp")
        activity_path = os.path.join(java_dir, "MainActivity.kt")
        with open(activity_path, "w", encoding="utf-8") as f:
            f.write(activity_content)
        print(f"MainActivity.kt created at {activity_path}")

    def build_apk(self):
        """Builds the APK using Gradle wrapper."""
        print(f"Attempting to build APK in {self.project_root}...")
        try:
            # Ensure gradlew exists
            if not os.path.exists(os.path.join(self.project_root, "gradlew")):
                print("Gradle wrapper not found. Attempting to download or create...")
                # This is a simplification. In a real scenario, you'd handle this more robustly.
                subprocess.run(["chmod", "+x", os.path.join(self.project_root, "gradlew")], check=True)
                # Alternatively, a more robust approach would be to use `gradlew wrapper`
                # but this requires a local Gradle installation and might be complex.

            # Ensure gradlew is executable
            if os.name != 'nt': # Not Windows
                subprocess.run(["chmod", "+x", os.path.join(self.project_root, "gradlew")], check=True)

            # Command to build the APK
            # Using assembleDebug for simplicity during development
            result = subprocess.run(
                [os.path.join(self.project_root, "gradlew"), "assembleDebug"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            print("Gradle build stdout:")
            print(result.stdout)
            print("Gradle build stderr:")
            print(result.stderr)

            if result.returncode == 0:
                print("APK build successful!")
                # Find the APK file
                apk_path = None
                for root, dirs, files in os.walk(os.path.join(self.project_root, "app", "build", "outputs", "apk", "debug")):
                    for file in files:
                        if file.endswith(".apk"):
                            apk_path = os.path.join(root, file)
                            break
                    if apk_path:
                        break
                if apk_path:
                    print(f"APK generated at: {apk_path}")
                    return apk_path
                else:
                    print("APK file not found after successful build.")
                    return None
            else:
                print(f"APK build failed with return code {result.returncode}.")
                return None
        except FileNotFoundError:
            print("Error: gradlew not found. Ensure it's present or download it.")
            print("You might need to run './gradlew wrapper' in the project root if you have Gradle installed.")
            return None
        except Exception as e:
            print(f"An error occurred during APK build: {e}")
            return None

    def generate_apk_from_spec(self, app_spec: dict):
        """
        Generates an APK from a high-level app specification.

        Args:
            app_spec (dict): A dictionary containing app specifications.
                             Expected keys: 'app_name', 'package_name', 'title_text_arabic'.
        """
        app_name = app_spec.get('app_name', 'ArabicApp')
        package_name = app_spec.get('package_name', 'com.example.arabicapp')
        title_text_arabic = app_spec.get('title_text_arabic', 'تطبيق عربي')

        print(f"\n--- Generating APK for: {app_name} ({package_name}) ---")

        # 1. Create project structure
        self.create_project_structure()

        # 2. Create AndroidManifest.xml and strings.xml
        self.create_manifest(app_name=app_name, package_name=package_name)

        # 3. Create Gradle files
        self.create_gradle_files() # Using default SDK versions, can be parameterized

        # 4. Create MainActivity.kt with Arabic text
        self.create_main_activity(app_title=title_text_arabic)

        # 5. Build the APK
        apk_path = self.build_apk()

        print(f"--- APK Generation Process for {app_name} Completed ---")
        return apk_path

# Example Usage:
if __name__ == "__main__":
    arabic_builder = ArabicAPKBuilder()

    # Simulate app specification from a previous lobe (e.g., Lobe 6_synthesis_lobe)
    sample_app_spec = {
        "app_name": "تطبيق ترحيبي",
        "package_name": "com.example.welcomearabic",
        "title_text_arabic": "أهلاً بك في تطبيقك الأول!"
    }

    generated_apk_path = arabic_builder.generate_apk_from_spec(sample_app_spec)

    if generated_apk_path:
        print(f"\nSuccessfully generated APK at: {generated_apk_path}")
    else:
        print("\nFailed to generate APK.")

    # Example of another app spec
    sample_app_spec_2 = {
        "app_name": "تطبيق بسيط",
        "package_name": "com.example.simpleapp",
        "title_text_arabic": "تحية عربية"
    }
    # Note: Building another APK would require cleaning or using a different project directory
    # to avoid conflicts. For demonstration, we'll just show the spec.
    print("\n--- Preparing for second APK generation (requires different directory or cleanup) ---")
    # arabic_builder_2 = ArabicAPKBuilder(project_root="arabic_apk_project_2")
    # generated_apk_path_2 = arabic_builder_2.generate_apk_from_spec(sample_app_spec_2)
    # if generated_apk_path_2:
    #     print(f"\nSuccessfully generated second APK at: {generated_apk_path_2}")
    # else:
    #     print("\nFailed to generate second APK.")