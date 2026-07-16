"""
WUTA-FSD 赛道可视化脚本 — 读取 YAML 赛道文件并绘制锥筒分布与原点信息

特性：
  - 自动根据赛道尺寸调整视图范围（含边距）
  - 支持鼠标滚轮缩放、左键拖拽平移（matplotlib 内置工具栏）
  - 支持命令行参数选择赛道文件，或交互式选择
  - 视觉元素（箭头、文字、点大小）随赛道尺寸自适应
  - 可选绘制锥筒连线以显示赛道边界走向

用法：
  python visualize_track.py                          # 交互式选择赛道
  python visualize_track.py trackdrive.yaml           # 指定赛道文件
  python visualize_track.py --lines eight_circle.yaml # 绘制边界连线
"""

import argparse
import os
import sys

import matplotlib  # noqa: E402

# —— 后端兼容性处理 ——
# 如果当前是非交互后端（Agg / PDF / SVG / PS），尝试切换到可用的 GUI 后端。
# 已经是交互后端（TkAgg / Qt5Agg / ...）则保持不动，避免破坏用户配置。
_interactive_backends = ("tkagg", "qt5agg", "qtagg", "gtk3agg",
                        "wxagg", "macosx", "nbagg", "webagg")
_cur = matplotlib.get_backend().lower()
if _cur not in _interactive_backends and not _cur.startswith("nb"):
    for _try in ("Qt5Agg", "QtAgg", "TkAgg"):
        try:
            matplotlib.use(_try, force=True)
            break
        except Exception:
            continue

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402

# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------

