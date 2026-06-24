import { useState } from 'react'
import BatchUpload from './components/BatchUpload.jsx'
import Header from './components/Header.jsx'
import ManualWhatIf from './components/ManualWhatIf.jsx'
import ModelMetricsPanel from './components/ModelMetricsPanel.jsx'
import ObraExplorer from './components/ObraExplorer.jsx'
import { API_BASE } from './api.js'

const TABS = [
  { id: 'explorar', label: 'Explorar obra' },
  { id: 'manual', label: 'Modo manual' },
  { id: 'csv', label: 'Carga CSV' },
]

export default function App() {
  const [tab, setTab] = useState('explorar')

  return (
    <div className="min-h-screen">
      <Header />
      <main className="mx-auto max-w-6xl space-y-4 p-6">
        <ModelMetricsPanel />

        <div className="flex gap-2">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`rounded-2xl px-4 py-2 text-sm font-medium ${
                tab === t.id ? 'bg-black text-white' : 'bg-gray-200 text-gray-700'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === 'explorar' && <ObraExplorer />}
        {tab === 'manual' && <ManualWhatIf />}
        {tab === 'csv' && <BatchUpload />}

        <div className="pt-6 text-xs text-gray-400">
          API: <code>{API_BASE}</code> — ajusta <code>VITE_API_BASE</code> en{' '}
          <code>apps/frontend/.env</code> si usas otra URL.
        </div>
      </main>
    </div>
  )
}
