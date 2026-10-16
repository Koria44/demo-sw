/**
 * @file menu.js
 * @description Controlador del menú de navegación móvil para pantallas táctiles.
 * Abre el panel lateral izquierdo con lista de categorías, enlaces directos y datos de contacto.
 */
import { AccessibleDrawer } from './drawer.js';

export function initMobileMenu() {
  const menuDrawer = new AccessibleDrawer({
    drawerId: 'mobile-menu-drawer',
    triggerSelector: '[data-menu-trigger]',
    closeSelector: '[data-menu-close]',
    backdropSelector: '[data-menu-backdrop]',
    panelSelector: '[data-menu-panel]',
  });

  return menuDrawer;
}
