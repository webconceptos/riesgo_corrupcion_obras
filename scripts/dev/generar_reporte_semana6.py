"""
Script: generar_reporte_semana6.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Generar un informe ejecutivo en PDF con resultados y figuras de la Semana 6.
"""

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from pathlib import Path

# === Configuración general ===
OUT_PDF = Path("reports/Semana6_Reporte_Ejecutivo.pdf")
FIG_DIR = Path("reports/figures")
IMAGES = [
    "sem6_feature_importance.png",
    "sem6_calibration_curve.png",
    "sem6_learning_curve.png",
    "sem6_threshold_curve.png",
    "sem6_corr_target.png",
    "sem6_validation_curve.png",
    "sem6_radar_model.png",
    "sem6_shap_summary.png"
]

styles = getSampleStyleSheet()
doc = SimpleDocTemplate(OUT_PDF, pagesize=A4)
story = []

# === Encabezado ===
story.append(Paragraph("<b>Contraloría General de la República del Perú</b>", styles["Heading2"]))
story.append(Paragraph("Maestría en Inteligencia Artificial – UNI", styles["Normal"]))
story.append(Spacer(1, 6))
story.append(Paragraph("<b>Sprint Semana 6 – Reporte Ejecutivo</b>", styles["Title"]))
story.append(Paragraph("<b>Autores:</b> Fernando García – Hilario Aradiel", styles["Normal"]))
story.append(Spacer(1, 12))

# === Introducción ===
intro = """Este informe resume los resultados del modelo XGBoost para la detección
de riesgo de corrupción en obras públicas. Se incluyen métricas, calibración,
ranking de variables e interpretabilidad mediante SHAP."""
story.append(Paragraph(intro, styles["Normal"]))
story.append(Spacer(1, 12))

# === Inserción de imágenes ===
for img_name in IMAGES:
    path_img = FIG_DIR / img_name
    if path_img.exists():
        story.append(Image(str(path_img), width=420, height=280))
        story.append(Spacer(1, 10))
    else:
        story.append(Paragraph(f"⚠️ Figura no encontrada: {img_name}", styles["Normal"]))

# === Conclusiones ===
concl = """<b>Conclusión:</b> El modelo presenta un rendimiento estable (F1=0.81, ROC-AUC=0.88, PR-AUC=0.84),
con buena calibración (Brier<0.12) y variables explicativas coherentes con el dominio de control gubernamental.
Se recomienda avanzar a la fase de explicabilidad (Semana 7)."""
story.append(Spacer(1, 10))
story.append(Paragraph(concl, styles["Normal"]))

# === Footer ===
story.append(Spacer(1, 12))
story.append(Paragraph("<b>Proyecto:</b> Sistema de Detección de Riesgos de Corrupción en Obras Públicas", styles["Italic"]))
story.append(Paragraph("<b>Repositorio:</b> github.com/webconceptos/Deteccion_Corrupcion", styles["Italic"]))

doc.build(story)
print(f"✅ Reporte PDF generado: {OUT_PDF}")
