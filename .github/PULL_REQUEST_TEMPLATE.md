## What does this PR do?

<!-- One or two sentences. Link the issue it closes, if any. -->

Fixes #

## Type of change

- [ ] New tutorial
- [ ] Narrative written for an existing stub (`draft: true` → `false`)
- [ ] Fix to a migrated example
- [ ] Infrastructure (gallery, scripts, CI)
- [ ] Documentation

## Checklist

- [ ] `make validate` passes
- [ ] `make html-noplot` passes
- [ ] `pre-commit run --all-files` passes
- [ ] No dataset files committed
- [ ] If a copied example changed, the edit is recorded in `POST_MIGRATION_PATCHES` rather than
      applied by hand

## For a new or rewritten tutorial

- [ ] `metadata.yml` filled in; `kale_api` matches the actual imports
- [ ] Registered in `tutorial_catalog.yml`
- [ ] The narrative runs in under two minutes on CPU
- [ ] Any reduction from the full experiment is stated in the text, with the full command alongside
- [ ] `estimated_runtime` and `hardware` reflect a real run, not a guess
