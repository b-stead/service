/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
    "./frontend/src/**/*.{js,jsx,ts,tsx}",
    "./frontend/public/index.html",
    "/app/src/**/*.{js,jsx,ts,tsx}", // Adjusted for Docker build context
    "/app/public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#519c4b",   // celadon
        secondary: "#0078cf", // cambridge Blue
        tertiary: "#356b30",  // true-blue
        quaternary: "#62965d",
        quinary: "#04426e",
        accent_dark: "#3f3047ff",     // english Violet"
        accent_light: "#eef36aff",     // icterine
      },
    },
  },
  plugins: [],
};

/*
primary: "#485551",   // Dark green
        secondary: "#bfea6a", // Light green
        tertiary: "#f1ffde",  // Pale yellow
        white: "#ffffff",     // White
        */