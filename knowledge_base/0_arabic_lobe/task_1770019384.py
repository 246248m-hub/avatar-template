import os
import re
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any

# --- Constants ---
ARABIC_WORD_IDENTIFIERS = {
    "noun": ["اسم", "اسم مجرور"],
    "verb": ["فعل", "فعل ماض", "فعل مضارع", "فعل أمر"],
    "adjective": ["صفة", "نعت"],
    "preposition": ["حرف جر"],
    "conjunction": ["حرف عطف"],
    "pronoun": ["ضمير"],
    "adverb": ["حال", "ظرف"],
    "interjection": ["حرف نداء", "حرف جواب", "حرف استفهام"],
}

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Lobe 0: Arabic NLP Core (Simplified) ---
class ArabicNLP:
    def __init__(self):
        logging.info("Initializing ArabicNLP module.")
        self.arabic_grammar_rules = {
            "sentence_structure": {
                "nominal_sentence": ["pronoun", "noun", "adjective", "preposition", "noun"], # Example: The big cat sat on the mat.
                "verbal_sentence": ["verb", "noun", "noun", "adjective"] # Example: The cat chased the mouse.
            },
            "word_order_preferences": {
                "adjective_after_noun": True,
                "prepositional_phrase_position": "flexible" # Can be before or after the main clause
            }
        }
        self.part_of_speech_mapping = {
            "اسم": "noun",
            "اسم مجرور": "noun",
            "فعل": "verb",
            "فعل ماض": "verb",
            "فعل مضارع": "verb",
            "فعل أمر": "verb",
            "صفة": "adjective",
            "نعت": "adjective",
            "حرف جر": "preposition",
            "حرف عطف": "conjunction",
            "ضمير": "pronoun",
            "حال": "adverb",
            "ظرف": "adverb",
            "حرف نداء": "interjection",
            "حرف جواب": "interjection",
            "حرف استفهام": "interjection",
        }
        self.pos_tags_to_word_types = {v: k for k, v_list in ARABIC_WORD_IDENTIFIERS.items() for v in v_list}


    def analyze_arabic_text(self, text: str) -> List[Dict[str, str]]:
        """
        Performs a simplified Part-of-Speech (POS) tagging for Arabic text.
        In a real scenario, this would involve sophisticated libraries like CAMeL Tools.
        For this demo, we'll use basic keyword matching.
        """
        logging.info(f"Analyzing Arabic text: '{text}'")
        words = text.split()
        tagged_words = []
        for word in words:
            # This is a highly simplified POS tagging.
            # A real implementation would use a morphological analyzer and tagger.
            pos_tag = "unknown"
            for arabic_tag, word_type in self.pos_tags_to_word_types.items():
                if arabic_tag in word: # Very crude matching
                    pos_tag = word_type
                    break
            tagged_words.append({"word": word, "pos": pos_tag})
        logging.info(f"Analyzed tags: {tagged_words}")
        return tagged_words

    def infer_sentence_structure(self, tagged_words: List[Dict[str, str]]) -> str:
        """
        Infers a basic sentence structure based on POS tags.
        This is a highly simplified inference.
        """
        if not tagged_words:
            return "empty_sentence"

        pos_sequence = [tag["pos"] for tag in tagged_words]
        logging.info(f"Inferring structure from POS sequence: {pos_sequence}")

        # Try to match against defined nominal and verbal sentence structures
        for struct_name, struct_pattern in self.arabic_grammar_rules["sentence_structure"].items():
            if len(pos_sequence) >= len(struct_pattern):
                # Simple sequential matching for demo purposes
                match = True
                seq_idx = 0
                struct_idx = 0
                while seq_idx < len(pos_sequence) and struct_idx < len(struct_pattern):
                    if pos_sequence[seq_idx] == struct_pattern[struct_idx] or \
                       (struct_pattern[struct_idx] == "noun" and pos_sequence[seq_idx] in ["noun", "pronoun"]) or \
                       (struct_pattern[struct_idx] == "adjective" and pos_sequence[seq_idx] in ["adjective", "noun"]): # Allow noun as part of adjective phrase loosely
                        seq_idx += 1
                        struct_idx += 1
                    elif struct_pattern[struct_idx] == "prepositional_phrase" and pos_sequence[seq_idx] == "preposition":
                        # Skip ahead to find a noun after preposition
                        seq_idx += 1
                        while seq_idx < len(pos_sequence) and pos_sequence[seq_idx] != "noun":
                            seq_idx += 1
                        if seq_idx < len(pos_sequence) and pos_sequence[seq_idx] == "noun":
                            seq_idx += 1
                            struct_idx += 1
                        else:
                            match = False
                            break
                    else:
                        match = False
                        break

                if match and struct_idx == len(struct_pattern):
                    logging.info(f"Inferred structure: {struct_name}")
                    return struct_name

        logging.warning("Could not infer a defined sentence structure.")
        return "complex_structure"

    def generate_arabic_phrase(self, structure_type: str, keywords: Dict[str, str]) -> str:
        """
        Generates a basic Arabic phrase based on a structure type and keywords.
        This is a highly simplified generation.
        """
        logging.info(f"Generating Arabic phrase for structure '{structure_type}' with keywords: {keywords}")
        if structure_type == "nominal_sentence":
            subject = keywords.get("noun", "شيء")
            adjective = keywords.get("adjective", "")
            preposition = keywords.get("preposition", "")
            object_noun = keywords.get("noun_object", "")

            phrase = subject
            if adjective:
                phrase += f" {adjective}"
            if preposition and object_noun:
                phrase += f" {preposition} {object_noun}"
            return phrase

        elif structure_type == "verbal_sentence":
            verb = keywords.get("verb", "فعل")
            subject = keywords.get("noun", "فاعل")
            object_noun = keywords.get("noun_object", "")
            adjective = keywords.get("adjective", "") # Could represent an adverbial phrase here

            phrase = verb
            if subject:
                phrase += f" {subject}"
            if object_noun:
                phrase += f" {object_noun}"
            if adjective: # Simplified: assuming this can be an adverbial modifier
                phrase += f" {adjective}"
            return phrase
        else:
            return " ".join(keywords.values()) # Fallback

    def process_arabic_request(self, request: str) -> Dict[str, Any]:
        """
        Processes a natural language Arabic request to extract keywords and infer structure.
        This acts as the entry point for the Arabic NLP Lobe.
        """
        logging.info(f"Processing Arabic request: '{request}'")
        tagged_words = self.analyze_arabic_text(request)
        structure = self.infer_sentence_structure(tagged_words)

        # Simplified keyword extraction based on assumed POS tags from request
        keywords = {}
        for word_data in tagged_words:
            pos = word_data["pos"]
            if pos in ["noun", "verb", "adjective", "preposition", "pronoun", "adverb", "interjection"]:
                # Basic handling for multiple nouns/objects
                if pos == "noun":
                    if "noun" not in keywords:
                        keywords["noun"] = word_data["word"]
                    elif "noun_object" not in keywords:
                        keywords["noun_object"] = word_data["word"]
                    else:
                        keywords[f"noun_{len(keywords)}"] = word_data["word"] # Handle more nouns if needed
                else:
                    keywords[pos] = word_data["word"]

        generated_phrase = self.generate_arabic_phrase(structure, keywords)

        return {
            "original_request": request,
            "tagged_words": tagged_words,
            "inferred_structure": structure,
            "extracted_keywords": keywords,
            "generated_phrase": generated_phrase
        }


