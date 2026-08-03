# README 宠物预览图实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 README 的“预览”章节展示现有的角色立绘、动作图集和 16 向观察图。

**Architecture:** 不生成或修改图片，只通过仓库相对路径引用 `assets/` 中已有 PNG。角色立绘限制显示宽度，另外两张横向或图集图片按 README 内容宽度展示。

**Tech Stack:** GitHub Flavored Markdown、GitHub README HTML 图片标签、Git。

---

### Task 1: 插入并验证预览图

**Files:**
- Modify: `README.md`
- Verify: `assets/model-sheet.png`
- Verify: `assets/contact-sheet.png`
- Verify: `assets/look-directions.png`

- [x] **Step 1: 确认三张图片存在**

Run:

```powershell
Get-Item assets/model-sheet.png, assets/contact-sheet.png, assets/look-directions.png
```

Expected: 三个路径均存在，且文件长度大于 0。

- [x] **Step 2: 在“预览”章节插入图片**

在现有说明后加入：

```markdown
### 角色立绘

<p align="center">
  <img src="assets/model-sheet.png" alt="鹿乃 Codex 宠物角色立绘" width="360">
</p>

### 动作总览

![鹿乃 Codex 宠物动作总览](assets/contact-sheet.png)

### 16 向观察

![鹿乃 Codex 宠物 16 向观察预览](assets/look-directions.png)
```

- [x] **Step 3: 验证范围和 Markdown 路径**

Run:

```powershell
git diff --check
git diff -- README.md
```

Expected: 无空白错误；README 只在“预览”章节增加三个标题和三张图片引用。

- [x] **Step 4: 提交并同步**

```powershell
git add README.md docs/superpowers/plans/2026-08-04-readme-pet-previews.md
git commit -m "docs: add Kano pet previews"
git push origin main
```

Expected: 本地 `main`、`origin/main` 和 GitHub 远端 `main` 指向同一提交；`.playwright-cli/` 保持未跟踪。
