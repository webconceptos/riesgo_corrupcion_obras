import { FileDown, Loader2, Upload } from 'lucide-react'
import Papa from 'papaparse'
import { useState } from 'react'
import { predictBatch } from '../api.js'
import { COLORS } from './RiskResultCard.jsx'

export default function BatchUpload() {
  const [file, setFile] = useState(null)
  const [filas, setFilas] = useState([])
  const [resultados, setResultados] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const onFile = (f) => {
    setFile(f)
    setResultados([])
    setError(null)
    Papa.parse(f, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (res) => setFilas(res.data),
      error: (err) => setError(err.message),
    })
  }

  const procesar = async () => {
    if (!filas.length) return
    setLoading(true)
    setError(null)
    try {
      const resp = await predictBatch(filas)
      setResultados(resp)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const descargar = () => {
    if (!resultados.length) return
    const filasConId = filas.map((fila, i) => ({
      ...fila,
      clase_predicha_label: resultados[i].clase_predicha_label,
      riesgoso: resultados[i].riesgoso,
      ...Object.fromEntries(
        Object.entries(resultados[i].probabilidades).map(([k, v]) => [`proba_${k}`, v]),
      ),
    }))
    const csv = Papa.unparse(filasConId)
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'predicciones.csv'
    link.click()
  }

  return (
    <div className="rounded-2xl bg-white p-5 shadow">
      <h2 className="mb-1 text-sm font-medium text-gray-700">Carga de CSV en lote</h2>
      <p className="mb-4 text-xs text-gray-400">
        El CSV debe traer columnas con los nombres de las variables del modelo (ver "Ver atributos
        de la obra" en la pestaña anterior). Columnas faltantes se imputan automáticamente.
      </p>

      <div className="flex flex-wrap items-center gap-3">
        <label className="flex cursor-pointer items-center gap-2 rounded-xl border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50">
          <Upload size={16} />
          {file ? file.name : 'Elegir CSV'}
          <input
            type="file"
            accept=".csv"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && onFile(e.target.files[0])}
          />
        </label>
        <button
          disabled={!filas.length || loading}
          onClick={procesar}
          className="flex items-center gap-2 rounded-xl bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : null}
          {loading ? 'Procesando…' : `Predecir ${filas.length} filas`}
        </button>
        <button
          disabled={!resultados.length}
          onClick={descargar}
          className="flex items-center gap-2 rounded-xl bg-gray-200 px-4 py-2 text-sm font-medium disabled:opacity-40"
        >
          <FileDown size={16} />
          Descargar predicciones
        </button>
      </div>

      {error && <p className="mt-3 text-xs text-red-600">{error}</p>}

      {resultados.length > 0 && (
        <div className="mt-4 max-h-80 overflow-auto rounded-xl border border-gray-100">
          <table className="min-w-full text-xs">
            <thead className="sticky top-0 bg-gray-50">
              <tr>
                <th className="px-3 py-2 text-left">#</th>
                <th className="px-3 py-2 text-left">Clase predicha</th>
                <th className="px-3 py-2 text-left">Riesgoso</th>
              </tr>
            </thead>
            <tbody>
              {resultados.map((r, i) => (
                <tr key={i} className="border-b border-gray-50">
                  <td className="px-3 py-2">{i + 1}</td>
                  <td className="px-3 py-2">
                    <span
                      className="rounded-full px-2 py-0.5 text-white"
                      style={{ backgroundColor: COLORS[r.clase_predicha_label] || '#666' }}
                    >
                      {r.clase_predicha_label}
                    </span>
                  </td>
                  <td className="px-3 py-2">{r.riesgoso ? 'Sí' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
