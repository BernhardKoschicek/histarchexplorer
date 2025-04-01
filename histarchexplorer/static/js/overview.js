document.getElementById("overview-content").innerHTML =
    `
<div><h1>TEST Blabla</h1></div>
<div class="col flex-column grid">

  <div class="${entity.description_class}">
    <div class="item-content">
      <div class="muuri-description">
        <span class="tile-label">DESCRIPTION</span>
        <p>${entity.description}</p>
      </div>
    </div>
  </div>

  ${entity.subunits ? `
    <div class="hierarchy-button">
      <div class="hierarchy-line"></div>
      <button type="button" class="btn btn-whitish rounded-5" disabled>
        <i class="bi bi-diagram-3"></i>
        <span class="nude-link">
          ${entity.subunits.length} ${entity.subunits.length === 1 ? "Subentity" : "Subentities"}
        </span>
      </button>
    </div>
   ` : ''}

`;






