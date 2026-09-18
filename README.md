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

## Content policy

This public repository is intended for non-explicit character portraits and development references. Explicit NSFW variants should use separate private storage.
