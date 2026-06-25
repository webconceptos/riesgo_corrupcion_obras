import { useEffect, useState } from 'react'
import { getModelMeta } from '../api.js'

const METRIC_LABELS = {
  macro_f1:           { label: 'Precisión global',              tecnico: 'Macro F1' },
  balanced_accuracy:  { label: 'Exactitud balanceada',          tecnico: 'Bal. Accuracy' },
  recall_extrema:     { label: 'Detección riesgo extremo',      tecnico: 'Recall Extrema' },
  brier_extrema:      { label: 'Calibración probabilística',    tecnico: 'Brier Extrema' },
  gap_train_val:      { label: 'Sobreajuste del modelo',        tecnico: 'Gap train-val' },
}

export default function ModelMetricsPanel() {
  const [meta, setMeta] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getModelMeta()
      .then(setMeta)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
        No se pudo cargar la metadata del modelo: {error}
      </div>
    )
  }

  if (!meta) {
    return <div className="rounded-2xl bg-white p-4 text-sm text-gray-400 shadow">Cargando métricas…</div>
  }

  const metrics = meta.metrics || {}
  const entries = Object.keys(METRIC_LABELS).filter((k) => metrics[k] !== undefined)

  return (
    <div className="rounded-2xl bg-white p-4 shadow">
      <h2 className="mb-3 text-sm font-medium text-gray-700">Desempeño del modelo</h2>
      <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
        {entries.map((k) => {
          const { label, tecnico } = METRIC_LABELS[k]
          return (
            <div key={k} className="rounded-xl bg-gray-50 p-3 text-center">
              <div className="text-lg font-semibold text-gray-900">
                {Number(metrics[k]).toFixed(4)}
              </div>
              <div className="text-xs font-medium text-gray-700">{label}</div>
              <div className="text-[10px] text-gray-400">({tecnico})</div>
            </div>
          )
        })}
      </div>
      <p className="mt-3 text-xs text-gray-400">
        Bosque Aleatorio — 3 niveles de riesgo
        <span className="text-gray-300">
          {' '}({meta.model_name} · {meta.n_features} variables · {meta.n_train} obras de entrenamiento · {meta.n_test} de validación)
        </span>
      </p>
    </div>
  )
}
