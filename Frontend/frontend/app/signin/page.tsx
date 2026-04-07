"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { USER_STORAGE_KEY } from "../lib/storage";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type Creator = {
  id: number;
  email: string;
  userName: string;
  niche: string;
  instagram: string | null;
  youtube: string | null;
  tiktok: string | null;
};

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [message, setMessage] = useState<string | null>(null);

  async function handleSignIn(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!email.includes("@")) {
      setStatus("error");
      setMessage("Enter a valid email address.");
      return;
    }

    setStatus("loading");
    setMessage("Searching for your profile…");

    try {
      const url = new URL(`${API_BASE}/users/me`);
      url.searchParams.set("email", email.toLowerCase());
      const response = await fetch(url);
      if (response.status === 404) {
        setStatus("error");
        setMessage("No account found. Please sign up.");
        return;
      }
      if (!response.ok) throw new Error("Unable to reach backend");
      const match: Creator = await response.json();
      if (typeof window !== "undefined") {
        window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(match));
      }
      setMessage("Signed in. Redirecting…");
      router.push("/");
    } catch (error) {
      setStatus("error");
      setMessage("Unable to sign in right now.");
    }
  }

  return (
    <div className="min-h-screen bg-[#05060b] px-4 py-16 text-white">
      <div className="mx-auto flex max-w-3xl flex-col gap-8 rounded-3xl border border-white/10 bg-gradient-to-br from-purple-600/30 via-black/60 to-black/80 p-10 shadow-[0_35px_80px_rgba(5,6,11,0.9)]">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-white/60">
            Creator-Link.AI
          </p>
          <h1 className="mt-3 text-4xl font-semibold text-white">
            Welcome back, creator
          </h1>
          <p className="mt-2 text-sm text-white/60">
            Sign in with your email to open the recommendation canvas. No
            account?{" "}
            <Link href="/signup" className="text-rose-400 underline">
              Create one
            </Link>
            .
          </p>
        </div>

        <form
          className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-black/40 p-6"
          onSubmit={handleSignIn}
        >
          <label className="text-sm text-white/70">
            Email
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              className="mt-1 w-full rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-white placeholder:text-white/40 focus:border-white focus:outline-none"
              placeholder="creator@studio.com"
            />
          </label>
          <button
            type="submit"
            className="mt-2 rounded-2xl bg-gradient-to-r from-fuchsia-500 via-pink-500 to-rose-500 px-6 py-3 text-lg font-semibold text-white transition hover:brightness-110 disabled:opacity-70"
            disabled={status === "loading"}
          >
            {status === "loading" ? "Checking…" : "Sign in"}
          </button>
        </form>
        {message && <p className="text-sm text-white/70">{message}</p>}
      </div>
    </div>
  );
}
