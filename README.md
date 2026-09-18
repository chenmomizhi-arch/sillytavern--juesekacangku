# SillyTavern Character Asset Repository

This repository is an image host for SillyTavern role-card projects.

## Layout

```text
projects/
  <project-id>/
    <version>/
      manifest.json
      prompts/
      portraits/
```

Each card project keeps its prompts, generated images, source notes, and version metadata in its own directory. Do not place assets for different card projects in the same version folder.

## URL policy

Use immutable commit-pinned URLs in cards. Do not bind cards to `main`, because a later update could silently replace an older image.

Example:

```text
https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/<commit>/projects/edina-dawn/v1.0.7/portraits/victoria.webp
```

The first Edina Dawn candidate release resolves to commit `0831babc8bb90f9f569f1c1095fd32b00d59984a` and is recorded in `projects/edina-dawn/v1.0.7/resolved-urls.json`. The complete 27-character worldbook release is under `projects/edina-dawn/v1.0.8/`.

## Content policy

This public repository is intended for non-explicit character portraits and development references. Explicit NSFW variants should use separate private storage.
