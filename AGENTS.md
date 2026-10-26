# Smart Approval AI - Port & Server Rules

## Dedicated Non-Conflicting Ports
This PC hosts 5-6 concurrent projects on Ngrok. To prevent collisions with any other project, Smart Approval AI MUST ALWAYS run on these dedicated ports:

- **Frontend (Next.js)**: Port **3051** (`http://localhost:3051`)
- **Backend (FastAPI)**: Port **8051** (`http://127.0.0.1:8051`)
- **Ngrok Web Inspector**: Port **4051** (`http://127.0.0.1:4051`)

## System Rules & Guidelines
1. **Never revert to default ports (3000, 8000, 4040)**:
   - Always run Next.js on port `3051` (`npx next dev -p 3051` or `npm run dev`).
   - Always run uvicorn / FastAPI on port `8051` (`--port 8051`).
   - Always bind Ngrok web inspector to `127.0.0.1:4051`.

2. **Next.js Reverse Proxy Architecture**:
   - All browser requests use relative `/api/...`.
   - `frontend/next.config.mjs` proxies `/api/:path*` to `http://127.0.0.1:8051/api/:path*`.
   - This ensures ONLY 1 Ngrok tunnel is needed (pointing to port 3051), preserving Ngrok tunnel limits across multiple projects.

3. **Launcher Scripts**:
   - `start_all_with_ngrok.bat`: Boots Backend (8051) + Frontend (3051) + Ngrok (4051) in separate terminals.
   - `start_dev.bat`: Boots Backend (8051) + Frontend (3051) for local development.
   - `start_ngrok.bat`: Launches the isolated Ngrok tunnel on port 3051.
