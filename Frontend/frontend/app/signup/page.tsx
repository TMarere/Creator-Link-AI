"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { CREATOR_STORAGE_KEY, USER_STORAGE_KEY } from "../lib/storage";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type Creator = {
  id: number;
  email: string;
  userName: string;
  niche: string;
};

export default function SignUpPage() {
  const router = useRouter();
  const [formState, setFormState] = useState({
    email: "",
    userName: "",
    niche: "",
  });
  const [status, setStatus] = useState<"idle" | "saving" | "error">("idle");
  const [message, setMessage] = useState<string | null>(null);

  async function handleSignUp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!formState.email.includes("@") || formState.userName.length < 2) {
      setStatus("error");
      setMessage("Provide a valid email and display name.");
      return;
    }
    if (!formState.niche.trim()) {
      setStatus("error");
      setMessage("Share your niche so we can recommend matches.");
      return;
    }

    setStatus("saving");
    setMessage("Creating your profile…");

    try {
      const response = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formState),
      });
      if (!response.ok) throw new Error("Unable to sign up");
      const payload: Creator = await response.json();
      if (typeof window !== "undefined") {
        window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(payload));
        const cached = window.localStorage.getItem(CREATOR_STORAGE_KEY);
        const list = cached ? (JSON.parse(cached) as Creator[]) : [];
        window.localStorage.setItem(
          CREATOR_STORAGE_KEY,
          JSON.stringify([...list, payload])
        );
      }
      setMessage("Profile created! Redirecting…");
      router.push("/");
    } catch (error) {
      setStatus("error");
      setMessage("Could not create your profile.");
    }
  }

  return (
    <div className="min-h-screen bg-[#040510] px-4 py-16 text-white">
      <div className="mx-auto flex max-w-3xl flex-col gap-8 rounded-3xl border border-white/10 bg-gradient-to-br from-indigo-500/30 via-black/60 to-black/80 p-10 shadow-[0_35px_80px_rgba(5,6,11,0.9)]">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-white/60">
            Creator-Link.AI
          </p>
          <h1 className="mt-3 text-4xl font-semibold text-white">
            Create your account
          </h1>
          <p className="mt-2 text-sm text-white/60">
            Already have an account?{" "}
            <Link href="/signin" className="text-rose-400 underline">
              Sign in
            </Link>
            .
          </p>
        </div>

        <form
          className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-black/40 p-6"
          onSubmit={handleSignUp}
        >
          <label className="text-sm text-white/70">
            Email
            <input
              type="email"
              value={formState.email}
              onChange={(event) =>
                setFormState((prev) => ({ ...prev, email: event.target.value }))
              }
              required
              className="mt-1 w-full rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-white placeholder:text-white/40 focus:border-white focus:outline-none"
              placeholder="creator@studio.com"
            />
          </label>
          <label className="text-sm text-white/70">
            Display name
            <input
              value={formState.userName}
              onChange={(event) =>
                setFormState((prev) => ({ ...prev, userName: event.target.value }))
              }
              required
              className="mt-1 w-full rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-white placeholder:text-white/40 focus:border-white focus:outline-none"
              placeholder="Tanatswa Creative"
            />
          </label>
          <label className="text-sm text-white/70">
            Niche
            <input
              value={formState.niche}
              onChange={(event) =>
                setFormState((prev) => ({ ...prev, niche: event.target.value }))
              }
              required
              className="mt-1 w-full rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-white placeholder:text-white/40 focus:border-white focus:outline-none"
              placeholder="Fashion, AI, or Wellness"
            />
          </label>
          <button
            type="submit"
            className="mt-2 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 px-6 py-3 text-lg font-semibold text-white transition hover:brightness-110 disabled:opacity-70"
            disabled={status === "saving"}
          >
            {status === "saving" ? "Creating…" : "Create account"}
          </button>
        </form>
        {message && <p className="text-sm text-white/70">{message}</p>}
      </div>
    </div>
  );
}
