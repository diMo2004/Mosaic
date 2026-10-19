/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./App.{js,jsx,ts,tsx}', './src/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        canvas: '#090d16',
        panel: '#131b2e',
        muted: '#94a3b8',
        accent: '#38bdf8',
      },
    },
  },
};
