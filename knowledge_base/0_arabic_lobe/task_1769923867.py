import os
import re
import subprocess
import shutil
import xml.etree.ElementTree as ET

# Assume KNOWLEDGE_BASE_DIR is defined elsewhere and accessible
# Assume OUTPUT_DIR is defined elsewhere and accessible

# --- Lobe 1_arabic_parser_lobe ---

class ArabicSyntaxAnalyzer:
    def __init__(self, grammar_rules_path="arabic_grammar.txt"):
        self.grammar_rules_path = grammar_rules_path
        self.grammar_rules = self._load_grammar()

    def _load_grammar(self):
        if not os.path.exists(self.grammar_rules_path):
            # Create a dummy grammar file if it doesn't exist for demonstration
            with open(self.grammar_rules_path, "w", encoding="utf-8") as f:
                f.write("sentence = subject verb object\n")
                f.write("subject = noun pronoun\n")
                f.write("verb = present_verb past_verb\n")
                f.write("object = noun pronoun\n")
                f.write("noun = 'سيارة' 'رجل' 'امرأة'\n")
                f.write("pronoun = 'هو' 'هي' 'هم'\n")
                f.write("present_verb = 'يذهب' 'يرى'\n")
                f.write("past_verb = 'ذهب' 'رأى'\n")
            print(f"Created dummy grammar file: {self.grammar_rules_path}")
        with open(self.grammar_rules_path, "r", encoding="utf-8") as f:
            rules = {}
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    rules[key.strip()] = [v.strip() for v in value.split()]
            return rules

    def parse(self, text):
        """
        Analyzes Arabic text against defined grammar rules.
        This is a simplified context-free grammar parser for demonstration.
        A real-world implementation would use more sophisticated NLP techniques
        like dependency parsing or transformer-based models.
        """
        tokens = text.split()
        analysis = self._recursive_parse(tokens, "sentence")
        return analysis

    def _recursive_parse(self, tokens, rule_name):
        if rule_name not in self.grammar_rules:
            if rule_name in tokens:
                return {"type": "token", "value": rule_name}
            else:
                return None

        for production in self.grammar_rules.get(rule_name, []):
            if isinstance(production, list):  # Handle multiple options for a rule
                for sub_production in production:
                    result = self._apply_production(tokens, rule_name, sub_production)
                    if result:
                        return result
            else:
                result = self._apply_production(tokens, rule_name, production)
                if result:
                    return result
        return None

    def _apply_production(self, tokens, rule_name, production_rule):
        if not isinstance(production_rule, list):
            production_rule = production_rule.split()

        current_tokens_index = 0
        parsed_components = []

        for component in production_rule:
            if component in self.grammar_rules:
                # It's a non-terminal symbol
                sub_rule_name = component
                # Try to match the sub-rule with the remaining tokens
                match_result = self._recursive_parse(tokens[current_tokens_index:], sub_rule_name)
                if match_result:
                    parsed_components.append({"type": "non_terminal", "name": sub_rule_name, "content": match_result})
                    # Advance tokens_index by the number of tokens consumed by the sub-rule
                    # This is a simplification; a real parser would track consumed tokens more precisely
                    if match_result.get("type") == "token":
                        current_tokens_index += 1
                    elif match_result.get("type") == "non_terminal":
                        # Count tokens consumed by the nested non-terminal
                        consumed_count = self._count_tokens_consumed(match_result)
                        current_tokens_index += consumed_count
                    else: # If it's a list of parsed elements
                        current_tokens_index += len(match_result.get("elements", []))
                else:
                    return None  # Failed to match sub-rule
            else:
                # It's a terminal symbol (a literal word)
                if current_tokens_index < len(tokens) and tokens[current_tokens_index] == component:
                    parsed_components.append({"type": "terminal", "value": component})
                    current_tokens_index += 1
                else:
                    return None  # Failed to match terminal
        
        # If all components of the production rule were matched successfully
        if current_tokens_index == len(tokens): # Ensure all tokens were consumed for this rule
            if len(parsed_components) == 1 and parsed_components[0].get("type") == "non_terminal":
                return parsed_components[0]["content"] # Return the content of the single non-terminal
            elif parsed_components:
                return {"type": "structure", "name": rule_name, "elements": parsed_components}
            else:
                return None
        return None
        
    def _count_tokens_consumed(self, parsed_data):
        """Helper to count tokens consumed by a parsed structure."""
        if parsed_data.get("type") == "token" or parsed_data.get("type") == "terminal":
            return 1
        elif parsed_data.get("type") == "non_terminal":
            return self._count_tokens_consumed(parsed_data["content"])
        elif parsed_data.get("type") == "structure":
            count = 0
            for element in parsed_data.get("elements", []):
                if element.get("type") == "token" or element.get("type") == "terminal":
                    count += 1
                elif element.get("type") == "non_terminal":
                    count += self._count_tokens_consumed(element["content"])
            return count
        return 0


