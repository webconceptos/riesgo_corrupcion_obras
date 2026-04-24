#!/bin/bash
# ==========================================================
# Script: push_semana.sh
# Proyecto: Detección de Riesgos de Corrupción en Obras Públicas
# Autores: Fernando García - Hilario Aradiel
# Objetivo: Automatizar commits y push a GitHub por semana
# ==========================================================

# Colores
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"

# Carpeta de logs
LOG_DIR="reports/logs"
mkdir -p "$LOG_DIR"
STAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/push_${STAMP}.log"

echo -e "${CYAN}=========================================================="
echo -e " 🚀 Script de subida a GitHub (push_semana.sh)"
echo -e "==========================================================${RESET}"

# === 1️⃣ Preguntar semana ===
read -p "📅 ¿A qué semana pertenece este commit? (Ejemplo: 6, 7, 8): " SEMANA
if [[ -z "$SEMANA" ]]; then
  echo -e "${YELLOW}⚠️  No ingresaste una semana. Cancelando.${RESET}"
  exit 1
fi
BRANCH="feat/semana${SEMANA}"

# === 2️⃣ Verificar rama actual ===
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  echo -e "${YELLOW}⚠️  Estás en la rama '${CURRENT_BRANCH}', pero deberías estar en '${BRANCH}'.${RESET}"
  read -p "¿Deseas cambiar automáticamente a la rama ${BRANCH}? (s/n): " SWITCH
  if [[ "$SWITCH" =~ ^[sS]$ ]]; then
    git checkout "$BRANCH" 2>&1 | tee -a "$LOG_FILE"
  else
    echo -e "${YELLOW}❌ No se cambió de rama. Cancelando.${RESET}"
    exit 1
  fi
fi

# === 3️⃣ Preguntar mensaje de commit ===
read -p "📝 Escribe el mensaje del commit: " MSG
if [[ -z "$MSG" ]]; then
  MSG="Semana ${SEMANA} ✅ Actualización automática del pipeline y resultados"
fi

# === 4️⃣ Mostrar resumen de confirmación ===
echo -e "\n${CYAN}Resumen:"
echo -e "  📅 Semana: ${SEMANA}"
echo -e "  🌿 Rama:   ${BRANCH}"
echo -e "  📝 Commit: ${MSG}"
echo -e "==========================================================${RESET}"
read -p "¿Deseas continuar con el push? (s/n): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[sS]$ ]]; then
  echo -e "${YELLOW}❌ Operación cancelada por el usuario.${RESET}"
  exit 0
fi

# === 5️⃣ Agregar y subir ===
echo -e "\n${GREEN}📦 Agregando archivos modificados...${RESET}"
git add . 2>&1 | tee -a "$LOG_FILE"

echo -e "\n${GREEN}✍️  Creando commit...${RESET}"
git commit -m "$MSG" 2>&1 | tee -a "$LOG_FILE"

echo -e "\n${GREEN}🚀 Subiendo a GitHub...${RESET}"
git push origin "$BRANCH" 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
  echo -e "\n${GREEN}✅ Push completado correctamente.${RESET}"
  echo -e "📘 Log: ${LOG_FILE}"
else
  echo -e "\n${YELLOW}⚠️  Hubo errores al subir. Revisa el log: ${LOG_FILE}${RESET}"
fi

echo -e "${CYAN}=========================================================="
echo -e " 🏁 Fin del proceso de subida a GitHub"
echo -e "==========================================================${RESET}"