# --- Lobe 6: Synthesis Lobe ---
class SynthesisLobe:
    def __init__(self):
        logging.info("Initializing SynthesisLobe.")
        self.arabic_nlp = ArabicNLP()

    def synthesize_apk_intent_description(self, arabic_request: str) -> Dict[str, Any]:
        """
        Synthesizes an intent description suitable for APK generation from an Arabic request.
        This involves processing the Arabic request using the ArabicNLP lobe.
        """
        logging.info(f"Synthesizing APK intent description for: '{arabic_request}'")
        nlp_result = self.arabic_nlp.process_arabic_request(arabic_request)

        # The generated_phrase from ArabicNLP can be seen as a simplified description
        # of the intent or action requested in Arabic.
        # For APK generation, we might map this to specific Android component intents
        # or basic UI element descriptions.

        intent_description = {
            "source_language": "arabic",
            "original_request": nlp_result["original_request"],
            "analyzed_structure": nlp_result["inferred_structure"],
            "keyword_mapping": nlp_result["extracted_keywords"],
            "synthesized_description": f"Perform action related to: {nlp_result['generated_phrase']}",
            "potential_android_intent": self._map_to_android_intent(nlp_result)
        }
        logging.info(f"Synthesized intent description: {intent_description}")
        return intent_description

    def _map_to_android_intent(self, nlp_result: Dict[str, Any]) -> str:
        """
        A placeholder function to map Arabic NLP results to Android intents.
        In a real system, this would be a complex mapping based on keywords and inferred structure.
        """
        keywords = nlp_result["extracted_keywords"]
        structure = nlp_result["inferred_structure"]

        if "verb" in keywords and "noun" in keywords:
            verb = keywords["verb"]
            noun = keywords["noun"]
            if verb == "افتح" and noun == "تطبيق": # Example: "Open application"
                return "android.intent.action.MAIN" # Generic app launch intent
            elif verb == "ابحث" and noun == "عن": # Example: "Search for"
                return "android.intent.action.SEARCH"
            elif verb == "اتصل" and noun == "بـ": # Example: "Call"
                return "android.intent.action.CALL"
            elif verb == "أرسل" and noun == "رسالة": # Example: "Send message"
                return "android.intent.action.SENDTO"
        elif structure == "nominal_sentence" and "noun" in keywords:
            # Could represent UI element creation or display
            return f"DISPLAY_TEXT:{keywords['noun']}"
        elif structure == "verbal_sentence" and "verb" in keywords:
            return f"EXECUTE_VERB:{keywords['verb']}"

        return "UNDEFINED_INTENT"


