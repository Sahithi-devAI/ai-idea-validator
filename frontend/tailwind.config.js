/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "media",
  theme: {
    extend: {
      colors: {
        surface: { light: "#fcfcfb", dark: "#1a1a19" },
        plane: { light: "#f9f9f7", dark: "#0d0d0d" },
        ink: {
          primary: { light: "#0b0b0b", dark: "#ffffff" },
          secondary: { light: "#52514e", dark: "#c3c2b7" },
          muted: "#898781",
        },
        hairline: { light: "#e1e0d9", dark: "#2c2c2a" },
        status: {
          good: "#0ca30c",
          warning: "#fab219",
          serious: "#ec835a",
          critical: "#d03b3b",
        },
        seq: {
          "track-light": "#cde2fb",
          "fill-light": "#2a78d6",
          "track-dark": "#184f95",
          "fill-dark": "#6da7ec",
        },
      },
    },
  },
  plugins: [],
};
