import os
import shutil
import subprocess

# Define constants for directories and file names
TEMP_PROJECT_DIR_PREFIX = "apk_gen_"
ANDROID_SDK_ROOT = os.environ.get("ANDROID_SDK_ROOT")
if not ANDROID_SDK_ROOT:
    raise EnvironmentError("ANDROID_SDK_ROOT environment variable not set.")

BUILD_TOOLS_DIR = os.path.join(ANDROID_SDK_ROOT, "build-tools")
# Find the latest build-tools version
build_tools_versions = sorted([d for d in os.listdir(BUILD_TOOLS_DIR) if os.path.isdir(os.path.join(BUILD_TOOLS_DIR, d))], reverse=True)
if not build_tools_versions:
    raise FileNotFoundError("No Android build-tools found in ANDROID_SDK_ROOT.")
LATEST_BUILD_TOOLS_VERSION = build_tools_versions[0]
AAPT2_PATH = os.path.join(BUILD_TOOLS_DIR, LATEST_BUILD_TOOLS_VERSION, "aapt2")
APAK_MERGE_TOOL_PATH = os.path.join(BUILD_TOOLS_DIR, LATEST_BUILD_TOOLS_VERSION, "apksigner") # Using apksigner as a placeholder for apk merging tool

# Helper function to ensure a directory exists
def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Function to create a basic AndroidManifest.xml
def create_manifest(project_dir):
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.generatedapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_dir = os.path.join(project_dir, "app", "src", "main")
    ensure_dir_exists(manifest_dir)
    manifest_path = os.path.join(manifest_dir, "AndroidManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    return manifest_path

# Function to create a basic strings.xml
def create_strings(project_dir, app_name="GeneratedApp", arabic_label="تطبيق مولد"):
    strings_content = f"""<resources>
    <string name="app_name">{app_name}</string>
    <string name="arabic_label">{arabic_label}</string>
</resources>
"""
    strings_dir = os.path.join(project_dir, "app", "src", "main", "res", "values")
    ensure_dir_exists(strings_dir)
    strings_path = os.path.join(strings_dir, "strings.xml")
    with open(strings_path, "w", encoding="utf-8") as f:
        f.write(strings_content)
    return strings_path

# Function to create a basic MainActivity.java
def create_main_activity(project_dir):
    activity_content = """package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Example: Setting a TextView from strings.xml
        TextView welcomeText = findViewById(R.id.welcome_text_view); // Assuming you have a TextView with this ID
        welcomeText.setText(R.string.arabic_label);
    }
}
"""
    activity_dir = os.path.join(project_dir, "app", "src", "main", "java", "com", "example", "generatedapp")
    ensure_dir_exists(activity_dir)
    activity_path = os.path.join(activity_dir, "MainActivity.java")
    with open(activity_path, "w", encoding="utf-8") as f:
        f.write(activity_content)
    return activity_path

# Function to create a basic activity_main.xml layout
def create_layout(project_dir):
    layout_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    layout_dir = os.path.join(project_dir, "app", "src", "main", "res", "layout")
    ensure_dir_exists(layout_dir)
    layout_path = os.path.join(layout_dir, "activity_main.xml")
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout_content)
    return layout_path

