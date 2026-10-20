# 备用区（入口 / 暂存 / 批次记录）

> **本目录不再是运行时 URL 来源。**
> 2026-10-21 素材树重整后，所有图片已移入 `../portraits/` 对应位置，本目录不再存放任何图片文件。
> 运行时素材真源只有 `../portraits/`。

## 目录结构

    备用/
    ├─ <char>/records/              该角色的选图复核文档（.md，14 份）
    ├─ _batch/                      批次说明文档
    │  ├─ avatar-batch-20261019/README.md
    │  └─ chatgpt-20261018/README.md
    ├─ 萝莉配方复现-20261021/       配方批次记录（README.md 说明图片去处）
    ├─ MANIFEST.csv                 当前清单（逐文件 sha256 / bytes / 尺寸 / 新路径）
    ├─ MANIFEST-history.csv         2026-10-19 旧版清单存档
    ├─ README.md                    本文件
    └─ 选图记录-20261019.md          选图过程记录

## 各目录边界

| 目录 | 边界 |
|---|---|
| `<char>/records/` | 选图复核文档，仅供人读。**不进运行时**。 |
| `_batch/` | 批次说明。**不进运行时**。 |
| `萝莉配方复现-20261021/` | 配方复现批次记录，说明其图片已归入 `../portraits/edina/`。 |
| `MANIFEST.csv` | 当前清单，路径已指向 `../portraits/` 新结构。 |
| `MANIFEST-history.csv` | 重组前的旧版清单存档，仅供对照。 |

## 查看与替换规则

1. 先查 `MANIFEST.csv` 与 `../manifest.json`，不要递归打开全部原图。
2. 需要视觉判断时，看 `../portraits/<char>/<kind>/thumbs/`（长边 768px WebP）。
3. 替换默认图时，先把旧图复制到 `../portraits/<char>/previous/`，再放入新图并校验 SHA-256。
4. 任何改动后同步更新 `../manifest.json` 与本目录 `MANIFEST.csv`，让清单与磁盘实际文件保持一致。

## 历史说明

- 2026-10-17 替换贝阿朵莉丝、克拉拉、塞西莉亚立绘，旧图备份进各角色 `previous/`。
- 2026-10-18 ChatGPT 网页版产出维多利亚立绘、克拉拉半身像、露米娜半身像，
  现存于 `../portraits/victoria/standee/chatgpt-20261018-fullbody.png`、
  `../portraits/clara/avatar/chatgpt-20261018-halfbody.png`、
  `../portraits/lumina/avatar/chatgpt-20261018-halfbody.png`。
- 2026-10-19 头像批次选定 12 张，总览图进各角色 `previous/`，复核记录留在本目录 `records/`。
- 2026-10-20 萝莉配方产出艾迪娜半身像与立绘，现存于
  `../portraits/edina/avatar/loli-recipe-20261020-portrait.png` 与
  `../portraits/edina/standee/loli-recipe-20261020-standee.png`。
- 2026-10-21 完成素材树重整：28 张初版头像进 `avatar/initial-avatar.webp`，
  44 张 512px 旧缩略图重生成成 768px，29 张批次总览图按角色归入 `previous/`，
  旧备份 `_backup-备用-20261020/` 移出项目到
  `图床仓库/_archive-snapshot/edina-dawn-2026-10-21/retired/`。
