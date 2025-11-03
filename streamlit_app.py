import streamlit as st
import random, math, colorsys, io
import numpy as np
import matplotlib.pyplot as plt

# ---------------- 页面配置 ----------------
st.set_page_config(page_title="Generative Poster", layout="centered")

# ---------------- 生成颜色与形状函数 ----------------
def random_palette(k=15, mode="pastel"):
    colors = []
    for _ in range(k):
        if mode == "vivid":
            h = random.random()
            s, v = 1, 1
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            colors.append((r, g, b))
        else:
            base = np.array([random.random(), random.random(), random.random()])
            pastel = (base + np.array([1, 1, 1])) / 2
            colors.append(tuple(pastel))
    return colors


def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ---------------- 生成海报函数 ----------------
def generate_poster(style="Vivid", seed=None, add_title=True):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')
    ax.set_facecolor((0.98, 0.98, 0.97))

    # 根据风格选择参数
    if style == "Minimal":
        n_layers = 5
        wobble_range = (0.01, 0.1)
        palette_mode = "pastel"
    elif style == "Vivid":
        n_layers = 12
        wobble_range = (0.2, 0.5)
        palette_mode = "vivid"
    elif style == "NoiseTouch":
        n_layers = 10
        wobble_range = (0.3, 0.7)
        palette_mode = "vivid"
    else:
        n_layers = 7
        wobble_range = (0.05, 0.3)
        palette_mode = "pastel"

    palette = random_palette(15, mode=palette_mode)

    # 绘制层叠形状
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.1, 0.3)
        wobble = random.uniform(*wobble_range)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    # 添加标题文字
    if add_title:
        ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
        ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout(pad=0)
    return fig

# ---------------- Streamlit 页面 UI ----------------
st.title("🎨 Generative Poster")
st.caption("Streamlit version of your Colab generative art project")

style = st.sidebar.selectbox("Select Style", ["Vivid", "Minimal", "NoiseTouch", "Default"])
seed = st.sidebar.number_input("Random Seed (optional)", min_value=0, max_value=10_000_000, value=42, step=1)
show_title = st.sidebar.checkbox("Show Title Text", value=True)

fig = generate_poster(style=style, seed=int(seed), add_title=show_title)
st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
st.download_button(
    "Download Poster as PNG",
    data=buf.getvalue(),
    file_name=f"poster_seed{int(seed)}.png",
    mime="image/png",
)
