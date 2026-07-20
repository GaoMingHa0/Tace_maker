# Track_maker

一个用于 **Formula Student 赛道制作与查看** 的轻量工具集。

## 包含内容

- `track_builder.html`：浏览器内交互式赛道编辑器（无需安装）
- `visualize_track.py`：读取 YAML 赛道并可视化锥桶与起点朝向
- `_build_autocross.py`：生成一份 autocross 示例赛道
- `_serve.js`：本地静态服务脚本（可选）

## 快速开始

### 1) 赛道编辑

直接打开：

```bash
track_builder.html
```

或本地起服务后访问 `http://localhost:8765`：

```bash
node _serve.js
```

### 2) 赛道可视化

安装依赖：

```bash
pip install pyyaml numpy matplotlib
```

运行：

```bash
python visualize_track.py <track.yaml>
python visualize_track.py --lines <track.yaml>
```

## 说明

- 赛道数据格式为 YAML（含 `track`、`start_pose`、各类 cones）
- 更详细说明见：
  - `README_TrackBuilder.md`
  - `README_visualize_track.md`
