/**
 * @file search.js
 * @description Módulo de búsqueda interactiva en vivo con debounce para demo-sw.
 * Consulta el endpoint JSON de catálogo en tiempo real, renderiza miniaturas de prendas
 * y maneja navegación por teclado.
 */
import { AccessibleDrawer } from './drawer.js';

export function initSearch() {
  const searchInput = document.getElementById('search-modal-input');
  const resultsContainer = document.getElementById('search-results-container');
  const resultsCount = document.getElementById('search-results-count');
  let debounceTimer = null;

  // Instancia del modal de búsqueda accesible
  const searchDrawer = new AccessibleDrawer({
    drawerId: 'search-modal',
    triggerSelector: '[data-search-trigger]',
    closeSelector: '[data-search-close]',
    backdropSelector: '[data-search-backdrop]',
    panelSelector: '[data-search-panel]',
    onOpen: () => {
      // Foco inmediato en el campo de texto de búsqueda al abrir
      setTimeout(() => {
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }, 150);
    },
    onClose: () => {
      if (searchInput) searchInput.value = '';
      if (resultsContainer) resultsContainer.innerHTML = '';
      if (resultsCount) resultsCount.textContent = '';
    }
  });

  if (!searchInput || !resultsContainer) return;

  // Escuchador de tipeo con debounce de 250ms
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(debounceTimer);

    if (query.length < 2) {
      resultsContainer.innerHTML = `
        <div class="py-12 text-center text-xs text-dark-muted uppercase tracking-wider-label">
          Escribe al menos 2 caracteres para buscar prendas...
        </div>
      `;
      if (resultsCount) resultsCount.textContent = '';
      return;
    }

    // Muestra skeleton mientras consulta
    resultsContainer.innerHTML = `
      <div class="space-y-3 py-4">
        <div class="h-16 bg-bone-dark/50 shimmer-mask"></div>
        <div class="h-16 bg-bone-dark/50 shimmer-mask"></div>
        <div class="h-16 bg-bone-dark/50 shimmer-mask"></div>
      </div>
    `;

    debounceTimer = setTimeout(() => {
      fetchSearchResults(query);
    }, 250);
  });

  /**
   * Consulta el endpoint de búsqueda y renderiza los resultados.
   * @param {string} query - Término de búsqueda.
   */
  async function fetchSearchResults(query) {
    try {
      const response = await fetch(`/catalogo/api/buscar/?q=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Error al consultar el servidor');
      const data = await response.json();

      renderResults(data.results, query);
    } catch (err) {
      resultsContainer.innerHTML = `
        <div class="py-8 text-center text-xs text-accent">
          Ocurrió un error al cargar los resultados. Intenta nuevamente.
        </div>
      `;
    }
  }

  /**
   * Genera el HTML de la lista de productos encontrados.
   * @param {Array} results - Lista de productos retornados por la API.
   * @param {string} query - Término de búsqueda.
   */
  function renderResults(results, query) {
    if (resultsCount) {
      resultsCount.textContent = `${results.length} ${results.length === 1 ? 'resultado' : 'resultados'} para "${query}"`;
    }

    if (results.length === 0) {
      resultsContainer.innerHTML = `
        <div class="py-16 text-center space-y-3">
          <p class="text-sm font-semibold uppercase tracking-wider-label text-dark">No encontramos coincidencias para "${query}"</p>
          <p class="text-xs text-dark-muted">Prueba buscando términos generales como "Hoodie", "Boxy", "Chocolate" o "Knit".</p>
        </div>
      `;
      return;
    }

    const itemsHtml = results.map((item) => `
      <a href="${item.url}" class="group flex items-center justify-between p-3 border-b border-bone-dark hover:bg-bone-dark/30 transition-colors">
        <div class="flex items-center space-x-4">
          <!-- Miniatura -->
          <div class="w-12 h-14 bg-bone-dark/60 flex items-center justify-center overflow-hidden flex-shrink-0">
            ${
              item.has_image
                ? `<img src="${item.image_url}" alt="${item.name}" class="w-full h-full object-cover">`
                : `<div class="w-7 h-9 flex items-center justify-center" style="color: ${item.hex_code}">
                     <svg viewBox="0 0 100 120" class="w-full h-full fill-current">
                       <path d="M20 25 L35 15 L65 15 L80 25 L88 45 L72 52 L68 36 L68 105 L32 105 L32 36 L28 52 L12 45 Z"/>
                     </svg>
                   </div>`
            }
          </div>
          <div>
            <span class="text-[10px] uppercase tracking-wider-label text-dark-muted font-mono block">${item.category_name}</span>
            <span class="text-xs font-semibold text-dark uppercase group-hover:underline">${item.name}</span>
          </div>
        </div>
        <div class="text-xs font-mono font-bold text-dark pl-4">
          ${item.formatted_price}
        </div>
      </a>
    `).join('');

    resultsContainer.innerHTML = `<div class="divide-y divide-bone-dark">${itemsHtml}</div>`;
  }

  return searchDrawer;
}
