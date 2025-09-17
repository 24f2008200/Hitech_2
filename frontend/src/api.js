const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultHeaders = { "Content-Type": "application/json" };

  return fetch(url, {
    headers: { ...defaultHeaders, ...(options.headers || {}) },
    ...options,
  });
}
