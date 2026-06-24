import { Loader2, Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { explain, getObra, getObras, predictProba } from '../api.js'
import RiskResultCard from './RiskResultCard.jsx'
import ShapChart from './ShapChart.jsx'

export default function ObraExplorer() {
  const [obras, setObras] = useState([])
  const [filtro, setFiltro] = useState('')
  const [seleccionada, setSeleccionada] = useState(null)
  const [detalle, setDetalle] = useState(null)
  const [resultado, setResultado] = useState(null)
  const [contribuciones, setContribuciones] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    getObras()
      .then((r) => setObras(r.obras))
      .catch((err) => setError(err.message))
  }, [])

  const obrasFiltradas = useMemo(() => {
    const q = filtro.trim().toLowerCase()
    if (!q) return obras.slice(0, 50)
    return obras
      .filter((o) =>
        [o.identificador_obra, o.sector, o.nivel_gobierno, o.departamento]
          .filter(Boolean)
          .some((v) => v.toLowerCase().includes(q)),
      )
      .slice(0, 50)
  }, [obras, filtro])

  const seleccionarObra = async (identificadorObra) => {
    setSeleccionada(identificadorObra)
    setResultado(null)
    setContribuciones(null)
    setError(null)
    try {
      const d = await getObra(identificadorObra)
      setDetalle(d)
    } catch (err) {
      setError(err.message)
    }
  }

  const predecir = async () => {
    if (!detalle) return
    setLoading(true)
    setError(null)
    try {
      const [pred, exp] = await Promise.all([
        predictProba(detalle.features),
        explain(detalle.features),
      ])
      setResultado(pred)
      setContribuciones(exp.contribuciones)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="space-y-4">
        <div className="rounded-2xl bg-white p-5 shadow">
          <h2 className="mb-3 text-sm font-medium text-gray-700">
            Seleccionar una obra real ({obras.length} disponibles)
          </h2>
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar por código, sector, departamento…"
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="w-full rounded-xl border border-gray-300 py-2 pl-9 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
          <div className="mt-3 max-h-72 overflow-auto rounded-xl border border-gray-100">
            {obrasFiltradas.map((o) => (
              <button
                key={o.identificador_obra}
                onClick={() => seleccionarObra(o.identificador_obra)}
                className={`block w-full border-b border-gray-50 px-3 py-2 text-left text-xs last:border-0 hover:bg-gray-50 ${
                  seleccionada === o.identificador_obra ? 'bg-gray-100' : ''
                }`}
              >
                <div className="font-medium text-gray-800">{o.identificador_obra}</div>
                <div className="text-gray-400">
                  {[o.sector, o.nivel_gobierno, o.departamento].filter(Boolean).join(' · ')}
                </div>
              </button>
            ))}
            {obrasFiltradas.length === 0 && (
              <div className="px-3 py-4 text-center text-xs text-gray-400">Sin resultados.</div>
            )}
          </div>
          <button
            disabled={!detalle || loading}
            onClick={predecir}
            className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : null}
            {loading ? 'Prediciendo…' : 'Predecir y explicar'}
          </button>
          {error && <p className="mt-2 text-xs text-red-600">{error}</p>}
        </div>

        {detalle && (
          <details className="rounded-2xl bg-white p-5 text-xs text-gray-600 shadow">
            <summary className="cursor-pointer text-sm font-medium text-gray-700">
              Ver atributos de la obra ({Object.keys(detalle.features).length})
            </summary>
            <div className="mt-3 grid max-h-60 grid-cols-2 gap-x-4 gap-y-1 overflow-auto">
              {Object.entries(detalle.features).map(([k, v]) => (
                <div key={k} className="flex justify-between gap-2 border-b border-gray-50 py-1">
                  <span className="truncate text-gray-400">{k}</span>
                  <span className="font-mono text-gray-700">{String(v ?? '—')}</span>
                </div>
              ))}
            </div>
          </details>
        )}
      </div>

      <div className="space-y-4">
        <RiskResultCard result={resultado} />
        <ShapChart contribuciones={contribuciones} />
      </div>
    </div>
  )
}
