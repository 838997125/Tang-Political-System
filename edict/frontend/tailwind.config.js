/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // 三省六部主题色
        imperial: {
          50: '#fef7ed',
          100: '#fdecd4',
          200: '#fad5a8',
          300: '#f7b671',
          400: '#f38d38',
          500: '#f07012',
          600: '#e15808',
          700: '#bb4009',
          800: '#95330f',
          900: '#792c10',
        },
        dynasty: {
          50: '#fdf4f3',
          100: '#fce8e4',
          200: '#fad4ce',
          300: '#f5b5ab',
          400: '#ee8a7a',
          500: '#e25f4d',
          600: '#cf4430',
          700: '#ae3624',
          800: '#903022',
          900: '#782d23',
        },
      },
    },
  },
  plugins: [],
}
