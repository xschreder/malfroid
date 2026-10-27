import { fetchConfig } from '@theme/utilities';
import { CartAddEvent } from '@theme/events';

/**
 * Suggestions de produits dans le tiroir panier (snippets/cart-drawer-upsell.liquid).
 * Ajoute la variante choisie au panier puis émet un CartAddEvent avec les sections
 * des cart-items-component, comme product-form.js, pour que le tiroir se mette à jour.
 *
 * @extends {HTMLElement}
 */
class CartDrawerUpsell extends HTMLElement {
  connectedCallback() {
    this.addEventListener('submit', this.#onSubmit);
  }

  disconnectedCallback() {
    this.removeEventListener('submit', this.#onSubmit);
  }

  /**
   * @param {SubmitEvent} event
   */
  #onSubmit = async (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;

    event.preventDefault();

    const button = form.querySelector('button[type="submit"]');
    const error = form.querySelector('.cart-upsell__error');
    if (button?.getAttribute('aria-busy') === 'true') return;

    button?.setAttribute('aria-busy', 'true');
    error?.setAttribute('hidden', '');

    const formData = new FormData(form);
    const sectionIds = new Set();
    for (const item of document.querySelectorAll('cart-items-component')) {
      if (item instanceof HTMLElement && item.dataset.sectionId) sectionIds.add(item.dataset.sectionId);
    }
    formData.append('sections', Array.from(sectionIds).join(','));

    const fetchCfg = fetchConfig('javascript', { body: formData });

    try {
      const response = await fetch(Theme.routes.cart_add_url, {
        ...fetchCfg,
        headers: {
          ...fetchCfg.headers,
          Accept: 'text/html',
        },
      });
      const data = await response.json();

      if (data.status) {
        if (error) {
          error.textContent = data.description || data.message;
          error.removeAttribute('hidden');
        }
        return;
      }

      this.dispatchEvent(
        new CartAddEvent({}, String(formData.get('id')), {
          source: 'cart-drawer-upsell',
          itemCount: Number(formData.get('quantity')) || 1,
          productId: form.dataset.productId,
          sections: data.sections,
        })
      );
    } catch (e) {
      console.error(e);
    } finally {
      button?.removeAttribute('aria-busy');
    }
  };
}

if (!customElements.get('cart-drawer-upsell')) {
  customElements.define('cart-drawer-upsell', CartDrawerUpsell);
}
