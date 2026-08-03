# README 宠物预览图设计

## 目标

在 README 的“预览”章节补充三张现有宠物图片，让访客能直接看到角色立绘、动作图集和 16 向观察方向。

## 范围

- 只修改 `README.md` 的预览章节。
- 只引用 `assets/model-sheet.png`、`assets/contact-sheet.png` 和 `assets/look-directions.png`。
- 保留用户现有文字、图片文件、运行包和宠物行为不变。

## 排版

- 角色立绘使用居中的 HTML 图片，宽度限制为 360px，避免竖图占满页面。
- 动作图集和 16 向图使用 GitHub README 的相对路径图片链接，按内容宽度展示。
- 每张图添加简短中文标题和中文替代文本。

## 验证

- 三个图片路径均存在且文件可读取。
- `README.md` 只新增预览图片标记和对应标题。
- `git diff --check` 通过。
