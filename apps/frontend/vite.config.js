import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    watch: {
      // Necesario en Windows+Docker: inotify no funciona sobre bind mounts
      usePolling: true,
      interval: 1000,
    },
  },
})
