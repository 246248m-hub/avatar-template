import os
import shutil
import subprocess
import logging

JAVA_PROJECT_DIR = "generated_java_project"
GRADLEW_SCRIPT = "gradlew"
GRADLEW_PROPERTIES = "gradle.properties"
ANDROID_MAIN_ACTIVITY_TEMPLATE = """
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
"""

ANDROID_MAIN_ACTIVITY_XML_TEMPLATE = """
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
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

ANDROID_GRADLE_BUILD_SCRIPT_TEMPLATE = """
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.myapp"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
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
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""

ANDROID_GRADLE_SETTINGS_SCRIPT_TEMPLATE = """
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "MyApp"
include ':app'
"""

ANDROID_APP_GRADLE_BUILD_SCRIPT_TEMPLATE = """
apply plugin: 'com.android.application'
apply plugin: 'kotlin-android'

android {
    compileSdkVersion 33
    buildToolsVersion "33.0.0" // Example version

    defaultConfig {
        applicationId "com.example.myapp"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    implementation "org.jetbrains.kotlin:kotlin-stdlib:1.7.20" // Example Kotlin version
    implementation "androidx.core:core-ktx:1.9.0"
    implementation "androidx.appcompat:appcompat:1.6.1"
    implementation "com.google.android.material:material:1.11.0"
    implementation "androidx.constraintlayout:constraintlayout:2.1.4"
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""

def setup_android_project_structure(project_dir: str):
    """
    Sets up the basic directory structure for an Android Java project.
    """
    app_dir = os.path.join(project_dir, "app")
    java_dir = os.path.join(app_dir, "src", "main", "java", "com", "example", "myapp")
    res_dir = os.path.join(app_dir, "src", "main", "res")
    layout_dir = os.path.join(res_dir, "layout")
    values_dir = os.path.join(res_dir, "values")

    os.makedirs(java_dir, exist_ok=True)
    os.makedirs(layout_dir, exist_ok=True)
    os.makedirs(values_dir, exist_ok=True)

    # Create dummy AndroidManifest.xml
    manifest_path = os.path.join(app_dir, "src", "main", "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp">
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
""")

    # Create dummy strings.xml
    strings_path = os.path.join(values_dir, "strings.xml")
    with open(strings_path, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">MyApp</string>
</resources>
""")

    # Create dummy themes.xml
    themes_path = os.path.join(values_dir, "themes.xml")
    with open(themes_path, "w", encoding="utf-8") as f:
        f.write("""<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.MyApp" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
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
        <!-- Customize theme here. -->
    </style>
</resources>
""")

    # Create dummy colors.xml
    colors_path = os.path.join(values_dir, "colors.xml")
    with open(colors_path, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
""")

    # Create dummy MainActivity.java
    main_activity_path = os.path.join(java_dir, "MainActivity.java")
    with open(main_activity_path, "w", encoding="utf-8") as f:
        f.write(ANDROID_MAIN_ACTIVITY_TEMPLATE)

    # Create dummy activity_main.xml
    activity_main_layout_path = os.path.join(layout_dir, "activity_main.xml")
    with open(activity_main_layout_path, "w", encoding="utf-8") as f:
        f.write(ANDROID_MAIN_ACTIVITY_XML_TEMPLATE)

    # Create build.gradle (app level)
    app_build_gradle_path = os.path.join(app_dir, "build.gradle")
    with open(app_build_gradle_path, "w", encoding="utf-8") as f:
        f.write(ANDROID_APP_GRADLE_BUILD_SCRIPT_TEMPLATE)

    # Create build.gradle (project level)
    project_build_gradle_path = os.path.join(project_dir, "build.gradle")
    with open(project_build_gradle_path, "w", encoding="utf-8") as f:
        f.write(ANDROID_GRADLE_BUILD_SCRIPT_TEMPLATE)

    # Create settings.gradle
    settings_gradle_path = os.path.join(project_dir, "settings.gradle")
    with open(settings_gradle_path, "w", encoding="utf-8") as f:
        f.write(ANDROID_GRADLE_SETTINGS_SCRIPT_TEMPLATE)

    # Create dummy gradlew and gradlew.bat
    with open(os.path.join(project_dir, GRADLEW_SCRIPT), "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\nexec gradle/wrapper/gradle-wrapper.jar \"$@\"\n")
    os.chmod(os.path.join(project_dir, GRADLEW_SCRIPT), 0o755)

    with open(os.path.join(project_dir, "gradlew.bat"), "w", encoding="utf-8") as f:
        f.write("@echo off\nif not exist \"gradle\\wrapper\\gradle-wrapper.jar\" goto fail\njava -jar \"gradle\\wrapper\\gradle-wrapper.jar\" %*\nexit /b %errorlevel%\n:fail\necho \"ERROR: Gradle wrapper jar not found!\"\nexit /b 1\n")

    # Create gradle directory and wrapper properties
    gradle_wrapper_dir = os.path.join(project_dir, "gradle", "wrapper")
    os.makedirs(gradle_wrapper_dir, exist_ok=True)
    with open(os.path.join(gradle_wrapper_dir, "gradle-wrapper.properties"), "w", encoding="utf-8") as f:
        f.write("distributionBase=GRADLE_USER_HOME\ndistributionUrl=https\x3a\/\/services.gradle.org\/distributions\/gradle-7.5-bin.zip\ndistributionPath=wrapper\/dists\nzipStorePath=wrapper\/dists\n")

    # Create proguard-rules.pro
    proguard_rules_path = os.path.join(app_dir, "proguard-rules.pro")
    with open(proguard_rules_path, "w", encoding="utf-8") as f:
        f.write("-keep public class * extends java.lang.Throwable\n-keep public interface {}")

    # Create dummy ic_launcher and ic_launcher_round
    icon_dir = os.path.join(res_dir, "mipmap-hdpi")
    os.makedirs(icon_dir, exist_ok=True)
    with open(os.path.join(icon_dir, "ic_launcher.png"), "w") as f: # Dummy file, replace with actual icon
        pass
    with open(os.path.join(icon_dir, "ic_launcher_round.png"), "w") as f: # Dummy file, replace with actual icon
        pass

    logging.info(f"Android project structure created at {project_dir}")


