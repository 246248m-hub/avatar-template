import os
import shutil

KNOWLEDGE_BASE_DIR = "knowledge_base"
GENERATED_APK_FILES_DIR = "generated_apk_files"

def initialize_directories():
    """Initializes necessary directories for knowledge base and APK generation."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Created directory: {KNOWLEDGE_BASE_DIR}")
    if not os.path.exists(GENERATED_APK_FILES_DIR):
        os.makedirs(GENERATED_APK_FILES_DIR)
        print(f"Created directory: {GENERATED_APK_FILES_DIR}")

def load_arabic_grammar_rules():
    """
    Loads Arabic grammar rules from a predefined structure or file.
    This function is a placeholder and would typically involve complex NLP parsing.
    For demonstration, we'll return a simplified representation.
    """
    print("Loading Arabic grammar rules...")
    # In a real scenario, this would parse complex grammar files or a dedicated knowledge graph.
    grammar_rules = {
        "sentence_structure": {
            "verb_noun_object": ["verb", "noun", "object"],
            "noun_verb_object": ["noun", "verb", "object"],
            "adjective_noun": ["adjective", "noun"]
        },
        "word_types": {
            "verb": ["فعل", "يأكل", "يشرب"],
            "noun": ["اسم", "تفاحة", "ماء"],
            "object": ["مفعول به", "التفاحة", "الماء"],
            "adjective": ["صفة", "جميل", "لذيذ"]
        }
    }
    print("Arabic grammar rules loaded.")
    return grammar_rules

def parse_arabic_text(text, grammar_rules):
    """
    Parses Arabic text based on the loaded grammar rules.
    This is a highly simplified parser for demonstration.
    """
    print(f"Parsing Arabic text: '{text}'")
    parsed_structure = []
    words = text.split()
    current_structure = []
    for word in words:
        found_type = None
        for word_type, examples in grammar_rules["word_types"].items():
            if word in examples:
                found_type = word_type
                break
        if found_type:
            current_structure.append(found_type)
        else:
            # Handle unknown words or more complex parsing logic
            current_structure.append("unknown")

    # Attempt to match the parsed structure to known sentence structures
    matched_structure = None
    for structure_name, structure_pattern in grammar_rules["sentence_structure"].items():
        if len(current_structure) == len(structure_pattern) and all(current_structure[i] == structure_pattern[i] for i in range(len(structure_pattern))):
            matched_structure = structure_name
            break

    if matched_structure:
        print(f"Text parsed into structure: {matched_structure}")
        return {"text": text, "structure": matched_structure, "word_types": current_structure}
    else:
        print("Could not match text to a known sentence structure.")
        return {"text": text, "structure": "unstructured", "word_types": current_structure}

def generate_code_from_arabic_structure(parsed_data, project_template_path="android_template"):
    """
    Generates Android project code (Java/Kotlin) based on parsed Arabic structure.
    This function orchestrates the creation of basic Android components.
    """
    print(f"Generating code from parsed Arabic structure: {parsed_data['structure']}")
    output_project_dir = os.path.join(GENERATED_APK_FILES_DIR, "GeneratedApp_" + os.path.basename(project_template_path))
    
    if os.path.exists(output_project_dir):
        shutil.rmtree(output_project_dir)
    shutil.copytree(project_template_path, output_project_dir)
    print(f"Copied project template to: {output_project_dir}")

    # Simplified logic:
    # If structure is "verb_noun_object", we might generate an activity that performs an action
    # and displays a result. If "adjective_noun", perhaps a UI element displaying the noun with its adjective.

    if parsed_data['structure'] == "verb_noun_object":
        activity_name = "ActionActivity"
        layout_name = "activity_action"
        # Modify MainActivity to launch ActionActivity or modify ActionActivity's content
        main_activity_path = os.path.join(output_project_dir, "app", "src", "main", "java", "com", "example", "generatedapp", "MainActivity.java")
        if os.path.exists(main_activity_path):
            with open(main_activity_path, "r") as f:
                main_activity_content = f.read()
            # Example modification: add a button to launch ActionActivity
            new_main_activity_content = main_activity_content.replace(
                "setContentView(R.layout.activity_main);",
                "setContentView(R.layout.activity_main);\n        Button launchButton = findViewById(R.id.launch_action_button);\n        launchButton.setOnClickListener(v -> {\n            Intent intent = new Intent(this, ActionActivity.class);\n            startActivity(intent);\n        });"
            )
            with open(main_activity_path, "w") as f:
                f.write(new_main_activity_content)
            print(f"Modified MainActivity to include a button to launch {activity_name}.")

        # Create a placeholder ActionActivity
        action_activity_dir = os.path.join(output_project_dir, "app", "src", "main", "java", "com", "example", "generatedapp")
        os.makedirs(action_activity_dir, exist_ok=True)
        action_activity_path = os.path.join(action_activity_dir, f"{activity_name}.java")
        with open(action_activity_path, "w") as f:
            f.write(f"""
