Getting started
===============

PyKale Tutorials are runnable scripts. You read the narrated version, then run the full experiment
when you want the real numbers. Here is the shortest path in.

Install PyKale
--------------

.. code-block:: bash

   pip install pykale

Datasets are never bundled — each tutorial downloads what it needs, or points at
`pykale/data <https://github.com/pykale/data>`_.

Run your first tutorial
-----------------------

The recommended starting point is :doc:`domain adaptation on digit images
</_gallery/others/image_classification/digit_domain_adaptation/plot_digit_domain_adaptation>`. It
trains a classifier on MNIST and adapts it to USPS without target labels — PyKale's core idea in a
few minutes on CPU.

.. code-block:: bash

   cd others/image_classification/digit_domain_adaptation
   pip install -r requirements.txt
   python main.py --cfg configs/MN2UP-DANN.yaml --devices 1

Explore a domain
----------------

Tutorials are filed by the domain that owns them:

.. grid:: 1 2 3 3
   :gutter: 2

   .. grid-item-card:: Protein
      :link: _pages/protein
      :link-type: doc

      Drug-target binding and polypharmacy side effects.

   .. grid-item-card:: Cancer
      :link: _pages/cancer
      :link-type: doc

      Multiomics integration for cancer classification.

   .. grid-item-card:: Cardiac
      :link: _pages/cardiac
      :link-type: doc

      Cardiac imaging and uncertainty estimation.

   .. grid-item-card:: Others
      :link: _pages/others
      :link-type: doc

      Method demonstrations: recognition, domain adaptation, few-shot learning.

   .. grid-item-card:: Materials
      :link: _pages/materials
      :link-type: doc

      Reserved — tutorials in development.

Adapt an example to your own data
---------------------------------

Every tutorial ships its complete ``main.py`` and config. Fork the folder, point
``DATASET.ROOT`` (or the equivalent config field) at your data, and adjust the model. See
:doc:`CONTRIBUTING` for conventions, and :doc:`all-tutorials` to browse everything.
