/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "media",
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "Segoe UI", "sans-serif"],
        display: ["Space Grotesk", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      colors: {
        ink: "#1B2540",
        cream: "#F5F3EC",
        muted: "#A8AFC0",
        card: {
          DEFAULT: "#FFFFFF",
          muted: "#8D959C",
          muted2: "#5B6377",
          text2: "#4A4558",
        },
        divider: "#E3E7EA",
        tier: {
          strong: "#2E7D4F",
          cautious: "#D1A62C",
          "cautious-text": "#B5841C",
          explore: "#8A94A0",
          reject: "#B5542B",
        },
      },
      backgroundImage: {
        "dot-grid":
          "radial-gradient(circle, rgba(255,255,255,0.055) 1px, transparent 1.4px)",
      },
      backgroundSize: {
        "dot-grid": "24px 24px",
      },
      keyframes: {
        "card-reveal": {
          "0%": { opacity: "0", transform: "translateY(18px) scale(0.95) rotate(var(--tilt, 0deg))" },
          "100%": { opacity: "1", transform: "translateY(0) scale(1) rotate(var(--tilt, 0deg))" },
        },
      },
      animation: {
        "card-reveal": "card-reveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) both",
      },
    },
  },
  plugins: [],
};
