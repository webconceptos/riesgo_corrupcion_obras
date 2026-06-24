import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export default function ShapChart({ contribuciones }) {
  if (!contribuciones || contribuciones.length === 0) {
    return null
  }

  const data = [...contribuciones]
    .sort((a, b) => Math.abs(b.shap_value) - Math.abs(a.shap_value))
    .slice(0, 12)
    .reverse()
    .map((c) => ({ ...c, shap_value: Number(c.shap_value.toFixed(4)) }))

  return (
    <div className="rounded-2xl bg-white p-5 shadow">
      <h2 className="mb-1 text-sm font-medium text-gray-700">¿Por qué? (TreeSHAP)</h2>
      <p className="mb-3 text-xs text-gray-400">
        Rojo: empuja hacia la clase predicha · Azul: la aleja.
      </p>
      <ResponsiveContainer width="100%" height={Math.max(280, data.length * 28)}>
        <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" tick={{ fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="feature"
            width={210}
            tick={{ fontSize: 11 }}
            interval={0}
          />
          <Tooltip formatter={(value) => Number(value).toFixed(4)} />
          <Bar dataKey="shap_value" radius={[0, 4, 4, 0]}>
            {data.map((entry) => (
              <Cell key={entry.feature} fill={entry.shap_value >= 0 ? '#B23A48' : '#4F81BD'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
