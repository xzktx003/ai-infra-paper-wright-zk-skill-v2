# 宣传材料

后摩论文科研研究 Skill 的小红书材料。主线是：确认写作逻辑，套模板，粗看 ICLR / ICML / NeurIPS 的起笔，把学术品味收成四层检查，再把验证过的 idea 流水线铺成带标记的完整初稿。

不是新的大模型，不跑实验，不保证录用。手册、模板、语料和脚本都在仓库里，可以直接看。

## 小红书

| 文件 | 用途 |
| --- | --- |
| `xiaohongshu/后摩论文科研研究Skill-写作流水线-小红书.mp4` | 竖屏 1080×1920，配音加烧录字幕，约 1–3 分钟 |
| `xiaohongshu/封面.png` | 3:4 封面，可作笔记首图 |
| `xiaohongshu/文案.md` | 复制到小红书正文 |
| `xiaohongshu/口播稿.md` | 视频里实际说的话 |
| `xiaohongshu/字幕.srt` | 与成片对齐的字幕 |

重做画面或配音：

```bash
python3 xiaohongshu/build_video.py --preview
python3 xiaohongshu/build_video.py --cues
python3 xiaohongshu/build_video.py
```

配音是 `zh-CN-XiaoxiaoNeural`，默认语速 `-2%`。中文字体在首次运行时从 Debian 镜像下载 Noto Sans CJK，不纳入版本库。
