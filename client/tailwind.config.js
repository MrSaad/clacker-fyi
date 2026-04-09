/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'system-ui',
          'sans-serif',
        ],
        space: ['"Space Grotesk"', 'sans-serif'],
      },
      colors: {
        // Solarized light palette
        sol: {
          base03: '#002b36',
          base02: '#073642',
          base01: '#586e75', // primary text on light bg
          base00: '#657b83', // body text
          base0:  '#839496',
          base1:  '#93a1a1', // muted text
          base2:  '#eee8d5', // surface / highlight
          base3:  '#fdf6e3', // background
          yellow:  '#b58900',
          orange:  '#cb4b16',
          red:     '#dc322f',
          magenta: '#d33682',
          violet:  '#6c71c4',
          blue:    '#268bd2',
          cyan:    '#2aa198',
          green:   '#859900',
        },
        reddit: '#ff4500',
      },
    },
  },
  plugins: [],
};
