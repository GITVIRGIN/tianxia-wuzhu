# 天下无主 0.16.0 — WebGL2 兼容与三端发布纠偏

本次修复针对 GitHub Pages 在缺少 WebGL2 的浏览器或内置网页容器中直接显示 Godot 英文硬错误的问题。

- 支持 WebGL2 的 Chrome、Edge、Firefox 继续直接进入完整 Godot 网页版。
- 缺少 WebGL2 或启动失败时改为中文兼容页，提供重新检测、在新标签打开、Windows 完整 ZIP 与 Android APK。
- Windows 下载入口只提供含 EXE 与 PCK 的完整 ZIP；必须完整解压后运行。
- 修正网页兼容审计脚本的 Windows PowerShell 5 兼容性、Windows 构建清单污染和 Pages 大文件属性误删。

验证范围：118 项自动测试；17 项网页壳静态完整性检查；真实浏览器正向游戏入口和强制负向兼容页；Windows 隔离目录完整 ZIP 自检；Android arm64 签名、包名与横屏清单复核。

Godot 4 网页版本身要求 WebGL2。本修复提供明确降级路径，不声称可在不支持 WebGL2 的浏览器中运行游戏。Android 尚未在实体 vivo X300 Pro 安装验证。本版本是可玩开发候选，不代表商业完成版。

冻结源指纹：`3E7ECA3C5BC8457953BAE7EE9C807BD3187384548383EF4A2BDF455400D3E783`