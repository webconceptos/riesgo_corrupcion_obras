import { Bar, BarChart, CartesianGrid, Cell, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

// Traducción de nombres técnicos a lenguaje auditor
const NOMBRES = {
  obra_n_participantes_mean:               'Nº promedio de participantes por proceso',
  obra_n_participantes_max:                'Nº máximo de participantes',
  obra_monto_contractual_sum:              'Monto contractual total (S/)',
  obra_ratio_contrato_participacion:       'Ratio monto contrato / nº participantes',
  obra_ratio_contractual_referencial:      'Ratio monto contrato vs. referencial',
  obra_ratio_repeticion_comite:            'Repetición de miembros en el comité',
  obra_n_convocatorias_comite:             'Nº de convocatorias del comité',
  obra_n_procesos_comite:                  'Nº de procesos del comité',
  obra_pct_postores_igual_ganador:         '% postores con oferta igual al ganador',
  obra_n_postores_igual_ganador:           'Nº postores con oferta igual al ganador',
  obra_ratio_oferta_contrato:              'Ratio oferta promedio vs. contrato',
  TOTAL_CONTROL_SIMULTANEO:               'Controles simultáneos registrados',
  TOTAL_CONTROL_PREVIO:                   'Controles previos registrados',
  TOTAL_CONTROL_POSTERIOR:                'Controles posteriores registrados',
  obra_ctx_metodo_contratacion_Convenio:   'Método de contratación: Convenio',
  'obra_ctx_nivel_gobierno_GOBIERNO_REGIONAL': 'Nivel de gobierno: Regional',
  'obra_ctx_nivel_gobierno_GOBIERNO_LOCAL':    'Nivel de gobierno: Local',
  'obra_ctx_nivel_gobierno_GOBIERNO_NACIONAL': 'Nivel de gobierno: Nacional',
  obra_ctx_sector_TRANSPORTE:             'Sector: Transporte',
  obra_ctx_sector_OTROS:                  'Sector: Otros',
  obra_ctx_sector_SALUD:                  'Sector: Salud',
  obra_ctx_sector_EDUCACION:              'Sector: Educación',
}

function traducir(nombre) {
  if (NOMBRES[nombre]) return NOMBRES[nombre]
  // Fallback: limpiar prefijos técnicos y underscores
  return nombre
    .replace(/^obra_(ctx_)?/, '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (l) => l.toUpperCase())
}

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const { feature, shap_value } = payload[0].payload
  const sube = shap_value >= 0
  return (
    <div className="rounded-lg border bg-white px-3 py-2 shadow-lg text-xs max-w-xs">
      <div className="font-semibold text-gray-800 mb-1">{traducir(feature)}</div>
      <div style={{ color: sube ? '#B23A48' : '#4F81BD' }} className="font-medium">
        {sube ? '▲ Aumenta' : '▼ Reduce'} el riesgo extremo
      </div>
      <div className="text-gray-500 mt-0.5">Contribución SHAP: {shap_value >= 0 ? '+' : ''}{shap_value.toFixed(4)}</div>
    </div>
  )
}

export default function ShapChart({ contribuciones }) {
  if (!contribuciones || contribuciones.length === 0) return null

  const data = [...contribuciones]
    .sort((a, b) => Math.abs(b.shap_value) - Math.abs(a.shap_value))
    .slice(0, 8)
    .reverse()
    .map((c) => ({ ...c, shap_value: Number(c.shap_value.toFixed(4)) }))

  return (
    <div className="rounded-2xl bg-white p-5 shadow">
      <h2 className="text-sm font-semibold text-gray-800 mb-0.5">
        Factores que explican esta predicción
      </h2>
      <p className="text-xs text-gray-400 mb-1">
        Análisis TreeSHAP — top 8 factores por peso explicativo
      </p>
      <div className="flex gap-4 text-xs mb-3">
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-sm" style={{ background: '#B23A48' }} />
          Aumenta el riesgo
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-sm" style={{ background: '#4F81BD' }} />
          Reduce el riesgo
        </span>
      </div>

      <ResponsiveContainer width="100%" height={Math.max(240, data.length * 36)}>
        <BarChart data={data} layout="vertical" margin={{ left: 8, right: 40, top: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f0f0f0" />
          <XAxis
            type="number"
            tick={{ fontSize: 10, fill: '#9ca3af' }}
            tickFormatter={(v) => v.toFixed(3)}
            label={{ value: '← Reduce   Aumenta →', position: 'insideBottom', offset: -2, fontSize: 10, fill: '#9ca3af' }}
          />
          <YAxis
            type="category"
            dataKey="feature"
            width={230}
            tick={{ fontSize: 11, fill: '#374151' }}
            tickFormatter={traducir}
            interval={0}
          />
          <ReferenceLine x={0} stroke="#d1d5db" strokeWidth={1.5} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="shap_value" radius={[0, 4, 4, 0]} maxBarSize={22}>
            {data.map((entry) => (
              <Cell key={entry.feature} fill={entry.shap_value >= 0 ? '#B23A48' : '#4F81BD'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
