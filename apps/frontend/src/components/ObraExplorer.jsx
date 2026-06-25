import { Loader2, Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { explain, getObra, getObras, predictProba } from '../api.js'
import RiskResultCard from './RiskResultCard.jsx'
import ShapChart from './ShapChart.jsx'

// ── Grupos de atributos para el auditor ──────────────────────────────────────
const GRUPOS = [
  {
    titulo: 'Identificación de la obra',
    campos: [
      ['obra_ctx_sector',               'Sector',                  null],
      ['obra_ctx_nivel_gobierno',       'Nivel de gobierno',       null],
      ['obra_ctx_departamento',         'Departamento',            null],
      ['obra_ctx_metodo_contratacion',  'Método de contratación',  null],
    ],
  },
  {
    titulo: 'Montos y ofertas',
    nota: 'Los ratios fueron calculados sobre los datos fuente (CGR) durante el preprocesamiento.',
    campos: [
      ['obra_monto_contractual_sum',        'Monto contractual total (S/)',       null],
      ['obra_ratio_contractual_referencial','Ratio monto contrato / referencial',  '(pre-calculado sobre datos crudos CGR)'],
      ['obra_ratio_oferta_contrato',        'Ratio oferta promedio / contrato',    '(pre-calculado)'],
      ['obra_ratio_ofertas_iguales',        'Proporción de ofertas idénticas',     null],
    ],
  },
  {
    titulo: 'Postores y participantes',
    campos: [
      ['obra_n_participantes_mean',      'Nº promedio de participantes por proceso', null],
      ['obra_n_participantes_max',       'Nº máximo de participantes',               null],
      ['obra_pct_postores_igual_ganador','% postores con oferta igual al ganador',   null],
      ['obra_n_postores_igual_ganador',  'Nº postores con oferta igual al ganador',  null],
      ['obra_n_contratos_postor_unico',  'Nº contratos con postor único',            null],
    ],
  },
  {
    titulo: 'Comité de selección',
    campos: [
      ['obra_ratio_repeticion_comite', 'Repetición de miembros en el comité', null],
      ['obra_n_convocatorias_comite',  'Nº de convocatorias del comité',      null],
      ['obra_n_procesos_comite',       'Nº de procesos del comité',           null],
      ['obra_comite_no_estandar',      'Comité no estándar (0=No / 1=Sí)',    null],
    ],
  },
  {
    titulo: 'Control CGR',
    campos: [
      ['TOTAL_CONTROL_PREVIO',      'Controles previos registrados',       null],
      ['TOTAL_CONTROL_SIMULTANEO',  'Controles simultáneos registrados',   null],
      ['TOTAL_CONTROL_POSTERIOR',   'Controles posteriores registrados',   null],
    ],
  },
]

function fmtValor(v) {
  if (v === null || v === undefined) return '—'
  if (typeof v === 'number') {
    return Number.isInteger(v) ? String(v) : Number(v).toLocaleString('es-PE', { maximumFractionDigits: 4 })
  }
  return String(v)
}

function AtributosObra({ features }) {
  const [expandido, setExpandido] = useState(false)
  return (
    <details className="rounded-2xl bg-white p-5 text-xs text-gray-600 shadow">
      <summary className="cursor-pointer text-sm font-medium text-gray-700">
        Ver atributos de la obra
      </summary>
      <div className="mt-3 space-y-4">
        {GRUPOS.map((grupo) => {
          // Filtrar solo campos con valor no nulo
          const camposVisibles = grupo.campos.filter(([key]) =>
            features[key] !== null && features[key] !== undefined
          )
          if (camposVisibles.length === 0) return null
          return (
            <div key={grupo.titulo}>
              <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-400">
                {grupo.titulo}
              </div>
              {grupo.nota && (
                <p className="mb-1 text-xs text-gray-400 italic">{grupo.nota}</p>
              )}
              <div className="divide-y divide-gray-50 rounded-lg border border-gray-100">
                {camposVisibles.map(([key, label, hint]) => (
                  <div key={key} className="flex justify-between gap-4 px-3 py-1.5">
                    <span className="text-gray-500">
                      {label}
                      {hint && <span className="ml-1 text-gray-300">{hint}</span>}
                    </span>
                    <span className="font-medium text-gray-800 text-right">{fmtValor(features[key])}</span>
                  </div>
                ))}
              </div>
            </div>
          )
        })}

        {/* Vista técnica colapsable */}
        <details className="mt-2" onToggle={(e) => setExpandido(e.target.open)}>
          <summary className="cursor-pointer text-xs text-gray-400 hover:text-gray-600">
            {expandido ? '▲' : '▶'} Ver las 61 variables técnicas del modelo
          </summary>
          <div className="mt-2 grid max-h-52 grid-cols-2 gap-x-4 gap-y-0.5 overflow-auto rounded border border-gray-100 p-2">
            {Object.entries(features).map(([k, v]) => (
              <div key={k} className="flex justify-between gap-2 border-b border-gray-50 py-0.5">
                <span className="truncate text-gray-400">{k}</span>
                <span className="font-mono text-gray-600">{fmtValor(v)}</span>
              </div>
            ))}
          </div>
        </details>
      </div>
    </details>
  )
}

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

        {detalle && <AtributosObra features={detalle.features} />}
      </div>

      <div className="space-y-4">
        <RiskResultCard result={resultado} />
        <ShapChart contribuciones={contribuciones} />
      </div>
    </div>
  )
}
