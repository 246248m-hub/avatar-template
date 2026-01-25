import requests, json, os, time, sys

def ask_gemini(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    for i in range(3):
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=90)
            data = res.json()
            if "candidates" in data: return data['candidates'][0]['content']['parts'][0]['text'].strip()
            time.sleep(30)
        except: time.sleep(20)
    return None

loop_stall = False
if os.path.exists("action_log.txt"):
    with open("action_log.txt", "r") as f:
        lines = f.readlines()
        if lines[-5:].count("RESULT: Failure\n") >= 4: loop_stall = True

conf = open("oracle_confidence.txt").read() if os.path.exists("oracle_confidence.txt") else "100"

memory = ""
if os.path.exists("knowledge_base"):
    for lobe in sorted(os.listdir("knowledge_base")):
        p = os.path.join("knowledge_base", lobe)
        if os.path.isdir(p) and (files := sorted(os.listdir(p))):
            memory += f"// Lobe {lobe} Last Thought: {open(os.path.join(p, files[-1])).read()[-300:]}\n"

prompt = f"""
Objective: {os.getenv('OBJECTIVE')}
Confidence: {conf}% | Stall: {loop_stall}
Interlinked Memory:
{memory}

TASK: Build the next logical FUNCTIONAL Python module.
CRITICAL RULES:
1. NO PLACEHOLDERS. Do not use 'print' statements only.
2. WRITES REAL LOGIC: Define functions, classes, and real algorithms.
3. INTEGRATION: Focus on building NLP Arabic logic and APK structure.
4. FORMAT: Respond ONLY with raw Python code. No conversational text.
"""

code = ask_gemini(prompt)
if code:
    code = code.replace("```python", "").replace("```", "").strip()
    with open("current_thought.txt", "w") as f: f.write(code)
    new_conf = min(100, int(conf) + 5) if len(code) > 200 else max(0, int(conf) - 15)
    with open("oracle_confidence.txt", "w") as f: f.write(str(new_conf))
else: sys.exit(0)
