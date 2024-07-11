
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

      screens: {
        'compact': '280px', // Breakpoint at 280px
        'sm-compact': '350px', // Breakpoint at 350px
        'md-compact': '375px', //Breakpoint at 375px
        'custom': '400px', // Breakpoint at 400px
        'portable': '500px', // Breakpoint at 500px
      },

      colors: {
        veryDarkGreen: '#002D38',
        veryShadyGreen: '#06393F',
        lightGreen: '#1ECC77',
        brightGreen: '#25C348',
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
        shadeAsh_5: '#CDCDCD',
        shadeAsh_6: '#D5D5D5',
        shadeAsh_7: '#9A9A9A',
        red: '#C90000',
        lightBlue: '#8DAEE0',
        navyBlue: '#22205F',
        mintBlue: '#005EFE',
        darkBlue: '#404B7C',
        darkBlue_2: '#0D1D54',
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



