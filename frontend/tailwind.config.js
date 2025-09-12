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
        primary: "#485551",   // Dark green
        secondary: "#bfea6a", // Light green
        tertiary: "#f1ffde",  // Pale yellow
        white: "#ffffff",     // White
      },
    },
  },
  plugins: [],
}

