import os
import shutil
import subprocess
import time

# Define directory paths (assuming they are defined elsewhere or will be)
JAVA_PROJECT_DIR = "generated_java_project"
APK_OUTPUT_DIR = "apk_output"
ARABIC_GRAMMAR_RULES_FILE = "arabic_grammar.json"
ARABIC_VOCABULARY_FILE = "arabic_vocabulary.json"
KNOWLEDGE_BASE_DIR = "knowledge_base"

def cleanup_directory(directory_path):
    """Removes a directory if it exists."""
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Cleaned up directory: {directory_path}")
        except OSError as e:
            print(f"Error cleaning up directory {directory_path}: {e}")

def create_directory_if_not_exists(directory_path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")
        except OSError as e:
            print(f"Error creating directory {directory_path}: {e}")

def load_arabic_grammar_rules(filepath):
    """
    Loads Arabic grammar rules from a JSON file.
    This is a placeholder. In a real scenario, this would parse a structured JSON.
    """
    print(f"Loading Arabic grammar rules from: {filepath}")
    # Simulate loading some grammar rules
    grammar_rules = {
        "verb_conjugation": {
            "past": {"1sg": "تُ", "2sg_m": "تَ", "3sg_m": ""},
            "present": {"1sg": "أ", "2sg_m": "ت", "3sg_m": "ي"}
        },
        "noun_declension": {
            "nominative": "ـُ",
            "accusative": "ـَ",
            "genitive": "ـِ"
        }
    }
    return grammar_rules

def load_arabic_vocabulary(filepath):
    """
    Loads Arabic vocabulary from a JSON file.
    This is a placeholder. In a real scenario, this would parse a structured JSON.
    """
    print(f"Loading Arabic vocabulary from: {filepath}")
    # Simulate loading some vocabulary
    vocabulary = {
        "write": {"root": "ك ت ب", "meaning": "to write"},
        "book": {"root": "ك ت ب", "meaning": "book"},
        "read": {"root": "ق ر أ", "meaning": "to read"},
        "I": {"pronoun": "أنا"},
        "you": {"pronoun": "أنتَ"},
        "he": {"pronoun": "هو"}
    }
    return vocabulary

def generate_arabic_sentence(prompt_text, grammar_rules, vocabulary):
    """
    Generates an Arabic sentence based on the prompt, grammar rules, and vocabulary.
    This is a highly simplified placeholder for complex NLP generation.
    """
    print(f"Generating Arabic sentence for prompt: '{prompt_text}'")
    words = prompt_text.lower().split()
    generated_sentence_parts = []

    # Very basic keyword matching and rule application
    if "I want to write a book" in prompt_text.lower():
        generated_sentence_parts.append(vocabulary.get("I", {}).get("pronoun", "أنا"))
        generated_sentence_parts.append("أريد أن") # want to
        verb_root = vocabulary.get("write", {}).get("root")
        if verb_root:
            # Simplified conjugation for "I want to write"
            conjugated_verb = "أكتب" # أنا + كتب
            generated_sentence_parts.append(conjugated_verb)
        else:
            generated_sentence_parts.append("أكتب") # fallback
        generated_sentence_parts.append(vocabulary.get("a", {}).get("article", "")) # article 'a'
        generated_sentence_parts.append(vocabulary.get("book", {}).get("word", "كتاب")) # book
        generated_sentence_parts.append(".")
    elif "he reads" in prompt_text.lower():
        generated_sentence_parts.append(vocabulary.get("he", {}).get("pronoun", "هو"))
        verb_root = vocabulary.get("read", {}).get("root")
        if verb_root:
            # Simplified conjugation for "he reads" (present tense)
            conjugated_verb = "يقرأ" # هو + قرأ (present)
            generated_sentence_parts.append(conjugated_verb)
        else:
            generated_sentence_parts.append("يقرأ") # fallback
        generated_sentence_parts.append(".")
    else:
        generated_sentence_parts.append("هذه جملة ")
        generated_sentence_parts.append(vocabulary.get("generated", {}).get("word", "مُولَّدة"))
        generated_sentence_parts.append(vocabulary.get("for", {}).get("preposition", "لِـ"))
        generated_sentence_parts.append(f"'{prompt_text}'.")

    return " ".join(generated_sentence_parts)

def create_android_manifest(package_name, app_name):
    """
    Creates a basic AndroidManifest.xml file for a given package name and app name.
    """
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
        <activity android:name=".MainActivity"
                  android:label="@string/app_name">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    return manifest_content

def create_main_activity_java(package_name, app_name):
    """
    Creates a basic MainActivity.java file.
    """
    java_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming you have activity_main.xml

        TextView welcomeText = findViewById(R.id.welcome_text); // Assuming a TextView with id 'welcome_text'
        welcomeText.setText("Welcome to {app_name}!");
    }}
}}
"""
    return java_code

def create_activity_main_layout_xml(app_name):
    """
    Creates a basic activity_main.xml layout file.
    """
    xml_content = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    return xml_content

def create_strings_xml(app_name):
    """
    Creates a basic strings.xml file.
    """
    xml_content = f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    return xml_content

class Lobe11ArabicNLPAndAPKStructure:
    """
    This lobe focuses on integrating Arabic NLP understanding with the structure
    required for APK generation. It will process natural language prompts,
    generate Arabic text, and then lay out the initial structure for an Android project.
    """

    def __init__(self):
        self.arabic_grammar_rules = None
        self.arabic_vocabulary = None
        self.java_project_dir = JAVA_PROJECT_DIR
        self.apk_output_dir = APK_OUTPUT_DIR

    def load_resources(self):
        """Loads necessary Arabic NLP resources."""
        self.arabic_grammar_rules = load_arabic_grammar_rules(ARABIC_GRAMMAR_RULES_FILE)
        self.arabic_vocabulary = load_arabic_vocabulary(ARABIC_VOCABULARY_FILE)
        print("Arabic NLP resources loaded.")

    def process_natural_language_prompt(self, prompt_text):
        """
        Processes a natural language prompt to generate Arabic text.
        This is the core NLP integration step.
        """
        if not self.arabic_grammar_rules or not self.arabic_vocabulary:
            self.load_resources()

        generated_arabic_text = generate_arabic_sentence(
            prompt_text,
            self.arabic_grammar_rules,
            self.arabic_vocabulary
        )
        print(f"Generated Arabic text: {generated_arabic_text}")
        return generated_arabic_text

    def create_apk_project_structure(self, app_name, package_name):
        """
        Creates the basic directory structure for an Android project.
        This prepares for Lobe 8 (APK Compiler).
        """
        print(f"\n--- Creating Android Project Structure for '{app_name}' ---")
        create_directory_if_not_exists(self.java_project_dir)
        create_directory_if_not_exists(self.apk_output_dir)

        # Create app/src/main directory structure
        main_dir = os.path.join(self.java_project_dir, "app", "src", "main")
        res_dir = os.path.join(main_dir, "res")
        layout_dir = os.path.join(res_dir, "layout")
        values_dir = os.path.join(res_dir, "values")
        java_package_dir = os.path.join(main_dir, "java", *package_name.split('.'))

        dirs_to_create = [
            main_dir,
            res_dir,
            layout_dir,
            values_dir,
            java_package_dir
        ]
        for directory in dirs_to_create:
            create_directory_if_not_exists(directory)

        # Create essential Android files
        with open(os.path.join(main_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
            f.write(create_android_manifest(package_name, app_name))
            print("Created AndroidManifest.xml")

        with open(os.path.join(java_package_dir, "MainActivity.java"), "w", encoding="utf-8") as f:
            f.write(create_main_activity_java(package_name, app_name))
            print("Created MainActivity.java")

        with open(layout_dir + "/activity_main.xml", "w", encoding="utf-8") as f:
            f.write(create_activity_main_layout_xml(app_name))
            print("Created activity_main.xml")

        with open(values_dir + "/strings.xml", "w", encoding="utf-8") as f:
            f.write(create_strings_xml(app_name))
            print("Created strings.xml")

        # Placeholder for build.gradle files (not creating actual build files here, as that's more Lobe 4)
        # In a real scenario, you'd generate these as well.

        print(f"Android project structure created in: {self.java_project_dir}")
        return True

    def demo(self):
        """Demonstrates the functionality of Lobe 11."""
        print("\n--- Lobe 11: Arabic NLP and APK Structure Demo ---")

        # 1. Load Arabic NLP resources
        self.load_resources()

        # 2. Process natural language prompts and generate Arabic text
        prompts = [
            "I want to write a book",
            "he reads",
            "tell me about AI"
        ]
        generated_texts = []
        for prompt in prompts:
            arabic_text = self.process_natural_language_prompt(prompt)
            generated_texts.append(arabic_text)

        # 3. Create the basic Android project structure
        app_name = "MyArabicApp"
        package_name = "com.example.myarabicapp"
        structure_created = self.create_apk_project_structure(app_name, package_name)

        if structure_created:
            print(f"\nAndroid project structure for '{app_name}' created successfully.")
            print(f"Project root: {self.java_project_dir}")
            print(f"APK output will be in: {self.apk_output_dir}")
        else:
            print("\nFailed to create Android project structure.")

        print("\n--- Lobe 11 Demo Finished ---")
        print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---") # Assuming next is code generation

if __name__ == '__main__':
    # Example of how to run the demo for Lobe 11
    lobe11 = Lobe11ArabicNLPAndAPKStructure()
    lobe11.demo()

    # Clean up dummy files created by the demo for the next run
    print("\n--- Cleaning up dummy files from Lobe 11 demo ---")
    cleanup_directory(JAVA_PROJECT_DIR)
    cleanup_directory(APK_OUTPUT_DIR)
    cleanup_directory(ARABIC_GRAMMAR_RULES_FILE)
    cleanup_directory(ARABIC_VOCABULARY_FILE)
    # KNOWLEDGE_BASE_DIR might be used by other lobes, so not cleaning it here unless explicitly intended.

    print("\n--- Lobe 11 setup for next iteration complete ---")