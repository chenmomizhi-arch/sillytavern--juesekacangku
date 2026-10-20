# 备用素材索引

> 本目录是替换素材与回滚区。卡片与图床运行时当前仍指向 `../portraits/`，本目录不会自动改变线上 URL。
> 2026-10-20 完成目录重组，旧的 `半身像/` `立绘/` `chatgpt-20261018/` `萝莉配方-20261020/` `头像批次-20261019/` 平铺结构已按角色重排。

## 目录结构

```
备用/
├─ <char>/                     28 个角色目录，char 见下表
│  ├─ avatar/                  半身像运行时素材（PNG 原图）
│  │  └─ thumbs/              对应缩略图（WebP）
│  ├─ standee/                 立绘运行时素材（PNG 原图）
│  │  └─ thumbs/              对应缩略图（WebP）
│  ├─ cg/                      CG 图占位目录，当前为空
│  ├─ previous/                被替换下来的旧立绘，仅供回滚
│  └─ records/                 该角色的选图复核文档（.md）
├─ _batch/                     批次证据目录，不进运行时
│  ├─ avatar-batch-20261019/
│  │  ├─ overviews/<char>/     编号总览图（JPG）
│  │  └─ README.md            批次说明
│  └─ chatgpt-20261018/
│     └─ README.md             批次说明
├─ MANIFEST.csv                当前清单，每个实际文件一行
├─ MANIFEST-history.csv        2026-10-19 旧版清单存档（45 行数据，含过期候选）
├─ README.md                   本文件
└─ 选图记录-20261019.md         选图过程记录
```

### 各目录边界

| 目录 | 边界 |
|---|---|
| `<char>/avatar/`、`<char>/standee/` | 运行时素材。头像用 `avatar/`，立绘用 `standee/`；同名文件按角色分开放，不再平铺。 |
| `<char>/cg/` | CG 图占位。当前 28 个角色目录均为空，等实际 CG 产出后直接放入。 |
| `<char>/previous/` | 回滚用旧立绘。**不进 catalog**，运行时不要引用。 |
| `<char>/records/` | 该角色的选图复核文档，仅供人读，不进运行时。 |
| `_batch/` | 批次证据（总览图、批次 README）。**不进运行时**，也不进角色目录。 |
| `<char>/<kind>/thumbs/` | 缩略图，长边 ≤512px 的 WebP，仅用于快速浏览，不能作为运行时素材。 |
| `MANIFEST.csv` | 当前清单；`MANIFEST-history.csv` 是重组前的旧版存档，仅供对照。 |

### 角色目录（28）

`victoria` `clara` `lumina` `merl` `cecilia` `beatrix` `yulia` `sylvana` `edina` `lilith`
`elise` `sariel` `sylph` `seraphina` `tia` `mimi` `kael` `lucius` `eludi` `freya`
`celine` `livia` `dorothy` `ophelia` `yuffie` `natasha` `roland` `jack`

## 文件数量

| 类别 | 数量 |
|---|---|
| 运行时素材（avatar 32 + standee 12 + previous 3） | 47 |
| 缩略图（avatar 32 + standee 12） | 44 |
| 复核文档 records | 14 |
| 总览图 overviews | 29 |
| 批次 README | 2 |
| 根目录文件 | 4 |
| 合计 | 140 |

`cg/` 目录 28 个，当前均为空（不含文件）。

## 远程 URL 规则

GitHub raw 的父目录名 `备用` 必须做 percent-encoding，`备` = `%E5%A4%87`，`用` = `%E7%94%A8`，
即 `备用` → `%E5%A4%87%E7%94%A8`。

```
https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/%E5%A4%87%E7%94%A8/<char>/<kind>/<file>
```

示例：

```
https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/%E5%A4%87%E7%94%A8/victoria/avatar/victoria.png
https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/%E5%A4%87%E7%94%A8/victoria/standee/victoria.png
https://raw.githubusercontent.com/chenmomizhi-arch/sillytavern--juesekacangku/main/projects/edina-dawn/%E5%A4%87%E7%94%A8/victoria/avatar/thumbs/victoria.webp
```

规则要点：

- 路径分隔符用 `/`，文件层不做其它转义。
- 角色目录名、文件名一律 ASCII，无需再编码；只有父目录 `备用` 需要编码。
- `previous/`、`records/`、`_batch/` 下的文件不作为运行时素材引用。
- 活动图床仍在 `projects/edina-dawn/portraits/`，其 URL 规则不变（`portraits/` 无需编码）。

## 上线状态

**尚未 push，线上可达性未验证。** 本次重组只在本地完成，没有执行 commit、push 或任何发布动作，
因此上面列出的 raw URL 目前无法确认线上可访问。若要启用，需要另行确认仓库授权后再 push，
并实测一条 URL 的 HTTP 状态。

## 查看与替换规则

1. 先查 `MANIFEST.csv`，不要递归打开全部原图。清单里每行都带 SHA-256、字节数、尺寸、来源路径和状态。
2. 需要视觉判断时，只看 `<char>/<kind>/thumbs/` 的缩略图（长边 ≤512px WebP），不要直接开原图。
3. 替换默认图时，先把旧图复制到 `<char>/previous/`，再复制新图并校验 SHA-256。
4. `_batch/` 与 `records/` 只作证据和复核用，未经明确指令不要提升为运行时素材。
5. 任何改动后同步更新 `MANIFEST.csv`，让清单与磁盘实际文件保持一致。

## 历史说明（重组前，保留备查）

- 2026-10-17 替换贝阿朵莉丝、克拉拉、塞西莉亚立绘，旧图备份在 `<char>/previous/`。
- 2026-10-18 ChatGPT 网页版产出维多利亚立绘、克拉拉半身像、露米娜半身像，现存于
  `victoria/standee/chatgpt-20261018-fullbody.png`、`clara/avatar/chatgpt-20261018-halfbody.png`、
  `lumina/avatar/chatgpt-20261018-halfbody.png`。
- 2026-10-19 头像批次选定 12 张，总览与复核记录见 `_batch/avatar-batch-20261019/` 与各角色 `records/`。
- 2026-10-20 萝莉配方产出艾迪娜半身像与立绘，现存于 `edina/avatar/loli-recipe-20261020-portrait.png`
  与 `edina/standee/loli-recipe-20261020-standee.png`。
- 2026-10-20 完成目录重组：92 条迁移清单三方 SHA-256 全通过，生成 44 张缩略图，
  重建 `MANIFEST.csv`（138 行数据），旧清单存为 `MANIFEST-history.csv`。
