# visualize_track.py 使用文档

## 一、简介

`visualize_track.py` 是 **WUTA-FSD** 赛道的可视化工具，用于读取 YAML 赛道文件并绘制锥筒分布、起点位置与朝向。

### 主要特性

| 特性 | 说明 |
|------|------|
| 📐 **自动缩放** | 根据赛道实际尺寸自动计算视图范围，从十几米的 skidpad 到数百米的 autocross 都能完美呈现 |
| 🖱️ **鼠标交互** | 滚轮缩放、左键拖拽平移、右键框选放大 |
| 📏 **自适应元素** | 起点箭头、文字偏移、锥筒点大小均随赛道尺寸自动调整 |
| 🏁 **多赛道支持** | 命令行参数或交互式菜单选择赛道文件 |
| 📏 **边界连线** | 可选 `--lines` 参数绘制锥筒间的连线，直观展示赛道边界走向 |
| 📊 **信息丰富** | 标题栏显示赛道类型、锥筒数量统计 |

---

## 二、环境要求

```bash
pip install pyyaml numpy matplotlib
```

conda 环境：

```bash
conda install pyyaml numpy matplotlib
```

---

## 三、使用方法

### 方式一：交互式选择赛道（推荐新手）

直接运行脚本不带参数，会弹出赛道文件列表：

```bash
python visualize_track.py
```

输出示例：

```
可用的赛道文件：
  [1] trackdrive.yaml
  [2] skidpad.yaml
  [3] eight_circle.yaml
  [4] skidpad0.yaml

请选择 (1-4): 
```

### 方式二：命令行指定赛道文件

直接传入文件名（支持相对路径和绝对路径）：

```bash
python visualize_track.py trackdrive.yaml
python visualize_track.py skidpad.yaml
python visualize_track.py eight_circle.yaml
python visualize_track.py /绝对/路径/到/赛道.yaml
```

### 方式三：绘制赛道边界连线

添加 `--lines` 参数，将同色锥筒按顺序连接，更直观地展示赛道形状：

```bash
python visualize_track.py --lines trackdrive.yaml
python visualize_track.py --lines skidpad0.yaml
```

### 方式四：查看帮助信息

```bash
python visualize_track.py --help
```

---

## 四、鼠标交互操作详解

matplotlib 内置导航工具栏提供完整的交互功能：

### 基本操作

| 操作 | 快捷键/鼠标 | 效果 |
|------|-------------|------|
| **缩放** | 滚动鼠标滚轮 | 以鼠标指针位置为中心放大/缩小 |
| **平移** | 按住左键拖拽 | 移动视图查看赛道不同区域 |
| **框选放大** | 按住右键拖拽绘制矩形 | 放大到选定区域 |
| **重置视图** | 点击工具栏 🏠 Home 按钮 | 回到初始全赛道视图 |
| **矩形缩放模式** | 点击工具栏 🔍 Zoom 按钮 | 进入矩形模式，左键拖拽框选放大 |
| **前后视图** | 点击工具栏 ← / → 按钮 | 在历史视图间前后切换 |
| **保存图片** | 点击工具栏 💾 保存按钮 | 将当前视图保存为 PNG/SVG/PDF |

### 提示

- 缩放操作以**鼠标指针位置**为锚点，方便对特定区域进行细节查看
- 平移和缩放支持无限次撤销/前进
- 窗口标题栏会显示当前操作提示

---

## 五、赛道文件说明

项目当前包含以下赛道文件：

### 5.1 trackdrive.yaml — Autocross 高速综合赛道

| 属性 | 值 |
|------|-----|
| 类型 | autocross |
| 尺寸 | 约 690m × 690m |
| 锥筒 | 蓝色 ~790 个 / 黄色 ~790 个 / 橙色 2 个 |
| 特点 | 单圈约 0.805km，包含直道、发夹弯、蛇形穿桩、复合弯道 |

> ⚠️ 由于锥筒数量众多（>1500个），初次渲染可能需等待 1~2 秒，建议使用 `--lines` 查看整体轮廓后再放大查看细节。

### 5.2 skidpad.yaml — Figure-8 8字绕环赛道

| 属性 | 值 |
|------|-----|
| 类型 | figure8 |
| 尺寸 | 约 40m × 40m |
| 锥筒 | 蓝色 30 个 / 黄色 48 个 / 橙色 2 个 |
| 特点 | 两圆心距 18.25m，内圈直径 15.25m，外圈直径 21.25m |

### 5.3 eight_circle.yaml — 8字绕环测试赛道

| 属性 | 值 |
|------|-----|
| 类型 | skidpad |
| 尺寸 | 约 40m × 40m |
| 锥筒 | 蓝色 34 个 / 黄色 26 个 / 橙色 1 个 |
| 特点 | 先跑右圆 2 圈（顺时针），再跑左圆 2 圈（逆时针） |

### 5.4 skidpad0.yaml — Skidpad 赛道

| 属性 | 值 |
|------|-----|
| 类型 | skidpad |
| 尺寸 | 约 16m × 30m |
| 锥筒 | 蓝色 0 个 / 黄色 0 个 / 橙色 36 个 |
| 特点 | 两圆半径各 9.125m，所有锥筒为橙色（不分蓝黄边界） |

