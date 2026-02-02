import os
import re
from typing import Dict, Any, List

# Assume these are imported from other lobes or utility modules
# For demonstration, we'll define them as placeholders with basic functionality.

class ArabicNLPProcessor:
    """
    A placeholder for Lobe 0's Arabic NLP capabilities.
    In a real scenario, this would be a sophisticated Arabic parser and intent recognizer.
    """
    def process_instruction(self, instruction: str) -> Dict[str, Any]:
        """
        Processes a natural language Arabic instruction and extracts relevant information.
        Returns a dictionary with identified entities and actions.
        """
        print(f"Simulating Arabic NLP processing for: '{instruction}'")
        # Basic parsing for demonstration: extract keywords and potential actions
        entities = {
            "elements": [],
            "actions": [],
            "attributes": {}
        }
        if "أضف" in instruction or "ضع" in instruction:
            entities["actions"].append("add")
        if "صورة" in instruction:
            entities["elements"].append("image")
            entities["attributes"]["image_source"] = "default_icon.png" # Placeholder source
        if "بجانب" in instruction:
            entities["attributes"]["position"] = "adjacent"
        if "النص" in instruction:
            entities["elements"].append("text")
            # Try to extract text content if it's immediately following
            match = re.search(r"النص الذي يشير إلى '(.*?)'", instruction)
            if match:
                entities["attributes"]["target_text"] = match.group(1)
        if "الصفحة الرئيسية" in instruction:
            entities["attributes"]["page_context"] = "homepage"

        # Further sophisticated parsing would identify more specific attributes,
        # relationships, and error handling for ambiguous instructions.
        return entities

