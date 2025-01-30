/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    fontFamily: {
      racing: ["Racing Sans One", "serif"],
      lato: ["Lato", "serif"],
    },
    extend: {
      colors: {
        "custom-blue": "#003087",
        "custom-gold": "#C7940D",
        "custom-dark-gray": "#131313",
        "custom-gray": "#252525",
        "custom-light-gray": "#373737",
        "custom-off-white": "#D9D9D9",
        "custom-Val": "#BA3A46",
        "custom-RL": "#0060FF",
        "custom-Apex": "#8D3F3F",
      },
    },
  },
  plugins: [],
};
