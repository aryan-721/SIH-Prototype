/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gov: {
          50: '#f0f7ff',
          100: '#e0effe',
          500: '#1d70b8',
          600: '#1d4ed8',
          700: '#1e40af',
          800: '#1e3a8a',
          900: '#0f172a',
        },
        brand: {
          blue: '#1d70b8',
          accent: '#2563eb',
          navy: '#0f2042',
          critical: '#dc2626',
          medium: '#ea580c',
          low: '#059669',
          satisfied: '#16a34a'
        }
      }
    },
  },
  plugins: [],
}
