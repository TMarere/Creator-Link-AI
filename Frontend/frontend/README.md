This Next.js project ships the Creator-Link.AI dashboard. Vision: sign up with an email, display name, and niche, then step straight into both the recommendation canvas and the connections tab that surfaces creators in your niche.

## Getting Started

1. `cd Frontend/frontend`
2. `npm install`
3. `NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev`

The default development server starts on [http://localhost:3000](http://localhost:3000). The `NEXT_PUBLIC_API_BASE` variable tells the UI where to fetch `/users`, `/recommendations`, and `/connections` from.

## Script reference

- `npm run dev` – Starts the Next.js app in development mode with hot reload.
- `npm run lint` – Runs the project's ESLint configuration to keep the new UI polished.

## UX flow

1. `/signin` is the entry point; it looks up your email via `GET /users` and, when found, stores that creator before redirecting to `/`.
2. If the email doesn’t exist yet, follow the “Create one” link to `/signup`, enter email + display name + niche + optional Instagram/YouTube/TikTok handles, and the app will create the profile and jump back to `/`.
3. The dashboard (`/`) only renders when a signed-in creator exists in `localStorage`. It exposes search/sorting on the creator list, plus dedicated “Recommendations” (short/long/deep idea lists + related creators) and “Connections” tabs powered by `/recommendations` and `/connections`.
