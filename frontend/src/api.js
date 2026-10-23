// Empty by default: in production, frontend and API share one Vercel domain,
// so requests to /api/* are same-origin. Local dev points at a separate
// uvicorn process via VITE_API_URL.
const API_URL = import.meta.env.VITE_API_URL || "";

export async function evaluateIdea(idea) {
  const res = await fetch(`${API_URL}/api/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idea, provider: "anthropic" }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Evaluation failed. Please try again.");
  }

  return data;
}
