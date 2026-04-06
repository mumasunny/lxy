# xhs 视频下载工具

浏览器里填写小红书作品链接，通过本页请求本机 [XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader) 的 API（默认 `http://127.0.0.1:5556/xhs/detail`）解析或下载作品。

## 使用

1. 在 XHS-Downloader 目录执行：`python main.py api`（需 Python ≥ 3.12，按上游项目说明安装依赖）。
2. 在本目录执行：`python3 serve.py`
3. 浏览器打开终端提示的地址（默认 `http://127.0.0.1:8765/index.html`）。

`serve.py` 仅用于本地静态页面 + 转发请求，避免浏览器直连 5556 时的跨域问题。

## 说明

请遵守法律法规与平台规则，仅处理你有权访问的内容。下载文件保存位置由 XHS-Downloader 配置决定（一般为该项目的 `Volume/Download`）。
