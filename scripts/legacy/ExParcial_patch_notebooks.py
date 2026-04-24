import nbformat
from nbformat.v4 import new_notebook, new_code_cell
import os

# ================================================================
#  ExParcial - Regenerador de Notebooks (Patch Rutas Absolutas)
# ================================================================

PATCH_CELL = new_code_cell("""
# ======================================================
# Patch rutas absolutas (compatible con papermill + jobs)
# ======================================================
import os

# Ruta absoluta a la raíz del proyecto
ROOT = os.path.abspath(os.path.join(os.getcwd(), ".."))

def path(*args):
    \"\"\"Devuelve rutas absolutas a partir de la raíz del proyecto.\"\"\"
    return os.path.join(ROOT, *args)

print("[Patch] Rutas absolutas activadas. ROOT =", ROOT)
""")

# Notebooks a regenerar
NOTEBOOKS = [
    "notebooks/ExParcial_IngAtributos.ipynb",
    "notebooks/ExParcial_Experimentos.ipynb",
    "notebooks/ExParcial_ValidacionResultados.ipynb",
    "notebooks/ExParcial_AblationStudy.ipynb",
    "notebooks/ExParcial_XAI.ipynb",
    "notebooks/ExParcial_EDA_Profesional.ipynb",
]

def patch_notebook(path_in):
    print(f"➡ Procesando notebook: {path_in}")

    nb = nbformat.read(path_in, as_version=4)

    # Si la primera celda YA contiene nuestro patch, no lo duplicamos
    if nb.cells and "Patch rutas absolutas" in nb.cells[0].get("source", ""):
        print("   ✓ Ya tenía el patch. Saltando.")
        return

    # Insertamos la celda al inicio
    nb.cells.insert(0, PATCH_CELL)

    # Guardamos sobre el mismo archivo
    nbformat.write(nb, path_in)
    print("   ✓ Patch insertado y guardado.")

def main():
    print("===============================================")
    print("   Regenerador de Notebooks - ExParcial")
    print("===============================================")

    for nb in NOTEBOOKS:
        if os.path.exists(nb):
            patch_notebook(nb)
        else:
            print(f"   ⚠ No encontrado: {nb}")

    print("\n✔ PATCH COMPLETADO.\nTodos los notebooks han sido regenerados correctamente.")

if __name__ == "__main__":
    main()
