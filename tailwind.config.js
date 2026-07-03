/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0B0B0C',
        card: '#151515',
        border: '#2A2A2A',
        primary: {
          DEFAULT: '#10A37F',
          foreground: '#FFFFFF',
        },
        muted: {
          DEFAULT: '#A1A1AA',
          foreground: '#A1A1AA',
        },
        success: '#22C55E',
        warning: '#F59E0B',
        error: '#EF4444',
      },
      borderRadius: {
        lg: '20px',
        md: '16px',
        sm: '12px',
      }
    },
  },
  plugins: [],
}
