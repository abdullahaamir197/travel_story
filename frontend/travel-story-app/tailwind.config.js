/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",

  ],
  theme: {
    fontFamily: {
      display:"poppins", "sans-serif",

    },
    extend: {
      //colors used in the project
      colors:{
        primary:"#058603", 
        secondary:"#EF863E",
      },
    },
  },
  plugins: [],
}

