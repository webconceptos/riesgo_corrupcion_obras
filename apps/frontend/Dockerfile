# Build: compila el dashboard Vite/React a archivos estáticos.
FROM node:20-slim AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# VITE_API_BASE se "hornea" en el build (variables Vite son de compilación,
# no de runtime) — para apuntar a otra API hay que reconstruir la imagen
# con --build-arg VITE_API_BASE=https://tu-api-real.
ARG VITE_API_BASE=http://localhost:8000
ENV VITE_API_BASE=${VITE_API_BASE}
RUN npm run build

# Serve: nginx sirviendo los estáticos (vite preview no está pensado para producción).
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
