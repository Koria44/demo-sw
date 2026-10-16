/**
 * Encabezado de configuración de Tailwind CSS para demo-sw (NORTE Studio)
 * Define los tokens de diseño visual de la marca: paleta sobria de streetwear,
 * tipografías con alta legibilidad, espaciados consistentes y radios de 0 a 4px
 * para una estética editorial minimalista y contemporánea.
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './static/js/**/*.js',
    './apps/**/*.py',
  ],
  theme: {
    extend: {
      // Paleta de colores de NORTE Studio:
      // Tonos neutros editoriales para la interfaz y colores característicos de prendas streetwear.
      colors: {
        // Fondo base "hueso editorial" (#F6F5F2) y variantes neutras
        bone: {
          DEFAULT: '#F6F5F2', // Fondo general de la tienda
          light: '#FCFBF9',   // Fondos de tarjetas y contenedores elevados
          dark: '#EAE8E1',    // Bordes sutiles y separadores divisorios
          subtle: '#D8D5CC',  // Bordes activos y estados hover en líneas
        },
        // Escala de texto y oscuros profundos
        dark: {
          DEFAULT: '#111111', // Texto principal, titulares y botones primarios
          surface: '#1A1A1A', // Fondo del footer y overlays oscuros
          muted: '#666666',   // Texto secundario, descripciones y placeholders
          faint: '#999999',   // Metadatos pequeños, fechas y etiquetas menores
        },
        // Paleta de productos streetwear (utilizados en filtros, variantes de color y SVGs)
        sw: {
          black: '#161616',     // Negro carbón / washed black
          chocolate: '#33261D', // Café chocolate profundo de alto gramaje
          melange: '#B6B5B0',   // Gris melange clásico de polerones
          navy: '#1E2530',      // Azul marino industrial sobrio
          burgundy: '#4A1525',  // Burdeo / vino profundo
          rose: '#D9B8B0',      // Rosa palo empolvado contemporáneo
          olive: '#383B2D',     // Verde oliva militar apagado
          cream: '#ECE7DE',     // Blanco crudo / raw cotton
        },
        // Color de acento editorial mínimo (para badges de oferta y alertas)
        accent: {
          DEFAULT: '#9E2A2B',   // Acento burdeo rojizo refinado
          light: '#F8E9E9',     // Fondo suave de alertas
        }
      },
      // Tipografías: Space Grotesk para titulares con fuerza e Inter para lectura fluida
      fontFamily: {
        sans: ['"Space Grotesk"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        body: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      // Tracking amplio para titulares en mayúsculas estilo lookbook
      letterSpacing: {
        'tightest': '-0.03em',
        'wider-label': '0.12em',
        'widest-caps': '0.22em', // Titulares editoriales h1/h2
      },
      // Radios de 0 a 4px estrictos según la dirección visual editorial (sin bordes redondeados tipo píldora)
      borderRadius: {
        'none': '0px',
        'xs': '1px',
        'sm': '2px',
        'DEFAULT': '2px',
        'md': '3px',
        'lg': '4px',
        'full': '9999px', // Reservado únicamente para los puntos selectores de color
      },
      // Relación de aspecto para prendas de ropa (editorial lookbook 4:5)
      aspectRatio: {
        'lookbook': '4 / 5',
      },
      // Curvas de animación suaves con easing natural
      transitionTimingFunction: {
        'editorial': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class', // Permite control granular de inputs mediante clases
    }),
  ],
};
