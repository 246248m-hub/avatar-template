import requests, json, os, time, sys, random

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

# 1. كشف الحلقات المفرغة (Behavioral Awareness)
loop_stall = False
if os.path.exists("action_log.txt"):
    with open("action_log.txt", "r") as f:
        lines = f.readlines()
        if lines[-5:].count("RESULT: Failure\n") >= 4: loop_stall = True

# 2. إدارة الثقة (Oracle Confidence)
conf = open("oracle_confidence.txt").read() if os.path.exists("oracle_confidence.txt") else "100"

# 3. جرد ذاكرة الفصوص الـ 12 للترابط المعرفي
memory = ""
if os.path.exists("knowledge_base"):
    for lobe in sorted(os.listdir("knowledge_base")):
        p = os.path.join("knowledge_base", lobe)
        if os.path.isdir(p) and (files := sorted(os.listdir(p))):
            memory += f"// Lobe {lobe} Context: {open(os.path.join(p, files[-1])).read()[-250:]}\n"

prompt = f"Objective: {os.getenv('OBJECTIVE')}\nStall: {loop_stall}\nConfidence: {conf}%\nMemory:\n{memory}\n"
prompt += "Task: Generate next step. Respond with Python code or 'COMMANDER_REPAIR:'/'YML_REPAIR:' + code."

code = ask_gemini(prompt)
if code:
    with open("current_thought.txt", "w") as f: f.write(code)
    # تحديث مقياس الثقة بناءً على جودة الاستجابة
    new_conf = min(100, int(conf) + 5) if len(code) > 100 else max(0, int(conf) - 10)
    with open("oracle_confidence.txt", "w") as f: f.write(str(new_conf))
else: sys.exit(0)
