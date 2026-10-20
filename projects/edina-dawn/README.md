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

## portraits/ 目录规则

    portraits/<characterId>/avatar/           头像原图（PNG / 初版 WebP）
    portraits/<characterId>/avatar/thumbs/    头像缩略图（WebP）
    portraits/<characterId>/standee/          立绘原图
    portraits/<characterId>/standee/thumbs/   立绘缩略图（WebP）
    portraits/<characterId>/cg/               CG 图（当前全部为空，预留）
    portraits/<characterId>/previous/         淘汰图与批次总览，仅供回滚

- `<characterId>` 为 ASCII 小写 id，共 28 个：`beatrix` `cecilia` `celine` `clara`
  `dorothy` `edina` `elise` `eludi` `freya` `jack` `kael` `lilith` `livia` `lucius`
  `lumina` `merl` `mimi` `natasha` `ophelia` `roland` `sariel` `seraphina` `sylph`
  `sylvana` `tia` `victoria` `yuffie` `yulia`。
- **子目录名与文件名一律 ASCII**。中文只出现在 `README.md` 等说明文本里。
- 每个角色只有一个统一的 `previous/` 目录。

## 缩略图规格

缩略图统一放在 `portraits/<characterId>/<kind>/thumbs/`，文件名与原图同名（扩展名改 `.webp`）：

- 长边 768px、保持宽高比、**不放大、不裁切**（`fit: inside` + `withoutEnlargement`）
- WebP 质量 q88
- 生成命令：`sharp(src).resize({ width: 768, height: 768, fit: 'inside', withoutEnlargement: true }).webp({ quality: 88 })`

原图长边本身小于 768px 时保持原尺寸。本轮 107 张缩略图长边全部为 768px。

## 头像变体语义

`avatar/` 下有两种变体并存，**互不覆盖**：

| 文件 | 含义 |
|---|---|
| `initial-avatar.webp` | **初版头像**。原 `portraits/` 根目录那 28 张 WebP 收拢后的正式变体。 |
| `<characterId>.png` | **默认头像**。由原 `备用/<id>/avatar/` 搬入的定稿半身像 PNG 原图。 |
| 其它文件 | 备选头像（如 `chatgpt-20261018-halfbody.png`、`loli-recipe-20261020-portrait.png`、`alice-legacy.png`、`edina-avatar-closeup.png`）。 |

艾迪娜特别说明：`portraits/edina.webp` 是驾驶员选定的现行正式版，同时落在那 28 张初版之列。
按不覆盖原则，它移到 `portraits/edina/avatar/initial-avatar.webp`，
而 `备用/edina/avatar/edina.png` 移到 `portraits/edina/avatar/edina.png` 作为默认头像源，
两者并存，谁也没有覆盖谁；没有从 `_backup-备用-20261020/` 或任何候选目录另挑图替换艾迪娜素材。

## previous/ 语义

`previous/` 只放**淘汰图**，供回滚和查证用，不作为运行时素材：

- 各角色原 `previous/` 里的旧立绘（如 `standee-20261012.png`）
- 头像批次 2026-10-19 的编号总览图（`<批次号>-<角色>-<变体>-overview.jpg`）

## 备用/ 的定位

`备用/` 已降级为**入口/暂存区与批次记录目录**：只保留说明文档、选图复核记录、批次 README
和历史清单，不再存放任何图片，也不再作为运行时 URL 来源。详见 `备用/README.md`。

## 运行时 URL

素材真源是 `projects/edina-dawn/portraits/`，路径全 ASCII，raw URL 无需 percent-encoding：

    https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/portraits/<characterId>/<kind>/<file>

卡侧 URL 契约见卡工程 `reports/media-contract.json`（含每个变体的 url、thumbnailUrl、sha256、尺寸）。
本轮未执行 commit / push，线上可达性**未验证**。
