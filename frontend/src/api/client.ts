export async function get<T>(url: string): Promise<T> {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`GET ${url}: ${r.status}`)
  return r.json()
}

export async function post<T>(url: string, body?: unknown): Promise<T> {
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  if (!r.ok) throw new Error(`POST ${url}: ${r.status}`)
  return r.json()
}

export async function upload(url: string, file: File): Promise<Record<string, string>> {
  const fd = new FormData()
  fd.append('file', file)
  const r = await fetch(url, { method: 'POST', body: fd })
  return r.json()
}
