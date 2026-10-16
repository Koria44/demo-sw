/**
 * @file drawer.js
 * @description Módulo de control accesible para paneles deslizantes y modales (Drawer).
 * Implementa gestión estricta de foco (Focus Trap), cierre con tecla Escape, bloqueo de scroll en el body
 * y sincronización de atributos ARIA (aria-expanded, aria-hidden) para lectores de pantalla.
 */

/**
 * Clase que encapsula la lógica de apertura, cierre y accesibilidad de un Drawer u Overlay.
 */
export class AccessibleDrawer {
  /**
   * Crea una instancia de AccessibleDrawer.
   * @param {Object} options - Parámetros de configuración.
   * @param {string} options.drawerId - ID del elemento contenedor del drawer.
   * @param {string} options.triggerSelector - Selector CSS de los botones que abren el drawer.
   * @param {string} options.closeSelector - Selector CSS de los botones de cierre.
   * @param {string} options.backdropSelector - Selector CSS del fondo oscuro/backdrop.
   * @param {string} [options.panelSelector] - Selector CSS del panel deslizante interno.
   * @param {Function} [options.onOpen] - Callback ejecutado al abrir.
   * @param {Function} [options.onClose] - Callback ejecutado al cerrar.
   */
  constructor({
    drawerId,
    triggerSelector,
    closeSelector,
    backdropSelector,
    panelSelector = '[data-drawer-panel]',
    onOpen = null,
    onClose = null,
  }) {
    this.drawer = document.getElementById(drawerId);
    if (!this.drawer) return;

    this.panel = this.drawer.querySelector(panelSelector) || this.drawer;
    this.triggers = document.querySelectorAll(triggerSelector);
    this.closeButtons = this.drawer.querySelectorAll(closeSelector);
    this.backdrop = this.drawer.querySelector(backdropSelector);
    this.onOpen = onOpen;
    this.onClose = onClose;

    this.isOpen = false;
    this.previousFocusedElement = null;
    this.focusableElementsSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

    this.init();
  }

  /**
   * Enlaza los escuchadores de eventos para interacción de usuario.
   */
  init() {
    // Apertura desde los disparadores
    this.triggers.forEach((trigger) => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        this.open(trigger);
      });
    });

    // Cierre desde botones designados
    this.closeButtons.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.close();
      });
    });

    // Cierre al hacer clic en el telón de fondo (backdrop)
    if (this.backdrop) {
      this.backdrop.addEventListener('click', () => this.close());
    }

    // Escuchador global de teclado para tecla Escape y ciclado de foco (Tab)
    document.addEventListener('keydown', (e) => {
      if (!this.isOpen) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        this.close();
      } else if (e.key === 'Tab') {
        this.trapFocus(e);
      }
    });
  }

  /**
   * Abre el drawer, bloquea el scroll y transfiere el foco.
   * @param {HTMLElement} [triggerElement] - Botón que disparó la apertura para restaurar el foco al cerrar.
   */
  open(triggerElement = null) {
    if (this.isOpen) return;
    this.isOpen = true;
    this.previousFocusedElement = triggerElement || document.activeElement;

    // Actualiza atributos ARIA
    this.drawer.setAttribute('aria-hidden', 'false');
    this.triggers.forEach((t) => t.setAttribute('aria-expanded', 'true'));

    // Muestra el contenedor
    this.drawer.classList.remove('pointer-events-none', 'opacity-0');
    this.drawer.classList.add('pointer-events-auto', 'opacity-100');

    // Desliza el panel interior
    if (this.panel) {
      this.panel.classList.remove('translate-x-full', '-translate-x-full', 'translate-y-full');
      this.panel.classList.add('translate-x-0', 'translate-y-0');
    }

    // Bloquea el scroll del documento
    document.body.style.overflow = 'hidden';

    // Foco accesible al primer elemento interactivo
    setTimeout(() => {
      const focusables = this.drawer.querySelectorAll(this.focusableElementsSelector);
      if (focusables.length > 0) {
        focusables[0].focus();
      }
    }, 100);

    if (typeof this.onOpen === 'function') {
      this.onOpen();
    }
  }

  /**
   * Cierra el drawer y restaura el foco al disparador original.
   */
  close() {
    if (!this.isOpen) return;
    this.isOpen = false;

    // Actualiza atributos ARIA
    this.drawer.setAttribute('aria-hidden', 'true');
    this.triggers.forEach((t) => t.setAttribute('aria-expanded', 'false'));

    // Oculta el contenedor con transición
    this.drawer.classList.add('opacity-0', 'pointer-events-none');
    this.drawer.classList.remove('opacity-100', 'pointer-events-auto');

    // Retrae el panel interior
    if (this.panel) {
      const isRight = this.panel.dataset.drawerPosition === 'right' || !this.panel.dataset.drawerPosition;
      if (isRight) {
        this.panel.classList.add('translate-x-full');
        this.panel.classList.remove('translate-x-0');
      } else {
        this.panel.classList.add('-translate-x-full');
        this.panel.classList.remove('translate-x-0');
      }
    }

    // Restaura el scroll del documento
    document.body.style.overflow = '';

    // Devuelve el foco al elemento disparador para navegación fluida por teclado
    if (this.previousFocusedElement && typeof this.previousFocusedElement.focus === 'function') {
      this.previousFocusedElement.focus();
    }

    if (typeof this.onClose === 'function') {
      this.onClose();
    }
  }

  /**
   * Retiene el foco dentro del drawer mientras esté activo (Focus Trap).
   * @param {KeyboardEvent} e - Evento de teclado de la tecla Tab.
   */
  trapFocus(e) {
    const focusable = Array.from(this.drawer.querySelectorAll(this.focusableElementsSelector)).filter(
      (el) => el.offsetParent !== null // Solo elementos visibles
    );

    if (focusable.length === 0) return;

    const firstElement = focusable[0];
    const lastElement = focusable[focusable.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      }
    } else {
      if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  }
}
