# Render.com + PostgreSQL Deployment Guide — Smart Approval AI

This guide walks you through deploying **Smart Approval AI** on [Render.com](https://render.com) using a **Managed PostgreSQL Database**.

---

## 🏗️ Architecture on Render

```
┌─────────────────────────────────┐
│     Next.js Frontend Service    │
│  (smart-approval-frontend)      │
│  Port: Dynamic ($PORT)          │
└────────────────┬────────────────┘
                 │ (Internal proxy /api/* -> BACKEND_URL)
                 ▼
┌─────────────────────────────────┐
│     FastAPI Backend Service     │
│   (smart-approval-backend)      │
│   Uvicorn on $PORT              │
└────────────────┬────────────────┘
                 │ (SQLAlchemy via DATABASE_URL)
                 ▼
┌─────────────────────────────────┐
│   Render Managed PostgreSQL     │
│      (smart-approval-db)        │
└─────────────────────────────────┘
```

---

## 🚀 Option 1: 1-Click Blueprint Deployment (Recommended)

Render includes native Infrastructure-as-Code support via the included [`render.yaml`](./render.yaml).

1. **Push your code to GitHub**:
   Ensure your latest code is pushed to your GitHub repository:
   ```bash
   git push origin main
   ```

2. **Open Render Dashboard**:
   - Go to [dashboard.render.com](https://dashboard.render.com).
   - Click **"New +"** in the top navigation bar.
   - Select **"Blueprint"**.

3. **Connect Your Repository**:
   - Select your GitHub repo (`Smart-aproval-AI`).
   - Render will detect [`render.yaml`](./render.yaml) automatically.

4. **Review & Configure Environment Variables**:
   Render will show the 3 components it will create:
   - 🐘 **Database**: `smart-approval-db` (PostgreSQL)
   - 🐍 **Backend**: `smart-approval-backend` (FastAPI)
   - ⚡ **Frontend**: `smart-approval-frontend` (Next.js)

   Fill in your secret keys when prompted:
   - `GEMINI_API_KEY`: Your Google AI Studio API key (`AQ.Ab8RN6...`).
   - (Optional) `OPENAI_API_KEY`: If using OpenAI.

5. **Click "Apply"**:
   Render provisions PostgreSQL, runs database migrations automatically on startup, compiles Next.js, and deploys both services with live HTTPS URLs!

---

## 🛠️ Option 2: Manual Setup via Render Dashboard

If you prefer to configure each service manually in the Render UI:

### Step 1: Create the PostgreSQL Database
1. In Render Dashboard, click **New +** → **PostgreSQL**.
2. Set:
   - **Name**: `smart-approval-db`
   - **Database**: `smart_approval`
   - **User**: `smart_approval_user`
   - **Region**: Same region for all services (e.g. `Oregon (US West)` or `Frankfurt (EU)`)
   - **Plan**: `Free`
3. Click **Create Database**.
4. Once created, copy the **Internal Database URL** (e.g. `postgres://smart_approval_user:...@dpg-...-a/smart_approval`).

---

### Step 2: Deploy the FastAPI Backend
1. Click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Name**: `smart-approval-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: `Free`

4. Add **Environment Variables** in the Environment tab:
   | Key | Value | Notes |
   | :--- | :--- | :--- |
   | `DATABASE_URL` | *(Paste Internal Database URL from Step 1)* | Automatically auto-converts `postgres://` to `postgresql://` |
   | `AI_PROVIDER` | `gemini` | Primary AI engine |
   | `GEMINI_MODEL` | `gemini-3.5-flash` | Fast, low latency |
   | `GEMINI_MODEL_FALLBACK` | `gemini-3.5-flash-lite` | Backup model |
   | `GEMINI_API_KEY` | *(Your Gemini API Key)* | From [aistudio.google.com](https://aistudio.google.com) |
   | `FIREBASE_PROJECT_ID` | `smart-approval-ai` | Auth / storage project |
   | `FIREBASE_STORAGE_BUCKET` | `smart-approval-ai.firebasestorage.app` | Storage bucket |

5. Click **Create Web Service**.
6. When the build finishes, copy your backend URL (e.g. `https://smart-approval-backend.onrender.com`).

---

### Step 3: Deploy the Next.js Frontend
1. Click **New +** → **Web Service**.
2. Connect the same repository.
3. Configure the service:
   - **Name**: `smart-approval-frontend`
   - **Region**: Same as backend
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Runtime**: `Node`
   - **Build Command**:
     ```bash
     npm install && npm run build
     ```
   - **Start Command**:
     ```bash
     npm run start
     ```
   - **Plan**: `Free`

4. Add **Environment Variables**:
   | Key | Value | Notes |
   | :--- | :--- | :--- |
   | `BACKEND_URL` | `https://smart-approval-backend.onrender.com` | URL from Step 2 |
   | `NEXT_PUBLIC_API_BASE` | `/api` | Relative base for frontend calls |

5. Click **Create Web Service**.

---

## 🔍 How PostgreSQL is Handled in Code

- In [`backend/config/database.py`](./backend/config/database.py):
  ```python
  DATABASE_URL = os.getenv("DATABASE_URL")
  if DATABASE_URL:
      if DATABASE_URL.startswith("postgres://"):
          DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
      engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)
  else:
      # Local development fallback to SQLite
      engine = create_engine(f"sqlite:///{DB_PATH}", ...)
  ```
- In [`backend/requirements.txt`](./backend/requirements.txt):
  - `psycopg2-binary>=2.9.9` is included for PostgreSQL support.
- In [`frontend/next.config.mjs`](./frontend/next.config.mjs):
  - Automatically rewrites all `/api/*` and `/docs` routes to `BACKEND_URL`.

---

## ✅ Post-Deployment Verification Checklist

1. **Verify Backend**: Open `https://<your-backend>.onrender.com/docs` to see Swagger UI.
2. **Verify Database**: Check backend logs in Render dashboard. You should see:
   ```
   INFO: Connecting to PostgreSQL database (Render / Production)
   INFO: PostgreSQL database initialized successfully (Render / Production)
   ```
3. **Verify Frontend**: Open `https://<your-frontend>.onrender.com` to see the Next.js application.
4. **Verify Proxied API**: Open `https://<your-frontend>.onrender.com/api/batches/list` — it should return JSON without CORS issues.
