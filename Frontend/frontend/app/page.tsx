"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type Creator = {
  id: number;
  email: string;
  userName: string;
};

export default function Home() {
  const [users, setUsers] = useState<Creator[]>([]);
  const [formState, setFormState] = useState({ email: "", userName: "" });
  const [status, setStatus] = useState<"idle" | "saving" | "error">("idle");
  const [message, setMessage] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [activeUser, setActiveUser] = useState<Creator | null>(null);
  const [isFetchingRecs, setIsFetchingRecs] = useState(false);

  const heroUser = useMemo(() => users[0] ?? null, [users]);

  useEffect(() => {
    void refreshUsers();
  }, []);

  async function refreshUsers() {
    try {
      const res = await fetch(`${API_BASE}/users/`);
      if (!res.ok) {
        throw new Error("Unable to load creators");
      }
      setUsers(await res.json());
      setMessage(null);
    } catch (err) {
      setMessage("Could not load creators right now.");
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("saving");
    setMessage(null);

    try {
      const response = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formState),
      });

      if (!response.ok) {
        throw new Error("Unable to save creator");
      }

      setFormState({ email: "", userName: "" });
      await refreshUsers();
      setStatus("idle");
      setMessage("Creator saved successfully!");
    } catch (err) {
      setStatus("error");
      setMessage("Saving failed — check your data and try again.");
    }
  }

  async function loadRecommendations(user: Creator) {
    setActiveUser(user);
    setIsFetchingRecs(true);
    setRecommendations([]);
    try {
      const response = await fetch(`${API_BASE}/recommendations/${user.id}`);
      if (!response.ok) {
        throw new Error("Failed to load recommendations");
      }
      const payload = await response.json();
      setRecommendations(payload.recommendations ?? []);
    } catch (err) {
      setMessage("Could not load recommendations for that creator.");
    } finally {
      setIsFetchingRecs(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#05060b] py-12 text-white">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-6 lg:flex-row lg:items-start">
        <section className="flex w-full flex-col gap-6 rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 via-white/0 to-transparent p-8 shadow-[0_25px_70px_rgba(8,12,20,0.9)] backdrop-blur-xl lg:w-2/3">
          <div className="flex flex-col gap-3">
            <p className="text-sm uppercase tracking-[0.4em] text-white/60">
              Creator-Link.AI
            </p>
            <h1 className="text-4xl font-semibold leading-tight text-white">
              Match creators with AI-assisted recommendations
            </h1>
            <p className="max-w-2xl text-lg text-white/70">
              Capture creator profiles, keep a live list, and peek at the
              recommendation candidates our backend serves up.
            </p>
          </div>

          <form
            className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-black/30 p-6"
            onSubmit={handleSubmit}
          >
            <div className="flex flex-col gap-2">
              <label className="text-sm text-white/70" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={formState.email}
                onChange={(event) =>
                  setFormState((prev) => ({ ...prev, email: event.target.value }))
                }
                required
                placeholder="creator@studio.com"
                className="rounded-xl border border-white/20 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 shadow-inner focus:border-white focus:outline-none"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm text-white/70" htmlFor="userName">
                Display name
              </label>
              <input
                id="userName"
                value={formState.userName}
                onChange={(event) =>
                  setFormState((prev) => ({
                    ...prev,
                    userName: event.target.value,
                  }))
                }
                required
                placeholder="Tanatswa Creative"
                className="rounded-xl border border-white/20 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 shadow-inner focus:border-white focus:outline-none"
              />
            </div>
            <button
              className="mt-2 rounded-2xl bg-gradient-to-r from-fuchsia-500 via-pink-500 to-rose-500 px-6 py-3 text-lg font-semibold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:brightness-75"
              type="submit"
              disabled={status === "saving"}
            >
              {status === "saving" ? "Saving..." : "Save creator"}
            </button>
          </form>

          <div className="flex items-center justify-between">
            <p className="text-sm text-white/60">Status</p>
            <p className="text-sm text-white/70">{message ?? "Idle"}</p>
          </div>
          {heroUser && (
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.3em] text-white/60">
                Most recent creator
              </p>
              <div className="mt-2 flex items-center justify-between">
                <div>
                  <p className="text-xl font-semibold text-white">
                    {heroUser.userName}
                  </p>
                  <p className="text-sm text-white/60">{heroUser.email}</p>
                </div>
                <button
                  className="rounded-xl border border-white/20 px-4 py-2 text-sm text-white transition hover:bg-white/10"
                  onClick={() => void loadRecommendations(heroUser)}
                >
                  Get recommendations
                </button>
              </div>
            </div>
          )}
        </section>

        <section className="flex w-full flex-col gap-8 lg:w-1/3">
          <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-black/50 p-6 shadow-[0_25px_30px_rgba(0,0,0,0.4)] backdrop-blur-xl">
            <h2 className="text-lg font-semibold text-white">Creators</h2>
            <div className="mt-4 flex flex-col gap-3">
              {users.length === 0 ? (
                <p className="text-sm text-white/60">No creators yet.</p>
              ) : (
                users.map((creator) => (
                  <button
                    key={creator.id}
                    className="flex w-full cursor-pointer items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-left text-white transition hover:border-white/60"
                    onClick={() => void loadRecommendations(creator)}
                  >
                    <div>
                      <p className="text-sm font-semibold">{creator.userName}</p>
                      <p className="text-xs text-white/60">{creator.email}</p>
                    </div>
                    <span className="text-xs text-white/50">recs →</span>
                  </button>
                ))
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-gradient-to-tr from-amber-500/10 via-pink-500/10 to-cyan-500/20 p-6 shadow-[0_25px_30px_rgba(0,0,0,0.4)] backdrop-blur-xl">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Recommendations</h2>
              {activeUser && (
                <span className="text-xs uppercase tracking-[0.3em] text-white/60">
                  for {activeUser.userName}
                </span>
              )}
            </div>
            {isFetchingRecs && (
              <p className="mt-3 text-sm text-white/60">Loading recs…</p>
            )}
            {!isFetchingRecs && recommendations.length === 0 && (
              <p className="mt-3 text-sm text-white/60">
                Click a creator to see matching collaborators.
              </p>
            )}
            <ul className="mt-4 flex flex-col gap-2">
              {recommendations.map((rec) => (
                <li
                  key={rec}
                  className="rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-white"
                >
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        </section>
      </div>
    </div>
  );
}