def build_apk(project_path: str) -> bool:
    """
    Builds an APK for the Android project using Gradle.
    Returns True if successful, False otherwise.
    """
    logging.info(f"Attempting to build APK for project at: {project_path}")
    gradlew_path = os.path.join(project_path, GRADLEW_SCRIPT)

    if not os.path.exists(gradlew_path):
        logging.error(f"Gradle wrapper script not found at: {gradlew_path}")
        return False

    try:
        # Execute the Gradle build command
        # 'assembleDebug' or 'assembleRelease' can be used depending on the need
        # For this demo, we'll use 'assembleDebug'
        command = [f"./{GRADLEW_SCRIPT}", "assembleDebug"]
        logging.info(f"Executing command: {' '.join(command)} in {project_path}")

        process = subprocess.Popen(command, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            logging.info("APK build successful.")
            logging.info(f"Gradle stdout:\n{stdout}")
            # You can parse stdout to find the APK path if needed
            # Example: Look for "Build successful." and then find the .apk file
            return True
        else:
            logging.error(f"APK build failed with return code {process.returncode}.")
            logging.error(f"Gradle stdout:\n{stdout}")
            logging.error(f"Gradle stderr:\n{stderr}")
            return False

    except FileNotFoundError:
        logging.error("Could not find the 'gradlew' command. Ensure it's executable and in the PATH or project directory.")
        return False
    except Exception as e:
        logging.error(f"An error occurred during the APK build process: {e}")
        return False


def cleanup_generated_project(project_dir: str):
    """
    Removes the generated Android project directory.
    """
    if os.path.exists(project_dir):
        try:
            shutil.rmtree(project_dir)
            logging.info(f"Cleaned up generated project directory: {project_dir}")
        except OSError as e:
            logging.error(f"Error removing directory {project_dir}: {e}")

# --- Lobe 7_apk_builder_lobe Functionality ---

class APKBuilder:
    """
    Manages the creation and building of Android APKs.
    """
    def __init__(self, output_dir: str = "output_apks"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_apk_from_code(self, java_code: str, package_name: str = "com.example.generatedapp"):
        """
        Creates a new Android project structure, writes the provided Java code
        (assuming it's for MainActivity), and attempts to build an APK.

        Args:
            java_code: The Java code content for MainActivity.
            package_name: The package name for the Android application.

        Returns:
            The path to the generated APK if successful, None otherwise.
        """
        generated_project_path = os.path.join(JAVA_PROJECT_DIR) # Using a fixed directory for simplicity in this demo
        cleanup_generated_project(generated_project_path) # Clean up previous runs

        logging.info(f"Setting up Android project structure at: {generated_project_path}")
        setup_android_project_structure(generated_project_path)

        # Write the provided Java code into MainActivity.java
        java_file_path = os.path.join(generated_project_path, "app", "src", "main", "java", *package_name.split('.'))
        os.makedirs(java_file_path, exist_ok=True)
        main_activity_path = os.path.join(java_file_path, "MainActivity.java")
        try:
            with open(main_activity_path, "w", encoding="utf-8") as f:
                f.write(java_code)
            logging.info(f"Wrote Java code to: {main_activity_path}")
        except IOError as e:
            logging.error(f"Error writing Java code to {main_activity_path}: {e}")
            return None

        # Update package name in relevant files if necessary (simplified here, full implementation requires parsing build.gradle, manifest, etc.)
        # For now, we assume the provided java_code has the correct package declaration or it can be managed externally.

        logging.info("Attempting to build the APK...")
        if build_apk(generated_project_path):
            logging.info("APK build process completed.")
            # Find the generated APK
            apk_dir = os.path.join(generated_project_path, "app", "build", "outputs", "apk", "debug")
            for file in os.listdir(apk_dir):
                if file.endswith(".apk"):
                    apk_path = os.path.join(apk_dir, file)
                    logging.info(f"Generated APK found at: {apk_path}")
                    # Optionally copy the APK to the output directory
                    dest_apk_path = os.path.join(self.output_dir, f"{package_name.replace('.', '_')}.apk")
                    try:
                        shutil.copy(apk_path, dest_apk_path)
                        logging.info(f"Copied APK to: {dest_apk_path}")
                        return dest_apk_path
                    except shutil.Error as e:
                        logging.error(f"Error copying APK from {apk_path} to {dest_apk_path}: {e}")
                        return apk_path # Return original path if copy fails
            logging.warning("Could not find the generated APK file in the expected directory.")
            return None
        else:
            logging.error("APK build failed.")
            return None

    def build_from_natural_language(self, natural_language_description: str) -> str | None:
        """
        This is a placeholder for Lobe 7's core functionality.
        It would parse the natural language description, extract intent,
        generate Java code for MainActivity, and then call create_apk_from_code.

        For demonstration purposes, this method will simulate the process.
        """
        logging.info(f"--- Lobe 7_apk_builder_lobe: Received instruction ---")
        logging.info(f"Natural language description: '{natural_language_description}'")

        # --- Simulation of NLP to Java Code Generation ---
        # In a real system, Lobe 0 (Arabic Lobe) and Lobe 4 (Code Generation Lobe)
        # would work together here.
        # For this example, we'll assume a simple mapping or use a hardcoded response.

        simulated_package_name = "com.example.simpleapp"
        simulated_java_code = ANDROID_MAIN_ACTIVITY_TEMPLATE # Default to a basic template
        simulated_app_name = "SimpleApp"

        if "hello world" in natural_language_description.lower():
            simulated_java_code = """
package com.example.simpleapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView textView = findViewById(R.id.messageTextView);
        textView.setText("Hello from Arabic NLP!");
    }
}
"""
            # Update activity_main.xml to include a TextView with an ID
            activity_main_xml_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "layout", "activity_main.xml")
            with open(activity_main_xml_path, "w", encoding="utf-8") as f:
                f.write("""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/messageTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
            logging.info("Simulated generation of 'Hello World' app code.")

        elif "calculate sum" in natural_language_description.lower() and "of 5 and 7" in natural_language_description.lower():
            simulated_java_code = """
package com.example.simpleapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        int num1 = 5;
        int num2 = 7;
        int sum = num1 + num2;

        TextView textView = findViewById(R.id.resultTextView);
        textView.setText("The sum of " + num1 + " and " + num2 + " is: " + sum);
    }
}
"""
            # Update activity_main.xml to include a TextView with an ID
            activity_main_xml_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "layout", "activity_main.xml")
            with open(activity_main_xml_path, "w", encoding="utf-8") as f:
                f.write("""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/resultTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Calculating..."
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
            logging.info("Simulated generation of 'calculate sum' app code.")

        elif "arabic greeting" in natural_language_description.lower():
            simulated_package_name = "com.example.arabicapp"
            simulated_app_name = "ArabicGreetingApp"
            simulated_java_code = """
package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView textView = findViewById(R.id.greetingTextView);
        textView.setText("السلام عليكم!"); // Assalamu alaikum!
    }
}
"""
            # Update activity_main.xml to include a TextView with an ID
            activity_main_xml_path = os.path.join(JAVA_PROJECT_DIR, "app", "src", "main", "res", "layout", "activity_main.xml")
            with open(activity_main_xml_path, "w", encoding="utf-8") as f:
                f.write("""<?xml version="1.0" encoding="utf-8"?>
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
        android:text="Loading greeting..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
            logging.info("Simulated generation of 'Arabic Greeting' app code.")
        else:
            logging.warning("Natural language description not understood for complex simulation. Using default template.")
            simulated_java_code = ANDROID_MAIN_ACTIVITY_TEMPLATE
            simulated_package_name = "com.example.defaultapp"
            simulated_app_name = "DefaultApp"

        # --- End Simulation ---

        logging.info("Calling create_apk_from_code with simulated Java code...")
        apk_path = self.create_apk_from_code(simulated_java_code, package_name=simulated_package_name)

        if apk_path:
            logging.info(f"Successfully generated APK: {apk_path}")
            return apk_path
        else:
            logging.error("Failed to generate APK.")
            return None

    def cleanup(self):
        """
        Cleans up the generated project directory.
        """
        logging.info("--- Cleaning up APK builder resources ---")
        cleanup_generated_project(JAVA_PROJECT_DIR)


if __name__ == '__main__':
    print("--- Lobe 7_apk_builder_lobe Demo ---")

    # Initialize the APK Builder
    apk_builder = APKBuilder()

    # Demo 1: Build a simple "Hello World" app from a natural language instruction
    print("\n--- Demo 1: Building 'Hello World' App ---")
    nl_instruction_1 = "Create an Android app that displays 'Hello from Arabic NLP!'"
    apk_path_1 = apk_builder.build_from_natural_language(nl_instruction_1)
    if apk_path_1:
        print(f"APK generated for '{nl_instruction_1}': {apk_path_1}")
    else:
        print(f"Failed to generate APK for '{nl_instruction_1}'.")

    # Demo 2: Build a simple calculator app from a natural language instruction
    print("\n--- Demo 2: Building 'Calculate Sum' App ---")
    nl_instruction_2 = "I need an app that can calculate the sum of 5 and 7 and show the result."
    apk_path_2 = apk_builder.build_from_natural_language(nl_instruction_2)
    if apk_path_2:
        print(f"APK generated for '{nl_instruction_2}': {apk_path_2}")
    else:
        print(f"Failed to generate APK for '{nl_instruction_2}'.")

    # Demo 3: Build an app with an Arabic greeting
    print("\n--- Demo 3: Building 'Arabic Greeting' App ---")
    nl_instruction_3 = "Generate an app that shows an Arabic greeting: السلام عليكم!"
    apk_path_3 = apk_builder.build_from_natural_language(nl_instruction_3)
    if apk_path_3:
        print(f"APK generated for '{nl_instruction_3}': {apk_path_3}")
    else:
        print(f"Failed to generate APK for '{nl_instruction_3}'.")

    # Demo 4: Build a default app if the instruction is not recognized
    print("\n--- Demo 4: Building Default App (Unrecognized Instruction) ---")
    nl_instruction_4 = "This is a test instruction that should not be matched."
    apk_path_4 = apk_builder.build_from_natural_language(nl_instruction_4)
    if apk_path_4:
        print(f"APK generated for '{nl_instruction_4}': {apk_path_4}")
    else:
        print(f"Failed to generate APK for '{nl_instruction_4}'.")

    # Final cleanup
    apk_builder.cleanup()
    print("\n--- Lobe 7_apk_builder_lobe Demo Finished ---")