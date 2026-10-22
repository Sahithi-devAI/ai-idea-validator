const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function evaluateIdea(idea) {
  const res = await fetch(`${API_URL}/evaluate`, {
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
