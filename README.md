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

- **Documented endpoints**:
  - `POST /users/` – Creates a creator. Accepts `{"email": "...", "userName": "..."}` and returns the saved `UserResponse`.
  - `GET /users/` – Lists every creator record in the database.
  - `GET /recommendations/{user_id}` – Calls the stubbed `generate_recommendations(user_id)` and returns `{"user_id": ..., "recommendations": [...]}` so clients can start consuming recommendation data right away.
