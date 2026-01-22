import requests, json, os, time

def ask_gemini(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    for i in range(5):
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=60)
            data = res.json()
            if "candidates" in data:
                return data['candidates'][0]['content']['parts'][0]['text'].replace("```python", "").replace("```", "").strip()
            time.sleep(40)
        except:
            time.sleep(20)
    return None

error_context = ""
if os.path.exists("error_log.txt"):
    with open("error_log.txt", "r") as f:
        error_context = f"\n⚠️ LAST FAILURE: {f.read()[-500:]}"

obj = os.getenv("OBJECTIVE")
prompt = f"Objective: {obj}. {error_context}\nWrite next Python script. Code only."

code = ask_gemini(prompt)
if code:
    with open("current_task.py", "w") as f: f.write(code)
else:
    exit(1)
