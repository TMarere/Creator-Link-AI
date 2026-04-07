# Creator-Link-AI
# CreatorLink AI

CreatorLink AI is a full-stack web application that helps small content creators generate content ideas and discover potential collaborators using AI-powered recommendations. Instead of building an internal messaging system, the platform connects creators directly through their Instagram profiles to encourage real-world collaboration.



---

## 🚀 Features

- **AI Content Generation**
  - Generates platform-specific content ideas based on niche, platform, and growth goals
  - Uses OpenAI’s API to produce creative and actionable suggestions

- **Creator Profiles**
  - Creators can create profiles including niche, platform, goals, and Instagram link
  - Profiles are stored and managed using a relational database

- **AI-Powered Creator Matching**
  - Recommends similar creators based on profile similarity
  - Designed to support embedding-based matching for scalable recommendations

- **Direct Instagram Linking**
  - Instead of building an internal chat system, creators can connect instantly via Instagram
  - Reduces system complexity while improving real-world usability

---

## 🧠 System Architecture

## 🐳 Docker

- The repository ships a `Dockerfile` that builds the backend using the pinned `Backend/requirements.txt`; it installs dependencies, copies the backend source, and runs `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Build the image with `docker build -t creator-link-ai .` (run from the repo root) and run it with `docker run -p 8000:8000 creator-link-ai`. The backend will then be reachable at `http://localhost:8000`.
- Use `.env` variables before building or mount a file into `/app/backend/.env` if you need custom secrets or database URLs.

## ⚙️ Backend API & Setup

- **Bootstrap steps**:
  1. `cd Backend`
  2. `source venv/bin/activate` (or use `./venv/bin/python` directly)
  3. `python -m pip install -r requirements.txt`
  4. `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
  5. `python -m pytest app/test/tests.py`
  6. Keep this backend process running while you develop; your frontend fetches from `localhost:8000` and the root returns `{"message":"CreatorLink AI backend is running"}` so you know it is healthy.

- **Documented endpoints**:
  - `POST /users/` – Creates a creator. Accepts `{"email": "...", "userName": "...", "niche": "...", "instagram": "...", "youtube": "...", "tiktok": "..."}` (the social handles are optional) and returns the saved `UserResponse`.
  - `GET /users/` – Lists every creator record in the database.
  - `GET /recommendations/{user_id}` – Returns structured content ideas (`short_form`, `long_form`, `deep_dive`) tailored to that creator’s niche plus `related_creators`.
- `GET /connections?niche={niche}&excludeId={id}` – Returns creators that share the same niche so the front-end “Connection” tab can show relevant matches.
- Recommendations now combine same-niche creators plus curated short/long/deep prompts using the new `generate_recommendations(db, user_id, niche)` helper, so the UI sees targeted content-creation ideas before falling back to defaults.

## 🎨 Frontend

- The Next.js client lives in `Frontend/frontend` and starts with a sign-in/sign-up card; after onboarding it renders the recommendation canvas plus the discovery tab for creators in your niche.
- Run the frontend workflow from that directory:
  1. `npm install`
  2. `NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev`
  3. `npm run lint`
- The environment variable `NEXT_PUBLIC_API_BASE` should point to whichever backend host you want to talk to (the default is `http://localhost:8000`).