# --- Lobe 2_arabic_generator_lobe ---

class ArabicTextGenerator:
    def __init__(self, language_model_path="arabic_lm.txt"):
        self.language_model_path = language_model_path
        self.language_model = self._load_language_model()

    def _load_language_model(self):
        if not os.path.exists(self.language_model_path):
            # Create a dummy language model for demonstration
            with open(self.language_model_path, "w", encoding="utf-8") as f:
                f.write("سيارة: جميلة, سريعة\n")
                f.write("رجل: طويل, قوي\n")
                f.write("امرأة: ذكية, لطيفة\n")
                f.write("يذهب: إلى, مع\n")
                f.write("يرى: القط, الكلب\n")
                f.write("ذهب: إلى, في\n")
                f.write("رأى: الأطفال, السماء\n")
                f.write("هو: سيارة, رجل, القط\n")
                f.write("هي: امرأة, سيارة, القط\n")
                f.write("هم: رجل, امرأة, الأطفال\n")
            print(f"Created dummy language model file: {self.language_model_path}")
        
        model = {}
        with open(self.language_model_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, value_str = line.strip().split(":", 1)
                    model[key.strip()] = [v.strip() for v in value_str.split(",")]
        return model

    def generate_text(self, prompt_parts, max_length=50):
        """
        Generates Arabic text based on a simplified language model.
        This is a very basic probabilistic generation.
        """
        generated_words = []
        current_prompt_part = prompt_parts[0] if prompt_parts else None
        
        if current_prompt_part not in self.language_model:
            return "لا يمكن توليد نص لهذا الجزء."

        possible_next_words = self.language_model[current_prompt_part]
        
        if not possible_next_words:
            return current_prompt_part

        # Simplified selection: just pick the first available for deterministic output
        # In a real model, this would involve sampling based on probabilities
        chosen_next_word = possible_next_words[0]
        generated_words.append(current_prompt_part)
        generated_words.append(chosen_next_word)

        # Continue generation based on the last generated word, if possible
        for _ in range(max_length - 2):
            if chosen_next_word in self.language_model:
                next_options = self.language_model[chosen_next_word]
                if next_options:
                    chosen_next_word = next_options[0] # Simplified selection
                    generated_words.append(chosen_next_word)
                else:
                    break
            else:
                break
        
        return " ".join(generated_words)

# --- Lobe 7_nlp_to_android_logic_lobe ---

class AndroidLogicMapper:
    def __init__(self, mapping_rules_path="nlp_to_android_rules.xml"):
        self.mapping_rules_path = mapping_rules_path
        self.mapping_rules = self._load_mapping_rules()

    def _load_mapping_rules(self):
        if not os.path.exists(self.mapping_rules_path):
            # Create a dummy mapping rule file for demonstration
            dummy_rules = """<?xml version="1.0" encoding="UTF-8"?>
<rules>
    <rule>
        <nlp_pattern>عرض النص</nlp_pattern>
        <android_logic>
            <activity_type>MainActivity</activity_type>
            <layout_element>TextView</layout_element>
            <action>setText</action>
        </android_logic>
    </rule>
    <rule>
        <nlp_pattern>النقر على الزر</nlp_pattern>
        <android_logic>
            <activity_type>MainActivity</activity_type>
            <layout_element>Button</layout_element>
            <action>setOnClickListener</action>
        </android_logic>
    </rule>
    <rule>
        <nlp_pattern>الانتقال إلى الشاشة</nlp_pattern>
        <android_logic>
            <activity_type>Intent</activity_type>
            <action>startActivity</action>
        </android_logic>
    </rule>
</rules>
            """
            with open(self.mapping_rules_path, "w", encoding="utf-8") as f:
                f.write(dummy_rules)
            print(f"Created dummy mapping rules file: {self.mapping_rules_path}")

        tree = ET.parse(self.mapping_rules_path)
        root = tree.getroot()
        rules = {}
        for rule_elem in root.findall('rule'):
            nlp_pattern = rule_elem.find('nlp_pattern').text
            android_logic = {}
            for child in rule_elem.find('android_logic'):
                android_logic[child.tag] = child.text
            rules[nlp_pattern] = android_logic
        return rules

    def map_nlp_to_android(self, nlp_command):
        """
        Maps a natural language command to Android development logic.
        This is a pattern matching approach.
        """
        for pattern, logic in self.mapping_rules.items():
            # Simple string matching for demonstration
            if pattern in nlp_command:
                return logic
        return None

# --- Lobe 0_arabic_lobe (Integration Example) ---

class ArabicAPKBuilderModule:
    def __init__(self, knowledge_base_dir="knowledge_base", output_dir="generated_apk_files"):
        self.knowledge_base_dir = knowledge_base_dir
        self.output_dir = output_dir

        # Ensure directories exist
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize lobes
        self.arabic_parser = ArabicSyntaxAnalyzer(grammar_rules_path=os.path.join(self.knowledge_base_dir, "arabic_grammar.txt"))
        self.arabic_generator = ArabicTextGenerator(language_model_path=os.path.join(self.knowledge_base_dir, "arabic_lm.txt"))
        self.nlp_android_mapper = AndroidLogicMapper(mapping_rules_path=os.path.join(self.knowledge_base_dir, "nlp_to_android_rules.xml"))

    def process_arabic_request(self, arabic_prompt):
        """
        Processes an Arabic prompt, parses it, generates Android logic,
        and conceptually prepares for APK building.
        """
        print(f"Received Arabic prompt: '{arabic_prompt}'")

        # 1. Parse the Arabic prompt
        parsed_structure = self.arabic_parser.parse(arabic_prompt)
        print(f"Parsed structure: {parsed_structure}")

        if not parsed_structure:
            print("Could not parse the Arabic prompt effectively.")
            return

        # 2. Map parsed NLP components to Android logic (simplified)
        # We'll use the raw prompt for mapping as a fallback/simpler example
        android_logic = self.nlp_android_mapper.map_nlp_to_android(arabic_prompt)
        print(f"Mapped Android logic: {android_logic}")

        if not android_logic:
            print("No specific Android logic mapped for this prompt.")
            return

        # 3. Generate conceptual Android code or configuration based on mapped logic
        # This is where Lobe 4_code_generation_lobe would come in.
        # For this module, we'll just print a conceptual representation.
        generated_android_concept = self._generate_android_concept(arabic_prompt, parsed_structure, android_logic)
        print(f"Generated Android Concept:\n{generated_android_concept}")

        # 4. Prepare for APK compilation (Lobe 8_apk_compiler_lobe)
        # This step would involve actually creating Java/Kotlin files, XML layouts, etc.
        # For now, we simulate by creating a placeholder file.
        self._simulate_apk_preparation(generated_android_concept)

        print("\n--- Arabic APK Builder Module Processing Complete ---")

    def _generate_android_concept(self, nlp_prompt, parsed_structure, android_logic):
        """
        Generates a conceptual representation of Android code based on NLP input.
        This is a placeholder for Lobe 4_code_generation_lobe.
        """
        concept = f"// Generated Android concept for NLP prompt: '{nlp_prompt}'\n"
        concept += f"// Parsed Structure: {parsed_structure}\n"
        concept += f"// Mapped Android Logic: {android_logic}\n\n"

        activity_type = android_logic.get('activity_type', 'Activity')
        layout_element = android_logic.get('layout_element', 'View')
        action = android_logic.get('action', 'performAction')

        concept += f"// Simulate Android Activity: {activity_type}\n"
        concept += f"public class {activity_type} {{\n"
        concept += f"    public void onCreate() {{\n"
        concept += f"        // Find {layout_element}\n"
        concept += f"        {layout_element} uiElement = findViewById({layout_element}_ID);\n"
        concept += f"        // Perform action: {action}\n"
        if action == 'setText':
            concept += f"        uiElement.setText(\"Hello from NLP!\");\n"
        elif action == 'setOnClickListener':
            concept += f"        uiElement.setOnClickListener(new View.OnClickListener() {{\n"
            concept += f"            @Override\n"
            concept += f"            public void onClick(View v) {{\n"
            concept += f"                // Handle click event\n"
            concept += f"            }}\n"
            concept += f"        }});\n"
        elif action == 'startActivity':
            concept += f"        Intent intent = new Intent(this, TargetActivity.class);\n"
            concept += f"        startActivity(intent);\n"
        else:
            concept += f"        // Placeholder for {action}\n"
        concept += f"    }}\n"
        concept += f"}}\n\n"

        return concept

    def _simulate_apk_preparation(self, android_concept):
        """
        Simulates the creation of files needed for an APK.
        This module will create a conceptual Android code file.
        """
        print(f"Simulating APK preparation in: {self.output_dir}")
        # Create a dummy Java/Kotlin file representing the Android code
        # In a real scenario, this would be part of a more complex project structure.
        java_code_filename = os.path.join(self.output_dir, "GeneratedActivity.java")
        with open(java_code_filename, "w", encoding="utf-8") as f:
            f.write(android_concept)
        print(f"Created conceptual Android code file: {java_code_filename}")

        # Clean up the dummy directory if it exists and contains old files from previous runs
        # This is to ensure a clean state for the demo.
        # In a real application, you might want to manage output directories differently.
        if os.path.exists(self.output_dir):
            for item in os.listdir(self.output_dir):
                item_path = os.path.join(self.output_dir, item)
                if os.path.isfile(item_path) and item != os.path.basename(java_code_filename):
                    os.remove(item_path)

    def demo(self):
        print("\n--- Arabic APK Builder Module Demo ---")

        # Example 1: Command to display text
        prompt_display_text = "أريد عرض النص على الشاشة"
        self.process_arabic_request(prompt_display_text)

        # Example 2: Command to click a button
        prompt_click_button = "عند النقر على الزر"
        self.process_arabic_request(prompt_click_button)

        # Example 3: Command to navigate
        prompt_navigate = "الانتقال إلى الشاشة التالية"
        self.process_arabic_request(prompt_navigate)

        # Example 4: A command that might not have a direct mapping
        prompt_unmapped = "تغيير لون الخلفية"
        self.process_arabic_request(prompt_unmapped)

        print("\n--- Arabic APK Builder Module Demo Finished ---")

# --- Main execution block for the module ---
if __name__ == "__main__":
    # This block is for demonstrating the module in isolation.
    # In the grand objective, these modules would be orchestrated.

    # Setup dummy directories if they don't exist
    if not os.path.exists("knowledge_base"):
        os.makedirs("knowledge_base")
    if not os.path.exists("generated_apk_files"):
        os.makedirs("generated_apk_files")

    arabic_builder = ArabicAPKBuilderModule(
        knowledge_base_dir="knowledge_base",
        output_dir="generated_apk_files"
    )
    arabic_builder.demo()

    # Clean up dummy files and directories created by the demo if desired
    # This is a basic cleanup for the demo script.
    # import shutil
    # if os.path.exists("knowledge_base"):
    #     shutil.rmtree("knowledge_base")
    #     print("Cleaned up knowledge_base directory.")
    # if os.path.exists("generated_apk_files"):
    #     shutil.rmtree("generated_apk_files")
    #     print("Cleaned up generated_apk_files directory.")