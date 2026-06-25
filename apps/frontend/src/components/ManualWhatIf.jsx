import { Loader2 } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { explain, getModelMeta, predictProba } from '../api.js'
import RiskResultCard from './RiskResultCard.jsx'
import ShapChart from './ShapChart.jsx'

const KEYWORDS = [
  'repeticion',
  'procesos',
  'convocatorias',
  'participantes',
  'control',
  'monto_contractual',
  'regional',
  'convenio',
]

const NOMBRES = {
  TOTAL_CONTROL_PREVIO:                        'Controles previos CGR',
  TOTAL_CONTROL_SIMULTANEO:                    'Controles simultáneos CGR',
  TOTAL_CONTROL_POSTERIOR:                     'Controles posteriores CGR',
  obra_monto_contractual_sum:                  'Monto contractual total (S/)',
  obra_n_participantes_mean:                   'Nº promedio de participantes',
  obra_n_participantes_max:                    'Nº máximo de participantes',
  obra_n_convocatorias_comite:                 'Nº de convocatorias del comité',
  obra_n_procesos_comite:                      'Nº de procesos del comité',
  obra_ratio_repeticion_comite:                'Repetición de miembros en el comité',
  'obra_ctx_nivel_gobierno_GOBIERNO_REGIONAL': 'Nivel gobierno: Regional',
  obra_ctx_metodo_contratacion_Convenio:       'Método de contratación: Convenio',
}

function traducir(nombre) {
  return NOMBRES[nombre] ?? nombre.replace(/^obra_(ctx_)?/, '').replace(/_/g, ' ')
}

export default function ManualWhatIf() {
  const [meta, setMeta] = useState(null)
  const [valores, setValores] = useState({})
  const [resultado, setResultado] = useState(null)
  const [contribuciones, setContribuciones] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    getModelMeta()
      .then((m) => {
        setMeta(m)
        const stats = m.feature_stats || {}
        const inicial = {}
        for (const [feature, s] of Object.entries(stats)) {
          inicial[feature] = s.median
        }
        setValores(inicial)
      })
      .catch((err) => setError(err.message))
  }, [])

  const sliders = useMemo(() => {
    if (!meta) return []
    const stats = meta.feature_stats || {}
    const numericFeatures = (meta.features || []).filter((f) => stats[f] !== undefined)
    const porKeyword = numericFeatures.filter((f) =>
      KEYWORDS.some((k) => f.toLowerCase().includes(k)),
    )
    const elegidas = (porKeyword.length ? porKeyword : numericFeatures).slice(0, 8)
    return elegidas.map((f) => ({ feature: f, ...stats[f] }))
  }, [meta])

  const ajustar = (feature, value) => {
    setValores((prev) => ({ ...prev, [feature]: Number(value) }))
  }

  const predecir = async () => {
    setLoading(true)
    setError(null)
    try {
      const [pred, exp] = await Promise.all([predictProba(valores), explain(valores)])
      setResultado(pred)
      setContribuciones(exp.contribuciones)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (!meta) {
    return <div className="rounded-2xl bg-white p-5 text-sm text-gray-400 shadow">Cargando…</div>
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-2xl bg-white p-5 shadow">
        <h2 className="mb-1 text-sm font-medium text-gray-700">Modo manual — qué pasaría si</h2>
        <p className="mb-4 text-xs text-gray-400">
          Ajusta los principales drivers; el resto de las {Object.keys(valores).length} variables
          numéricas toma la mediana del dataset.
        </p>
        <div className="space-y-4">
          {sliders.map(({ feature, min, max, median }) => (
            <div key={feature}>
              <div className="flex justify-between text-xs text-gray-600">
                <span className="truncate font-medium" title={feature}>
                  {traducir(feature)}
                </span>
                <span className="font-mono text-gray-400">{Number(valores[feature] ?? median).toFixed(2)}</span>
              </div>
              <input
                type="range"
                min={min}
                max={max}
                step={(max - min) / 100 || 1}
                value={valores[feature] ?? median}
                onChange={(e) => ajustar(feature, e.target.value)}
                className="w-full accent-black"
              />
            </div>
          ))}
        </div>
        <button
          disabled={loading}
          onClick={predecir}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : null}
          {loading ? 'Prediciendo…' : 'Predecir y explicar'}
        </button>
        {error && <p className="mt-2 text-xs text-red-600">{error}</p>}
      </div>

      <div className="space-y-4">
        <RiskResultCard result={resultado} />
        <ShapChart contribuciones={contribuciones} />
      </div>
    </div>
  )
}