def load_track(yaml_path: str) -> dict:
    """加载 YAML 赛道文件。

    容错处理：部分赛道文件（如 eight_circle.yaml）在 `track:`
    之前包含非 YAML 的文档头（=== 分隔线 + 中文说明），
    这里自动剥离这些行，使解析器只看到合法的 YAML。
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = raw.splitlines()
    start = 0
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        # 跳过空行、=== 分隔线、以及不带冒号的中文说明行
        if not stripped:
            start = i + 1
            continue
        if stripped.startswith("=") or stripped.startswith("#"):
            start = i + 1
            continue
        if ":" in stripped and not stripped.startswith("-"):
            # 遇到第一个合法的 YAML 键，停止剥离
            break
        # 没有冒号的纯文本行 → 说明行，剥掉
        start = i + 1
    cleaned = "\n".join(lines[start:])

    data = yaml.safe_load(cleaned)

    if "track" not in data:
        raise ValueError(f"{yaml_path}: 缺少 'track' 顶层键（剥离后内容以 '{cleaned[:40]}' 开头）")

    return data


def collect_all_points(track_data: dict) -> np.ndarray:
    """收集所有锥筒 + 起点坐标，用于自动计算视图范围。"""
    track = track_data["track"]
    start = track["start_pose"]
    pts = [[start["x"], start["y"]]]
    for key in ("blue_cones", "yellow_cones", "orange_cones", "crossover_cones"):
        cones = track.get(key) or []
        for c in cones:
            pts.append(c[:2])
    return np.array(pts)


def compute_view_bounds(track_data: dict, padding_ratio: float = 0.08):
    """
    根据所有锥筒的包围盒计算视图范围。
    返回 (x_min, x_max, y_min, y_max, diag)，其中 diag 为对角线长度，
    用于自适应视觉元素大小。
    """
    pts = collect_all_points(track_data)
    if len(pts) < 2:
        return -10, 10, -10, 10, 20

    xy_min = pts.min(axis=0)
    xy_max = pts.max(axis=0)
    center = (xy_min + xy_max) / 2
    span = xy_max - xy_min
    diag = np.linalg.norm(span)

    # 以较长的一边为基准，加上边距，保证两个方向都不被压缩
    half = max(span) / 2 * (1 + padding_ratio)
    x_min, y_min = center - half
    x_max, y_max = center + half

    # 防止某方向跨度为 0（比如纯圆形赛道在某一轴上）
    if span[0] < 1e-3:
        x_min, x_max = center[0] - half, center[0] + half
    if span[1] < 1e-3:
        y_min, y_max = center[1] - half, center[1] + half

    return x_min, x_max, y_min, y_max, diag


# ---------------------------------------------------------------------------
# 绘图
# ---------------------------------------------------------------------------

def draw_boundary_lines(ax, cones, color, linewidth=0.8, alpha=0.4):
    """按顺序连接锥筒，绘制赛道边界线。"""
    if not cones or len(cones) < 2:
        return
    arr = np.array(cones)
    ax.plot(arr[:, 0], arr[:, 1], color=color,
            linewidth=linewidth, alpha=alpha, zorder=2)


def plot_track(track_data: dict, title: str = "WUTA-FSD Track",
               show_lines: bool = False) -> None:
    track = track_data["track"]
    start = track["start_pose"]

    # ---- 自适应参数 ----
    x_min, x_max, y_min, y_max, diag = compute_view_bounds(track_data)
    # 视觉元素按对角线长度的比例缩放
    arrow_len = diag * 0.04
    text_offset = diag * 0.015
    total_cones = (len(track.get("blue_cones", [])) +
                   len(track.get("yellow_cones", [])) +
                   len(track.get("orange_cones", [])) +
                   len(track.get("crossover_cones", [])))
    cone_size = max(8, min(60, 3000 / max(total_cones, 1)))

    # ---- 自适应画布尺寸 ----
    span_x = x_max - x_min
    span_y = y_max - y_min
    aspect = span_x / span_y if span_y > 0 else 1
    base = 10  # 长边基准英寸
    if aspect >= 1:
        fig_w, fig_h = base, base / aspect
    else:
        fig_w, fig_h = base * aspect, base
    fig_w = max(6, min(16, fig_w))
    fig_h = max(5, min(14, fig_h))

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # ---- 绘制锥筒 ----
    def draw_cones(cones, color, label, marker="^"):
        if not cones:
            return
        arr = np.array(cones)
        ax.scatter(arr[:, 0], arr[:, 1],
                   c=color, marker=marker, s=cone_size, edgecolors="k",
                   linewidths=0.5, label=label, zorder=3)

    blue = track.get("blue_cones", [])
    yellow = track.get("yellow_cones", [])
    orange = track.get("orange_cones", [])

    # 切点/交叉点锥桶（cross-cones 通常为单独一类，用不同标记突出显示）
    crossover = track.get("crossover_cones", [])
    if crossover:
        arr = np.array(crossover)
        ax.scatter(arr[:, 0], arr[:, 1],
                   c="#A020F0", marker="D", s=cone_size * 1.2,
                   edgecolors="k", linewidths=0.6,
                   label=f"切点/交叉锥筒 ({len(crossover)})", zorder=4)

    draw_cones(blue,    "#1E90FF", f"蓝锥筒 ({len(blue)})")
    draw_cones(yellow,  "#FFD700", f"黄锥筒 ({len(yellow)})")
    draw_cones(orange,  "#FF8C00", f"橙锥筒 ({len(orange)})")

    # 可选：绘制边界连线
    if show_lines:
        draw_boundary_lines(ax, blue,   "#1E90FF")
        draw_boundary_lines(ax, yellow, "#FFD700")

    # ---- 标注起点 ----
    ax.plot(start["x"], start["y"], "r*", markersize=14, label="起点", zorder=5)

    dx = arrow_len * np.cos(start["yaw"])
    dy = arrow_len * np.sin(start["yaw"])
    ax.annotate(
        "", xy=(start["x"] + dx, start["y"] + dy),
        xytext=(start["x"], start["y"]),
        arrowprops=dict(arrowstyle="->", color="red", lw=2),
        zorder=5,
    )
    ax.text(
        start["x"] + text_offset, start["y"] + text_offset,
        f"Start  ({start['x']:.2f}, {start['y']:.2f})  yaw={start['yaw']}°",
        color="red", fontsize=8,
    )

    # ---- 视图范围 ----
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")

    # ---- 图表美化 ----
    track_type = track.get("type", "unknown")
    n_xover = len(track.get("crossover_cones", []))
    cone_detail = f"蓝{len(blue)} 黄{len(yellow)} 橙{len(orange)}"
    if n_xover:
        cone_detail += f" 交叉{n_xover}"
    info = f"{title}   |  类型: {track_type}   |  锥筒: {cone_detail}"
    ax.set_title(info, fontsize=12, fontweight="bold")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.legend(loc="best", fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    # 窗口标题
    if fig.canvas.manager is not None:
        fig.canvas.manager.set_window_title(
            "WUTA-FSD Track Viewer  "
            "[滚轮缩放 | 左键拖拽平移 | 右键框选放大]"
        )

    # 确保工具栏可见（针对 Qt 后端；其他后端原生自带工具栏）
    toolbar = getattr(fig.canvas, "toolbar", None)
    if toolbar is not None:
        try:
            toolbar.setVisible(True)
            toolbar.update()
        except Exception:
            pass

    # 用 subplot_adjust 代替 tight_layout，避免挤压底部工具栏空间
    fig.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.08)

    # block=True 保证事件循环不被跳过，鼠标事件才能被持续处理
    plt.show(block=True)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def list_available_tracks(directory: str) -> list:
    """列出目录下所有 .yaml 赛道文件。"""
    return sorted(f for f in os.listdir(directory) if f.endswith(".yaml"))


def interactive_select(directory: str) -> str:
    """交互式选择赛道文件。"""
    files = list_available_tracks(directory)
    if not files:
        print("未找到任何 .yaml 赛道文件。")
        sys.exit(1)

    print("\n可用的赛道文件：")
    for i, f in enumerate(files, 1):
        print(f"  [{i}] {f}")
    print()

    while True:
        try:
            choice = input(f"请选择 (1-{len(files)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return os.path.join(directory, files[idx])
        except (ValueError, EOFError):
            pass
        print("输入无效，请重试。")


def main():
    parser = argparse.ArgumentParser(
        description="WUTA-FSD 赛道可视化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
鼠标交互说明：
  滚轮          — 以鼠标位置为中心缩放
  左键拖拽      — 平移视图
  右键拖拽      — 框选区域放大
  工具栏 Home    — 重置为全赛道视图
  工具栏 Zoom    — 矩形缩放模式
""",
    )
    parser.add_argument(
        "yaml_file", nargs="?",
        help="赛道 YAML 文件路径（省略则交互式选择）",
    )
    parser.add_argument(
        "--lines", action="store_true",
        help="绘制锥筒之间的连线以显示赛道边界走向",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if args.yaml_file:
        yaml_path = args.yaml_file
        if not os.path.isabs(yaml_path):
            yaml_path = os.path.join(script_dir, yaml_path)
    else:
        yaml_path = interactive_select(script_dir)

    if not os.path.isfile(yaml_path):
        print(f"文件不存在: {yaml_path}")
        sys.exit(1)

    print(f"加载赛道: {yaml_path}")
    # 打印当前后端，方便用户排查鼠标交互问题
    print(f"matplotlib 后端: {matplotlib.get_backend()}  "
          f"(若鼠标无法交互，请见 README_visualize_track 第 8 节)")
    data = load_track(yaml_path)
    track_name = os.path.splitext(os.path.basename(yaml_path))[0]
    plot_track(data, title=f"WUTA-FSD — {track_name}", show_lines=args.lines)


if __name__ == "__main__":
    main()
