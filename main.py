import urllib.request
import json
import os
import sys

# Define configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
QWEN_MODEL = "local-deepseek"
GRANITE_MODEL = "granite-direct:latest" # Custom model from earlier projects
DATA_FILE = "sample_seo_data.txt"
OUTPUT_FILE = "SEO_Report.md"

def generate_ollama(model_name, prompt, system_prompt="", disable_think=False):
    """Utility function to call Ollama API."""
    print(f"[*] Calling model: {model_name}...")
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }
    
    if disable_think:
        payload["options"]["think"] = False
        
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "")
    except Exception as e:
        print(f"[!] Error communicating with Ollama: {e}")
        sys.exit(1)

def main():
    if not os.path.exists(DATA_FILE):
        print(f"[!] Error: {DATA_FILE} not found.")
        sys.exit(1)
        
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        seo_data = f.read()

    print("[*] Stage 1: Clustering Search Intents and identifying Cannibalization (Qwen)...")
    qwen_system_prompt = (
        "You are an expert SEO Strategist. Analyze the provided keyword and URL data. "
        "Cluster the search intents, identify overlapping keywords across different URLs "
        "(keyword cannibalization), and provide a strategic recommendation to resolve conflicts. "
        "CRITICAL: Do not output any <think> tags or reasoning steps. Only output the final analysis."
    )
    
    qwen_prompt = f"Data:\n{seo_data}\n\nAnalyze the data and find cannibalization issues."
    
    # Passing disable_think=True to add options={"think": False}
    qwen_analysis = generate_ollama(QWEN_MODEL, qwen_prompt, qwen_system_prompt, disable_think=True)
    
    print("[*] Stage 2: Formatting output into a professional Markdown report (Granite)...")
    granite_system_prompt = (
        "You are an expert technical writer and AI assistant. Your task is to take the raw SEO analysis "
        "and format it into a pristine, highly professional Markdown report. Use headers, bullet points, "
        "tables, and bold text for emphasis. Do not alter the core findings."
    )
    
    granite_prompt = f"Raw SEO Analysis:\n{qwen_analysis}\n\nPlease format this into a professional Markdown document."
    
    final_report = generate_ollama(GRANITE_MODEL, granite_prompt, granite_system_prompt)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"[*] Success! Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
