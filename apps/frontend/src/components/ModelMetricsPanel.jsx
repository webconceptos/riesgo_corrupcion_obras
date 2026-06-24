import { useEffect, useState } from 'react'
import { getModelMeta } from '../api.js'

const METRIC_LABELS = {
  macro_f1: 'Macro F1',
  balanced_accuracy: 'Bal. Accuracy',
  recall_extrema: 'Recall Extrema',
  brier_extrema: 'Brier Extrema',
  gap_train_val: 'Gap train-val',
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
        {entries.map((k) => (
          <div key={k} className="rounded-xl bg-gray-50 p-3 text-center">
            <div className="text-lg font-semibold text-gray-900">
              {Number(metrics[k]).toFixed(4)}
            </div>
            <div className="text-xs text-gray-500">{METRIC_LABELS[k]}</div>
          </div>
        ))}
      </div>
      <p className="mt-3 text-xs text-gray-400">
        Modelo: {meta.model_name} · {meta.n_features} features · n_train={meta.n_train} · n_test=
        {meta.n_test}
      </p>
    </div>
  )
}