# --- Lobe 8: APK Compiler Lobe ---
class APKCompilerLobe:
    def __init__(self):
        logging.info("Initializing APKCompilerLobe.")
        self.synthesis_lobe = SynthesisLobe()
        self.android_project_template_dir = Path("./android_project_template")
        self.build_tools_path = self._find_android_build_tools()
        if not self.build_tools_path:
            logging.error("Android SDK Build Tools not found. Please ensure ANDROID_HOME is set and build tools are installed.")
            # In a real scenario, this would raise an exception or have a more robust fallback.

    def _find_android_build_tools(self) -> Path | None:
        """Attempts to find the Android SDK build tools directory."""
        android_home = os.environ.get("ANDROID_HOME")
        if not android_home:
            logging.warning("ANDROID_HOME environment variable not set.")
            # Try common default locations
            possible_paths = [
                Path.home() / "Android/Sdk",
                Path("C:/Users") / os.getlogin() / "AppData/Local/Android/Sdk" # Windows
            ]
            for sdk_path in possible_paths:
                if sdk_path.exists():
                    android_home = str(sdk_path)
                    logging.info(f"Found potential ANDROID_HOME at: {android_home}")
                    break

        if not android_home:
            return None

        sdk_root = Path(android_home)
        build_tools_dir = None
        for entry in sdk_root.iterdir():
            if entry.name.startswith("build-tools") and entry.is_dir():
                # Pick the latest version found
                if build_tools_dir is None or entry.name > build_tools_dir.name:
                    build_tools_dir = entry

        if build_tools_dir:
            logging.info(f"Using Android build tools: {build_tools_dir}")
            return build_tools_dir
        return None

    def _create_dummy_android_project(self, app_name: str, package_name: str, main_activity_content: str) -> Path:
        """
        Creates a very basic Android project structure for demonstration.
        This is a highly simplified stub. A real implementation would involve
        using templates or build scripts.
        """
        logging.info(f"Creating dummy Android project: {app_name}")
        project_path = self.android_project_template_dir / app_name.replace(" ", "_").lower()
        project_path.mkdir(parents=True, exist_ok=True)

        # app/src/main/java/<package_name>/MainActivity.java
        java_dir = project_path / "app" / "src" / "main" / "java"
        package_path = java_dir / Path(*package_name.split('.'))
        package_path.mkdir(parents=True, exist_ok=True)

        main_activity_file = package_path / "MainActivity.java"
        main_activity_file.write_text(main_activity_content)

        # app/src/main/AndroidManifest.xml
        manifest_dir = project_path / "app" / "src" / "main"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_file = manifest_dir / "AndroidManifest.xml"
        manifest_file.write_text(f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">
    <uses-permission android:name="android.permission.INTERNET"/>
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
        """)

        # res/values/strings.xml
        res_values_dir = project_path / "app" / "src" / "main" / "res" / "values"
        res_values_dir.mkdir(parents=True, exist_ok=True)
        strings_file = res_values_dir / "strings.xml"
        strings_file.write_text(f"""
<resources>
    <string name="app_name">{app_name}</string>
</resources>
        """)

        # Build.gradle (simplified)
        app_gradle_file = project_path / "app" / "build.gradle"
        app_gradle_file.write_text("""
plugins {
    id 'com.android.application'
}

android {
    compileSdk 33 // Or your target SDK

    defaultConfig {
        applicationId "your.package.name" // Will be replaced
        minSdk 21
        targetSdk 33
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
}

dependencies {
    // Add necessary dependencies here if needed
}
        """)
        # Replace placeholder package name in build.gradle
        gradle_content = app_gradle_file.read_text().replace("your.package.name", package_name)
        app_gradle_file.write_text(gradle_content)

        logging.info(f"Dummy project structure created at: {project_path}")
        return project_path

    def _compile_apk(self, project_path: Path, app_name: str) -> str | None:
        """
        Compiles the Android project into an APK using Gradle.
        """
        if not self.build_tools_path:
            logging.error("Cannot compile APK: Android SDK Build Tools not found.")
            return None

        logging.info(f"Attempting to compile APK for project at: {project_path}")

        # Execute Gradle wrapper for building the APK
        # Assumes a 'gradlew' script exists in the project root (standard for Android projects)
        # If not, we'd need to create it or call Gradle directly.
        gradlew_path = project_path / "gradlew"
        if not gradlew_path.exists():
            logging.error("Gradle wrapper (gradlew) not found in project. Cannot compile APK.")
            # Fallback: Try to run Gradle command directly if gradlew is not present
            # This is less robust and depends on Gradle being in PATH.
            try:
                logging.warning("gradlew not found, attempting to use 'gradle' command directly.")
                subprocess.run(
                    ["gradle", "assembleDebug", "-p", str(project_path)],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except FileNotFoundError:
                logging.error(" 'gradle' command not found in PATH. Cannot compile APK.")
                return None
            except subprocess.CalledProcessError as e:
                logging.error(f"Gradle build failed: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}")
                return None
        else:
            # Make gradlew executable if it's not already (important on Linux/macOS)
            if os.name != 'nt': # Not Windows
                os.chmod(str(gradlew_path), 0o755)

            try:
                # Execute the Gradle wrapper to build the debug APK
                # '-p' specifies the project directory
                result = subprocess.run(
                    [str(gradlew_path), "assembleDebug", "-p", str(project_path)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logging.info("Gradle build successful.")
                # logging.debug(f"Gradle stdout:\n{result.stdout}") # Uncomment for detailed logs
            except subprocess.CalledProcessError as e:
                logging.error(f"Gradle build failed: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}")
                return None
            except FileNotFoundError:
                logging.error("gradlew not found or not executable. Cannot compile APK.")
                return None

        # Find the generated APK file
        # It's usually in app/build/outputs/apk/debug/
        apk_dir = project_path / "app" / "build" / "outputs" / "apk" / "debug"
        if apk_dir.exists():
            apk_files = list(apk_dir.glob("*.apk"))
            if apk_files:
                generated_apk_path = str(apk_files[0])
                logging.info(f"Successfully generated APK at: {generated_apk_path}")
                return generated_apk_path
            else:
                logging.error(f"No APK files found in {apk_dir}")
        else:
            logging.error(f"APK output directory not found: {apk_dir}")

        return None

    def _generate_main_activity_code(self, intent_description: Dict[str, Any]) -> str:
        """
        Generates a basic MainActivity.java content based on the synthesized intent description.
        """
        app_name = "GeneratedApp"
        package_name = "com.example.generatedapp" # Default, should be set by caller
        intent_action = intent_description.get("potential_android_intent", "UNDEFINED_INTENT")
        synthesized_desc = intent_description.get("synthesized_description", "No description")
        original_request = intent_description.get("original_request", "")

        # Basic mapping to simple Java code for MainActivity
        display_text = synthesized_desc
        if original_request:
            display_text = f"Request: {original_request}\n\n{synthesized_desc}"

        java_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Import TextView

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        // setContentView(R.layout.activity_main); // Assuming a default layout

        TextView textView = new TextView(this);
        textView.setText("App generated from Arabic request:\\n\\n{display_text.replace("\"", "\\\"")}\\n\\nIntent: {intent_action}");
        setContentView(textView); // Set the TextView as the content view
    }}
}}
        """
        return java_code

    def _cleanup_android_project_template(self):
        """Cleans up the dummy project directory."""
        logging.info("Cleaning up demo project directory.")
        if self.android_project_template_dir.exists():
            try:
                import shutil
                shutil.rmtree(self.android_project_template_dir)
                logging.info("Demo project directory removed.")
            except OSError as e:
                logging.error(f"Error removing demo project directory: {e}")

    def generate_apk_from_arabic(self, arabic_request: str) -> str | None:
        """
        The main function to generate an APK from an Arabic natural language request.
        This orchestrates the synthesis and compilation steps.
        """
        logging.info(f"\n--- Initiating APK generation for Arabic request: '{arabic_request}' ---")

        # Step 1: Synthesize intent description using SynthesisLobe
        intent_description = self.synthesis_lobe.synthesize_apk_intent_description(arabic_request)

        if intent_description.get("potential_android_intent") == "UNDEFINED_INTENT":
            logging.warning("Could not map Arabic request to a defined Android intent. APK generation may be basic.")
            # Proceed with a generic app structure if no specific intent is recognized.

        # Step 2: Prepare Android project structure
        # Use a more dynamic app name and package name
        app_name = "ArabicApp"
        package_name = f"com.example.arabicapp.{re.sub(r'[^a-z0-9]+', '', arabic_request.lower())[:10]}" # Create a somewhat unique package name
        main_activity_content = self._generate_main_activity_code(intent_description)
        # Ensure package name is correctly set in the generated content
        main_activity_content = main_activity_content.replace("package com.example.generatedapp;", f"package {package_name};")

        project_path = self._create_dummy_android_project(app_name, package_name, main_activity_content)

        # Step 3: Compile the APK
        generated_apk_path = self._compile_apk(project_path, app_name)

        # Step 4: Clean up dummy project
        self._cleanup_android_project_template()

        if generated_apk_path:
            logging.info(f"APK generation process successful. APK saved at: {generated_apk_path}")
            return generated_apk_path
        else:
            logging.error("APK generation process failed.")
            return None

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Demonstrating APK Compiler Lobe ---")

    # Instantiate the APK Compiler Lobe
    apk_compiler = APKCompilerLobe()

    # Example Arabic requests
    arabic_requests = [
        "افتح التطبيق",                # Open the application (simple app launch)
        "أرسل رسالة نصية",             # Send a text message
        "اتصل بصديق",                  # Call a friend
        "هذه شاشة رئيسية",             # This is a main screen (basic UI display)
        "البحث عن معلومات",            # Search for information
        "قطة جميلة تجلس على السجادة" # A beautiful cat sits on the rug (more descriptive)
    ]

    for request in arabic_requests:
        print(f"\n--- Generating APK for: '{request}' ---")
        generated_apk_path = apk_compiler.generate_apk_from_arabic(request)

        if generated_apk_path:
            print(f"Successfully generated APK at: {generated_apk_path}")
        else:
            print("\nAPK generation process failed.")
        print("-" * 40)

    print("\n--- APK Compiler Lobe Demo Finished ---")