---

## 六、输出说明

### 图表元素

| 元素 | 含义 |
|------|------|
| 🔵 蓝色三角 | 蓝锥筒 — 赛道左边界 / 内圈 |
| 🟡 黄色三角 | 黄锥筒 — 赛道右边界 / 外圈 / 减速标识 / 换向标识 |
| 🟠 橙色三角 | 橙锥筒 — 起止线 / 赛道标识 |
| ⭐ 红色星号 | 车辆起点位置 |
| → 红色箭头 | 车辆初始朝向（yaw 角） |

### 标题信息

标题栏显示：`WUTA-FSD — 赛道名 | 类型: xxx | 锥筒: 蓝N 黄N 橙N`

例如：
```
WUTA-FSD — trackdrive |  类型: autocross   |  锥筒: 蓝790 黄790 橙2
```

---

## 七、添加新的赛道文件

将新的 `.yaml` 文件放入 `tracks/` 目录，确保包含以下基本结构：

```yaml
track:
  type: <赛道类型>
  start_pose:
    x: <起点X坐标>
    y: <起点Y坐标>
    yaw: <起点朝向角>

  blue_cones:      # 左边界/内圈（可选）
    - [x, y, z]

  yellow_cones:    # 右边界/外圈（可选）
    - [x, y, z]

  orange_cones:    # 起止线/标识（可选）
    - [x, y, z]
```

锥筒坐标为 `[x, y, z]` 格式，单位米。脚本自动读取所有锥筒计算视图范围，无需额外配置。

---

## 八、常见问题

### Q: 鼠标滚轮缩放 / 左键拖拽平移不起作用？

这是最常见的问题，请按以下顺序排查：

#### 1️⃣ 确认运行方式（最常见原因）

**必须从系统终端运行，不要在 VS Code 内联终端或调试模式下运行。**

❌ **不推荐**（鼠标交互可能失效）：
- VS Code 右上角 ▶ 运行按钮
- VS Code 调试模式 (F5)
- VS Code 内联 Python 终端

✅ **推荐**（鼠标交互正常）：
```bash
# 先激活 conda 环境
conda activate TGAC_new

# 再运行脚本
cd C:\Users\g2909\Desktop\WUTA_sim\track_loader\src\simulation\wuta_simulator\tracks
python visualize_track.py skidpad.yaml
```

#### 2️⃣ 确认后端

脚本启动时会打印当前后端，正常应显示 `TkAgg`、`Qt5Agg` 等 GUI 后端：

```
加载赛道: skidpad.yaml
matplotlib 后端: TkAgg
```

如果显示 `Agg`，说明没有可用的 GUI 后端，需要安装：
```bash
# Tk 后端（Python 自带，通常已有）
# 如果缺失，安装 tk
conda install tk

# 或安装 Qt 后端
pip install PyQt5
```

#### 3️⃣ 确认工具栏可见

窗口底部应有一排工具栏按钮（Home、←、→、✥、🔍、💾）。
如果看不到工具栏，说明窗口太小或被隐藏，尝试：
- 拉大窗口
- 检查是否被其他窗口遮挡

#### 4️⃣ 操作确认

| 操作 | 正确方式 |
|------|----------|
| 缩放 | 在绘图区域**滚动鼠标滚轮**（不是拖动） |
| 平移 | **按住鼠标左键**不放，然后拖动 |
| 框选放大 | **按住鼠标右键**不放，拖出矩形区域 |
| 复位 | 点击工具栏 🏠 **Home** 按钮 |

---

### Q: 为什么 trackdrive 赛道显示为一团，看不清细节？

A: 因为 trackdrive 赛道达到 690m 级别，而锥筒只有几米间距。请使用**滚轮放大**感兴趣的区域，或使用**左键拖拽**移动到特定弯道查看。可以先使用 `--lines` 参数查看赛道全貌轮廓：

```bash
python visualize_track.py --lines trackdrive.yaml
```

### Q: 如何保存图片？

A: 点击 matplotlib 工具栏中的 💾 保存按钮，支持 PNG、SVG、PDF 等格式。

### Q: 可以比较两个赛道吗？

A: 当前版本一次只能显示一个赛道。如需比较，可打开两个终端分别运行，或修改脚本在同一个坐标系中叠加绘制。

### Q: 锥筒数量太多导致显示卡顿？

A: 对于 trackdrive 这类大型赛道，可以先不显示锥筒点（修改代码注释掉 scatter 调用），仅用 `--lines` 查看边界线，会流畅很多。

---

## 九、命令行参数速查

```
位置参数:
  yaml_file           赛道 YAML 文件路径（省略则交互式选择）

可选参数:
  --lines             绘制锥筒连线以显示赛道边界走向
  -h, --help          显示帮助信息并退出

示例:
  python visualize_track.py                              # 交互式选择
  python visualize_track.py trackdrive.yaml              # 显示指定赛道
  python visualize_track.py --lines skidpad.yaml         # 显示边界连线
```
