import streamlit as st
import random, math, colorsys, io
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dreamy Purple Hearts", layout="centered")

# ---------------- 柔和梦幻紫色调 ----------------
def dreamy_purple_palette(k=12):
    """生成多层次梦幻紫调"""
    hues = np.linspace(0.70, 0.85, k)  # 蓝紫到粉紫
    colors = []
    for h in hues:
        s = random.uniform(0.25, 0.45)   # 柔和饱和度
        l = random.uniform(0.70, 0.85)   # 明亮度
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        colors.append((r, g, b))
    return colors

# ---------------- 爱心形状函数 ----------------
def heart(center=(0.5, 0.5), scale=0.12, rotation=0.0, points=300):
    t = np.linspace(0, 2*np.pi, points)
    x = 16 * (np.sin(t) ** 3)
    y = (13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t))
    m = max(np.max(np.abs(x)), np.max(np.abs(y)))
    x = x / m
    y = y / m
    c, s = math.cos(rotation), math.sin(rotation)
    xr = x * c - y * s
    yr = x * s + y * c
    X = center[0] + scale * xr
    Y = center[1] + scale * yr
    return X, Y

# ---------------- 生成梦幻紫色爱心海报 ----------------
def generate_poster(
    seed=42,
    n_hearts=18,
    size_min=0.08,
    size_max=0.18,
    alpha_min=0.25,
    alpha_max=0.55,
    bg_color="#EDE9F9",  # 淡淡的紫蓝背景
    add_title=True,
    title_text="Dreamy Purple Hearts",
    subtitle_text="Soft, Calm & Magical",
    rotate=True,
):
    random.seed(int(seed))
    np.random.seed(int(seed))

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis("off")

    # 背景颜色
    def hex_to_rgb01(hexstr):
        hexstr = hexstr.lstrip("#")
        return tuple(int(hexstr[i:i+2], 16)/255.0 for i in (0, 2, 4))
    ax.set_facecolor(hex_to_rgb01(bg_color))

    palette = dreamy_purple_palette(max(12, n_hearts))

    # 绘制爱心
    for _ in range(n_hearts):
        cx, cy = random.random(), random.random()
        scale = random.uniform(size_min, size_max)
        rot = random.uniform(-math.pi/8, math.pi/8) if rotate else 0.0
        x, y = heart(center=(cx, cy), scale=scale, rotation=rot)
        color = random.choice(palette)
        alpha = random.uniform(alpha_min, alpha_max)
        ax.fill(x, y, color=color, alpha=alpha)  # 无描边 edgecolor 默认去掉

    # 添加文字
    if add_title:
        ax.text(0.05, 0.95, title_text, fontsize=20, weight="bold", color="#513E78", transform=ax.transAxes)
        ax.text(0.05, 0.91, subtitle_text, fontsize=12, color="#6A5CA8", transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout(pad=0)
    return fig

# ---------------- Streamlit 交互区 ----------------
st.title("💜 Dreamy Purple Hearts Poster")
st.caption("Generate magical heart-shaped art with dreamy purple tones")

seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=10_000_000, value=42, step=1)
n_hearts = st.sidebar.slider("Number of Hearts", 4, 50, 18)
size_min, size_max = st.sidebar.slider("Heart Size Range", 0.04, 0.30, (0.08, 0.18))
alpha_min, alpha_max = st.sidebar.slider("Transparency Range", 0.10, 0.85, (0.25, 0.55))
bg_color = st.sidebar.color_picker("Background Color", value="#EDE9F9")
add_title = st.sidebar.checkbox("Show Title", value=True)
title_text = st.sidebar.text_input("Title", value="Dreamy Purple Hearts")
subtitle_text = st.sidebar.text_input("Subtitle", value="Soft, Calm & Magical")
rotate = st.sidebar.checkbox("Random Rotation", value=True)

fig = generate_poster(
    seed=seed,
    n_hearts=int(n_hearts),
    size_min=float(size_min),
    size_max=float(size_max),
    alpha_min=float(alpha_min),
    alpha_max=float(alpha_max),
    bg_color=bg_color,
    add_title=add_title,
    title_text=title_text,
    subtitle_text=subtitle_text,
    rotate=rotate
)
st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
st.download_button(
    "Download Poster as PNG",
    data=buf.getvalue(),
    file_name=f"dreamy_hearts_seed{int(seed)}.png",
    mime="image/png",
)
