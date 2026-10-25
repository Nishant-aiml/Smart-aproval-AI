"""Check database, storage, and auth status"""
import os
import sys

# Check database
try:
    from config.database import get_db, Batch, Block, Document
    db = next(get_db())
    batches = db.query(Batch).count()
    blocks = db.query(Block).count()
    docs = db.query(Document).count()
    print("DATABASE: OK")
    print(f"  - Batches: {batches}")
    print(f"  - Blocks: {blocks}")
    print(f"  - Documents: {docs}")
    db.close()
except Exception as e:
    print(f"DATABASE: FAILED - {e}")

# Check storage
upload_dir = "data/uploads"
if os.path.exists(upload_dir):
    files = len(os.listdir(upload_dir))
    print(f"STORAGE: OK (data/uploads exists, {files} files)")
else:
    print("STORAGE: data/uploads not found")

# Check auth config
try:
    from config.settings import settings
    has_firebase = bool(settings.FIREBASE_API_KEY and settings.FIREBASE_PROJECT_ID)
    if has_firebase:
        print("AUTH (Firebase): Configured")
        print(f"  - Project: {settings.FIREBASE_PROJECT_ID}")
    else:
        print("AUTH (Firebase): NOT configured (missing API key or project ID)")
except Exception as e:
    print(f"AUTH: Error checking - {e}")

# Check AI (Gemini primary)
try:
    from config.settings import settings
    if settings.GEMINI_API_KEY:
        print(f"GEMINI (Primary): Configured (Model: {settings.GEMINI_MODEL})")
    else:
        print(f"GEMINI (Primary): NOT configured (GEMINI_API_KEY missing, Model: {settings.GEMINI_MODEL})")
    if settings.OPENAI_API_KEY:
        print("OPENAI (Fallback): Configured")
    else:
        print("OPENAI (Fallback): NOT configured")
except Exception as e:
    print(f"AI Status: Error - {e}")
