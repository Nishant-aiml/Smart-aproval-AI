# Smart Approval AI - Port & Server Rules

## Dedicated Non-Conflicting Ports
This PC hosts 5-6 concurrent projects on Ngrok. To prevent collisions with any other project, Smart Approval AI MUST ALWAYS run on these dedicated ports:

- **Frontend (Next.js)**: Port **3050** (`http://localhost:3050`)
- **Backend (FastAPI)**: Port **8050** (`http://127.0.0.1:8050`)
- **Ngrok Web Inspector**: Port **4050** (`http://127.0.0.1:4050`)

## System Rules & Guidelines
1. **Never revert to default ports (3000, 8000, 4040)**:
   - Always run Next.js on port `3050` (`npx next dev -p 3050` or `npm run dev`).
   - Always run uvicorn / FastAPI on port `8050` (`--port 8050`).
   - Always bind Ngrok web inspector to `127.0.0.1:4050`.

2. **Next.js Reverse Proxy Architecture**:
   - All browser requests use relative `/api/...`.
   - `frontend/next.config.mjs` proxies `/api/:path*` to `http://127.0.0.1:8050/api/:path*`.
   - This ensures ONLY 1 Ngrok tunnel is needed (pointing to port 3050), preserving Ngrok tunnel limits across multiple projects.

3. **Launcher Scripts**:
   - `start_all_with_ngrok.bat`: Boots Backend (8050) + Frontend (3050) + Ngrok (4050) in separate terminals.
   - `start_dev.bat`: Boots Backend (8050) + Frontend (3050) for local development.
   - `start_ngrok.bat`: Launches the isolated Ngrok tunnel on port 3050.
