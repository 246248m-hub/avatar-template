import os
import shutil

# Assume a simplified structure for demonstration.
# In a real scenario, these would be more complex and dynamic.
class AndroidProjectGenerator:
    def __init__(self, project_name="MyAwesomeApp", package_name="com.example.myawesomeapp"):
        self.project_name = project_name
        self.package_name = package_name
        self.base_dir = f"./{self.project_name}_project"
        self.src_dir = os.path.join(self.base_dir, "app", "src", "main", "java", *self.package_name.split('.'))
        self.res_dir = os.path.join(self.base_dir, "app", "src", "main", "res")
        self.manifest_path = os.path.join(self.base_dir, "app", "src", "main", "AndroidManifest.xml")
        self.build_gradle_path = os.path.join(self.base_dir, "app", "build.gradle")

    def create_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(os.path.join(self.res_dir, "layout"), exist_ok=True)
        os.makedirs(os.path.join(self.res_dir, "values"), exist_ok=True)
        print(f"Created project structure for '{self.project_name}' at '{self.base_dir}'")

    def create_manifest(self):
        """Creates a basic AndroidManifest.xml file."""
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity"
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
        print(f"Created '{self.manifest_path}'")

    def create_build_gradle(self):
        """Creates a basic app/build.gradle file."""
        build_gradle_content = """
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    compileSdk 34 // Use a common compile SDK version

    defaultConfig {
        applicationId "com.example.myawesomeapp" // Placeholder, will be replaced
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
        # Replace placeholder with actual package name
        build_gradle_content = build_gradle_content.replace('"com.example.myawesomeapp"', f'"{self.package_name}"')

        with open(self.build_gradle_path, "w", encoding="utf-8") as f:
            f.write(build_gradle_content)
        print(f"Created '{self.build_gradle_path}'")

    def create_main_activity(self, layout_name="activity_main"):
        """Creates a basic MainActivity.kt file."""
        main_activity_content = f"""
package {self.package_name}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.{layout_name})
    }}
}}
"""
        main_activity_file = os.path.join(self.src_dir, "MainActivity.kt")
        with open(main_activity_file, "w", encoding="utf-8") as f:
            f.write(main_activity_content)
        print(f"Created '{main_activity_file}'")

    def create_layout_file(self, layout_name="activity_main"):
        """Creates a basic layout XML file."""
        layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
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
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_file_path = os.path.join(self.base_dir, "app", "src", "main", "res", "layout", f"{layout_name}.xml")
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"Created layout file: '{layout_file_path}'")

    def create_values_files(self):
        """Creates basic strings.xml and themes.xml files."""
        strings_content = """
<resources>
    <string name="app_name">MyAwesomeApp</string>
</resources>
"""
        strings_file_path = os.path.join(self.base_dir, "app", "src", "main", "res", "values", "strings.xml")
        with open(strings_file_path, "w", encoding="utf-8") as f:
            f.write(strings_content)
        print(f"Created strings file: '{strings_file_path}'")

        themes_content = """
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">#008577</item>
        <item name="colorOnPrimary">#FFFFFF</item>
        <item name="colorSecondary">#03DAC5</item>
        <item name="colorOnSecondary">#000000</item>
        <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryVariant</item>
    </style>
