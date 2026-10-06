'use strict';
const root = document.documentElement;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  navigation.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Ouvrir le menu');
}
menuButton.addEventListener('click', () => {
  const isOpen = navigation.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Fermer le menu' : 'Ouvrir le menu');
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation.classList.contains('open')) {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.header')) closeMenu();
});
window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});
if ('IntersectionObserver' in window && !reducedMotion.matches) {
  root.classList.add('js');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
}
const motionButton = document.querySelector('.motion-toggle');
motionButton.addEventListener('click', () => {
  const paused = root.classList.toggle('motion-paused');
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.textContent = paused ? 'Reprendre les animations' : 'Mettre les animations en pause';
});
const light = document.querySelector('.cursor-light');
let pointerX = -1000;
let pointerY = -1000;
let pendingFrame = false;
window.addEventListener('pointermove', event => {
  if (event.pointerType !== 'mouse' || reducedMotion.matches || root.classList.contains('motion-paused')) return;
  pointerX = event.clientX - 300;
  pointerY = event.clientY - 300;
  if (!pendingFrame) {
    pendingFrame = true;
    requestAnimationFrame(() => {
      light.style.transform = `translate(${pointerX}px, ${pointerY}px)`;
      pendingFrame = false;
    });
  }
}, { passive: true });
document.documentElement.addEventListener('pointerleave', () => {
  light.style.transform = 'translate(-1000px, -1000px)';
});
const emailLink = document.querySelector('#email-link');
document.querySelectorAll('[data-offer]').forEach(link => {
  link.addEventListener('click', () => {
    const offer = link.dataset.offer;
    document.querySelector('#selected-offer').textContent = `Parlons de ton projet : ${offer}`;
    emailLink.href = `mailto:hello@vogzmotion.example?subject=${encodeURIComponent(`Mon projet — ${offer}`)}`;
  });
});
document.querySelector('#year').textContent = new Date().getFullYear();
