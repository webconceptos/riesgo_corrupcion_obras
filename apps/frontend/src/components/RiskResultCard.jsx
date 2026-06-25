const COLORS = {
  'Bajo Riesgo': '#0E7C66',
  'Med/Alt Riesgosa': '#C77B19',
  'Extrem. Riesgosa': '#B23A48',
}

const ETIQUETAS = {
  'Bajo Riesgo': 'Bajo riesgo',
  'Med/Alt Riesgosa': 'Riesgo medio-alto',
  'Extrem. Riesgosa': 'Riesgo extremo',
}

export default function RiskResultCard({ result }) {
  if (!result) {
    return (
      <div className="rounded-2xl bg-white p-6 text-sm text-gray-400 shadow">
        Selecciona una obra (o ajusta el modo manual) y presiona predecir.
      </div>
    )
  }

  const { clase_predicha_label: label, probabilidades, riesgoso } = result
  const color = COLORS[label] || '#666'

  // Probabilidad acumulada de ser riesgosa (Med/Alt + Extrema)
  const probRiesgosa =
    (probabilidades['Med/Alt Riesgosa'] || 0) + (probabilidades['Extrem. Riesgosa'] || 0)

  return (
    <div className="rounded-2xl bg-white p-5 shadow space-y-4">

      {/* Veredicto principal */}
      <div>
        <div className="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">
          ¿Requiere priorización de control?
        </div>
        <div
          className="flex items-center gap-3 rounded-xl border px-4 py-3"
          style={{ backgroundColor: `${color}18`, borderColor: color }}
        >
          <span className="text-3xl">{riesgoso ? '⚠️' : '✅'}</span>
          <div>
            <div className="text-xl font-bold leading-tight" style={{ color }}>
              {riesgoso ? 'SÍ — Obra riesgosa' : 'NO — Sin riesgo significativo'}
            </div>
            <div className="text-xs mt-0.5" style={{ color }}>
              Clasificada como: {ETIQUETAS[label] || label}
            </div>
          </div>
        </div>
      </div>

      {/* Probabilidad de riesgo total */}
      {riesgoso && (
        <div className="rounded-lg bg-red-50 border border-red-100 px-4 py-2 text-sm text-red-700">
          <span className="font-semibold">{(probRiesgosa * 100).toFixed(0)}%</span> de probabilidad
          acumulada de riesgo medio-alto o extremo
        </div>
      )}

      {/* Barras de probabilidad por clase */}
      <div>
        <div className="text-xs font-medium text-gray-500 mb-2">Probabilidad por nivel de riesgo</div>
        <div className="space-y-2">
          {Object.entries(probabilidades).map(([clase, proba]) => (
            <div key={clase}>
              <div className="flex justify-between text-xs text-gray-600 mb-0.5">
                <span>{ETIQUETAS[clase] || clase}</span>
                <span className="font-medium">{(proba * 100).toFixed(0)}%</span>
              </div>
              <div className="h-2 w-full rounded-full bg-gray-100">
                <div
                  className="h-2 rounded-full transition-all duration-500"
                  style={{ width: `${proba * 100}%`, backgroundColor: COLORS[clase] || '#999' }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export { COLORS }
