/* Click a figure to read it full size.
 *
 * Any <img data-zoomable> opens in an overlay. If the image has a data-full
 * attribute it is used as the large source, so the page can ship a small
 * thumbnail and only fetch the readable version on demand.
 *
 * No dependencies; progressive enhancement -- with JS off the figures are
 * still visible inline, just not enlargeable.
 */
(function () {
  "use strict";

  var overlay = null;
  var lastFocused = null;

  function close() {
    if (!overlay) return;
    overlay.remove();
    overlay = null;
    document.body.classList.remove("lightbox-open");
    document.removeEventListener("keydown", onKeydown);
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  function onKeydown(e) {
    if (e.key === "Escape") close();
  }

  function open(img) {
    close();
    lastFocused = document.activeElement;

    overlay = document.createElement("figure");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", img.alt || "Figure");
    overlay.style.margin = "0";

    var button = document.createElement("button");
    button.className = "lightbox-close";
    button.type = "button";
    button.setAttribute("aria-label", "Close");
    button.innerHTML = "&times;";

    var big = document.createElement("img");
    big.src = img.getAttribute("data-full") || img.currentSrc || img.src;
    big.alt = img.alt || "";

    overlay.appendChild(button);
    overlay.appendChild(big);

    if (img.alt) {
      var caption = document.createElement("figcaption");
      caption.textContent = img.alt;
      overlay.appendChild(caption);
    }

    // click anywhere except the image itself closes
    overlay.addEventListener("click", function (e) {
      if (e.target !== big) close();
    });

    document.body.appendChild(overlay);
    document.body.classList.add("lightbox-open");
    document.addEventListener("keydown", onKeydown);
    button.focus();
  }

  document.addEventListener("click", function (e) {
    var img = e.target.closest && e.target.closest("img[data-zoomable]");
    if (!img) return;
    e.preventDefault();
    open(img);
  });

  // keyboard: figures are focusable via tabindex, Enter/Space opens
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var el = document.activeElement;
    if (el && el.matches && el.matches("img[data-zoomable]")) {
      e.preventDefault();
      open(el);
    }
  });
})();