package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{layout_name.split('_')[-1]}); // Use the base name for layout

        // Simplified logic: display a generic message based on the parsed structure
        TextView messageView = findViewById(R.id.message_text_view);
        if (messageView != null) {{
            messageView.setText("Performing action: eat apple"); // Example based on verb_noun_object
        }}
    }}
}}
""")
        print(f"Created placeholder {activity_name}.java")

        # Create a placeholder layout
        layout_dir = os.path.join(output_project_dir, "app", "src", "main", "res", "layout")
        os.makedirs(layout_dir, exist_ok=True)
        layout_path = os.path.join(layout_dir, f"activity_{layout_name.split('_')[-1]}.xml")
        with open(layout_path, "w") as f:
            f.write(f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/message_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"/>

</androidx.constraintlayout.widget.ConstraintLayout>
""")
        print(f"Created placeholder {layout_path}")

    elif parsed_data['structure'] == "adjective_noun":
        # Placeholder for adjective_noun structure: e.g., display a styled text view
        print("Handling 'adjective_noun' structure: Placeholder logic for UI styling.")

    print(f"Code generation complete for output directory: {output_project_dir}")
    return output_project_dir

def build_next_module():
    """
    This function represents the next logical step in the grand objective.
    It focuses on Arabic NLP parsing and generating code structures.
    """
    print("\n--- Initiating next step: Lobe 2_arabic_nlp_lobe ---")
    initialize_directories()
    grammar_rules = load_arabic_grammar_rules()

    # Example Arabic text input
    arabic_sentence_1 = "فعل اسم مفعول به" # Verb Noun Object
    arabic_sentence_2 = "صفة اسم"        # Adjective Noun

    # Process first sentence
    parsed_data_1 = parse_arabic_text(arabic_sentence_1, grammar_rules)
    project_dir_1 = generate_code_from_arabic_structure(parsed_data_1)

    # Process second sentence
    parsed_data_2 = parse_arabic_text(arabic_sentence_2, grammar_rules)
    project_dir_2 = generate_code_from_arabic_structure(parsed_data_2)

    print("\n--- Lobe 2_arabic_nlp_lobe Module Finished ---")
    print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---")
    # In a real system, this would pass the generated project directories to the code generation lobe.
    print(f"Generated project for '{arabic_sentence_1}': {project_dir_1}")
    print(f"Generated project for '{arabic_sentence_2}': {project_dir_2}")
    # Next step would involve Lobe 4_code_generation_lobe to refine and finalize code,
    # then Lobe 8_apk_compiler_lobe.

if __name__ == '__main__':
    # Dummy android_template directory for demonstration
    if not os.path.exists("android_template"):
        os.makedirs("android_template", exist_ok=True)
        with open(os.path.join("android_template", "AndroidManifest.xml"), "w") as f:
            f.write("<manifest package=\"com.example.generatedapp\"></manifest>")
        
        app_dir = os.path.join("android_template", "app", "src", "main", "java", "com", "example", "generatedapp")
        os.makedirs(app_dir, exist_ok=True)
        with open(os.path.join(app_dir, "MainActivity.java"), "w") as f:
            f.write("""
package com.example.generatedapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.content.Intent;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Placeholder for button to launch ActionActivity (added dynamically by build_next_module)
        Button launchButton = findViewById(R.id.launch_action_button);
        if (launchButton != null) {
            launchButton.setOnClickListener(v -> {
                Intent intent = new Intent(this, ActionActivity.class);
                startActivity(intent);
            });
        }
    }
}
""")
        res_layout_dir = os.path.join("android_template", "app", "src", "main", "res", "layout")
        os.makedirs(res_layout_dir, exist_ok=True)
        with open(os.path.join(res_layout_dir, "activity_main.xml"), "w") as f:
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
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
        
    <Button
        android:id="@+id/launch_action_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Launch Action"
        app:layout_constraintTop_toBottomOf="@id/constraintLayout" // Example constraint
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"/>

</androidx.constraintlayout.widget.ConstraintLayout>
""")
        print("Created dummy 'android_template' directory.")

    build_next_module()