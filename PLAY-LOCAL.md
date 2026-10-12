# 在本机运行《天下无主》v0.26.15 网页版

在线地址：https://gitvirgin.github.io/tianxia-wuzhu/

1. 完整解压 `TianxiaWuzhu-Web-v0.26.15.zip`，不要只提取 HTML。
2. 本机安装 Node.js 后，在 Windows 双击 `PLAY_BROWSER.cmd`。启动器仅监听本机，默认打开 `http://127.0.0.1:8791/`。
3. 其他系统可在解压目录运行 `node scripts/serve-web.mjs --root dist/browser --port 8791`，再用浏览器访问该地址。

如 8791 端口正在运行另一份游戏，启动器会明确提示，不会替换它。也可在 PowerShell 使用 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start-browser.ps1 -Port 8792` 启动另一个地址。

请在游戏“存档”页保存并下载备份。进度按浏览器和地址保存，本机地址与 GitHub Pages 不共享存档；换端口也不会自动带走旧进度。直接以文件方式打开 HTML 无法正常加载游戏。

浏览器须支持 WebGL2。此包是网页版，不含本次更新的原生 EXE 或 APK。
