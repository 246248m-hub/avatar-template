import os
import subprocess
import shutil

# Assume these are defined elsewhere and represent your core functionalities
from lobe_0_language_lobe import generate_text_from_prompt  # Simplified representation
from lobe_0_arabic_lobe import parse_arabic_nlp_data, generate_apk_structure_from_arabic

# Constants for project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "app", "src", "main", "java")
MANIFEST_DIR = os.path.join(PROJECT_ROOT, "app", "src", "main")
RES_DIR = os.path.join(PROJECT_ROOT, "app", "src", "main", "res")
BUILD_GRADLE_PATH = os.path.join(PROJECT_ROOT, "app", "build.gradle")
SETTINGS_GRADLE_PATH = os.path.join(PROJECT_ROOT, "settings.gradle")
MAIN_ACTIVITY_TEMPLATE = os.path.join(PROJECT_ROOT, "templates", "MainActivity.java.template")
ANDROID_MANIFEST_TEMPLATE = os.path.join(PROJECT_ROOT, "templates", "AndroidManifest.xml.template")

# --- Lobe 0_language_lobe Integration (Simplified) ---
def get_arabic_code_snippets(prompt: str) -> dict:
    """
    Generates Java code snippets based on Arabic natural language descriptions.
    This is a placeholder for a more sophisticated language lobe integration.
    """
    # In a real scenario, this would call lobe_0_language_lobe.generate_text_from_prompt
    # with appropriate Arabic prompts and parse the output.
    # For this example, we'll return predefined snippets.
    if "Hello World Activity" in prompt:
        return {
            "MainActivity.java": """
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.hello_text);
        textView.setText("مرحباً بالعالم!");
    }
}
"""
        }
    elif "Basic Counter App" in prompt:
        return {
            "MainActivity.java": """
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private int count = 0;
    private TextView countTextView;
    private Button incrementButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        countTextView = findViewById(R.id.count_text);
        incrementButton = findViewById(R.id.increment_button);

        incrementButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                count++;
                countTextView.setText(String.valueOf(count));
            }
        });
    }
}
"""
        }
    return {}

# --- Lobe 0_arabic_lobe Integration ---
def get_android_project_structure_from_arabic(arabic_nlp_data: str) -> dict:
    """
    Parses Arabic NLP data to determine the required Android project structure
    and basic component definitions (e.g., Activities, layouts).
    This is a placeholder for lobe_0_arabic_lobe.generate_apk_structure_from_arabic.
    """
    # In a real scenario, this would call lobe_0_arabic_lobe.parse_arabic_nlp_data
    # and then lobe_0_arabic_lobe.generate_apk_structure_from_arabic.
    # For this example, we'll infer structure from keywords.
    project_config = {
        "package_name": "com.example.myapp",
        "activities": [],
        "layouts": {},
        "strings": {}
    }

    if "نشاط ترحيبي" in arabic_nlp_data or "Hello World Activity" in arabic_nlp_data:
        project_config["activities"].append("MainActivity")
        project_config["layouts"]["activity_main"] = """
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/hello_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="مرحباً!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        project_config["strings"]["hello_text_content"] = "مرحباً بالعالم!"

    if "تطبيق عداد بسيط" in arabic_nlp_data or "Basic Counter App" in arabic_nlp_data:
        project_config["activities"].append("MainActivity")
        project_config["layouts"]["activity_main"] = """
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/count_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="0"
        android:textSize="48sp"
        app:layout_constraintBottom_toTopOf="@+id/increment_button"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_chainStyle="packed" />

    <Button
        android:id="@+id/increment_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="زيادة"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/count_text" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        project_config["strings"]["increment_button_text"] = "زيادة"

    return project_config


