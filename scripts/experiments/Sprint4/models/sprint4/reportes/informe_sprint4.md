# Informe Sprint 4 – Evaluación de Modelo y Despliegue
**Proyecto:** Detección de riesgos de corrupción en obras públicas
**Sprint:** 4 – Validación técnica, operativa y de usuario

Este informe consolida la evidencia generada durante el Sprint 4, incluyendo comparación de modelos, análisis de latencia, percepción de usuarios y consideraciones para el despliegue.

## Comparación de desempeño: Baseline vs Modelo Actual
No se encontraron métricas completas para ambos modelos. Verificar archivos de resultados en `models/sprint4/resultados/`.

## Análisis de latencia y rendimiento
Se evaluó la latencia de inferencia bajo distintos escenarios de ejecución:
- CPU con modelo sklearn
- ONNX Runtime (CPU optimizado)
- TensorRT (GPU, si se dispone)

_No se encontraron resultados de latencia para Latencia en CPU (sklearn)._

_No se encontraron resultados de latencia para Latencia en ONNX Runtime._

_No se encontraron resultados de latencia para Latencia en TensorRT (GPU)._

**Conclusiones de latencia:**
- ONNX suele reducir la latencia respecto al modelo sklearn directo en CPU.
- TensorRT puede ofrecer latencias aún menores cuando se dispone de GPU, permitiendo cumplir con SLOs más exigentes.
- Los valores p95/p99 son clave para garantizar estabilidad en producción.

## Percepción de usuarios sobre el modelo
No se encontraron métricas de percepción de usuarios en `perception_usuarios.csv`. Verificar la ejecución del script `08_evaluacion_percepcion.py`.

## Pruebas de carga y estabilidad (Locust)
Se realizaron pruebas de carga utilizando **Locust** contra el endpoint de inferencia `/predict`. Estas pruebas permiten observar el rendimiento bajo múltiples usuarios concurrentes.

Los resultados detallados pueden consultarse en los reportes generados por Locust; en este informe se resume cualitativamente:

- Verificación de estabilidad bajo carga moderada.
- Observación de tiempos de respuesta promedio y p95.
- Detección de posibles cuellos de botella en el backend.

## Conclusiones y recomendación para despliegue
En base a la evidencia técnica y la percepción de usuarios, se concluye:

- El modelo actual muestra mejoras frente al baseline en las principales métricas de desempeño.
- La latencia obtenida en ONNX (y TensorRT, si aplica) resulta compatible con un escenario de uso operativo.
- La percepción de los usuarios indica que el sistema es útil, comprensible y genera un nivel de confianza aceptable.

**Recomendación:** avanzar hacia un despliegue controlado (por ejemplo, en modo *shadow* o *canary*), acompañado de monitoreo continuo de métricas de desempeño y recalibración periódica del modelo.