</resources>
"""
        themes_file_path = os.path.join(self.base_dir, "app", "src", "main", "res", "values", "themes.xml")
        with open(themes_file_path, "w", encoding="utf-8") as f:
            f.write(themes_content)
        print(f"Created themes file: '{themes_file_path}'")

    def generate_project(self, project_name="GeneratedApp", package_name="com.generated.app"):
        """Orchestrates the creation of a complete Android project structure."""
        self.project_name = project_name
        self.package_name = package_name
        self.base_dir = f"./{self.project_name}_project"
        self.src_dir = os.path.join(self.base_dir, "app", "src", "main", "java", *self.package_name.split('.'))
        self.res_dir = os.path.join(self.base_dir, "app", "src", "main", "res")
        self.manifest_path = os.path.join(self.base_dir, "app", "src", "main", "AndroidManifest.xml")
        self.build_gradle_path = os.path.join(self.base_dir, "app", "build.gradle")


        if os.path.exists(self.base_dir):
            print(f"Project directory '{self.base_dir}' already exists. Removing and recreating.")
            shutil.rmtree(self.base_dir)

        self.create_project_structure()
        self.create_manifest()
        self.create_build_gradle()
        self.create_main_activity()
        self.create_layout_file()
        self.create_values_files()
        print(f"\n--- Android Project '{project_name}' Generation Complete ---")
        print(f"Project created at: {self.base_dir}")
        return self.base_dir


class ArabicAndroidProjectGenerator(AndroidProjectGenerator):
    def __init__(self, project_name="ArabicApp", package_name="com.example.arabicapp"):
        super().__init__(project_name, package_name)
        self.res_values_dir = os.path.join(self.base_dir, "app", "src", "main", "res")

    def create_arabic_layout_file(self, layout_name="activity_main"):
        """Creates a layout XML file with basic Arabic support."""
        arabic_layout_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity"
    android:layoutDirection="rtl"> {/* Added for Right-to-Left direction */}

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="مرحباً بالعالم!"  # Arabic for "Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        # Ensure the correct resource directory for Arabic is used if specific locale is needed
        # For general RTL, it can be in the default layout folder.
        layout_file_path = os.path.join(self.res_values_dir, "layout", f"{layout_name}.xml")
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(arabic_layout_content)
        print(f"Created Arabic layout file: '{layout_file_path}'")

    def create_arabic_strings(self):
        """Creates strings.xml with Arabic string resources."""
        arabic_strings_content = """
<resources>
    <string name="app_name">تطبيق عربي</string> {/* Arabic for "Arabic App" */}
</resources>
"""
        strings_file_path = os.path.join(self.res_values_dir, "values", "strings.xml")
        with open(strings_file_path, "w", encoding="utf-8") as f:
            f.write(arabic_strings_content)
        print(f"Created Arabic strings file: '{strings_file_path}'")

        # Create a values-ar directory for Arabic specific resources if needed for full localization
        # For this example, we'll update the default strings.xml
        # If you want separate files:
        # arabic_values_dir = os.path.join(self.res_values_dir, "values-ar")
        # os.makedirs(arabic_values_dir, exist_ok=True)
        # arabic_strings_file_path = os.path.join(arabic_values_dir, "strings.xml")
        # with open(arabic_strings_file_path, "w", encoding="utf-8") as f:
        #     f.write(arabic_strings_content)
        # print(f"Created Arabic strings file in values-ar: '{arabic_strings_file_path}'")

    def generate_arabic_project(self, project_name="GeneratedArabicApp", package_name="com.generated.arabic"):
        """Orchestrates the creation of an Arabic-enabled Android project."""
        print("\n--- Initiating Arabic Android Project Generation ---")
        generated_project_path = self.generate_project(project_name, package_name)

        # Overwrite default layout and strings with Arabic versions
        self.create_arabic_layout_file()
        self.create_arabic_strings()

        # Update Manifest for RTL if not already handled by android:layoutDirection="rtl" in layout
        # This is often automatic with modern Android Studio and correct layout settings.
        # If explicit manifest tag is needed:
        # e.g., <application android:supportsRtl="true" ...>
        # The current manifest already includes android:supportsRtl="true".

        print(f"\n--- Arabic Android Project '{project_name}' Generation Complete ---")
        print(f"Project created at: {generated_project_path}")
        return generated_project_path

# Example of how to use this module (this part would not be in the final output)
if __name__ == "__main__":
    generator = ArabicAndroidProjectGenerator()
    project_path = generator.generate_arabic_project(project_name="MyArabicApp", package_name="com.example.myarabicapp")

    # Optional: Clean up the generated project directory
    # cleanup_choice = input("Do you want to clean up the generated project directory? (y/n): ")
    # if cleanup_choice.lower() == 'y':
    #     if os.path.exists(project_path):
    #         shutil.rmtree(project_path)
    #         print(f"Cleaned up directory: {project_path}")