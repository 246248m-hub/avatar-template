# Lobe 2_context_understanding_lobe

import re

class ContextUnderstandingLobe:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.context_cache = {}

    def understand_context(self, natural_language_input: str, user_id: str = "default_user") -> dict:
        """
        Analyzes natural language input to extract contextual information,
        identifying entities, intents, and relationships relevant to APK generation.
        """
        if user_id in self.context_cache and self.context_cache[user_id]['input'] == natural_language_input:
            return self.context_cache[user_id]['context']

        context_data = {
            "entities": self._extract_entities(natural_language_input),
            "intent": self._determine_intent(natural_language_input),
            "relationships": self._identify_relationships(natural_language_input),
            "keywords": self._extract_keywords(natural_language_input)
        }
        self.context_cache[user_id] = {'input': natural_language_input, 'context': context_data}
        return context_data

    def _extract_entities(self, text: str) -> list:
        """
        Placeholder for named entity recognition (NER).
        In a real implementation, this would use NLP libraries (e.g., spaCy, NLTK)
        and potentially custom trained models for APK-specific entities.
        For now, a simple regex-based approach for demonstration.
        """
        entities = []
        # Example: Look for words that might represent UI elements or features
        potential_ui_elements = re.findall(r'\b(button|text field|label|image|list|screen|activity|dialog)\b', text, re.IGNORECASE)
        for element in potential_ui_elements:
            entities.append({"type": "UI_ELEMENT", "value": element.lower()})

        # Example: Look for common programming concepts
        potential_code_concepts = re.findall(r'\b(function|variable|class|method|loop|condition|data)\b', text, re.IGNORECASE)
        for concept in potential_code_concepts:
            entities.append({"type": "CODE_CONCEPT", "value": concept.lower()})

        # Add more sophisticated entity extraction here, possibly by querying knowledge_base
        # Example: If knowledge_base contains known component names or libraries
        # for known_component in self.knowledge_base.get("apk_components", []):
        #     if known_component.lower() in text.lower():
        #         entities.append({"type": "KNOWN_COMPONENT", "value": known_component})

        return entities

    def _determine_intent(self, text: str) -> str:
        """
        Placeholder for intent classification.
        Determines the user's primary goal or action.
        """
        text_lower = text.lower()
        if "create an app" in text_lower or "build an apk" in text_lower:
            return "CREATE_APK"
        elif "add a button" in text_lower or "include text" in text_lower:
            return "ADD_UI_ELEMENT"
        elif "define a function" in text_lower or "write code" in text_lower:
            return "DEFINE_LOGIC"
        elif "show a list" in text_lower or "display data" in text_lower:
            return "DISPLAY_DATA"
        else:
            return "UNKNOWN_INTENT"

    def _identify_relationships(self, text: str) -> list:
        """
        Placeholder for relationship extraction.
        Identifies how different entities are related.
        """
        relationships = []
        # Example: Simple relationship extraction based on keywords
        if "add a" in text and "to the" in text:
            parts = text.split("add a", 1)[1].split("to the", 1)
            if len(parts) == 2:
                item_to_add = parts[0].strip()
                target_element = parts[1].strip()
                relationships.append({
                    "subject": {"type": "UI_ELEMENT", "value": item_to_add},
                    "predicate": "ADD_TO",
                    "object": {"type": "UI_ELEMENT", "value": target_element}
                })
        return relationships

    def _extract_keywords(self, text: str) -> list:
        """
        Extracts significant keywords from the input text.
        """
        # Simple keyword extraction using common NLP techniques (e.g., TF-IDF if applied to a corpus)
        # For simplicity here, just split and filter common words.
        words = re.findall(r'\w+', text.lower())
        stopwords = set(["a", "an", "the", "is", "it", "of", "to", "and", "in", "for", "with", "this", "that", "on", "at", "by", "from"])
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        return list(set(keywords))

# --- Integration with previous lobes (conceptual) ---
# This lobe would typically receive input from Lobe 1 (Natural Language Processing)
# and pass its extracted context to Lobe 3 (Abstraction and Modeling) or directly
# to Lobe 4 (Code Generation) if the context is simple enough.

# Example usage (for demonstration, not part of the final output):
if __name__ == "__main__":
    # Mock knowledge base for demonstration
    mock_knowledge_base = {
        "apk_components": ["TextView", "Button", "EditText", "ImageView", "RecyclerView", "Activity", "Fragment"],
        "common_libraries": ["androidx.appcompat.app.AppCompatActivity", "android.widget.Button"]
    }

    context_analyzer = ContextUnderstandingLobe(mock_knowledge_base)

    user_prompt_1 = "Create a simple Android app with a button that says 'Click Me' and a text field."
    context_1 = context_analyzer.understand_context(user_prompt_1)
    print(f"Context for prompt 1: {context_1}")

    user_prompt_2 = "I need to add a function to handle button clicks."
    context_2 = context_analyzer.understand_context(user_prompt_2)
    print(f"Context for prompt 2: {context_2}")

    user_prompt_3 = "Show a list of user names on the main screen."
    context_3 = context_analyzer.understand_context(user_prompt_3)
    print(f"Context for prompt 3: {context_3}")

# // Lobe 2_context_understanding_lobe Last Thought: The context understanding lobe has been implemented with basic entity, intent, and relationship extraction capabilities.
# // The next logical step is to process this extracted context into a more abstract representation, suitable for further processing or code generation.
# // This leads to Lobe 3_abstraction_and_modeling_lobe.

print("\n--- Initiating next step: Lobe 3_abstraction_and_modeling_lobe ---")