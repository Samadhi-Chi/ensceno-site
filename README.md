# Ensceno 支持网站

入境 / Ensceno 的中英文帮助与隐私政策，面向 GitHub Pages。网站仅包含可公开的产品说明和品牌图标，不包含 App 源码、私人媒体、服务器地址或审核凭据。

## 当前状态

2026-10-30：用户确认 `ensceno.app@outlook.com` 已注册，收信与发信均已验证正常，用作公开支持邮箱。验证依据为用户确认，本轮未代发邮件。公开主体为 SHENGJIE SUN，托管沿用免费 GitHub Pages 方案。中英文帮助和隐私页面已定稿并公开发布，正式构建启用邮件入口。

正式网址：https://samadhi-chi.github.io/ensceno-site/

独立公开仓库：https://github.com/Samadhi-Chi/ensceno-site 。GitHub Actions 部署通过；中英文帮助、隐私、样式和图标 6 个地址的匿名 HTTP 200 与发布内容校验通过，浏览器语言切换正常。App 源码仓库仍为私有。

## 本地查看

```sh
python3 tools/build.py
python3 tools/check.py
python3 -m http.server 56539 --bind 127.0.0.1 --directory dist
```

中文帮助：`/zh/`；英文帮助：`/en/`；隐私政策分别为 `/zh/privacy.html` 与 `/en/privacy.html`。根页面可选择语言。没有广告、访问统计、第三方字体、Cookie、网页表单或浏览器本地存储。

编辑 `content/zh.json` 和 `content/en.json` 时保持内容一致。共享样式位于 `assets/site.css`。页面不依赖 JavaScript，FAQ 使用浏览器原生 details 元素。

## GitHub Pages 发布

使用单独的公开仓库 `Samadhi-Chi/ensceno-site`，App 仓库继续私有。发布前核对真实邮箱与收发结果，然后更新 `site.json` 中三个邮箱验证状态；不得为了构建通过而跳过验证。网站地址改变时同步修改 `base_url` 和 404 页入口。

```sh
python3 tools/build.py --release
python3 tools/check.py
```

正式构建会移除预览提示并提供已验证的邮件链接。缺少注册或收发确认时，`--release` 会直接停止。将通过检查的 `dist/` 内容作为 Pages 发布目录，通过 `.github/workflows/pages.yml` 自动构建并部署；推送网站仓库的 main 或手动触发工作流即可发布。不要把本机 `.preview/`、邮箱注册截图、诊断文件或 App 仓库历史推送到公开仓库。

公开后检查四个语言页面均能匿名访问、语言切换和联系链接正确，再把最终支持与隐私网址写回 App 发布资料。邮箱注册、网站发布、App 内入口更新是分别核验的事项。
