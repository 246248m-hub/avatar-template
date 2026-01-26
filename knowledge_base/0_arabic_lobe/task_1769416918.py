import os
import shutil
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants (these would typically be loaded from a config or dynamic sources)
ARABIC_PROJECT_ROOT = "arabic_android_projects"
JAVA_PROJECT_DIR = os.path.join(ARABIC_PROJECT_ROOT, "temp_android_project_dubai")
KNOWLEDGE_BASE_DIR = "knowledge_base" # Assuming this is where NLP models/data reside

# Ensure directories exist
os.makedirs(ARABIC_PROJECT_ROOT, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

def generate_android_project_structure(project_name: str):
    """
    Generates a basic Android project directory structure.
    This is a simplified representation and would be more complex in a real scenario.
    """
    project_path = os.path.join(ARABIC_PROJECT_ROOT, project_name)
    if os.path.exists(project_path):
        logging.warning(f"Project directory '{project_path}' already exists. Skipping creation.")
        return project_path

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "java"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "layout"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "values"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "gradle", "wrapper"), exist_ok=True)

    # Create dummy build.gradle (app level)
    with open(os.path.join(project_path, "app", "build.gradle"), "w", encoding="utf-8") as f:
        f.write("""
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.arabicapp'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.arabicapp"
        minSdk 24
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
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
""")

    # Create dummy build.gradle (project level)
    with open(os.path.join(project_path, "build.gradle"), "w", encoding="utf-8") as f:
        f.write("""
plugins {
    id 'com.android.application' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.0' apply false
}
""")

    # Create dummy AndroidManifest.xml
    with open(os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write("""
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
""")

    # Create dummy strings.xml
    with open(os.path.join(project_path, "app", "src", "main", "res", "values", "strings.xml"), "w", encoding="utf-8") as f:
        f.write("""
<resources>
    <string name="app_name">Arabic App</string>
</resources>
""")

    # Create dummy layout file
    with open(os.path.join(project_path, "app", "src", "main", "res", "layout", "activity_main.xml"), "w", encoding="utf-8") as f:
        f.write("""
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
""")
    # Create dummy MainActivity.java
    with open(os.path.join(project_path, "app", "src", "main", "java", "com", "example", "arabicapp", "MainActivity.java"), "w", encoding="utf-8") as f:
        f.write("""
package com.example.arabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
""")

    logging.info(f"Generated basic Android project structure at: {project_path}")
    return project_path

def extract_arabic_intent_from_text(text: str) -> dict:
    """
    Parses natural language Arabic text to extract user intent related to app creation or modification.
    This is a placeholder for a more sophisticated NLP model.
    """
    logging.info(f"Analyzing Arabic text for intent: '{text}'")
    intent_data = {
        "project_name": None,
        "features": [],
        "ui_elements": [],
        "arabic_text_content": ""
    }

    # Simple keyword-based extraction for demonstration
    if "إنشاء تطبيق جديد" in text or "عمل تطبيق" in text or "بناء تطبيق" in text:
        match_name = re.search(r"(?:تطبيق|اسم التطبيق)\s+([\w\s]+?)(?:بـ|مع|الذي)", text)
        if match_name:
            intent_data["project_name"] = match_name.group(1).strip()
            if "مع" in text or "بـ" in text: # Assuming "with" or "featuring" implies adding something
                intent_data["features"].append("basic_ui") # Defaulting to basic UI

    if "أضف زر" in text:
        intent_data["ui_elements"].append("button")
        intent_data["features"].append("button_functionality")
    if "شاشة تسجيل دخول" in text:
        intent_data["features"].append("login_screen")
    if "عرض قائمة" in text:
        intent_data["features"].append("list_view")

    # Extract any Arabic text intended for display
    # This is a very basic approach, a real NLP would need to differentiate intent from content
    arabic_content_match = re.search(r"النص هو ['\"](.*?)['\"]", text) # Example: "النص هو 'مرحبا بالعالم'"
    if arabic_content_match:
        intent_data["arabic_text_content"] = arabic_content_match.group(1)
    elif "للنص" in text: # More general, if the text is "for the text"
         # This part needs careful handling to not capture instructions
         pass


    logging.info(f"Extracted intent data: {intent_data}")
    return intent_data

def integrate_arabic_nlp_into_project(project_path: str, intent_data: dict):
    """
    Integrates extracted Arabic NLP data into the Android project structure.
    This function will call other lobes/modules for specific tasks.
    """
    logging.info(f"Integrating NLP data into project at: {project_path}")

    # 1. Update strings.xml with extracted Arabic text if available
    strings_xml_path = os.path.join(project_path, "app", "src", "main", "res", "values", "strings.xml")
    if intent_data.get("arabic_text_content"):
        try:
            with open(strings_xml_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if app_name needs updating or a new string needs to be added
            app_name_pattern = r'<string name="app_name">(.*?)</string>'
            if intent_data.get("project_name"):
                # Replace existing app_name or add if not found
                if re.search(app_name_pattern, content):
                    content = re.sub(app_name_pattern, f'<string name="app_name">{intent_data["project_name"]}</string>', content)
                else:
                    content = content.replace("</resources>", f'\n    <string name="app_name">{intent_data["project_name"]}</string>\n</resources>')
            
            # Add custom text content if provided
            if intent_data.get("arabic_text_content"):
                custom_text = intent_data["arabic_text_content"]
                # Sanitize custom_text to be a valid string resource name (e.g., replace spaces with underscores)
                string_name = re.sub(r'\W+', '_', custom_text.lower())[:30] # Basic sanitization and length limit
                if not string_name: # If sanitization results in empty string
                    string_name = f"custom_text_{hash(custom_text)}" # Fallback

                string_entry = f'<string name="{string_name}">{custom_text}</string>'
                if string_entry not in content:
                    content = content.replace("</resources>", f'\n    {string_entry}\n</resources>')
                    logging.info(f"Added custom string '{string_name}' to strings.xml")

            with open(strings_xml_path, "w", encoding="utf-8") as f:
                f.write(content)
            logging.info("Updated strings.xml with provided text content.")
        except FileNotFoundError:
            logging.error(f"strings.xml not found at {strings_xml_path}")
        except Exception as e:
            logging.error(f"Error updating strings.xml: {e}")

    # 2. Modify layout files based on UI elements (simplified)
    if "button" in intent_data.get("ui_elements", []):
        layout_file = os.path.join(project_path, "app", "src", "main", "res", "layout", "activity_main.xml")
        try:
            with open(layout_file, "r", encoding="utf-8") as f:
                layout_content = f.read()
            
            # Add a button to the layout
            button_xml = """
    <Button
        android:id="@+id/customButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me"
        app:layout_constraintTop_toBottomOf="@id/textView"  <!-- Example positioning -->
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>
"""
            # Find a suitable place to insert the button, e.g., after TextView
            layout_content = re.sub(r'(<TextView.*?/>)', r'\1' + button_xml, layout_content, count=1)
            
            with open(layout_file, "w", encoding="utf-8") as f:
                f.write(layout_content)
            logging.info("Added a Button to activity_main.xml.")
        except FileNotFoundError:
            logging.error(f"Layout file not found at {layout_file}")
        except Exception as e:
            logging.error(f"Error updating layout file: {e}")

    # 3. Add or modify Java/Kotlin code (placeholder for more complex logic)
    # This would involve generating new Activities, Fragments, or modifying existing ones.
    # For now, we'll just log the intention.
    if "login_screen" in intent_data.get("features", []):
        logging.info("Feature 'login_screen' requested. Requires code generation for a new Activity/Fragment.")
        # Example: call a function to generate login activity code
        # generate_login_activity(project_path)
    
    if "list_view" in intent_data.get("features", []):
        logging.info("Feature 'list_view' requested. Requires code generation for List Activity/Fragment and adapter.")
        # Example: call a function to generate list view code
        # generate_list_activity(project_path)

    # 4. Update MainActivity if needed based on new features
    main_activity_path = os.path.join(project_path, "app", "src", "main", "java", "com", "example", "arabicapp", "MainActivity.java")
    try:
        with open(main_activity_path, "r", encoding="utf-8") as f:
            main_activity_code = f.read()
        
        if "button" in intent_data.get("ui_elements", []) and "customButton" in main_activity_code:
            # Example: add an OnClickListener to the button
            logging.info("Adding OnClickListener to customButton in MainActivity.")
            button_click_listener = """
        Button customButton = findViewById(R.id.customButton);
        customButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Handle button click - potentially display custom text or navigate
                Log.d("MainActivity", "Custom button clicked!");
                // Example: show a Toast with custom text
                // Toast.makeText(MainActivity.this, "تم النقر على الزر!", Toast.LENGTH_SHORT).show();
            }
        });
"""
            # Insert the listener code, e.g., after setContentView
            main_activity_code = re.sub(r'setContentView\(R\.layout\.activity_main\);', 
                                        r'setContentView(R.layout.activity_main);\n' + button_click_listener, 
                                        main_activity_code, count=1)
            
            # Add necessary imports
            if "import android.widget.Button;" not in main_activity_code:
                main_activity_code = main_activity_code.replace("import androidx.appcompat.app.AppCompatActivity;", "import androidx.appcompat.app.AppCompatActivity;\nimport android.widget.Button;\nimport android.view.View;")
            if "import android.util.Log;" not in main_activity_code:
                 main_activity_code = main_activity_code.replace("import android.os.Bundle;", "import android.os.Bundle;\nimport android.util.Log;")

            with open(main_activity_path, "w", encoding="utf-8") as f:
                f.write(main_activity_code)
            logging.info("Updated MainActivity with button click listener.")
            
    except FileNotFoundError:
        logging.error(f"MainActivity.java not found at {main_activity_path}")
    except Exception as e:
        logging.error(f"Error updating MainActivity: {e}")

    logging.info(f"Finished integrating NLP data into project: {project_path}")


# --- Module Execution Example ---
if __name__ == "__main__":
    logging.info("--- Arabic NLP Integration Module Demo ---")

    # 1. Simulate receiving an Arabic request
    arabic_request_1 = "أريد إنشاء تطبيق جديد اسمه 'تطبيق دبي' مع شاشة تسجيل دخول."
    arabic_request_2 = "أضف زر إلى التطبيق الذي اسمه 'تطبيق دبي'. النص الذي سيعرض هو 'مرحبا يا عالم'."

    # 2. Process the first request
    intent_data_1 = extract_arabic_intent_from_text(arabic_request_1)
    
    project_name_1 = intent_data_1.get("project_name", "default_arabic_app")
    project_path_1 = generate_android_project_structure(project_name_1)
    integrate_arabic_nlp_into_project(project_path_1, intent_data_1)
    
    print(f"\n--- Project '{project_name_1}' created and basic integration done. ---")
    print(f"Project structure at: {project_path_1}")
    print(f"Intent data from request 1: {intent_data_1}")

    # 3. Process the second request, updating the existing project
    # We need to parse the project name again if it's mentioned, or assume it refers to the last created one.
    # For simplicity, let's assume the second request refers to the project from the first request.
    intent_data_2 = extract_arabic_intent_from_text(arabic_request_2)
    # Ensure project path is correctly referenced if the name was extracted
    if intent_data_2.get("project_name") and intent_data_2["project_name"] in project_name_1: # Crude check
        integrate_arabic_nlp_into_project(project_path_1, intent_data_2)
    else:
        logging.warning("Second request did not clearly refer to an existing project, or project name extraction failed. Skipping update.")

    print(f"\n--- Project '{project_name_1}' updated with features from request 2. ---")
    print(f"Intent data from request 2: {intent_data_2}")

    # Simulate cleanup (optional, depending on desired persistence)
    # print("\n--- Cleaning up dummy project structure ---")
    # if os.path.exists(project_path_1):
    #     try:
    #         shutil.rmtree(project_path_1)
    #         logging.info(f"Removed project directory: {project_path_1}")
    #     except OSError as e:
    #         logging.error(f"Error removing {project_path_1}: {e}")

    print("\n--- Arabic NLP Integration Module Demo Finished ---")