/**
 * @file product.js
 * @description Controlador de interacciones de la ficha de producto para demo-sw.
 * Maneja el cambio de color en vivo (modificando dinámicamente las capas de la ilustración SVG),
 * la selección de tallas con actualización de disponibilidad de stock,
 * conmutación de vista frontal/trasera y acordeones accesibles de especificaciones técnicas.
 */

export function initProductPage() {
  const productContainer = document.querySelector('[data-product-detail-container]');
  if (!productContainer) return;

  // Selectores de variantes de color
  const colorDots = productContainer.querySelectorAll('[data-color-dot]');
  const selectedColorNameLabel = productContainer.querySelector('[data-selected-color-name]');
  const hiddenColorInput = productContainer.querySelector('[data-color-input]');

  // Selectores de talla
  const sizeChips = productContainer.querySelectorAll('[data-size-chip]');
  const hiddenSizeInput = productContainer.querySelector('[data-size-input]');
  const selectedSizeLabel = productContainer.querySelector('[data-selected-size-label]');

  // Contador de cantidad
  const qtyInput = productContainer.querySelector('[data-qty-input]');
  const qtyIncBtn = productContainer.querySelector('[data-qty-inc]');
  const qtyDecBtn = productContainer.querySelector('[data-qty-dec]');

  // Botones de conmutación de vista (Frontal / Trasera)
  const viewSwitchButtons = productContainer.querySelectorAll('[data-view-switch]');
  const frontViewWrapper = productContainer.querySelector('[data-view-front]');
  const backViewWrapper = productContainer.querySelector('[data-view-back]');

  // Acordeones técnicos
  const accordionTriggers = productContainer.querySelectorAll('[data-accordion-trigger]');

  // 1. Lógica de cambio de color en vivo
  colorDots.forEach((dot) => {
    dot.addEventListener('click', () => {
      colorDots.forEach((d) => d.classList.remove('active'));
      dot.classList.add('active');

      const hex = dot.dataset.hexCode;
      const name = dot.dataset.colorName;
      const colorId = dot.dataset.colorId;

      if (selectedColorNameLabel) selectedColorNameLabel.textContent = name;
      if (hiddenColorInput) hiddenColorInput.value = colorId;

      // Actualiza en vivo el color de la tela en la ilustración SVG
      updateGarmentSvgColor(hex);
    });
  });

  /**
   * Cambia el relleno hexadecimal de todas las partes textiles del SVG.
   * @param {string} hexCode - Color hexadecimal elegido por el usuario.
   */
  function updateGarmentSvgColor(hexCode) {
    const clothElements = productContainer.querySelectorAll('[data-garment-cloth]');
    clothElements.forEach((el) => {
      el.style.fill = hexCode;
      el.setAttribute('fill', hexCode);
    });

    // Actualiza la tonalidad de sombras sutiles
    const shadowElements = productContainer.querySelectorAll('[data-garment-fold]');
    shadowElements.forEach((el) => {
      // Ajusta opacidad de pliegues para mantener contraste según el fondo
      el.style.stroke = '#000000';
    });
  }

  // 2. Lógica de selección de talla
  sizeChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      if (chip.classList.contains('disabled')) return;

      sizeChips.forEach((c) => c.classList.remove('active'));
      chip.classList.add('active');

      const sizeValue = chip.dataset.sizeValue;
      if (hiddenSizeInput) hiddenSizeInput.value = sizeValue;
      if (selectedSizeLabel) selectedSizeLabel.textContent = sizeValue;

      // Limpia advertencias previas si existían
      const errorMsg = productContainer.querySelector('[data-size-error-msg]');
      if (errorMsg) errorMsg.remove();
    });
  });

  // 3. Controles de cantidad
  if (qtyIncBtn && qtyInput) {
    qtyIncBtn.addEventListener('click', () => {
      const current = parseInt(qtyInput.value, 10) || 1;
      qtyInput.value = current + 1;
    });
  }

  if (qtyDecBtn && qtyInput) {
    qtyDecBtn.addEventListener('click', () => {
      const current = parseInt(qtyInput.value, 10) || 1;
      if (current > 1) qtyInput.value = current - 1;
    });
  }

  // 4. Conmutación de vistas (Frontal vs Trasera)
  viewSwitchButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      viewSwitchButtons.forEach((b) => b.classList.remove('border-dark', 'bg-dark', 'text-bone'));
      btn.classList.add('border-dark', 'bg-dark', 'text-bone');

      const view = btn.dataset.viewSwitch;
      if (view === 'front') {
        if (frontViewWrapper) frontViewWrapper.classList.remove('hidden');
        if (backViewWrapper) backViewWrapper.classList.add('hidden');
      } else if (view === 'back') {
        if (frontViewWrapper) frontViewWrapper.classList.add('hidden');
        if (backViewWrapper) backViewWrapper.classList.remove('hidden');
      }
    });
  });

  // 5. Acordeones accesibles
  accordionTriggers.forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
      const panelId = trigger.getAttribute('aria-controls');
      const panel = document.getElementById(panelId);
      const icon = trigger.querySelector('[data-accordion-icon]');

      if (!panel) return;

      if (isExpanded) {
        trigger.setAttribute('aria-expanded', 'false');
        panel.classList.add('hidden');
        if (icon) icon.style.transform = 'rotate(0deg)';
      } else {
        trigger.setAttribute('aria-expanded', 'true');
        panel.classList.remove('hidden');
        if (icon) icon.style.transform = 'rotate(180deg)';
      }
    });
  });
}