class AndroidProjectBuilder:
    """
    Manages the creation and structuring of an Android project from parsed
    Arabic NLP data and generated code snippets.
    """
    def __init__(self, project_name: str = "MyApp", package_name: str = "com.example.myapp"):
        self.project_name = project_name
        self.package_name = package_name
        self.project_root = os.path.join(os.getcwd(), self.project_name)
        self.app_dir = os.path.join(self.project_root, "app")
        self.src_dir = os.path.join(self.app_dir, "src", "main", "java", *package_name.split('.'))
        self.manifest_dir = os.path.join(self.app_dir, "src", "main")
        self.res_dir = os.path.join(self.app_dir, "src", "main", "res")
        self.layout_dir = os.path.join(self.res_dir, "layout")
        self.values_dir = os.path.join(self.res_dir, "values")

    def create_project_structure(self):
        """Creates the basic directory structure for an Android project."""
        print(f"Creating project directory: {self.project_root}")
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.layout_dir, exist_ok=True)
        os.makedirs(self.values_dir, exist_ok=True)

    def create_build_gradle(self):
        """Creates a basic app/build.gradle file."""
        build_gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace '{self.package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId "{self.package_name}"
        minSdk 24
        targetSdk 34
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
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        with open(BUILD_GRADLE_PATH, "w") as f:
            f.write(build_gradle_content.strip())
        print(f"Created {BUILD_GRADLE_PATH}")

    def create_settings_gradle(self):
        """Creates a basic settings.gradle file."""
        settings_gradle_content = f"""
rootProject.name = "{self.project_name}"
include ':app'
"""
        with open(SETTINGS_GRADLE_PATH, "w") as f:
            f.write(settings_gradle_content.strip())
        print(f"Created {SETTINGS_GRADLE_PATH}")

    def create_android_manifest(self, activity_names: list):
        """Creates a basic AndroidManifest.xml file."""
        activity_declarations = ""
        for activity_name in activity_names:
            is_launcher = "android.intent.category.LAUNCHER" if activity_name == "MainActivity" else ""
            activity_declarations += f"""
        <activity android:name=".{activity_name}" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="{is_launcher}" />
            </intent-filter>
        </activity>
"""

        manifest_content = f"""
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
        android:theme="@style/Theme.{self.project_name}"
        tools:targetApi="31">
        {activity_declarations}
    </application>
</manifest>
"""
        with open(os.path.join(self.manifest_dir, "AndroidManifest.xml"), "w") as f:
            f.write(manifest_content.strip())
        print(f"Created {os.path.join(self.manifest_dir, 'AndroidManifest.xml')}")

    def create_activity_file(self, activity_name: str, code_snippet: str):
        """Creates a Java activity file."""
        activity_path = os.path.join(self.src_dir, f"{activity_name}.java")
        with open(activity_path, "w") as f:
            f.write(code_snippet.strip())
        print(f"Created {activity_path}")

    def create_layout_file(self, layout_name: str, layout_xml: str):
        """Creates an XML layout file."""
        layout_path = os.path.join(self.layout_dir, f"{layout_name}.xml")
        with open(layout_path, "w") as f:
            f.write(layout_xml.strip())
        print(f"Created {layout_path}")

    def create_values_files(self):
        """Creates basic values files (strings.xml, styles.xml)."""
        strings_content = """
<resources>
    <string name="app_name">MyApp</string>
</resources>
"""
        with open(os.path.join(self.values_dir, "strings.xml"), "w") as f:
            f.write(strings_content.strip())
        print(f"Created {os.path.join(self.values_dir, 'strings.xml')}")

        styles_content = """
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Theme.MyApp" parent="Theme.AppCompat.Light.DarkActionBar">
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
</resources>
"""
        with open(os.path.join(self.values_dir, "themes.xml"), "w") as f: # Changed to themes.xml for newer AGP versions
            f.write(styles_content.strip())
        print(f"Created {os.path.join(self.values_dir, 'themes.xml')}")

        colors_content = """
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B1</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
        with open(os.path.join(self.values_dir, "colors.xml"), "w") as f:
            f.write(colors_content.strip())
        print(f"Created {os.path.join(self.values_dir, 'colors.xml')}")


    def build_project(self, arabic_nlp_data: str):
        """
        Orchestrates the creation of an Android project based on Arabic NLP input.
        """
        print("\n--- Initiating Android Project Builder ---")

        # 1. Parse Arabic NLP data to get project structure and components
        project_config = get_android_project_structure_from_arabic(arabic_nlp_data)
        package_name = project_config.get("package_name", "com.example.myapp")
        activity_names = project_config.get("activities", [])
        layouts = project_config.get("layouts", {})

        # 2. Initialize the project builder
        builder = AndroidProjectBuilder(project_name=self.project_name, package_name=package_name)
        builder.create_project_structure()
        builder.create_build_gradle()
        builder.create_settings_gradle()
        builder.create_values_files() # Create strings, themes, colors

        # 3. Create AndroidManifest.xml
        builder.create_android_manifest(activity_names)

        # 4. Create layout files
        for layout_name, layout_xml in layouts.items():
            builder.create_layout_file(layout_name, layout_xml)

        # 5. Create activity files and corresponding code snippets
        # This step involves generating code based on the identified components
        # and potentially using language_lobe for more complex logic.
        for activity_name in activity_names:
            # Construct a prompt for the language lobe to get the Java code
            # This is a simplification. A real implementation would involve
            # more sophisticated prompt engineering based on the project_config.
            prompt_for_code = f"Generate Java code for an Android Activity named '{activity_name}' with the following layout '{activity_name.lower()}'. Consider the components defined in the layout."
            if "MainActivity" in activity_name and "Hello World Activity" in arabic_nlp_data:
                 prompt_for_code = "Generate Java code for a 'Hello World Activity' in Android."
            elif "MainActivity" in activity_name and "Basic Counter App" in arabic_nlp_data:
                 prompt_for_code = "Generate Java code for a 'Basic Counter App Activity' in Android with a button and a text view."


            java_code_snippets = get_arabic_code_snippets(prompt_for_code)
            activity_code = java_code_snippets.get(f"{activity_name}.java", None)

            if activity_code:
                builder.create_activity_file(activity_name, activity_code)
            else:
                print(f"Warning: No code snippet found for {activity_name}. Skipping file creation.")

        print(f"\n--- Android Project Builder Finished ---")
        print(f"Project '{self.project_name}' created at: {self.project_root}")
        print(f"Package name: {package_name}")

        return self.project_root

# Example Usage (for demonstration purposes - this part would be called by another lobe)
if __name__ == '__main__':
    # Simulate Arabic NLP input
    arabic_input_1 = "إنشاء تطبيق أندرويد بسيط مع نشاط ترحيبي باسم MainActivity."
    arabic_input_2 = "أريد تطبيق عداد بسيط. يجب أن يكون هناك زر لزيادة العداد وعرضه على الشاشة."

    # Create a temporary directory for the projects
    if not os.path.exists("output_projects"):
        os.makedirs("output_projects")
    os.chdir("output_projects")

    # Clean up previous runs if they exist
    if os.path.exists("MyApp_HelloWorld"):
        shutil.rmtree("MyApp_HelloWorld")
    if os.path.exists("MyApp_Counter"):
        shutil.rmtree("MyApp_Counter")

    print("--- Building Hello World App ---")
    builder_hw = AndroidProjectBuilder(project_name="MyApp_HelloWorld")
    builder_hw.build_project(arabic_input_1)

    print("\n" + "="*50 + "\n")

    print("--- Building Basic Counter App ---")
    builder_counter = AndroidProjectBuilder(project_name="MyApp_Counter")
    builder_counter.build_project(arabic_input_2)

    # Change back to the original directory
    os.chdir("..")