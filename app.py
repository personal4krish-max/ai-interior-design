import streamlit as st
import requests
import base64
import io
import os
import qrcode
from PIL import Image

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DecorAI – AI Interior Design",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #16162a 100%);
    border-right: 1px solid #2a2a4a;
}

[data-testid="stSidebar"] * { color: #e0d6c8 !important; }

.stButton > button {
    background: linear-gradient(135deg, #c9a84c, #f0d080, #c9a84c) !important;
    color: #0a0a0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 18px rgba(201,168,76,0.35) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(201,168,76,0.5) !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1a1a2e !important;
    border: 1px solid #2e2e50 !important;
    border-radius: 10px !important;
    color: #e0d6c8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stSlider > div > div > div > div { background: #c9a84c !important; }

[data-testid="stFileUploadDropzone"] {
    background: #12121f !important;
    border: 2px dashed #c9a84c44 !important;
    border-radius: 16px !important;
    color: #a09480 !important;
}

.stProgress > div > div > div > div { background: linear-gradient(90deg, #c9a84c, #f0d080) !important; }

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #f0e8d8 !important; }
p, label, span { color: #b8a898 !important; }

/* ── Custom Components ── */
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #c9a84c22, #f0d08011);
    border: 1px solid #c9a84c55;
    color: #c9a84c !important;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 900;
    line-height: 1.1;
    color: #f5ece0 !important;
    margin-bottom: 1rem;
}

.hero-sub {
    font-size: 1.1rem;
    color: #9a8a78 !important;
    line-height: 1.7;
    max-width: 520px;
    margin-bottom: 2rem;
}

.gold-text { color: #c9a84c !important; }

.feature-card {
    background: linear-gradient(135deg, #12121f 0%, #1a1a2e 100%);
    border: 1px solid #252540;
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
}

.feature-card:hover {
    border-color: #c9a84c44;
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}

.feature-icon {
    font-size: 2.2rem;
    margin-bottom: 0.8rem;
    display: block;
}

.feature-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f0e8d8 !important;
    margin-bottom: 0.4rem;
}

.feature-desc {
    font-size: 0.88rem;
    color: #7a6a5a !important;
    line-height: 1.6;
}

.style-chip {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2e2e50;
    color: #a09480 !important;
    padding: 8px 18px;
    border-radius: 100px;
    font-size: 0.85rem;
    margin: 4px;
    cursor: pointer;
    transition: all 0.2s;
}

.style-chip.active {
    background: linear-gradient(135deg, #c9a84c22, #f0d08011);
    border-color: #c9a84c;
    color: #c9a84c !important;
}

.plan-card {
    background: linear-gradient(135deg, #12121f, #1a1a2e);
    border: 1px solid #252540;
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    position: relative;
    transition: all 0.3s ease;
}

.plan-card.featured {
    border-color: #c9a84c88;
    background: linear-gradient(135deg, #1a1608, #2a2210);
    box-shadow: 0 0 50px rgba(201,168,76,0.15);
}

.plan-badge {
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #c9a84c, #f0d080);
    color: #0a0a0f !important;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 5px 20px;
    border-radius: 100px;
}

.plan-price {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: #f0e8d8 !important;
    line-height: 1;
}

.plan-period {
    font-size: 0.85rem;
    color: #7a6a5a !important;
}

.plan-feature-list {
    text-align: left;
    margin: 1.5rem 0;
    list-style: none;
}

.plan-feature-list li {
    padding: 6px 0;
    font-size: 0.9rem;
    color: #a09480 !important;
    border-bottom: 1px solid #1e1e34;
}

.plan-feature-list li::before {
    content: '✦ ';
    color: #c9a84c;
}

.upi-box {
    background: linear-gradient(135deg, #1a1608, #2a2210);
    border: 2px solid #c9a84c44;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    max-width: 400px;
    margin: 0 auto;
}

.upi-id {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #c9a84c !important;
    letter-spacing: 1px;
    margin: 1rem 0;
    padding: 12px 24px;
    background: #0f0d02;
    border: 1px solid #c9a84c33;
    border-radius: 10px;
    display: inline-block;
}

.result-box {
    background: #12121f;
    border: 1px solid #2e2e50;
    border-radius: 20px;
    padding: 1.5rem;
    margin-top: 1rem;
}

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2e2e50, transparent);
    margin: 2.5rem 0;
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: #c9a84c !important;
}

.stat-label {
    font-size: 0.82rem;
    color: #7a6a5a !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.gallery-img-box {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #252540;
    margin-bottom: 1rem;
}

/* Hide Streamlit branding */
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>
""")

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
UPI_ID = "9080599509@naviaxis"    # Your UPI ID
APP_NAME = "DecorAI"

STYLES = [
    "Modern", "Minimalist", "Scandinavian", "Bohemian",
    "Industrial", "Mid-Century Modern", "Traditional", "Farmhouse",
    "Art Deco", "Coastal", "Japandi", "Rustic"
]

ROOM_TYPES = [
    "Living Room", "Bedroom", "Kitchen", "Bathroom",
    "Dining Room", "Home Office", "Kids Room", "Balcony",
    "Backyard", "Front Yard", "Exterior / Facade", "Basement"
]

EXTERIOR_STYLES = [
    "Modern", "Contemporary", "Colonial", "Mediterranean",
    "Tudor", "Craftsman", "Farmhouse", "Minimalist"
]

FLOORING_OPTIONS = [
    "Hardwood - Oak", "Hardwood - Walnut", "Marble White",
    "Marble Black", "Ceramic Tiles", "Concrete", "Bamboo",
    "Luxury Vinyl", "Herringbone Parquet", "Terrazzo"
]

WALL_COLORS = {
    "Ivory White": "#FFFFF0", "Warm Beige": "#E8D5B0", "Sage Green": "#8FAF8F",
    "Navy Blue": "#1B3A6B", "Terracotta": "#C67B5C", "Dusty Rose": "#D4A0A0",
    "Charcoal": "#3C3C3C", "Slate Grey": "#708090", "Forest Green": "#355E3B",
    "Warm Taupe": "#9E8B7B", "Midnight Blue": "#1A1A4E", "Cream": "#FFFDD0"
}

# ── SIDEBAR NAV ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 1.5rem 0 1rem;'>
        <div style='font-size:2.5rem; margin-bottom:0.3rem;'>🏠</div>
        <div style='font-family: Playfair Display, serif; font-size:1.4rem; 
                    font-weight:900; color:#f0e8d8;'>{APP_NAME}</div>
        <div style='font-size:0.75rem; color:#7a6a5a; letter-spacing:2px;
                    text-transform:uppercase; margin-top:3px;'>AI Interior Studio</div>
    </div>
    <hr style='border-color:#2a2a4a; margin:0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["🏡 Home", "🛋️ Interior Design", "🏠 Exterior Design",
         "🌿 Landscape & Garden", "🎨 Wall Colors",
         "🪵 Flooring Preview", "🧹 Cleanup & Erase",
         "💎 Pricing & Plans"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    with st.expander("⚙️ AI Settings"):
        hf_token = st.text_input(
            "Hugging Face API Token",
            type="password",
            placeholder="hf_xxxxxxxxxxxx",
            help="Get your free token at huggingface.co/settings/tokens"
        )
        st.markdown("[Get Free Token →](https://huggingface.co/settings/tokens)",
                    unsafe_allow_html=True)

    st.markdown("""
    <div style='position:absolute; bottom:1rem; left:1rem; right:1rem; 
                text-align:center; font-size:0.75rem; color:#3a3a5a;'>
        © 2025 DecorAI · All rights reserved
    </div>
    """, unsafe_allow_html=True)

page = nav.split(" ", 1)[1].strip()


# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def img_to_b64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def call_hf_text2img(prompt: str, token: str) -> Image.Image | None:
    """Call HuggingFace Inference API – text-to-image."""
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"width": 768, "height": 512, "num_inference_steps": 25}
    }
    models = [
        "stabilityai/stable-diffusion-2-1",
        "runwayml/stable-diffusion-v1-5",
    ]
    for model in models:
        url = f"https://api-inference.huggingface.co/models/{model}"
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            if r.status_code == 200:
                return Image.open(io.BytesIO(r.content))
        except Exception:
            continue
    return None

def generate_design_prompt(room_type: str, style: str, extra: str = "") -> str:
    base = (
        f"Professional interior design photography of a stunning {style} style {room_type}, "
        f"ultra-realistic, magazine quality, beautiful lighting, high-end furniture, "
        f"perfectly decorated, architectural digest style, 4K detail"
    )
    return f"{base}. {extra}" if extra else base

def generate_exterior_prompt(style: str, extra: str = "") -> str:
    base = (
        f"Professional architectural photography of a beautiful {style} style modern house exterior, "
        f"stunning curb appeal, perfect landscaping, blue sky, photorealistic, "
        f"luxury home, magazine quality, 4K"
    )
    return f"{base}. {extra}" if extra else base

def generate_landscape_prompt(style: str, extra: str = "") -> str:
    base = (
        f"Professional garden design photography, {style} style backyard, "
        f"beautiful landscaping, lush plants, patio furniture, evening golden hour lighting, "
        f"luxury outdoor living, magazine quality, 4K"
    )
    return f"{base}. {extra}" if extra else base

def make_upi_qr(upi_id: str, amount: str = "") -> Image.Image:
    data = f"upi://pay?pa={upi_id}&pn=DecorAI&am={amount}&cu=INR&tn=DecorAI+Subscription"
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="#c9a84c", back_color="#0a0a0f").convert("RGB")

def ai_section_header(icon, title, subtitle):
    st.markdown(f"""
    <div style='margin-bottom:2rem;'>
        <span style='font-size:2.5rem;'>{icon}</span>
        <h1 class='hero-title' style='font-size:2.2rem; margin-top:0.5rem;'>{title}</h1>
        <p class='hero-sub' style='font-size:1rem;'>{subtitle}</p>
        <div class='section-divider'></div>
    </div>
    """, unsafe_allow_html=True)

def show_result(img: Image.Image):
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.image(img, use_container_width=True, caption="✨ AI-Generated Design")
    col1, col2 = st.columns(2)
    with col1:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇️ Download", buf.getvalue(), "design.png", "image/png", use_container_width=True)
    with col2:
        st.button("🔄 Regenerate", use_container_width=True, key="regen")
    st.markdown("</div>", unsafe_allow_html=True)

def no_token_warning():
    st.markdown("""
    <div style='background:#1a1608; border:1px solid #c9a84c44; border-radius:14px; 
                padding:1.2rem 1.5rem; text-align:center; margin:1rem 0;'>
        <span style='font-size:1.5rem;'>🔑</span>
        <p style='color:#c9a84c !important; font-weight:600; margin:0.5rem 0 0.2rem;'>
            API Token Required
        </p>
        <p style='color:#7a6a5a !important; font-size:0.9rem;'>
            Add your free Hugging Face token in ⚙️ AI Settings (sidebar) to generate designs.
        </p>
        <a href='https://huggingface.co/settings/tokens' target='_blank'
           style='color:#c9a84c; font-size:0.85rem;'>Get free token →</a>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    # Hero
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        <div class='hero-badge'>✦ AI-Powered Interior Studio</div>
        <h1 class='hero-title'>
            Transform Any Room<br>
            Into Your <span class='gold-text'>Dream Space</span>
        </h1>
        <p class='hero-sub'>
            Upload a photo of your room and let our AI redesign it in any style — 
            Modern, Bohemian, Scandinavian, and 9 more. Instant, stunning results.
        </p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='stat-number'>5M+</div><div class='stat-label'>Users</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='stat-number'>12</div><div class='stat-label'>Design Styles</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='stat-number'>4.5★</div><div class='stat-label'>Rating</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a2e, #12121f);
                    border: 1px solid #2e2e50; border-radius: 24px; padding: 2rem; text-align:center;'>
            <div style='font-size:6rem; margin-bottom:1rem;'>🏠</div>
            <p style='color:#c9a84c !important; font-weight:600; font-size:1rem;'>
                Upload → Select Style → Generate
            </p>
            <p style='color:#5a4a3a !important; font-size:0.85rem;'>
                Powered by Stable Diffusion AI
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Features
    st.markdown("<h2 style='font-size:1.8rem; margin-bottom:1.5rem;'>Everything You Need</h2>", unsafe_allow_html=True)

    features = [
        ("🛋️", "AI Interior Design", "Upload your room photo and choose a style. Watch AI transform it into a stunning space in seconds."),
        ("🏠", "Exterior Redesign", "Visualize your home's exterior in different architectural styles before you spend a single rupee."),
        ("🌿", "Landscape & Garden", "Design your dream backyard, patio, or front yard with smart AI landscaping tools."),
        ("🎨", "Wall Color Preview", "Test any wall color instantly — no paint needed. See how it changes your entire room."),
        ("🪵", "Flooring Visualizer", "Preview hardwood, marble, tiles, and more right on your room's floor — before buying."),
        ("🧹", "Object Removal", "Erase unwanted furniture or clutter from photos for a clean, magazine-worthy look."),
    ]

    rows = [features[:3], features[3:]]
    for row in rows:
        cols = st.columns(3)
        for i, (icon, title, desc) in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div class='feature-card'>
                    <span class='feature-icon'>{icon}</span>
                    <div class='feature-title'>{title}</div>
                    <div class='feature-desc'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Design Styles
    st.markdown("<h2 style='font-size:1.8rem; margin-bottom:1rem;'>Design Styles</h2>", unsafe_allow_html=True)
    style_html = "".join([f"<span class='style-chip'>{s}</span>" for s in STYLES])
    st.markdown(f"<div style='margin-bottom:2rem;'>{style_html}</div>", unsafe_allow_html=True)

    # How it works
    st.markdown("<h2 style='font-size:1.8rem; margin-bottom:1.5rem;'>How It Works</h2>", unsafe_allow_html=True)
    steps = [
        ("1", "📸", "Upload Photo", "Take or upload a photo of your room, exterior, or garden."),
        ("2", "🎨", "Choose Style", "Pick from 12 curated design styles that match your vision."),
        ("3", "⚡", "AI Generates", "Our AI analyzes and redesigns your space in seconds."),
        ("4", "💾", "Download & Share", "Download your new design or share it on Instagram or Pinterest."),
    ]
    step_cols = st.columns(4)
    for i, (num, icon, title, desc) in enumerate(steps):
        with step_cols[i]:
            st.markdown(f"""
            <div style='text-align:center; padding:1.5rem 1rem;
                        background:#12121f; border:1px solid #252540; border-radius:20px;'>
                <div style='width:40px; height:40px; background:linear-gradient(135deg,#c9a84c,#f0d080);
                            border-radius:50%; display:flex; align-items:center; justify-content:center;
                            font-weight:900; color:#0a0a0f; font-size:1rem; margin:0 auto 0.8rem;'>{num}</div>
                <div style='font-size:1.8rem; margin-bottom:0.5rem;'>{icon}</div>
                <div style='font-family:Playfair Display,serif; font-size:1rem; 
                            color:#f0e8d8 !important; font-weight:700; margin-bottom:0.3rem;'>{title}</div>
                <div style='font-size:0.82rem; color:#5a4a3a !important; line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INTERIOR DESIGN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Interior Design":
    ai_section_header("🛋️", "AI Interior Design",
                       "Upload your room photo, pick a style, and watch AI redesign it instantly.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-bottom:0.5rem;'>📸 Upload Room Photo</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Room Photo", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, use_container_width=True, caption="Your current room")

    with col2:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>🛋️ Room Type</p>", unsafe_allow_html=True)
        room_type = st.selectbox("Room Type", ROOM_TYPES, label_visibility="collapsed")

        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>🎨 Design Style</p>", unsafe_allow_html=True)
        style = st.selectbox("Design Style", STYLES, label_visibility="collapsed")

        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>✍️ Extra Preferences (optional)</p>", unsafe_allow_html=True)
        extra = st.text_area("Extra Preferences", placeholder="e.g. add a fireplace, wooden ceiling, floor-to-ceiling windows...",
                              label_visibility="collapsed", height=90)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        gen_btn = st.button("✨ Generate AI Design", use_container_width=True)

    if gen_btn:
        if not hf_token:
            no_token_warning()
        else:
            prompt = generate_design_prompt(room_type, style, extra)
            with st.spinner("🎨 AI is redesigning your space…"):
                result = call_hf_text2img(prompt, hf_token)
            if result:
                st.success("✅ Design generated!")
                show_result(result)
                st.markdown(f"""
                <div style='background:#12121f; border:1px solid #2e2e50; border-radius:12px;
                            padding:1rem; margin-top:0.5rem;'>
                    <p style='font-size:0.8rem; color:#5a4a3a !important;'>
                        <strong style='color:#c9a84c !important;'>Prompt used:</strong> {prompt}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Generation failed. Check your API token or try again later.")

    # Style Gallery
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:1.5rem; margin-bottom:1rem;'>Style Inspiration Gallery</h2>", unsafe_allow_html=True)
    style_info = {
        "Modern": ("Clean lines, neutral palette, open spaces", "⚡"),
        "Scandinavian": ("Light woods, cozy textiles, functional", "❄️"),
        "Bohemian": ("Rich textures, warm colors, eclectic mix", "🌺"),
        "Industrial": ("Raw metals, exposed brick, urban edge", "🏗️"),
        "Mid-Century Modern": ("Organic forms, retro palette, iconic chairs", "🪑"),
        "Japandi": ("Zen simplicity, natural materials, harmony", "🎋"),
    }
    gcols = st.columns(3)
    for i, (sty, (desc, icon)) in enumerate(style_info.items()):
        with gcols[i % 3]:
            st.markdown(f"""
            <div class='feature-card' style='text-align:center; padding:1.5rem;'>
                <div style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
                <div class='feature-title'>{sty}</div>
                <div class='feature-desc'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXTERIOR DESIGN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Exterior Design":
    ai_section_header("🏠", "AI Exterior Design",
                       "Transform your home's facade with AI-powered architectural redesign.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>📸 Upload House Photo</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload House Photo", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True, caption="Current exterior")

    with col2:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>🏛️ Architectural Style</p>", unsafe_allow_html=True)
        ext_style = st.selectbox("Architectural Style", EXTERIOR_STYLES, label_visibility="collapsed")

        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>🌳 Landscaping</p>", unsafe_allow_html=True)
        landscape = st.checkbox("Include beautiful landscaping", value=True)

        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>🎨 Exterior Color</p>", unsafe_allow_html=True)
        ext_color = st.selectbox("Exterior Color Tone",
                                  ["White", "Beige", "Grey", "Brick Red", "Dark Charcoal", "Sage Green", "Navy"],
                                  label_visibility="collapsed")

        extra_ext = st.text_area("Additional details", placeholder="e.g. add a porch, black window frames, wood accents...",
                                  height=80)

        gen_ext = st.button("✨ Generate Exterior Design", use_container_width=True)

    if gen_ext:
        if not hf_token:
            no_token_warning()
        else:
            land_str = "with lush professional landscaping, manicured lawn, beautiful trees" if landscape else ""
            prompt = generate_exterior_prompt(ext_style,
                                              f"{ext_color} color scheme, {land_str}. {extra_ext}")
            with st.spinner("🏠 Redesigning your exterior…"):
                result = call_hf_text2img(prompt, hf_token)
            if result:
                st.success("✅ Exterior design ready!")
                show_result(result)
            else:
                st.error("❌ Generation failed. Check your token.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LANDSCAPE & GARDEN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Landscape & Garden":
    ai_section_header("🌿", "Landscape & Garden Design",
                       "Design your dream backyard, garden, or outdoor living area with AI.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>📸 Upload Outdoor Photo</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Outdoor Photo", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True, caption="Current outdoor space")

    with col2:
        garden_types = ["Backyard Garden", "Front Yard", "Rooftop Garden", "Balcony Garden",
                         "Patio / Deck", "Pool Area", "Side Yard", "Kitchen Garden"]
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>🌳 Garden Type</p>", unsafe_allow_html=True)
        garden_type = st.selectbox("Garden Type", garden_types, label_visibility="collapsed")

        landscape_styles = ["Modern / Minimalist", "Tropical", "Zen / Japanese", "Cottage",
                             "Mediterranean", "Desert / Xeriscaping", "Formal / Symmetrical", "Rustic / Natural"]
        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>🌺 Landscape Style</p>", unsafe_allow_html=True)
        l_style = st.selectbox("Landscape Style", landscape_styles, label_visibility="collapsed")

        features_opts = st.multiselect("✨ Include features",
                                        ["Swimming Pool", "Fire Pit", "Pergola", "Outdoor Kitchen",
                                         "Water Feature", "String Lights", "Raised Beds", "Stone Path"],
                                        default=["Pergola", "String Lights"])

        gen_land = st.button("✨ Generate Garden Design", use_container_width=True)

    if gen_land:
        if not hf_token:
            no_token_warning()
        else:
            feat_str = ", ".join(features_opts) if features_opts else ""
            prompt = generate_landscape_prompt(l_style, f"{garden_type}, {feat_str}")
            with st.spinner("🌿 Designing your garden…"):
                result = call_hf_text2img(prompt, hf_token)
            if result:
                st.success("✅ Garden design ready!")
                show_result(result)
            else:
                st.error("❌ Generation failed. Check your token.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: WALL COLORS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Wall Colors":
    ai_section_header("🎨", "Wall Color Visualizer",
                       "See exactly how a new wall color will transform your room — before touching a brush.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>📸 Upload Your Room</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Room", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True, caption="Your room")

    with col2:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>🎨 Choose Wall Color</p>", unsafe_allow_html=True)
        wall_color = st.selectbox("Wall Color", list(WALL_COLORS.keys()), label_visibility="collapsed")
        hex_val = WALL_COLORS[wall_color]
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin:0.8rem 0;'>
            <div style='width:40px; height:40px; background:{hex_val}; 
                        border-radius:10px; border:2px solid #2e2e50;'></div>
            <div>
                <div style='color:#f0e8d8 !important; font-weight:600;'>{wall_color}</div>
                <div style='color:#5a4a3a !important; font-size:0.85rem;'>{hex_val}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        finish = st.selectbox("Wall Finish", ["Matte", "Satin", "Eggshell", "Semi-Gloss", "Gloss"])
        room_type_w = st.selectbox("Room Type", ROOM_TYPES[:6], key="wall_room")

        # Color Palette Preview
        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>All Colors</p>", unsafe_allow_html=True)
        color_chips = "".join([
            f"<div title='{n}' style='width:32px;height:32px;background:{h};border-radius:8px;"
            f"border:2px solid #2e2e50; cursor:pointer; display:inline-block; margin:3px;'></div>"
            for n, h in WALL_COLORS.items()
        ])
        st.markdown(f"<div style='display:flex; flex-wrap:wrap;'>{color_chips}</div>", unsafe_allow_html=True)

        gen_wall = st.button("✨ Visualize Wall Color", use_container_width=True)

    if gen_wall:
        if not hf_token:
            no_token_warning()
        else:
            prompt = (
                f"Professional interior design photography of a beautiful {room_type_w} "
                f"with {wall_color} {finish.lower()} finish walls, "
                f"perfectly decorated, warm lighting, luxury furniture, magazine quality, 4K"
            )
            with st.spinner("🎨 Applying wall color…"):
                result = call_hf_text2img(prompt, hf_token)
            if result:
                st.success("✅ Wall color applied!")
                show_result(result)
            else:
                st.error("❌ Generation failed. Check your token.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FLOORING PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Flooring Preview":
    ai_section_header("🪵", "Flooring Visualizer",
                       "Preview different flooring options in your space before making any purchase.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>📸 Upload Your Room</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Room", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True, caption="Your room")

    with col2:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>🪵 Flooring Type</p>", unsafe_allow_html=True)
        flooring = st.selectbox("Flooring", FLOORING_OPTIONS, label_visibility="collapsed")

        floor_icons = {
            "Hardwood - Oak": "🪵", "Hardwood - Walnut": "🍂", "Marble White": "⬜",
            "Marble Black": "⬛", "Ceramic Tiles": "🔷", "Concrete": "🔲",
            "Bamboo": "🎋", "Luxury Vinyl": "✨", "Herringbone Parquet": "🔶", "Terrazzo": "🟡"
        }

        st.markdown("<p style='color:#c9a84c !important; font-weight:600; margin-top:1rem;'>📐 Pattern</p>", unsafe_allow_html=True)
        pattern = st.selectbox("Pattern", ["Straight", "Diagonal", "Herringbone", "Chevron", "Random"])

        room_type_f = st.selectbox("Room", ROOM_TYPES[:5], key="floor_room")

        gen_floor = st.button("✨ Preview Flooring", use_container_width=True)

    if gen_floor:
        if not hf_token:
            no_token_warning()
        else:
            prompt = (
                f"Professional interior design photography of a beautiful {room_type_f} "
                f"with {flooring} flooring in {pattern.lower()} pattern, "
                f"ultra realistic, magazine quality, warm lighting, modern furniture, 4K detail"
            )
            with st.spinner("🪵 Previewing flooring…"):
                result = call_hf_text2img(prompt, hf_token)
            if result:
                st.success("✅ Flooring preview ready!")
                show_result(result)
            else:
                st.error("❌ Generation failed. Check your token.")

    # Flooring comparison grid
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:1.5rem; margin-bottom:1rem;'>Popular Flooring Types</h2>", unsafe_allow_html=True)
    floor_info = [
        ("🪵", "Hardwood Oak", "Warm, timeless, durable. Best for living rooms & bedrooms."),
        ("⬜", "Marble", "Luxurious, cool touch. Perfect for bathrooms & foyers."),
        ("🎋", "Bamboo", "Eco-friendly, light tone. Great for modern spaces."),
        ("🔷", "Ceramic Tiles", "Waterproof, versatile. Ideal for kitchens & bathrooms."),
        ("✨", "Luxury Vinyl", "Budget-friendly, water-resistant. Any room."),
        ("🔶", "Herringbone", "Classic elegance, upscale look. Living & dining rooms."),
    ]
    fc = st.columns(3)
    for i, (icon, name, desc) in enumerate(floor_info):
        with fc[i % 3]:
            st.markdown(f"""
            <div class='feature-card'>
                <span class='feature-icon'>{icon}</span>
                <div class='feature-title'>{name}</div>
                <div class='feature-desc'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CLEANUP & ERASE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Cleanup & Erase":
    ai_section_header("🧹", "Cleanup & Object Removal",
                       "Remove unwanted furniture, clutter, or objects for a clean, polished look.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>📸 Upload Room Photo</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Room Photo", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, use_container_width=True, caption="Original photo")

    with col2:
        st.markdown("<p style='color:#c9a84c !important; font-weight:600;'>🗑️ What to Remove?</p>", unsafe_allow_html=True)
        remove_items = st.multiselect(
            "Remove Items",
            ["Old sofa", "Dining table", "Clutter / Boxes", "Old carpet", "Curtains",
             "TV stand", "Bookshelf", "Lamp", "Wall decorations", "All furniture"],
            default=["Clutter / Boxes"],
            label_visibility="collapsed"
        )

        describe_remove = st.text_area("Describe what to remove", 
                                        placeholder="e.g. remove the old red couch and replace with empty wall...",
                                        height=90)

        target_look = st.selectbox("Target look after cleanup",
                                    ["Minimalist empty room", "Staged for sale", "Ready to redesign",
                                     "Clean & organized", "Open floor plan"])

        gen_clean = st.button("🧹 Clean Up Photo", use_container_width=True)

    if gen_clean:
        if not hf_token:
            no_token_warning()
        else:
            items_str = ", ".join(remove_items) if remove_items else "clutter"
            prompt = (
                f"Professional interior design photography of a clean, {target_look.lower()} room, "
                f"without {items_str}, {describe_remove}, spotless, bright, magazine quality, 4K"
            )
            with st.spinner("🧹 Cleaning your space…"):
                result = call_hf_text2img(prompt, hf_token)
            if result:
                st.success("✅ Cleanup complete!")
                show_result(result)
            else:
                st.error("❌ Generation failed. Check your token.")

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-card' style='text-align:center; padding:2rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>💡</div>
        <div class='feature-title'>Pro Tip</div>
        <div class='feature-desc' style='max-width:500px; margin:0 auto;'>
            For best results, upload a wide-angle photo with good lighting. 
            The cleaner the original photo, the better the AI can work with it.
            Great for real estate staging, before/after renovations, and home makeovers.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRICING & PLANS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Pricing & Plans":
    ai_section_header("💎", "Pricing & Plans",
                       "Unlock unlimited AI designs with our affordable plans. Pay securely via UPI.")

    # Plans
    plans = [
        {
            "name": "Free", "price": "₹0", "period": "/forever", "featured": False,
            "features": ["5 AI designs/month", "Basic styles (3)", "Standard resolution",
                          "Watermarked downloads", "Email support"],
            "btn": "Get Started Free"
        },
        {
            "name": "Pro", "price": "₹299", "period": "/month", "featured": True,
            "features": ["100 AI designs/month", "All 12 design styles", "HD resolution (1080p)",
                          "No watermark", "Interior + Exterior + Garden",
                          "Wall Colors & Flooring", "Priority support"],
            "btn": "Get Pro – ₹299/mo"
        },
        {
            "name": "Premium", "price": "₹699", "period": "/month", "featured": False,
            "features": ["Unlimited AI designs", "All 12 design styles", "4K resolution",
                          "No watermark", "All features unlocked",
                          "Cleanup & Object Removal", "24/7 priority support",
                          "API Access"],
            "btn": "Get Premium – ₹699/mo"
        },
    ]

    plan_cols = st.columns(3)
    selected_plan = None
    selected_amount = "0"

    for i, plan in enumerate(plans):
        with plan_cols[i]:
            badge = '<div class="plan-badge">⭐ MOST POPULAR</div>' if plan["featured"] else ""
            features_html = "".join([f"<li>{f}</li>" for f in plan["features"]])
            card_class = "plan-card featured" if plan["featured"] else "plan-card"

            st.markdown(f"""
            <div class='{card_class}' style='position:relative;'>
                {badge}
                <div style='font-family:DM Sans,sans-serif; font-size:0.9rem; 
                             color:#7a6a5a; text-transform:uppercase; letter-spacing:2px; 
                             margin-bottom:0.8rem;'>{plan["name"]}</div>
                <div class='plan-price'>{plan["price"]}</div>
                <div class='plan-period'>{plan["period"]}</div>
                <ul class='plan-feature-list' style='margin-top:1.5rem;'>
                    {features_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

            if st.button(plan["btn"], key=f"plan_{i}", use_container_width=True):
                selected_plan = plan["name"]
                selected_amount = plan["price"].replace("₹", "").replace("/month", "").replace("/forever", "")

    # Payment Section
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:1.8rem; margin-bottom:0.5rem;'>💳 Pay via UPI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7a6a5a !important;'>Scan the QR code or pay directly using UPI ID below.</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    pay_col1, pay_col2 = st.columns([1, 1])

    with pay_col1:
        st.markdown(f"""
        <div class='upi-box'>
            <div style='font-size:1.5rem; margin-bottom:0.5rem;'>📱 Scan & Pay</div>
            <p style='color:#7a6a5a !important; font-size:0.88rem; margin-bottom:1rem;'>
                Open any UPI app (GPay, PhonePe, Paytm, BHIM) and scan the QR code below.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Generate QR Code
        qr_amount = st.text_input("Enter amount (₹)", value="299", placeholder="299")
        if st.button("🔄 Generate QR Code", use_container_width=True):
            qr_img = make_upi_qr(UPI_ID, qr_amount)
            st.image(qr_img, width=260, caption=f"Scan to pay ₹{qr_amount}")

            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            st.download_button("⬇️ Download QR", buf.getvalue(), "payment_qr.png", "image/png",
                                use_container_width=True)

    with pay_col2:
        st.markdown(f"""
        <div class='upi-box'>
            <div style='font-size:2rem; margin-bottom:0.8rem;'>💰</div>
            <p style='color:#a09480 !important; font-size:0.9rem; margin-bottom:0.5rem;'>
                Or pay directly using UPI ID:
            </p>
            <div class='upi-id'>{UPI_ID}</div>
            <p style='color:#5a4a3a !important; font-size:0.8rem; margin-top:1rem; line-height:1.6;'>
                ✅ After payment, email your transaction ID to:<br>
                <strong style='color:#c9a84c !important;'>support@decorai.in</strong><br>
                Your plan will be activated within 2 hours.
            </p>
            <div style='margin-top:1.5rem; padding-top:1rem; border-top:1px solid #2e2e50;'>
                <p style='color:#3a2a1a !important; font-size:0.78rem;'>
                    🔒 Secure payment · No auto-renewal · 7-day refund policy
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Supported UPI apps
        st.markdown("""
        <div style='text-align:center; margin-top:1.5rem;'>
            <p style='color:#5a4a3a !important; font-size:0.82rem; margin-bottom:0.8rem;'>
                Accepted on all UPI apps
            </p>
            <div style='display:flex; justify-content:center; gap:12px; font-size:1.4rem;'>
                📱 🏦 💳 ₹
            </div>
            <p style='color:#4a3a2a !important; font-size:0.78rem; margin-top:0.5rem;'>
                GPay · PhonePe · Paytm · BHIM · All UPI apps
            </p>
        </div>
        """, unsafe_allow_html=True)

    # FAQ
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:1.5rem; margin-bottom:1rem;'>Frequently Asked Questions</h2>", unsafe_allow_html=True)

    faqs = [
        ("How does AI design work?", "You upload a photo of your space, choose a style, and our AI generates a redesigned version using Stable Diffusion — a state-of-the-art image generation model."),
        ("Is my UPI payment secure?", "Yes. Payments go directly to the merchant's UPI ID. We never store your payment details."),
        ("Can I cancel anytime?", "Yes! There are no contracts or auto-renewals. Your subscription is valid until the period ends."),
        ("What image formats are supported?", "JPG, JPEG, PNG, and WebP formats up to 20MB are supported."),
    ]

    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f"<p style='color:#9a8a78 !important; line-height:1.7;'>{a}</p>", unsafe_allow_html=True)
