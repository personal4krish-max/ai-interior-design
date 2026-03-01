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

# ── GLOBAL CSS (Fixed for better mobile responsiveness) ──────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
/* Base Theme */
[data-testid="stAppViewContainer"] { background: #0a0a0f; font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0f1a 0%, #16162a 100%); border-right: 1px solid #2a2a4a; }

/* Gold Gradient Buttons */
.stButton > button {
    background: linear-gradient(135deg, #c9a84c, #f0d080, #c9a84c) !important;
    color: #0a0a0f !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    border: none !important;
    transition: 0.3s;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(201,168,76,0.4); }

/* Typography */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #f0e8d8 !important; }
.hero-title { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; line-height: 1.1; }
.gold-text { color: #c9a84c !important; }

/* Custom Components */
.feature-card {
    background: #12121f;
    border: 1px solid #252540;
    border-radius: 20px;
    padding: 1.5rem;
    transition: 0.3s;
}
.feature-card:hover { border-color: #c9a84c; }

.upi-id {
    font-family: 'Courier New', monospace;
    background: #000;
    color: #c9a84c;
    padding: 10px;
    border-radius: 5px;
    border: 1px dashed #c9a84c;
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
# CHANGE THIS TO YOUR UPI ID
UPI_ID = "9080599509@naviaxis" 
APP_NAME = "Nabi's DecorAI"

STYLES = ["Modern", "Minimalist", "Scandinavian", "Bohemian", "Industrial", "Japandi", "Rustic", "Art Deco"]
ROOM_TYPES = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Home Office", "Balcony"]
WALL_COLORS = {"Ivory White": "#FFFFF0", "Warm Beige": "#E8D5B0", "Sage Green": "#8FAF8F", "Navy Blue": "#1B3A6B", "Charcoal": "#3C3C3C"}

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def call_hf_api(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    # Using a more reliable stable diffusion model for interior design
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            st.error(f"Error: {response.status_code}. The AI is currently busy.")
            return None
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return None

def make_upi_qr(upi_id, amount=""):
    data = f"upi://pay?pa={upi_id}&pn=DecorAI&am={amount}&cu=INR"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="#c9a84c", back_color="#0a0a0f").convert("RGB")

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title(f"🏠 {APP_NAME}")
    nav = st.radio("Navigation", ["🏡 Home", "🛋️ Interior Design", "🎨 Wall Colors", "💎 Pricing"])
    
    st.markdown("---")
    hf_token = st.text_input("Hugging Face Token", type="password", help="Get it from huggingface.co/settings/tokens")
    if not hf_token:
        st.info("🔑 Please enter your API token to use AI features.")

# ── PAGES ────────────────────────────────────────────────────────────────────
if nav == "🏡 Home":
    st.markdown(f"""
    <div class='hero-badge'>✦ AI-Powered Interior Studio</div>
    <h1 class='hero-title'>Redesign Your <span class='gold-text'>Dream Home</span> In Seconds</h1>
    <p style='color:#9a8a78; font-size:1.2rem;'>Professional AI tools for homeowners and decorators.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-card'><h3>🛋️ Interior</h3><p>Change furniture and layouts instantly.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><h3>🎨 Colors</h3><p>Preview wall paints without the mess.</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'><h3>💎 Premium</h3><p>Get high-resolution 4K renders.</p></div>", unsafe_allow_html=True)

elif nav == "🛋️ Interior Design":
    st.subheader("🛋️ AI Interior Redesign")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Room Photo", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Original Room", use_container_width=True)
            
    with col2:
        room = st.selectbox("Room Type", ROOM_TYPES)
        style = st.selectbox("Design Style", STYLES)
        extra = st.text_area("Specific Instructions (e.g., 'Add a velvet sofa')", "")
        
        if st.button("✨ Generate New Design"):
            if not hf_token:
                st.warning("Please add your Hugging Face token in the sidebar.")
            else:
                with st.spinner("AI is painting your room..."):
                    prompt = f"High-end interior design of a {style} {room}, {extra}, hyper-realistic, 4k, architectural photography"
                    result = call_hf_api(prompt, hf_token)
                    if result:
                        st.image(result, caption="AI Redesign", use_container_width=True)
                        # Download Button
                        buf = io.BytesIO()
                        result.save(buf, format="PNG")
                        st.download_button("📥 Download Image", buf.getvalue(), "design.png", "image/png")

elif nav == "🎨 Wall Colors":
    st.subheader("🎨 Wall Color Visualizer")
    color_name = st.selectbox("Select Paint Color", list(WALL_COLORS.keys()))
    hex_code = WALL_COLORS[color_name]
    st.markdown(f"Selected: **{color_name}** (<span style='color:{hex_code}'>█</span> `{hex_code}`)", unsafe_allow_html=True)
    
    st.info("Feature Note: This tool currently uses AI to re-render the room with the chosen color palette.")

elif nav == "💎 Pricing":
    st.subheader("💎 Premium Plans")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='border: 2px solid #c9a84c;'>
            <h2 class='gold-text'>Pro Plan</h2>
            <p>₹299 / Month</p>
            <ul>
                <li>100 HD Renders</li>
                <li>All 12+ Styles</li>
                <li>No Watermark</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("### 💳 Quick Pay")
        st.write("Scan the QR code below to upgrade to Pro.")
        qr_img = make_upi_qr(UPI_ID, "299")
        st.image(qr_img, width=250)
        st.markdown(f"**UPI ID:** <span class='upi-id'>{UPI_ID}</span>", unsafe_allow_html=True)
        st.success("After payment, send the screenshot to support@decorai.in")

st.markdown("---")
st.caption("© 2026 DecorAI Studio - Powered by Streamlit & Stable Diffusion")
