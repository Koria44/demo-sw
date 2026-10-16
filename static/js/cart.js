/**
 * @file cart.js
 * @description Gestor integral del Carrito de Compras en el frontend para demo-sw.
 * Controla el drawer lateral, la sincronización en vivo mediante peticiones fetch a la API de Django,
 * el cálculo visual de la barra de progreso hacia el despacho gratis ($70.000 CLP) y las microanimaciones.
 */
import { AccessibleDrawer } from './drawer.js';

export function initCart() {
  const cartDrawerEl = document.getElementById('cart-drawer');
  if (!cartDrawerEl) return null;

  // Drawer accesible del carrito
  const cartDrawer = new AccessibleDrawer({
    drawerId: 'cart-drawer',
    triggerSelector: '[data-cart-trigger]',
    closeSelector: '[data-cart-close]',
    backdropSelector: '[data-cart-backdrop]',
    panelSelector: '[data-cart-panel]',
    onOpen: () => {
      // Sincroniza el estado del carrito al abrir
      syncCartState();
    }
  });

  const cartItemsContainer = document.getElementById('cart-items-list');
  const cartEmptyState = document.getElementById('cart-empty-state');
  const cartSubtotalEl = document.getElementById('cart-subtotal-val');
  const cartShippingCostEl = document.getElementById('cart-shipping-cost-val');
  const cartTotalEl = document.getElementById('cart-total-val');
  const cartFreeShippingText = document.getElementById('cart-free-shipping-text');
  const cartFreeShippingBar = document.getElementById('cart-free-shipping-bar');
  const headerCartCounters = document.querySelectorAll('[data-cart-counter]');

  // Sincronización inicial
  syncCartState();

  // Escuchador global de botones de añadir al carrito
  document.addEventListener('submit', (e) => {
    const form = e.target.closest('[data-add-to-cart-form]');
    if (!form) return;

    e.preventDefault();
    handleAddToCart(form);
  });

  // Delegación de eventos para botones de sumar, restar o eliminar dentro del drawer
  if (cartItemsContainer) {
    cartItemsContainer.addEventListener('click', (e) => {
      const incBtn = e.target.closest('[data-cart-qty-inc]');
      const decBtn = e.target.closest('[data-cart-qty-dec]');
      const removeBtn = e.target.closest('[data-cart-remove]');

      if (incBtn) {
        const itemKey = incBtn.dataset.itemKey;
        const currentQty = parseInt(incBtn.dataset.currentQty, 10);
        updateItemQuantity(itemKey, currentQty + 1);
      } else if (decBtn) {
        const itemKey = decBtn.dataset.itemKey;
        const currentQty = parseInt(decBtn.dataset.currentQty, 10);
        updateItemQuantity(itemKey, Math.max(0, currentQty - 1));
      } else if (removeBtn) {
        const itemKey = removeBtn.dataset.itemKey;
        removeItem(itemKey);
      }
    });
  }

  /**
   * Procesa la adición de una prenda validando la selección de talla.
   * @param {HTMLFormElement} form - Formulario que contiene product_id, size y color_id.
   */
  async function handleAddToCart(form) {
    const formData = new FormData(form);
    const productId = formData.get('product_id');
    const size = formData.get('size');
    const colorId = formData.get('color_id');
    const quantity = formData.get('quantity') || 1;
    const submitBtn = form.querySelector('[type="submit"]');

    // Validación de selección obligatoria de talla
    if (!size) {
      showSizeSelectionWarning(form);
      return;
    }

    // Efecto visual en el botón de compra
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.dataset.originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = `
        <span class="inline-flex items-center space-x-2">
          <svg class="animate-spin h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
          </svg>
          <span>Añadiendo...</span>
        </span>
      `;
    }

    try {
      const response = await fetch('/carrito/api/agregar/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
          product_id: productId,
          size: size,
          color_id: colorId,
          quantity: quantity,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || 'No se pudo agregar la prenda al carrito.');
        return;
      }

      // Actualiza la interfaz del carrito y abre el drawer
      renderCartData(data.cart);
      cartDrawer.open();

      // Microanimación en el contador del header
      animateCartBadge();
    } catch (err) {
      console.error('Error al agregar al carrito:', err);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = submitBtn.dataset.originalText || 'Agregar al Carrito';
      }
    }
  }

  /**
   * Resalta visualmente el selector de tallas cuando el usuario olvida seleccionarla.
   * @param {HTMLElement} form - Contenedor del producto.
   */
  function showSizeSelectionWarning(form) {
    const sizeContainer = form.querySelector('[data-size-selector-container]') || form;
    const existingAlert = form.querySelector('[data-size-error-msg]');

    if (existingAlert) {
      existingAlert.classList.add('animate-bounce');
      setTimeout(() => existingAlert.classList.remove('animate-bounce'), 800);
      return;
    }

    const alertEl = document.createElement('div');
    alertEl.dataset.sizeErrorMsg = 'true';
    alertEl.className = 'text-[11px] font-bold text-accent uppercase tracking-wider-label mt-2 py-1 px-2 bg-accent-light border-l-2 border-accent transition-opacity';
    alertEl.textContent = '↑ Por favor selecciona una talla para continuar';

    sizeContainer.appendChild(alertEl);

    setTimeout(() => {
      alertEl.style.opacity = '0';
      setTimeout(() => alertEl.remove(), 400);
    }, 4000);
  }

  /**
   * Modifica la cantidad de una prenda o la retira si llega a 0.
   */
  async function updateItemQuantity(itemKey, quantity) {
    try {
      const response = await fetch('/carrito/api/actualizar/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ item_key: itemKey, quantity: quantity }),
      });

      const data = await response.json();
      if (data.success) {
        renderCartData(data.cart);
        animateCartBadge();
      }
    } catch (err) {
      console.error('Error al actualizar cantidad:', err);
    }
  }

  /**
   * Elimina un ítem específico del carrito.
   */
  async function removeItem(itemKey) {
    try {
      const response = await fetch('/carrito/api/eliminar/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ item_key: itemKey }),
      });

      const data = await response.json();
      if (data.success) {
        renderCartData(data.cart);
        animateCartBadge();
      }
    } catch (err) {
      console.error('Error al eliminar ítem:', err);
    }
  }

  /**
   * Consulta el estado del carrito al servidor para sincronizar frontend.
   */
  async function syncCartState() {
    try {
      const response = await fetch('/carrito/api/estado/');
      if (!response.ok) return;
      const data = await response.json();
      renderCartData(data);
    } catch (err) {
      console.warn('No se pudo sincronizar el carrito:', err);
    }
  }

  /**
   * Actualiza el DOM del drawer, subtotales y barra de envío gratis.
   * @param {Object} cart - Objeto serializado del carrito.
   */
  function renderCartData(cart) {
    // Actualiza contadores del header
    headerCartCounters.forEach((counter) => {
      counter.textContent = cart.total_items;
      if (cart.total_items > 0) {
        counter.classList.remove('hidden');
      } else {
        counter.classList.add('hidden');
      }
    });

    // Actualiza barra de envío gratis
    if (cartFreeShippingBar && cartFreeShippingText) {
      const percentage = cart.free_shipping_progress_percentage;
      cartFreeShippingBar.style.width = `${percentage}%`;

      if (cart.qualifies_for_free_shipping) {
        cartFreeShippingText.innerHTML = `
          <span class="font-bold text-dark">¡FELICITACIONES!</span> TIENES DESPACHO GRATIS A TODO CHILE
        `;
        cartFreeShippingBar.className = 'h-full bg-dark transition-all duration-500 ease-editorial';
      } else {
        cartFreeShippingText.innerHTML = `
          TE FALTAN <span class="font-bold text-dark font-mono">${cart.formatted_remaining_for_free_shipping}</span> PARA DESPACHO GRATIS
        `;
        cartFreeShippingBar.className = 'h-full bg-dark/70 transition-all duration-500 ease-editorial';
      }
    }

    // Actualiza subtotales
    if (cartSubtotalEl) cartSubtotalEl.textContent = cart.formatted_subtotal;
    if (cartShippingCostEl) cartShippingCostEl.textContent = cart.formatted_shipping_cost;
    if (cartTotalEl) cartTotalEl.textContent = cart.formatted_total;

    // Renderiza la lista de ítems o muestra estado vacío
    if (!cartItemsContainer) return;

    if (cart.items.length === 0) {
      if (cartEmptyState) cartEmptyState.classList.remove('hidden');
      cartItemsContainer.innerHTML = '';
      const checkoutBtn = document.getElementById('cart-drawer-checkout-btn');
      if (checkoutBtn) checkoutBtn.classList.add('opacity-50', 'pointer-events-none');
      return;
    }

    if (cartEmptyState) cartEmptyState.classList.add('hidden');
    const checkoutBtn = document.getElementById('cart-drawer-checkout-btn');
    if (checkoutBtn) checkoutBtn.classList.remove('opacity-50', 'pointer-events-none');

    cartItemsContainer.innerHTML = cart.items.map((item) => `
      <div class="flex items-center space-x-4 py-4 border-b border-bone-dark group">
        <!-- Miniatura de la prenda -->
        <a href="/catalogo/producto/${item.slug}/" class="w-16 h-20 bg-bone-dark/50 flex-shrink-0 flex items-center justify-center overflow-hidden border border-bone-subtle">
          ${
            item.has_image
              ? `<img src="${item.image_url}" alt="${item.name}" class="w-full h-full object-cover">`
              : `<div class="w-9 h-12 flex items-center justify-center" style="color: ${item.color_hex}">
                   <svg viewBox="0 0 100 120" class="w-full h-full fill-current">
                     <path d="M20 25 L35 15 L65 15 L80 25 L88 45 L72 52 L68 36 L68 105 L32 105 L32 36 L28 52 L12 45 Z"/>
                   </svg>
                 </div>`
          }
        </a>

        <!-- Datos del producto -->
        <div class="flex-1 min-w-0">
          <div class="flex justify-between items-start">
            <a href="/catalogo/producto/${item.slug}/" class="text-xs font-semibold text-dark uppercase tracking-wider-label truncate block hover:underline">
              ${item.name}
            </a>
            <button type="button" data-cart-remove data-item-key="${item.item_key}" class="text-dark-muted hover:text-accent p-1 transition-colors" aria-label="Eliminar ${item.name}">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <div class="flex items-center space-x-2 text-[11px] text-dark-muted font-mono mt-1">
            <span>Talla: <strong class="text-dark">${item.size}</strong></span>
            <span>•</span>
            <span class="inline-flex items-center space-x-1">
              <span class="w-2.5 h-2.5 rounded-full inline-block border border-bone-subtle" style="background-color: ${item.color_hex}"></span>
              <span>${item.color_name}</span>
            </span>
          </div>

          <!-- Controles de cantidad y precio por línea -->
          <div class="flex items-center justify-between mt-3">
            <div class="inline-flex items-center border border-bone-subtle bg-bone-light">
              <button type="button" data-cart-qty-dec data-item-key="${item.item_key}" data-current-qty="${item.quantity}" class="w-7 h-7 flex items-center justify-center text-xs text-dark hover:bg-bone-dark transition-colors" aria-label="Disminuir cantidad">
                -
              </button>
              <span class="w-8 text-center text-xs font-mono font-medium">${item.quantity}</span>
              <button type="button" data-cart-qty-inc data-item-key="${item.item_key}" data-current-qty="${item.quantity}" class="w-7 h-7 flex items-center justify-center text-xs text-dark hover:bg-bone-dark transition-colors" aria-label="Aumentar cantidad">
                +
              </button>
            </div>
            <span class="text-xs font-mono font-bold text-dark">${item.formatted_line_total}</span>
          </div>
        </div>
      </div>
    `).join('');
  }

  /**
   * Ejecuta microanimación de salto en el badge del carrito.
   */
  function animateCartBadge() {
    headerCartCounters.forEach((badge) => {
      badge.classList.remove('badge-bounce');
      // Forzar reflujo para reiniciar la animación
      void badge.offsetWidth;
      badge.classList.add('badge-bounce');
    });
  }

  /**
   * Obtiene el token CSRF desde la cookie de Django.
   */
  function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    // Fallback al input hidden de CSRF si existe
    if (!cookieValue) {
      const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
      if (csrfInput) cookieValue = csrfInput.value;
    }
    return cookieValue;
  }

  return cartDrawer;
}