class APKStructureGenerator:
    """
    A placeholder for Lobe 6's APK structure generation capabilities.
    This would create the basic Android project file structure.
    """
    def create_android_project(self, project_name: str, package_name: str) -> str:
        """
        Creates a basic Android project directory structure.
        Returns the root path of the created project.
        """
        print(f"Simulating creation of Android project: '{project_name}' with package '{package_name}'")
        project_root = f"./{project_name}_project"
        os.makedirs(project_root, exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.')), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "drawable"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "mipmap"), exist_ok=True)
        with open(os.path.join(project_root, "app", "build.gradle"), "w") as f:
            f.write("// Placeholder build.gradle\n")
        with open(os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml"), "w") as f:
            f.write(f'<?xml version="1.0" encoding="utf-8"?>\n<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package_name}">\n    <application>\n        <activity android:name=".MainActivity">\n            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>')
        with open(os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.'), "MainActivity.java"), "w") as f:
            f.write(f'package {package_name};\n\nimport androidx.appcompat.app.AppCompatActivity;\nimport android.os.Bundle;\n\npublic class MainActivity extends AppCompatActivity {{\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {{\n        super.onCreate(savedInstanceState);\n        setContentView(R.layout.activity_main);\n    }}\n}}')
        return project_root

    def cleanup_android_project_template(self, project_path: str):
        """
        Cleans up the generated Android project directory.
        """
        print(f"Simulating cleanup of demo project: '{project_path}'")
        import shutil
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            print("Demo project cleaned up.")

class CodeGenerator:
    """
    A placeholder for Lobe 4's code generation capabilities.
    This would translate NLP instructions into Java/Kotlin code snippets.
    """
    def generate_layout_element_code(self, element_type: str, attributes: Dict[str, Any]) -> str:
        """
        Generates XML layout code for a given UI element.
        """
        print(f"Simulating layout element code generation for type '{element_type}' with attributes: {attributes}")
        element_id = attributes.get("id", f"{element_type}_{hash(str(attributes)) % 10000}")
        layout_code = f'<TextView android:id="@+id/{element_id}"\n'
        layout_code += f'          android:layout_width="wrap_content"\n'
        layout_code += f'          android:layout_height="wrap_content"\n'
        if "text" in attributes:
            layout_code += f'          android:text="{attributes["text"]}"\n'
        if "image_source" in attributes:
            # For an image, it would be ImageView. This is a simplification.
            layout_code = f'<ImageView android:id="@+id/{element_id}"\n'
            layout_code += f'             android:layout_width="wrap_content"\n'
            layout_code += f'             android:layout_height="wrap_content"\n'
            layout_code += f'             android:src="@drawable/{attributes["image_source"].replace(".png", "")}"\n' # Assumes drawable resource
        layout_code += f'/>'
        return layout_code

    def generate_activity_code_snippet(self, element_id: str, action: str, attributes: Dict[str, Any]) -> str:
        """
        Generates a Java code snippet for activity logic.
        """
        print(f"Simulating activity code snippet generation for element ID '{element_id}', action '{action}', attributes: {attributes}")
        snippet = f"// Logic for {action} on element {element_id}\n"
        if action == "add" and "image" in attributes.get("elements", []):
            target_text = attributes.get("attributes", {}).get("target_text")
            if target_text:
                snippet += f"TextView targetTextView = findViewById(R.id.{self.find_element_id_by_text(target_text, 'layout.xml')});\n" # Needs a way to find the ID from text
                snippet += f"ImageView newImageView = new ImageView(this);\n"
                snippet += f"newImageView.setImageResource(R.drawable.{attributes['attributes']['image_source'].replace('.png', '')});\n"
                # This would require more complex layout manipulation to place it next to the text.
                # For now, just demonstrating the intent.
                snippet += f"// Logic to add newImageView next to targetTextView would go here.\n"
        return snippet

    def find_element_id_by_text(self, text_content: str, layout_file_path: str) -> str:
        """
        Placeholder to find the ID of a TextView element given its text content.
        In reality, this would parse the layout XML.
        """
        print(f"Simulating search for element ID with text '{text_content}' in '{layout_file_path}'")
        # For this demo, we'll assume a convention or a simplified lookup.
        # A real implementation would involve XML parsing.
        if "الصفحة الرئيسية" in text_content:
            return "homepage_text_view_id" # Example assumed ID
        return "unknown_element_id"

class APKGemerator:
    """
    Placeholder for Lobe 8, which compiles the APK.
    """
    def generate_apk(self, project_path: str, app_name: str) -> str:
        """
        Simulates the APK generation process.
        Returns the path to the generated APK.
        """
        print(f"Simulating APK generation for project at: '{project_path}'")
        # In a real scenario, this would involve invoking Android SDK tools (like Gradle)
        # to build the project and generate the APK.
        generated_apk_path = os.path.join(project_path, "app", "build", "outputs", "apk", "debug", f"{app_name}-debug.apk")
        os.makedirs(os.path.dirname(generated_apk_path), exist_ok=True)
        with open(generated_apk_path, "w") as f:
            f.write("This is a dummy APK file.")
        print(f"Successfully simulated APK generation at: {generated_apk_path}")
        return generated_apk_path


class ArabicAPKBuilder:
    """
    The core module that orchestrates the Arabic NLP to APK generation process.
    It integrates Lobe 0 (Arabic NLP), Lobe 4 (Code Generation), Lobe 6 (Structure), and Lobe 8 (Compilation).
    """

    def __init__(self):
        self.arabic_nlp = ArabicNLPProcessor()
        self.structure_generator = APKStructureGenerator()
        self.code_generator = CodeGenerator()
        self.apk_generator = APKGemerator()
        self.current_project_path = None
        self.package_name = "com.example.arabicapp"
        self.project_name = "ArabicApp"
        self.layout_file_path = None
        self.main_activity_java_path = None

    def _initialize_project(self, project_name: str, package_name: str):
        """Initializes or re-initializes the Android project structure."""
        self.project_name = project_name
        self.package_name = package_name
        if self.current_project_path and os.path.exists(self.current_project_path):
            print("Cleaning up existing project before re-initialization.")
            self.structure_generator.cleanup_android_project_template(self.current_project_path)
        self.current_project_path = self.structure_generator.create_android_project(self.project_name, self.package_name)
        self.layout_file_path = os.path.join(self.current_project_path, "app", "src", "main", "res", "layout", "activity_main.xml")
        self.main_activity_java_path = os.path.join(self.current_project_path, "app", "src", "main", "java", *self.package_name.split('.'), "MainActivity.java")
        print(f"Project initialized at: {self.current_project_path}")

    def _update_layout_file(self, element_xml: str, position: str = "end_of_file"):
        """Appends new UI element XML to the activity_main.xml file."""
        if not self.layout_file_path:
            raise RuntimeError("Layout file path not set. Project not initialized.")

        print(f"Updating layout file: {self.layout_file_path}")
        with open(self.layout_file_path, 'r') as f:
            layout_content = f.read()

        # Simple insertion: find the closing tag of the root layout and insert before it.
        # More sophisticated logic would parse XML and insert based on position.
        match = re.search(r"(<LinearLayout.*?>\n)(.*?)(\n</LinearLayout>)", layout_content, re.DOTALL)
        if match:
            root_start, existing_elements, root_end = match.groups()
            # Add the new element. For "adjacent" positioning, this needs more logic
            # to modify parent layout params or add constraints.
            # For now, we just append.
            new_layout_content = f"{root_start}{existing_elements}\n{element_xml}\n{root_end}"
        else:
            # Fallback if the assumed LinearLayout structure isn't found
            # This assumes the existing layout has a root element that can be closed.
            if '</LinearLayout>' in layout_content:
                parts = layout_content.split('</LinearLayout>')
                new_layout_content = parts[0] + f'\n{element_xml}\n' + '</LinearLayout>' + "".join(parts[1:])
            elif '</RelativeLayout>' in layout_content:
                parts = layout_content.split('</RelativeLayout>')
                new_layout_content = parts[0] + f'\n{element_xml}\n' + '</RelativeLayout>' + "".join(parts[1:])
            elif '</ConstraintLayout>' in layout_content:
                parts = layout_content.split('</ConstraintLayout>')
                new_layout_content = parts[0] + f'\n{element_xml}\n' + '</ConstraintLayout>' + "".join(parts[1:])
            else:
                # Very basic fallback: append before the closing manifest tag (if not XML) or at the end.
                new_layout_content = layout_content.replace("</activity_main>", f"{element_xml}\n</activity_main>")


        with open(self.layout_file_path, 'w') as f:
            f.write(new_layout_content)

    def _update_activity_file(self, code_snippet: str):
        """Appends code snippets to the MainActivity.java file."""
        if not self.main_activity_java_path:
            raise RuntimeError("Main Activity Java path not set. Project not initialized.")

        print(f"Updating activity file: {self.main_activity_java_path}")
        with open(self.main_activity_java_path, 'r') as f:
            activity_content = f.read()

        # Find the onCreate method and insert the snippet before the closing brace.
        # This is a simplified approach; real code injection needs AST parsing.
        onCreate_match = re.search(r"protected void onCreate\(Bundle savedInstanceState\) \{\n(.*)\n\}\n", activity_content, re.DOTALL)
        if onCreate_match:
            onCreate_body = onCreate_match.group(1)
            # Ensure we don't add duplicates or break formatting
            if code_snippet not in onCreate_body:
                # Add a newline if needed, and ensure no double newlines
                new_onCreate_body = onCreate_body.strip() + "\n\n" + code_snippet.strip() + "\n"
                new_activity_content = activity_content.replace(onCreate_match.group(0), f"protected void onCreate(Bundle savedInstanceState) {{\n{new_onCreate_body}}}\n", 1)
            else:
                new_activity_content = activity_content # Snippet already exists
        else:
            # Fallback if onCreate not found in expected format
            new_activity_content = activity_content.replace("}\n}", f"{code_snippet}\n}}")


        with open(self.main_activity_java_path, 'w') as f:
            f.write(new_activity_content)

    def process_arabic_instruction_to_apk(self, arabic_instruction: str, project_name: str = "ArabicApp", package_name: str = "com.example.arabicapp") -> str:
        """
        Processes a natural language Arabic instruction and orchestrates the generation of an APK.
        This function acts as the main entry point for the objective.

        Args:
            arabic_instruction: The natural language Arabic instruction (e.g., "أضف صورة بجانب النص الذي يشير إلى 'الصفحة الرئيسية'.").
            project_name: The desired name for the Android project.
            package_name: The desired package name for the Android application.

        Returns:
            The path to the generated APK file, or an empty string if generation failed.
        """
        print(f"\n--- Processing Arabic Instruction: '{arabic_instruction}' ---")

        # Step 1: Initialize or ensure project structure exists (Lobe 6)
        if self.current_project_path is None or self.project_name != project_name or self.package_name != package_name:
            self._initialize_project(project_name, package_name)

        # Step 2: Parse the Arabic instruction (Lobe 0)
        parsed_instruction = self.arabic_nlp.process_instruction(arabic_instruction)
        print(f"Parsed instruction: {parsed_instruction}")

        # Step 3: Generate code based on parsed instruction (Lobe 4)
        # This part is highly dependent on the NLP output and requires mapping
        # parsed entities to UI elements and actions.

        generated_ui_element_xml = ""
        generated_activity_snippet = ""
        element_id = None
        target_text_for_linking = None

        # Handle adding an image next to text as per the example instruction
        if "add" in parsed_instruction.get("actions", []) and "image" in parsed_instruction.get("elements", []):
            image_attributes = parsed_instruction.get("attributes", {})
            element_id = f"img_{image_attributes.get('image_source', 'default').replace('.png', '')}" # Generate a unique ID

            # Generate the ImageView XML
            generated_ui_element_xml = self.code_generator.generate_layout_element_code(
                element_type="ImageView",
                attributes={
                    "id": element_id,
                    "image_source": image_attributes.get("image_source", "default_icon.png"),
                    "layout_width": "wrap_content", # Defaulting for now
                    "layout_height": "wrap_content"  # Defaulting for now
                }
            )

            # Generate activity snippet to potentially link it to text
            target_text_for_linking = image_attributes.get("target_text")
            if target_text_for_linking:
                # We need to find the ID of the TextView that corresponds to target_text_for_linking.
                # This requires looking at what has already been added to the layout, or
                # assuming a standard "homepage" text element exists.
                # For now, let's assume `code_generator.find_element_id_by_text` can resolve it.
                existing_element_id = self.code_generator.find_element_id_by_text(target_text_for_linking, self.layout_file_path)
                generated_activity_snippet = self.code_generator.generate_activity_code_snippet(
                    element_id=element_id,
                    action="add",
                    attributes={
                        "elements": ["image"],
                        "attributes": {
                            "target_text_id": existing_element_id,
                            "image_source": image_attributes.get("image_source", "default_icon.png")
                        }
                    }
                )

        # Add a placeholder for the text if it's mentioned and not already handled implicitly
        if "text" in parsed_instruction.get("elements", []) and target_text_for_linking:
             text_attributes = parsed_instruction.get("attributes", {})
             # If the target text itself needs to be added as a new element
             if "target_text" in text_attributes and text_attributes["target_text"] not in self.current_layout_elements_text:
                text_element_id = f"text_{hash(text_attributes['target_text']) % 10000}"
                generated_text_xml = self.code_generator.generate_layout_element_code(
                    element_type="TextView",
                    attributes={
                        "id": text_element_id,
                        "text": text_attributes["target_text"],
                        "layout_width": "wrap_content",
                        "layout_height": "wrap_content"
                    }
                )
                # Update layout file with the text element
                self._update_layout_file(generated_text_xml)
                self.current_layout_elements_text.append(text_attributes["target_text"]) # Track added text

             # If the image is meant to be next to *this* specific text
             if "image" in parsed_instruction.get("elements", []): # If image is also requested
                 image_attributes_for_text = parsed_instruction.get("attributes", {})
                 # Ensure we have an image element generated and linked to the text
                 if not generated_ui_element_xml:
                     element_id = f"img_{image_attributes_for_text.get('image_source', 'default').replace('.png', '')}"
                     generated_ui_element_xml = self.code_generator.generate_layout_element_code(
                        element_type="ImageView",
                        attributes={
                            "id": element_id,
                            "image_source": image_attributes_for_text.get("image_source", "default_icon.png"),
                            "layout_width": "wrap_content",
                            "layout_height": "wrap_content"
                        }
                    )
                 if not generated_activity_snippet:
                    existing_element_id = self.code_generator.find_element_id_by_text(text_attributes["target_text"], self.layout_file_path)
                    generated_activity_snippet = self.code_generator.generate_activity_code_snippet(
                        element_id=element_id,
                        action="add",
                        attributes={
                            "elements": ["image"],
                            "attributes": {
                                "target_text_id": existing_element_id,
                                "image_source": image_attributes_for_text.get("image_source", "default_icon.png")
                            }
                        }
                    )


        # Step 4: Update layout file with generated UI elements (integrating Lobe 4 with Lobe 6)
        if generated_ui_element_xml:
            self._update_layout_file(generated_ui_element_xml)

        # Step 5: Update activity file with generated code snippets (integrating Lobe 4 with Lobe 6)
        if generated_activity_snippet:
            self._update_activity_file(generated_activity_snippet)

        # Step 6: Compile the APK (Lobe 8)
        print("\n--- Initiating APK compilation ---")
        generated_apk_path = self.apk_generator.generate_apk(self.current_project_path, self.project_name)

        print("\n--- APK Generation Process Finished ---")
        if generated_apk_path and os.path.exists(generated_apk_path):
            print(f"Successfully generated APK at: {generated_apk_path}")
            return generated_apk_path
        else:
            print("APK generation process failed.")
            return ""

    def cleanup_project(self):
        """Cleans up the currently managed Android project."""
        if self.current_project_path:
            print(f"\n--- Cleaning up demo project: {self.current_project_path} ---")
            self.structure_generator.cleanup_android_project_template(self.current_project_path)
            self.current_project_path = None
            print("Project cleanup complete.")

    # Internal tracking for elements added to the layout to aid linking
    current_layout_elements_text: List[str] = []
    current_layout_elements_ids: Dict[str, str] = {} # map text to id, or id to type


# --- Example Usage ---
if __name__ == "__main__":
    builder = ArabicAPKBuilder()

    # Example 1: Add an image next to text indicating "Homepage"
    instruction_1 = "أضف صورة بجانب النص الذي يشير إلى 'الصفحة الرئيسية'."
    # For this to work, we need to ensure 'الصفحة الرئيسية' text is present or generated.
    # Let's assume the initial template doesn't have it, so we might need to add it.
    # In a more advanced scenario, the NLP would detect that the target text doesn't exist and propose to add it.

    # Let's first add the "Homepage" text, then the image next to it.
    # This requires a multi-step process or a more intelligent single instruction parser.

    print("--- Scenario: Adding text and then an image ---")
    # Simulate adding the text first
    builder._initialize_project("MyArabicApp", "com.example.myarabicapp")
    homepage_text_id = "homepage_text_view" # Example ID
    builder.current_layout_elements_text.append("الصفحة الرئيسية")
    builder.current_layout_elements_ids["الصفحة الرئيسية"] = homepage_text_id

    text_element_xml = builder.code_generator.generate_layout_element_code(
        element_type="TextView",
        attributes={
            "id": homepage_text_id,
            "text": "الصفحة الرئيسية",
            "layout_width": "wrap_content",
            "layout_height": "wrap_content"
        }
    )
    builder._update_layout_file(text_element_xml)
    print("Added 'الصفحة الرئيسية' text to layout.")

    # Now, process the instruction to add an image next to it.
    # We need to modify the instruction or how it's processed to recognize "الصفحة الرئيسية" refers to an existing element.
    # For simplicity here, we'll manually pass the 'target_text_id' during parsing simulation.
    # In a real system, Lobe 0 would need to infer this from the available UI elements.

    # Mocking Lobe 0's output for the complex instruction to include the target text ID
    mocked_parsed_instruction_1 = {
        "actions": ["add"],
        "elements": ["image"],
        "attributes": {
            "image_source": "homepage_icon.png",
            "position": "adjacent",
            "target_text": "الصفحة الرئيسية",
            "target_text_id": homepage_text_id # This would be inferred by NLP/UI analysis
        }
    }
    # Override NLP processor for this specific call to use mocked output
    original_process_instruction = builder.arabic_nlp.process_instruction
    builder.arabic_nlp.process_instruction = lambda instruction: mocked_parsed_instruction_1
    print("\n--- Processing instruction to add image next to 'الصفحة الرئيسية' ---")
    generated_apk_path_1 = builder.process_arabic_instruction_to_apk(instruction_1, project_name="MyArabicApp", package_name="com.example.myarabicapp")

    # Restore the original NLP processor
    builder.arabic_nlp.process_instruction = original_process_instruction

    if generated_apk_path_1:
        print(f"APK generated for instruction 1: {generated_apk_path_1}")
    else:
        print("APK generation failed for instruction 1.")

    builder.cleanup_project()

    print("\n--- Scenario: Simple text addition ---")
    # Example 2: Add simple text
    instruction_2 = "أضف نصًا يقول 'مرحباً بالعالم'."
    builder._initialize_project("HelloWorldApp", "com.example.helloworld")

    # Simulate processing this instruction
    parsed_instruction_2 = builder.arabic_nlp.process_instruction(instruction_2)
    print(f"Parsed instruction 2: {parsed_instruction_2}")

    if "add" in parsed_instruction_2.get("actions", []) and "text" in parsed_instruction_2.get("elements", []):
        text_attributes_2 = parsed_instruction_2.get("attributes", {})
        text_content_2 = text_attributes_2.get("text", "Default Text")
        text_element_id_2 = f"text_{hash(text_content_2) % 10000}"
        builder.current_layout_elements_text.append(text_content_2)
        builder.current_layout_elements_ids[text_content_2] = text_element_id_2

        generated_text_xml_2 = builder.code_generator.generate_layout_element_code(
            element_type="TextView",
            attributes={
                "id": text_element_id_2,
                "text": text_content_2,
                "layout_width": "wrap_content",
                "layout_height": "wrap_content"
            }
        )
        builder._update_layout_file(generated_text_xml_2)
        print(f"Added text element to layout: {generated_text_xml_2}")

        # No specific activity snippet needed for simple text addition for this demo.
        generated_apk_path_2 = builder.process_arabic_instruction_to_apk(instruction_2, project_name="HelloWorldApp", package_name="com.example.helloworld")

        if generated_apk_path_2:
            print(f"APK generated for instruction 2: {generated_apk_path_2}")
        else:
            print("APK generation failed for instruction 2.")
    else:
        print("Instruction 2 not recognized as a text addition.")

    builder.cleanup_project()