export async function fetchKeyboards() {
  const res = await fetch('/api/keyboards');
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
