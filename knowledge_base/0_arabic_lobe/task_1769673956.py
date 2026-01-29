import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Assume these are defined in other lobes or globally
# For now, let's define dummy versions for demonstration
class ProjectStructure:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.src_dir = root_dir / "src"
        self.manifest_path = root_dir / "AndroidManifest.xml"
        self.gradle_build_file = root_dir / "build.gradle"
        self.app_gradle_file = self.src_dir / "app" / "build.gradle"
        self.java_dir = self.src_dir / "app" / "src" / "main" / "java"
        self.res_dir = self.src_dir / "app" / "src" / "main" / "res"
        self.assets_dir = self.src_dir / "app" / "src" / "main" / "assets"

    def create_directories(self):
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.src_dir.mkdir(parents=True, exist_ok=True)
        self.java_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def create_default_files(self, package_name: str):
        self.manifest_path.write_text(self._generate_manifest(package_name))
        self.gradle_build_file.write_text(self._generate_gradle_build())
        self.app_gradle_file.write_text(self._generate_app_gradle(package_name))

    def _generate_manifest(self, package_name: str) -> str:
        return f"""<?xml version="1.0" encoding="utf-8"?>
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

    def _generate_gradle_build(self) -> str:
        return """buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.0.4' // Example version
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
"""

    def _generate_app_gradle(self, package_name: str) -> str:
        return f"""plugins {{
    id 'com.android.application'
    id 'kotlin-android'
}}

android {{
    namespace '{package_name}'
    compileSdk 33 // Example version

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21 // Example version
        targetSdk 33 // Example version
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
    implementation 'androidx.core:core-ktx:1.8.0' // Example version
    implementation 'androidx.appcompat:appcompat:1.6.1' // Example version
    implementation 'com.google.android.material:material:1.9.0' // Example version
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4' // Example version
    testImplementation 'junit:junit:4.13.2' // Example version
    androidTestImplementation 'androidx.test.ext:junit:1.1.5' // Example version
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1' // Example version
}}
"""

class ArabicProjectBuilder:
    """
    Lobe responsible for constructing a basic Android project structure
    and integrating Arabic language-specific components.
    """

    def __init__(self, output_dir: Path = Path("./generated_apk_project")):
        self.output_dir = output_dir
        self.project_structure: Optional[ProjectStructure] = None

    def build_project_structure(self, app_name: str = "MyApp", package_name: str = "com.example.myapp") -> ProjectStructure:
        """
        Creates the fundamental directory and file structure for an Android project.
        """
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        project_structure = ProjectStructure(self.output_dir)
        project_structure.create_directories()
        project_structure.create_default_files(package_name)

        # Create dummy resources for Arabic support
        arabic_strings_path = project_structure.res_dir / "values-ar" / "strings.xml"
        arabic_strings_path.parent.mkdir(parents=True, exist_ok=True)
        arabic_strings_path.write_text(self._generate_arabic_strings(app_name))

        # Create a dummy MainActivity in Arabic layout if applicable, or just a basic one
        main_activity_java_path = project_structure.java_dir / package_name.replace('.', os.sep) / "MainActivity.java"
        main_activity_java_path.parent.mkdir(parents=True, exist_ok=True)
        main_activity_java_path.write_text(self._generate_main_activity(package_name))

        # Create a simple layout file that might favor Arabic if the system is set to Arabic
        layout_dir = project_structure.res_dir / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        activity_main_xml_path = layout_dir / "activity_main.xml"
        activity_main_xml_path.write_text(self._generate_activity_main_layout())


        self.project_structure = project_structure
        return project_structure

    def _generate_arabic_strings(self, app_name: str) -> str:
        return f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
    <string name="hello_world">مرحباً بالعالم!</string>
    <string name="change_language">تغيير اللغة</string>
</resources>
"""

    def _generate_main_activity(self, package_name: str) -> str:
        return f"""package {package_name};

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText(R.string.hello_world); // This will pick up Arabic string if system locale is Arabic
    }}
}}
"""

    def _generate_activity_main_layout(self) -> str:
        return f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textDirection="locale"
        android:gravity="center"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

    def add_arabic_nlp_features(self, natural_language_instructions: str):
        """
        Placeholder for future integration of Arabic NLP capabilities.
        This would involve parsing instructions and modifying project files
        accordingly (e.g., adding Arabic text views, input fields, or
        integrating specific Arabic libraries).
        """
        if not self.project_structure:
            raise RuntimeError("Project structure not built yet. Call build_project_structure first.")

        print(f"\n--- Integrating Arabic NLP Features ---")
        print(f"Processing instructions: '{natural_language_instructions}'")
        # In a real scenario, this would involve:
        # 1. Parsing natural_language_instructions using an Arabic NLP model.
        # 2. Identifying elements to add or modify (e.g., "add a button with text 'Click Me'").
        # 3. Generating corresponding XML for layouts or Java/Kotlin code.
        # 4. Adding these generated components to the project structure (e.g., res/layout, src/...).
        print("Placeholder: Arabic NLP features integration logic would go here.")
        print("This might involve dynamically creating or modifying layout files and code based on NLP input.")

    def generate_apk_project(self, natural_language_description: str) -> Path:
        """
        The main function to build the APK project from a natural language description.
        This function orchestrates the building of the project structure and
        the integration of NLP features.
        """
        # Basic parsing of description to get app name and package name
        # In a real scenario, this would be much more sophisticated NLP.
        app_name_guess = "MyArabicApp"
        package_name_guess = "com.example.myarabicapp"

        # Simple extraction: if "app named X" or "package Y" is found
        if "app named" in natural_language_description.lower():
            parts = natural_language_description.lower().split("app named")
            if len(parts) > 1:
                app_name_guess = parts[1].split(" ")[0].strip().capitalize()
                package_name_guess = f"com.example.{app_name_guess.lower()}"
        elif "package" in natural_language_description.lower():
            parts = natural_language_description.lower().split("package")
            if len(parts) > 1:
                package_name_guess = parts[1].split(" ")[0].strip()
                app_name_guess = package_name_guess.split('.')[-1].capitalize()


        print(f"Building project with App Name: '{app_name_guess}', Package: '{package_name_guess}'")
        self.build_project_structure(app_name=app_name_guess, package_name=package_name_guess)

        # Assume the natural language description contains instructions for Arabic NLP features
        self.add_arabic_nlp_features(natural_language_description)

        print(f"\n--- APK Project Generation Complete ---")
        print(f"Project structure generated at: {self.output_dir.resolve()}")
        return self.output_dir.resolve()