# Function to create a basic build.gradle file
def create_build_gradle(project_dir):
    build_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    compileSdk 33 // Or a suitable SDK version

    defaultConfig {
        applicationId "com.example.generatedapp"
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
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    build_gradle_path = os.path.join(project_dir, "app", "build.gradle")
    with open(build_gradle_path, "w", encoding="utf-8") as f:
        f.write(build_gradle_content)
    return build_gradle_path

# Function to create a dummy project structure
def setup_project_structure(base_dir=".", temp_dir_name="generated_apk_project"):
    temp_project_dir = os.path.join(base_dir, temp_dir_name)
    if os.path.exists(temp_project_dir):
        shutil.rmtree(temp_project_dir)
    os.makedirs(temp_project_dir)

    # Create basic app module directory
    app_module_dir = os.path.join(temp_project_dir, "app")
    os.makedirs(app_module_dir)

    # Create necessary subdirectories within app module
    ensure_dir_exists(os.path.join(app_module_dir, "src", "main", "java", "com", "example", "generatedapp"))
    ensure_dir_exists(os.path.join(app_module_dir, "src", "main", "res", "values"))
    ensure_dir_exists(os.path.join(app_module_dir, "src", "main", "res", "layout"))

    # Create essential files
    create_manifest(temp_project_dir)
    create_strings(temp_project_dir)
    create_main_activity(temp_project_dir)
    create_layout(temp_project_dir)
    create_build_gradle(temp_project_dir)

    return temp_project_dir

# Function to compile the APK using AAPT2 and Javac/D8
def compile_apk(project_dir, output_apk_path):
    app_module_dir = os.path.join(project_dir, "app")
    build_dir = os.path.join(app_module_dir, "build", "intermediates", "dex")
    ensure_dir_exists(build_dir)

    # Compile Java sources to .class files
    javac_command = [
        "javac",
        "-d", os.path.join(build_dir, "classes"),
        "-cp", os.path.join(ANDROID_SDK_ROOT, "platforms", "android-33", "android.jar"), # Adjust API level as needed
        os.path.join(app_module_dir, "src", "main", "java", "com", "example", "generatedapp", "MainActivity.java")
    ]
    subprocess.run(javac_command, check=True, cwd=app_module_dir)

    # Convert .class files to DEX files using D8 (part of build-tools)
    d8_command = [
        os.path.join(BUILD_TOOLS_DIR, LATEST_BUILD_TOOLS_VERSION, "d8"),
        os.path.join(build_dir, "classes"),
        "--output", os.path.join(build_dir, "dex")
    ]
    subprocess.run(d8_command, check=True, cwd=app_module_dir)

    # Compile resources using AAPT2
    res_dir = os.path.join(app_module_dir, "src", "main", "res")
    aapt2_compile_command = [
        AAPT2_PATH,
        "compile",
        "--dir", res_dir,
        "-o", os.path.join(app_module_dir, "build", "intermediates", "compiled_resources.zip")
    ]
    subprocess.run(aapt2_compile_command, check=True, cwd=app_module_dir)

    # Link resources and generate R.java (though we already created it, this is part of the process)
    # AAPT2 link command for generating intermediate APK assets
    aapt2_link_command = [
        AAPT2_PATH,
        "link",
        "--manifest", os.path.join(app_module_dir, "src", "main", "AndroidManifest.xml"),
        os.path.join(app_module_dir, "build", "intermediates", "compiled_resources.zip"),
        "-o", os.path.join(app_module_dir, "build", "intermediates", "app-debug.zip"),
        "--proguard", "false", # For simplicity, disable ProGuard for now
        "--java-symbols", os.path.join(app_module_dir, "build", "generated", "source", "r", "debug") # Output for R.java if needed
    ]
    subprocess.run(aapt2_link_command, check=True, cwd=app_module_dir)


    # Package the application into an APK
    # This involves zipping the compiled code, resources, and manifest.
    # A more robust solution would involve using the Android Gradle Plugin's build process.
    # For this simplified example, we'll create a directory structure that resembles
    # an unaligned APK and then use `zipalign` (implicitly handled by apksigner for basic cases)
    # and `apksigner`.

    # A more direct way to create an APK from compiled components is complex and often relies
    # on build tools that orchestrate multiple steps (like Gradle).
    # For this example, we will simulate the final packaging using a hypothetical tool or
    # demonstrate the signing process, which is a crucial step.

    # Simplified APK creation: combine DEX, compiled resources, and manifest into a zip.
    # This is a highly simplified step and might not produce a fully functional APK without
    # proper alignment and signing.

    # Using apksigner to create a signed APK (requires a debug keystore)
    # For a real scenario, you would generate a debug keystore or use a release keystore.
    # For this demo, we'll assume a debug.keystore exists in the project root or use a placeholder.
    debug_keystore = os.path.join(project_dir, "debug.keystore")
    if not os.path.exists(debug_keystore):
        # Create a dummy keystore for demonstration if it doesn't exist
        try:
            subprocess.run([
                "keytool", "-genkey", "-v", "-keystore", debug_keystore,
                "-alias", "debugkey", "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-dname", "CN=Android Debug,O=Android,C=US",
                "-storepass", "android", "-keypass", "android"
            ], check=True, capture_output=True, text=True)
            print("Created dummy debug.keystore")
        except FileNotFoundError:
            print("keytool command not found. Cannot create dummy keystore. Please ensure Java JDK is installed and in PATH.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error creating dummy keystore: {e.stderr}")
            return False


    # Use `apksigner` to sign the intermediate zip. This tool can also bundle.
    # In a real build, this step happens after zipalign.
    # The input to apksigner is typically a directory containing compiled resources, dex files, etc.
    # We will create a temporary directory to hold the APK contents before signing.

    temp_apk_contents_dir = os.path.join(project_dir, "build", "temp_apk")
    ensure_dir_exists(temp_apk_contents_dir)

    # Copy compiled resources
    compiled_resources_zip = os.path.join(app_module_dir, "build", "intermediates", "app-debug.zip")
    shutil.copy(compiled_resources_zip, os.path.join(temp_apk_contents_dir, "resources.zip")) # Placeholder name

    # Copy DEX files
    dex_output_dir = os.path.join(app_module_dir, "build", "intermediates", "dex", "dex")
    for dex_file in os.listdir(dex_output_dir):
        if dex_file.endswith(".dex"):
            shutil.copy(os.path.join(dex_output_dir, dex_file), os.path.join(temp_apk_contents_dir, dex_file))

    # Copy manifest (already handled by aapt2 link, but for clarity)
    shutil.copy(os.path.join(app_module_dir, "src", "main", "AndroidManifest.xml"), os.path.join(temp_apk_contents_dir, "AndroidManifest.xml"))

    # Create the APK by zipping the contents
    # This is a simplified zipping process. `apksigner` expects a directory structure.
    # A more accurate process would be:
    # 1. Create a directory with `AndroidManifest.xml`, `classes.dex`, `res/` folder, `assets/` folder.
    # 2. Use `zipalign` on this directory.
    # 3. Use `apksigner sign`.

    # Let's try a more direct approach for signing a directory of files.
    # `apksigner` can take a directory as input and package it if it has the right structure.
    # However, it's designed for signing existing APKs or JARs.

    # Alternative: use `apkanalyzer` or `aapt` (older) to list contents and then build.
    # The most reliable way is to use Gradle. Since we are avoiding Gradle,
    # we'll simulate the final APK creation using a simplified zip process and then sign it.

    # Creating a temporary directory to hold the unpacked APK structure
    unaligned_apk_dir = os.path.join(project_dir, "build", "unaligned_apk")
    ensure_dir_exists(unaligned_apk_dir)

    # Copy manifest
    shutil.copy(os.path.join(app_module_dir, "src", "main", "AndroidManifest.xml"), os.path.join(unaligned_apk_dir, "AndroidManifest.xml"))

    # Copy DEX files
    for dex_file in os.listdir(dex_output_dir):
        if dex_file.endswith(".dex"):
            shutil.copy(os.path.join(dex_output_dir, dex_file), os.path.join(unaligned_apk_dir, dex_file))

    # Copy compiled resources into a 'res' folder
    res_output_dir = os.path.join(unaligned_apk_dir, "res")
    ensure_dir_exists(res_output_dir)
    # Copy contents from the AAPT2 compiled zip (this part is tricky without proper unzipping and structuring)
    # For simplicity, we'll assume AAPT2 'link' output creates a structure we can copy.
    # In reality, AAPT2 link outputs to a zip or directly to an APK file.

    # Let's re-run AAPT2 link to produce an intermediate APK structure
    aapt2_link_output_dir = os.path.join(app_module_dir, "build", "intermediates", "apk_contents")
    ensure_dir_exists(aapt2_link_output_dir)
    aapt2_link_final_apk_command = [
        AAPT2_PATH,
        "link",
        "--manifest", os.path.join(app_module_dir, "src", "main", "AndroidManifest.xml"),
        "--resources", os.path.join(app_module_dir, "build", "intermediates", "compiled_resources.zip"),
        "-o", os.path.join(aapt2_link_output_dir, "unsigned.apk"), # Output as an APK file
        "--proguard", "false",
        "--java-symbols", os.path.join(app_module_dir, "build", "generated", "source", "r", "debug")
    ]
    subprocess.run(aapt2_link_final_apk_command, check=True, cwd=app_module_dir)

    # Now, unpack the unsigned.apk to get the resource structure
    unzip_command = [
        "unzip",
        os.path.join(aapt2_link_output_dir, "unsigned.apk"),
        "-d", unaligned_apk_dir
    ]
    subprocess.run(unzip_command, check=True, cwd=app_module_dir)

    # Add the compiled DEX files to the unpacked structure
    for dex_file in os.listdir(dex_output_dir):
        if dex_file.endswith(".dex"):
            shutil.copy(os.path.join(dex_output_dir, dex_file), os.path.join(unaligned_apk_dir, dex_file))

    # Ensure AndroidManifest.xml is correctly placed if not already by unzip
    if not os.path.exists(os.path.join(unaligned_apk_dir, "AndroidManifest.xml")):
        shutil.copy(os.path.join(app_module_dir, "src", "main", "AndroidManifest.xml"), os.path.join(unaligned_apk_dir, "AndroidManifest.xml"))


    # Sign the APK using apksigner
    sign_command = [
        APAK_MERGE_TOOL_PATH, # This is apksigner
        "sign",
        "--ks", debug_keystore,
        "--ks-key-alias", "debugkey",
        "--ks-pass", "pass:android",
        "--key-pass", "pass:android",
        "--out", output_apk_path,
        os.path.join(aapt2_link_output_dir, "unsigned.apk") # Signing the intermediate APK
    ]
    try:
        subprocess.run(sign_command, check=True)
        print(f"Successfully signed APK to {output_apk_path}")
        return True
    except FileNotFoundError:
        print("apksigner command not found. Please ensure Android build-tools are in your PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error signing APK: {e.stderr}")
        return False


# Main function to orchestrate the APK generation
def generate_hyper_efficient_apk(natural_language_prompt: str, output_path: str):
    """
    Generates a hyper-efficient APK from a natural language prompt.
    This is a simplified implementation focusing on structure and Arabic integration.
    """
    print(f"--- Generating APK for prompt: '{natural_language_prompt}' ---")

    # 1. Parse the natural language prompt (Lobe 0_language_lobe, Lobe 2_arabic_parsing_lobe)
    # This step would involve complex NLP to extract app name, features, UI elements, etc.
    # For this example, we'll hardcode some values or use a very basic extraction.
    app_name_from_prompt = "MyArabicApp"
    arabic_label_from_prompt = "تطبيق بالعربي"

    # Dummy parsing (replace with actual Lobe 0 and Lobe 2 logic)
    if "arabic" in natural_language_prompt.lower() or "عربي" in natural_language_prompt:
        app_name_from_prompt = "ArabicAppGenerator"
        arabic_label_from_prompt = "تطبيق عربي فعال"

    # 2. Set up the project structure (Lobe 1_project_setup_lobe)
    temp_project_dir = setup_project_structure(temp_dir_name=f"{APK_GENERATOR_PREFIX}{os.urandom(4).hex()}")
    print(f"Project structure set up at: {temp_project_dir}")

    # 3. Generate APK components (Lobe 3_ui_layout_lobe, Lobe 4_code_generation_lobe, Lobe 5_resource_generation_lobe)
    # This would involve generating XML layouts, Java/Kotlin code, and resource files
    # based on the parsed prompt.
    # For this example, we have pre-defined functions to create basic components.
    # The integration with Lobe 0 and Lobe 2's output would happen here.

    # Update strings.xml with Arabic label
    create_strings(temp_project_dir, app_name=app_name_from_prompt, arabic_label=arabic_label_from_prompt)
    print("Updated strings.xml with app name and Arabic label.")

    # 4. Compile and package the APK (Lobe 6_synthesis_lobe, Lobe 8_apk_compiler_lobe)
    # This involves using Android build tools (aapt2, dx/d8, apksigner).
    apk_generated = compile_apk(temp_project_dir, output_path)

    # 5. Cleanup (Lobe 9_cleanup_lobe)
    if os.path.exists(temp_project_dir):
        print(f"Cleaning up temporary project directory: {temp_project_dir}")
        shutil.rmtree(temp_project_dir)

    if apk_generated:
        print(f"--- APK generation complete. Output saved to: {output_path} ---")
    else:
        print(f"--- APK generation failed. ---")

# Example Usage (demonstrates how this module would be called)
if __name__ == "__main__":
    # Define a placeholder for the APK generator prefix
    APK_GENERATOR_PREFIX = "apk_gen_"
    OUTPUT_APK_PATH = "generated_arabic_app.apk"

    # Create a dummy debug.keystore if it doesn't exist, for apksigner
    if not os.path.exists("debug.keystore"):
        try:
            subprocess.run([
                "keytool", "-genkey", "-v", "-keystore", "debug.keystore",
                "-alias", "debugkey", "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-dname", "CN=Android Debug,O=Android,C=US",
                "-storepass", "android", "-keypass", "android"
            ], check=True, capture_output=True, text=True)
            print("Created dummy debug.keystore for demonstration.")
        except FileNotFoundError:
            print("keytool command not found. Please ensure Java JDK is installed and in PATH.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating dummy keystore: {e.stderr}")

    # Example prompt that might trigger Arabic specific logic
    test_prompt_arabic = "Generate a simple Android app with Arabic support."
    generate_hyper_efficient_apk(test_prompt_arabic, OUTPUT_APK_PATH)

    # Clean up the generated APK and dummy keystore if they exist
    # if os.path.exists(OUTPUT_APK_PATH):
    #     os.remove(OUTPUT_APK_PATH)
    #     print(f"Removed generated APK: {OUTPUT_APK_PATH}")
    # if os.path.exists("debug.keystore"):
    #     os.remove("debug.keystore")
    #     print("Removed dummy debug.keystore")