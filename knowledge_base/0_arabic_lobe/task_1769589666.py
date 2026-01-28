import os
import shutil
import re
from pathlib import Path

# Assuming the existence of a Lobe 0_language_lobe and Lobe 6_synthesis_lobe for context.
# These would handle natural language processing and synthesis of Arabic text.

class ArabicApkModule:
    """
    This module focuses on generating APK structures and basic AndroidManifest.xml
    content specifically tailored for Arabic language support and content.
    It acts as a preliminary step towards full APK generation, laying the groundwork
    for more complex logic handled by subsequent lobes.
    """

    def __init__(self, base_project_path: Path = Path("./arabic_apk_project")):
        """
        Initializes the ArabicApkModule.

        Args:
            base_project_path: The root directory for the generated APK project.
        """
        self.base_project_path = base_project_path
        self.src_main_path = self.base_project_path / "app" / "src" / "main"
        self.manifest_path = self.src_main_path / "AndroidManifest.xml"
        self.values_path = self.src_main_path / "res" / "values"
        self.values_ar_path = self.src_main_path / "res" / "values-ar"

    def create_project_structure(self):
        """
        Creates the basic directory structure for an Android project,
        including directories for Arabic resources.
        """
        print(f"Creating project structure at: {self.base_project_path}")
        self.base_project_path.mkdir(parents=True, exist_ok=True)
        self.src_main_path.mkdir(parents=True, exist_ok=True)
        self.values_path.mkdir(parents=True, exist_ok=True)
        self.values_ar_path.mkdir(parents=True, exist_ok=True)

    def generate_basic_manifest(self, app_name: str = "ArabicApp", package_name: str = "com.example.arabicapp"):
        """
        Generates a very basic AndroidManifest.xml file with essential elements
        and sets the default language to Arabic.

        Args:
            app_name: The name of the application.
            package_name: The package name of the application.
        """
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name.replace(' ', '')}">

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
        print(f"Generating basic AndroidManifest.xml at: {self.manifest_path}")
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

    def generate_strings_xml(self, app_name: str = "ArabicApp"):
        """
        Generates the default strings.xml and a specific strings.xml for Arabic.

        Args:
            app_name: The name of the application to be used as the app name string.
        """
        # Default strings.xml
        default_strings_content = f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
        print(f"Generating default strings.xml at: {self.values_path / 'strings.xml'}")
        with open(self.values_path / "strings.xml", "w", encoding="utf-8") as f:
            f.write(default_strings_content)

        # Arabic strings.xml
        arabic_strings_content = f"""<resources>
    <string name="app_name">{app_name} (العربية)</string>
    <string name="hello_world">مرحبا بالعالم!</string>
    <string name="example_button_text">اضغط هنا</string>
</resources>
"""
        print(f"Generating Arabic strings.xml at: {self.values_ar_path / 'strings.xml'}")
        with open(self.values_ar_path / "strings.xml", "w", encoding="utf-8") as f:
            f.write(arabic_strings_content)

    def generate_theme_xml(self, app_name: str = "ArabicApp"):
        """
        Generates a basic theme.xml file.

        Args:
            app_name: The name of the application, used for theme naming.
        """
        theme_name = f"Theme.{app_name.replace(' ', '')}"
        theme_content = f"""<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="{theme_name}" parent="Theme.Material3.DayNight.NoActionBar">
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
        <item name="android:textColorPrimary">@color/black</item> <!-- For default text color -->
        <item name="android:windowIsRtl">true</item> <!-- Explicitly set RTL for the theme -->
    </style>

    <!-- Colors for the theme -->
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
        print(f"Generating theme.xml at: {self.values_path / 'themes.xml'}")
        with open(self.values_path / "themes.xml", "w", encoding="utf-8") as f:
            f.write(theme_content)

    def generate_arabic_theme_xml(self, app_name: str = "ArabicApp"):
        """
        Generates a basic theme.xml file specifically for Arabic, ensuring RTL support.
        This might override or supplement the default theme for RTL contexts.

        Args:
            app_name: The name of the application, used for theme naming.
        """
        theme_name = f"Theme.{app_name.replace(' ', '')}"
        arabic_theme_content = f"""<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme for Arabic. Inherits from the default theme -->
    <style name="{theme_name}" parent="Theme.{app_name.replace(' ', '')}">
        <!-- Ensure RTL support is explicitly enabled here if not inherited -->
        <item name="android:windowIsRtl">true</item>
        <!-- You can override other RTL-specific attributes if needed -->
        <item name="android:gravity">right_gravity</item> <!-- Example: Default gravity for layouts -->
    </style>