# --- Demo ---
if __name__ == "__main__":
    # This part is for demonstration purposes and would typically be
    # triggered by a higher-level Lobe orchestrating the process.

    DUMMY_PROJECT_ROOT = Path("./demo_arabic_project_output")

    try:
        # Clean up previous runs
        if DUMMY_PROJECT_ROOT.exists():
            print(f"Cleaning up previous demo project: {DUMMY_PROJECT_ROOT}")
            shutil.rmtree(DUMMY_PROJECT_ROOT)

        # Instantiate the builder
        builder = ArabicProjectBuilder(output_dir=DUMMY_PROJECT_ROOT)

        # Example natural language description for an Arabic-friendly app
        # This description would be parsed by a more advanced NLP module
        # to extract app name, package, and specific UI/logic requirements.
        nl_description = (
            "Create an Android app named 'My Arabic Translator' with package 'com.mytranslator.arabic'. "
            "The app should greet the user in Arabic and have a button to switch languages."
        )

        print(f"--- Starting ArabicProjectBuilder Demo ---")
        print(f"Input Natural Language Description: '{nl_description}'")

        generated_project_path = builder.generate_apk_project(nl_description)

        print(f"\nDemo successful. Generated project at: {generated_project_path}")
        print("\n--- ArabicProjectBuilder Module Demo Finished ---")

    except Exception as e:
        print(f"\nError during ArabicProjectBuilder demo: {e}")
    finally:
        # Clean up the dummy project after demo
        if DUMMY_PROJECT_ROOT.exists():
            print(f"\n--- Cleaning up dummy project directory: {DUMMY_PROJECT_ROOT} ---")
            shutil.rmtree(DUMMY_PROJECT_ROOT)