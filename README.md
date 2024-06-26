# 环境

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

推荐使用清华源

# 说明

本项目基于PySide6和YOLOv8设计了一个简单的交通标志检测系统，美化时使用了qfluentwidgets（[b站教程](https://www.bilibili.com/video/BV1o94y1a7Yv/?spm_id_from=333.337.search-card.all.click&amp;vd_source=6f3196e1b0bd3d5cbbd607c6d661275f )  [官网地址](https://qfluentwidgets.com/zh/)），使用的数据集为处理后的TT100K2021（[官网地址](https://cg.cs.tsinghua.edu.cn/traffic-sign/)），处理中用到的筛选类别的方法见[这篇博文](https://blog.csdn.net/m0_63774211/article/details/132941991)，处理后得到45类交通标志，可在main.py中查看相应类名

系统支持选择图片、视频以及摄像头进行检测，图片和视频的默认文件夹为picture和video

可在resources中放入自己想要的logo

# 演示

见[b站演示视频](https://www.bilibili.com/video/BV1R4421S7bh/?vd_source=6f3196e1b0bd3d5cbbd607c6d661275f)
