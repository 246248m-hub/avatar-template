import os
import json
import re
import shutil

# --- Constants ---
KNOWLEDGE_BASE_DIR = "knowledge_base"
ARABIC_KEYWORDS_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_keywords.json")
ARABIC_SYNONYMS_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_synonyms.json")
ARABIC_GRAMMAR_RULES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_grammar_rules.json")
PROJECT_ROOT = "generated_apk_project"
MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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
MAIN_ACTIVITY_TEMPLATE = """package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("{greeting_message}");
    }}
}}
"""
ACTIVITY_MAIN_XML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
APP_NAME_STRING_XML_TEMPLATE = """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""

# --- Helper Functions ---

def load_knowledge_base():
    """Loads Arabic keywords, synonyms, and grammar rules from JSON files."""
    knowledge_base = {
        "keywords": {},
        "synonyms": {},
        "grammar_rules": {}
    }
    try:
        with open(ARABIC_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            knowledge_base["keywords"] = json.load(f)
        with open(ARABIC_SYNONYMS_FILE, 'r', encoding='utf-8') as f:
            knowledge_base["synonyms"] = json.load(f)
        with open(ARABIC_GRAMMAR_RULES_FILE, 'r', encoding='utf-8') as f:
            knowledge_base["grammar_rules"] = json.load(f)
    except FileNotFoundError:
        print("Knowledge base files not found. Please ensure they exist.")
    except json.JSONDecodeError:
        print("Error decoding JSON from knowledge base files.")
    return knowledge_base

def get_arabic_keyword_mapping(text, keywords_map):
    """Finds Arabic keywords in the input text and maps them to their semantic categories."""
    found_keywords = {}
    for category, words in keywords_map.items():
        for word in words:
            if word in text:
                found_keywords[word] = category
    return found_keywords

def extract_app_info_from_arabic(arabic_text, knowledge_base):
    """Extracts application name and greeting message from Arabic text using semantic analysis."""
    app_name = "MyArabicApp"  # Default
    greeting_message = "مرحباً بالعالم!"  # Default

    keywords_map = knowledge_base.get("keywords", {})
    grammar_rules = knowledge_base.get("grammar_rules", {})

    # Simple keyword extraction for app name (e.g., "تطبيق اسمه")
    app_name_match = re.search(r"(?:تطبيق|برنامج)\s+اسمه\s+([\w\s]+)", arabic_text, re.IGNORECASE)
    if app_name_match:
        app_name = app_name_match.group(1).strip()

    # Simple keyword extraction for greeting message (e.g., "رسالة ترحيب")
    greeting_match = re.search(r"رسالة\s+ترحيب(?:ك|ك)\\s+هي\s+([\w\s]+)", arabic_text, re.IGNORECASE)
    if greeting_match:
        greeting_message = greeting_match.group(1).strip()
    else:
        # More sophisticated parsing based on grammar rules if direct match fails
        # This part can be significantly expanded based on the complexity of grammar_rules
        pass # Placeholder for more advanced grammar rule application

    return app_name, greeting_message

def create_android_project_structure(project_path, package_name, app_name, greeting_message):
    """Creates the basic Android project directory structure and essential files."""
    app_src_path = os.path.join(project_path, "app", "src", "main")
    manifest_path = os.path.join(app_src_path, "AndroidManifest.xml")
    java_dir = os.path.join(app_src_path, "java", *package_name.split('.'))
    res_dir = os.path.join(app_src_path, "res")
    layout_dir = os.path.join(res_dir, "layout")
    values_dir = os.path.join(res_dir, "values")

    os.makedirs(java_dir, exist_ok=True)
    os.makedirs(layout_dir, exist_ok=True)
    os.makedirs(values_dir, exist_ok=True)

    # Create AndroidManifest.xml
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(MANIFEST_TEMPLATE.format(package_name=package_name))

    # Create MainActivity.java
    main_activity_path = os.path.join(java_dir, "MainActivity.java")
    with open(main_activity_path, "w", encoding="utf-8") as f:
        f.write(MAIN_ACTIVITY_TEMPLATE.format(package_name=package_name, greeting_message=greeting_message))

    # Create activity_main.xml
    activity_main_path = os.path.join(layout_dir, "activity_main.xml")
    with open(activity_main_path, "w", encoding="utf-8") as f:
        f.write(ACTIVITY_MAIN_XML_TEMPLATE.format())

    # Create strings.xml for app name
    strings_xml_path = os.path.join(values_dir, "strings.xml")
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(APP_NAME_STRING_XML_TEMPLATE.format(app_name=app_name))

def generate_apk_from_arabic(arabic_prompt: str, output_dir: str = PROJECT_ROOT):
    """
    Generates a hyper-efficient APK structure from a natural language Arabic prompt.
    This module focuses on understanding Arabic input and setting up the basic Android project.
    """
    print(f"--- Initiating Lobe 0_arabic_lobe for prompt: '{arabic_prompt}' ---")

    # 1. Load Arabic Knowledge Base
    knowledge_base = load_knowledge_base()
    if not knowledge_base["keywords"]:
        print("Warning: Arabic keywords not loaded. NLP capabilities will be limited.")
        # Potentially create dummy knowledge base files if they don't exist for testing
        if not os.path.exists(KNOWLEDGE_BASE_DIR):
            os.makedirs(KNOWLEDGE_BASE_DIR)
        if not os.path.exists(ARABIC_KEYWORDS_FILE):
            with open(ARABIC_KEYWORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"app_name_indicators": ["اسم", "تطبيق"], "greeting_indicators": ["مرحبا", "ترحيب"]}, f)
        if not os.path.exists(ARABIC_SYNONYMS_FILE):
            with open(ARABIC_SYNONYMS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"تطبيق": ["برنامج"], "مرحبا": ["أهلا"]}, f)
        if not os.path.exists(ARABIC_GRAMMAR_RULES_FILE):
            with open(ARABIC_GRAMMAR_RULES_FILE, 'w', encoding='utf-8') as f:
                json.dump({"sentence_structure_for_app_name": ["NOUN", "VERB", "NOUN"], "sentence_structure_for_greeting": ["NOUN", "VERB"]}, f)
        knowledge_base = load_knowledge_base() # Reload after potential creation


    # 2. Extract Information from Arabic Prompt
    app_name, greeting_message = extract_app_info_from_arabic(arabic_prompt, knowledge_base)

    print(f"Extracted App Name: {app_name}")
    print(f"Extracted Greeting Message: {greeting_message}")

    # 3. Define Package Name (can be derived or default)
    # For simplicity, using a reversed version of app name or a default
    package_name_parts = [part.lower() for part in re.findall(r'\w+', app_name)]
    if len(package_name_parts) > 2:
        package_name = f"com.{'.'.join(package_name_parts[-2:][::-1])}"
    elif len(package_name_parts) == 2:
        package_name = f"com.{package_name_parts[1]}.{package_name_parts[0]}"
    else:
        package_name = f"com.example.{app_name.lower().replace(' ', '')}"

    print(f"Generated Package Name: {package_name}")

    # 4. Create Android Project Structure
    print(f"Creating Android project structure in: {output_dir}")
    if os.path.exists(output_dir):
        print(f"Removing existing project directory: {output_dir}")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    create_android_project_structure(output_dir, package_name, app_name, greeting_message)

    print(f"--- Lobe 0_arabic_lobe finished. Project structure generated at {output_dir} ---")

    # Return generated information for further processing
    return {
        "package_name": package_name,
        "app_name": app_name,
        "greeting_message": greeting_message,
        "project_path": output_dir
    }

# Example Usage (for demonstration purposes, will be called by other lobes)
if __name__ == "__main__":
    # Ensure knowledge base files exist for this standalone run
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
    if not os.path.exists(ARABIC_KEYWORDS_FILE):
        with open(ARABIC_KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "app_name_indicators": ["تطبيق", "برنامج"],
                "greeting_indicators": ["مرحبا", "سلام", "تحية"],
                "button_labels": ["زر", "اضغط"],
                "text_content": ["نص", "عرض"]
            }, f)
    if not os.path.exists(ARABIC_SYNONYMS_FILE):
        with open(ARABIC_SYNONYMS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "تطبيق": ["برنامج"],
                "مرحبا": ["أهلا", "سلام عليكم"],
                "زر": ["مفتاح"],
                "نص": ["كلمات", "عبارة"]
            }, f)
    if not os.path.exists(ARABIC_GRAMMAR_RULES_FILE):
        with open(ARABIC_GRAMMAR_RULES_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "app_name_pattern": r"(?:تطبيق|برنامج)\s+اسمه\s+([\w\s]+)",
                "greeting_pattern": r"(?:رسالة\s+ترحيب|تحية)\s*(?:هي|ك|ك)\\s*([\w\s]+)",
                "button_action_pattern": r"(?:عند الضغط على|عند)\s+([\w\s]+?)\s+(?:زر|مفتاح)\s+([\w\s]+)"
            }, f)

    # Example Arabic prompt
    arabic_input_prompt = "أريد إنشاء تطبيق اسمه 'رسالة خاصة' وتعرض رسالة ترحيب تقول 'أهلاً بك يا صديقي'."
    generated_info = generate_apk_from_arabic(arabic_input_prompt)

    print("\n--- Generation Complete ---")
    print(f"Generated Project Path: {generated_info['project_path']}")
    print(f"Package Name: {generated_info['package_name']}")
    print(f"App Name: {generated_info['app_name']}")
    print(f"Greeting Message: {generated_info['greeting_message']}")

    # Clean up generated project for repeated runs
    if os.path.exists(PROJECT_ROOT):
        print(f"\n--- Cleaning up generated project: {PROJECT_ROOT} ---")
        shutil.rmtree(PROJECT_ROOT)