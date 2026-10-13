# Edina Dawn Card v1.2.9

Packaged SillyTavern artifacts for `圣女今天也很努力（大概）！`.

Card repository build revision: `af87b0f test(gates): 语义版本门禁 + 恒真断言重写 + v1.2.9 重建`.
Card repository documentation revision for this package: `e0de909 docs: 登记 mvu_zod 滚动依赖为已知残留`.

Lineage: v1.2.9 is the rebuilt formal artifact of the driver-accepted BP-048 batch 4 theme-refinement candidate `v1.2.8-BP048主题精修4` (driver acceptance recorded 2026-10-13). Portrait assets remain the stable v1.0.9 set under `projects/edina-dawn/portraits/` and are referenced by stable `main` URLs.

Files:

- `候补圣女今天也在好好努力（大概）v1.2.9.json`
- `候补圣女今天也在好好努力（大概）v1.2.9.png`
- `预览-v1.2.9-状态栏与开局页.html`
- `run-v1.2.9-2026-10-13T07-26-05-905Z.json`
- `rounds-v1.2.9.json`
- `real-host-v1.2.8-BP048主题精修4.json`
- `driver-acceptance-2026-10-13.md`

Validation (v1.2.9 build receipt, 0 failures):

- Static card checks `246/246`
- Variable mapping `979/979` across `14` groups
- Relation full update `9/9`
- Equipment and skill chain `14/14`
- Deterministic continuity rounds `29/29` over `5` rounds
- HUD checks `119/119`
- PNG round trip `8/8`
- Handoff document checks `25/25`
- Worldbook order: `214` maintained entries and `215` embedded entries
- Event-task fixture: `12` items, `0` failures

Real-host evidence boundary:

- The bundled real-host receipt covers the content baseline candidate `v1.2.8-BP048主题精修4`, not a fresh import of the v1.2.9 package.
- Receipt result: `79` checks, `78` PASS, `1` known FAIL, `panel-settings-theme-text` (`textPersisted=false`). This is not an all-green receipt, and the failed check has not been fixed or authorized for repair.
- The exact v1.2.9 packaged artifact has not been re-imported into SillyTavern for a fresh real-host run.

Artifact hashes:

- JSON SHA-256: `6C626A66B65958E2C109C8F4AAF38A8EFF391E28C5767CC63511637C142B7AD7`
- PNG SHA-256: `FB7ED9EC142A1BD1A75D444FBE4C4DBB203AD8D33319D25ADCE284A599DD8336`

Runtime dependency boundary:

- The MVU runtime bundle is pinned to `MagicalAstrogy/MagVarUpdate@dd4f1d92b450dc7eaa1b43e23b6e3fb832c909d1`.
- The schema helper `mvu_zod.js` currently imports `StageDog/tavern_resource/dist/util/mvu_zod.js` without a commit or tag pin. This upstream drift risk is recorded in the card project's `NEXT.md`; it was not changed in this package.

Distribution boundary:

- This package contains a heavy NSFW SillyTavern card. The repository's public content policy says explicit NSFW variants should use separate private storage.
- Push status at packaging time: local commit only; no remote push. Publishing this package to the public repository requires an explicit driver decision.
