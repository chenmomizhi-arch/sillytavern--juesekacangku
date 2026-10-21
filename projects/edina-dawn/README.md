# Edina Dawn

Source project: `圣女今天也很努力（大概）！`

自 2026-10-21 起，本目录是**一棵以 `portraits/` 为唯一运行时素材来源的正式素材树**。
目录根下只保留三个目录和三个说明文件：

    projects/edina-dawn/
    ├─ portraits/          唯一运行时素材来源（按角色分目录）
    ├─ prompts/            提示词与生成记录
    ├─ 备用/               入口/暂存区与批次记录，不再是运行时 URL 来源
    ├─ manifest.json       素材清单（逐文件 sha256 / bytes / 尺寸 / 缩略图路径）
    ├─ resolved-urls.json  运行时 URL 解析表
    └─ README.md           本文件

已退役并删除的目录：`archive/`、`cards/`、`v1.0.8/`、`v1.0.9/`。
删除前的完整快照在仓库外归档目录
`图床仓库/_archive-snapshot/edina-dawn-2026-10-21/`，逐文件 SHA-256 记录于其 `manifest.json`，
可整体回滚。

## portraits/ 目录规则（2026-10-21 起，`edina` 为参考实现）

    portraits/<characterId>/
    ├─ avatar/                     运行时头像与立绘（编号变体）
    │  ├─ <id>-1.png               头像（默认，always）
    │  ├─ <id>-2.png               立绘（默认，always）
    │  ├─ <id>-3.png               初版立绘（好感 ≥ 20 解锁）
    │  ├─ <id>-N.png               其他运行时变体
    │  └─ thumbs/<同名>.webp       缩略图
    ├─ cg/                         事件 CG（运行时）
    │  ├─ <id>-<事件名>.png        例：edina-好奇.png
    │  └─ thumbs/<同名>.webp       缩略图
    ├─ previous/                   淘汰下来、不再使用的正式图片（仅供回滚）
    │  └─ thumbs/<同名>.webp
    └─ standee/                    已定稿但尚未投入正式使用的图片（暂存）
       └─ thumbs/<同名>.webp

### 硬性规则

1. **`avatar/` 是运行时头像与立绘的唯一来源。** 编号语义固定：
   - `<id>-1.png` = 头像（默认变体，`unlock: always`）
   - `<id>-2.png` = 立绘（默认变体，`unlock: always`）
   - `<id>-3.png` = 初版立绘（`unlock: affinity, minAffinity: 20`）
   - 更高编号按需追加，必须在 `manifest.json` 与 `media-contract.json` 写明 label / unlock。
2. **`cg/` 是事件 CG 的唯一来源。** 命名格式 `<id>-<事件名>.png`（如 `edina-好奇.png`）；
   事件名可用中文，但 `portraits/<id>/` 前缀必须是 ASCII 小写 `<id>`。
   事件 CG 由剧情状态推送，默认 `unlock: { type: "event", eventId: "<id>-<事件名>" }`。
3. **`previous/` 只放淘汰下来、不再使用的正式图片。** 禁止放总览图、批次截图、缩略图或未使用候选；
   这些应放 `备用/` 或 `standee/`（见下）。
4. **`standee/` 只放已定稿但尚未投入正式使用的图片。** **禁止从此处推送任何图片到玩家角色卡或运行时 URL。**
   一旦某张图投入正式使用，应移入 `avatar/`（立绘）或 `cg/`（事件 CG），不要留在 `standee/`。
5. **缩略图**统一放对应 kind 的 `thumbs/`，文件名与原图同名（扩展名改 `.webp`）：
   长边 768px、WebP q88、保持宽高比、不放大、不裁切（`fit: inside` + `withoutEnlargement`）。
6. **运行时 URL 只允许指向 `avatar/` 与 `cg/`。** 禁止指向 `standee/`、`previous/`、`备用/`。
7. 新增角色或迁移旧角色时，按本规则重建；旧结构（`<id>.png` / `initial-avatar.webp` / `standee/<id>.png`）
   迁移完成后删除。迁移前旧角色仍按旧结构工作，但**新图不得再写入旧结构**。
8. 每次改动后更新 `manifest.json` 与卡工程 `reports/media-contract.json`，
   并跑 `node tools/verify-media-catalog.mjs`；缩略图必须重新生成，不得复用旧 thumbs。

### 新旧命名对照

| 旧结构 | 新结构 |
| --- | --- |
| `avatar/<id>.png` | `avatar/<id>-1.png` |
| `avatar/initial-avatar.webp` | `avatar/<id>-3.png`（初版立绘，好感 ≥ 20） |
| `standee/<id>.png` | `avatar/<id>-2.png`（默认立绘） |
| `standee/<其它>.png` | `standee/<其它>.png`（只暂存，禁止运行时） |
| `previous/<批次>-overview.jpg` | `previous/<旧正式图>.png`（禁止总览图） |
| `cg/`（空） | `cg/<id>-<事件名>.png` |

## 当前参考实现：`portraits/edina/`

    portraits/edina/
    ├─ avatar/
    │  ├─ edina-1.png            头像，always
    │  ├─ edina-2.png            立绘，always
    │  ├─ edina-3.png            初版立绘，好感 ≥ 20
    │  └─ thumbs/edina-1.webp / edina-2.webp / edina-3.webp
    ├─ cg/
    │  ├─ edina-好奇.png         事件 CG（剧情状态推送）
    │  └─ thumbs/edina-好奇.webp
    ├─ previous/                 淘汰正式图（当前待清理旧 thumb）
    └─ standee/                  已定稿未使用（禁止运行时）

## 缩略图规格

- 长边 768px、保持宽高比、**不放大、不裁切**（`fit: inside` + `withoutEnlargement`）
- WebP 质量 q88
- 生成命令：
  ```js
  sharp(src).resize({ width: 768, height: 768, fit: 'inside', withoutEnlargement: true }).webp({ quality: 88 })
  ```

## 运行时 URL

素材真源是 `projects/edina-dawn/portraits/`，`<characterId>` 与编号文件名均为 ASCII：

    https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/portraits/<characterId>/avatar/<id>-<n>.png
    https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/portraits/<characterId>/cg/<id>-<事件名>.png

卡侧 URL 契约见卡工程 `reports/media-contract.json`（含每个变体的 url、thumbnailUrl、sha256、尺寸）。
线上可达性以推送后 HEAD 校验为准。

## 禁止事项（给后续模型）

- 禁止从 `standee/` 推送任何图片到玩家角色卡。
- 禁止把 `previous/` 当候选仓库；它只放淘汰正式图。
- 禁止复用旧 thumbs；原图改名/改内容后必须重新生成缩略图。
- 禁止把事件 CG 命名成 `<id>.png` 或塞进 `avatar/`；事件 CG 必须在 `cg/<id>-<事件名>.png`。
- 禁止让运行时 URL 指向 `备用/`、`standee/`、`previous/`。
