import requests, json, os, time

def ask_gemini(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json", "User-Agent": "Phoenix-Architect/1.0"}
    
    for i in range(5):
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=60)
            data = res.json()
            if "candidates" in data:
                return data['candidates'][0]['content']['parts'][0]['text'].replace("```python", "").replace("```", "").strip()
            print(f"⚠️ Retry {i+1} due to: {data}")
            time.sleep(40 * (i+1))
        except:
            time.sleep(20)
    return None

# جلب سياق الأخطاء السابقة للإصلاح
error_context = ""
if os.path.exists("error_log.txt"):
    with open("error_log.txt", "r") as f:
        error_context = f"\n⚠️ PREVIOUS FAILURE ERROR: {f.read()[-600:]}\nFix this error in the new code."

# جلب سياق الذاكرة السابقة
context = ""
if os.path.exists("knowledge_base"):
    files = sorted([f for f in os.listdir("knowledge_base") if f.startswith("task_")])
    for f in files[-3:]:
        with open(os.path.join("knowledge_base", f), "r") as c: context += c.read()[-800:]

objective = os.getenv("OBJECTIVE")
full_prompt = f"Objective: {objective}. {error_context}\nPast Context: {context}\nTask: Write the next self-contained Python script. Respond ONLY with raw code."

code = ask_gemini(full_prompt)
if code:
    with open("current_task.py", "w") as f: f.write(code)
    print("✅ Evolution Code Generated.")
else:
    print("❌ Failed to reach AI Core."); exit(1)