</resources>
"""
        # For simplicity, we'll merge this into the main theme.xml or ensure it's applied correctly.
        # A more robust approach would be to create values-ldrtl/themes.xml.
        # For this module's scope, we'll add a note or merge.
        # For now, we create a separate file as a demonstration of language-specific resources.
        print(f"Generating Arabic-specific theme.xml at: {self.values_ar_path / 'themes.xml'}")
        # Note: In a real scenario, the app would use `values-ldrtl/themes.xml` for layout direction,
        # and `values-ar/themes.xml` might contain other Arabic-specific styling.
        # For this example, we'll write to `values-ar` to highlight the concept.
        with open(self.values_ar_path / "themes.xml", "w", encoding="utf-8") as f:
            f.write(arabic_theme_content)

    def generate_layout_file(self, layout_name: str = "activity_main.xml"):
        """
        Generates a basic layout XML file with some Arabic text elements.

        Args:
            layout_name: The name of the layout file to generate.
        """
        layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView_greeting"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        android:textSize="24sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toTopOf="@id/button_action"
        android:layout_marginBottom="32dp" />

    <Button
        android:id="@+id/button_action"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/example_button_text"
        app:layout_constraintTop_toBottomOf="@id/textView_greeting"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_path = self.src_main_path / "layout" / layout_name
        print(f"Generating layout file at: {layout_path}")
        layout_path.parent.mkdir(parents=True, exist_ok=True)
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content)

    def generate_arabic_layout_file(self, layout_name: str = "activity_main.xml"):
        """
        Generates a layout file specifically for Arabic, demonstrating RTL adjustments.
        In a real app, this might be placed in `layout-ldrtl/`. For demonstration,
        we'll create a separate file to show the concept.

        Args:
            layout_name: The name of the layout file to generate.
        """
        # This demonstrates how constraints might be different or text alignment adjusted.
        # A more practical approach would be to use `layout-ldrtl` and override specific
        # constraints or use start/end instead of left/right.
        arabic_layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView_greeting"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        android:textSize="24sp"
        android:gravity="end" <!-- Explicitly align text to end for RTL -->
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintEnd_toStartOf="parent" <!-- Flipping constraints for RTL -->
        app:layout_constraintStart_toEndOf="parent"
        app:layout_constraintBottom_toTopOf="@id/button_action"
        android:layout_marginBottom="32dp" />

    <Button
        android:id="@+id/button_action"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/example_button_text"
        app:layout_constraintTop_toBottomOf="@id/textView_greeting"
        app:layout_constraintEnd_toStartOf="parent" <!-- Flipping constraints for RTL -->
        app:layout_constraintStart_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        # In a real Android project, you would typically use `res/layout-ldrtl/` directory
        # for RTL-specific layouts. For this module's demonstration, we'll create a file
        # in the `values-ar` directory to conceptually show language-specific adaptations.
        # A more accurate way to handle RTL is via `layout-ldrtl`.
        arabic_layout_path = self.values_ar_path / layout_name.replace(".xml", "_rtl.xml") # Differentiating for demo
        print(f"Generating Arabic-centric layout file (conceptual) at: {arabic_layout_path}")
        arabic_layout_path.parent.mkdir(parents=True, exist_ok=True)
        with open(arabic_layout_path, "w", encoding="utf-8") as f:
            f.write(arabic_layout_content)

    def generate_placeholder_java_activity(self, activity_name: str = "MainActivity.java", package_name: str = "com.example.arabicapp"):
        """
        Generates a placeholder Java activity file. This module does not generate
        full Java code but sets up the file structure.

        Args:
            activity_name: The name of the activity file.
            package_name: The package name of the application.
        """
        java_code = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Button;
import android.widget.Toast;

public class {activity_name.replace('.java', '')} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // Set the layout. The Android system will pick the correct one based on
        // locale and layout direction (e.g., layout-ar, layout-ldrtl).
        // For this basic setup, we assume 'activity_main' will be used.
        setContentView(R.layout.activity_main);

        TextView greetingTextView = findViewById(R.id.textView_greeting);
        Button actionButton = findViewById(R.id.button_action);

        // The text will be loaded from strings.xml based on the current locale.
        // greetingTextView.setText(R.string.hello_world); // Usually set by layout

        actionButton.setOnClickListener(v -> {{
            Toast.makeText(this, getString(R.string.example_button_text) + " clicked!", Toast.LENGTH_SHORT).show();
        }});
    }}
}}
"""
        java_dir = self.src_main_path / "java" / package_name.replace('.', '/')
        print(f"Generating placeholder Java activity at: {java_dir / activity_name}")
        java_dir.mkdir(parents=True, exist_ok=True)
        with open(java_dir / activity_name, "w", encoding="utf-8") as f:
            f.write(java_code)

    def generate_placeholder_kotlin_activity(self, activity_name: str = "MainActivity.kt", package_name: str = "com.example.arabicapp"):
        """
        Generates a placeholder Kotlin activity file.

        Args:
            activity_name: The name of the activity file.
            package_name: The package name of the application.
        """
        kotlin_code = f"""package {package_name}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView
import android.widget.Button
import android.widget.Toast
// import com.example.arabicapp.R // R will be generated by the build system

class {activity_name.replace('.kt', '')} : AppCompatActivity() {{

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        // Set the layout. The Android system will pick the correct one based on
        // locale and layout direction (e.g., layout-ar, layout-ldrtl).
        // For this basic setup, we assume 'activity_main' will be used.
        setContentView(R.layout.activity_main)

        val greetingTextView = findViewById<TextView>(R.id.textView_greeting)
        val actionButton = findViewById<Button>(R.id.button_action)

        // The text will be loaded from strings.xml based on the current locale.
        // greetingTextView.text = getString(R.string.hello_world) // Usually set by layout

        actionButton.setOnClickListener {{
            Toast.makeText(this, "${{getString(R.string.example_button_text)}} clicked!", Toast.LENGTH_SHORT).show()
        }}
    }}
}}
"""
        kotlin_dir = self.src_main_path / "java" / package_name.replace('.', '/') # Android Studio puts Kotlin in 'java' dir
        print(f"Generating placeholder Kotlin activity at: {kotlin_dir / activity_name}")
        kotlin_dir.mkdir(parents=True, exist_ok=True)
        with open(kotlin_dir / activity_name, "w", encoding="utf-8") as f:
            f.write(kotlin_code)


    def clean_project_directory(self):
        """
        Removes the generated project directory if it exists.
        """
        print(f"\n--- Cleaning up generated project directory: {self.base_project_path} ---")
        if self.base_project_path.exists():
            shutil.rmtree(self.base_project_path)
            print(f"Removed: {self.base_project_path}")
        else:
            print("Project directory does not exist, no cleanup needed.")

    def build_module(self, app_name: str = "MyArabicApp", package_name: str = "com.example.myarabicapp", use_kotlin: bool = True):
        """
        Executes the core logic of this module to build the basic Arabic APK structure.

        Args:
            app_name: The name of the application.
            package_name: The package name for the application.
            use_kotlin: Whether to generate Kotlin or Java placeholder activity.
        """
        self.clean_project_directory() # Start with a clean slate
        self.create_project_structure()
        self.generate_basic_manifest(app_name=app_name, package_name=package_name)
        self.generate_strings_xml(app_name=app_name)
        self.generate_theme_xml(app_name=app_name)
        self.generate_arabic_theme_xml(app_name=app_name) # Demonstrate Arabic specific theme
        self.generate_layout_file()
        self.generate_arabic_layout_file() # Demonstrate Arabic specific layout concept

        if use_kotlin:
            self.generate_placeholder_kotlin_activity(package_name=package_name)
        else:
            self.generate_placeholder_java_activity(package_name=package_name)

        print("\n--- ArabicApkModule Finished ---")

if __name__ == '__main__':
    # Example Usage:
    arabic_module = ArabicApkModule()
    arabic_module.build_module(app_name="My RTL App", package_name="com.rtl.arabic.demo", use_kotlin=True)

    print("\n--- Running cleanup after demo ---")
    arabic_module.clean_project_directory()

    # Example with Java
    # arabic_module_java = ArabicApkModule(base_project_path=Path("./arabic_apk_project_java"))
    # arabic_module_java.build_module(app_name="My RTL App Java", package_name="com.rtl.arabic.javademo", use_kotlin=False)
    # arabic_module_java.clean_project_directory()