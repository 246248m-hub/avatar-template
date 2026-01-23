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
            if res.status_code == 429:
                print(f"⚠️ Quota Exhausted. Sleeping 70s...")
                time.sleep(70); continue
            if "candidates" in data:
                text = data['candidates'][0]['content']['parts'][0]['text']
                return text.replace("```python", "").replace("```", "").strip()
            time.sleep(30)
        except:
            time.sleep(20)
    return None

error_context = ""
if os.path.exists("error_log.txt"):
    with open("error_log.txt", "r") as f: error_context = f.read()[-800:]

memory = ""
if os.path.exists("knowledge_base"):
    files = sorted([f for f in os.listdir("knowledge_base") if f.startswith("task_")])
    if files:
        with open(os.path.join("knowledge_base", files[-1]), "r") as c:
            memory = f"// Last Task Context: {c.read()[-300:]}\n"

obj = os.getenv("OBJECTIVE")
prompt = f"Objective: {obj}\nErrors: {error_context}\nLast Memory: {memory}\nTask: Generate next Python code. Respond ONLY with raw code."

code = ask_gemini(prompt)
if code and len(code) > 20:
    with open("current_thought.txt", "w") as f: f.write(code)
else:
    print("⚠️ Quota/API issue. Hibernating.")
    sys.exit(0) 
