const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function request(path, options) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    throw new Error(detail?.detail ? JSON.stringify(detail.detail) : `Error ${res.status} en ${path}`)
  }
  return res.json()
}

export const getModelMeta = () => request('/model_meta')

export const getObras = () => request('/obras')

export const getObra = (identificadorObra) => request(`/obras/${encodeURIComponent(identificadorObra)}`)

export const predictProba = (fila) =>
  request('/predict_proba', { method: 'POST', body: JSON.stringify({ filas: [fila] }) }).then(
    (r) => r.resultados[0],
  )

export const explain = (fila) =>
  request('/explain', { method: 'POST', body: JSON.stringify({ fila }) })

export const predictBatch = (filas) =>
  request('/predict_batch', { method: 'POST', body: JSON.stringify(filas) }).then((r) => r.resultados)

export { API_BASE }
