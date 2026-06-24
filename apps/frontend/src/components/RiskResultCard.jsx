const COLORS = {
  'Bajo Riesgo': '#0E7C66',
  'Med/Alt Riesgosa': '#C77B19',
  'Extrem. Riesgosa': '#B23A48',
}

export default function RiskResultCard({ result }) {
  if (!result) {
    return (
      <div className="rounded-2xl bg-white p-6 text-sm text-gray-400 shadow">
        Selecciona una obra (o ajusta el modo manual) y presiona predecir.
      </div>
    )
  }

  const { clase_predicha_label: label, probabilidades } = result
  const color = COLORS[label] || '#666'

  return (
    <div className="rounded-2xl bg-white p-5 shadow">
      <h2 className="mb-3 text-sm font-medium text-gray-700">Resultado de la clasificación</h2>
      <div
        className="rounded-xl border p-4"
        style={{ backgroundColor: `${color}1a`, borderColor: color }}
      >
        <div className="text-xs font-semibold uppercase tracking-wide" style={{ color }}>
          Nivel de riesgo predicho
        </div>
        <div className="text-2xl font-bold" style={{ color }}>
          {label}
        </div>
      </div>

      <div className="mt-4 space-y-2">
        {Object.entries(probabilidades).map(([clase, proba]) => (
          <div key={clase}>
            <div className="flex justify-between text-xs text-gray-600">
              <span>{clase}</span>
              <span>{(proba * 100).toFixed(0)}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-gray-100">
              <div
                className="h-2 rounded-full"
                style={{ width: `${proba * 100}%`, backgroundColor: COLORS[clase] || '#999' }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export { COLORS }
