# SillyTavern Card and Asset Repository

This repository stores SillyTavern role-card projects, their current portrait assets, archived iterations, prompts, manifests, and release packages.

## Layout

```text
projects/
  <project-id>/
    README.md
    manifest.json
    resolved-urls.json
    portraits/               # current active portraits
    prompts/                 # current maintained prompts
    cards/                    # released card packages
      <version>/
    archive/                 # retired versions and discarded iterations
      <version>/
```

Do not create a new active image directory for every card revision. Update the current portrait in place and move the retired image or discarded iteration into `archive/`.

## URL policy

Cards use stable `main` paths for current portrait assets:

```text
https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/portraits/victoria.webp
```

Retired assets remain recoverable under the project archive, but are not used as active card dependencies unless a rollback is explicitly requested.

## Content policy

This public repository is intended for non-explicit character portraits and development references. Explicit NSFW variants should use separate private storage.
