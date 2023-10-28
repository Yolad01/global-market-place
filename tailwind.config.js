// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [],
//   theme: {
//     extend: {},
//   },
//   plugins: [
//     require('@tailwindcss/forms'),
//     require('@tailwindcss/typography'),
//   ],
// }

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./skillas-pages/**/*.{html,js}', './skillas-dashboard/**/*.{html,js}',
    './client-pages/**/*.{html,js}',],
  theme: {
    extend: {
      fontFamily: {
        'primary': ['Inter'],
        'secondary': ['Poppins'],
      },
      colors: {
        veryDarkGreen: '#002D38',
        veryShadyGreen: '#06393F',
        lightGreen: '#1ECC77',
        shadeGreen: '#32C770',
        veryLightGreen: '#62EFB4',
        lightBlack: '#383838',
        someBlack: '#1C313A',
        someKindBlack: '#070707',
        veryLightBlack: '#333333',
        aKindOfBlack: '#494949',
        midBlack: '#656565',
        anotherBlack: '#252525',
        hr_black: '#22205F',
        purple: '#9747FF',
        ash: '#F3F2F7',
        white_ash: '#F7F7F7',
        lightAsh: '#D9D9D9',
        extremelyLightAsh: '#818181',
        veryLightAsh: '#B3B3B3',
        darkAsh: '#313131',
        shadeAsh: '#3E3E3E',
        shadeAsh_2: '#6F6F6F',
        shadeAsh_3: '#D9D9D9',
        shadeAsh_4: '#818181',
        red: '#C90000'
      },
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}

