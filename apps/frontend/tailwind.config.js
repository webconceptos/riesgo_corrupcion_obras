/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        riesgo: {
          bajo: '#0E7C66',
          medio: '#C77B19',
          extrema: '#B23A48',
        },
      },
    },
  },
  plugins: [],
}
