import React, { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileDown, Send, RefreshCw } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const numberOrEmpty = (v) => (v === '' || v === null || v === undefined ? '' : Number(v))

const initialForm = {
  costo_total: '',
  plazo_meses: '',
  adicionales_pct: '',
  ampliaciones: '',
  penalidades: '',
  baja_competencia: 0,
  empresa_sancionada: 0,
  consorcio: 0,
  experiencia_entidad: 0,
  region_riesgo: 'MEDIA',
  tipo_proceso: 'Licitación'
}

export default function App() {
  const [tab, setTab] = useState('single')
  const [form, setForm] = useState(initialForm)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [file, setFile] = useState(null)
  const [batchRows, setBatchRows] = useState([])

  const canSend = useMemo(() => {
    const req = ['costo_total','plazo_meses','adicionales_pct','ampliaciones','penalidades']
    return req.every((k) => form[k] !== '' && !Number.isNaN(Number(form[k])))
  }, [form])

  const onChange = (k, v) => setForm((s) => ({ ...s, [k]: v }))

  const handlePredictSingle = async () => {
    try {
      setLoading(true)
      const payload = {
        ...form,
        costo_total: Number(form.costo_total),
        plazo_meses: Number(form.plazo_meses),
        adicionales_pct: Number(form.adicionales_pct),
        ampliaciones: Number(form.ampliaciones),
        penalidades: Number(form.penalidades),
        baja_competencia: Number(form.baja_competencia),
        empresa_sancionada: Number(form.empresa_sancionada),
        consorcio: Number(form.consorcio),
        experiencia_entidad: Number(form.experiencia_entidad),
      }
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) throw new Error('Error en respuesta del servidor')
      const data = await res.json()
      setResult(data)
    } catch (err) {
      alert(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async () => {
    if (!file) return alert('Selecciona un archivo CSV primero.')
    try {
      setLoading(true)
      const fd = new FormData()
      fd.append('file', file)
      const res = await fetch(`${API_BASE}/predict-csv`, { method: 'POST', body: fd })
      if (!res.ok) throw new Error('Error en respuesta del servidor')
      const data = await res.json()
      setBatchRows(data.rows || [])
    } catch (err) {
      alert(err.message)
    } finally {
      setLoading(false)
    }
  }

  const downloadCSV = () => {
    if (!batchRows.length) return
    const cols = Object.keys(batchRows[0])
    const csv = [cols.join(',')].concat(
      batchRows.map(r => cols.map(c => JSON.stringify(r[c] ?? '')).join(','))
    ).join('\n')
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'predicciones.csv'
    link.click()
  }

  return (
    <div className="min-h-screen p-6 md:p-10">
      <div className="max-w-6xl mx-auto">
        <motion.h1 initial={{opacity:0,y:-8}} animate={{opacity:1,y:0}} className="text-2xl md:text-3xl font-semibold">
          Predictor de Riesgo de Corrupción — Obras Públicas (Perú)
        </motion.h1>

        <div className="mt-4 flex gap-2">
          <button onClick={() => setTab('single')} className={`px-4 py-2 rounded-2xl ${tab==='single'?'bg-black text-white':'bg-gray-200'}`}>Predicción puntual</button>
          <button onClick={() => setTab('batch')} className={`px-4 py-2 rounded-2xl ${tab==='batch'?'bg-black text-white':'bg-gray-200'}`}>Predicción por archivo</button>
        </div>

        {tab === 'single' ? (
          <section className="mt-6 grid md:grid-cols-3 gap-4">
            <div className="md:col-span-2 bg-white rounded-2xl p-4 shadow">
              <h2 className="font-medium mb-3">Datos de la obra</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <NumberField label="Costo total (S/.)" value={form.costo_total} onChange={(v)=>onChange('costo_total', v)} />
                <NumberField label="Plazo (meses)" value={form.plazo_meses} onChange={(v)=>onChange('plazo_meses', v)} />
                <NumberField label="% Adicionales" step="0.01" value={form.adicionales_pct} onChange={(v)=>onChange('adicionales_pct', v)} />
                <NumberField label="N° Ampliaciones" value={form.ampliaciones} onChange={(v)=>onChange('ampliaciones', v)} />
                <NumberField label="N° Penalidades" value={form.penalidades} onChange={(v)=>onChange('penalidades', v)} />

                <Toggle label="Baja competencia" value={!!form.baja_competencia} onChange={(v)=>onChange('baja_competencia', v?1:0)} />
                <Toggle label="Empresa sancionada" value={!!form.empresa_sancionada} onChange={(v)=>onChange('empresa_sancionada', v?1:0)} />
                <Toggle label="Consorcio" value={!!form.consorcio} onChange={(v)=>onChange('consorcio', v?1:0)} />
                <Toggle label="Experiencia con la entidad" value={!!form.experiencia_entidad} onChange={(v)=>onChange('experiencia_entidad', v?1:0)} />

                <Select label="Región de riesgo" value={form.region_riesgo} onChange={(v)=>onChange('region_riesgo', v)} options={['ALTA','MEDIA','BAJA']} />
                <Select label="Tipo de proceso" value={form.tipo_proceso} onChange={(v)=>onChange('tipo_proceso', v)} options={['Licitación','Adjudicación Simplificada','Contratación Directa']} />
              </div>

              <div className="mt-4 flex gap-2">
                <button disabled={!canSend || loading} onClick={handlePredictSingle} className="px-4 py-2 rounded-xl bg-black text-white flex items-center gap-2 disabled:opacity-50">
                  <Send size={16}/> {loading? 'Prediciendo...' : 'Predecir'}
                </button>
                <button onClick={()=>{ setForm(initialForm); setResult(null); }} className="px-4 py-2 rounded-xl bg-gray-200 flex items-center gap-2">
                  <RefreshCw size={16}/> Limpiar
                </button>
              </div>
            </div>

            <div className="bg-white rounded-2xl p-4 shadow">
              <h2 className="font-medium mb-3">Resultado</h2>
              {result ? (
                <div className="space-y-2">
                  <div className="text-sm">Probabilidad de riesgo</div>
                  <div className="text-3xl font-semibold">{(result.prob_riesgo*100).toFixed(1)}%</div>
                  <div className={`inline-block px-3 py-1 rounded-full text-sm ${result.pred_riesgo===1?'bg-red-600 text-white':'bg-green-600 text-white'}`}>
                    {result.pred_riesgo===1? 'ALTO RIESGO' : 'BAJO RIESGO'}
                  </div>
                  {result.top_flags?.length ? (
                    <div className="text-sm mt-2">
                      <div className="font-medium mb-1">Señales (flags):</div>
                      <ul className="list-disc pl-5">
                        {result.top_flags.map((f,i)=>(<li key={i}>{f}</li>))}
                      </ul>
                    </div>
                  ) : null}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">Ingresa datos y presiona <b>Predecir</b>.</p>
              )}
            </div>
          </section>
        ) : (
          <section className="mt-6 bg-white rounded-2xl p-4 shadow">
            <h2 className="font-medium mb-3">Cargar archivo CSV</h2>
            <div className="flex flex-col md:flex-row items-start md:items-center gap-3">
              <input type="file" accept=".csv" onChange={(e)=>setFile(e.target.files?.[0] || null)} />
              <button onClick={handleUpload} disabled={!file || loading} className="px-4 py-2 rounded-xl bg-black text-white flex items-center gap-2 disabled:opacity-50">
                <Upload size={16}/> {loading? 'Procesando...' : 'Subir y predecir'}
              </button>
              <button onClick={downloadCSV} disabled={!batchRows.length} className="px-4 py-2 rounded-xl bg-gray-200 flex items-center gap-2 disabled:opacity-50">
                <FileDown size={16}/> Descargar predicciones
              </button>
            </div>

            <p className="text-sm text-gray-600 mt-2">El CSV debe incluir columnas mínimas: <code>costo_total, plazo_meses, adicionales_pct, ampliaciones, penalidades, baja_competencia, empresa_sancionada, consorcio, experiencia_entidad, region_riesgo, tipo_proceso</code>.</p>

            {batchRows.length ? (
              <div className="mt-4 overflow-auto">
                <table className="min-w-full text-sm">
                  <thead className="bg-gray-100">
                    <tr>
                      {Object.keys(batchRows[0]).map(h=>(<th key={h} className="text-left px-3 py-2 whitespace-nowrap">{h}</th>))}
                    </tr>
                  </thead>
                  <tbody>
                    {batchRows.map((r, idx)=>(
                      <tr key={idx} className="border-b">
                        {Object.keys(batchRows[0]).map(h=>(<td key={h} className="px-3 py-2 whitespace-nowrap">{String(r[h])}</td>))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : null}
          </section>
        )}

        <div className="mt-10 text-xs text-gray-500">
          API: <code>{API_BASE}</code> — Ajusta <code>VITE_API_BASE</code> en <code>.env</code> si usas otra URL.
        </div>
      </div>
    </div>
  )
}

function NumberField({ label, value, onChange, step }) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-sm text-gray-700">{label}</span>
      <input type="number" step={step || '1'} value={value}
        onChange={(e)=>onChange(e.target.value)}
        className="px-3 py-2 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-black"/>
    </label>
  )
}

function Toggle({ label, value, onChange }) {
  return (
    <label className="flex items-center gap-2 select-none">
      <input type="checkbox" checked={value} onChange={(e)=>onChange(e.target.checked)} />
      <span className="text-sm text-gray-700">{label}</span>
    </label>
  )
}

function Select({ label, value, onChange, options }) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-sm text-gray-700">{label}</span>
      <select value={value} onChange={(e)=>onChange(e.target.value)}
        className="px-3 py-2 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-black">
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  )
}
