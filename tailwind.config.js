
module.exports = {
  content: [
    'main/templates/**/*.{html,js}'
  ],
  theme: {
    extend: {
      fontFamily: {
        'primary': ['Inter'],
        'secondary': ['Poppins'],
      },
      // screens: {
      //   'sm': '640px',     // Small screens

      // },
      colors: {
        veryDarkGreen: '#002D38',
        veryShadyGreen: '#06393F',
        lightGreen: '#1ECC77',
        shadeGreen: '#32C770',
        veryLightGreen: '#62EFB4',
        lightBlack: '#383838',
        blackEssence: '#13254E',
        someBlack: '#1C313A',
        someKindBlack: '#070707',
        veryLightBlack: '#333333',
        aKindOfBlack: '#494949',
        midBlack: '#656565',
        anotherBlack: '#252525',
        hr_black: '#22205F',
        shade_black: '#1E1E1E',
        purple: '#9747FF',
        ash: '#F3F2F7',
        white_ash: '#F7F7F7',
        lightAsh: '#D9D9D9',
        light_ash: '#949191',
        extremelyLightAsh: '#818181',
        veryLightAsh: '#B3B3B3',
        darkAsh: '#313131',
        shadeAsh: '#3E3E3E',
        shadeAsh_2: '#6F6F6F',
        shadeAsh_3: '#D9D9D9',
        shadeAsh_4: '#818181',
        red: '#C90000',
        navyBlue: '#22205F',
        orangeEssence: '#FF7126',
        purpleEssence: '#58479F',
        pinkEssence: '#D1334D',
        blueEssence: '#1494D7',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ]
}