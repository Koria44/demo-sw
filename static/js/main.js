/**
 * @file main.js
 * @description Punto de entrada principal para el JavaScript modular de demo-sw (NORTE Studio).
 * Inicializa el menú móvil, el drawer del carrito, el overlay de búsqueda en vivo,
 * los controladores de producto y el motor de animaciones y transiciones de página.
 */
import { initMobileMenu } from './menu.js';
import { initCart } from './cart.js';
import { initSearch } from './search.js';
import { initProductPage } from './product.js';
import { initAnimations } from './animations.js';

document.addEventListener('DOMContentLoaded', () => {
  // Inicialización de componentes interactivos accesibles
  initMobileMenu();
  initCart();
  initSearch();
  initProductPage();
  initAnimations();

  // Transición suave entre enlaces internos
  initPageTransitions();
});

/**
 * Añade una transición de desvanecimiento sutil al hacer clic en enlaces internos.
 */
function initPageTransitions() {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  const links = document.querySelectorAll('a[href^="/"]:not([target="_blank"]):not([download]):not([href^="/api"])');
  links.forEach((link) => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      // Ignorar anclas internas o enlaces vacíos
      if (href === '#' || href.startsWith('#') || e.ctrlKey || e.metaKey || e.shiftKey) return;

      // Desvanecer contenido principal
      const mainContent = document.querySelector('main');
      if (mainContent) {
        mainContent.style.transition = 'opacity 0.18s ease-out';
        mainContent.style.opacity = '0.4';
      }
    });
  });
}
