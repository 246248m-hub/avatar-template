import os
import re
import shutil
import subprocess
from pathlib import Path

# --- Lobe 0: Language Lobe (Simplified for demonstration) ---
# In a real scenario, this would handle complex NLP tasks for Arabic.

def parse_arabic_intent(text):
    """
    Simulates parsing Arabic text to identify user intent and extract parameters.
    This is a highly simplified example.
    """
    intent_map = {
        "حساب": "calculator",
        "جمع": "add",
        "طرح": "subtract",
        "ضرب": "multiply",
        "قسمة": "divide",
        "رقم": "number"
    }
    words = re.findall(r'\b\w+\b', text.lower(), re.UNICODE)
    intent = "unknown"
    params = {}

    for word in words:
        if word in intent_map:
            intent = intent_map[word]
            break

    # Simple number extraction (assuming integers for demonstration)
    numbers = re.findall(r'\d+', text)
    if numbers:
        params['numbers'] = [int(n) for n in numbers]

    # Basic operator extraction based on intent
    if intent == "add" and 'numbers' in params and len(params['numbers']) >= 2:
        params['operation'] = 'add'
    elif intent == "subtract" and 'numbers' in params and len(params['numbers']) >= 2:
        params['operation'] = 'subtract'
    elif intent == "multiply" and 'numbers' in params and len(params['numbers']) >= 2:
        params['operation'] = 'multiply'
    elif intent == "divide" and 'numbers' in params and len(params['numbers']) >= 2:
        params['operation'] = 'divide'
    elif intent == "calculator" and 'numbers' in params and len(params['numbers']) >= 2:
        # Default to add if just "calculator" and numbers are present
        params['operation'] = 'add'
    elif intent == "calculator" and not params.get('numbers'):
        # Placeholder for a more complex calculator intent that might require specific operations
        params['operation'] = 'prompt_for_operation'


    return {"intent": intent, "params": params}

def generate_arabic_response(parsed_data):
    """
    Generates an Arabic response based on parsed intent.
    """
    intent = parsed_data.get("intent")
    params = parsed_data.get("params", {})
    numbers = params.get('numbers', [])
    operation = params.get('operation', 'unknown')

    if intent == "calculator":
        if operation == 'add':
            result = sum(numbers)
            return f"نتيجة الجمع للأرقام {numbers} هي {result}."
        elif operation == 'subtract' and len(numbers) == 2:
            result = numbers[0] - numbers[1]
            return f"نتيجة الطرح لـ {numbers[0]} - {numbers[1]} هي {result}."
        elif operation == 'multiply' and len(numbers) == 2:
            result = numbers[0] * numbers[1]
            return f"نتيجة الضرب لـ {numbers[0]} * {numbers[1]} هي {result}."
        elif operation == 'divide' and len(numbers) == 2 and numbers[1] != 0:
            result = numbers[0] / numbers[1]
            return f"نتيجة القسمة لـ {numbers[0]} / {numbers[1]} هي {result}."
        elif operation == 'prompt_for_operation':
            return "ما هي العملية الحسابية التي تود إجراؤها؟"
        elif 'numbers' in params and len(numbers) < 2:
            return "أحتاج إلى رقمين على الأقل لإجراء عملية حسابية."
        else:
            return "لا يمكنني فهم العملية الحسابية المطلوبة."
    else:
        return "عذرًا، لا يمكنني فهم طلبك."

# --- Lobe 4: Code Generation Lobe (Simplified for demonstration) ---

def generate_calculator_python_code(operation, numbers):
    """
    Generates Python code for a simple calculator based on the operation and numbers.
    """
    if operation == 'add':
        code = f"result = sum({numbers})\nprint(f'The sum is: {{result}}')\n"
    elif operation == 'subtract' and len(numbers) == 2:
        code = f"result = {numbers[0]} - {numbers[1]}\nprint(f'The difference is: {{result}}')\n"
    elif operation == 'multiply' and len(numbers) == 2:
        code = f"result = {numbers[0]} * {numbers[1]}\nprint(f'The product is: {{result}}')\n"
    elif operation == 'divide' and len(numbers) == 2 and numbers[1] != 0:
        code = f"result = {numbers[0]} / {numbers[1]}\nprint(f'The quotient is: {{result}}')\n"
    else:
        code = "# No valid operation or operands provided\n"
    return code

# --- Lobe 6: Synthesis Lobe ---
# This lobe would orchestrate the flow between other lobes.

