import streamlit as st


def generate_poster(style="Vivid", seed=None, add_title=True):
if seed is not None:
random.seed(seed)
np.random.seed(seed)


fig, ax = plt.subplots(figsize=(7, 10))
ax.axis('off')
ax.set_facecolor((0.98, 0.98, 0.97))


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


for _ in range(n_layers):
cx, cy = random.random(), random.random()
rr = random.uniform(0.1, 0.3)
wobble = random.uniform(*wobble_range)
x, y = blob(center=(cx, cy), r=rr, wobble=wobble)
color = random.choice(palette)
alpha = random.uniform(0.25, 0.6)
ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))


if add_title:
ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)


ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
fig.tight_layout(pad=0)
return fig




# ---------------- UI ----------------
st.title("Generative Poster")
st.caption("Streamlit port of your Colab script — pick a style, seed and export as PNG.")


style = st.sidebar.selectbox("Style", ["Vivid", "Minimal", "NoiseTouch", "Default"])
seed = st.sidebar.number_input("Random Seed (optional)", min_value=0, max_value=10_000_000, value=42, step=1)
show_title = st.sidebar.checkbox("Show Title Text", value=True)


fig = generate_poster(style=style, seed=int(seed), add_title=show_title)


st.pyplot(fig)


buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
st.download_button(
"Download PNG",
data=buf.getvalue(),
file_name=f"poster_seed{int(seed)}.png",
mime="image/png",
)
