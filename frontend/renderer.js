
const {remote} = require('electron');
const {Menu} = remote;


const menu = Menu.buildFromTemplate(template)
Menu.setApplicationMenu(menu)

const {droppable, addon} = require('electron-drag-drop');

class MyElement extends window.HTMLElement {
  constructor () {
    super();

    this.attachShadow({
      mode: 'open'
    });
    this.shadowRoot.innerHTML = `
      <div class="drop-area">
        Drop Area
      </div>
    `;

    this.$droparea = this.shadowRoot.querySelector('.drop-area');
    this._inited = false;
  }

  connectedCallback () {
    if ( this._inited ) {
      return;
    }
    this._inited = false;
    this._initDroppable(this.$droparea);
  }
}

addon(MyElement.prototype, droppable);

window.customElements.define('my-element', MyElement);

