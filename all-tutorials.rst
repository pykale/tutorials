:html_theme.sidebar_secondary.remove: true

All tutorials
=============

The full catalogue. Filter by domain, task, modality, difficulty, runtime and status; the result
count and URL update as you go, so a filtered view can be shared.

.. raw:: html

   <div id="pky-catalog" class="pky-catalog" data-src="_static/tutorials.json" data-sync-url="true">
     <div class="pky-catalog-controls">
       <div class="pky-search">
         <label for="pky-q" class="pky-visually-hidden">Search tutorials</label>
         <input id="pky-q" type="search" placeholder="Search tutorials…" autocomplete="off">
       </div>
       <div id="pky-facets" class="pky-facets" role="group" aria-label="Filters"></div>
       <button id="pky-clear" class="pky-btn pky-btn-ghost pky-clear" type="button">Clear filters</button>
     </div>
     <p id="pky-count" class="pky-count" role="status" aria-live="polite"></p>
     <div id="pky-grid" class="pky-grid"></div>
     <p id="pky-empty" class="pky-empty" hidden>No tutorials match these filters.</p>
     <noscript><p>Enable JavaScript to filter, or browse the domain pages.</p></noscript>
   </div>
