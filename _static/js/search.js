/*
 * Keyboard handling for the navbar search field (search-field.html).
 *
 * The navbar now uses a real <input> (not the modal-opening button), so clicking it focuses it and
 * typing works natively. This binds Ctrl+K / Cmd+K to focus that same input (in the capture phase,
 * so it wins over the theme's default "open the search modal" handler) and Escape to blur it.
 * Enter submits to the local Sphinx search page via the form's own action.
 */
(function () {
  "use strict";

  function navbarSearchInput() {
    var form = document.querySelector(".navbar-header-items .bd-search, .navbar-persistent--container .bd-search, header .bd-search");
    return form ? form.querySelector("input[type='search']") : null;
  }

  document.addEventListener(
    "keydown",
    function (e) {
      var isK = (e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K");
      if (isK) {
        var input = navbarSearchInput();
        if (input) {
          e.preventDefault();
          e.stopImmediatePropagation(); // block the theme's modal
          input.focus();
          input.select();
        }
      } else if (e.key === "Escape") {
        var active = document.activeElement;
        if (active && active.matches && active.matches(".bd-search input")) {
          active.blur();
        }
      }
    },
    true // capture phase
  );
})();
