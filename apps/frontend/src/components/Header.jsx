import { ShieldCheck } from 'lucide-react'

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto max-w-6xl px-6 py-5">
        <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-gray-500">
          <ShieldCheck size={16} className="text-gray-400" />
          Contraloría General de la República · Revisión con Machine Learning
        </div>
        <h1 className="mt-1 text-2xl font-semibold text-gray-900 md:text-3xl">
          ¿Qué tan riesgosa es esta obra?
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Inferencia en vivo contra el modelo oficial (Random Forest, 3 clases, Macro F1 = 0.6469)
          servido por la API FastAPI del proyecto.
        </p>
      </div>
    </header>
  )
}
