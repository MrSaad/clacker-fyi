export async function fetchKeyboards() {
  const res = await fetch('/api/keyboards');
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function fetchTaxonomy() {
  const res = await fetch('/api/taxonomy');
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
