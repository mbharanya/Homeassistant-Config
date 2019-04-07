class CustomGroupCard extends HTMLElement {

  setConfig(config) {
    if (!config.group) {
      throw new Error('Please specify a group');
    }

    if (this.lastChild) this.removeChild(this.lastChild);
    const cardConfig = Object.assign({}, config);
    if (!cardConfig.card) cardConfig.card = {};
    if (!cardConfig.card.type) cardConfig.card.type = 'entities';

    this._config = cardConfig;
  }

  set hass(hass) {
    const config = this._config;
    const entities = hass.states[config.group].attributes['entity_id'];
    if (!config.card.entities || config.card.entities.length !== entities.length ||
      !config.card.entities.every((value, index) => value.entity === entities[index].entity)) {
      config.card.entities = entities;
    }

    entities.forEach(e => {
      const createdElement = document.createElement(`${config.card.type.replace("custom:", "")}`);
      this.appendChild(createdElement);
    })

    const children = Array.from(this.children)

    setTimeout(() => {
      children.map((child, i) => {
        child.setConfig(Object.assign({
          entity: config.card.entities[i]
        }, config.card))
        child.hass = hass
      })
    }, 500 )
  }

  getCardSize() {
    return 'getCardSize' in this.lastChild ? this.lastChild.getCardSize() : 1;
  }
}

customElements.define('custom-group-card', CustomGroupCard);
