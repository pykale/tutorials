Learn with PyKale
=================

.. raw:: html

   <section class="pky-hero" aria-label="Introduction">
     <div class="pky-hero-inner">
       <div class="pky-hero-copy">
         <p class="pky-eyebrow">PyKale Tutorials</p>
         <p class="pky-hero-title">Learn with PyKale</p>
         <p class="pky-hero-lead">
           Runnable, reproducible tutorials for multimodal learning, transfer learning and
           interdisciplinary AI — organised by the domain that owns them.
         </p>
         <div class="pky-hero-cta">
           <a class="pky-btn pky-btn-primary" href="pages/getting-started.html">Start learning</a>
           <a class="pky-btn pky-btn-ghost" href="pages/all-tutorials.html">Browse tutorials</a>
           <a class="pky-btn pky-btn-ghost" href="https://github.com/pykale/tutorials"
              target="_blank" rel="noopener">View on GitHub ↗</a>
         </div>
       </div>
       <div class="pky-hero-art" aria-hidden="true">
         <svg viewBox="0 0 320 240" xmlns="http://www.w3.org/2000/svg" role="presentation">
           <g fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55">
             <line x1="60" y1="60" x2="160" y2="40"/><line x1="160" y1="40" x2="250" y2="90"/>
             <line x1="250" y1="90" x2="200" y2="170"/><line x1="200" y1="170" x2="90" y2="180"/>
             <line x1="90" y1="180" x2="60" y2="60"/><line x1="60" y1="60" x2="200" y2="170"/>
             <line x1="160" y1="40" x2="200" y2="170"/><line x1="90" y1="180" x2="250" y2="90"/>
           </g>
           <g fill="currentColor">
             <circle cx="60" cy="60" r="9"/><circle cx="160" cy="40" r="9"/>
             <circle cx="250" cy="90" r="9"/><circle cx="200" cy="170" r="9"/>
             <circle cx="90" cy="180" r="9"/>
           </g>
         </svg>
       </div>
     </div>
   </section>

.. raw:: html

   <div class="pky-home-overview">

Get started
-----------

.. container:: pky-start-steps

   1. **Install PyKale.** Run ``pip install pykale``. :doc:`Setup guide <pages/getting-started>`
   2. **Try the first tutorial.** :doc:`Domain adaptation on digit images
      </_gallery/others/image_classification/digit_domain_adaptation/plot_digit_domain_adaptation>`
      is the recommended starting point.
   3. **Find your next topic.** :doc:`Browse all tutorials <pages/all-tutorials>` or
      :doc:`follow a learning path <pages/learning-paths>`.

What's new
----------

.. include:: _generated/news.rst

.. raw:: html

   </div>

Featured learning paths
-----------------------

Choose a route, then follow its tutorials in order.

.. include:: _generated/featured_paths.rst

Browse all tutorials
--------------------

Filter the full catalogue by domain, task, modality, difficulty, runtime and status.

.. raw:: html

   <div id="pky-catalog" class="pky-catalog" data-home data-src="_static/tutorials.json">
     <div class="pky-catalog-controls">
       <div class="pky-search">
         <label for="pky-q" class="pky-visually-hidden">Search tutorials</label>
         <input id="pky-q" type="search" placeholder="Search tutorials…" autocomplete="off">
       </div>
       <details class="pky-filter-details" open>
         <summary id="pky-filter-summary">Filters</summary>
         <div id="pky-facets" class="pky-facets" role="group" aria-label="Filters"></div>
       </details>
       <button id="pky-clear" class="pky-btn pky-btn-ghost pky-clear" type="button">Clear filters</button>
     </div>
     <p id="pky-count" class="pky-count" role="status" aria-live="polite"></p>
     <div id="pky-grid" class="pky-grid"></div>
     <p id="pky-empty" class="pky-empty" hidden>No tutorials match these filters.</p>
     <noscript>
       <p>Enable JavaScript to filter, or use the Domains menu to browse tutorials.</p>
     </noscript>
   </div>

Contributing
------------

.. grid:: 1 2 2 4
   :gutter: 3
   :class-container: pky-contributing

   .. grid-item-card:: Add a tutorial
      :link: CONTRIBUTING
      :link-type: doc

      Start from the templates in ``source/_shared/templates/``.

   .. grid-item-card:: Improve one
      :link: pages/tutorial-status
      :link-type: doc

      See which narratives are still drafts and pick one to write.

   .. grid-item-card:: Report an issue
      :link: https://github.com/pykale/tutorials/issues

      Something wrong or unclear? Open an issue.

   .. grid-item-card:: Read the guide
      :link: CONTRIBUTING
      :link-type: doc

      The full contribution workflow and conventions.

.. toctree::
   :hidden:

   pages/getting-started
   pages/all-tutorials
   pages/learning-paths
   pages/tutorial-status
   pages/about

.. toctree::
   :caption: Domains
   :hidden:

   _pages/protein
   _pages/cancer
   _pages/cardiac
   _pages/materials
   _pages/others

.. toctree::
   :caption: Project
   :hidden:

   CONTRIBUTING
