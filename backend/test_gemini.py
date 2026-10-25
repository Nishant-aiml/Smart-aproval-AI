"""
Test Google Gemini API connectivity and functionality.
Model: Gemini 1.5 Flash (cheapest, fastest, free tier)
"""

import os
import sys
import time
import warnings
from pathlib import Path
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=FutureWarning)

# Set utf-8 output encoding if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load env variables from backend/.env or root .env
backend_env = Path(__file__).resolve().parent / ".env"
root_env = Path(__file__).resolve().parent.parent / ".env"

if backend_env.exists():
    load_dotenv(backend_env)
if root_env.exists():
    load_dotenv(root_env)

# Also ensure backend is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

print("=" * 60)
print("GOOGLE GEMINI API DIAGNOSTIC TEST")
print("=" * 60)
print(f"Target Model: {model_name} (Fast, Cheap, Free-tier)")

if not gemini_key:
    print("\n[!] GEMINI_API_KEY is not set!")
    print("Please add your key to .env or backend/.env:")
    print("  GEMINI_API_KEY=your_gemini_api_key_here")
    print("\nGet a free API key at: https://aistudio.google.com/app/apikey")
    sys.exit(1)

print(f"API Key present: Yes (Length: {len(gemini_key)} chars)")

# Test 1: Native google.generativeai SDK
print("\n--- Test 1: Native google.generativeai SDK ---")
try:
    import google.generativeai as genai
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel(model_name)
    
    start = time.time()
    response = model.generate_content("Say hello and confirm you are Gemini in under 10 words.")
    elapsed = time.time() - start
    
    print(f"[OK] Native Gemini call succeeded in {elapsed:.2f}s")
    print(f"     Response: {response.text.strip()}")
except Exception as e:
    print(f"[FAIL] Native Gemini call failed: {e}")

# Test 2: OpenAI-Compatible Endpoint
print("\n--- Test 2: OpenAI-Compatible Endpoint (v1beta/openai) ---")
try:
    from openai import OpenAI
    client = OpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    start = time.time()
    res = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": "Say hello"}],
        timeout=30
    )
    elapsed = time.time() - start
    reply = (res.choices[0].message.content or "").strip()
    print(f"[OK] OpenAI-compatible endpoint succeeded in {elapsed:.2f}s")
    print(f"     Response: {reply}")
except Exception as e:
    print(f"[FAIL] OpenAI-compatible endpoint failed: {e}")

# Test 3: Structured JSON Extraction Test
print("\n--- Test 3: Structured JSON Generation (Used for block extraction) ---")
try:
    from ai.gemini_client import GeminiClient
    client = GeminiClient()
    start = time.time()
    test_json = client.generate_text(
        prompt="Extract: 'Total Faculty: 45, Infrastructure area: 12000 sq ft' into JSON with total_faculty and area.",
        system_prompt="Return only valid JSON.",
        json_mode=True
    )
    elapsed = time.time() - start
    print(f"[OK] JSON generation succeeded in {elapsed:.2f}s")
    print(f"     Output: {test_json.strip()}")
except Exception as e:
    print(f"[FAIL] JSON generation test failed: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
