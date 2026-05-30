# 灰度相交互归纳工具

## 启动

在 PowerShell 中运行：

```powershell
& 'C:\Users\xbszl\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\xbszl\Documents\New project 3\phase_tool\server.py'
```

然后打开：

```text
http://127.0.0.1:8765
```

## 功能

- 上传 `.tif/.tiff/.png/.jpg/.bmp` 图片
- 点击图像采样灰度并创建/更新相
- 通过容差把相近灰度自动归纳到当前相
- 支持新增、删除、改名、改颜色、手动调整灰度上下限
- 支持灰度、叠加、纯分相三种显示模式
- 支持滚轮缩放、空格/中键/右键拖拽平移，便于精细选点
- 支持撤销采样、新增/删除相、自动阈值整理、相名称/颜色/阈值修改等操作
- 导出分相 PNG
- 导出每个相的单独分布图 PNG
- 导出灰度阈值和面积统计 CSV
- 导出工程 JSON，保留相名称、颜色、阈值和采样点

## 点击方式

- 普通点击：按当前笔刷半径取平均灰度，并按容差扩展当前相范围
- `Shift + 点击`：只采样单个像素点
- 鼠标滚轮：以鼠标位置为中心缩放图像
- 按住 `Space`、鼠标中键或右键拖拽：平移图像
- `Ctrl + Z`：撤销最近一次分相编辑
- “自动整理阈值”：按各相灰度中心自动整理相邻边界，减少重叠