def synthesize_apk_from_arabic(arabic_prompt, output_apk_name="GeneratedApp"):
    """
    Synthesizes an APK from an Arabic natural language prompt.
    This is a high-level orchestration function.
    """
    print(f"\n--- Synthesizing APK for prompt: '{arabic_prompt}' ---")

    # Step 1: Parse Arabic prompt using Lobe 0
    parsed_data = parse_arabic_intent(arabic_prompt)
    print(f"Parsed Data: {parsed_data}")

    intent = parsed_data.get("intent")
    params = parsed_data.get("params", {})
    operation = params.get('operation', 'unknown')
    numbers = params.get('numbers', [])

    # Step 2: Generate Python code using Lobe 4
    generated_code = "# Placeholder for generated code\n"
    if intent == "calculator" and operation in ['add', 'subtract', 'multiply', 'divide'] and len(numbers) >= 2:
        generated_code = generate_calculator_python_code(operation, numbers)
        print("Generated Python code for calculator.")
    else:
        print("Could not generate specific code for the prompt. Generating a basic app structure.")
        # Fallback to a simple app structure if specific code generation fails
        generated_code = "print('Hello from your generated app!')\n"

    # Step 3: Prepare for APK Building (Simulated - uses Lobe 8)
    # In a real system, this would involve more complex project setup.
    print("Preparing for APK build...")
    # For demonstration, we'll assume a dummy Python file is created and then passed to the builder.
    dummy_py_file = "generated_script.py"
    with open(dummy_py_file, "w", encoding="utf-8") as f:
        f.write(generated_code)
    print(f"Dummy Python script created: {dummy_py_file}")

    # Step 4: Build APK using Lobe 8 (Simulated APK Builder)
    # This part relies on the APK Builder module (Lobe 8), which is stubbed here.
    try:
        apk_path = build_apk_from_script(dummy_py_file, output_apk_name)
        print(f"APK built successfully: {apk_path}")
        return apk_path
    except Exception as e:
        print(f"Error during APK build: {e}")
        return None
    finally:
        # Clean up dummy files
        if os.path.exists(dummy_py_file):
            os.remove(dummy_py_file)
            print(f"Cleaned up dummy file: {dummy_py_file}")

# --- Lobe 8: APK Compiler Lobe (Simplified Stub) ---
# This lobe would interface with actual Android SDK tools to build an APK.

def build_apk_from_script(python_script_path, app_name):
    """
    Simulates building an APK from a Python script.
    In a real implementation, this would use tools like Kivy/Buildozer, BeeWare, etc.
    """
    print(f"\n--- Simulating APK Build Process for '{app_name}' ---")
    print(f"  - Input Python script: {python_script_path}")

    # Simulate creating a project structure and running build commands
    project_dir = f"{app_name}_project"
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir, exist_ok=True)

    # Simulate copying the script and creating necessary build files
    target_script_path = os.path.join(project_dir, "main.py")
    shutil.copy(python_script_path, target_script_path)

    # Simulate build command execution (e.g., using a hypothetical build tool)
    print(f"  - Executing build command for Android (simulated)...")
    # Example: subprocess.run(['buildozer', 'android', 'debug'], cwd=project_dir, check=True)

    # Simulate the output APK file
    output_apk_dir = os.path.join(project_dir, "bin")
    os.makedirs(output_apk_dir, exist_ok=True)
    simulated_apk_path = os.path.join(output_apk_dir, f"{app_name.lower()}-debug.apk")

    # Create a dummy APK file
    with open(simulated_apk_path, "w") as f:
        f.write(f"This is a simulated APK file for {app_name}.\n")
        f.write(f"Generated from: {python_script_path}\n")

    print(f"  - Simulated APK created at: {simulated_apk_path}")
    print("--- APK Build Simulation Complete ---")
    return simulated_apk_path

# --- Demonstration ---

if __name__ == "__main__":
    # Test Case 1: Simple addition
    arabic_prompt_1 = "احسب مجموع 5 و 7"
    print(f"\n--- Testing Arabic prompt: '{arabic_prompt_1}' ---")
    apk_path_1 = synthesize_apk_from_arabic(arabic_prompt_1, "SumCalculator")
    if apk_path_1:
        print(f"Generated APK for '{arabic_prompt_1}': {apk_path_1}")

    # Test Case 2: Subtraction
    arabic_prompt_2 = "اطرح 10 من 25"
    print(f"\n--- Testing Arabic prompt: '{arabic_prompt_2}' ---")
    apk_path_2 = synthesize_apk_from_arabic(arabic_prompt_2, "DifferenceCalculator")
    if apk_path_2:
        print(f"Generated APK for '{arabic_prompt_2}': {apk_path_2}")

    # Test Case 3: Multiplication
    arabic_prompt_3 = "اضرب 3 في 4"
    print(f"\n--- Testing Arabic prompt: '{arabic_prompt_3}' ---")
    apk_path_3 = synthesize_apk_from_arabic(arabic_prompt_3, "ProductCalculator")
    if apk_path_3:
        print(f"Generated APK for '{arabic_prompt_3}': {apk_path_3}")

    # Test Case 4: Division
    arabic_prompt_4 = "اقسم 100 على 5"
    print(f"\n--- Testing Arabic prompt: '{arabic_prompt_4}' ---")
    apk_path_4 = synthesize_apk_from_arabic(arabic_prompt_4, "QuotientCalculator")
    if apk_path_4:
        print(f"Generated APK for '{arabic_prompt_4}': {apk_path_4}")

    # Test Case 5: Unclear intent for calculator
    arabic_prompt_5 = "أريد استخدام الآلة الحاسبة"
    print(f"\n--- Testing Arabic prompt: '{arabic_prompt_5}' ---")
    apk_path_5 = synthesize_apk_from_arabic(arabic_prompt_5, "BasicCalculator")
    if apk_path_5:
        print(f"Generated APK for '{arabic_prompt_5}': {apk_path_5}")

    # Test Case 6: Unrelated Arabic prompt
    arabic_prompt_6 = "ما هو الطقس اليوم؟"
    print(f"\n--- Testing Arabic prompt: '{arabic_prompt_6}' ---")
    apk_path_6 = synthesize_apk_from_arabic(arabic_prompt_6, "GreetingApp")
    if apk_path_6:
        print(f"Generated APK for '{arabic_prompt_6}': {apk_path_6}")

    print("\n--- All Demonstrations Completed ---")