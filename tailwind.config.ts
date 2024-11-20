import type { Config } from 'tailwindcss';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {}
	},

	daisyui: {
		themes: [
			{
				mytheme: {
					"primary": "#104547",
					"secondary": "#1D232A",
					"accent": "#FFFFFF",
					"neutral": "#161616",
					"base-100": "#1E2125",
					"info": "#00C4FF",
					"success": "#4CAF50",
					"warning": "#FF9800",
					"error": "#F44336",
				},
			},
			{
                newtheme: {
                    "primary": "#2e282a",  
					"secondary": "#ece3ca",  
					"accent": "#ffffff",  
					"neutral": "#161616",  
					"base-100": "#ece3ca",  
					"info": "#00C4FF",  
					"success": "#4CAF50",  
					"warning": "#FF9800", 
					"error": "#F44336",
                },
            },
		],
	},
	plugins: [require('daisyui'),]
} satisfies Config;
