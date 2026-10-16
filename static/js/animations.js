/**
 * @file animations.js
 * @description Módulo de animaciones de entrada, scroll y microinteracciones para demo-sw.
 * Integra GSAP y ScrollTrigger con degradación elegante a IntersectionObserver y CSS.
 * Respeta rigurosamente las preferencias de usuario 'prefers-reduced-motion'.
 */

export function initAnimations() {
  // Verificación estricta de preferencia de movimiento reducido
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    // Si el usuario prefiere movimiento reducido, removemos el preloader sin transiciones
    const preloader = document.getElementById('site-preloader');
    if (preloader) preloader.style.display = 'none';
    return;
  }

  // 1. Preloader inicial y revelado del Hero
  initPreloaderAndHero();

  // 2. Control de Header al hacer scroll (ocultar al bajar, mostrar al subir)
  initHeaderScrollBehavior();

  // 3. Barra de progreso de lectura / scroll
  initScrollProgressBar();

  // 4. Rotador de mensajes de la barra de anuncios
  initAnnouncementTicker();

  // 5. Animación de revelado progresivo con ScrollTrigger / IntersectionObserver
  initScrollReveals();
}

/**
 * Preloader editorial breve con el isotipo de NORTE Studio.
 */
function initPreloaderAndHero() {
  const preloader = document.getElementById('site-preloader');
  if (!preloader) return;

  window.addEventListener('load', () => {
    setTimeout(() => {
      preloader.classList.add('opacity-0', 'pointer-events-none');
      setTimeout(() => {
        preloader.remove();
        // Dispara la animación de entrada del hero
        animateHeroEntrance();
      }, 450);
    }, 300);
  });
}

/**
 * Entrada escalonada de elementos del Hero.
 */
function animateHeroEntrance() {
  const heroElements = document.querySelectorAll('[data-hero-reveal]');
  heroElements.forEach((el, index) => {
    setTimeout(() => {
      el.classList.remove('opacity-0', 'translate-y-6');
      el.classList.add('opacity-100', 'translate-y-0');
    }, index * 120);
  });
}

/**
 * Oculta el header al hacer scroll hacia abajo y lo reaparece al subir.
 */
function initHeaderScrollBehavior() {
  const header = document.getElementById('site-header');
  if (!header) return;

  let lastScrollY = window.scrollY;
  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const currentScrollY = window.scrollY;

        // Añade sombra y fondo sólido si se ha bajado más de 20px
        if (currentScrollY > 20) {
          header.classList.add('bg-bone/95', 'backdrop-blur-md', 'border-b', 'border-bone-dark');
        } else {
          header.classList.remove('bg-bone/95', 'backdrop-blur-md', 'border-b', 'border-bone-dark');
        }

        // Ocultar al bajar, mostrar al subir (solo tras superar 120px)
        if (currentScrollY > 120 && currentScrollY > lastScrollY) {
          header.classList.add('-translate-y-full');
        } else {
          header.classList.remove('-translate-y-full');
        }

        lastScrollY = Math.max(0, currentScrollY);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/**
 * Barra fina de progreso de scroll ubicada bajo el header.
 */
function initScrollProgressBar() {
  const bar = document.getElementById('scroll-progress-indicator');
  if (!bar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight <= 0) return;
    const progress = (window.scrollY / totalHeight) * 100;
    bar.style.width = `${progress}%`;
  }, { passive: true });
}

/**
 * Rota los anuncios superiores con transición sutil.
 */
function initAnnouncementTicker() {
  const tickerItems = document.querySelectorAll('[data-announcement-item]');
  if (tickerItems.length <= 1) return;

  let currentIndex = 0;
  setInterval(() => {
    tickerItems[currentIndex].classList.add('opacity-0', '-translate-y-2');
    tickerItems[currentIndex].classList.remove('opacity-100', 'translate-y-0');

    currentIndex = (currentIndex + 1) % tickerItems.length;

    setTimeout(() => {
      tickerItems.forEach((it, idx) => {
        if (idx !== currentIndex) {
          it.classList.add('hidden');
        }
      });
      tickerItems[currentIndex].classList.remove('hidden');
      void tickerItems[currentIndex].offsetWidth; // forzar reflujo
      tickerItems[currentIndex].classList.remove('opacity-0', '-translate-y-2');
      tickerItems[currentIndex].classList.add('opacity-100', 'translate-y-0');
    }, 200);
  }, 4500);
}

/**
 * Revelado escalonado de tarjetas de producto y secciones editoriales al entrar al viewport.
 */
function initScrollReveals() {
  const revealTargets = document.querySelectorAll('[data-scroll-reveal]');
  if (revealTargets.length === 0) return;

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('opacity-0', 'translate-y-8');
          entry.target.classList.add('opacity-100', 'translate-y-0');
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '0px 0px -50px 0px',
      threshold: 0.1,
    });

    revealTargets.forEach((el) => {
      el.classList.add('opacity-0', 'translate-y-8', 'transition-all', 'duration-700', 'ease-editorial');
      observer.observe(el);
    });
  } else {
    // Si el navegador no soporta IntersectionObserver, mostramos directamente
    revealTargets.forEach((el) => el.classList.remove('opacity-0'));
  }
}
