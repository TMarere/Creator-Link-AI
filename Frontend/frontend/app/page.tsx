"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { CREATOR_STORAGE_KEY, USER_STORAGE_KEY } from "./lib/storage";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type CreatorCard = {
  id: number;
  userName: string;
  niche: string;
  instagram: string | null;
  youtube: string | null;
  tiktok: string | null;
};

type SignedInCreator = CreatorCard & {
  email: string;
};

type RecommendationSet = {
  short_form: string[];
  long_form: string[];
  deep_dive: string[];
  related_creators: string[];
};

function Section({
  title,
  items,
}: {
  title: string;
  items: string[];
}) {
  if (items.length === 0) return null;
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
      <p className="text-xs uppercase tracking-[0.4em] text-white/60">{title}</p>
      <ul className="mt-3 flex flex-col gap-1 text-sm text-white">
        {items.map((entry) => (
          <li key={entry} className="text-sm text-white/75">
            {entry}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function Home() {
  const router = useRouter();
  const [currentUser, setCurrentUser] = useState<SignedInCreator | null>(null);
  const [users, setUsers] = useState<CreatorCard[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [recommendations, setRecommendations] =
    useState<RecommendationSet | null>(null);
  const [connections, setConnections] = useState<CreatorCard[]>([]);
  const [isFetchingRecs, setIsFetchingRecs] = useState(false);
  const [isFetchingConnections, setIsFetchingConnections] = useState(false);
  const [activeTab, setActiveTab] = useState<"recommendations" | "connections">(
    "recommendations"
  );
  const [searchQuery, setSearchQuery] = useState("");
  const [sortKey, setSortKey] = useState<"userName" | "niche">("userName");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const storedUser = window.localStorage.getItem(USER_STORAGE_KEY);
    if (!storedUser) {
      router.push("/signin");
      return;
    }
    const parsed: SignedInCreator = JSON.parse(storedUser);
    setCurrentUser(parsed);
    const cachedCreators = window.localStorage.getItem(CREATOR_STORAGE_KEY);
    if (cachedCreators) {
      setUsers(JSON.parse(cachedCreators));
    }
  }, [router]);

  useEffect(() => {
    if (!currentUser) return;
    void refreshUsers();
    void loadRecommendations(currentUser);
    void loadConnections(currentUser);
  }, [currentUser]);

  const visibleUsers = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    const filtered = users.filter((creator) => {
      if (!query) return true;
      return (
        creator.userName.toLowerCase().includes(query) ||
        creator.niche.toLowerCase().includes(query) ||
        (creator.instagram?.toLowerCase().includes(query) ?? false) ||
        (creator.youtube?.toLowerCase().includes(query) ?? false) ||
        (creator.tiktok?.toLowerCase().includes(query) ?? false)
      );
    });

    const sorted = [...filtered].sort((a, b) => {
      const valueA = a[sortKey].toLowerCase();
      const valueB = b[sortKey].toLowerCase();
      const comparison = valueA.localeCompare(valueB);
      return sortDirection === "asc" ? comparison : -comparison;
    });

    return sorted;
  }, [users, searchQuery, sortDirection, sortKey]);

  async function refreshUsers() {
    try {
      const response = await fetch(`${API_BASE}/users/`);
      if (!response.ok) throw new Error("Unable to load creators");
      const data: CreatorCard[] = await response.json();
      setUsers(data);
      setMessage(null);
      if (typeof window !== "undefined") {
        window.localStorage.setItem(CREATOR_STORAGE_KEY, JSON.stringify(data));
      }
    } catch (error) {
      setMessage("Unable to load creators right now.");
    }
  }

  async function loadRecommendations(user: CreatorCard) {
    setActiveTab("recommendations");
    setIsFetchingRecs(true);
    setRecommendations(null);
    try {
      const url = new URL(`${API_BASE}/recommendations/${user.id}`);
      url.searchParams.set("niche", user.niche);
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch recs");
      const payload: RecommendationSet = await response.json();
      setRecommendations(payload);
    } catch (error) {
      setMessage("Could not load recommendations.");
    } finally {
      setIsFetchingRecs(false);
    }
  }

  async function loadConnections(user: CreatorCard) {
    setActiveTab("connections");
    setIsFetchingConnections(true);
    setConnections([]);
    try {
      const url = new URL(`${API_BASE}/connections`);
      url.searchParams.set("niche", user.niche);
      url.searchParams.set("excludeId", String(user.id));
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to load connections");
      const data: Creator[] = await response.json();
      setConnections(data);
    } catch (error) {
      setMessage("Could not load connection ideas.");
    } finally {
      setIsFetchingConnections(false);
    }
  }

  function handleConnect(target: CreatorCard) {
    setMessage(`Connection request sent to ${target.userName}.`);
  }

  if (!currentUser) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#030712] px-6 py-10 text-white">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-8 lg:grid lg:grid-cols-[1.2fr_0.8fr]">
        <section className="flex flex-col gap-6 rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 via-white/0 to-transparent p-8 shadow-[0_35px_80px_rgba(0,0,0,0.8)] backdrop-blur-xl">
          <div>
            <p className="text-xs uppercase tracking-[0.45em] text-white/60">
              Dashboard
            </p>
            <h2 className="mt-2 text-3xl font-semibold text-white">
              Visual recommendation canvas
            </h2>
            <p className="mt-2 text-sm text-white/60">
              You are signed in as {currentUser.userName} ({currentUser.niche}).
              Explore creators below or click a card to prime the recommendation
              flow.
            </p>
          </div>

          <div className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-black/40 p-4">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex flex-col">
                <label className="text-xs uppercase tracking-[0.4em] text-white/60">
                  Search creators
                </label>
                <input
                  value={searchQuery}
                  onChange={(event) => setSearchQuery(event.target.value)}
                  className="mt-1 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-white placeholder:text-white/40 focus:border-white focus:outline-none"
                  placeholder="Search by name, email, or niche"
                />
              </div>
              <div className="flex items-center gap-2 text-xs uppercase tracking-[0.35em] text-white/60">
                <button
                  className="rounded-full border border-white/20 px-3 py-1 transition hover:border-white"
                  onClick={() =>
                    setSortKey((prev) => (prev === "userName" ? "email" : "userName"))
                  }
                >
                  Sort: {sortKey}
                </button>
                <button
                  className="rounded-full border border-white/20 px-3 py-1 transition hover:border-white"
                  onClick={() =>
                    setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"))
                  }
                >
                  {sortDirection === "asc" ? "Ascending" : "Descending"}
                </button>
              </div>
            </div>
            <div className="flex flex-col gap-3">
              {visibleUsers.length === 0 ? (
                <p className="text-sm text-white/50">No creators yet.</p>
              ) : (
                visibleUsers.map((creator) => (
                  <button
                    key={creator.id}
                    className="flex w-full flex-col gap-1 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-left transition hover:border-white/60"
                    onClick={() => void loadRecommendations(creator)}
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-semibold text-white">
                        {creator.userName}
                      </p>
                      <span className="text-xs text-white/50">{creator.niche}</span>
                    </div>
                    <div className="text-xs text-white/60">
                      {creator.instagram && (
                        <span className="mr-3">IG: {creator.instagram}</span>
                      )}
                      {creator.youtube && (
                        <span className="mr-3">YT: {creator.youtube}</span>
                      )}
                      {creator.tiktok && (
                        <span className="mr-3">TikTok: {creator.tiktok}</span>
                      )}
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </section>

        <section className="flex flex-col gap-6 rounded-3xl border border-white/10 bg-gradient-to-br from-black/80 to-white/5 p-6 shadow-[0_35px_80px_rgba(0,0,0,0.8)]">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.4em] text-white/60">
                Active creator
              </p>
              <p className="text-xl font-semibold text-white">
                {currentUser.userName}
              </p>
              <p className="text-sm text-white/60">
                {currentUser.email} · {currentUser.niche}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                className={`rounded-2xl px-3 py-1 text-xs font-semibold transition ${
                  activeTab === "recommendations"
                    ? "bg-gradient-to-r from-fuchsia-500 to-pink-500 text-white"
                    : "border border-white/30 text-white/70"
                }`}
                onClick={() => setActiveTab("recommendations")}
              >
                Recommendations
              </button>
              <button
                className={`rounded-2xl px-3 py-1 text-xs font-semibold transition ${
                  activeTab === "connections"
                    ? "bg-gradient-to-r from-teal-500 to-cyan-500 text-white"
                    : "border border-white/30 text-white/70"
                }`}
                onClick={() => void loadConnections(currentUser)}
              >
                Connections
              </button>
            </div>
          </div>

          {activeTab === "recommendations" && (
            <div className="flex flex-col gap-4">
              {isFetchingRecs && (
                <p className="text-sm text-white/60">Loading recommendations…</p>
              )}
              {!isFetchingRecs && !recommendations && (
                <p className="text-sm text-white/60">
                  Select a creator to load niche ideas.
                </p>
              )}
              {!isFetchingRecs && recommendations && (
                <>
                  <Section title="Short-form sparks" items={recommendations.short_form} />
                  <Section title="Long-form series" items={recommendations.long_form} />
                  <Section title="Deep-dive themes" items={recommendations.deep_dive} />
                  <Section title="Related creators" items={recommendations.related_creators} />
                </>
              )}
            </div>
          )}

          {activeTab === "connections" && (
            <div className="flex flex-col gap-3">
              {isFetchingConnections ? (
                <p className="text-sm text-white/60">Loading connections…</p>
              ) : connections.length === 0 ? (
                <p className="text-sm text-white/60">
                  No nearby creators in this niche yet.
                </p>
              ) : (
                <div className="flex flex-col gap-3">
                  {connections.map((creator) => (
                    <div
                      key={creator.id}
                      className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3 transition hover:border-white/60"
                    >
                      <div>
                        <p className="text-sm font-semibold text-white">
                          {creator.userName}
                        </p>
                        <p className="text-xs text-white/60">
                          {creator.instagram && (
                            <span className="mr-3">IG: {creator.instagram}</span>
                          )}
                          {creator.youtube && (
                            <span className="mr-3">YT: {creator.youtube}</span>
                          )}
                          {creator.tiktok && (
                            <span className="mr-3">TikTok: {creator.tiktok}</span>
                          )}
                        </p>
                      </div>
                      <button
                        className="rounded-full border border-white/30 px-3 py-1 text-xs text-white/70 transition hover:border-white hover:text-white"
                        onClick={() => handleConnect(creator)}
                      >
                        Connect
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {message && (
            <p className="text-sm text-white/60">{message}</p>
          )}
        </section>
      </div>
    </div>
  );
}
