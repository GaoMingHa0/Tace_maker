import math

W = 1.75
blue = []
yellow = []
orange = []

def ring(x, y, h):
    blue.append((x - W*math.sin(h), y + W*math.cos(h)))
    yellow.append((x + W*math.sin(h), y - W*math.cos(h)))

def straight(x0, y0, h, L, step=2.5):
    n = max(2, int(round(L/step)))
    for i in range(1, n+1):
        d = L*i/n
        ring(x0 + d*math.cos(h), y0 + d*math.sin(h), h)
    return x0 + L*math.cos(h), y0 + L*math.sin(h)

def arc(x0, y0, h, R, turn, deg, step=2.5):
    cx = x0 + turn*R*math.cos(h + math.pi/2)
    cy = y0 + turn*R*math.sin(h + math.pi/2)
    phi0 = math.atan2(y0 - cy, x0 - cx)
    A = math.radians(deg)
    n = max(2, int(round(R*A/step)))
    for i in range(1, n+1):
        f = i/n
        phi = phi0 + turn*f*A
        nx = cx + R*math.cos(phi); ny = cy + R*math.sin(phi)
        ring(nx, ny, h + turn*f*A)
    phi1 = phi0 + turn*A
    return cx + R*math.cos(phi1), cy + R*math.sin(phi1), h + turn*A

def slalom(x0, y0, h, n_pylons, spacing, lateral=2.5):
    xs, ys = x0, y0
    for i in range(n_pylons):
        xs = xs + spacing*math.cos(h)
        ys = ys + spacing*math.sin(h)
        s = lateral if i%2==0 else -lateral
        px = xs + s*(-math.sin(h)); py = ys + s*math.cos(h)
        blue.append((px - W*math.sin(h), py + W*math.cos(h)))
        yellow.append((px + W*math.sin(h), py - W*math.cos(h)))
    return xs, ys

def orange_line(x, y, h):
    orange.append((x - W*math.sin(h), y + W*math.cos(h)))
    orange.append((x + W*math.sin(h), y - W*math.cos(h)))

x, y, h = 0.0, 0.0, 0.0
orange_line(x, y, h)

x, y = straight(x, y, h, 42.0)                 # [1] east straight
x, y, h = arc(x, y, h, 25.0, -1, 90.0)         # [2] big sweeper R25 90 right
x, y = straight(x, y, h, 55.0)                 # [3] south straight
x, y, h = arc(x, y, h, 9.0, +1, 180.0)         # [4] hairpin R9 180 left
x, y = straight(x, y, h, 33.0)                 # [5] north straight
x, y, h = arc(x, y, h, 18.0, -1, 35.0)         # [6a] decreasing radius
x, y, h = arc(x, y, h, 10.0, -1, 35.0)         # [6b]
x, y, h = arc(x, y, h, 6.0, -1, 35.0)          # [6c]
x, y = straight(x, y, h, 50.0)                 # [7] west straight
x, y = slalom(x, y, h, 5, 12.19)               # [8] slalom 5 @12.19
x, y = straight(x, y, h, 20.0)                 # [9] short straight
x, y, h = arc(x, y, h, 15.0, +1, 60.0)         # [10] left sweeper R15
x, y = straight(x, y, h, 30.0)                 # [11] straight
x, y, h = arc(x, y, h, 16.0, -1, 40.0)         # [12a] shrinking right
x, y, h = arc(x, y, h, 9.0, -1, 45.0)          # [12b]
x, y = straight(x, y, h, 40.0)                 # [13]
orange_line(x, y, h)                            # finish

def fmt(t):
    return f"[{t[0]:.3f}, {t[1]:.3f}, 0.0]"

lines = []
lines.append("# ============================================================")
lines.append("# WUTA-FSD Autocross - High-Speed Avoidance Track")
lines.append("# Rules: straight<=60/45m; hairpin min R9m;")
lines.append("#        slalom spacing 7.62-12.19m; track width 3.5m")
lines.append("# Blue=left boundary, Yellow=right, Orange=start/finish")
lines.append("# ============================================================")
lines.append("track:")
lines.append("  type: autocross")
lines.append("  start_pose:")
lines.append("    x: 0.0")
lines.append("    y: 0.0")
lines.append("    yaw: 0.0")
lines.append("")
lines.append("  blue_cones:")
for p in blue:
    lines.append(f"    - {fmt(p)}")
lines.append("")
lines.append("  yellow_cones:")
for p in yellow:
    lines.append(f"    - {fmt(p)}")
lines.append("")
lines.append("  orange_cones:")
for p in orange:
    lines.append(f"    - {fmt(p)}")

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autocross_high_speed.yaml")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print("OK", out, "blue", len(blue), "yellow", len(yellow), "orange", len(orange))
