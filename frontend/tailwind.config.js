/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#ecfdf9',
          100: '#d0fef1',
          200: '#a3fce2',
          300: '#64f7cf',
          400: '#22e5b3',
          500: '#05c896',
          600: '#00a07a',
          700: '#008063',
          800: '#036650',
          900: '#045342',
        },
      },
      animation: {
        'bounce-once': 'bounce 0.4s ease-in-out',
        'fade-in': 'fadeIn 0.4s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'float': 'float 6s ease-in-out infinite',
        'shimmer': 'shimmer 1.8s infinite',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-18px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(14,165,233,0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(16,185,129,0.5)' },
        },
      },
      boxShadow: {
        'card': '0 2px 16px 0 rgba(0,0,0,0.4)',
        'card-hover': '0 8px 40px 0 rgba(14,165,233,0.25)',
        'glow-sky': '0 0 30px rgba(14,165,233,0.4)',
        'glow-emerald': '0 0 30px rgba(16,185,129,0.4)',
        'inner-glow': 'inset 0 1px 0 rgba(255,255,255,0.08)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
