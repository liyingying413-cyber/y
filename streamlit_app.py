import streamlit as st
import random, math, colorsys, io
import numpy as np
import matplotlib.pyplot as plt

# ---------------- 页面配置 ----------------
st.set_page_config(page_title="Generative Hearts Poster", layout="centered")

# ---------------- 工具函数：柔和配色 ----------------
def pastel_palette(k=12, mood="spring", custom_hue=0.55, hue_spread=0.10,
                   s_range=(0.25, 0.45), l_range=(0.72, 0.88)):
    """使用 HLS 生成柔和清新配色（低到中等饱和度、高亮度）"""
    colors = []
    if mood == "spring":
        base_hues = [0.96, 0.03, 0.38, 0.55]  # 粉、红、薄荷、淡蓝
    elif mood == "sky":
        base_hues = [0.58, 0.66, 0.73, 0.80]  # 蓝、长春花、薰衣草
    elif mood == "peach":
        base_hues = [0.02, 0.06, 0.10, 0.14]  # 桃、杏、珊瑚
    else:  # custom
        base_hues = [custom_hue]

    for i in range(k):
        h = random.choice(base_hues) + random.uniform(-hue_spread, hue_spread)
        h = h % 1.0
        s = random.uniform(*s_range)
        l = random.uniform(*l_range)
        r, g, b = colorsys.hls_to_rgb(h, l, s)  # 注意顺序: HLS
        colors.append((r, g, b))
    return colors

# ---------------- 爱心路径 ----------------
def heart(center=(0.5, 0.5), scale=0.12, rotation=0.0, points=300):
    """
    经典心形参数曲线：
    x = 16 sin^3 t
    y = 13 cos t - 5 cos 2t - 2 cos 3t - cos 4t
    做归一化 → 旋转 → 平移
    """
    t = np.linspace(0, 2*np.pi, points)
    x = 16 * (np.sin(t) ** 3)
    y = (13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t))

    # 归一化到 [-1,1] 以内
    m = max(np.max(np.abs(x)), np.max(np.abs(y)))
    x = x / m
    y = y / m

    # 旋转
    c, s = math.cos(rotation), math.sin(rotation)
    xr = x * c - y * s
    yr = x * s + y * c

    # 缩放 & 平移到中心
    X = center[0] + scale * xr
    Y = center[1] + scale * yr
    return X, Y

# ---------------- 海报生成 ----------------
def generate_poster(
    seed=42,
    mood="spring",
    custom_hue=0.55,
    hue_spread=0.10,
    n_hearts=14,
    size_min=0.08,
    size_max=0.18,
    alpha_min=0.25,
    alpha_max=0.55,
    bg_color="#FAFAF7",
    add_title=True,
    title_text="Generative Hearts",
    subtitle_text="Soft & Fresh Palette",
    rotate=True,
    add_shadow=True,
    shadow_offset=(0.008, -0.008),
    shadow_alpha=0.10
):
    random.seed(int(seed))
    np.random.seed(int(seed))

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis("off")

    # 背景
    # 将 hex 转成 0-1 RGB
    def hex_to_rgb01(hexstr):
        hexstr = hexstr.lstrip("#")
        return tuple(int(hexstr[i:i+2], 16)/255.0 for i in (0, 2, 4))
    ax.set_facecolor(hex_to_rgb01(bg_color))

    # 调色板
    palette = pastel_palette(k=max(12, n_hearts), mood=mood, custom_hue=custom_hue,
                             hue_spread=hue_spread)

    # 绘制多个爱心
    for _ in range(n_hearts):
        cx, cy = random.random(), random.random()
        scale = random.uniform(size_min, size_max)
        rot = random.uniform(-math.pi/6, math.pi/6) if rotate else 0.0
        x, y = heart(center=(cx, cy), scale=scale, rotation=rot)

        color = random.choice(palette)
        alpha = random.uniform(alpha_min, alpha_max)

        # 阴影（先画阴影层）
        if add_shadow:
            sx = x + shadow_offset[0]
            sy = y + shadow_offset[1]
            ax.fill(sx, sy, color=(0, 0, 0), alpha=shadow_alpha, edgecolor=(0, 0, 0, 0))

        # 主体
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    if add_title:
        ax.text(0.05, 0.95, title_text, fontsize=20, weight="bold", transform=ax.transAxes)
        ax.text(0.05, 0.91, subtitle_text, fontsize=12, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout(pad=0)
    return fig

# ---------------- Streamlit UI ----------------
st.title("💗 Generative Hearts Poster")
st.caption("Soft & fresh palettes • randomized heart shapes • export as PNG")

# 侧边栏：基础
seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=10_000_000, value=42, step=1)
n_hearts = st.sidebar.slider("Number of Hearts", 4, 60, 18)
size_min, size_max = st.sidebar.slider("Heart Size Range", 0.04, 0.30, (0.08, 0.18))
alpha_min, alpha_max = st.sidebar.slider("Alpha Range", 0.10, 0.85, (0.25, 0.55))
bg_color = st.sidebar.color_picker("Background", value="#FAFAF7")

# 侧边栏：配色
mood = st.sidebar.selectbox("Palette Mood",
                            ["spring (mint/blush)", "sky (blue/lavender)", "peach (peach/cream)", "custom"])
if mood.startswith("spring"):
    mood_key = "spring"
elif mood.startswith("sky"):
    mood_key = "sky"
elif mood.startswith("peach"):
    mood_key = "peach"
else:
    mood_key = "custom"

if mood_key == "custom":
    custom_hue = st.sidebar.slider("Custom Hue Center (0~1)", 0.0, 1.0, 0.55, 0.01)
    hue_spread = st.sidebar.slider("Hue Spread", 0.0, 0.25, 0.10, 0.01)
else:
    custom_hue = 0.55
    hue_spread = 0.10

# 侧边栏：装饰
rotate = st.sidebar.checkbox("Slight Rotation Jitter", value=True)
add_shadow = st.sidebar.checkbox("Soft Shadow", value=True)

# 标题文本
add_title = st.sidebar.checkbox("Show Title", value=True)
title_text = st.sidebar.text_input("Title", value="Generative Hearts")
subtitle_text = st.sidebar.text_input("Subtitle", value="Soft & Fresh Palette")

# 生成与展示
fig = generate_poster(
    seed=seed,
    mood=mood_key,
    custom_hue=custom_hue,
    hue_spread=hue_spread,
    n_hearts=int(n_hearts),
    size_min=float(size_min),
    size_max=float(size_max),
    alpha_min=float(alpha_min),
    alpha_max=float(alpha_max),
    bg_color=bg_color,
    add_title=add_title,
    title_text=title_text,
    subtitle_text=subtitle_text,
    rotate=rotate,
    add_shadow=add_shadow
)
st.pyplot(fig)

# 下载
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
st.download_button(
    "Download PNG",
    data=buf.getvalue(),
    file_name=f"hearts_seed{int(seed)}.png",
    mime="image/png",
)
